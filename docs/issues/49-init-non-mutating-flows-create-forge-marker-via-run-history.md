# Init Non-Mutating Flows Create `.forge` Marker via Run History

## Problem

`forge init` paths that should be non-mutating still create `.forge/runs.jsonl` via global run-history persistence.
This implicitly creates the `.forge` marker and changes repository state even for informational/dry-run/failed flows.

## Evidence

Reproduced in fresh temp directories:
- `forge init --list-templates` creates `.forge/` and `.forge/runs.jsonl`
- `forge init --dry-run --non-interactive --template balanced` reports no write but still creates `.forge/`
- `forge init` without TTY (expected fail) still creates `.forge/`

Root cause path:
- CLI appends run history for all capabilities except `runs` and `logs`.
- `append_run(...)` writes `.forge/runs.jsonl`, creating `.forge/` as side effect.

## Required behavior

- Non-mutating init flows must not create repository marker/state:
  - `--list-templates`
  - `--dry-run`
  - precondition failures (non-tty, invalid template, etc.)
- Marker creation should only happen on successful write-intent init execution.

## Done criteria

- Above non-mutating/failed flows leave filesystem unchanged in fresh directories.
- `.forge/` marker appears only after successful init write path.
- Regression tests cover each non-mutating init path.

## Linked Features

- [Feature 112 - Init Side-Effect Guard for Non-Mutating and Failed Flows](/Users/tino/PhpstormProjects/forge/docs/features/112-init-side-effect-guard-for-non-mutating-and-failed-flows.md)
