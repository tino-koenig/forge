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

## Implemented Behavior (Current)

- Removed obsolete ask-compatibility logic from query mode (`modes/query.py`), including ask preset filtering/warnings and ask-only output sections.
- Updated CLI help wording for `forge ask` to reflect dedicated ask capability routing.
- Added quality-gate coverage to enforce explicit ask/query boundary contracts:
  - `query` output no longer exposes stale ask sections.
  - `ask:*` aliases still resolve to `capability=ask`.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Focus checks:
  - `gate_ask_query_boundary_cleanup`
  - existing ask/web gates remain green (`gate_ask_web_access_policy`, `gate_ask_latest_freshness_policy`, `gate_ask_source_aware_provenance`)

## Known Limits / Notes

- This cleanup does not change ask mode internals; it only removes stale query-side compatibility paths.
