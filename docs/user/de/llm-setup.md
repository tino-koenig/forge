# LLM-Setup

Forge unterstuetzt OpenAI-kompatible Endpunkte, auch self-hosted/lokal.

## Beispielkonfiguration

```toml
[llm]
provider = "openai_compatible"
base_url = "http://localhost:8080/v1"
model = "local/devstral-small-24b"
```

## Deterministischer Fallback

```bash
forge --llm-mode off query "Wo wird der Cache gebaut?"
```
