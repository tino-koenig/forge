# Query Orchestration Policy Settings and Source-Traceable Resolution

## Description

Externalize query orchestration progress policy and handler-cost coefficients into canonical runtime settings.

Goals:
- remove hidden hardcoded policy constants
- make tuning transparent and reproducible
- integrate with runtime settings precedence/source tracing

## Addresses Issues

- [Issue 23 - Query Progress Policy and Handler Costs Are Hardcoded](/Users/tino/PhpstormProjects/forge/docs/issues/23-query-progress-policy-and-handler-costs-are-hardcoded.md)

## Spec

### New settings scope

Add canonical keys for query orchestration policy and accounting, for example:
- `query.orchestrator.progress.threshold`
- `query.orchestrator.progress.no_progress_streak_limit`
- `query.orchestrator.handler.read.max_batch`
- `query.orchestrator.handler.read.token_cost_per_line`
- `query.orchestrator.handler.search.token_cost_per_match`
- `query.orchestrator.handler.explain.base_token_cost`

### Resolution and observability

- Resolve via runtime settings foundation precedence (cli > session > repo > user > toml > default).
- Expose effective values and their sources in query output sections.

### Compatibility

- Defaults preserve current behavior unless overridden.

## Definition of Done

- Hardcoded progress/cost constants in query orchestration are replaced by resolved settings.
- `forge get --source` can show origin for these keys.
- Regression gates cover custom policy behavior and fallback-to-default behavior.
