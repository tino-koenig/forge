# Review Target Resolution Contract for Path-like Inputs

## Description

Define deterministic resolution behavior for review targets that look like paths.

## Addresses Issues

- [Issue 30 - Review Path-Like Targets Fallback to Symbol Matching and Produce Misleading Findings](/Users/tino/PhpstormProjects/forge/docs/issues/30-review-path-like-targets-fallback-to-symbol-matching-and-produce-misleading-findings.md)

## Spec

- Detect path-like payloads early.
- If unresolved as repo file/path, return unresolved-target response without symbol fallback.
- Keep symbol fallback for symbol-like payloads.

## Definition of Done

- Path-like unresolved inputs no longer produce unrelated symbol-based findings.
- Target-source semantics are explicit and correct in output contracts.
- Regression tests cover path-like and symbol-like branches.
