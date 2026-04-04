# Derive Logs Capability Filter Choices from Capability Model

## Description

Use the canonical capability model as single source of truth for `forge logs --capability` accepted values.

## Addresses Issues

- [Issue 47 - Logs Capability Filter Is Hardcoded and Can Drift from Capability Model](/Users/tino/PhpstormProjects/forge/docs/issues/47-logs-capability-filter-is-hardcoded-and-can-drift-from-capability-model.md)

## Spec

- Generate CLI logs capability filter choices from `core.capability_model.Capability` values.
- Keep parser help explicit and deterministic.
- Add guard test that fails on drift between model and CLI choices.

## Definition of Done

- Adding a capability in the model automatically updates accepted `logs --capability` values.
- No duplicated hardcoded capability tuple remains for logs filter parsing.
- Regression gate catches future drift.
