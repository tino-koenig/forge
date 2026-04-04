# Review Target Resolution Contract for Path-like Inputs

## Description

Define deterministic resolution behavior for review targets that look like paths.

## Addresses Issues

- [Issue 30 - Review Path-Like Targets Fallback to Symbol Matching and Produce Misleading Findings](/Users/tino/PhpstormProjects/forge/docs/issues/30-review-path-like-targets-fallback-to-symbol-matching-and-produce-misleading-findings.md)

## Spec

- Detect path-like payloads early.
- If unresolved as repo file/path, return unresolved-target response without symbol fallback.
- Keep symbol fallback for symbol-like payloads.

## Definition of Done

- Path-like unresolved inputs no longer produce unrelated symbol-based findings.
- Target-source semantics are explicit and correct in output contracts.
- Regression tests cover path-like and symbol-like branches.

## Implemented Behavior (Current)

- Review now detects path-like payloads (`/`, `./`, `../`, separators, file suffixes) before symbol resolution.
- For path-like payloads, review resolves file targets only:
  - resolved file -> regular review flow (`target_source=file`)
  - unresolved path -> deterministic unresolved response, no symbol fallback
- Symbol fallback remains active for symbol-like payloads (for example `compute_price`).
- Added regression gate `gate_review_path_like_target_resolution_contract`.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_review_path_like_target_resolution_contract` passes.

## Known Limits / Notes

- The path-like guard is currently enforced in review mode target resolution; other modes keep their own target resolution semantics.
