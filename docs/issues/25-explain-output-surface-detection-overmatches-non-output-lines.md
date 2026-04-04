# Explain Output Surface Detection Overmatches Non-Output Lines

## Problem

`explain:outputs` can classify non-output lines as output surfaces due to broad regex patterns.

## Evidence

- In `modes/explain.py`, `extract_output_surfaces` matches any `.forge/` and `.jsonl` text as output evidence.
- This allows passive string mentions (for example printed status text) to be labeled as artifact/log output producers.
- Example observed: `.forge/*` surface inferred from status print line in `modes/query.py`.

## Required behavior

- Output surfaces must require producer semantics (write/emit/log APIs), not mere path-string mentions.
- Confidence levels should reflect evidence quality and not overstate weak matches.

## Done criteria

- `explain:outputs` no longer reports artifact/log surfaces from plain path mentions alone.
- Evidence categories distinguish producer APIs from descriptive strings.
- Regression gate covers false-positive examples.

## Linked Features

- [Feature 082 - Explain Output Surface Precision Contract](/Users/tino/PhpstormProjects/forge/docs/features/082-explain-output-surface-precision-contract.md)

## Implemented Behavior (Current)

- Output surface extraction now classifies outputs only when producer APIs/calls are present.
- Passive path mentions (`.forge/...`, `.jsonl`) no longer generate output-surface findings.
- Regression gate coverage was added for mention-only false-positive cases.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_explain_output_surface_precision` passes.

## Known Limits / Notes

- Detection remains deterministic and lexical; runtime-only emission paths may require future deeper analysis.
