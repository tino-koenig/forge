# Strict Invalid-Target No-Write Contract for Init

## Description

Guarantee that init invalid-target failures remain diagnostic-only and cannot create filesystem artifacts.

## Addresses Issues

- [Issue 50 - Init Invalid Target Can Create Directory Tree via History Persistence](/Users/tino/PhpstormProjects/forge/docs/issues/50-init-invalid-target-can-create-directory-tree-via-history-persistence.md)

## Spec

- Ensure invalid target path failures short-circuit before any persistence path can create directories/files.
- Keep explicit error messaging and actionable next-step guidance.

## Definition of Done

- Failed init on missing target path leaves path absent.
- No `.forge` directories/files are created for invalid-target failures.
- Regression test enforces no-write guarantee.
