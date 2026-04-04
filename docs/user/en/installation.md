# Installation

## Development install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Workstation install with pipx

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install forge-repo-tool
```

`forge-repo-tool` is the package name, `forge` is the CLI command.
