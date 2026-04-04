# Doctor Read-Only Contract Violated by Session Side Effects

## Problem

`forge doctor` is specified as read-only, but it can create/update session artifacts due to session auto-activation in CLI bootstrap.

## Evidence

- Repro:
  - remove `.forge/sessions`
  - run `python3 forge.py --repo-root <repo> --output-format json doctor`
  - observed creation of `.forge/sessions/index.json` and `auto-*.json`
- `config validate` alias path does not trigger the same write in equivalent run, creating behavior inconsistency.
- Relevant flow:
  - runtime-consuming capability set includes `doctor`
  - bootstrap calls `ensure_active_session(...)` before capability execution

## Required behavior

- Doctor/config-validate must remain strictly read-only: no session auto-create and no activity writes.
- Alias behavior (`doctor` vs `config validate`) must be semantically equivalent for side effects.

## Done criteria

- Running `doctor` does not create/modify `.forge/sessions/*`.
- `doctor` and `config validate` have consistent side-effect behavior.
- Regression gate asserts read-only behavior for both entrypoints.

## Linked Features

- [Feature 102 - Read-Only Capability Guard for Session Auto-Activation](/Users/tino/PhpstormProjects/forge/docs/features/102-read-only-capability-guard-for-session-auto-activation.md)
