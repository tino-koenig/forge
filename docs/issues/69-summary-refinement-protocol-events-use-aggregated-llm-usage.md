# Summary-Refinement Protocol Events Use Aggregated LLM Usage

## Problem

Protocol log assembly in `forge_cmd/cli.py` emits `summary_refinement` LLM events from
`sections.llm_usage` (aggregated usage).

In query JSON output, `sections.llm_usage` aggregates planner/orchestrator participation, so
`used=true` can appear even when `summary_refinement` itself is skipped.

Result:
- false-positive `summary_refinement` LLM events in protocol logs.
- quality gate `gate_llm_fallback_analytics_policy_disabled_not_counted` fails.

## Scope

- derive summary-refinement protocol events from stage-specific usage when available.
- keep planner/orchestrator event emission unchanged.

## Acceptance Criteria

- no `summary_refinement` llm events are emitted when `stage_usage.summary_refinement` is
  not attempted/used.
- planner/orchestrator llm events remain visible.

## Resolution Notes

- in CLI protocol assembly, use `llm_usage.stage_usage.summary_refinement` (merged over base
  llm metadata) for `summary_refinement` event derivation.
