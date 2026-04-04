# Explain Analysis Foundation Extraction

## Description

Refactor explain internals into reusable core foundations while preserving deterministic behavior.

## Addresses Issues

- [Issue 27 - Explain Pipeline Is Monolithic and Not Foundationized](/Users/tino/PhpstormProjects/forge/docs/issues/27-explain-pipeline-is-monolithic-and-not-foundationized.md)

## Spec

- Extract reusable components for:
  - facet extraction primitives
  - dependency/resource edge extraction
  - evidence/inference shaping
- Keep mode entrypoint focused on wiring and output.
- Ensure compatibility with existing explain contracts.

## Definition of Done

- Explain core logic is split into focused core modules with tests.
- Mode-level code size/responsibility is substantially reduced.
- Existing explain outputs remain backward-compatible.

## Implemented Behavior (Current)

- Introduced `core/explain_analysis_foundation.py` as reusable explain-analysis foundation.
- Extracted facet primitives from mode-local code into core:
  - settings/defaults/llm/output/symbol extraction
  - shared explain analysis data classes and confidence helper
- `modes/explain.py` now imports these primitives instead of defining duplicates.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_explain_analysis_foundation_extraction` passes.

## Known Limits / Notes

- Dependency/resource edge extraction remains mode-local in this increment and can be extracted further in later iterations.
