# Runtime Session Source Metadata Consistency

## Description

Align runtime diagnostics so session source origin metadata is consistent with actual source used in resolution.

## Addresses Issues

- [Issue 4 - Runtime Scope Path Session Source Mismatch](/Users/tino/PhpstormProjects/forge/docs/issues/4-runtime-scope-path-session-source-mismatch.md)

## Spec

- If named session values participate, diagnostics should expose named-session origin (or merged origins) in session scope metadata.
- If env session payload participates, diagnostics should expose env origin explicitly.
- Source metadata should remain deterministic and human-auditable.

## Definition of Done

- `doctor` runtime section no longer reports contradictory session origin metadata.
- `sources.*` and `scope_paths.session` (or equivalent metadata field) are semantically aligned.
- Quality gate asserts consistency.
