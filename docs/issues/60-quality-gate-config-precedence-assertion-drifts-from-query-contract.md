# Quality Gate Config Precedence Assertion Drifts from Query LLM Contract

## Problem

`gate_config_precedence` failed with:
- `CLI model must override env and TOML`

Reason:
- gate asserted legacy top-level `sections.llm_usage.model` and `config_source` fields.
- current query contract surfaces model/provider at stage-level usage (`query_planner.usage`, `action_orchestration.usage`).

## Scope

- align precedence gate assertions with stage-level usage contract.
- keep original intent: CLI model must override env and TOML-provided model.

## Acceptance Criteria

- `gate_config_precedence` passes reliably.
- planner and orchestrator usage both report `model-from-cli`.
- provider remains `openai_compatible` from configured source.

## Resolution Notes

- updated gate to assert:
  - `sections.query_planner.usage.model == model-from-cli`
  - `sections.action_orchestration.usage.model == model-from-cli`
  - `sections.query_planner.usage.provider == openai_compatible`
