# Describe Does Not Use Central Orchestration Runtime

## Problem

Describe mode executes a mode-local sequential pipeline and does not use a central shared orchestration runtime.

## Evidence

- `modes/describe.py` drives resolve -> collect -> summarize -> render directly in `run`.
- No shared orchestration runtime is used by describe.

## Required behavior

- Describe should execute via a central orchestrator runtime reusable by modes.
- Mode-specific describe steps should be expressed as handlers/adapters over the shared engine.

## Done criteria

- Describe emits central orchestration trace metadata.
- Mode-local sequencing boilerplate is reduced.
- Output contract compatibility is preserved.

## Linked Features

- [Feature 095 - Describe Adoption of Central Mode Orchestrator](/Users/tino/PhpstormProjects/forge/docs/features/095-describe-adoption-of-central-mode-orchestrator.md)
- [Feature 079 - Central Orchestration Foundation for Modes](/Users/tino/PhpstormProjects/forge/docs/features/079-central-orchestration-foundation-for-modes.md)
