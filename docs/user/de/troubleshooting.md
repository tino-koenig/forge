# Fehlerbehebung

## `No initialized Forge repository found`

Ausfuehren:

```bash
forge init --non-interactive --template balanced
```

## LLM-Endpunktfehler

- `llm.base_url` pruefen
- `forge doctor --check-llm-endpoint` ausfuehren

## Unerwartetes Query-Ranking

- JSON-Ausgabe pruefen: `sections.likely_locations`, `sections.evidence`, `sections.uncertainty`
