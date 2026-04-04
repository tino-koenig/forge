# Central Orchestration Foundation for Modes

## Description

Extract orchestration runtime from mode-local query logic into a central reusable core foundation.

Goals:
- make orchestration available across modes
- reduce duplicated state-machine logic in mode modules
- preserve explicit, auditable behavior

## Addresses Issues

- [Issue 22 - Query Orchestration Loop Is Not a Central Reusable System](/Users/tino/PhpstormProjects/forge/docs/issues/22-query-orchestration-loop-is-not-a-central-reusable-system.md)

## Spec

### Central runtime

- Add a core orchestration engine that handles:
  - bounded iteration lifecycle
  - budget accounting
  - done-reason transitions
  - progress tracking and stop criteria
  - iteration trace accumulation

### Mode adapter contract

- Modes provide:
  - action catalog
  - deterministic handler implementations
  - mode policy boundaries
  - mode-specific sections serialization
- Engine remains mode-agnostic.

### Migration scope

- First migrate query to the central engine.
- Add one additional mode using the same engine to validate reusability.

## Definition of Done

- Query orchestration loop is no longer primarily implemented inline in `modes/query.py`.
- Shared engine lives under `core` with stable adapter contracts.
- Existing query orchestration output structure remains backward-compatible.
