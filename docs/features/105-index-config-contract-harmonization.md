# Index Config Contract Harmonization

## Description

Harmonize documented index configuration contract with actual runtime behavior.

## Addresses Issues

- [Issue 11 - Feature 002 Config Contract Diverges from Runtime Behavior](/Users/tino/PhpstormProjects/forge/docs/issues/11-feature-002-config-contract-diverges-from-runtime-behavior.md)

## Spec

- Choose one canonical direction:
  - implement documented `.forge/defaults.yml`/`.forge/repo.yml` merge model, or
  - update feature specs/docs to the implemented TOML-based contract.
- Ensure doctor/docs/status explicitly reflect the chosen contract.

## Definition of Done

- No contradiction between feature docs and runtime behavior remains.
- Config source model is clearly documented and validated.
- Regression/documentation checks prevent drift.
