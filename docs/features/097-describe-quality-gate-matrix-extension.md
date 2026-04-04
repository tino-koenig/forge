# Describe Quality Gate Matrix Extension

## Description

Expand describe quality-gate coverage to semantic resolution and evidence-precision cases.

## Addresses Issues

- [Issue 40 - Describe Regression Coverage Misses Unresolved-Target and Symbol-Anchor Cases](/Users/tino/PhpstormProjects/forge/docs/issues/40-describe-regression-coverage-misses-unresolved-target-and-symbol-anchor-cases.md)

## Spec

- Add deterministic gates for:
  - unresolved explicit target handling
  - symbol-target evidence anchoring
  - important-file ranking noise control
  - describe contract compatibility after policy/orchestrator changes

## Definition of Done

- New describe gates are integrated into standard quality-gate execution.
- Regressions fail with clear deterministic diagnostics.
