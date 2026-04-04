# Describe Unresolved Target Falls Back to Repo Summary

## Problem

When `describe` receives an unresolved explicit target, it silently falls back to repository-level description instead of reporting unresolved target semantics.

## Evidence

- `resolve_describe_target` returns `kind="repo"` with `source="fallback"` when neither path nor symbol resolves.
- Code path: `/Users/tino/PhpstormProjects/forge/core/analysis_primitives.py` (`resolve_describe_target`).
- Repro:
  - `python3 forge.py --llm-provider mock --output-format json --view full describe src/does_not_exist.py`
  - Result: `sections.target.kind = "repo"`, repository summary emitted, no unresolved warning.

## Required behavior

- Explicit unresolved targets must produce an unresolved-target contract (or explicit unresolved target state), not a repo fallback answer.
- Implicit empty payload (`forge describe`) must continue to describe the repository root.

## Done criteria

- Unresolved explicit payload yields deterministic unresolved output with guidance.
- Empty payload still maps to repo overview.
- Regression tests cover both branches.

## Linked Features

- [Feature 092 - Describe Target Resolution Contract for Explicit Unresolved Inputs](/Users/tino/PhpstormProjects/forge/docs/features/092-describe-target-resolution-contract-for-explicit-unresolved-inputs.md)
