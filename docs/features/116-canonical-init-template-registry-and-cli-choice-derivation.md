# Canonical Init Template Registry and CLI Choice Derivation

## Description

Use one canonical init template/option registry and derive CLI parser choices from it.

## Addresses Issues

- [Issue 53 - Init Template and Option Choices Are Duplicated Across CLI and Mode](/Users/tino/PhpstormProjects/forge/docs/issues/53-init-template-and-option-choices-are-duplicated-across-cli-and-mode.md)

## Spec

- Extract canonical init template metadata to a shared foundation module.
- Derive CLI `--template` choices from canonical registry.
- Where applicable, derive related option domains from canonical constants.
- Preserve deterministic help output and command UX.

## Definition of Done

- No duplicated template-id literal lists remain between CLI and mode runtime.
- Template changes propagate automatically to parser validation/help.
- Regression test enforces parser/runtime registry consistency.
