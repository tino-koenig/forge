# Quality Gates Script Fails in CI due to Missing Repo-Root Import Path

## Problem

Running `python3 scripts/run_quality_gates.py` in CI fails early with:
- `ModuleNotFoundError: No module named 'core'`

Reason:
- when invoked as a file, Python sets `sys.path[0]` to `scripts/`, not repo root.
- direct imports like `from core...` fail unless repo root is on `sys.path`.

## Scope

- make `scripts/run_quality_gates.py` self-sufficient for direct execution from repository root and CI runner shells.
- keep local invocation stable without requiring external `PYTHONPATH` setup.

## Acceptance Criteria

- `python3 scripts/run_quality_gates.py` no longer fails with `ModuleNotFoundError: core`.
- GitHub Actions quality-gates workflow runs the script without custom `PYTHONPATH` setup.
- behavior of existing gates is unchanged beyond bootstrap/import reliability.

## Resolution Notes

- prepend repository root to `sys.path` at script startup before importing project modules.
- update workflow action versions to current majors to remove Node.js 20 deprecation warning noise.
