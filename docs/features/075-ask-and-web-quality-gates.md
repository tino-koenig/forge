# Ask and Web Quality Gates

## Description

Add dedicated quality gates for ask mode and web foundations.

Goals:
- prevent silent regressions in ask preset behavior,
- enforce policy/provenance/fallback contracts,
- keep external dependency behavior deterministic in CI.

## Spec

### Gate coverage

Include checks for:
- ask preset routing and contract sections
- access policy blocked-path handling
- web search/retrieval fallback semantics under no-network or provider errors
- provenance correctness for web evidence
- `ask:docs` vs `ask:latest` behavior divergence

### Test strategy

- use deterministic fixtures/mocks for web layers where possible
- avoid brittle reliance on live internet responses in gate suite

## Definition of Done

- Quality gate suite includes ask/web gates.
- CI catches contract and policy regressions for ask presets.
- Gate logs provide actionable failure diagnostics.

## Addresses Issues

- [18-ask-and-web-foundations-lack-regression-quality-gates.md](/Users/tino/PhpstormProjects/forge/docs/issues/18-ask-and-web-foundations-lack-regression-quality-gates.md)
