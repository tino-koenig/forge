# Explain Facet Quality Gate Matrix

## Description

Add dedicated quality gates for explain facets and option combinations.

## Addresses Issues

- [Issue 24 - Explain Facet Regression Coverage Is Incomplete](/Users/tino/PhpstormProjects/forge/docs/issues/24-explain-facet-regression-coverage-is-incomplete.md)

## Spec

- Add gates for:
  - alias/flag parity (`explain:<facet>` vs `explain --focus`)
  - `settings`, `defaults`, `llm`, `outputs`, `symbols`
  - `dependencies/resources/uses` with `--direction` and `--source-scope`
- Include negative tests for conflicting/invalid argument combinations.

## Definition of Done

- Explain facet matrix is covered by deterministic gates.
- CI failure pinpoints facet contract regressions.
