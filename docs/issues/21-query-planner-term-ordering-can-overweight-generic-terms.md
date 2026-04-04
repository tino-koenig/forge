# Query Planner Term Ordering Can Overweight Generic Terms

## Problem

Planner output may still place generic terms at the front of `search_terms` for natural-language locate-definition questions, even when a concrete symbol is present.
Because ranking uses position-based term weights, this can overweight weak generic terms.

Observed example:
- lead terms include `enrich_detailed_context`
- search terms become `where, ist, enrich_detailed_context, definiert`
- ranking and evidence generation are biased toward generic terms

## Evidence

- Repro command:
  - `python3 forge.py --llm-provider mock --output-format json --view full query "Wo ist enrich_detailed_context definiert?"`
- `sections.query_planner.lead_terms` contains symbol-like anchor, but `search_terms` order starts with generic terms.
- Weighting uses term order via `build_term_weight_map` in `modes/query.py`.

## Required behavior

- Search-term ordering must prioritize concrete anchors from planner lead terms.
- Generic/support terms must not outrank anchor terms in retrieval weighting.
- Planner-to-retrieval transfer should preserve intent priority deterministically.

## Done criteria

- For locate-definition questions with identifier anchors, anchor terms are first in effective retrieval order.
- Generic terms remain support-only and cannot dominate score over exact symbol/definition evidence.
- Regression gate validates order/weight behavior.

## Linked Features

- [Feature 078 - Query Planner-to-Retrieval Priority Contract](/Users/tino/PhpstormProjects/forge/docs/features/078-query-planner-to-retrieval-priority-contract.md)
