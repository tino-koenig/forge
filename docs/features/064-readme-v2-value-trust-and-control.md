# README v2: Value, Trust & Control Positioning

## Description

This feature defines a full README redesign focused on adoption and trust.

Primary goals:
- communicate Forge value in under 60 seconds
- make **Trust & Safety** a first-class product feature
- show explicit control over readable resources and writable change scope
- position LLM strategy clearly: local/self-hosted first, OpenAI-compatible always supported

## Problem

The current README is technically solid but too long and architecture-heavy for first contact.
Potential users do not quickly see:
- immediate practical value
- concrete trust guarantees beyond generic wording
- scope boundaries (what Forge may read / may change)
- how to use own LLM infra versus OpenAI-compatible endpoints

## Scope

Create README v2 with a clear conversion-oriented structure:
1. Hero (outcome-first)
2. 60-second quickstart
3. Core use-cases (jobs-to-be-done)
4. **Trust & Safety** (main section, high prominence)
5. LLM deployment model (local/self-hosted + OpenAI-compatible)
6. concise command overview
7. roadmap and contribution links

## Naming and Branding (Mandatory)

Use the following public positioning in README v2 hero/header:
- Name/Add-on: `Forge – AI Repo Workbench`
- Subtitle: `Explicit AI for real repository work.`
- Repository slug: `forge-ai-repo-workbench`

Operational identifiers remain unchanged:
- Project name: `Forge`
- CLI command: `forge`
- Python module: `forge`

## Mandatory README v2 sections

### 1) Outcome-first hero

- short value statement
- three concrete outcomes users can achieve quickly
- one minimal command CTA

### 2) Trust & Safety (main feature section)

This section must be visually and structurally prominent.

Must include explicit policy dimensions:
- **Mode boundary**: read-only analysis vs change-capable workflows
- **Resource access scope** (read side):
  - repository files
  - Forge index artifacts
  - local docs/framework paths
  - web search/retrieval (when enabled)
- **Change scope** (write side, for future/edit modes):
  - which files can be modified
  - optional target narrowing (file/class/function)
  - dependency-change policy boundaries
- **Auditability**:
  - visible contracts
  - run history
  - explicit fallback/warnings

Recommended format:
- policy matrix/table with columns: `Capability`, `Reads`, `Writes`, `Notes`

### 3) Control surfaces

README must explain how users control behavior:
- CLI flags
- config
- (upcoming) runtime settings / sessions
- deterministic precedence concept

### 4) LLM positioning (required)

README must clearly state:
- Forge is designed to work with your own LLM setup (local/self-hosted)
- Forge supports any OpenAI-compatible provider endpoint
- default behavior remains bounded and deterministic when LLM is unavailable

Include concise examples for:
- local/self-hosted OpenAI-compatible endpoint
- provider-off fallback behavior

### 5) Quick proof section

Provide a short real output excerpt (contract-oriented) showing:
- evidence anchors
- fallback clarity
- no hidden execution steps

## Content quality requirements

- reduce conceptual repetition
- keep README concise and skimmable
- move deep technical details (long config, internals) to dedicated docs and link them
- keep wording concrete and testable, avoid vague trust claims

## Non-goals

- no full architecture deep dive in README
- no exhaustive config reference in README
- no marketing-only claims without operational evidence

## Rollout plan

1. define README v2 outline and section goals
2. draft Trust & Safety matrix from existing capability contracts
3. draft LLM deployment section (self-hosted + OpenAI-compatible)
4. add quickstart + proof snippets
5. move long config/details to dedicated docs and cross-link

## Definition of Done

- README has a clear outcome-first top section
- Trust & Safety is presented as a primary product feature
- resource-access and change-scope boundaries are explicitly documented
- LLM strategy (own infra + OpenAI-compatible) is explicit and actionable
- README length/structure improves first-time comprehension and onboarding speed

## Implemented Behavior (Current)

- `README.md` was redesigned around outcome-first onboarding and explicit control surfaces.
- Public positioning now uses:
  - `Forge - AI Repo Workbench`
  - `Explicit AI for real repository work.`
  - repository slug reference `forge-ai-repo-workbench`
- README now includes a prominent Trust & Safety policy matrix (`Capability`, `Reads`, `Writes`, `Notes`) plus explicit mode-boundary and auditability sections.
- LLM deployment guidance now explicitly covers self-hosted OpenAI-compatible endpoints and deterministic provider-off fallback behavior.

## How To Validate Quickly

1. Open `README.md` and verify section order:
   - Hero/value
   - 60-second quickstart
   - Core use-cases
   - Trust & Safety
   - Control surfaces
   - LLM deployment model
   - Quick proof excerpt
   - command overview + roadmap/contribution links
2. Verify Trust & Safety matrix includes both read-side scope and write-side boundaries.
3. Verify LLM section includes both self-hosted OpenAI-compatible configuration and provider-off fallback command.

## Known Limits / Notes

- README stays intentionally concise; deep internals and exhaustive configuration details remain in dedicated docs/spec files.
