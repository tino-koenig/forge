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
