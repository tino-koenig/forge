# Query Orchestration Loop Is Not a Central Reusable System

## Problem

The orchestration state machine and action-handler execution are largely embedded in `modes/query.py`.
This prevents reuse by other modes and duplicates orchestration concerns in mode code.

## Evidence

- `modes/query.py` contains:
  - iterative loop control
  - budget accounting
  - anti-stall overrides
  - handler execution (`search/read/explain/rank/summarize/stop`)
  - progress scoring application
  - iteration trace assembly
- `core/llm_integration.py` only returns decisions; orchestration runtime is not shared as a mode-agnostic engine.

## Required behavior

- Orchestration runtime must be a central reusable system in `core`.
- Modes should provide only mode-specific handlers/adapters and deterministic policy boundaries.
- Shared tracing, budgeting, progress policy, and done-reason mechanics should be unified.

## Done criteria

- Query uses a central orchestration engine (not mode-local loop as primary implementation).
- At least one additional mode can reuse the same orchestration foundation with mode-specific actions.
- Existing query orchestration output contract remains compatible.

## Linked Features

- [Feature 079 - Central Orchestration Foundation for Modes](/Users/tino/PhpstormProjects/forge/docs/features/079-central-orchestration-foundation-for-modes.md)
