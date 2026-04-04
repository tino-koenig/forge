# Stale Ask Logic Remains in Query and CLI Wording

## Problem

Ask was split into dedicated capability, but query still contains legacy ask-preset logic and CLI help text still says ask "maps to query".

Observed behavior:
- `modes/query.py` contains `apply_ask_preset(...)` and ask-specific warnings.
- CLI help string for `ask` claims mapping to query, although runtime routes to `Capability.ASK`.

This increases cognitive load and risks behavior drift between ask and query paths.

## Required behavior

- Remove/retire legacy ask-only logic from query where no longer needed.
- Align CLI help and docs with current ask capability architecture.

## Done criteria

- Query no longer contains obsolete ask-preset compatibility flow.
- CLI/help text reflects dedicated ask mode accurately.
- Regression checks ensure command routing remains explicit and correct.

## Linked Features

- [076-ask-query-boundary-cleanup.md](/Users/tino/PhpstormProjects/forge/docs/features/076-ask-query-boundary-cleanup.md)
