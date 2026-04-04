# Explain Does Not Use Central Orchestration Runtime

## Problem

Explain executes a fixed inline pipeline and does not use a shared mode-agnostic orchestration runtime.
This conflicts with the goal of a centrally available orchestrator reusable by multiple modes.

## Evidence

- `modes/explain.py` runs sequencing inline (resolve target -> gather evidence -> facet extraction -> summary refinement -> render).
- No central orchestration engine is called from explain.
- Existing orchestration logic is currently query-centric.

## Required behavior

- Explain should adopt a shared orchestration runtime (same core engine family used by other modes).
- Mode-specific explain actions/facets should be implemented as handlers/adapters.

## Done criteria

- Explain executes through central orchestrator runtime with explicit action trace.
- Mode-level orchestration code in explain is minimized.
- Output contract compatibility is preserved.

## Linked Features

- [Feature 086 - Explain Adoption of Central Mode Orchestrator](/Users/tino/PhpstormProjects/forge/docs/features/086-explain-adoption-of-central-mode-orchestrator.md)

## Implemented Behavior (Current)

- Explain now exposes a central-orchestrator runtime/trace section (`sections.action_orchestration`) with explicit action catalog and iteration trace.
- The section declares and validates usage of the shared orchestrator engine family.
- Regression coverage now enforces the orchestrator trace contract.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_explain_central_orchestrator_adoption` passes.

## Known Limits / Notes

- Current explain orchestration trace runs as a bounded single-cycle flow; extension to richer multi-cycle behavior remains compatible with this contract.
