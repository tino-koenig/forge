# Query Progress Scoring and Stop Criteria

## Description

This feature introduces explicit progress scoring to decide whether additional orchestration iterations are useful.

Primary goals:
- avoid low-value extra iterations
- stop confidently when evidence quality is sufficient
- make continuation decisions measurable

## Spec

### Scope

Define a deterministic progress score computed after each iteration.

Progress signals may include:
- new high-signal candidate paths in top results
- improved top confidence/linkage confidence
- increased evidence quality and coverage
- reduced ambiguity in summary intent alignment

### No-progress policy

If progress remains below threshold for configurable consecutive iterations, orchestration must stop with `done_reason = no_progress`.

### Budget interplay

Progress scoring must work together with hard budgets:
- even high progress cannot bypass budget ceilings
- low progress should stop before exhausting budgets where appropriate

### Output and trace

Query output should expose concise progress context in full diagnostic views:
- per-iteration progress score
- stop trigger (sufficient evidence, no progress, or budget)

## Design

### Why this feature

Bounded loops still need quality-aware stopping to avoid wasted latency and token cost. Progress scoring provides predictable, inspectable continuation logic.

### Non-goals

- no opaque black-box stopping heuristic
- no LLM-only stopping decision without deterministic checks

## Definition of Done

- deterministic progress score is computed per iteration
- no-progress stopping is implemented and tested
- done_reason selection reflects progress and budget outcomes
- full diagnostics include progress and stop rationale
