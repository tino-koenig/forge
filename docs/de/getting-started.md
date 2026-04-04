# Schnellstart

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Repository initialisieren

```bash
forge init --non-interactive --template balanced
```

## Erste Queries

```bash
forge doctor
forge query "Wo ist enrich_detailed_context definiert?"
forge explain:dependencies core/graph_cache.py
```

## Empfohlene Ausgabearten

- Menschlich lesbar: Standard-Textausgabe
- Auditierbar maschinenlesbar: `--output-format json`
