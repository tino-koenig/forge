# Forge — AI Repo Workbench

**Explicit AI for real repository work.**

Repository slug: `forge-ai-repo-workbench`

Forge helps you inspect, explain, review, and improve repositories with **auditable outputs**, **explicit boundaries**, and **human-readable evidence**.

It is built for people who want AI help on real codebases without giving up control.

---

## Why Forge

Most AI coding tools feel magical right up to the point where you need to trust, verify, or reproduce what happened.

Forge takes a different approach:

- **explicit instead of opaque** — capabilities, boundaries, and outputs are visible
- **read-only by default** — repository analysis comes before code mutation
- **evidence-first** — answers point to files, paths, symbols, graph edges, or config surfaces
- **auditable by design** — runs, protocol events, fallbacks, and warnings are inspectable
- **local-first LLM friendly** — works well with self-hosted OpenAI-compatible setups

Forge is not just for “find symbol X”. It is for the kind of questions developers actually ask when entering or debugging a real project.

---

## What Forge Helps You Do

### Understand an unfamiliar codebase

Ask for architecture, behavior, config, dependencies, or entry points:

```bash
forge query "Where is the OpenAI-compatible provider configured?"
forge query "Which files decide whether web access is allowed?"
forge query "Where does Forge store protocol logs and run history?"
forge describe
```

### Explain behavior, not just locations

Use `explain` when you want structured answers about settings, dependencies, resources, outputs, or LLM participation:

```bash
forge explain:settings modes/ask.py
forge explain:dependencies modes/query.py
forge explain:outputs modes/review.py
forge explain:llm core/llm_foundation.py
```

### Review code with reproducible findings

Run deterministic review heuristics with visible evidence and bounded scope:

```bash
forge review modes/query.py
forge review core/config.py
```

### Inspect trust, provenance, and execution traces

Audit what happened, how Forge decided, and where LLMs or web access were involved:

```bash
forge runs list
forge logs tail
forge logs stats
forge logs show --run-id 42
```

### Draft tests from real context

```bash
forge test modes/settings.py --case "session-scoped override precedence"
```

---

## 60-Second Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
forge init --non-interactive --template balanced
forge doctor
forge query "Where is the runtime settings precedence resolved?"
```

That gives you:

- a local Forge setup in the repository
- an initialized `.forge/` workspace
- baseline diagnostics
- a first useful repository question instead of a low-value symbol lookup

### Workstation install (global `forge`)

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install forge-repo-tool
forge --help
```

`forge-repo-tool` is the published Python package name that provides the `forge` CLI.

---

## Good Example Questions

These are closer to real repository work than “where is symbol X defined?”

### Query examples

```bash
forge query "Where is the framework profile selected and loaded?"
forge query "Which config keys control LLM behavior?"
forge query "How does Forge decide whether a capability is read-only?"
forge query "Where are session TTL and runtime scope files handled?"
forge query "Which files control graph validation and graph warnings?"
```

### Explain examples

```bash
forge explain:settings core/runtime_settings_resolver.py
forge explain:defaults modes/init.py
forge explain:dependencies modes/explain.py
forge explain:resources core/protocol_log.py
forge explain:llm core/llm_integration.py
```

### Review examples

```bash
forge review modes/ask.py
forge review core/session_store.py
forge review scripts/run_quality_gates.py
```

### Ask-mode examples

```bash
forge ask:repo "How does Forge balance deterministic retrieval with LLM assistance?"
forge ask:docs "What does the framework integration layer support?"
forge ask:latest "What changed most recently in the logging pipeline?"
```

---

## Core Capabilities

- `query` — locate implementation, configuration, entry points, and relevant evidence
- `explain` — inspect one target through facets such as dependencies, settings, defaults, outputs, resources, and LLM usage
- `review` — run deterministic review heuristics with evidence
- `describe` — orient yourself in a repository or module quickly
- `test` — draft test plans and cases from real code context
- `ask`, `ask:repo`, `ask:docs`, `ask:latest` — ask broader questions with explicit source boundaries
- `runs`, `logs` — inspect execution history, protocol traces, and analytics
- `doctor` — validate setup, config, and runtime readiness
- `init` — bootstrap Forge in a repo with team-oriented templates and onboarding

---

## Team Templates and Repository Onboarding

Forge is designed to start from a real repository, not a blank AI chat.

`forge init` supports **team templates** and guided onboarding so teams can standardize how Forge behaves inside a repo:

- choose a baseline template for the repository
- generate repo-owned `.forge/*` configuration artifacts
- define source scope and framework-policy defaults during onboarding
- keep configuration inside the repository instead of hiding it in per-user magic

This makes Forge useful for individual repos, but also practical for teams that want consistent AI behavior across projects.

---

## Framework Integration, Better Said

Forge does more than simple file search.

It can use **framework-aware source profiles** and optional framework references to retrieve better evidence from framework-specific code and docs. In practice, that means Forge can work with:

- local framework profile definitions
- optional framework docs/reference paths
- framework-aware retrieval and graph references
- source-aware provenance in output contracts

So instead of saying “framework integration” as a vague feature, the stronger wording is:

**Forge can become framework-aware through explicit profiles, local reference sources, and graph-backed retrieval.**

That keeps the capability powerful without making it sound magical.

---

## Local LLMs First

Forge is designed for your own LLM deployment first, while staying OpenAI-compatible.

It works well with:

- self-hosted OpenAI-compatible endpoints
- local or on-prem model serving
- provider APIs that expose an OpenAI-compatible interface
- deterministic fallback when LLM support is disabled or unavailable

