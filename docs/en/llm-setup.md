# LLM Setup

Forge supports OpenAI-compatible endpoints, including local/self-hosted deployments.

## Example

```toml
[llm]
provider = "openai_compatible"
base_url = "http://localhost:8080/v1"
model = "local/devstral-small-24b"
```

## Deterministic fallback mode

```bash
forge --llm-mode off query "Where is the cache built?"
```
