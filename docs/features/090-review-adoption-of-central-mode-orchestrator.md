# Review Adoption of Central Mode Orchestrator

## Description

Adopt shared central orchestration runtime for review mode.

## Addresses Issues

- [Issue 33 - Review Does Not Use Central Orchestration Runtime](/Users/tino/PhpstormProjects/forge/docs/issues/33-review-does-not-use-central-orchestration-runtime.md)
- [Issue 22 - Query Orchestration Loop Is Not a Central Reusable System](/Users/tino/PhpstormProjects/forge/docs/issues/22-query-orchestration-loop-is-not-a-central-reusable-system.md)

## Spec

- Model review flow as orchestrated actions (resolve, detect, aggregate, summarize, finalize).
- Keep deterministic policy boundaries and explicit tracing.
- Reuse central orchestrator engine shared with other modes.

## Definition of Done

- Review runs through central orchestrator runtime.
- Mode-local sequencing boilerplate is reduced.
- Backward compatibility for review contracts is preserved.

## Implemented Behavior (Current)

- Review now emits explicit orchestration trace metadata in `sections.action_orchestration`:
  - action catalog
  - iteration action trace
  - done reason
  - central engine annotation (`core.mode_orchestrator.iter_bounded_cycles`)
- Review action trace now covers:
  - `resolve_target`
  - `detect`
  - `expand_related`
  - `aggregate`
  - `summarize`
  - `finalize`
- Added regression gate `gate_review_central_orchestrator_adoption`.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_review_central_orchestrator_adoption` passes.

## Known Limits / Notes

- Current review orchestration is a bounded single-cycle trace; this preserves deterministic behavior while exposing a reusable central orchestration surface.
