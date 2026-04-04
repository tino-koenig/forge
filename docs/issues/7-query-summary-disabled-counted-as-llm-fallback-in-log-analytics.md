# Query Summary Disabled Counted as LLM Fallback in Log Analytics

## Problem

When query summary refinement is disabled by policy (for example JSON output), protocol events still emit `summary_refinement` as `llm` with terminal `fallback`.
This inflates fallback analytics in feature 033 despite no real failed LLM call.

Observed behavior:
- Query JSON sets `sections.llm_usage` with `attempted=false`, `used=false`, fallback reason ("summary refinement disabled for json output").
- Event conversion still emits llm started+fallback entries for that stage.
- `forge logs --step-type llm stats` reports non-trivial fallback rates from policy-disabled paths.

## Required behavior

- Policy-disabled/non-attempted LLM stages must not be counted as failure/fallback events in operational analytics.
- Fallback metrics should represent actual attempted LLM instability, not expected disabled behavior.
- If disabled-stage visibility is desired, use explicit non-llm policy events or separate counters.

## Done criteria

- Query JSON mode no longer adds synthetic llm fallback for disabled summary refinement.
- `logs stats` fallback rate for simple mock query scenarios is not inflated by disabled stages.
- Existing llm fallback reporting still works for real planner/orchestrator/provider failures.


## Linked Features

- [Feature 106 - Policy-Disabled LLM Events Must Not Inflate Fallback Analytics](/Users/tino/PhpstormProjects/forge/docs/features/106-policy-disabled-llm-events-must-not-inflate-fallback-analytics.md)
