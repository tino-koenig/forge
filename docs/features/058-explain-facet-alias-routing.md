# Explain Facet Alias Routing

## Description

This feature adds explicit facet aliases for explain so focused analysis can be requested directly from the command name.

Primary goals:
- reduce friction for facet-oriented explain usage
- keep mode semantics explicit while improving ergonomics
- preserve backwards compatibility with `forge explain`

## Spec

### Scope

Add alias commands that map deterministically to `forge explain --focus <facet>`.

Initial aliases:
- `forge explain:overview <target>`
- `forge explain:symbols <target>`
- `forge explain:dependencies <target>`
- `forge explain:resources <target>`
- `forge explain:uses <target>`
- `forge explain:settings <target>`
- `forge explain:defaults <target>`
- `forge explain:llm <target>`
- `forge explain:outputs <target>`

### CLI behavior

- Aliases are syntactic sugar only; capability remains `explain`.
- Existing `forge explain ... --focus ...` remains canonical and fully supported.
- If both alias and `--focus` are given and differ, return a clear CLI validation error.
- Existing `--direction` and `--source-scope` options remain available for relevant facets.

### Output and provenance

- Output contract should include:
  - `sections.explain.focus`
  - `sections.explain.focus_source` (`alias` or `flag`)
- `from-run` behavior and mode-transition metadata remain unchanged.

### Compatibility constraints

- No changes to read/write effect boundaries.
- No hidden fallback to other capabilities.
- Existing scripts using `forge explain` must remain stable.

## Design

### Why this feature

Users often think in concrete question forms ("explain dependencies", "explain outputs"). Alias routing keeps behavior explicit while making that intent fast to express.

### Non-goals

- no new analysis semantics by itself
- no auto-switching between facets
- no generic "agent" loop

## Definition of Done

- explain facet aliases are available and documented in CLI help
- aliases resolve to the same runtime behavior as `--focus`
- conflict handling between alias and `--focus` is deterministic and user-visible
- output contract records resolved focus and source
- quality gates cover alias routing and conflict behavior

## Implemented Behavior (Current)

- Implementation status: implemented.
- Traceability: `CHANGELOG.md` references feature 058; status and notes are indexed in `docs/status/features-index.md`.
- Added explain facet alias commands:
  - `explain:overview`, `explain:symbols`, `explain:dependencies`, `explain:resources`, `explain:uses`
  - `explain:settings`, `explain:defaults`, `explain:llm`, `explain:outputs`
- Added `--focus` to `forge explain` with the same facet set.
- Alias routing is deterministic: alias commands resolve to capability `explain` with fixed focus.
- Conflict validation is explicit: mismatched alias focus and `--focus` values produce a CLI error.
- Explain output contract now includes focus provenance:
  - `sections.explain.command`
  - `sections.explain.focus`
  - `sections.explain.focus_source`

## How To Validate Quickly

- Run alias:
  - `forge --view full explain:dependencies core/llm_observability.py`
- Run canonical focus:
  - `forge --view full explain --focus dependencies core/llm_observability.py`
- Validate conflict handling:
  - `forge explain:dependencies --focus outputs core/llm_observability.py`
  - expected: deterministic CLI error
- Validate JSON provenance:
  - `forge --output-format json explain:settings core/config.py`
  - inspect `sections.explain`

## Known Limits / Notes

- Alias routing currently standardizes focus/provenance only; deeper facet analysis behavior is implemented per facet feature.
- `--direction` / `--source-scope` remain reserved for facet-specific implementations and are not universally active for every alias.
