# Review Heuristics and Thresholds Are Hardcoded, Not Configurable

## Problem

Review detection thresholds and caps are hardcoded in mode logic, reducing adaptability and transparency.

## Evidence

- Examples in `modes/review.py`:
  - large-file thresholds (`350`, `700`)
  - per-pattern evidence limits
  - profile-based max findings (`6/10/15`)
  - related-file limits (`1/3`)
- No runtime settings keys expose these review policy parameters.

## Required behavior

- Review policy knobs should be configurable via runtime settings with source tracing.
- Defaults must remain deterministic.

## Done criteria

- Canonical review settings keys exist for major thresholds/caps.
- Effective values and sources can be inspected (`forge get --source`).
- Regression tests validate default and overridden behavior.

## Linked Features

- [Feature 088 - Review Runtime Settings Surface for Heuristic Policy](/Users/tino/PhpstormProjects/forge/docs/features/088-review-runtime-settings-surface-for-heuristic-policy.md)
