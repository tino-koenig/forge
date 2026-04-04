# Runtime Settings & Sessions

This page explains runtime scopes, setting precedence, and session lifecycle commands.

## Runtime Scopes

Forge runtime settings can come from:

- `session` scope (active named session)
- `repo` scope (`.forge/runtime.toml`)
- `user` scope (user runtime config)
- config files (`.forge/config.toml`, `.forge/config.local.toml`)
- defaults

## Effective Precedence (high -> low)

1. explicit CLI flags
2. session scope
3. repo scope
4. user scope
5. config TOML values
6. defaults

Use `forge get --source` to inspect where a value came from.

## `forge set`

```bash
forge set [--scope session|repo|user] <key> <value>
```

Examples:

```bash
forge set --scope session output.view full
forge set --scope repo llm.mode off
forge set --scope user access.web off
```

Notes:
- default scope is `session`
- aliases are supported (for example `output`, `llm`, `execution`, `access web|write`)

## `forge get`

```bash
forge get [--scope session|repo|user] [--resolved] [--source] [key]
```

Examples:

```bash
forge get
forge get llm.mode --source
forge get --scope repo output
forge get --resolved --source
```

Behavior:
- without `--scope`, returns resolved/effective view
- `--scope` reads raw values from one scope
- `--resolved` forces effective merge view
- `--source` includes per-key provenance

## `forge session`

```bash
forge session [--ttl-minutes N] [--revive] <command>
```

Commands:
- `new <name>`
- `use <name>`
- `list`
- `show [name]`
- `clear-context [name]`
- `end [name]`

Examples:

```bash
forge session new work --ttl-minutes 180
forge session use work
forge session list
forge session clear-context work
forge session end work
```

## Typical Workflows

### 1) Per-repo baseline + session override

```bash
forge set --scope repo llm.mode auto
forge set --scope repo output.format text
forge session new triage --ttl-minutes 120
forge set --scope session output.view full
forge get --resolved --source
```

### 2) Strict local policy

```bash
forge set --scope user access.web off
forge set --scope user access.write off
forge get access --resolved --source
```

## Troubleshooting

- If a value does not behave as expected, run:
  - `forge get <key> --resolved --source`
- If session values are stale/expired, switch with:
  - `forge session use <name> --revive`
