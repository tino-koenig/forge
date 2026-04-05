# Output Contract Foundation Parallel Core Bootstrap

## Description

Implement Foundation 10 as a new parallel core output-contract foundation with central section builders, stable section status semantics, contract validation, and JSON-first human-view derivation.

## Spec

- Add `OutputContract`, `SectionBuilderResult`, `ContractDiagnostic`.
- Build contracts from structured input (`SectionInput`) via central section builders.
- Keep `sections` as mapping with stable required keys.
- Enforce section status semantics: `available|not_applicable|omitted|fallback`.
- Keep JSON contract as source of truth; derive human views from JSON without adding semantics.
- Keep diagnostics/policy_violations/limits semantically separated.
- Preserve normative status/done_reason semantics from Foundation 02 (no reinterpretation).

## Definition of Done

- Core builder API and validator exist in `core/output_contract_foundation.py`.
- Required section-key mapping is stable and versioned.
- Human views (`compact|standard|full`) are derived from contract payload only.
- Unit tests cover section status, contract version, minimum semantics, separation guarantees, and normative status passthrough.

## Implemented Behavior (Current)

- Added parallel foundation module `core/output_contract_foundation.py`.
- Added central section-builder base with per-section schema allowlists and section diagnostics.
- Added contract core assembler (`build_contract_core`) and schema checks (`validate_contract_schema`).
- Added human-view renderer (`render_view`) derived directly from contract payload.

## How To Validate Quickly

1. Run `python3 -m unittest tests/test_output_contract_foundation.py`.
2. Verify required section-key mapping and section status semantics.
3. Verify views reflect contract status/done_reason without reinterpretation.

## Known Limits / Notes

- This change is intentionally parallel and does not replace existing mode output/render paths.
- Advanced V2 result-type and proposal/execution section-classification is intentionally deferred.
