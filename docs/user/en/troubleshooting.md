# Troubleshooting

## `No initialized Forge repository found`

Run:

```bash
forge init --non-interactive --template balanced
```

## LLM endpoint errors

- check `llm.base_url`
- run `forge doctor --check-llm-endpoint`

## Unexpected query ranking

- inspect JSON output: `sections.likely_locations`, `sections.evidence`, `sections.uncertainty`
