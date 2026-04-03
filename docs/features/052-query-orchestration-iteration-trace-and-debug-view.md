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

## Implemented Behavior (Current)

- Query emits a structured per-iteration trace in `sections.action_orchestration.iterations[]` with:
  - decision and action fields (`decision`, `next_action`, `reason`, `confidence`, `done_reason`)
  - handler execution status (`handler_status`, `handler_detail`)
  - budget transitions (`budget_files_before/after`, `budget_tokens_before/after`)
  - retrieval state transitions (`candidate_count_before/after`, `evidence_count_before/after`)
  - top candidate snapshots (`top_candidates_before`, `top_candidates_after`)
  - source-aware diagnostics:
    - `source_distribution_before`, `source_distribution_after`
    - `source_scope`, `source_scope_reason`
    - `source_caps` (`remaining_*`, framework-top counters, framework-expansion flag)
  - fallback/policy diagnostics (`fallback_trigger`, `blocked_reason`)
  - progress diagnostics (`progress_score`, `progress_passed`, `progress_components`)
- Full text view (`--view full`) prints compact iteration trace blocks including:
  - budgets before/after
  - scope/scope reason
  - top candidate snapshots
  - source distribution and caps
  - fallback/block reasons when present

## How To Validate Quickly

- Text trace:
  - `forge --view full query "Where is query orchestration implemented?"`
  - inspect `Action Orchestration -> Iterations`
- JSON trace:
  - `forge --output-format json query "Where is query orchestration implemented?"`
  - inspect `sections.action_orchestration.iterations[]`
  - inspect `sections.action_orchestration.usage.fallback_reason` for orchestrator fallback visibility

## Known Limits / Notes

- Trace data is intentionally emitted only in full diagnostics (text) and structured JSON sections; compact text output stays concise.
- Candidate snapshots are bounded summaries (top paths), not full ranked dumps.
- Source-cap diagnostics are budget/counter oriented and not yet framework-profile specific.
