# Getting Started

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Initialize repository

```bash
forge init --non-interactive --template balanced
```

## First queries

```bash
forge doctor
forge query "Where is enrich_detailed_context defined?"
forge explain:dependencies core/graph_cache.py
```

## Recommended output modes

- Human readable: default text output
- Auditable machine output: `--output-format json`
