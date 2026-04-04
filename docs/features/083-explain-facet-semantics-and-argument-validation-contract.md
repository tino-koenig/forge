# Explain Facet Semantics and Argument Validation Contract

## Description

Normalize and validate explain facet argument semantics, especially for `uses` and direction handling.

## Addresses Issues

- [Issue 26 - Explain Uses Facet Accepts Direction But Ignores It](/Users/tino/PhpstormProjects/forge/docs/issues/26-explain-uses-facet-accepts-direction-but-ignores-it.md)

## Spec

- Define explicit compatibility matrix for `focus x direction x source_scope`.
- For unsupported combinations, either normalize with explicit warning or reject with clear error.
- Ensure reported metadata matches effective behavior.

## Definition of Done

- `uses` direction semantics are explicit and consistent.
- Contract metadata reflects effective behavior.
- Quality gates cover normalized and rejected combinations.
