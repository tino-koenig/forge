# Explain Analysis Foundation Extraction

## Description

Refactor explain internals into reusable core foundations while preserving deterministic behavior.

## Addresses Issues

- [Issue 27 - Explain Pipeline Is Monolithic and Not Foundationized](/Users/tino/PhpstormProjects/forge/docs/issues/27-explain-pipeline-is-monolithic-and-not-foundationized.md)

## Spec

- Extract reusable components for:
  - facet extraction primitives
  - dependency/resource edge extraction
  - evidence/inference shaping
- Keep mode entrypoint focused on wiring and output.
- Ensure compatibility with existing explain contracts.

## Definition of Done

- Explain core logic is split into focused core modules with tests.
- Mode-level code size/responsibility is substantially reduced.
- Existing explain outputs remain backward-compatible.
