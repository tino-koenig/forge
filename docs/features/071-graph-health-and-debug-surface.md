# Graph Health and Debug Surface

## Description

Add explicit graph health diagnostics for operators and CI.

Goals:
- make graph readiness visible,
- explain why graph was ignored or degraded,
- reduce deep manual inspection for graph-related failures.

## Spec

### Diagnostic content

Provide structured checks for:
- graph file presence and parseability
- schema/version validity
- node/edge counts and cap saturation status
- incremental reuse stats sanity (`reused_files`/`rebuilt_files`)
- framework ref status (loaded/missing/invalid)

### Interface

Expose in deterministic machine-readable form (and concise human output) via doctor/status command surface.

## Design

### Why this feature

Graph behavior is central for query/explain quality but currently hard to audit quickly when results degrade.

### Non-goals

- no runtime mutation of graph artifacts during diagnostics

## Definition of Done

- Graph health checks are available in CLI diagnostics.
- Output is actionable and references concrete artifact paths/ref ids.
- Regression tests assert warning/error paths for invalid graph scenarios.
