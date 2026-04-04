# Ask and Web Foundations Lack Regression Quality Gates

## Problem

No quality gates or tests currently target ask command behavior and web foundation integration.

Observed behavior:
- `scripts/run_quality_gates.py` contains no `ask`/web-search/web-retrieval gates.
- Current regressions can ship without automated detection (policy gating, provenance, preset divergence).

## Required behavior

- Add explicit ask/web integration gates and focused test fixtures.
- Cover success, fallback, policy-blocked, and no-network scenarios.

## Done criteria

- Quality gate suite includes ask/web checks.
- Core ask preset contracts and provenance fields are asserted in CI.
- Deterministic no-network path is validated without brittle external dependencies.

## Linked Features

- [075-ask-and-web-quality-gates.md](/Users/tino/PhpstormProjects/forge/docs/features/075-ask-and-web-quality-gates.md)
