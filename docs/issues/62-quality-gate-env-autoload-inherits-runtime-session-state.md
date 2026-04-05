# Quality Gate `.env` Autoload Inherits Runtime/Session State from Earlier Gates

## Problem

`gate_env_file_autoload` can fail in full-suite execution while passing standalone.

Reason:
- the gate runs on the shared fixture repo after earlier gates that persist runtime/session state.
- inherited state (for example `llm.mode` overrides) can suppress LLM usage and invalidate `.env` autoload assertions.

## Scope

- isolate `gate_env_file_autoload` from prior runtime/session side effects.
- keep assertion intent focused on `.env` key loading and config-provider preservation.

## Acceptance Criteria

- gate passes both standalone and after stateful runtime/session gates.
- `gate_runtime_settings_foundation,gate_env_file_autoload` sequence passes in one run.

## Resolution Notes

- before running the gate, remove `.forge/runtime.toml` and `.forge/sessions/` in the shared fixture repo.
- clear runtime-related environment overrides (`FORGE_RUNTIME_SESSION_JSON`, `FORGE_USER_RUNTIME_TOML`) for the subprocess env.
