# Logs Capability Filter Is Hardcoded and Can Drift from Capability Model

## Problem

`forge logs --capability` uses a hardcoded choice list in CLI parsing.
This can drift when capabilities evolve, causing valid capabilities to be rejected or stale values to remain accepted.

## Evidence

- `forge_cmd/cli.py` defines explicit choices tuple for `--capability`.
- Capability names are already centrally defined in `core/capability_model.py`.
- The two lists are maintained separately, creating contract drift risk.

## Required behavior

- `logs --capability` choices should be derived from the canonical capability model (single source of truth).
- Parser/help output should remain deterministic and explicit.

## Done criteria

- CLI `--capability` choices are generated from the central capability model.
- Regression test fails if capability-model additions are not reflected in logs filtering.

## Linked Features

- [Feature 109 - Derive Logs Capability Filter Choices from Capability Model](/Users/tino/PhpstormProjects/forge/docs/features/109-derive-logs-capability-filter-choices-from-capability-model.md)
