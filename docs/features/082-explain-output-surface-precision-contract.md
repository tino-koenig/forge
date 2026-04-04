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
