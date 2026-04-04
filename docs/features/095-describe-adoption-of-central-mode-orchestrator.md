# Describe Adoption of Central Mode Orchestrator

## Description

Adopt shared central orchestration runtime for describe mode.

## Addresses Issues

- [Issue 38 - Describe Does Not Use Central Orchestration Runtime](/Users/tino/PhpstormProjects/forge/docs/issues/38-describe-does-not-use-central-orchestration-runtime.md)
- [Issue 22 - Query Orchestration Loop Is Not a Central Reusable System](/Users/tino/PhpstormProjects/forge/docs/issues/22-query-orchestration-loop-is-not-a-central-reusable-system.md)

## Spec

- Express describe flow as orchestrated actions (resolve, collect, synthesize, render).
- Reuse central orchestration engine and trace model shared with other modes.
- Preserve current describe output contracts.

## Definition of Done

- Describe runs via central orchestrator runtime.
- Describe emits orchestration trace metadata.
- Mode-local sequencing boilerplate is reduced.

## Implemented Behavior (Current)

- Describe now emits explicit orchestration trace metadata in `sections.action_orchestration`:
  - action catalog
  - iteration action trace
  - done reason
  - central engine annotation (`core.mode_orchestrator.iter_bounded_cycles`)
- Describe action trace now covers:
  - `resolve_target`
  - `collect_context`
  - `synthesize`
  - `summarize`
  - `finalize`
- Added regression gate `gate_describe_central_orchestrator_adoption`.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_describe_central_orchestrator_adoption` passes.

## Known Limits / Notes

- Describe orchestration currently runs as bounded single-cycle trace; this keeps behavior deterministic and compatible with future multi-cycle orchestration.
