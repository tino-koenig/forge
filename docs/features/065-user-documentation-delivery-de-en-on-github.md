# User Documentation Delivery on GitHub (DE/EN)

## Description

This feature defines how Forge should deliver end-user documentation on GitHub with first-class bilingual support (German/English).

Primary goals:
- publish clear user documentation for adoption and daily usage
- support DE/EN from day one with predictable URLs
- keep documentation contribution and release workflow simple for maintainers

## Problem

Current documentation is repository-internal and feature-focused.
For user onboarding and trust, Forge needs a public, structured, navigable documentation surface that is easy to maintain.

## Delivery methods on GitHub (evaluated)

### Option A: `docs/` Markdown only (rendered in repository)

Pros:
- zero infrastructure
- simple PR-based contribution flow

Cons:
- weak navigation/search experience
- weak bilingual UX (manual cross-linking)
- less discoverable for non-contributors

Suitability:
- good as bootstrap only

### Option B: GitHub Wiki

Pros:
- quick to start
- built-in GitHub editing workflow

Cons:
- weaker structured i18n workflows
- weaker long-term structure/versioning for product docs
- GitHub itself recommends Pages for indexable docs and larger docs sets

Suitability:
- acceptable for informal notes, not ideal as primary DE/EN product docs

### Option C: GitHub Pages + Docusaurus

Pros:
- native i18n system with locale-aware structure
- strong docs UX (navigation, search integration, versioning model)
- good fit for bilingual documentation at scale
- deployable via GitHub Actions

Cons:
- JS toolchain overhead
- initial setup larger than plain Markdown

Suitability:
- **recommended primary option**

### Option D: GitHub Pages + MkDocs Material (+ i18n plugin)

Pros:
- strong docs UX
- excellent Markdown authoring flow
- good DE/EN support via static i18n plugin
- good fit if Python tooling is preferred

Cons:
- multilingual setup depends on plugin conventions
- i18n integration is less native than Docusaurus core i18n

Suitability:
- strong alternative, especially for Python-centric teams

## Recommendation

Preferred solution:
- **GitHub Pages + Docusaurus with built-in i18n**

Why:
- DE/EN is a core requirement and should be native, not bolted-on
- stable locale routing (`/de/`, `/en/`) and translation workflows
- scalable for later growth (guides, reference, tutorials, policy docs)

Strong alternative:
- GitHub Pages + MkDocs Material + `mkdocs-static-i18n`

Decision guardrail:
- choose Docusaurus unless team strongly prefers Python docs tooling and accepts plugin-based i18n model.

## Scope

Define and implement documentation delivery foundation:
- docs site generator selection
- GitHub Pages deployment pipeline via GitHub Actions
- DE/EN information architecture
- contribution workflow for bilingual docs changes
- ownership and quality checks

## Proposed information architecture (DE/EN)

Top-level sections for both languages:
- Getting Started
- Installation
- Core Commands
- Trust & Safety
- Runtime Settings & Sessions
- LLM Setup (Local / OpenAI-compatible)
- Recipes / Common Workflows
- Troubleshooting
- FAQ

Language model:
- English as default locale (`/` or `/en/`)
- German as second locale (`/de/`)
- every user-facing core page has DE and EN counterpart

## URL and hosting model

- host on GitHub Pages from this repository
- project pages URL pattern: `https://<org-or-user>.github.io/<repo>/`
- locale paths:
  - EN: `/` (or `/en/`)
  - DE: `/de/`

## Authoring and maintenance model

- docs source lives in repository under version control
- PR template includes checklist:
  - EN updated
  - DE updated (or flagged intentionally pending)
  - links validated
- docs CI checks:
  - build succeeds
  - internal links valid
  - locale parity check for required pages

## Rollout plan

1. choose generator (Docusaurus default)
2. scaffold docs site and enable DE/EN locales
3. configure GitHub Actions deployment to Pages
4. migrate essential user docs (quickstart, trust, llm setup, commands)
5. add locale parity and link checks in CI

## Definition of Done

- user documentation is publicly available on GitHub Pages
- DE/EN locales are accessible and navigable
- essential onboarding and trust docs exist in both languages
- contribution workflow for bilingual updates is documented
- CI/deploy pipeline is stable and repeatable

## Related Features

- Feature 066 defines a pragmatic MkDocs Material MVP delivery path (fast launch, strong landing page, DE/EN parity) while keeping migration path toward Docusaurus open.

## Source Notes (method suitability)

- GitHub Pages is the recommended static hosting path and supports custom build workflows via Actions.
- GitHub Docs indicates Actions as the recommended deployment/automation approach for Pages workflows.
- GitHub Wiki is valid for long-form docs but has indexing/scale caveats and is less suitable as primary product docs.
- Docusaurus provides native i18n workflows suitable for bilingual docs.
- MkDocs + Material is strong for docs UX; `mkdocs-static-i18n` provides multilingual docs builds.
