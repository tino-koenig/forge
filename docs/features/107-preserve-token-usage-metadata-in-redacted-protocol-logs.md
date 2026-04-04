# Preserve Token Usage Metadata in Redacted Protocol Logs

## Description

Keep non-secret token accounting fields visible in protocol logs while preserving strict secret redaction.

## Addresses Issues

- [Issue 8 - Protocol Redaction Overmasks `token_usage` Metadata](/Users/tino/PhpstormProjects/forge/docs/issues/8-protocol-redaction-overmasks-token-usage-metadata.md)

## Spec

- Redaction policy must distinguish credential tokens from usage counters.
- Keep sanitized `token_usage` fields (`prompt_tokens`, `completion_tokens`, `total_tokens`, `source`) in persisted protocol events.
- Continue masking secrets/auth tokens/API keys deterministically.

## Definition of Done

- Persisted `.forge/logs/events.jsonl` retains non-secret token usage counters when available.
- Privacy gate still passes for secret injection and bearer/api-key masking.
- Logs analytics can consume token/cost metadata consistently.
