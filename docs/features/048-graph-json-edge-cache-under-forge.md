# Graph JSON Edge Cache under .forge

## Description

This feature introduces a deterministic repository edge cache at `.forge/graph.json`.

Primary goals:
- persist file/symbol/resource relationships for fast reuse
- improve query/explain dependency and resource reasoning
- keep writes explicitly scoped to index/graph build workflows

## Spec

### Scope

Add a graph artifact generated from deterministic repository analysis.

Primary artifact:
- `.forge/graph.json`

Initial supported edge classes:
- `import`
- `call` (best-effort where cheaply derivable)
- `resource_read` (e.g. template/config/file loads)
- `resource_write` (if detectable)
- `symbol_def`
- `symbol_ref` (best-effort)

### Artifact schema (initial)

Top-level fields should include:
- `graph_version`
- `generated_at`
- `repo_root`
- `nodes`
- `edges`
- `stats`

Edge fields should include:
- `id`
- `kind`
- `source`
- `target`
- `evidence` (path + line anchors)
- `confidence`
- `detector`

### Ownership and mode boundaries

Only write-capable index/graph workflows may create or refresh `.forge/graph.json`.

Read-only capabilities (`query`, `explain`, `review`, `describe`, `test`) may consume graph data but must not mutate it.

### Incremental refresh policy

Graph refresh should be incremental where possible:
- recompute changed files by content hash
- invalidate dependent edges deterministically
- preserve stable edge IDs where unchanged

### Failure behavior

- graph generation failures must not corrupt existing graph artifact
- partial detector failures should degrade gracefully with explicit warnings
- index core behavior remains usable without graph artifact

## Design

### Why this feature

A deterministic graph cache enables faster and more accurate dependency-style analysis without repeatedly re-deriving relationships at query time.

### Non-goals

- no LLM-authored edge assertions written into graph by default
- no mandatory full cross-language AST parity in v1
- no requirement to commit graph artifact to repository git

## Definition of Done

- `.forge/graph.json` schema is defined and versioned
- index/graph workflow can build and refresh graph artifact
- explain/query can consume graph edges for dependency/resource answers
- read-only capabilities never write graph artifact
- docs describe graph lifecycle and fallback behavior when missing
