# Fehlerbehebung

## No initialized Forge repository found

```bash
forge init --non-interactive --template balanced
```

## LLM-Endpunktprobleme

```bash
forge doctor --check-llm-endpoint
```

Zusatzlich `llm.base_url` und `llm.model` pruefen.

## Unerwartetes Ranking

JSON-Ausgabe nutzen und Evidenz-/Unsicherheits-Sektionen pruefen:

```bash
forge --output-format json query "Wo ist X definiert?"
```
