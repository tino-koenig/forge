# Core Commands

This page explains the main Forge commands, their typical parameters, and when to use them.

## Global Parameters (apply to all commands)

- `--repo-root <path>`: start path for repo detection (`.forge/` marker lookup).
- `--env-file <path>`: explicit `.env` file.
- `--output-format text|json`: human text or machine-readable contract output.
- `--view compact|standard|full`: text detail level.
- `--details`: shorthand for `--view full`.
- `--llm-mode auto|off|force`: LLM usage policy.
- `--llm-provider <id>`, `--llm-model <id>`, `--llm-base-url <url>`, `--llm-timeout-s <n>`
- `--llm-output-language <lang|auto>`
- `--query-input-mode planner|exact`: query interpretation mode.

Many capability commands also accept an optional profile prefix in positional input:
- `simple`
- `standard`
- `detailed`

Example:

```bash
forge --output-format json query detailed "Where is enrich_detailed_context defined?"
```

## Query

`forge query [--framework-profile <id>] <question>`

Use `query` to locate files, symbols, and evidence snippets for concrete repo questions.

Important parameters:
- `--framework-profile <id>`: load optional framework profile from `.forge/frameworks.toml`.
- global: `--query-input-mode planner|exact`, `--llm-*`, output/view parameters.

Example:

```bash
forge query --query-input-mode exact "def load_framework_graph_references"
```

## Ask (+ Presets)

- `forge ask <question>`
- `forge ask:repo <question>`
- `forge ask:docs <question>`
- `forge ask:latest <question>`

Use `ask` for broader Q/A. `ask:*` presets control source strategy.

Important parameters:
- `--framework-profile` / `--profile` (alias)
- `--guided` (reserved staged mode)
- global: `--llm-*`, output/view parameters

Example:

```bash
forge ask:docs "Which config key controls query source scope?"
```

## Explain (+ Facet Aliases)

- `forge explain <target>`
- aliases: `forge explain:dependencies <target>`, `explain:settings`, `explain:outputs`, ...

Use `explain` for deeper, target-focused analysis.

Important parameters:
- `--focus overview|symbols|dependencies|resources|uses|settings|defaults|llm|outputs`
- `--direction out|in` (dependency-like facets)
- `--source-scope repo_only|framework_only|all`
- `--from-run <id>` + `--confirm-transition`

Example:

```bash
forge explain --focus dependencies --direction out core/graph_cache.py
```

## Review

`forge review <target>`

Use `review` for deterministic findings based on repository evidence.

Important parameters:
- `--from-run <id>`
- `--confirm-transition`

## Describe

`forge describe [target]`

Use `describe` for repo/module orientation and summaries.

Important parameters:
- `--from-run <id>`
- `--confirm-transition`

## Test

`forge test <target>`

Use `test` to draft test plans and cases from existing code context.

Important parameters:
- `--from-run <id>`
- `--confirm-transition`

## Doctor and Config

- `forge doctor [--check-llm-endpoint]`
- `forge config validate` (alias path)

Use for setup/config diagnostics.

## Runs

`forge runs ...`

Common usage:
- `forge runs list`
- `forge runs last`
- `forge runs <id> show [compact|standard|full]`
- `forge runs <id> rerun`
- `forge runs prune [--keep-last N] [--older-than-days D] [--dry-run]`

## Logs

`forge logs ...`

Common usage:
- `forge logs tail [count]`
- `forge logs run <run_id>`
- `forge logs show <event_id>`
- `forge logs stats`

Filter parameters:
- `--run-id`, `--capability`, `--step-type`, `--status`
- `--since`, `--until`, `--provider`, `--model`

## Init and Index

- `forge init [--template ...] [--non-interactive] [--force] [--dry-run] ...`
- `forge index`

Use `init` to bootstrap `.forge` config/artifacts and `index` to build repo metadata.

## Session / Set / Get

- `forge session new|use|list|show|clear-context|end ...`
- `forge set [--scope session|repo|user] <key> <value>`
- `forge get [--scope ...] [--resolved] [--source] [key]`

These commands control runtime settings and session behavior. See: `runtime-settings-and-sessions.md`.
