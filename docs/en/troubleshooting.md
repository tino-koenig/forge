# Troubleshooting

## No initialized Forge repository found

```bash
forge init --non-interactive --template balanced
```

## LLM endpoint issues

```bash
forge doctor --check-llm-endpoint
```

Also verify `llm.base_url` and `llm.model`.

## Unexpected ranking

Use JSON output and inspect evidence/uncertainty sections:

```bash
forge --output-format json query "Where is X defined?"
```
