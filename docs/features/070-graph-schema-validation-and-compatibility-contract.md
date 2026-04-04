# Graph Schema Validation and Compatibility Contract

## Description

Introduce a shared deterministic graph validation contract for repo and framework graph artifacts before runtime consumption.

Goals:
- enforce minimum schema integrity,
- enforce compatible `graph_version`,
- make `graph_usage` fields truthful and auditable.

## Spec

### Validation scope

Apply to:
- `.forge/graph.json` loading
- framework refs in `[graph.framework_refs]`

### Minimal required fields

Validate presence/type for:
- `graph_version`
- `source_type`
- `source_id`
- `nodes` (list)
- `edges` (list)
- `stats` (object)

### Compatibility

- supported version set is explicit
- incompatible versions are rejected with deterministic warning

### Reporting

- runtime outputs include graph validation outcome per source
- invalid sources are excluded from `*_graph_*_loaded` fields

## Design

### Why this feature

Without validation, malformed graph payloads are silently treated as loaded, causing misleading confidence and provenance.

### Non-goals

- no auto-migration in first step
- no implicit rewriting of invalid framework artifacts

## Definition of Done

- Shared validator exists and is used by repo and framework graph loaders.
- Consumers only use validated graph payloads.
- JSON/full outputs expose validation warnings and acceptance state.
- Regression gates cover malformed dict payloads and incompatible versions.
