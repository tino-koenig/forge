# Runtime-Settings & Sessions

Diese Seite erklaert Scopes, Prioritaeten und Session-Lifecycle-Befehle.

## Runtime-Scopes

Forge-Runtime-Settings koennen aus folgenden Quellen kommen:

- `session`-Scope (aktive benannte Session)
- `repo`-Scope (`.forge/runtime.toml`)
- `user`-Scope (user runtime config)
- config-Dateien (`.forge/config.toml`, `.forge/config.local.toml`)
- Defaults

## Effektive Prioritaet (hoch -> niedrig)

1. explizite CLI-Flags
2. session scope
3. repo scope
4. user scope
5. config TOML values
6. defaults

Mit `forge get --source` kannst du die Herkunft jedes Werts sehen.

## `forge set`

```bash
forge set [--scope session|repo|user] <key> <value>
```

Beispiele:

```bash
forge set --scope session output.view full
forge set --scope repo llm.mode off
forge set --scope user access.web off
```

Hinweise:
- Default-Scope ist `session`
- Aliase werden unterstuetzt (z. B. `output`, `llm`, `execution`, `access web|write`)

## `forge get`

```bash
forge get [--scope session|repo|user] [--resolved] [--source] [key]
```

Beispiele:

```bash
forge get
forge get llm.mode --source
forge get --scope repo output
forge get --resolved --source
```

Verhalten:
- ohne `--scope`: aufgeloeste/effektive Sicht
- `--scope`: rohe Werte aus genau einem Scope
- `--resolved`: erzwingt die effektive Merge-Sicht
- `--source`: fuegt pro Key die Herkunft hinzu

## `forge session`

```bash
forge session [--ttl-minutes N] [--revive] <command>
```

Kommandos:
- `new <name>`
- `use <name>`
- `list`
- `show [name]`
- `clear-context [name]`
- `end [name]`

Beispiele:

```bash
forge session new work --ttl-minutes 180
forge session use work
forge session list
forge session clear-context work
forge session end work
```

## Typische Workflows

### 1) Repo-Basis + Session-Override

```bash
forge set --scope repo llm.mode auto
forge set --scope repo output.format text
forge session new triage --ttl-minutes 120
forge set --scope session output.view full
forge get --resolved --source
```

### 2) Strikte lokale Policy

```bash
forge set --scope user access.web off
forge set --scope user access.write off
forge get access --resolved --source
```

## Fehlerbehebung

- Wenn ein Wert unerwartet wirkt:
  - `forge get <key> --resolved --source`
- Wenn Session-Werte veraltet/abgelaufen sind:
  - `forge session use <name> --revive`
