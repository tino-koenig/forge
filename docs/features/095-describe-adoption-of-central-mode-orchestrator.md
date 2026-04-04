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
