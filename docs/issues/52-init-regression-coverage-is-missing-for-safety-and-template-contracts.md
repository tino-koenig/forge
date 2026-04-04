# Init Regression Coverage Is Missing for Safety and Template Contracts

## Problem

Quality gates currently do not include dedicated init coverage for critical contracts:
- non-mutating flows
- overwrite safety
- template output contracts
- init-to-doctor coherence

## Evidence

- No `gate_*` function for init-specific scenarios found in `scripts/run_quality_gates.py`.
- Existing gates cover many other features in depth but not init behavior matrix.

## Required behavior

- Add explicit init gate matrix for deterministic safety and onboarding contracts.
- Ensure regression catches side effects and template drift.

## Done criteria

- Dedicated init gates exist and run in standard quality-gate execution.
- Matrix includes dry-run/list/invalid-target/non-tty/overwrite/template variants.
- Failures are actionable with clear gate messages.

## Linked Features

- [Feature 115 - Init Quality-Gate Matrix for Safety and Template Contracts](/Users/tino/PhpstormProjects/forge/docs/features/115-init-quality-gate-matrix-for-safety-and-template-contracts.md)
