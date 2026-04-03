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
- source-scope behavior (`repo_only`, `framework_only`, `all`)

### Handler semantics

- `search`: extend candidate pool with bounded new matches
- `read`: collect additional evidence for selected candidates
- `explain`: derive explain feedback for selected candidates
- `rank`: recompute candidate order from current signals
- `summarize`: prepare final synthesis without modifying repo
- `stop`: terminate loop with explicit reason

Source-aware requirements:
- `search` and `rank` must preserve source attribution for each candidate/evidence
- default flow should prioritize repo candidates before framework expansion
- framework handlers must enforce dedicated caps to stay bounded on large ecosystems (for example TYPO3)

### Validation

- unsupported/invalid action for current state is rejected with policy-safe fallback
- handlers must not mutate repository files
- handlers must not mutate shared framework artifacts

## Design

### Why this feature

Without explicit handlers, orchestration decisions cannot reliably improve result quality. This feature turns orchestration from intent-only to execution-capable behavior.

### Non-goals

- no free-form action expansion at runtime
- no capability escalation via action choice
- no unbounded framework crawl caused by `search` action

## Definition of Done

- all catalog actions have implemented, tested handlers
- action execution changes query state deterministically
- handler-level budget accounting is visible in run metadata
- invalid actions degrade safely with explicit fallback reason
- source-aware execution and caps are enforced per handler
