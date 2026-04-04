# Init Default Values Are Duplicated and Can Drift from Central Config Foundation

## Problem

Init renders several config defaults as literals that are also defined in central config defaults.
This duplication can drift and produce inconsistent baseline behavior across init-generated repos and runtime defaults.

## Evidence

- `modes/init.py` renders planner/orchestrator numeric defaults as literals.
- `core/config.py` also defines canonical defaults/ranges for the same settings.
- There is no shared source ensuring init output stays aligned when defaults evolve.

## Required behavior

- Use a shared default-value foundation for generated init config where values overlap with central config defaults.
- Keep template-specific overrides explicit while deriving common defaults centrally.

## Done criteria

- No duplicated literal defaults remain for overlapping planner/orchestrator baseline settings.
- Init output and central defaults stay aligned by construction.
- Regression test guards against drift.

## Linked Features

- [Feature 118 - Shared Init Default-Value Foundation with Central Config](/Users/tino/PhpstormProjects/forge/docs/features/118-shared-init-default-value-foundation-with-central-config.md)
