# Init-Generated Defaults Fail Doctor on Provider Required Fields

## Problem

All init templates generate `provider = "openai_compatible"` but omit provider-required fields (`base_url`, `model`).
Immediately after successful init, `forge doctor` reports failures (`llm_base_url`, `llm_model`).

## Evidence

Reproduced for templates:
- balanced
- strict-review
- lightweight

Result pattern:
- init status: initialized
- doctor status: fail
- `config_validation`: pass
- `llm_base_url`: fail (`unset`)
- `llm_model`: fail (`unset`)

## Required behavior

- Fresh init baseline should not put users into immediate hard-fail doctor state by default.
- Init/default provider semantics and doctor mandatory checks should be aligned.

## Done criteria

- Post-init doctor result is coherent (no contradictory pass/fail semantics for baseline setup).
- Template output and diagnostics messaging are aligned with expected onboarding path.
- Regression test validates `init -> doctor` baseline across templates.

## Linked Features

- [Feature 114 - Init Baseline and Doctor Coherence for Provider Requirements](/Users/tino/PhpstormProjects/forge/docs/features/114-init-baseline-and-doctor-coherence-for-provider-requirements.md)
