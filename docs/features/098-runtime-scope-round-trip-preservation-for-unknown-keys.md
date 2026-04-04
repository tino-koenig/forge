# Runtime Scope Round-Trip Preservation for Unknown Keys

## Description

Preserve unknown/non-registry keys when writing repo/user runtime scope files via `forge set`.

## Addresses Issues

- [Issue 3 - Runtime `set` Overwrites Unknown Scope Keys](/Users/tino/PhpstormProjects/forge/docs/issues/3-runtime-set-overwrites-unknown-scope-keys.md)

## Spec

- Runtime file update must be non-destructive for unknown keys/tables.
- Known canonical key writes should merge into existing payload rather than replacing whole file content with recognized keys only.
- Deterministic formatting should remain stable.

## Definition of Done

- Unknown keys survive `forge set --scope repo|user` updates.
- Target key updates remain deterministic and auditable.
- Regression tests cover unknown-key preservation.
