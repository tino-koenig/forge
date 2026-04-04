# Configurable Session TTL Policy via Runtime Settings

## Description

Expose session default TTL policy as canonical runtime/config settings for better operational control.

## Addresses Issues

- [Issue 42 - Session Default TTL for Auto-Created Sessions Is Hardcoded](/Users/tino/PhpstormProjects/forge/docs/issues/42-session-default-ttl-for-auto-created-sessions-is-hardcoded.md)

## Spec

- Add canonical setting(s) for session inactivity TTL defaults.
- Auto-create session path resolves effective TTL through runtime settings precedence.
- TTL source is visible through diagnostics/source tracing.

## Definition of Done

- Auto-created sessions use resolved TTL policy instead of fixed constant only.
- Effective TTL and source are inspectable.
- Validation and tests cover bounds and precedence.
