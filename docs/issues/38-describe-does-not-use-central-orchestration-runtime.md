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

## Implemented Behavior (Current)

- Describe now exposes a central orchestrator trace section (`sections.action_orchestration`) with explicit action catalog and iteration trace.
- The trace declares usage of the shared orchestrator engine family.
- Describe resolved-target flows now include deterministic orchestration metadata without breaking existing describe contract fields.
- Regression coverage added via `gate_describe_central_orchestrator_adoption`.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_describe_central_orchestrator_adoption` passes.

## Known Limits / Notes

- Current describe orchestration uses bounded single-cycle execution with explicit trace output.
