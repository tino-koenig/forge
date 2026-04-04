# Explain Uses Facet Accepts Direction But Ignores It

## Problem

`explain:uses` accepts `--direction` and reports it in metadata, but behavior remains inbound-only regardless of provided direction.

## Evidence

- `modes/explain.py` builds `uses` answer from inbound edges only.
- Running `explain:uses ... --direction out` and `--direction in` produces identical inbound results.
- `sections.explain.direction` still echoes user input, creating a misleading contract.

## Required behavior

- Direction semantics must be explicit and consistent:
  - either enforce `uses => direction=in` (normalize/reject `out`),
  - or implement true bidirectional semantics.

## Done criteria

- CLI/contract behavior for `uses` + `--direction` is deterministic and non-misleading.
- Regression tests cover valid and invalid direction combinations.

## Linked Features

- [Feature 083 - Explain Facet Semantics and Argument Validation Contract](/Users/tino/PhpstormProjects/forge/docs/features/083-explain-facet-semantics-and-argument-validation-contract.md)
