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
