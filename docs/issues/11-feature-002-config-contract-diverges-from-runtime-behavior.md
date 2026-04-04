# Feature 002 Config Contract Diverges from Runtime Behavior

## Problem

Feature 002 specifies repo-owned functional config via:
- `.forge/defaults.yml`
- `.forge/repo.yml`

and a merge order that includes both files.

Current runtime behavior in index implementation uses hardcoded defaults plus `.forge/config.toml` enrichment settings. The documented `.forge/defaults.yml`/`.forge/repo.yml` contract is not implemented.

This creates a contract mismatch between implemented behavior and feature documentation/status.

## Required behavior

Choose one explicit direction and make docs + implementation consistent:
- either implement the specified yaml-based merge model,
- or update feature specs/status notes to reflect toml-based and hardcoded behavior.

## Done criteria

- No contradiction remains between Feature 002 spec and runtime config behavior.
- Validation docs show the canonical config sources for index path classes and enrichment settings.
- A regression/documentation check protects the chosen contract.

## Linked Features

- [Feature 105 - Index Config Contract Harmonization](/Users/tino/PhpstormProjects/forge/docs/features/105-index-config-contract-harmonization.md)
