# Ask Provenance Mislabels Web Evidence as `repository_artifacts`

## Problem

Ask mode uses shared `provenance_section(...)` that hardcodes `evidence_source="repository_artifacts"`.

Observed behavior:
- Ask responses sourced from web search/retrieval still report repository evidence source.
- Provenance is semantically incorrect for web-derived evidence.

This reduces auditability and can mislead downstream analytics.

## Required behavior

- Provenance must be source-aware for ask mode (`web_search`, `web_retrieval`, `none`, mixed if needed).
- Shared provenance helper should support explicit evidence-source typing rather than hardcoded repository label.

## Done criteria

- Ask provenance reports correct evidence source for web-driven answers.
- Existing query/repo consumers keep correct repository provenance.
- Regression test verifies provenance values for ask presets.

## Linked Features

- [074-source-aware-provenance-contract.md](/Users/tino/PhpstormProjects/forge/docs/features/074-source-aware-provenance-contract.md)

## Implemented Behavior (Current)

- Shared provenance helper now supports explicit evidence-source typing.
- Ask now reports source-aware provenance categories:
  - `web_retrieval` when retrieval snippets drive evidence
  - `web_search` when search candidates drive evidence
  - `none` when no evidence anchors exist
- Query and other repository-grounded consumers keep repository provenance semantics.

## How To Validate Quickly

- `access.web=false` with ask web preset:
  - `sections.provenance.evidence_source == "none"`
- `access.web=true` with ask web preset:
  - `sections.provenance.evidence_source` reflects actual web evidence channel (`web_search` or `web_retrieval`)

## Known Limits / Notes

- `mixed` provenance category is supported by the shared helper but not yet emitted by ask’s current deterministic evidence selection path.
