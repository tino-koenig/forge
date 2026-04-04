# Runtime Scope Path Session Source Mismatch

## Problem

Runtime resolution reports session key sources as `session:<name>`, but `scope_paths.session` still shows `env:FORGE_RUNTIME_SESSION_JSON`.
This produces contradictory diagnostics in `doctor` and other runtime introspection outputs.

Observed behavior:
- `sources.llm.model = "session:auto-..."`
- `scope_paths.session = "env:FORGE_RUNTIME_SESSION_JSON"`

## Required behavior

- Diagnostics must expose the actually used session source path/origin.
- When named session values are used, session scope path/origin should reflect named session storage (or explicitly show merged origins).
- Session source tracing should stay deterministic and human-auditable.

## Done criteria

- `doctor` runtime section no longer reports misleading session scope origin.
- Session source metadata clearly distinguishes env session payload vs named session store.
- Add quality-gate assertion for this metadata consistency.

## Linked Features

- [Feature 099 - Runtime Session Source Metadata Consistency](/Users/tino/PhpstormProjects/forge/docs/features/099-runtime-session-source-metadata-consistency.md)
