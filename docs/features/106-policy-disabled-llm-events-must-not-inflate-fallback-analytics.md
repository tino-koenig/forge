# Policy-Disabled LLM Events Must Not Inflate Fallback Analytics

## Description

Ensure operational fallback metrics represent real attempted LLM instability, not policy-disabled/non-attempted stages.

## Addresses Issues

- [Issue 7 - Query Summary Disabled Counted as LLM Fallback in Log Analytics](/Users/tino/PhpstormProjects/forge/docs/issues/7-query-summary-disabled-counted-as-llm-fallback-in-log-analytics.md)

## Spec

- Update step-event derivation for LLM usage so policy-disabled/non-attempted stages are not emitted as `step_type=llm` with terminal `fallback`.
- If visibility is required, emit explicit `policy` events (or equivalent separate counters) to keep analytics semantics clean.
- Preserve real fallback events for attempted LLM calls that actually fail or fallback.

## Definition of Done

- `forge logs --step-type llm stats` fallback rate is not inflated by policy-disabled summary refinement in JSON query mode.
- Real attempted LLM failures still appear as llm fallback events.
- Regression coverage includes disabled-stage and real-failure scenarios.
