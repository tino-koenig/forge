# Graph JSON Edge Cache under .forge

## Description

This feature introduces deterministic graph edge caches for repository and optional framework sources.

Primary goals:
- persist file/symbol/resource relationships for fast reuse
- improve query/explain dependency and resource reasoning
- keep writes explicitly scoped to index/graph build workflows
- support large framework ecosystems via reusable versioned graph artifacts

## Spec

### Scope

Add graph artifacts generated from deterministic analysis.

Primary repository artifact:
- `.forge/graph.json`

Optional framework artifact model (shared/team cache):
- framework graph manifests and shards addressed by `framework_id@version`
- local repo config may reference these artifacts read-only (for example TYPO3 version pins)
- repo workflows must not rewrite shared framework artifacts implicitly

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
- `source_type` (`repo` | `framework`)
- `source_id` (for example `repo:<absolute-root>` or `framework:typo3@12`)
- `nodes`
- `edges`
- `stats`

Node fields should include:
- `id`
- `kind`
- `source_type`
- `source_id`
- `path` (for file-like nodes)
- optional framework metadata (`framework_id`, `framework_version`, `package`)

Edge fields should include:
- `id`
- `kind`
- `source`
- `target`
- `evidence` (path + line anchors)
- `confidence`
- `detector`
- `source_type`
- `source_id`

### Ownership and mode boundaries

Only write-capable index/graph workflows may create or refresh repo-local graph artifacts under `.forge/`.

Read-only capabilities (`query`, `explain`, `review`, `describe`, `test`) may consume graph data but must not mutate it.

Shared framework graph artifacts are read-only from repository workflows by default.

### Incremental refresh policy

Graph refresh should be incremental where possible:
- recompute changed files by content hash
- invalidate dependent edges deterministically
- preserve stable edge IDs where unchanged

Framework scalability policy:
- support sharded graph storage by package/namespace to avoid monolithic loads
- load only needed framework shards for active query scope
- allow max-node/max-edge safety caps per source

### Failure behavior

- graph generation failures must not corrupt existing graph artifact
- partial detector failures should degrade gracefully with explicit warnings
- index core behavior remains usable without graph artifact
- missing/unavailable framework graph should degrade to repo-only behavior with explicit note

## Design

### Why this feature

A deterministic graph cache enables faster and more accurate dependency-style analysis without repeatedly re-deriving relationships at query time. Versioned shared framework graphs reduce duplicate indexing cost across teams.

### Non-goals

- no LLM-authored edge assertions written into graph by default
- no mandatory full cross-language AST parity in v1
- no requirement to commit graph artifact to repository git
- no default indexing of entire framework codebases on every repo run

## Definition of Done

- `.forge/graph.json` schema is defined and versioned
- index/graph workflow can build and refresh repo graph artifact
- framework graph references by `framework_id@version` are supported for read-only consumption
- explain/query can consume graph edges for dependency/resource answers
- read-only capabilities never write graph artifact
- docs describe graph lifecycle and fallback behavior when missing
