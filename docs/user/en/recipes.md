# Recipes

## Find a function definition

```bash
forge query "Where is log_llm_event defined?"
```

## Explain dependencies of one file

```bash
forge explain:dependencies core/graph_cache.py
```

## Focus one quality gate

```bash
PYTHONPATH=. python3 scripts/run_quality_gates.py --only gate_runtime_settings_set_get
```