Tested and developed with a strong focus on:

- `Devstral-Small-2-24B-Instruct-2512`
- `Mistral-Small-3.2-24B-Instruct-2506`
- `Qwen3-30B-A3B`
- `Codestral-22B-v0.1`

Example:

```toml
[llm]
provider = "openai_compatible"
base_url = "http://localhost:8080/v1"
model = "local/devstral-small-24b"
```

Deterministic fallback example:

```bash
forge --llm-mode off query "Where is the cache built?"
```

Forge still remains useful when the LLM is unavailable. That is a design goal, not an accident.

---

## Auditability and Logging

Auditability is one of Forge’s core product properties.

Forge does not just return a result — it gives you a way to inspect how that result was produced.

That includes:

- structured output contracts
- run history with inspectable records
- protocol event logs for execution traces
- explicit warnings and fallback states
- log filtering, analytics, and run-focused inspection
- redaction/privacy guards for sensitive log content

Useful commands:

```bash
forge runs list
forge runs show 42
forge logs tail
forge logs stats
forge logs show --run-id 42
```

This means Forge is not only explainable at the answer level, but also **traceable at the execution level**.

---

## Trust & Safety Model

Forge treats trust as a product feature: **explicit capabilities, explicit read scopes, explicit side effects**.

| Capability | Reads | Writes | Notes |
|---|---|---|---|
| `query`, `explain`, `review`, `describe`, `test` | repo files, `.forge/index.json`, `.forge/graph.json`, optional framework refs/docs | none | read-only analysis modes |
| `ask`, `ask:repo`, `ask:docs`, `ask:latest` | question + optional web/doc retrieval (policy-controlled) | none | web access only when enabled by policy/settings |
| `doctor`, `config validate`, `get`, `runs`, `logs` | local config, run/log artifacts | none | diagnostics and inspection only |
| `index` | repository files + existing index/graph artifacts | `.forge/index.json`, `.forge/graph.json` | repository metadata build, no source edits |
| `session`, `set` | runtime/session config context | `.forge/sessions/*`, runtime scope files | settings and session state only |
| `init` | target path state, templates | `.forge/*` bootstrap artifacts | repository setup only |
| future `fix`, `implement` | planned explicit target scope | planned explicit bounded writes | not current default behavior |

### Mode boundary

- Current analysis workflows are read-only for repository source code.
- Current write-capable operations are limited to Forge-owned artifacts, config, and session state.
- Future code-writing modes are planned with explicit target narrowing and policy controls.

---

## Control Surfaces

You control Forge through:

- CLI flags
- repo config: `.forge/config.toml`
- local overrides: `.forge/config.local.toml`
- runtime/session settings: `forge set/get`, `forge session ...`

Deterministic precedence is applied and can be traced through diagnostics and output metadata.

---

## Contract-Oriented Output

Example:

```bash
forge --output-format json query "Which files decide whether web access is allowed?"
```

Example shape:

```json
{
  "summary": "Most likely relevant files include modes/ask.py and runtime settings/config resolution paths.",
  "evidence": [
    {
      "path": "modes/ask.py",
      "line": 1,
      "text": "..."
    }
  ],
  "sections": {
    "llm_usage": {
      "used": true,
      "fallback_reason": null
    },
    "action_orchestration": {
      "done_reason": "sufficient_evidence"
    }
  },
  "uncertainty": [
    "Results are based on indexed retrieval and bounded heuristic ranking."
  ]
}
```

The point is not the exact JSON shape. The point is that the output is **inspectable**, **structured**, and **not pretending to be magic**.

---

## Command Overview

```bash
forge query "Where is the OpenAI-compatible provider configured?"
forge explain:dependencies modes/query.py
forge explain:settings core/runtime_settings_resolver.py
forge review core/config.py
forge describe
forge test modes/settings.py --case "session-scoped override precedence"
forge doctor
forge logs stats
forge runs list
```

Run full quality gates:

```bash
PYTHONPATH=. python3 scripts/run_quality_gates.py
```

Run focused quality gates:

```bash
PYTHONPATH=. python3 scripts/run_quality_gates.py --only gate_runtime_settings_set_get
```

---

## Current Project State

Forge already includes implemented support for:

- team-template-based initialization
- framework-aware profiles and local framework reference sources
- reusable LLM foundations
- runtime settings with deterministic precedence and source tracing
- named sessions with TTL
- structured run history
- protocol event logging, analytics, and redaction
- central bounded orchestration foundations
- rich `query`, `explain`, `review`, `describe`, and `ask` behavior

The current repository state reflects a broad implemented feature base, including logging, protocol analytics, framework-aware retrieval, team-template onboarding, and explicit control/audit surfaces. fileciteturn1file0 fileciteturn1file2

---

## Roadmap and Contribution

- Product direction and principles: [AGENTS.md](AGENTS.md)
- Project roadmap: [docs/roadmap.md](docs/roadmap.md)
- User docs (DE/EN): [docs/user/README.md](docs/user/README.md)
- Feature status index: [docs/status/features-index.md](docs/status/features-index.md)
- Issue status index: [docs/status/issues-index.md](docs/status/issues-index.md)
- Feature specs: [docs/features](docs/features)
- Issues and spec corrections: [docs/issues](docs/issues)

If you contribute changes, run quality gates and keep feature/issue docs plus status in sync.

---

## Short Positioning

Forge is for developers and teams who want AI help with real repositories — but still want to know:

- what was read
- what was inferred
- what was logged
- what the model did
- where the answer came from

**With control, not magic.**
