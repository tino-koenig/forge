# Docs MVP on GitHub Pages with MkDocs Material (DE/EN)

## Description

This feature defines a pragmatic documentation MVP using MkDocs Material with a strong landing page and bilingual content (DE/EN).

Primary goals:
- launch fast with high perceived quality
- provide a strong homepage/entrypoint (product-style intro + CTA)
- deliver bilingual user docs on GitHub Pages with low maintenance overhead

## Relationship to Feature 065

- Feature 065 defines strategic delivery options and recommends Docusaurus as long-term default.
- This feature defines an **implementation-first MVP path** with MkDocs Material.
- Rationale: lower initial setup cost while still achieving a high-quality docs experience.

## Why Separate (not merged into 065)

Keep separate concerns:
- 065 = strategy and option analysis (platform-level)
- 066 = concrete MVP implementation plan (tool-specific)

This avoids rewriting strategy whenever implementation phases change.

## Scope

Implement a docs MVP in-repo:
- MkDocs Material setup
- bilingual site structure (`en` + `de`)
- polished landing page (hero, value props, quick links)
- GitHub Pages deployment via GitHub Actions
- minimal docs IA for onboarding and trust

## UX target

Landing page should feel comparable to lightweight product-doc homepages:
- clear headline + subheadline
- quick start CTA
- core value blocks (query/review/test/describe + trust)
- visible path into full docs navigation

## Proposed structure

Repository files (example):
- `mkdocs.yml`
- `docs/en/index.md`
- `docs/de/index.md`
- `docs/en/getting-started.md`
- `docs/de/getting-started.md`
- `docs/en/trust-and-safety.md`
- `docs/de/trust-and-safety.md`
- optional `overrides/` for homepage styling tweaks

Language routing:
- EN default at `/`
- DE at `/de/`

## Required content for MVP

Must include both DE and EN:
- Getting Started
- Core Commands
- Trust & Safety (resource and change boundaries)
- LLM Setup (local/self-hosted + OpenAI-compatible)
- FAQ / Troubleshooting (short)

## Deployment model

- build with MkDocs via GitHub Actions
- publish to GitHub Pages
- PR checks include docs build and link validation

## Quality gates

- build succeeds on PR
- no broken internal links
- locale parity check for required core pages
- homepage renders with clear CTA and navigation to docs sections

## Migration guardrails (toward Docusaurus if needed)

To keep future migration low-risk:
- keep Markdown content framework-agnostic
- keep locale files mirrored (`en`/`de` parity)
- avoid heavy theme-specific shortcodes where possible
- maintain a simple docs metadata map for page parity

## Non-goals

- no full docs versioning in MVP
- no advanced search backend customization in MVP
- no custom plugin ecosystem unless required for DE/EN parity

## Rollout plan

1. scaffold MkDocs Material with DE/EN structure
2. implement landing page and key navigation
3. migrate essential user docs (quickstart/trust/llm/commands)
4. configure GitHub Actions + Pages deploy
5. add docs CI checks and locale parity checks

## Definition of Done

- docs site is live on GitHub Pages
- strong landing page exists and links into full docs
- DE/EN core pages are available and navigable
- contributor workflow for docs updates is documented
- migration path to Docusaurus remains open and low-friction
