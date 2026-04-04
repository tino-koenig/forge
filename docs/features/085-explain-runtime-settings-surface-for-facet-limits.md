# Explain Runtime Settings Surface for Facet Limits

## Description

Expose explain extraction limits and thresholds as runtime settings with source-traceable resolution.

## Addresses Issues

- [Issue 28 - Explain Analysis Limits Are Hardcoded, Not Runtime Configurable](/Users/tino/PhpstormProjects/forge/docs/issues/28-explain-analysis-limits-are-hardcoded-not-runtime-configurable.md)

## Spec

- Add canonical settings for explain limits (examples):
  - `explain.evidence.max_items`
  - `explain.edges.max_items`
  - `explain.settings.max_items`
  - `explain.defaults.max_items`
  - `explain.outputs.max_items`
- Resolve via runtime settings foundation precedence and expose effective values/sources.

## Definition of Done

- Hardcoded explain extraction caps are replaced by resolved settings with deterministic defaults.
- `forge get --source` reports origins for explain keys.
- Regression tests cover default and overridden limit behavior.
