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
