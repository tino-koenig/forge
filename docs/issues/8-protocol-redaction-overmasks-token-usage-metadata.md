# Protocol Redaction Overmasks `token_usage` Metadata

## Problem

Protocol-log redaction treats any key containing `token` as sensitive and replaces it with `[redacted]`.
This masks `metadata.token_usage` in persisted protocol events, reducing observability for features 029/030/033.

Observed behavior:
- Run history protocol events contain structured `token_usage`.
- Persisted `.forge/logs/events.jsonl` replaces `token_usage` with `[redacted]`.
- Cost/token observability becomes inconsistent between run history and protocol logs.

## Required behavior

- Redaction must keep non-secret token accounting fields (`prompt_tokens`, `completion_tokens`, `total_tokens`, `source`) visible.
- Secret-bearing fields must still be redacted deterministically.
- Redaction policy should distinguish credential tokens from usage counters.

## Done criteria

- Persisted protocol events keep sanitized token usage counters while still masking actual secrets/tokens.
- Privacy regression gate continues to pass with synthetic secret injection.
- Logs analytics can rely on token/cost metadata consistency where available.


## Linked Features

- [Feature 107 - Preserve Token Usage Metadata in Redacted Protocol Logs](/Users/tino/PhpstormProjects/forge/docs/features/107-preserve-token-usage-metadata-in-redacted-protocol-logs.md)
