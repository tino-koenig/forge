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

## Implemented Behavior (Current)

- Query now derives top-level `sections.llm_usage` from aggregated stage usage:
  - `summary_refinement`
  - `query_planner`
  - `query_action_orchestrator`
- Query exposes explicit stage-level diagnostics in `sections.llm_usage.stage_usage`.
- Query provenance now uses aggregated stage participation:
  - `deterministic_heuristics+llm` when any stage used LLM
  - `deterministic_heuristics` otherwise

## How To Validate Quickly

- Run:
  - `python3 forge.py --output-format json --llm-provider mock query "compute_price"`
- Verify:
  - `sections.query_planner.usage.used == true`
  - `sections.action_orchestration.usage.used == true`
  - `sections.llm_usage.used == true`
  - `sections.provenance.inference_source == "deterministic_heuristics+llm"`
- Gate check:
  - `PYTHONPATH=. python3 -c "import shutil,tempfile; from pathlib import Path; from scripts.run_quality_gates import FIXTURE_BASIC_SRC, gate_query_llm_provenance_consistency; td=tempfile.TemporaryDirectory(prefix='forge-gate-'); repo=Path(td.name)/'repo'; shutil.copytree(FIXTURE_BASIC_SRC, repo); gate_query_llm_provenance_consistency(repo); print('ok')"`

## Known Limits / Notes

- Top-level usage aggregation reflects participation, not semantic quality of individual stage outputs.
