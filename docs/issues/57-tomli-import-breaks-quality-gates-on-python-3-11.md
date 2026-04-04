# `tomli` Import Breaks Quality Gates on Python 3.11

## Problem

Quality-gates execution fails on Python 3.11 environments with:
- `ModuleNotFoundError: No module named 'tomli'`

Reason:
- project code imports `tomli` directly in multiple modules.
- Python 3.11 provides TOML parsing via stdlib `tomllib`, while `tomli` dependency is only declared for Python < 3.11.

## Scope

- provide a central TOML compatibility import path usable across project modules.
- remove direct `import tomli` usage from runtime code paths used by quality gates.

## Acceptance Criteria

- all previous direct `tomli` imports in runtime/gate modules use compatibility import.
- quality-gates startup/import path succeeds on Python 3.11 without installing `tomli`.
- Python < 3.11 behavior remains compatible.

## Resolution Notes

- added `core/toml_compat.py` with `tomllib` (3.11+) / `tomli` fallback.
- updated modules and scripts to import `tomli` via `from core.toml_compat import tomli`.
