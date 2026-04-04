# Session Default TTL for Auto-Created Sessions Is Hardcoded

## Problem

Auto-created sessions always use a fixed default TTL constant (60 minutes) with no runtime/config setting.
This limits control for teams that need shorter or longer inactivity windows.

## Evidence

- `ensure_active_session` creates sessions with `DEFAULT_TTL_MINUTES`.
- No canonical runtime setting key exists for session default TTL.
- Current runtime registry contains only output/llm/execution/access families.

## Required behavior

- Default TTL for auto-created sessions should be configurable via canonical runtime/config setting(s), with deterministic fallback to 60.
- Source tracing should reveal where effective TTL came from.

## Done criteria

- New canonical session TTL setting(s) are supported and validated.
- Auto-create path uses resolved effective TTL.
- `doctor`/`get --source` expose TTL source visibility.

## Linked Features

- [Feature 101 - Configurable Session TTL Policy via Runtime Settings](/Users/tino/PhpstormProjects/forge/docs/features/101-configurable-session-ttl-policy-via-runtime-settings.md)
