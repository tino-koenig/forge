# Describe Target Resolution Contract for Explicit Unresolved Inputs

## Description

Define deterministic describe behavior for explicit targets that cannot be resolved.

## Addresses Issues

- [Issue 35 - Describe Unresolved Target Falls Back to Repo Summary](/Users/tino/PhpstormProjects/forge/docs/issues/35-describe-unresolved-target-falls-back-to-repo-summary.md)

## Spec

- Distinguish implicit repo-target invocation (`forge describe`) from explicit unresolved targets.
- For explicit unresolved targets, emit unresolved-target contract/state with guidance.
- Do not silently convert explicit unresolved targets into repo-level descriptions.

## Definition of Done

- Explicit unresolved targets do not yield repo fallback summaries.
- Implicit empty payload still yields repo overview.
- Regression tests cover both paths.

## Implemented Behavior (Current)

- Describe now distinguishes explicit unresolved payloads from implicit repo-overview invocation.
- For explicit unresolved targets, describe returns deterministic unresolved output:
  - `sections.target.kind = "unresolved"`
  - `sections.status = "unresolved_target"`
  - no repository fallback evidence
- Implicit empty payload (`forge describe`) still resolves to repository overview (`target.kind = "repo"`).
- Added regression gate `gate_describe_explicit_unresolved_target_contract`.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_describe_explicit_unresolved_target_contract` passes.

## Known Limits / Notes

- This contract applies specifically to explicit unresolved describe inputs; other mode resolution semantics remain mode-specific.
