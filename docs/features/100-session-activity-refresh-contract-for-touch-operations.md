# Session Activity Refresh Contract for Touch Operations

## Description

Ensure successful session-touching operations refresh session activity timestamps and TTL window.

## Addresses Issues

- [Issue 41 - Session Touch Operations Do Not Refresh `last_activity_at` or `expires_at`](/Users/tino/PhpstormProjects/forge/docs/issues/41-session-touch-operations-do-not-refresh-last-activity-or-expiry.md)

## Spec

- Refresh `last_activity_at` and `expires_at` for successful touch operations including:
  - `session use` (non-expired and revived)
  - `set --scope session`
  - `session clear-context`
  - other session-mutating operations
- Keep timestamp update behavior deterministic and testable.

## Definition of Done

- Touch operations advance activity timestamps.
- TTL extension is consistent across touch operations.
- Regression tests validate timestamp refresh semantics.
