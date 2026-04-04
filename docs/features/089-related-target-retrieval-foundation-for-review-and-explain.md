# Related-Target Retrieval Foundation for Review and Explain

## Description

Create a shared deterministic related-target retrieval foundation for modes that expand context (review/explain).

## Addresses Issues

- [Issue 32 - Related-File Selection for Review Is Too Lexical and Can Add Noise](/Users/tino/PhpstormProjects/forge/docs/issues/32-related-file-selection-for-review-is-too-lexical-and-can-add-noise.md)

## Spec

- Introduce weighted related-target scoring using signals such as:
  - import/dependency links
  - directory locality
  - index metadata/path class
  - lexical fallback
- Expose rationale metadata for chosen related targets.

## Definition of Done

- Review and explain use shared related-target retrieval primitives.
- Noise from lexical collisions is reduced in fixtures.
- Output includes relation rationale for selected related targets.
