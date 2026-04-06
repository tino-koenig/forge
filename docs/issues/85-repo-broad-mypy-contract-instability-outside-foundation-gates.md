# Repo-Broad Mypy Contract Instability Outside Foundation Gates

## Problem

Repository-wide typing is currently much less stable than the green Foundation-focused quality gates suggest.

A broader mypy run across non-gated modules surfaces substantial contract failures outside the currently enforced Foundation subset. As a result, the repository can report green scoped quality gates while still carrying significant static contract instability in core and mode code that remains outside the active typing gate.

## Why this matters

- Green Foundation gates can be misread as evidence of broader repository type health.
- Contract regressions can accumulate in non-gated modules without visible pressure to fix them.
- Static instability in core and mode paths increases refactor risk even when Foundation tests stay green.
- Quality reporting becomes too optimistic relative to actual repository-wide typing health.

## Evidence

- The current quality gates focus on a Foundation subset rather than the full repository typing surface.
- A broader mypy run across `core`, `modes`, `forge`, and `forge_cmd` reports substantial additional failures.
- The observed result was 206 mypy errors across 22 files in the broader run.
- Representative affected files include areas such as `core/session_store.py`, `core/graph_cache.py`, `modes/query.py`, and `modes/explain.py`.

## Required behavior

- Repository-wide typing health must be visible separately from Foundation-scoped gate health.
- Broader mypy failures outside the active gate must be tracked explicitly rather than implied away by green scoped gates.
- The project must define whether repo-wide mypy is advisory, baseline-tracked, or progressively enforced.
- Quality reporting must make scoped-versus-global typing coverage unambiguous.

## Done criteria

- Repo-wide mypy status is surfaced explicitly in quality reporting or companion reporting.
- The distinction between Foundation-gated typing and broader repository typing is documented clearly.
- A tracked baseline exists for the current broader mypy failure set.
- There is an explicit reduction plan, triage policy, or ratchet strategy for bringing the broader error count down over time.

## Scope

This issue is limited to repository-wide typing visibility, policy, and reduction strategy outside the current Foundation gate.

It does not require immediate zero-error repo-wide mypy, and it does not redefine the Foundation subset itself.

## Implemented Behavior (Current)

- Quality gates now include a dedicated repo-wide typing visibility gate: `gate_repo_wide_mypy_baseline`.
- The gate runs mypy across `core`, `modes`, `forge`, and `forge_cmd`, and reports results explicitly as advisory output.
- Foundation-scoped type enforcement remains unchanged and separate (`gate_foundation_mypy_contracts`).
- Repo-wide mypy is baseline-tracked via a configured threshold:
  - baseline: `206` errors
  - gate fails only when the observed count exceeds baseline
- This makes scoped-versus-global typing health explicit while allowing incremental debt reduction.

## Suggested implementation direction

- Add a broader repo-wide mypy mode that runs in parallel with the Foundation-scoped type checks.
- Publish scoped and global typing results separately so green Foundation gates cannot be misread as repo-wide success.
- Capture the current broader error count as a baseline and ratchet downward over time.
- Group failures by module area or error class so reduction work can be planned incrementally.

## How To Validate Quickly

1. Run the current Foundation typing gate path and record the result.
2. Run the broader mypy command across `core`, `modes`, `forge`, and `forge_cmd`.
3. Confirm that broader failures are surfaced separately from Foundation gate success.
4. Confirm that the current failure baseline is recorded and can be compared over time.

## Known Limits / Notes

- This issue is about visibility, policy, and reduction strategy for broader typing debt.
- It does not require flipping repo-wide mypy to a hard failing gate immediately.
- Quality-gate wording and whole-repo PASS semantics are closely related, but broader gate-scope clarification may still be tracked separately.
