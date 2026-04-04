# Index Graph Warning Not Persisted in `index.json`

## Problem

`forge index` writes `.forge/index.json` before graph build.
If graph build fails, code sets `data["graph"]["warning"]` afterward, but the updated payload is not written again.

Observed behavior:
- Console output can report `Graph cache: graph build skipped due to error: ...`.
- Persisted `.forge/index.json` may still miss the corresponding graph warning field.

This creates an observability gap between runtime output and persisted index metadata.

## Required behavior

- Graph warning/status metadata must be persisted in `.forge/index.json` when graph generation fails.
- Persisted index metadata and console output must be consistent for graph build outcome.

## Done criteria

- A forced graph-build-failure scenario produces a persisted graph warning in `.forge/index.json`.
- Existing successful graph path remains unchanged.
- A regression gate verifies warning persistence.
