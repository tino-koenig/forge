# Log Filtering and LLM Query Analytics

## Description

This feature adds filterable log analysis, with special support for LLM event filtering and latency bottleneck detection.

## Spec

### Scope

Add filter options to `forge logs`:
- `--run-id <id>`
- `--capability <name>`
- `--step-type llm`
- `--status failed|fallback|completed`
- `--since <iso8601>`
- `--until <iso8601>`
- `--provider <name>`
- `--model <name>`

### Analytics summaries

Add aggregate subcommands:
- `forge logs stats`
- `forge logs stats --step-type llm`
- `forge logs stats --capability query`

Metrics:
- event counts by type/status
- p50/p95 duration
- slowest steps
- fallback rate
- per-model/provider usage snapshot

### Time-finder workflow

Primary use case:
- identify time-consuming runs/steps
- identify unstable LLM calls (high fallback/latency)

### Constraints

- stats must be computed from persisted event logs only
- no mutation of run history
- unknown/invalid filters fail with clear message

## Design

### Why this feature

Users need operational answers quickly:
- where is time lost?
- which LLM calls are unstable?
- which capability path is slow?

### Non-goals

- no external BI integration
- no real-time streaming dashboard in this feature

## Definition of Done

- LLM-focused filtering works reliably
- latency and fallback analytics are available in CLI
- outputs are usable in both text and JSON modes

## Implemented Behavior (Current)

- Implementation status: implemented.
- Traceability: `CHANGELOG.md` references feature 033; status/implemented date are tracked in `docs/status/features-index.md`.
- Added `forge logs` filter options:
  - `--run-id <id>`
  - `--capability <name>`
  - `--step-type deterministic|llm|io|policy`
  - `--status started|completed|failed|fallback`
  - `--since <iso8601>`
  - `--until <iso8601>`
  - `--provider <name>`
  - `--model <name>`
- Added aggregate analytics command:
  - `forge logs stats`
  - filters can be combined with `stats` (for example `--step-type llm`, `--capability query`)
- Stats include:
  - counts by step type/status
  - duration percentiles (`p50`, `p95`)
  - slowest steps (top 5)
  - fallback rate
  - provider/model usage snapshot

## How To Validate Quickly

- Run:
  - `forge --llm-provider mock query "compute_price"`
- Filtered tail:
  - `forge logs --step-type llm --status completed tail 10`
- Stats:
  - `forge logs stats`
  - `forge logs --step-type llm stats`
  - `forge logs --capability query stats`
- Time window:
  - `forge logs --since 2026-04-04T00:00:00Z --until 2026-04-04T23:59:59Z tail 20`

## Known Limits / Notes

- Percentiles are computed from persisted terminal events with numeric `duration_ms`.
- Filters are applied on persisted protocol events only (no run-history mutation, no live sampling).
