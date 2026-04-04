# Web Search Policy Entrypoints Are Not Used in Query Planning

## Problem

Web search policy includes `entrypoints`, but search query planning ignores them.

Observed behavior:
- `build_web_search_policy(...)` computes normalized entrypoints.
- `_build_query_plan(...)` only uses raw question + `site:<host>` variants.
- Entry-point-aware seeding promised by spec is not realized in execution.

This weakens targeted docs discovery and diverges from feature intent.

## Required behavior

- Query planning should incorporate entrypoints as first-class discovery seeds (or equivalent deterministic strategy).
- Output should make entrypoint usage visible.

## Done criteria

- Search query plan/selection demonstrably uses configured entrypoints.
- Behavior is covered by deterministic tests with fixture profiles.

## Linked Features

- [072-ask-web-access-policy-and-settings-integration.md](/Users/tino/PhpstormProjects/forge/docs/features/072-ask-web-access-policy-and-settings-integration.md)
