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

## Implemented Behavior (Current)

- Added dedicated review quality-gate matrix aggregator:
  - `gate_review_quality_gate_matrix`
- The matrix covers:
  - path-like unresolved target behavior (no symbol fallback)
  - symbol vs file target-source behavior
  - runtime policy override behavior
  - related-target noise filtering and rationale metadata
  - central orchestrator trace contract for review
  - external rule loading and invalid-rule handling
- Matrix is integrated into `run_all_gates` as standard execution path.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_review_quality_gate_matrix` passes.

## Known Limits / Notes

- The matrix aggregates existing focused review gates for deterministic regression diagnosis while keeping individual gate granularity intact.
