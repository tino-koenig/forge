# Review Quality Gate Matrix Extension

## Description

Expand review quality gates to cover target resolution and noise-sensitive scenarios.

## Addresses Issues

- [Issue 34 - Review Regression Coverage Misses Critical Target-Resolution and Noise Cases](/Users/tino/PhpstormProjects/forge/docs/issues/34-review-regression-coverage-misses-critical-target-resolution-and-noise-cases.md)

## Spec

- Add deterministic gates for:
  - path-like unresolved target handling
  - symbol-target behavior
  - related-target noise regression cases
  - external rule + baseline heuristic interaction

## Definition of Done

- Review gate suite fails on misleading target resolution/noise regressions.
- New gates are integrated into standard quality-gate execution.
