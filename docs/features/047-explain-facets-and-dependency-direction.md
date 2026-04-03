# Explain Facets and Dependency Direction

## Description

This feature extends `forge explain` from generic target description to explicit analysis facets.

Primary goals:
- answer focused technical questions with less ambiguity
- expose deterministic dependency direction (`out` and `in`)
- improve explain usefulness for integration and resource tracing

## Spec

### Scope

Add facet-oriented explain modes so users can request specific analysis intent.

Initial facets:
- `overview` (default)
- `symbols`
- `dependencies`
- `resources`
- `uses`

Direction control for dependency-like facets:
- `--direction out` (what target calls/loads/imports)
- `--direction in` (what references/uses target)

Source scope control:
- `--source-scope repo_only` (default)
- `--source-scope framework_only`
- `--source-scope all`

### CLI

Examples:
- `forge explain core/llm_integration.py --focus overview`
- `forge explain core/llm_integration.py --focus dependencies --direction out`
- `forge explain core/llm_integration.py --focus dependencies --direction in`
- `forge explain core/llm_integration.py --focus resources`
- `forge explain core/llm_integration.py --focus dependencies --direction out --source-scope all`

If `--focus` is omitted, behavior remains `overview`-first for backwards compatibility.

### Output contract additions

Explain sections should include facet-specific sections when requested.

For dependency facets:
- `dependency_edges_out`
- `dependency_edges_in`

For resource facets:
- `resource_edges` (e.g. template/config/file reads)

Each edge should include:
- source path
- target path (or unresolved raw reference)
- edge kind
- evidence anchors (file + line)
- confidence level
- `source_type` and `target_type` (`repo|framework|external`)
- optional framework identity (`framework_id`, `framework_version`) when applicable

### Read-only guarantees

Explain remains strictly read-only.

It may consume index/graph artifacts under `.forge/`, but must not mutate repository files.

## Design

### Why this feature

Current explain output is strong for local file interpretation but weak for directional dependency questions. Facet-based explain keeps UX explicit while improving precision for real engineering tasks.

### Non-goals

- no hidden write operations
- no mandatory language-specific deep semantic graph in first version
- no speculative dependency claims without evidence anchors
- no default expansion to entire framework universes when `repo_only` already answers the question

## Definition of Done

- explain supports `--focus` and `--direction` for relevant facets
- explain can answer both dependency directions with evidence-backed edges
- explain can expose resource edges (e.g. prompt/template file usage)
- explain output contracts include facet-specific edge sections
- read-only behavior is preserved
- explain supports source-scoped dependency/resource analysis with explicit source typing
