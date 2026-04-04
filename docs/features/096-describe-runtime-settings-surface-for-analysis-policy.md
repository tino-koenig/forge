# Describe Runtime Settings Surface for Analysis Policy

## Description

Expose describe analysis limits and policy knobs via canonical runtime settings.

## Addresses Issues

- [Issue 39 - Describe Policy Thresholds and Scan Limits Are Hardcoded](/Users/tino/PhpstormProjects/forge/docs/issues/39-describe-policy-thresholds-and-scan-limits-are-hardcoded.md)

## Spec

- Add canonical describe settings (examples):
  - describe.framework_hints.max_files
  - describe.languages.max_items
  - describe.components.max_items
  - describe.important_files.max_items
  - describe.symbols.max_items
- Resolve through runtime settings precedence with source tracing.

## Definition of Done

- Hardcoded describe policy limits are replaced by resolved defaults.
- Effective values and sources are inspectable.
- Regression tests validate overridden settings behavior.
