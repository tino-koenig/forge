# Query Deterministic Symbol-First Resolution

## Description

This feature adds a deterministic symbol-first resolution step for locate-definition questions before broad lexical ranking.

Goal:
- return precise file/location answers when symbol evidence already exists,
- reduce dependence on generic lexical terms,
- keep behavior transparent and auditable.

## Spec

### Trigger

For queries whose intent is definition/location of code entities (function/class/variable), run a symbol-first stage.

### Resolution strategy

- Use exact and normalized symbol candidates from index metadata first.
- If exact symbol matches exist, prioritize those candidates ahead of generic lexical matches.
- Attach explicit evidence type (`symbol_exact`, `symbol_prefix`, etc.) and confidence.

### Fallback

If symbol stage has no usable evidence, continue with existing lexical/path/summary/graph ranking.

## Design

### Why this feature

A symbol already present in `.forge/index.json` should dominate generic terms like `function`/`definition`.

### Non-goals

- no opaque LLM-only resolution
- no mandatory AST pipeline

## Definition of Done

- Definition queries with exact indexed symbol resolve to the defining file in top results.
- Output shows symbol-stage evidence explicitly.
- Regression test covers `enrich_detailed_context`-style query and prevents fallback to filler-term dominance.
