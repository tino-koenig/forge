# LLM Setup

Forge supports OpenAI-compatible endpoints, including self-hosted/local setups.

## Example config

```toml
[llm]
provider = "openai_compatible"
base_url = "http://localhost:8080/v1"
model = "local/devstral-small-24b"
```

## Deterministic fallback

```bash
forge --llm-mode off query "Where is the cache built?"
```
