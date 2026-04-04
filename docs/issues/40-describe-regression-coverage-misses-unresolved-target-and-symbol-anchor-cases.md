# Describe Regression Coverage Misses Unresolved-Target and Symbol-Anchor Cases

## Problem

Current quality gates cover baseline contract shape for describe but miss critical semantic correctness cases.

## Evidence

- Existing gates validate describe JSON structure and fixture language extraction.
- No gate for explicit unresolved target behavior.
- No gate for symbol-target evidence anchoring.
- No gate for important-file ranking noise in fixture-heavy repos.

## Required behavior

- Add describe gate matrix covering semantic resolution and evidence precision behaviors.

## Done criteria

- New gates cover:
  - unresolved explicit target contract
  - symbol-anchor evidence presence
  - important-file ranking/next-step noise control
- Regressions fail deterministically with clear messages.

## Linked Features

- [Feature 097 - Describe Quality Gate Matrix Extension](/Users/tino/PhpstormProjects/forge/docs/features/097-describe-quality-gate-matrix-extension.md)
