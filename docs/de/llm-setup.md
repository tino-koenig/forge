# LLM-Setup

Forge unterstuetzt OpenAI-kompatible Endpunkte, auch lokal/self-hosted.

## Beispiel

```toml
[llm]
provider = "openai_compatible"
base_url = "http://localhost:8080/v1"
model = "local/devstral-small-24b"
```

## Deterministischer Fallback-Modus

```bash
forge --llm-mode off query "Wo wird der Cache gebaut?"
```
