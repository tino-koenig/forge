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

## Implemented Behavior (Current)

- Init baseline no longer sets `llm.provider` in generated `.forge/config.toml`.
- Provider wiring is now explicitly guided via `.forge/config.local.toml` example.
- Resulting baseline: `config_validation=pass`, `llm_provider=warn` (onboarding), no hard-fail contradiction directly after init.

## How To Validate Quickly

- Run `forge init --template balanced --non-interactive --force`.
- Run `forge --output-format json doctor` and confirm:
  - `checks.config_validation.status == pass`
  - `checks.llm_provider.status == warn`
  - overall doctor status is not `fail`
- Repeat for templates `strict-review` and `lightweight`.

## Known Limits / Notes

- A configured `provider=openai_compatible` without required fields still fails validation (see feature 104).
- This feature adjusts onboarding baseline behavior; it does not weaken provider-required validation.
