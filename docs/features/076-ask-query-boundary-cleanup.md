# Ask/Query Boundary Cleanup

## Description

Remove obsolete compatibility remnants and align user-facing wording with the dedicated ask capability architecture.

Goals:
- keep mode boundaries explicit,
- reduce dead-path complexity,
- avoid contradictory UX messaging.

## Spec

### Cleanup scope

- retire legacy ask-preset logic from query mode when no longer used.
- update CLI/help/docs wording that still claims ask maps to query.
- keep command routing and capability model explicit and auditable.

## Definition of Done

- Query mode contains no stale ask-only ranking/filter compatibility path.
- CLI/help text reflects current ask capability model.
- Regression checks assert command-to-capability routing remains correct.

## Addresses Issues

- [19-stale-ask-logic-remains-in-query-and-cli-wording.md](/Users/tino/PhpstormProjects/forge/docs/issues/19-stale-ask-logic-remains-in-query-and-cli-wording.md)
