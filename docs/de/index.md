# Forge - AI Repo Workbench

Explizite KI fuer echte Repository-Arbeit.

Forge hilft Teams, Repository-Fragen mit klaren Grenzen, auditierbarer Ausgabe und deterministischem Fallback zu beantworten.

## Start in 60 Sekunden

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
forge init --non-interactive --template balanced
forge query "Wo ist load_framework_graph_references definiert?"
```

## Warum Forge

- Explizite Modus-Grenzen statt undurchsichtiger Agent-Loops.
- Read/Write-Scope ist sichtbar und pruefbar.
- Output-Contracts enthalten Evidenz, Warnungen und Fallback-Status.

## Kernfaehigkeiten

- Repository-Orte und Evidenz finden (`query`)
- Ein Ziel tief analysieren (`explain`)
- Deterministische Findings erzeugen (`review`)
- Systeme schnell beschreiben (`describe`)
- Testplaene aus Code-Kontext entwerfen (`test`)

## Trust & Safety zuerst

Siehe [Trust & Safety](trust-and-safety.md) fuer capability-basierte Read/Write-Grenzen.

## Weiter

- [Schnellstart](getting-started.md)
- [Kernbefehle](core-commands.md)
- [Runtime-Settings & Sessions](runtime-settings-and-sessions.md)
- [LLM-Setup](llm-setup.md)
- [Fehlerbehebung](troubleshooting.md)
