# Explain LLM and Output Facets

## Description

This feature adds explain facets for two operational questions:
- `llm`: which LLM components/stages are involved
- `outputs`: which outputs and side-effect channels are produced

Primary goals:
- make LLM participation explicit and evidence-backed
- make output surfaces explicit (console/json/log/artifacts)
- improve traceability for debugging and architecture review

## Spec

### Scope

Add explain facets:
- `--focus llm`
- `--focus outputs`

### Facet behavior

`llm` facet should identify:
- invocation points (for example summary refinement/planner/orchestrator calls)
- policy/mode gating sites
- provider/config dependencies
- stage boundaries (what is deterministic vs LLM-shaped)

`outputs` facet should identify:
- user-facing output channels (console sections, JSON contract fields)
- persisted artifacts (for example `.forge/...` files, logs)
- notable side effects within read-only boundaries (for example web fetches)

### Output contract additions

For `llm`:
- `llm_participation`:
  - `stage`
  - `kind` (`required|optional|disabled_by_policy|fallback`)
  - `evidence` (file + line)
  - `confidence`

For `outputs`:
- `output_surfaces`:
  - `surface` (`console|json_contract|log_file|artifact_file`)
  - `path_or_section`
  - `producer`
  - `evidence` (file + line)
  - `confidence`

Shared:
- `direct_answer`
- `uncertainty_notes`

### Presentation requirements

- Full view: show dedicated blocks `LLM Participation` and `Output Surfaces`.
- Standard/compact views: keep concise but include direct answer sentence.

### Safety and boundaries

- Explain remains read-only.
- LLM facet reports usage/participation but does not expose prompts or secrets.

## Design

### Why this feature

Many real questions are operational ("is LLM involved here?", "what does this write/log?"). These facets provide explicit, inspectable answers without broadening explain into a generic agent mode.

### Non-goals

- no runtime telemetry aggregation in this feature
- no automatic policy changes or provider rewrites
- no hidden code execution beyond normal explain read path

## Definition of Done

- `llm` and `outputs` facets are available and documented
- outputs include evidence-backed participation/surface entries
- full view presents dedicated sections
- JSON contract contains stable `llm_participation` / `output_surfaces` arrays
- quality gates validate no fabricated stages/surfaces

## Implemented Behavior (Current)

- Implementation status: implemented.
- Traceability: `CHANGELOG.md` references feature 060; status and notes are indexed in `docs/status/features-index.md`.
- Explain focus routing supports:
  - `llm` -> deterministic `direct_answer` + `llm_participation`
  - `outputs` -> deterministic `direct_answer` + `output_surfaces`
- Full text view includes dedicated blocks:
  - `LLM Participation`
  - `Output Surfaces`
- JSON output includes the same structured arrays under `sections`.

## How To Validate Quickly

- Run:
  - `forge --view full explain:llm modes/query.py`
  - `forge --view full explain:outputs modes/ask.py`
- Validate JSON sections:
  - `forge --output-format json explain:llm modes/query.py`
  - `forge --output-format json explain:outputs modes/ask.py`

## Known Limits / Notes

- Detection is static and pattern-based; runtime execution paths are not evaluated.
- Stage/surface confidence is heuristic and evidence-density based.
