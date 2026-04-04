# Protocol Log Config Bypasses Central Config Resolution

## Problem

Protocol log settings are loaded by a local TOML reader that reads only `.forge/config.toml`.
This bypasses the central config-resolution behavior (including `.forge/config.local.toml` precedence and shared validation semantics).

## Evidence

- `core/protocol_log.py` reads only `.forge/config.toml` in `_read_protocol_log_config(...)`.
- Repro:
  - `.forge/config.toml`: `logs.protocol.max_events_count = 100`
  - `.forge/config.local.toml`: `logs.protocol.max_events_count = 1`
  - after multiple runs, active `events.jsonl` still contains many lines (`>1`), proving local override is ignored.

## Required behavior

- Protocol-log settings must use the same central config pipeline as other runtime settings.
- `.forge/config.local.toml` must be able to override repo defaults for logs behavior.
- Validation and source-tracing should be consistent with the central config contract.

## Done criteria

- Logs retention/redaction settings are resolved via a shared config foundation.
- Local override precedence works for logs settings.
- Regression coverage includes a config-local override scenario for logs protocol settings.

## Linked Features

- [Feature 108 - Centralized Logs Protocol Settings in Config Foundation](/Users/tino/PhpstormProjects/forge/docs/features/108-centralized-logs-protocol-settings-in-config-foundation.md)
