# Review Path-Like Targets Fallback to Symbol Matching and Produce Misleading Findings

## Problem

When a path-like review target does not exist in the current repository, review falls back to symbol matching and may return unrelated findings.

## Evidence

- `resolve_file_or_symbol_target` tries symbol fallback after file-path resolution failure.
- Repro in this repo:
  - `python3 forge.py --llm-provider mock --output-format json --view full review src/controller.py`
- Result: target resolved as `symbol`, evidence points to unrelated file (`scripts/run_quality_gates.py`) and reports a misleading finding.

## Required behavior

- Path-like inputs (`/`, `./`, `../`, file extensions, directory separators) that cannot be resolved should not silently fall back to symbol search.
- Review should return an unresolved-target response with explicit guidance.

## Done criteria

- Path-like unresolved inputs produce deterministic unresolved-target contract, no unrelated findings.
- Symbol fallback remains available for true symbol-like payloads.
- Regression gate covers both branches.

## Linked Features

- [Feature 087 - Review Target Resolution Contract for Path-like Inputs](/Users/tino/PhpstormProjects/forge/docs/features/087-review-target-resolution-contract-for-path-like-inputs.md)
