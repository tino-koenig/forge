# Trust & Safety

Forge favors explicit capability boundaries over hidden automation.

## Read scope

- repository files
- `.forge` artifacts (`index.json`, `graph.json`, runs/logs)
- optional framework refs/docs
- optional web retrieval in ask presets (when enabled)

## Write scope

- current writes are limited to Forge-owned artifacts/settings/session state
- current analysis modes do not modify source code
- future code-writing modes must define explicit target boundaries

## Auditability

- machine-readable output contracts (`--output-format json`)
- explicit uncertainty/fallback sections
- run history and logs are inspectable
