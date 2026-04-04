# Query Token-Aware Matching and Exact-Term Retrieval Contract

## Description

Improve query retrieval precision by replacing substring-based matching with token/identifier-aware matching.

Goals:
- eliminate false positives from short generic fragments
- preserve deterministic behavior
- keep symbol/identifier anchors dominant for locate-definition intents

## Addresses Issues

- [Issue 20 - Query Substring Matching Causes False-Positive Retrieval](/Users/tino/PhpstormProjects/forge/docs/issues/20-query-substring-matching-causes-false-positive-retrieval.md)

## Spec

### Matching contract

- Content matching must use token-aware logic (word/identifier boundaries), not unconstrained substring checks.
- Identifier-like terms (snake_case, camelCase, dotted names) should be matched exactly or via bounded structural decomposition.
- Generic short terms should not match inside unrelated identifiers by default.

### Ranking contract

- Exact identifier hits in code/symbol channels must outrank incidental generic token hits.
- Evidence should reflect match type explicitly (for example `identifier_exact`, `identifier_token`, `symbol_exact`).

### Compatibility

- Existing output contract remains stable; only evidence quality and ranking improve.

## Definition of Done

- Query no longer matches `ist` against `exists`/`list`/`dist` in content channel.
- Definition query for `enrich_detailed_context` resolves to `modes/query.py` in top result under mock planner.
- Regression gates cover DE and EN locate-definition phrasings.
