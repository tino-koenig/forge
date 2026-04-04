# Runtime-Settings & Sessions

## Scopes

Runtime-Werte koennen kommen aus:
- CLI-Flags
- session scope
- repo scope (`.forge/runtime.toml`)
- user scope
- config TOML values
- defaults

## Effektive Prioritaet

1. CLI
2. session
3. repo
4. user
5. config TOML
6. defaults

Quellen anzeigen mit:

```bash
forge get --resolved --source
```

## Werte setzen

```bash
forge set --scope session output.view full
forge set --scope repo llm.mode auto
forge set --scope user access.web off
```

## Werte lesen

```bash
forge get
forge get llm.mode --source
forge get --scope repo output
forge get --resolved --source
```

## Session-Lifecycle

```bash
forge session new work --ttl-minutes 180
forge session use work
forge session list
forge session clear-context work
forge session end work
```
