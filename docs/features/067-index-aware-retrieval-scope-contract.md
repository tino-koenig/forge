# Index-Aware Retrieval Scope Contract

## Description

This feature defines a single deterministic retrieval-scope contract between index producers and read-only consumers (especially `query`).

Goal:
- make index participation states actionable in retrieval,
- keep behavior explicit,
- avoid hidden path-class drift between indexing and query-time scanning.

## Spec

### Scope

Apply the contract to read-only capabilities that scan repository files (`query` first, then `describe`/`review`/`test` where applicable).

### Retrieval semantics

When index exists:
- `hard_ignore`: never scanned/read.
- `index_exclude`: excluded from default retrieval.
- `low_priority`/`normal`/`preferred`: eligible for default retrieval.

When index is missing:
- fallback behavior remains available via repo scan.

### Explicit overrides

Add explicit source-scope toggles (or equivalent deterministic controls) to include `index_exclude` paths when needed.

### Transparency

Output should expose effective retrieval scope in machine-readable sections (for example source caps/scope metadata).

## Design

### Why this feature

Today indexing and retrieval can diverge in practice. A shared scope contract removes ambiguity and reduces noisy candidates.

### Non-goals

- no hidden auto-expansion into excluded paths
- no index mandatory requirement

## Definition of Done

- Query default retrieval honors index participation state when index is present.
- Explicit override path exists for including `index_exclude` sources.
- Regression fixture covers high-noise `vendor` scenario.
- JSON/full outputs expose the effective scope decision.
