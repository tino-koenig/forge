# Runtime `set` Overwrites Unknown Scope Keys

## Problem

`forge set --scope repo|user ...` rewrites the full target runtime file from recognized canonical keys only.
Unknown or future keys in the same file are silently removed.

Observed behavior:
- Existing custom table/keys in `.forge/runtime.toml` are lost after one `forge set`.
- This also drops non-registry values that should survive round-trips.

## Required behavior

- `forge set` must preserve unknown keys when updating repo/user runtime scope files.
- Updating one setting must not delete unrelated existing settings.
- Runtime settings writes should remain deterministic and inspectable.

## Done criteria

- Repro with pre-existing unknown keys keeps those keys after `forge set`.
- `forge set` updates target keys without destructive rewrite side effects.
- Add/extend quality gate coverage for preservation behavior.

## Linked Features

- [Feature 098 - Runtime Scope Round-Trip Preservation for Unknown Keys](/Users/tino/PhpstormProjects/forge/docs/features/098-runtime-scope-round-trip-preservation-for-unknown-keys.md)
