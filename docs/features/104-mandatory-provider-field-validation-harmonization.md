# Mandatory Provider Field Validation Harmonization

## Description

Unify config-validation semantics so provider-required fields are part of mandatory validation status.

## Addresses Issues

- [Issue 45 - Config Validation Passes While Provider-Required Fields Are Missing](/Users/tino/PhpstormProjects/forge/docs/issues/45-config-validation-passes-while-provider-required-fields-are-missing.md)

## Spec

- Treat required provider fields (`base_url`, `model`, key reference) as mandatory validation when provider is configured.
- Keep diagnostics explicit and non-secretive.
- Align `doctor` and `config validate` reporting/status logic.

## Definition of Done

- Missing required provider fields cannot result in `config_validation: pass`.
- `doctor` and `config validate` report consistent mandatory validation status.
- Regression tests cover init-generated and malformed provider configurations.
