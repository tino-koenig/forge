# Review Regression Coverage Misses Critical Target-Resolution and Noise Cases

## Problem

Current review gates cover baseline findings and external rules, but miss critical false-positive/noise scenarios.

## Evidence

- Existing gates validate rule loading and basic finding presence.
- No gate for unresolved path-like target behavior.
- No gate for related-file noise control.
- No gate ensuring symbol-target review stays scoped and non-misleading.

## Required behavior

- Add dedicated review gate matrix for path/symbol resolution behavior and noise-sensitive scenarios.

## Done criteria

- New gates cover:
  - path-like unresolved target handling
  - symbol vs file targeting behavior
  - related-file expansion precision cases
- Regressions fail deterministically with clear messages.

## Linked Features

- [Feature 091 - Review Quality Gate Matrix Extension](/Users/tino/PhpstormProjects/forge/docs/features/091-review-quality-gate-matrix-extension.md)
