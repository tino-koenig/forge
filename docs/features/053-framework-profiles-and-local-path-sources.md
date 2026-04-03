# Framework Profiles and Local Path Sources

## Description

This feature introduces `frameworks.toml` as an optional source-profile registry for framework-aware retrieval.

Primary goals:
- simplify user-facing source selection (for example `ask:docs` with profile aliases)
- support team-shared framework index/graph artifacts per framework version
- support local non-git framework paths as read-only retrieval sources

## Spec

### Scope

Add optional config file:
- `.forge/frameworks.toml`

Each framework profile may define:
- identity (`id`, `version`, `label`)
- aliases (for CLI ergonomics)
- local framework paths (non-git allowed)
- optional references to framework index/graph artifacts
- docs allowlists/canonical URLs
- retrieval defaults (scope, freshness, budgets)

### Local path sources

Profiles may include local framework paths outside repository git tracking:
- `local_paths.framework_roots`
- `local_paths.framework_docs_roots`
- `local_paths.exclude_globs`

Rules:
- paths are read-only
- missing paths must not fail hard; emit warning and fallback
- all results from these paths must be marked as framework-origin sources

### Source typing and provenance

Query/explain contracts must preserve:
- `source_type` (`repo` | `framework` | `web_docs` | `web_general`)
- `source_origin` (`repo`, `framework_shared_cache`, `framework_local_unversioned`, ...)
- optional framework identity (`framework_id`, `framework_version`)

### CLI integration expectations

This feature enables simplified user commands while preserving advanced orchestration controls:
- aliases like `forge ask:repo`, `forge ask:docs`, `forge ask:latest`
- profile selection via `--profile <framework-profile>`

Advanced source/budget options remain available internally and for power users.

### Validation and fallback

If profile references cannot be resolved:
- degrade to repo-only or configured fallback policy
- surface explicit warnings in output/trace
- never perform hidden writes

## Design

### Why this feature

Framework-heavy ecosystems (for example TYPO3) are too large for repeated ad-hoc retrieval. Versioned profiles and reusable framework artifacts keep retrieval fast and explicit while reducing user-side complexity.

### Non-goals

- no mandatory framework profile requirement for normal repo usage
- no automatic indexing of entire framework trees on every query
- no secret/token storage in `frameworks.toml`

## Definition of Done

- `frameworks.toml` schema is defined and documented
- local non-git framework paths are supported as read-only sources
- source provenance includes framework/local origin typing
- profile-based framework version targeting is supported
- fallback behavior is explicit and safe when profile data is incomplete

## Implemented Behavior (Current)

- Added optional framework profile registry loader for `.forge/frameworks.toml`:
  - supports `default_profile`
  - supports profile lookup by `id` or alias
  - supports both `profiles` and `frameworks` table-array keys for compatibility
- Added query CLI profile selection:
  - `forge query --framework-profile <id-or-alias> "..."`
  - if omitted: uses `default_profile` when configured, otherwise no profile
- Added local path retrieval sources (read-only):
  - `local_paths.framework_roots` -> source type `framework`
  - `local_paths.framework_docs_roots` -> source type `web_docs`
  - `local_paths.exclude_globs` applied to local-path traversal
- Missing/invalid framework paths do not fail query:
  - warnings are emitted in diagnostics and uncertainty notes
  - query degrades safely to repo-only/index behavior when needed
- Query provenance is now source-aware in contracts:
  - `source_type` and `source_origin` added to query evidence
  - `source_origin`, `framework_id`, `framework_version` added to likely locations
  - `sections.framework_profile` exposes requested/resolved profile and warnings
- Explain contract now includes explicit source provenance fields for evidence/target (repo source baseline).

## How To Validate Quickly

- Baseline (no profile file):
  - `forge --view full query "Where is query orchestration implemented?"`
  - verify `Framework profile` section reports no active profile and no failure
- Profile selection:
  - create `.forge/frameworks.toml` with one profile and local roots
  - run `forge --view full query --framework-profile <id-or-alias> "..."`
  - verify trace and JSON show framework profile resolution and source-aware metadata
- JSON checks:
  - inspect `evidence[].source_type/source_origin`
  - inspect `sections.likely_locations[].source_origin/framework_id/framework_version`
  - inspect `sections.framework_profile`

## Known Limits / Notes

- Local framework retrieval currently supports read-only content scanning and provenance tagging; shared framework cache/index artifacts are not yet consumed.
- `source_type` values `web_general` and shared-cache `source_origin` variants are reserved for future source integrations.
- Explain remains repo-targeted; provenance fields are now explicit even for repo-only explain flows.
