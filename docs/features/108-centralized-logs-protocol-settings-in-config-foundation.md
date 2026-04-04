# Centralized Logs Protocol Settings in Config Foundation

## Description

Move logs protocol settings to the shared config foundation so precedence, validation, and source semantics are consistent.

## Addresses Issues

- [Issue 46 - Protocol Log Config Bypasses Central Config Resolution](/Users/tino/PhpstormProjects/forge/docs/issues/46-protocol-log-config-bypasses-central-config-resolution.md)

## Spec

- Add logs protocol settings to central config resolution (including local override support).
- Replace local direct-TOML parsing in protocol log writer with resolved config usage.
- Expose settings/source diagnostics consistently in doctor/config-validate surfaces.

## Definition of Done

- Logs settings respect `.forge/config.local.toml` precedence.
- Validation diagnostics cover logs protocol limits/values.
- Regression tests prove precedence and retention behavior under resolved config.
