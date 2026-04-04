# Source-Aware Provenance Contract

## Description

Generalize provenance reporting so evidence source is not hardcoded to repository artifacts.

Goals:
- keep provenance semantically correct across repo/web/mixed modes,
- improve downstream analytics and trust.

## Spec

### Provenance model

- provenance helper accepts explicit evidence-source classification from caller.
- supported source categories include: `repository_artifacts`, `web_search`, `web_retrieval`, `mixed`, `none`.

### Backward compatibility

- existing repository-grounded modes retain current semantics.
- ask/web modes report source-aware provenance without breaking contract shape.

## Definition of Done

- Provenance section is source-aware and deterministic.
- Ask contracts report web evidence source correctly.
- Regression tests assert provenance values for representative modes.

## Addresses Issues

- [15-ask-provenance-mislabels-web-evidence-as-repository-artifacts.md](/Users/tino/PhpstormProjects/forge/docs/issues/15-ask-provenance-mislabels-web-evidence-as-repository-artifacts.md)
