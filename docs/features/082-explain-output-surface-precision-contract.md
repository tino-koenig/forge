# Explain Output Surface Precision Contract

## Description

Tighten `explain:outputs` extraction so output claims require producer evidence rather than passive string mentions.

## Addresses Issues

- [Issue 25 - Explain Output Surface Detection Overmatches Non-Output Lines](/Users/tino/PhpstormProjects/forge/docs/issues/25-explain-output-surface-detection-overmatches-non-output-lines.md)

## Spec

- Distinguish producer evidence (write/log/emit calls) from descriptive text/path mentions.
- Do not classify output surfaces solely by `.forge/` or `.jsonl` string presence.
- Keep confidence aligned to evidence strength.

## Definition of Done

- False positives from passive path mentions are eliminated.
- Output facet evidence remains human-auditable and deterministic.
- Regression fixtures validate precision.

## Implemented Behavior (Current)

- `extract_output_surfaces` now requires producer semantics for output classification.
- Passive `.forge/` or `.jsonl` string mentions are no longer sufficient evidence.
- Added regression gate `gate_explain_output_surface_precision` to lock this behavior.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_explain_output_surface_precision` passes.

## Known Limits / Notes

- Heuristics remain static-pattern based; dynamic/runtime writes that do not appear in readable producer calls may remain undetected.
