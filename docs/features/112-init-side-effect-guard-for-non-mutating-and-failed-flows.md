# Init Side-Effect Guard for Non-Mutating and Failed Flows

## Description

Prevent repository mutations for init flows that are informational, preview-only, or precondition-failed.

## Addresses Issues

- [Issue 49 - Init Non-Mutating Flows Create `.forge` Marker via Run History](/Users/tino/PhpstormProjects/forge/docs/issues/49-init-non-mutating-flows-create-forge-marker-via-run-history.md)

## Spec

- Introduce explicit policy: non-mutating init outcomes must skip run-history persistence and marker creation.
- Covered flows:
  - `init --list-templates`
  - `init --dry-run`
  - precondition failures (non-tty interactive, invalid template, invalid target)
- Keep successful write-intent init behavior unchanged.

## Definition of Done

- Non-mutating and failed init flows produce no `.forge` artifacts in fresh dirs.
- Successful init still records history normally.
- Regression matrix covers all listed flows.
