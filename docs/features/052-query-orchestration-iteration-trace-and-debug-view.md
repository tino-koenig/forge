# Query Orchestration Iteration Trace and Debug View

## Description

This feature adds iteration-level orchestration trace output for diagnostics and reproducibility.

Primary goals:
- make orchestrated query behavior inspectable by humans
- simplify debugging of retrieval decisions
- align orchestration visibility with Forge transparency principles

## Spec

### Scope

Extend query run metadata and full text diagnostics with per-iteration traces.

Each iteration trace should include:
- iteration index
- decision (`continue|stop`) and `next_action`
- decision reason and confidence
- action execution summary
- budget usage before/after
- progress score delta
- top candidate snapshot before/after
- source distribution before/after (`repo`, `framework`, optional `external`)
- source-scope and source-cap counters (for example framework-read budget remaining)

### Output integration

- JSON output includes structured `action_orchestration.iterations[]`
- text `--view full` prints compact iteration blocks

### Failure visibility

When fallback occurs, trace must show:
- fallback trigger
- blocked decision/action
- policy or validation reason
- source-scope reason when framework expansion is denied or capped

## Design

### Why this feature

Adaptive orchestration without iteration-level visibility is hard to trust and tune. Iteration traces preserve auditable control while enabling rapid quality improvement.

### Non-goals

- no verbose-by-default output in compact/standard view
- no exposure of secrets in trace payloads
- no omission of source context when source-aware orchestration is active

## Definition of Done

- iteration-level traces are emitted in JSON and full text views
- fallback and policy-block cases are traceable per iteration
- diagnostics remain concise in non-full views
- trace format is stable and documented
- source-aware decisions are inspectable from trace data alone
