# `ask:latest` Has No Distinct Freshness Behavior

## Problem

`ask:latest` currently runs the same search/retrieval policy and query-plan strategy as `ask:docs`.

Observed behavior:
- Same web mode (`docs_web_search`), same policy limits, same host-constrained plan shape.
- No recency-aware query strategy, no freshness scoring, no additional freshness metadata extraction.

This does not satisfy the promised freshness-focused intent of `ask:latest`.

## Required behavior

- `ask:latest` must apply explicit freshness strategy beyond docs preset defaults.
- Runtime output must indicate freshness policy and caveats clearly.

## Done criteria

- `ask:latest` uses distinct recency/freshness controls compared to `ask:docs`.
- Contract sections expose freshness strategy + resulting signals.
- Regression tests validate divergence from docs preset behavior.

## Linked Features

- [073-ask-latest-freshness-policy.md](/Users/tino/PhpstormProjects/forge/docs/features/073-ask-latest-freshness-policy.md)
