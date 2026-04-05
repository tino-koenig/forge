from __future__ import annotations

import json
from pathlib import Path

from core.capability_model import Capability, CommandRequest
from core.effects import ExecutionSession
from core.output_contracts import build_contract, emit_contract_json
from core.protocol_analytics_foundation import (
    apply_filters,
    build_run_totals,
    safe_int,
    sort_events,
    stats_payload,
)
from core.protocol_log import events_log_path, load_protocol_events


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
            count = safe_int(parts[1])
            if count is None or count <= 0:
                raise ValueError("Usage: forge logs tail [count>0]")
            return "tail", count, None
        return "tail", 20, None
    if first == "run":
        if len(parts) < 2:
            raise ValueError("Usage: forge logs run <run_id>")
        run_id = safe_int(parts[1])
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


def run(request: CommandRequest, args, session: ExecutionSession) -> int:
    repo_root = Path(args.repo_root).resolve()
    is_json = args.output_format == "json"
    view = args.view
    parts: list[str] = list(getattr(args, "parts", []) or [])
    try:
        action, value, event_id = _parse_logs_command(parts)
        events = sort_events(apply_filters(load_protocol_events(repo_root), args))
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
        stats = stats_payload(events)
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

    run_events = [item for item in events if safe_int(item.get("run_id")) == run_id]
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

    totals = build_run_totals(run_events)
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
