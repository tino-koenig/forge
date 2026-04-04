from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from core.capability_model import Capability, CommandRequest
from core.effects import ExecutionSession
from core.output_contracts import build_contract, emit_contract_json
from core.protocol_log import events_log_path, load_protocol_events


def _parse_iso(value: object) -> datetime:
    if not isinstance(value, str):
        return datetime.min.replace(tzinfo=timezone.utc)
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _parse_iso_filter(value: object, *, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"invalid {field} filter: expected ISO-8601 timestamp")
    parsed = _parse_iso(value)
    if parsed == datetime.min.replace(tzinfo=timezone.utc):
        raise ValueError(f"invalid {field} filter: expected ISO-8601 timestamp")
    return parsed


def _sort_events(events: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(events, key=lambda item: _parse_iso(item.get("timestamp")))


def _safe_int(value: object) -> int | None:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _terminal_duration(event: dict[str, object]) -> int:
    duration = event.get("duration_ms")
    if isinstance(duration, int) and duration >= 0:
        return duration
    return 0


def _provider_of(event: dict[str, object]) -> str | None:
    metadata = event.get("metadata")
    if not isinstance(metadata, dict):
        return None
    provider = metadata.get("provider")
    if isinstance(provider, str) and provider.strip():
        return provider.strip()
    return None


def _model_of(event: dict[str, object]) -> str | None:
    metadata = event.get("metadata")
    if not isinstance(metadata, dict):
        return None
    model = metadata.get("model")
    if isinstance(model, str) and model.strip():
        return model.strip()
    return None


def _event_line(event: dict[str, object]) -> str:
    ts = str(event.get("timestamp") or "unknown-ts")
    run_id = event.get("run_id")
    step = str(event.get("step_name") or "unknown_step")
    step_type = str(event.get("step_type") or "deterministic")
    status = str(event.get("status") or "unknown")
    duration = event.get("duration_ms")
    duration_txt = f"{duration}ms" if isinstance(duration, int) else "-"
    prefix = "!" if status in {"failed", "fallback"} else "-"
    return f"{prefix} {ts} | run={run_id} | {step} [{step_type}] | {status} | {duration_txt}"


def _parse_logs_command(parts: list[str]) -> tuple[str, int | None, str | None]:
    # returns (action, run_id_or_count, event_id)
    if not parts:
        return "tail", 20, None
    first = parts[0].lower()
    if first == "tail":
        if len(parts) >= 2:
            count = _safe_int(parts[1])
            if count is None or count <= 0:
                raise ValueError("Usage: forge logs tail [count>0]")
            return "tail", count, None
        return "tail", 20, None
    if first == "run":
        if len(parts) < 2:
            raise ValueError("Usage: forge logs run <run_id>")
        run_id = _safe_int(parts[1])
        if run_id is None or run_id <= 0:
            raise ValueError("Usage: forge logs run <run_id>")
        return "run", run_id, None
    if first == "show":
        if len(parts) < 2:
            raise ValueError("Usage: forge logs show <event_id>")
        event_id = parts[1].strip()
        if not event_id:
            raise ValueError("Usage: forge logs show <event_id>")
        return "show", None, event_id
    if first == "stats":
        return "stats", None, None
    raise ValueError("Usage: forge logs [tail [count] | run <run_id> | show <event_id> | stats]")


def _apply_filters(events: list[dict[str, object]], args) -> list[dict[str, object]]:
    filtered = list(events)
    since_raw = getattr(args, "since", None)
    until_raw = getattr(args, "until", None)
    since = _parse_iso_filter(since_raw, field="--since") if since_raw is not None else None
    until = _parse_iso_filter(until_raw, field="--until") if until_raw is not None else None
    if since is not None and until is not None and since > until:
        raise ValueError("invalid time filters: --since must be <= --until")

    run_id_filter = getattr(args, "logs_run_id", None)
    if run_id_filter is not None:
        filtered = [item for item in filtered if _safe_int(item.get("run_id")) == int(run_id_filter)]
    capability_filter = getattr(args, "logs_capability", None)
    if isinstance(capability_filter, str) and capability_filter.strip():
        cap = capability_filter.strip().lower()
        filtered = [item for item in filtered if str(item.get("capability", "")).lower() == cap]
    step_type_filter = getattr(args, "logs_step_type", None)
    if isinstance(step_type_filter, str) and step_type_filter.strip():
        st = step_type_filter.strip().lower()
        filtered = [item for item in filtered if str(item.get("step_type", "")).lower() == st]
    status_filter = getattr(args, "logs_status", None)
    if isinstance(status_filter, str) and status_filter.strip():
        st = status_filter.strip().lower()
        filtered = [item for item in filtered if str(item.get("status", "")).lower() == st]
    provider_filter = getattr(args, "logs_provider", None)
    if isinstance(provider_filter, str) and provider_filter.strip():
        provider_norm = provider_filter.strip().lower()
        filtered = [
            item for item in filtered if (_provider_of(item) or "").lower() == provider_norm
        ]
    model_filter = getattr(args, "logs_model", None)
    if isinstance(model_filter, str) and model_filter.strip():
        model_norm = model_filter.strip().lower()
        filtered = [item for item in filtered if (_model_of(item) or "").lower() == model_norm]
    if since is not None:
        filtered = [item for item in filtered if _parse_iso(item.get("timestamp")) >= since]
    if until is not None:
        filtered = [item for item in filtered if _parse_iso(item.get("timestamp")) <= until]
    return filtered


def _count_by(events: list[dict[str, object]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event in events:
        value = str(event.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[0]))


def _percentile(sorted_values: list[int], p: float) -> int:
    if not sorted_values:
        return 0
    if len(sorted_values) == 1:
        return sorted_values[0]
    idx = int(round((len(sorted_values) - 1) * p))
    if idx < 0:
        idx = 0
    if idx >= len(sorted_values):
        idx = len(sorted_values) - 1
    return sorted_values[idx]


def _stats_payload(events: list[dict[str, object]]) -> dict[str, object]:
    terminal = [event for event in events if str(event.get("status")) in {"completed", "failed", "fallback"}]
    durations = sorted(_terminal_duration(item) for item in terminal)
    slowest = sorted(terminal, key=_terminal_duration, reverse=True)[:5]
    llm_terminal = [event for event in terminal if str(event.get("step_type")) == "llm"]
    fallback_rate = (sum(1 for event in terminal if str(event.get("status")) == "fallback") / len(terminal)) if terminal else 0.0
    provider_model_snapshot: dict[str, int] = {}
    for event in llm_terminal:
        provider = _provider_of(event) or "unknown_provider"
        model = _model_of(event) or "unknown_model"
        key = f"{provider}:{model}"
        provider_model_snapshot[key] = provider_model_snapshot.get(key, 0) + 1
    return {
        "event_count": len(events),
        "counts_by_step_type": _count_by(events, "step_type"),
        "counts_by_status": _count_by(events, "status"),
        "duration_ms": {
            "p50": _percentile(durations, 0.50),
            "p95": _percentile(durations, 0.95),
        },
        "slowest_steps": [
            {
                "event_id": item.get("event_id"),
                "run_id": item.get("run_id"),
                "step_name": item.get("step_name"),
                "step_type": item.get("step_type"),
                "status": item.get("status"),
                "duration_ms": _terminal_duration(item),
            }
            for item in slowest
        ],
        "fallback_rate": round(fallback_rate, 6),
        "provider_model_usage": dict(sorted(provider_model_snapshot.items(), key=lambda item: item[0])),
    }


def _build_run_totals(events: list[dict[str, object]]) -> dict[str, int]:
    terminal = [event for event in events if str(event.get("status")) in {"completed", "failed", "fallback"}]
    return {
        "total_events": len(events),
        "total_duration_ms": sum(_terminal_duration(event) for event in terminal),
        "llm_step_count": sum(1 for event in terminal if str(event.get("step_type")) == "llm"),
        "fallback_count": sum(1 for event in terminal if str(event.get("status")) == "fallback"),
        "failed_count": sum(1 for event in terminal if str(event.get("status")) == "failed"),
    }


def run(request: CommandRequest, args, session: ExecutionSession) -> int:
    repo_root = Path(args.repo_root).resolve()
    is_json = args.output_format == "json"
    view = args.view
    parts: list[str] = list(getattr(args, "parts", []) or [])
    try:
        action, value, event_id = _parse_logs_command(parts)
        events = _sort_events(_apply_filters(load_protocol_events(repo_root), args))
    except ValueError as exc:
        if is_json:
            emit_contract_json(
                build_contract(
                    capability=request.capability.value,
                    profile=request.profile.value,
                    summary="Invalid logs command/filter.",
                    evidence=[],
                    uncertainty=[str(exc)],
                    next_step="Run: forge logs tail",
                    sections={"status": "fail"},
                )
            )
            return 1
        print(str(exc))
        return 1

    if action == "tail":
        count = int(value or 20)
        tail = events[-count:]
        if is_json:
            emit_contract_json(
                build_contract(
                    capability=request.capability.value,
                    profile=request.profile.value,
                    summary=f"Showing {len(tail)} protocol events (tail).",
                    evidence=[],
                    uncertainty=[] if tail else ["No protocol events matched the current filters."],
                    next_step="Run: forge logs run <run_id>",
                    sections={
                        "status": "ok",
                        "path": str(events_log_path(repo_root).relative_to(repo_root)),
                        "events": tail,
                    },
                )
            )
            return 0
        print("=== FORGE LOGS TAIL ===")
        if not tail:
            print("No protocol events matched the current filters.")
            print("Run: forge logs tail")
            return 0
        for event in tail:
            print(_event_line(event))
        print("\n--- Next Step ---")
        print("Run: forge logs run <run_id>")
        return 0

    if action == "show":
        match = next((item for item in events if str(item.get("event_id")) == str(event_id)), None)
        if match is None:
            message = f"Event '{event_id}' not found."
            if is_json:
                emit_contract_json(
                    build_contract(
                        capability=request.capability.value,
                        profile=request.profile.value,
                        summary=message,
                        evidence=[],
                        uncertainty=["No matching event_id in filtered protocol events."],
                        next_step="Run: forge logs tail",
                        sections={"status": "missing"},
                    )
                )
                return 1
            print(message)
            print("Run: forge logs tail")
            return 1
        if is_json:
            emit_contract_json(
                build_contract(
                    capability=request.capability.value,
                    profile=request.profile.value,
                    summary=f"Event {event_id} loaded.",
                    evidence=[],
                    uncertainty=[],
                    next_step=f"Run: forge logs run {match.get('run_id')}",
                    sections={"status": "ok", "event": match},
                )
            )
            return 0
        print("=== FORGE LOGS EVENT ===")
        print(_event_line(match))
        if view == "full":
            print("\n--- Metadata ---")
            print(json.dumps(match.get("metadata", {}), ensure_ascii=False, indent=2))
        print("\n--- Next Step ---")
        print(f"Run: forge logs run {match.get('run_id')}")
        return 0

    if action == "stats":
        stats = _stats_payload(events)
        if is_json:
            emit_contract_json(
                build_contract(
                    capability=request.capability.value,
                    profile=request.profile.value,
                    summary=f"Computed protocol log stats for {stats['event_count']} events.",
                    evidence=[],
                    uncertainty=[] if stats["event_count"] else ["No protocol events matched the current filters."],
                    next_step="Run: forge logs tail",
                    sections={"status": "ok", "stats": stats},
                )
            )
            return 0
        print("=== FORGE LOGS STATS ===")
        print(f"Events: {stats['event_count']}")
        duration = stats["duration_ms"]
        print(f"Duration p50/p95: {duration['p50']}ms / {duration['p95']}ms")
        print(f"Fallback rate: {stats['fallback_rate']:.3f}")
        print("\n--- Counts By Step Type ---")
        for key, count in stats["counts_by_step_type"].items():
            print(f"{key}: {count}")
        print("\n--- Counts By Status ---")
        for key, count in stats["counts_by_status"].items():
            print(f"{key}: {count}")
        print("\n--- Slowest Steps ---")
        slowest = stats["slowest_steps"]
        if not slowest:
            print("None.")
        else:
            for item in slowest:
                print(
                    f"run={item['run_id']} event={item['event_id']} "
                    f"{item['step_name']}[{item['step_type']}] {item['status']} {item['duration_ms']}ms"
                )
        print("\n--- Provider/Model Usage ---")
        usage = stats["provider_model_usage"]
        if not usage:
            print("None.")
        else:
            for key, count in usage.items():
                print(f"{key}: {count}")
        return 0

    run_id = int(value or 0)
    run_filter = getattr(args, "logs_run_id", None)
    if run_filter is not None and int(run_filter) != run_id:
        message = f"conflicting run filters: command run_id={run_id} differs from --run-id={run_filter}"
        if is_json:
            emit_contract_json(
                build_contract(
                    capability=request.capability.value,
                    profile=request.profile.value,
                    summary="Invalid logs filter combination.",
                    evidence=[],
                    uncertainty=[message],
                    next_step=f"Run: forge logs run {run_id}",
                    sections={"status": "fail"},
                )
            )
            return 1
        print(message)
        return 1

    run_events = [item for item in events if _safe_int(item.get("run_id")) == run_id]
    if not run_events:
        message = f"No protocol events found for run {run_id}."
        if is_json:
            emit_contract_json(
                build_contract(
                    capability=request.capability.value,
                    profile=request.profile.value,
                    summary=message,
                    evidence=[],
                    uncertainty=["Run id missing in filtered protocol log."],
                    next_step="Run: forge runs last",
                    sections={"status": "missing"},
                )
            )
            return 1
        print(message)
        print("Run: forge runs last")
        return 1

    totals = _build_run_totals(run_events)
    problematic = [item for item in run_events if str(item.get("status")) in {"failed", "fallback"}]

    if is_json:
        emit_contract_json(
            build_contract(
                capability=request.capability.value,
                profile=request.profile.value,
                summary=f"Run {run_id} protocol timeline with {totals['total_events']} events.",
                evidence=[],
                uncertainty=[],
                next_step="Run: forge logs show <event_id>",
                sections={
                    "status": "ok",
                    "run_id": run_id,
                    "totals": totals,
                    "timeline": run_events,
                    "problematic": problematic,
                },
            )
        )
        return 0

    print("=== FORGE LOGS RUN ===")
    print(f"Run: {run_id}")
    print(
        "Totals: "
        f"events={totals['total_events']}, "
        f"duration_ms={totals['total_duration_ms']}, "
        f"llm_steps={totals['llm_step_count']}, "
        f"fallback={totals['fallback_count']}, failed={totals['failed_count']}"
    )
    print("\n--- Timeline ---")
    for event in run_events:
        print(_event_line(event))
        if view == "full":
            metadata = event.get("metadata")
            if isinstance(metadata, dict) and metadata:
                print(f"  metadata={json.dumps(metadata, ensure_ascii=False)}")
    print("\n--- Problematic Steps ---")
    if not problematic:
        print("None.")
    else:
        for event in problematic:
            print(_event_line(event))
    print("\n--- Next Step ---")
    target = problematic[-1].get("event_id") if problematic else run_events[-1].get("event_id")
    print(f"Run: forge logs show {target}")
    return 0
