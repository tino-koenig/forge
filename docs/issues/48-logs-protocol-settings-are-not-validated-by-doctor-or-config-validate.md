# Logs Protocol Settings Are Not Validated by Doctor or Config Validate

## Problem

Invalid `logs.protocol` values are silently clamped at write time and do not fail validation checks.
This hides misconfiguration and weakens operator trust in diagnostics.

## Evidence

- Repro config:
  - `[logs.protocol]`
  - `max_events_count = -1`
  - `max_event_age_days = 0`
  - `max_file_size_bytes = 1`
- `forge --output-format json doctor` still reports `config_validation = pass`.
- Current behavior in `core/protocol_log.py` clamps values to minimums instead of surfacing validation errors.

## Required behavior

- `doctor` / `config validate` must validate `logs.protocol` ranges and report invalid values explicitly.
- Runtime should avoid silent correction without operator-visible diagnostics.

## Done criteria

- Invalid logs protocol settings produce deterministic validation findings.
- Validation messaging includes offending key/path and expected range.
- Regression tests cover malformed logs protocol config.

## Linked Features

- [Feature 110 - Logs Protocol Validation Surface in Config Diagnostics](/Users/tino/PhpstormProjects/forge/docs/features/110-logs-protocol-validation-surface-in-config-diagnostics.md)
