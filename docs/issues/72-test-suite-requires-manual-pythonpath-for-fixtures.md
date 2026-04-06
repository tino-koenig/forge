

# Test Suite Requires Manual PYTHONPATH for Fixture Imports

## Problem

The test suite currently requires a manual `PYTHONPATH` adjustment to import fixture modules (e.g. `tests/fixtures/basic_repo/src`).

Without setting `PYTHONPATH=tests/fixtures/basic_repo`, test collection fails with errors like:

> ModuleNotFoundError: No module named 'src'

This makes the test suite environment-dependent and harder to run for new contributors and in CI.

## Why this matters

A reliable test suite must be:

- self-contained,
- reproducible,
- runnable without manual environment tweaks.

If tests depend on manual `PYTHONPATH` setup:

- local runs become error-prone,
- CI pipelines require special handling,
- onboarding becomes harder,
- subtle import differences can mask real issues.

## Evidence

- Running `pytest` without `PYTHONPATH` fails during test collection for fixture-based tests.
- Tests succeed only when explicitly running:

```bash
PYTHONPATH=tests/fixtures/basic_repo pytest -q
```

## Required behavior

- The test suite must run successfully without requiring manual `PYTHONPATH` changes.
- Fixture imports must resolve deterministically using standard Python import mechanisms.

## Done criteria

- `pytest -q` runs successfully from repo root without additional environment variables.
- No `ModuleNotFoundError` occurs for fixture modules.
- CI can execute tests without special path configuration.

## Scope

This issue focuses on test discovery and import behavior for fixture-based tests.

## Implemented Behavior (Current)

- Pytest configuration is now centralized in `pyproject.toml` under `[tool.pytest.ini_options]`.
- Fixture imports using `from src...` resolve without manual environment setup via:
  - `pythonpath = ["tests/fixtures/basic_repo"]`
- Test collection is stabilized against mutation-workspace bleed-through via:
  - `testpaths = ["tests"]`
  - `norecursedirs` containing `mutants`
- Result: `pytest -q` runs from repository root without manual `PYTHONPATH`.

## Suggested implementation direction

- Make fixture modules importable via package structure (e.g. add `__init__.py` where appropriate).
- Adjust import paths in fixture tests to use explicit module paths instead of relying on `PYTHONPATH`.
- Optionally configure `pytest` (e.g. `pythonpath` in `pytest.ini` or `conftest.py`) to include required paths.
- Ensure consistency between local, CI and tooling environments.

## How To Validate Quickly

1. Run `pytest -q` from the repository root.
2. Confirm that all tests pass without setting `PYTHONPATH`.
3. Confirm fixture test import resolution:
   - `pytest -q tests/fixtures/basic_repo/tests/test_service.py`

## Known Limits / Notes

- Some fixture layouts may need minor restructuring to behave like real packages.
- This issue is about environment reproducibility, not test logic changes.
