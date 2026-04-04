# Explain Adoption of Central Mode Orchestrator

## Description

Adopt the shared central orchestration runtime for explain mode.

## Addresses Issues

- [Issue 29 - Explain Does Not Use Central Orchestration Runtime](/Users/tino/PhpstormProjects/forge/docs/issues/29-explain-does-not-use-central-orchestration-runtime.md)
- [Issue 22 - Query Orchestration Loop Is Not a Central Reusable System](/Users/tino/PhpstormProjects/forge/docs/issues/22-query-orchestration-loop-is-not-a-central-reusable-system.md)

## Spec

- Use central orchestrator runtime for explain with explicit action catalog, for example:
  - resolve_target
  - collect_evidence
  - extract_facet
  - synthesize
  - summarize
  - finalize
- Keep deterministic policy boundaries and bounded budgets.
- Expose iteration/action trace in full/json views.

## Definition of Done

- Explain no longer relies on a mode-local orchestration pipeline as primary control flow.
- Shared orchestrator services at least query + explain.
- Regression tests verify parity with previous explain behavior.

## Implemented Behavior (Current)

- Explain now emits explicit orchestration trace metadata in `sections.action_orchestration`:
  - action catalog
  - iteration action trace
  - done reason
  - central engine annotation (`core.mode_orchestrator.iter_bounded_cycles`)
- Trace covers the explain pipeline stages (`resolve_target`, `collect_evidence`, `extract_facet`, `synthesize`, `summarize`, `finalize`).
- Added regression gate `gate_explain_central_orchestrator_adoption`.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_explain_central_orchestrator_adoption` passes.

## Known Limits / Notes

- This increment introduces central orchestrator trace/runtime surface for explain; deeper multi-iteration explain orchestration can evolve on top of the same engine contract.
