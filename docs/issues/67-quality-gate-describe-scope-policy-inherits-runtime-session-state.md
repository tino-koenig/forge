# Quality Gate Describe Scope Policy Inherits Runtime/Session State

## Problem

`gate_describe_important_file_scope_policy` can fail in full-suite execution while passing in
isolated execution.

Cause:
- shared fixture repo state from earlier gates can persist runtime/session overrides.
- those overrides may alter describe ranking output and suppress the expected explicit
  fixture-subtree deprioritization rationale.

## Scope

- keep describe scope-policy assertions unchanged.
- isolate this gate from runtime/session side effects.

## Acceptance Criteria

- `gate_describe_important_file_scope_policy` passes both standalone and in full-suite order.
- gate still validates primary-scope preference and explicit fixture-subtree rationale.

## Resolution Notes

- run this gate against its own temporary fixture-repo copy instead of shared `temp_repo`.
- clear runtime override env vars (`FORGE_RUNTIME_SESSION_JSON`, `FORGE_USER_RUNTIME_TOML`)
  for the describe subprocess invocation.
- apply a gate-local runtime override (`describe.important_files.max_items=100`) via
  temporary `FORGE_USER_RUNTIME_TOML` to keep rationale metadata complete within contract limits.
