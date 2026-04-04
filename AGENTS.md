

# AGENTS.md

## Project

Forge is a transparent, composable AI-assisted repo tool for understanding, reviewing, testing, documenting, and improving code.

Forge is built around explicit modes, visible tool usage, and understandable workflows. It should remain useful in small, focused tasks without relying on hidden automation.

Core idea:
- with control, not magic

## Product direction

Forge is not meant to be a vague "run an agent" shell.

It should evolve as a repo-first workbench with explicit modes such as:
- query
- review
- test
- describe
- later: fix
- later: implement
- later: issue

Advanced workflows must be built from the same understandable foundations as the basic ones.

## Priorities

1. Keep the architecture explicit and easy to inspect.
2. Prefer small, composable building blocks over hidden orchestration.
3. Keep the core useful without heavy configuration.
4. Make outputs understandable and auditable by humans.
5. Preserve a clear separation between core functionality and optional sharpening through profiles, rules, or templates.

## Principles

### Explicit over implicit
Forge should prefer clear modes, visible steps, and predictable behavior over hidden automation.

### Composable, not magical
Complex workflows should be built from simple, understandable parts.

### AI where it helps
AI should be used for interpretation, summarization, prioritization, and proposal generation — not to hide core logic.

### Human-auditable by default
Results should be grounded in file paths, matches, findings, commands, or generated artifacts that a human can inspect.

### Local-first, repo-first
Forge should work directly against a real repository and remain useful without platform lock-in.

### Configuration sharpens, it does not define
Profiles, rules, templates, and overrides should refine behavior, not become the center of the product.

## Current scope

Primary public v1 focus:
- query
- review
- describe
- test drafting

Later workflows:
- fix
- implement
- issue-driven flows

Do not prematurely optimize for full autonomy.

## Implementation guidance

### Architecture
- Prefer a clear, boring architecture over clever abstraction.
- Keep modules focused and small.
- Avoid hidden control flow where possible.
- Make it easy to understand how a mode works from reading the code.

### Code readability and maintainability
- Prefer code that looks like careful human project code, not generated code.
- Reuse existing repo patterns before introducing new helpers, abstractions, or layers.
- Prefer straightforward control flow and explicit data movement over compact cleverness.
- Keep functions small, purpose-specific, and easy to test.
- Use names that describe domain intent, not temporary implementation detail.
- Avoid speculative generalization, one-off abstractions, and "future-proofing" without a current need.
- Comments should explain intent, constraints, or non-obvious decisions — not restate the code.
- When several valid implementations exist, choose the one that is easiest for a human maintainer to read six months later.

### CLI design
- Prefer explicit subcommands such as `forge query`, `forge review`, `forge test`, `forge describe`.
- Do not make a generic `run everything` style command the primary interface.
- Keep command behavior predictable and mode-specific.

### Tools
- Build strong foundational tools first.
- Basic tools should remain useful on their own.
- Favor transparent tool pipelines such as search → read → analyze → answer.
- Avoid turning core functionality into an opaque agent loop too early.


### Change discipline
- Prefer narrow, well-scoped changes over broad rewrites.
- Touch the minimum number of files necessary to deliver the feature correctly.
- Avoid incidental renames, drive-by refactors, or style-only churn unless they are required for the task.
- Keep diffs reviewable and easy to map to the requested behavior.
- Before introducing a new shared component, helper, or abstraction, check whether an existing one can be reused directly.

### Change strategy by work type
- For issue and bugfix work, prefer the smallest correct change that fixes the problem.
- For issue and bugfix work, fix first; do not bundle broad refactors into the same change unless they are required for correctness or safety.
- For issue and bugfix work, minimize blast radius and avoid touching unrelated parts of the system.
- For feature work, prefer focused implementation, but allow structural changes when they clearly improve the feature fit, consistency, or maintainability.
- Do not use a feature as a pretext for unrelated large-scale rewrites.
- If a feature requires a broader refactor, keep the reason explicit and limit the change strictly to what the feature needs.
- Features may reshape local structure, but must preserve reviewability and clear scope.

