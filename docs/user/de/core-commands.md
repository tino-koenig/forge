# Kernbefehle

Diese Seite erklaert die zentralen Forge-Befehle, typische Parameter und Einsatzfaelle.

## Allgemeine Parameter (gelten fuer alle Befehle)

- `--repo-root <path>`: Startpfad fuer Repo-Erkennung (`.forge/`-Marker).
- `--env-file <path>`: explizite `.env`-Datei.
- `--output-format text|json`: Textausgabe oder maschinenlesbarer Contract.
- `--view compact|standard|full`: Detailgrad der Textausgabe.
- `--details`: Kurzform fuer `--view full`.
- `--llm-mode auto|off|force`: LLM-Nutzungspolitik.
- `--llm-provider <id>`, `--llm-model <id>`, `--llm-base-url <url>`, `--llm-timeout-s <n>`
- `--llm-output-language <lang|auto>`
- `--query-input-mode planner|exact`: Query-Interpretationsmodus.

Viele Capability-Befehle akzeptieren zusaetzlich ein Profil-Praefix im Payload:
- `simple`
- `standard`
- `detailed`

Beispiel:

```bash
forge --output-format json query detailed "Wo ist enrich_detailed_context definiert?"
```

## Query

`forge query [--framework-profile <id>] <frage>`

`query` findet Dateien, Symbole und Evidenzstellen fuer konkrete Repo-Fragen.

Wichtige Parameter:
- `--framework-profile <id>`: optionales Framework-Profil aus `.forge/frameworks.toml`.
- global: `--query-input-mode planner|exact`, `--llm-*`, output/view-Parameter.

Beispiel:

```bash
forge query --query-input-mode exact "def load_framework_graph_references"
```

## Ask (+ Presets)

- `forge ask <frage>`
- `forge ask:repo <frage>`
- `forge ask:docs <frage>`
- `forge ask:latest <frage>`

`ask` ist fuer breitere Q/A. `ask:*`-Presets steuern die Quellenstrategie.

Wichtige Parameter:
- `--framework-profile` / `--profile` (Alias)
- `--guided` (staged/reserviert)
- global: `--llm-*`, output/view-Parameter

Beispiel:

```bash
forge ask:docs "Welcher config key steuert query source scope?"
```

## Explain (+ Facet-Aliase)

- `forge explain <target>`
- Aliase: `forge explain:dependencies <target>`, `explain:settings`, `explain:outputs`, ...

`explain` liefert tiefe, zielgerichtete Analyse.

Wichtige Parameter:
- `--focus overview|symbols|dependencies|resources|uses|settings|defaults|llm|outputs`
- `--direction out|in` (fuer dependency-aehnliche Facets)
- `--source-scope repo_only|framework_only|all`
- `--from-run <id>` + `--confirm-transition`

Beispiel:

```bash
forge explain --focus dependencies --direction out core/graph_cache.py
```

## Review

`forge review <target>`

`review` liefert deterministische Findings auf Basis von Repo-Evidenz.

Wichtige Parameter:
- `--from-run <id>`
- `--confirm-transition`

## Describe

`forge describe [target]`

`describe` ist fuer Repo-/Modul-Ueberblick und Zusammenfassungen.

Wichtige Parameter:
- `--from-run <id>`
- `--confirm-transition`

## Test

`forge test <target>`

`test` entwirft Testplaene/-faelle aus realem Code-Kontext.

Wichtige Parameter:
- `--from-run <id>`
- `--confirm-transition`

## Doctor und Config

- `forge doctor [--check-llm-endpoint]`
- `forge config validate` (Alias-Pfad)

Fuer Setup-/Konfigurationsdiagnostik.

## Runs

`forge runs ...`

Typische Nutzung:
- `forge runs list`
- `forge runs last`
- `forge runs <id> show [compact|standard|full]`
- `forge runs <id> rerun`
- `forge runs prune [--keep-last N] [--older-than-days D] [--dry-run]`

## Logs

`forge logs ...`

Typische Nutzung:
- `forge logs tail [count]`
- `forge logs run <run_id>`
- `forge logs show <event_id>`
- `forge logs stats`

Filter-Parameter:
- `--run-id`, `--capability`, `--step-type`, `--status`
- `--since`, `--until`, `--provider`, `--model`

## Init und Index

- `forge init [--template ...] [--non-interactive] [--force] [--dry-run] ...`
- `forge index`

`init` bootstrapped `.forge`-Konfiguration/Artefakte, `index` baut Repo-Metadaten.

## Session / Set / Get

- `forge session new|use|list|show|clear-context|end ...`
- `forge set [--scope session|repo|user] <key> <value>`
- `forge get [--scope ...] [--resolved] [--source] [key]`

Diese Befehle steuern Runtime-Settings und Session-Verhalten. Siehe: `runtime-settings-and-sessions.md`.
