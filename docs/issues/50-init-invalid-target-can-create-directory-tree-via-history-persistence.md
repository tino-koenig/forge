# Init Invalid Target Can Create Directory Tree via History Persistence

## Problem

When init target path is invalid/missing, command returns failure but still creates target directories through run-history persistence.
This violates safety expectations and can leave unexpected artifacts.

## Evidence

Repro:
- run `forge --repo-root <missing-path> init --non-interactive --template balanced --output-format json`
- command exits with failure
- `<missing-path>/` gets created, including `<missing-path>/.forge/runs.jsonl`

The creation happens after capability returns, during global `append_run(...)` path.

## Required behavior

- Failed init on invalid target must not create target directories/files.
- Failure should remain purely diagnostic.

## Done criteria

- Missing target path remains missing after failed init.
- No `.forge` artifacts are created on invalid-target failure path.
- Regression test covers this exact scenario.

## Linked Features

- [Feature 113 - Strict Invalid-Target No-Write Contract for Init](/Users/tino/PhpstormProjects/forge/docs/features/113-strict-invalid-target-no-write-contract-for-init.md)
