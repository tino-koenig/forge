# Config Validation Does Not Report Unknown Keys

## Problem

Unknown keys in `.forge/config.toml` are silently ignored. Typoed keys degrade behavior but pass `config_validation`.

## Evidence

- Repro config:
  - `[llm]`
  - `providr = "openai_compatible"` (typo)
- `doctor` output:
  - `config_validation = pass`
  - `llm_provider = warn (no LLM provider configured)`
- No explicit unknown-key diagnostic is emitted.

## Required behavior

- Config validation should report unknown/unsupported keys (at least as warn, preferably fail in strict validation mode).
- Diagnostics should point to probable intended keys.

## Done criteria

- Unknown key diagnostics are emitted deterministically with path/key detail.
- `doctor`/`config validate` expose these findings in checks.
- Regression coverage includes typo-key scenarios.

## Linked Features

- [Feature 103 - Schema-Aware Unknown-Key Validation for Config TOML](/Users/tino/PhpstormProjects/forge/docs/features/103-schema-aware-unknown-key-validation-for-config-toml.md)