### Configuration and profiles
- Keep default behavior useful with little or no configuration.
- Add profiles and overrides only where they clearly sharpen repo understanding or workflow quality.
- Do not let configuration complexity become the product.
- Repo- or user-specific conventions should be configurable, not hardcoded.

### Review and analysis
- Review results should contain concrete evidence.
- Prefer findings with file paths, snippets, or rationale over vague judgments.
- Heuristics are acceptable, but they should be visible and explainable.

### Test support
- Start with test drafting and test planning before ambitious autonomous test workflows.
- Respect existing test conventions in a repository when possible.
- Prefer grounded test generation over generic boilerplate.

### Fixes and implementation
- Later fix and implementation flows must build on the same explicit foundation.
- Avoid introducing a separate black-box "agent mode" that bypasses the architecture.
- Changes should remain inspectable and understandable.

## Non-goals

Forge should not become:
- a configuration-first framework
- a generic autonomous agent shell
- a prompt box with hidden behavior
- a platform-specific product at its core

## Working style for coding agents

When working in this repository:
- preserve explicitness
- preserve clarity over cleverness
- avoid unnecessary framework layers
- avoid introducing hidden automation
- prefer readable, human-maintainable code over compressed or overly abstract code
- follow existing repository patterns before inventing new ones
- keep control flow straightforward and inspectable
- keep functions and modules focused on one responsibility
- avoid speculative extensibility and overengineering
- keep diffs narrow and directly related to the requested change

When adding new functionality:
1. keep the user-facing mode clear
2. keep the internal tool flow understandable
3. keep the implementation easy to inspect
4. keep the defaults useful
5. keep configuration optional and secondary

### Delivery standard for coding agents
Before finalizing a change, verify that:
- the result matches an existing repo style or intentionally extends it in a consistent way
- naming is specific and understandable without extra explanation
- the change does not introduce abstraction that is only used once without a strong reason
- comments explain why when needed, not what the code obviously does
- the diff is small enough that a human reviewer can understand it quickly
- the final code would still feel reasonable if no AI tooling had been involved

## Decision standard

When multiple implementation options are possible, prefer the option that best satisfies this order:
1. clarity for a human reader
2. consistency with existing repo patterns
3. explicit and inspectable behavior
4. small, reviewable diff size
5. extensibility only where it serves an immediate need

Do not choose a more abstract design merely because it appears more flexible.

### Change tracking (mandatory)
- Every implementation change must be mapped to at least one Feature ID (`docs/features/...`) or Issue ID (`docs/issues/...`).
- Product/application changes must be documented in `CHANGELOG.md`.
- Changelog entries must explicitly include the referenced Feature ID or Issue ID.
- Documentation-only updates (feature specs, roadmap text, wording cleanups) do not require `CHANGELOG.md` entries.
- If no matching Feature/Issue exists yet, define one first and then reference it in the changelog entry.

### Implemented-doc addendum (mandatory)
- For every Feature/Issue marked `implemented`, keep the spec and an implementation addendum in the same document.
- Add (or maintain) these sections at the end of implemented docs:
  - `## Implemented Behavior (Current)`
  - `## How To Use` (or `## How To Validate Quickly` when usage is not command-facing)
  - `## Known Limits / Notes`
- Keep the addendum concise and operational. Prefer concrete commands and observable behavior over architecture narrative.
- When behavior changes later, update both:
  - `CHANGELOG.md`
  - the implementation addendum in the corresponding feature/issue doc
- Do not set an item to `implemented` in `docs/status/status-overrides.toml` unless the corresponding feature/issue document has been updated in the same change.

## Definition of success

A successful Forge change should make the project:
- more understandable
- more composable
- more useful for real repo work
- more transparent in behavior
- easier to extend without becoming magical

## Short reminder

Forge is a transparent repo tool with AI assistance.
It should help with real repository work from analysis to implementation, while keeping both behavior and code understandable to humans.
It should remain understandable by humans at every stage.

**With control, not magic.**
