# Rezepte

## Funktionsdefinition finden

```bash
forge query "Wo ist log_llm_event definiert?"
```

## Abhaengigkeiten einer Datei erklaeren

```bash
forge explain:dependencies core/graph_cache.py
```

## Einzelnes Quality Gate ausfuehren

```bash
PYTHONPATH=. python3 scripts/run_quality_gates.py --only gate_runtime_settings_set_get
```
