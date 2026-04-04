# Log Viewer and Run-Focused Inspection

## Description

This feature adds a first-class CLI log viewer for protocol events.

Users can inspect logs for:
- a specific run
- a capability
- recent timeline slices

## Spec

### Scope

Add command family:
- `forge logs tail`
- `forge logs run <run_id>`
- `forge logs show <event_id>`

Views:
- text (human-first)
- json (`--output-format json`)

### Run-focused behavior

`forge logs run <run_id>` should:
- show ordered step timeline
- include status and duration per step
- highlight failed/fallback steps
- provide summary totals (duration, llm step count, fallback count)

### Human-first output

Default text should prioritize:
1. timeline overview
2. problematic steps
3. next diagnostic hint

Detailed metadata available via full/detail view.

### Constraints

- viewer is read-only
- missing run id gives explicit actionable message

## Design

### Why this feature

Protocol logging is only useful if users can inspect it quickly during real troubleshooting.

### Non-goals

- no GUI viewer in this phase

## Definition of Done

- log viewer commands exist and are documented
- run-focused view is chronological and useful for debugging
- JSON output supports automation

## Implemented Behavior (Current)

- Implementation status: implemented.
- Traceability: `CHANGELOG.md` references feature 032; status/implemented date are tracked in `docs/status/features-index.md`.
- Added command family:
  - `forge logs tail [count]`
  - `forge logs run <run_id>`
  - `forge logs show <event_id>`
- Viewer reads protocol events from `.forge/logs/events.jsonl` (read-only).
- Supports text and JSON output:
  - text: human-first timeline
  - json: structured contract with timeline/event payloads
- `logs run <run_id>` exposes:
  - ordered timeline
  - step status + duration
  - summary totals (`total_duration_ms`, `llm_step_count`, `fallback_count`, `failed_count`)
  - problematic step slice (`failed|fallback`)

## How To Validate Quickly

- Create events:
  - `forge --llm-provider mock query "compute_price"`
- Tail:
  - `forge logs tail`
- Run-focused timeline:
  - `forge --output-format json runs last`
  - `forge logs run <run_id>`
- Single event:
  - `forge logs show <event_id>`

## Known Limits / Notes

- Filtering by capability/time range is not yet exposed as dedicated flags (tail/run/show form only).
- Viewer tolerates malformed JSONL lines by skipping invalid entries.
