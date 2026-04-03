# Query Path And Symbol Signals

## Description

This feature improves query candidate retrieval by adding explicit path and symbol signals from the index to ranking.

Primary goals:
- make path hints (for example `controller`, `sitepackage`) first-class signals
- use indexed `top_level_symbols` for stronger code-target retrieval
- keep scoring robust against noisy short directory names such as `api`

## Spec

### Scope

Extend query ranking with:
- path-based retrieval/scoring from relative file path and path segments
- symbol-based retrieval/scoring from indexed `top_level_symbols`
- summary-based retrieval/scoring from indexed `explain_summary`
- existing `path_class` usage retained
- explicit retrieval-source marking per candidate/evidence (`content_match`, `path_match`, `symbol_match`, `summary_match`)

### Path scoring semantics

Signals should be explicit and bounded:
- exact filename or stem match: strong boost
- exact path-segment match: medium boost
- long-token substring in full path: weak boost
- path-fragment terms containing separators (`/`, `.`, `_`, `-`): strong boost on match
- multi-word terms should also be tokenized and matched as bag-of-tokens; this bag signal stays weaker than explicit full-fragment matches

Guardrail:
- short/common terms (length <= 3, e.g. `api`) must only add a minimal score, even on segment match
- total path boost must be capped

### Symbol scoring semantics

Use `top_level_symbols` from index entries:
- exact symbol match: strong boost
- prefix symbol match: medium boost
- long-token symbol substring: weak boost
- total symbol boost must be capped

### Summary scoring semantics

Use index enrichment `explain_summary`:
- direct multi-word term overlap: medium boost
- tokenized overlap (bag-of-tokens): weak-to-medium boost
- short/common token overlap alone must stay weak
- total summary boost must be capped

### Constraints

- keep deterministic behavior and index-optional fallback
- no hidden writes in query mode
- preserve inspectable scoring logic in code

## Design

### Why this feature

Path intent is often explicit in user questions, while content-only matching can miss or under-rank relevant candidates. Indexed symbols are similarly high-signal for function/class-focused questions.

### Non-goals

- no vector or embedding search in this feature
- no replacement of existing lexical evidence model
- no aggressive boosts for short/common directory names

## Definition of Done

- query ranking uses bounded path and symbol signals
- query ranking uses bounded summary signals from index enrichment metadata
- path retrieval is a first-class candidate channel (not only fallback)
- short common path tokens are prevented from dominating scores
- index fallback behavior remains unchanged
