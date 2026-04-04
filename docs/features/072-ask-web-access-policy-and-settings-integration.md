# Ask Web Access Policy and Settings Integration

## Description

Integrate ask web behavior with explicit runtime/repo settings so access and budgets are policy-driven instead of hardcoded in mode execution.

Goals:
- enforce `access.web` consistently,
- allow deterministic tuning of web search/retrieval budgets,
- keep shared foundations reusable and configuration-driven.

## Spec

### Access gating

- `ask:docs` / `ask:latest` must check effective runtime access settings before invoking web foundations.
- with web access denied, foundations are skipped and contract reports policy block.

### Configurable policies

Support controlled settings for web stages (runtime/toml), for example:
- search: `max_queries`, `max_urls_considered`, `max_urls_returned`, `max_search_time_ms`
- retrieval: `max_urls_fetched`, `max_content_chars_per_url`, `max_total_context_chars`, `max_snippets`, `max_retrieval_time_ms`, `request_timeout_s`

### Foundation boundary

- policy resolution should be centralized and reused by all future web consumers.
- modes should pass resolved policy objects, not reimplement policy defaults.

## Definition of Done

- Ask web execution honors `access.web`.
- Web policy budgets are configurable via approved config channels.
- Output includes effective policy and policy source provenance.
- Regression tests cover policy allow/deny and overridden budget paths.

## Addresses Issues

- [14-ask-ignores-access-web-runtime-setting.md](/Users/tino/PhpstormProjects/forge/docs/issues/14-ask-ignores-access-web-runtime-setting.md)
- [17-web-search-policy-entrypoints-are-not-used-in-query-planning.md](/Users/tino/PhpstormProjects/forge/docs/issues/17-web-search-policy-entrypoints-are-not-used-in-query-planning.md)
