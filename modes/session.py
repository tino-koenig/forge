from __future__ import annotations

from pathlib import Path

from core.capability_model import CommandRequest, EffectClass
from core.effects import ExecutionSession
from core.output_contracts import build_contract, emit_contract_json
from core.output_views import is_full, resolve_view
from core.session_store import (
    DEFAULT_TTL_MINUTES,
    clear_session_context,
    create_session,
    end_session,
    ensure_active_session,
    list_sessions,
    show_session,
    use_session,
)


def _result_contract(
    request: CommandRequest,
    *,
    summary: str,
    next_step: str,
    sections: dict[str, object],
    uncertainty: list[str] | None = None,
) -> dict[str, object]:
    return build_contract(
        capability=request.capability.value,
        profile=request.profile.value,
        summary=summary,
        evidence=[],
        uncertainty=uncertainty or [],
        next_step=next_step,
        sections=sections,
    )


def run(request: CommandRequest, args, session: ExecutionSession) -> int:
    view = resolve_view(args)
    repo_root = Path(args.repo_root).resolve()
    session.record_effect(EffectClass.READ_ONLY, f"read sessions under {repo_root / '.forge' / 'sessions'}")
    # Parse session subcommand from positional payload parts.
    parts = getattr(args, "parts", []) or []
    command = parts[0] if parts else "status"
    uncertainty: list[str] = []

    try:
        if command == "status":
            active, auto_created, warnings = ensure_active_session(repo_root)
            session.record_effect(EffectClass.FORGE_WRITE, "ensure active named session")
            uncertainty.extend(warnings)
            payload = show_session(repo_root, active.name)
            contract = _result_contract(
                request,
                summary=f"Active session: {active.name}",
                next_step="Run: forge session list",
                sections={
                    "session_command": "status",
                    "auto_created": auto_created,
                    "active_session": payload,
                },
                uncertainty=uncertainty,
            )
        elif command == "new":
            if len(parts) < 2:
                raise ValueError("session new requires a name")
            ttl_minutes = int(getattr(args, "session_ttl_minutes", DEFAULT_TTL_MINUTES) or DEFAULT_TTL_MINUTES)
            created = create_session(repo_root, name=parts[1], ttl_minutes=ttl_minutes, activate=True)
            session.record_effect(EffectClass.FORGE_WRITE, f"create session {created.name}")
            payload = show_session(repo_root, created.name)
            contract = _result_contract(
                request,
                summary=f"Created and activated session '{created.name}'.",
                next_step=f"Run: forge session show {created.name}",
                sections={"session_command": "new", "session": payload},
            )
        elif command == "use":
            if len(parts) < 2:
                raise ValueError("session use requires a name")
            target, revived = use_session(repo_root, parts[1], revive=bool(getattr(args, "session_revive", False)))
            session.record_effect(EffectClass.FORGE_WRITE, f"use session {target.name}")
            payload = show_session(repo_root, target.name)
            contract = _result_contract(
                request,
                summary=f"Activated session '{target.name}'.",
                next_step=f"Run: forge session show {target.name}",
                sections={"session_command": "use", "revived": revived, "session": payload},
            )
        elif command == "list":
            items = list_sessions(repo_root)
            contract = _result_contract(
                request,
                summary=f"Listed {len(items)} sessions.",
                next_step="Run: forge session",
                sections={"session_command": "list", "sessions": items},
            )
        elif command == "show":
            name = parts[1] if len(parts) >= 2 else None
            payload = show_session(repo_root, name)
            if payload is None:
                raise ValueError("session not found")
            contract = _result_contract(
                request,
                summary=f"Session details for '{payload.get('name')}'.",
                next_step="Run: forge session list",
                sections={"session_command": "show", "session": payload},
            )
        elif command == "clear-context":
            name = parts[1] if len(parts) >= 2 else None
            updated = clear_session_context(repo_root, name=name)
            session.record_effect(EffectClass.FORGE_WRITE, f"clear context for session {updated.name}")
            payload = show_session(repo_root, updated.name)
            contract = _result_contract(
                request,
                summary=f"Cleared context for session '{updated.name}'.",
                next_step=f"Run: forge session show {updated.name}",
                sections={"session_command": "clear-context", "session": payload},
            )
        elif command == "end":
            name = parts[1] if len(parts) >= 2 else None
            ended = end_session(repo_root, name=name)
            session.record_effect(EffectClass.FORGE_WRITE, f"end session {ended}")
            contract = _result_contract(
                request,
                summary=f"Ended session '{ended}'.",
                next_step="Run: forge session list",
                sections={"session_command": "end", "ended_session": ended},
            )
        else:
            raise ValueError(
                "unknown session command; use one of: status|new|use|list|show|clear-context|end"
            )
    except ValueError as exc:
        contract = _result_contract(
            request,
            summary=f"Session command failed: {exc}",
            next_step="Run: forge session list",
            sections={"session_command": command, "status": "error"},
            uncertainty=[str(exc)],
        )
        if args.output_format == "json":
            emit_contract_json(contract)
            return 1
        print("=== FORGE SESSION ===")
        print(f"Profile: {request.profile.value}")
        print("\n--- Summary ---")
        print(contract["summary"])
        print("\n--- Uncertainty ---")
        for note in contract.get("uncertainty", []):
            print(f"- {note}")
        print("\n--- Next Step ---")
        print(contract["next_step"])
        return 1

    if args.output_format == "json":
        emit_contract_json(contract)
        return 0

    print("=== FORGE SESSION ===")
    print(f"Profile: {request.profile.value}")
    print("\n--- Summary ---")
    print(contract["summary"])
    sections = contract.get("sections", {})
    if is_full(view):
        print("\n--- Session ---")
        for key in sorted(sections.keys()):
            print(f"{key}: {sections[key]}")
    print("\n--- Next Step ---")
    print(contract["next_step"])
    return 0
