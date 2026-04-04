# Query Planner-to-Retrieval Priority Contract

## Description

Define a strict transfer contract from planner priorities to deterministic retrieval weighting.

Goals:
- preserve planner intent ordering in retrieval
- prevent generic terms from dominating anchor terms
- keep planner output interpretable and auditable

## Addresses Issues

- [Issue 21 - Query Planner Term Ordering Can Overweight Generic Terms](/Users/tino/PhpstormProjects/forge/docs/issues/21-query-planner-term-ordering-can-overweight-generic-terms.md)

## Spec

### Priority mapping

- Retrieval weighting must be driven by planner priority buckets first:
  - lead terms (anchor)
  - support terms (qualifier)
  - fallback search terms
- If `search_terms` order conflicts with lead/support priority, lead/support takes precedence in effective weighting.

### Deterministic safeguards

- Generic classifier terms (`where`, `code`, `location`, `function`, `module`, etc.) cannot outweigh concrete lead terms.
- Planner output normalization must enforce stable ordering and dedup semantics.

### Observability

- Query output should expose effective weighted term order used for retrieval.

## Definition of Done

- Effective retrieval order visibly places concrete anchor terms first for locate-definition queries.
- Generic terms remain supportive and cannot outrank exact identifier signals.
- Quality gates validate planner-to-retrieval mapping.
