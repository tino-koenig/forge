# Query LLM Provenance Inconsistent with Planner/Orchestrator Usage

## Problem

`forge query --output-format json` can use LLM planner/orchestrator while top-level provenance still reports deterministic-only inference.

Observed behavior:
- `sections.query_planner.usage.used = true`
- `sections.action_orchestration.usage.used = true`
- but `sections.llm_usage.used = false`
- and `sections.provenance.inference_source = deterministic_heuristics`

This creates conflicting diagnostics for features 028/029/030 and breaks expectations of LLM-path gates.

## Required behavior

- Query provenance must reflect effective LLM participation across all query LLM stages (summary refinement, planner, orchestrator).
- Top-level LLM usage reporting should remain internally consistent with stage usage sections.
- JSON output should not claim deterministic-only inference when planner/orchestrator were used.

## Done criteria

- Repro with mock provider reports consistent provenance/usage for query.
- Quality gates no longer fail due query LLM-path inconsistency.
- Query contract documents how top-level vs stage-level usage is derived.
