# Logs Protocol Validation Surface in Config Diagnostics

## Description

Extend central config validation/doctor diagnostics to include `logs.protocol` settings with explicit error reporting.

## Addresses Issues

- [Issue 48 - Logs Protocol Settings Are Not Validated by Doctor or Config Validate](/Users/tino/PhpstormProjects/forge/docs/issues/48-logs-protocol-settings-are-not-validated-by-doctor-or-config-validate.md)

## Spec

- Add `logs.protocol` fields to deterministic config validation rules:
  - `max_file_size_bytes`
  - `max_event_age_days`
  - `max_events_count`
  - `allow_full_prompt_until`
- Fail validation on out-of-range/invalid values instead of silent-only clamping.
- Expose diagnostics in both `doctor` and `config validate` outputs.

## Definition of Done

- Invalid `logs.protocol` values are surfaced as validation failures/warnings with clear guidance.
- `doctor` and `config validate` remain consistent for malformed logs settings.
- Regression gate includes malformed logs config matrix.
