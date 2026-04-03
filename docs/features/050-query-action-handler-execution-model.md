# Query Action Handler Execution Model

## Description

This feature defines concrete execution semantics for orchestrator actions in query mode.

Primary goals:
- map each allowed action to deterministic runtime behavior
- eliminate no-op orchestration actions
- keep action effects auditable

## Spec

### Scope

Define action handlers for query orchestration catalog:
- `search`
- `read`
- `explain`
- `rank`
- `summarize`
- `stop`

Each handler must declare:
- input state requirements
- deterministic effect on state
- budget cost accounting
- failure/fallback behavior

### Handler semantics

- `search`: extend candidate pool with bounded new matches
- `read`: collect additional evidence for selected candidates
- `explain`: derive explain feedback for selected candidates
- `rank`: recompute candidate order from current signals
- `summarize`: prepare final synthesis without modifying repo
- `stop`: terminate loop with explicit reason

### Validation

- unsupported/invalid action for current state is rejected with policy-safe fallback
- handlers must not mutate repository files

## Design

### Why this feature

Without explicit handlers, orchestration decisions cannot reliably improve result quality. This feature turns orchestration from intent-only to execution-capable behavior.

### Non-goals

- no free-form action expansion at runtime
- no capability escalation via action choice

## Definition of Done

- all catalog actions have implemented, tested handlers
- action execution changes query state deterministically
- handler-level budget accounting is visible in run metadata
- invalid actions degrade safely with explicit fallback reason
