# Ask Ignores `access.web` Runtime Setting

## Problem

`ask:docs` and `ask:latest` execute web search/retrieval even when runtime setting `access.web` is `false`.

Observed behavior:
- Runtime registry defines `access.web` (default `false`).
- Ask mode always enters web pipeline for presets `docs|latest`.
- No policy gate blocks outbound web search/retrieval based on runtime access settings.

This breaks expected runtime access control semantics.

## Required behavior

- Ask web stages must honor effective runtime access policy.
- With `access.web=false`, web search/retrieval must be skipped deterministically and reported as policy-blocked.
- Output metadata should expose that web usage was denied by runtime policy (not network/provider fallback).

## Done criteria

- `ask:docs` / `ask:latest` with `access.web=false` do not execute web foundations.
- Contract sections include explicit policy-blocked reason.
- Regression test covers both blocked and allowed (`access.web=true`) behavior.

## Linked Features

- [072-ask-web-access-policy-and-settings-integration.md](/Users/tino/PhpstormProjects/forge/docs/features/072-ask-web-access-policy-and-settings-integration.md)
