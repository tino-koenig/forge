# LLM Cost and Token Tracking

## Description

This feature adds explicit per-request token and cost tracking for LLM usage.

It is intentionally separate from query-planning quality features.
Goal: observability and spend control without changing capability semantics.

## Spec

### Scope

Capture and expose LLM usage metrics for all LLM-assisted capabilities:
- query
- explain
- review
- describe
- test

Metrics per request:
- provider/model
- prompt/input tokens
- completion/output tokens
- total tokens
- estimated cost (if pricing configured)
- LLM latency
- fallback status

### Output exposure

Expose metrics in:
- JSON output (`sections.llm_usage.cost` and related fields)
- run history metadata for later analysis

Text output policy:
- no cost block in compact/standard by default
- available in full details mode

### Configuration

Add pricing configuration to `.forge/config.toml`:
- `llm.pricing.input_per_1k`
- `llm.pricing.output_per_1k`
- `llm.pricing.currency`

Controls:
- `llm.cost_tracking.enabled` (`true|false`)
- optional warning thresholds:
  - `llm.cost_tracking.warn_cost_per_request`
  - `llm.cost_tracking.warn_tokens_per_request`

### Behavior

- if provider returns usage tokens, use provider numbers
- if unavailable, set fields to `unknown` (do not fabricate)
- estimated cost only when pricing is configured and token counts are known

### Safety and constraints

- never log API keys or auth headers
- no behavior change in retrieval/review logic due to cost tracking alone
- missing pricing config must not fail capability execution

## Design

### Why this feature

Cost transparency is necessary for production usage and model strategy decisions.
Separating this from query-planner quality keeps concerns clean.

### Non-goals

- no billing/export integration in this feature
- no hard cost enforcement (warn-only in first phase)

## Definition of Done

- token/cost fields are emitted when data is available
- unknown values are explicit when provider does not return usage
- run history stores cost-related metadata
- quality gates cover:
  - usage-present path
  - usage-missing path
  - pricing-config and no-pricing variants

## Implemented Behavior (Current)

- Implementation status: implemented.
- Traceability: `CHANGELOG.md` references feature 029; status/implemented date are tracked in `docs/status/features-index.md`.
- Added LLM cost-tracking config fields in resolved settings:
  - `llm.cost_tracking.enabled`
  - `llm.cost_tracking.warn_cost_per_request`
  - `llm.cost_tracking.warn_tokens_per_request`
  - `llm.pricing.input_per_1k`
  - `llm.pricing.output_per_1k`
  - `llm.pricing.currency`
- `sections.llm_usage` now carries token and cost metadata for LLM-assisted paths with explicit unknown fallback:
  - `token_usage` (`prompt_tokens`, `completion_tokens`, `total_tokens`, `source`)
  - `cost_tracking` (`enabled`, pricing fields, currency)
  - `cost` (`estimated_per_request`, `currency`, warning status/messages)
- Query planner and query action orchestrator usage blocks expose the same token/cost structures in their `usage` sections.
- Pricing is warn-only: no retrieval/scoring behavior is changed by cost tracking.

## How To Validate Quickly

- Explain JSON contract:
  - `forge --output-format json --view full explain core/llm_observability.py`
  - inspect `sections.llm_usage.token_usage`, `sections.llm_usage.cost_tracking`, `sections.llm_usage.cost`
- Query JSON contract:
  - `forge --output-format json --view full query "Wo ist enrich_detailed_context definiert?"`
  - inspect:
    - `sections.query_planner.usage.token_usage/cost_tracking/cost`
    - `sections.action_orchestration.usage.token_usage/cost_tracking/cost`
- With no provider usage/pricing, fields stay explicit (`"unknown"`), capability execution continues.

## Known Limits / Notes

- Cost estimates are only produced when both token usage and pricing are available.
- Current provider token extraction relies on standard usage fields (`prompt_tokens`, `completion_tokens`, `total_tokens`).
- Warning thresholds are informational and surfaced via usage warnings/uncertainty notes; they do not enforce hard stop behavior.
