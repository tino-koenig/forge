# Protocol Analytics Foundation for Logs and Future Modes

## Description

Extract reusable protocol-event filtering and analytics helpers from `modes/logs.py` into a shared foundation module.

## Spec

- Move filter parsing/apply and stats aggregation (`counts`, percentiles, fallback-rate, provider/model snapshot) into a core analytics foundation.
- Keep `modes/logs.py` as a thin mode adapter (command parsing + output contract rendering).
- Reuse the foundation in other surfaces (for example doctor diagnostics or future observability/reporting modes).

## Definition of Done

- Logs analytics logic is no longer mode-local monolith.
- Shared helpers have direct unit coverage.
- Existing logs command behavior/output contracts remain stable.

## Implemented Behavior (Current)

- Reusable protocol analytics/filtering helpers were extracted into [core/protocol_analytics_foundation.py](/Users/tino/PhpstormProjects/forge/core/protocol_analytics_foundation.py).
- `modes/logs.py` now uses this foundation for filtering, stats aggregation, and run totals instead of local monolithic helper logic.
- Existing `forge logs` output contract structure remains unchanged.

## How To Validate Quickly

- Run `forge --output-format json logs stats` and verify unchanged sections (`stats`, `counts_by_*`, `fallback_rate`, `provider_model_usage`).
- Run `python3 scripts/run_quality_gates.py` and confirm the protocol analytics foundation gate passes.

## Known Limits / Notes

- This feature extracts shared read-only analytics helpers; it does not add new CLI flags or analytics dimensions.
