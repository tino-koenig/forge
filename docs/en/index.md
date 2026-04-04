# Forge - AI Repo Workbench

Explicit AI for real repository work.

Forge helps teams answer repository questions with explicit boundaries, auditable output, and deterministic fallback behavior.

## Start in 60 seconds

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
forge init --non-interactive --template balanced
forge query "Where is load_framework_graph_references defined?"
```

## Why Forge

- Explicit mode boundaries instead of opaque agent loops.
- Read/write scope is visible and reviewable.
- Output contracts include evidence, warnings, and fallback state.

## Core capabilities

- Query repository locations and evidence (`query`)
- Explain one target deeply (`explain`)
- Review with deterministic findings (`review`)
- Describe systems quickly (`describe`)
- Draft test plans from code context (`test`)

## Trust & Safety first

See [Trust & Safety](trust-and-safety.md) for capability-level read/write boundaries.

## Continue

- [Getting Started](getting-started.md)
- [Core Commands](core-commands.md)
- [Runtime Settings & Sessions](runtime-settings-and-sessions.md)
- [LLM Setup](llm-setup.md)
- [Troubleshooting](troubleshooting.md)
