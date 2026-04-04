from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from core.capability_model import CommandRequest
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
    raise ValueError("Usage: forge logs [tail [count] | run <run_id> | show <event_id>]")


def _build_run_totals(events: list[dict[str, object]]) -> dict[str, int]:
    terminal = [event for event in events if str(event.get("status")) in {"completed", "failed", "fallback"}]
    return {
        "total_events": len(events),
        "total_duration_ms": sum(_terminal_duration(event) for event in terminal),
        "llm_step_count": sum(1 for event in terminal if str(event.get("step_type")) == "llm"),
        "fallback_count": sum(1 for event in terminal if str(event.get("status")) == "fallback"),
        "failed_count": sum(1 for event in terminal if str(event.get("status")) == "failed"),
    }


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


def run(request: CommandRequest, args, session: ExecutionSession) -> int:
    repo_root = Path(args.repo_root).resolve()
    is_json = args.output_format == "json"
    view = args.view
    parts: list[str] = list(getattr(args, "parts", []) or [])
    try:
        action, value, event_id = _parse_logs_command(parts)
    except ValueError as exc:
        if is_json:
            emit_contract_json(
                build_contract(
                    capability=request.capability.value,
                    profile=request.profile.value,
                    summary="Invalid logs command.",
                    evidence=[],
                    uncertainty=[str(exc)],
                    next_step="Run: forge logs tail",
                    sections={"status": "fail"},
                )
            )
            return 1
        print(str(exc))
        return 1

    events = _sort_events(load_protocol_events(repo_root))
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
                    uncertainty=[] if tail else ["No protocol events recorded yet."],
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
            print("No protocol events recorded yet.")
            print("Run: forge query \"where is ...\"")
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
                        uncertainty=["No matching event_id in .forge/logs/events.jsonl."],
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

    run_id = int(value or 0)
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
                    uncertainty=["Run id missing in protocol log."],
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
