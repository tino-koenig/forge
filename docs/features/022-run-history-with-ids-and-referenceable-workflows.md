# Run History with IDs and Referenceable Workflows

## Description

This feature introduces persistent run history with stable IDs.

Users can reference previous results directly in follow-up workflows, for example:
- `forge runs 12 show full`
- `forge runs 12 rerun`
- `forge runs last --output-format json`

## Spec

### Scope

Persist executed capability runs in:
- `.forge/runs.jsonl`

Each entry contains:
- run id
- timestamp
- request metadata (capability/profile/payload)
- execution metadata (exit code/output format)
- captured output (text + optional JSON contract)

### CLI surface

Add `forge runs` command family:
- `forge runs list`
- `forge runs last`
- `forge runs show <id> [compact|standard|full]`
- `forge runs <id> show [compact|standard|full]`
- `forge runs <id> rerun`

### Reference model

Runs are repository-local and ordered by execution.
ID assignment is monotonic in the history file.

### Constraints

- no secrets persisted in history payloads
- no hidden mutation effects from reading history
- rerun is explicit and opt-in

## Definition of Done

- run history file is created and appended automatically
- runs can be listed, shown, and rerun by id
- `runs last --output-format json` returns machine-consumable record
- quality gates validate history creation and rerun path
