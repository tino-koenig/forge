# Quality Gates Missing `--only` Filter Support

## Problem

`scripts/run_quality_gates.py` executes the full gate suite unconditionally and does not parse CLI filters.
Calls like `--only gate_runtime_settings_set_get` are ignored, which causes unrelated failures during focused validation.

Observed behavior:
- Script has no argument parsing for `--only`.
- `main()` always calls `run_all_gates()` without selection.

## Required behavior

- Gate runner should support focused execution (for example `--only <gate_name>`).
- Focused execution must not run unrelated gates.
- Invalid gate names should produce actionable errors.

## Done criteria

- `python3 scripts/run_quality_gates.py --only <gate>` runs exactly the selected gate(s).
- Existing full-suite invocation remains unchanged by default.
- CI/local diagnostics can isolate runtime/session gates deterministically.

## Implemented Behavior (Current)

- `scripts/run_quality_gates.py` now supports focused execution via `--only`.
- `--only` accepts repeated flags and comma-separated gate names.
- Unknown gate names fail fast with an actionable error listing available gate ids.
- Default invocation without `--only` still executes the complete suite unchanged.

## How To Validate Quickly

1. Run one gate only:
   - `PYTHONPATH=. python3 scripts/run_quality_gates.py --only gate_runtime_settings_set_get`
2. Run multiple gates:
   - `PYTHONPATH=. python3 scripts/run_quality_gates.py --only gate_a,gate_b`
3. Validate error path:
   - `PYTHONPATH=. python3 scripts/run_quality_gates.py --only gate_does_not_exist`

## Known Limits / Notes

- `--only` executes exactly the named gate functions and does not infer dependency trees.
- The script still requires a repository import context (for example `PYTHONPATH=.` when run directly).
