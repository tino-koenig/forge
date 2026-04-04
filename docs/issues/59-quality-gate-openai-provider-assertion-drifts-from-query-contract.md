# Quality Gate OpenAI Provider Assertion Drifts from Query LLM Contract

## Problem

`gate_openai_compatible_provider` failed while query behavior was functionally correct.

Reason:
- gate asserted legacy top-level `sections.llm_usage.provider` and refined-summary prefix.
- current query JSON contract exposes provider participation primarily via stage-level usage (`query_planner.usage`, `action_orchestration.usage`) and may keep deterministic summary wording.

## Scope

- align gate assertions with current query LLM contract semantics.
- keep provider verification strict, but target stable stage-level fields.

## Acceptance Criteria

- `gate_openai_compatible_provider` passes with `FORGE_LLM_PROVIDER=openai_compatible` and mock base URL.
- assertions validate provider and usage in stage-level usage sections.
- gate no longer relies on brittle summary prefix wording.

## Resolution Notes

- updated gate to assert:
  - `sections.llm_usage.used is true`
  - `sections.query_planner.usage.provider == openai_compatible`
  - `sections.action_orchestration.usage.provider == openai_compatible`
