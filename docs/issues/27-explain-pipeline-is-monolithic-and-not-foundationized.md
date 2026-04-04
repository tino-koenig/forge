# Explain Pipeline Is Monolithic and Not Foundationized

## Problem

Explain mode currently concentrates extraction, graph integration, inference shaping, rendering, and contract assembly in one large module.
This reduces reuse and makes cross-mode consistency harder to maintain.

## Evidence

- `modes/explain.py` is ~1800+ lines and contains many distinct responsibilities in one file.
- Reusable analysis concerns (symbol extraction, dependency/resource edge derivation, facet adapters) are mode-local, not exposed as shared foundations.

## Required behavior

- Extract reusable explain-analysis primitives into core foundations.
- Keep mode entrypoint thin and orchestration-friendly.
- Preserve explicit deterministic behavior while improving composability.

## Done criteria

- Explain implementation is split into focused core modules with stable contracts.
- Mode file primarily coordinates flow and I/O.
- Existing output contracts remain compatible.

## Linked Features

- [Feature 084 - Explain Analysis Foundation Extraction](/Users/tino/PhpstormProjects/forge/docs/features/084-explain-analysis-foundation-extraction.md)

## Implemented Behavior (Current)

- Explain facet-analysis primitives were moved into a dedicated core module (`core/explain_analysis_foundation.py`).
- The explain mode now consumes this shared foundation and no longer keeps duplicate local extraction implementations.
- A regression gate verifies that foundation extraction remains in place.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_explain_analysis_foundation_extraction` passes.

## Known Limits / Notes

- This increment addresses the facet-analysis portion of the monolith; additional orchestration/runtime extraction is tracked separately.
