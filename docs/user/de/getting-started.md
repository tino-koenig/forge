# Schnellstart

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
forge init --non-interactive --template balanced
forge query "Wo ist load_framework_graph_references definiert?"
```

## Erste Checks

- `forge doctor`
- `forge --output-format json query "Wo ist X definiert?"`
