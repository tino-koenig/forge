# Installation

## Entwicklungsinstallation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Workstation-Installation mit pipx

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install forge-repo-tool
```

`forge-repo-tool` ist der Paketname, `forge` ist der CLI-Befehl.
