# Init Source-Scope and Framework Policy Onboarding

## Description

Extend init to capture high-impact source-policy decisions (source scope and framework allowlist) in both interactive and non-interactive modes.

## Addresses Issues

- [Issue 54 - Init Does Not Onboard Source-Scope and Framework Policy Settings](/Users/tino/PhpstormProjects/forge/docs/issues/54-init-does-not-onboard-source-scope-and-framework-policy-settings.md)

## Spec

- Add minimal onboarding controls for source policy:
  - source scope default (`repo_only` or `all`)
  - optional framework allowlist identifiers
- Provide equivalent non-interactive flags.
- Persist selected policy in generated config files using explicit, auditable settings.

## Definition of Done

- Interactive and non-interactive init support policy selection.
- Generated config contains deterministic source-policy settings.
- Regression tests cover policy selection paths.
