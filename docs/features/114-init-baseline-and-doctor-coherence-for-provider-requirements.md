# Init Baseline and Doctor Coherence for Provider Requirements

## Description

Align init-generated defaults with doctor/config-validation semantics so first-run baseline is coherent.

## Addresses Issues

- [Issue 51 - Init-Generated Defaults Fail Doctor on Provider Required Fields](/Users/tino/PhpstormProjects/forge/docs/issues/51-init-generated-defaults-fail-doctor-on-provider-required-fields.md)

## Spec

- Resolve mismatch between template-generated provider defaults and required provider field diagnostics.
- Choose one consistent baseline strategy, for example:
  - do not set concrete provider until local endpoint/model is configured, or
  - keep provider but treat missing endpoint/model as onboarding-warning state (not hard-fail), or
  - generate explicit local override defaults that satisfy mandatory checks.
- Keep diagnostics explicit and operator-trustworthy.

## Definition of Done

- `init -> doctor` baseline is coherent and intentional across all templates.
- No contradictory pass/fail semantics for default onboarding path.
- Regression matrix validates template-wise behavior.
