# Explain Settings and Defaults Facets

## Description

This feature adds two explain facets for configuration influence analysis:
- `settings`: which runtime/config inputs influence the target behavior
- `defaults`: which in-code defaults are active when no override is provided

Primary goals:
- answer "which settings affect this?" with evidence
- answer "what defaults are hardcoded?" with evidence
- keep results deterministic and auditable

## Spec

### Scope

Add explain facets:
- `--focus settings`
- `--focus defaults`

Inputs considered:
- CLI arguments
- environment variables
- repo config files (for example `.forge/config.toml`, `.forge/frameworks.toml`)
- in-code constant/default values

### Output contract additions

For `settings`:
- `settings_influences`: list of influence items with
  - `setting_key`
  - `input_channel` (`cli|env|toml|code`)
  - `effect_summary`
  - `evidence` (file + line)
  - `confidence`

For `defaults`:
- `default_values`: list with
  - `name`
  - `value_repr`
  - `activation_condition`
  - `evidence` (file + line)
  - `confidence`

Shared:
- `direct_answer` (concise plain-language answer to the facet intent)
- `uncertainty_notes` when activation/precedence cannot be fully proven from local evidence

### Deterministic-first behavior

- Extraction should be deterministic from visible code and known config structures.
- LLM may improve phrasing only; it must not invent unknown setting keys or defaults.

### Source boundaries

- Default source scope remains repo-local.
- Framework/external references may be included only when explicitly requested and anchored.

## Design

### Why this feature

Explain is currently strong on structural role but weak on operational questions ("which knobs control this behavior"). These facets close that gap without changing mode boundaries.

### Non-goals

- no runtime value inspection from live process state
- no speculative precedence resolution when code is ambiguous
- no config mutation suggestions in this feature

## Definition of Done

- `settings` and `defaults` facets are available via explain focus
- outputs include deterministic, evidence-backed settings/default entries
- direct answers are present in text and JSON output
- no fabricated keys/values in quality-gate fixtures
- read-only boundaries remain unchanged

## Implemented Behavior (Current)

- Implementation status: implemented.
- Traceability: `CHANGELOG.md` references feature 059; status and notes are indexed in `docs/status/features-index.md`.
- Explain facet aliases and focus routing can trigger:
  - `settings` -> deterministic `direct_answer` + `settings_influences`
  - `defaults` -> deterministic `direct_answer` + `default_values`
- Full text view includes dedicated blocks (`Focus Answer`, `Settings Influences`, `Default Values`) when the corresponding focus is selected.
- JSON output includes the same structured sections under `sections`.

## How To Validate Quickly

- Run:
  - `forge --view full explain:settings core/config.py`
  - `forge --view full explain:defaults core/config.py`
- Validate JSON sections:
  - `forge --output-format json explain:settings core/config.py`
  - `forge --output-format json explain:defaults core/config.py`

## Known Limits / Notes

- Detection is static and heuristic-based; dynamic runtime branches are not executed.
- Confidence remains evidence-density based and may be conservative for sparse targets.
