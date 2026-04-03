# Query Orchestration Iterative State Machine

## Description

This feature upgrades query orchestration from a single decision pass to a bounded multi-iteration state machine.

Primary goals:
- execute orchestration decisions as a real loop
- make each iteration explicit and inspectable
- preserve strict budget and policy boundaries

## Spec

### Scope

Introduce a canonical query loop state and iterate until stop conditions are met.

Required state fields:
- question and planner context
- candidate set and ranking snapshot
- evidence payload
- iteration counter
- budget usage (`tokens`, `files`, `wall_time_ms`)
- last decision and done reason

### Loop protocol

Each iteration must follow:
1. decision request (`continue|stop` + `next_action`)
2. policy and schema validation
3. action execution
4. state update
5. stop evaluation

### Termination

Loop must terminate with one explicit `done_reason`:
- `sufficient_evidence`
- `budget_exhausted`
- `policy_blocked`
- `no_progress`

### Guardrails

- max iterations must be enforced at runtime
- no hidden extra iterations beyond configured bounds
- invalid decisions must route to deterministic fallback and terminate safely

## Design

### Why this feature

Current orchestration quality is limited when only one decision cycle is executed. A bounded state machine allows controlled adaptive retrieval without losing transparency.

### Non-goals

- no unbounded autonomous loop
- no write actions in query mode

## Definition of Done

- query orchestration executes multiple iterations when needed
- state transitions are explicit and logged per iteration
- done reasons are deterministic and reproducible
- budget and policy bounds are enforced in every iteration
