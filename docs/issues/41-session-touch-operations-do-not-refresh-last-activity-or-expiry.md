# Session Touch Operations Do Not Refresh `last_activity_at` or `expires_at`

## Problem

Multiple successful commands that touch an existing session do not refresh session activity timestamps.
This can leave actively used sessions appearing stale or expired.

## Evidence

- Repro on temporary fixture repo:
  - `forge session new work --ttl-minutes 1`
  - `forge set --scope session output view full`
  - `forge session use work`
- Observed `work.json` before/after values remain unchanged for:
  - `last_activity_at`
  - `expires_at`
- Relevant code paths:
  - `update_session_runtime_settings` preserves existing timestamps.
  - `use_session` updates timestamps only for expired+revive path.

## Required behavior

- Any successful command that mutates or activates a session should refresh `last_activity_at` and derived `expires_at`.
- Behavior must be deterministic across:
  - `session use`
  - `set --scope session`
  - `session clear-context`
  - other session-mutating paths

## Done criteria

- Session-touching operations advance activity timestamps.
- TTL window extends consistently after successful touch operations.
- Regression tests cover these touch paths.

## Linked Features

- [Feature 100 - Session Activity Refresh Contract for Touch Operations](/Users/tino/PhpstormProjects/forge/docs/features/100-session-activity-refresh-contract-for-touch-operations.md)
