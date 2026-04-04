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
