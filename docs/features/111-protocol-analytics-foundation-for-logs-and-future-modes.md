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
