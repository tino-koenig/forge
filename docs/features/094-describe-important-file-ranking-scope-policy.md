# Describe Important-File Ranking Scope Policy

## Description

Constrain repository-level important-file ranking to prefer primary project scope and reduce fixture/example noise.

## Addresses Issues

- [Issue 37 - Describe Important-File Selection Can Surface Irrelevant Fixture Paths](/Users/tino/PhpstormProjects/forge/docs/issues/37-describe-important-file-selection-can-surface-irrelevant-fixture-paths.md)

## Spec

- Add deterministic scope-aware ranking signals (root proximity, index participation/path class, repository area role).
- Deprioritize fixture/example/test subtree candidates for repo-overview next-step selection.
- Emit rationale metadata for selected important files.

## Definition of Done

- Important-file output favors primary repo entry/config paths in fixture-heavy repos.
- Next-step suggestions are less noisy and more actionable.
- Regression tests cover fixture-dense repositories.
