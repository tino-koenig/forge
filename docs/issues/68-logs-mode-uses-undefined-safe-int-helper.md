# Logs Mode Uses Undefined `_safe_int` Helper

## Problem

`modes/logs.py` parses `logs tail` and `logs run` arguments via `_safe_int`, but no such helper
exists in the module.

Result:
- `forge logs tail ...` and `forge logs run ...` raise `NameError: name '_safe_int' is not defined`.
- quality-gates fail in `gate_logs_viewer_and_run_focused_inspection`.

## Scope

- restore integer parsing for logs command arguments using existing shared foundation helpers.

## Acceptance Criteria

- `forge logs tail <n>` and `forge logs run <id>` parse without NameError.
- logs viewer quality gates proceed past command parsing.

## Resolution Notes

- replaced `_safe_int(...)` calls with imported `safe_int(...)` from
  `core.protocol_analytics_foundation`.
