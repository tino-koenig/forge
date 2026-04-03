from __future__ import annotations

from pathlib import Path

from core.capability_model import Capability, CommandRequest
from core.effects import ExecutionSession
from core.llm_integration import maybe_refine_summary, provenance_section, resolve_settings
from core.output_contracts import build_contract, emit_contract_json
from core.output_views import is_full, resolve_view


def run(request: CommandRequest, args, session: ExecutionSession) -> int:
    _ = session
    is_json = args.output_format == "json"
    view = resolve_view(args)
    question = request.payload.strip()
    repo_root = Path(args.repo_root).resolve()

    ask_preset = str(getattr(args, "ask_preset", "") or "auto")
    ask_command = str(getattr(args, "ask_command", "") or "ask")
    ask_guided = bool(getattr(args, "ask_guided", False))
    framework_profile = getattr(args, "framework_profile", None)

    deterministic_summary = "No LLM answer available for this free ask question."
    task_context = [question]
    task_context.append(f"ask_preset={ask_preset}")
    if framework_profile:
        task_context.append(f"framework_profile={framework_profile}")
    if ask_guided:
        task_context.append("guided=true")
    llm_task = "\n".join(task_context)

    llm_settings = resolve_settings(args, repo_root)
    llm_outcome = maybe_refine_summary(
        capability=Capability.ASK,
        profile=request.profile,
        task=llm_task,
        deterministic_summary=deterministic_summary,
        evidence=[],
        settings=llm_settings,
        repo_root=repo_root,
    )

    summary = llm_outcome.summary if llm_outcome.summary.strip() else deterministic_summary
    uncertainty = [
        "Ask mode is a free LLM question and does not perform repository file search.",
        "No repository evidence anchors are available in ask mode output.",
    ]
    uncertainty.extend(llm_outcome.uncertainty_notes)
    if ask_preset == "latest":
        uncertainty.append("ask:latest does not run web retrieval in this phase; answer is model-generated only.")
    if ask_guided:
        uncertainty.append("--guided is reserved for a later rollout and is currently not interactive.")
    if llm_outcome.usage.get("fallback_reason"):
        uncertainty.append(f"LLM fallback: {llm_outcome.usage['fallback_reason']}")

    sections: dict[str, object] = {
        "ask": {
            "command": ask_command,
            "preset": ask_preset,
            "guided_requested": ask_guided,
            "framework_profile": framework_profile,
            "mode": "free_llm_question",
        },
        "llm_usage": llm_outcome.usage,
        "provenance": provenance_section(llm_used=bool(llm_outcome.usage.get("used")), evidence_count=0),
    }
    next_step = (
        'Use `forge query "..."` for repository-grounded file locations.'
        if ask_preset in {"auto", "repo", "docs"}
        else 'Verify freshness with external sources if "latest" accuracy is required.'
    )
    contract = build_contract(
        capability=request.capability.value,
        profile=request.profile.value,
        summary=summary,
        evidence=[],
        uncertainty=uncertainty,
        next_step=next_step,
        sections=sections,
    )
    if is_json:
        emit_contract_json(contract)
        return 0

    print("=== FORGE ASK ===")
    print(f"Profile: {request.profile.value}")
    print(f"Question: {question}")
    print("\n--- Answer ---")
    print(summary)
    if is_full(view):
        print("\n--- Ask ---")
        print(f"Command: {ask_command}")
        print(f"Preset: {ask_preset}")
        print(f"Guided requested: {ask_guided}")
        print(f"Framework profile: {framework_profile or '-'}")
        print("\n--- LLM Usage ---")
        print(f"Policy: {llm_outcome.usage.get('policy')}")
        print(f"Mode: {llm_outcome.usage.get('mode')}")
        print(f"Used: {llm_outcome.usage.get('used')}")
        print(f"Provider: {llm_outcome.usage.get('provider') or 'none'}")
        print(f"Model: {llm_outcome.usage.get('model') or 'none'}")
        if llm_outcome.usage.get("fallback_reason"):
            print(f"Fallback: {llm_outcome.usage.get('fallback_reason')}")
    print("\n--- Next Step ---")
    print(next_step)
    print("\n--- Uncertainty ---")
    notes = uncertainty if is_full(view) else uncertainty[:1]
    for note in notes:
        print(f"- {note}")
    return 0
