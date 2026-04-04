# Review Does Not Use Central Orchestration Runtime

## Problem

Review mode executes a fixed inline pipeline and does not use a shared central orchestrator runtime.

## Evidence

- `modes/review.py` runs sequential mode-local control flow (resolve -> analyze -> aggregate -> summarize -> render).
- No centralized mode-orchestrator runtime is used by review.

## Required behavior

- Review should run via a shared orchestration runtime usable across modes.
- Mode-specific detection steps should be handlers/adapters on top of the central engine.

## Done criteria

- Review emits orchestration trace from central engine.
- Mode-local orchestration boilerplate is reduced.
- Existing review contracts remain compatible.

## Linked Features

- [Feature 090 - Review Adoption of Central Mode Orchestrator](/Users/tino/PhpstormProjects/forge/docs/features/090-review-adoption-of-central-mode-orchestrator.md)

## Implemented Behavior (Current)

- Review now exposes a central orchestrator trace section (`sections.action_orchestration`) with explicit action catalog and iteration trace.
- The trace declares and validates usage of the shared orchestrator engine family.
- Resolved and unresolved target paths now both surface orchestrator metadata with deterministic done reasons.
- Regression coverage now enforces this via `gate_review_central_orchestrator_adoption`.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_review_central_orchestrator_adoption` passes.

## Known Limits / Notes

- Review orchestration currently runs as bounded single-cycle execution; this is compatible with future richer multi-cycle orchestration.
