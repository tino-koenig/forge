# Trust & Safety

Forge haelt Capability-Grenzen explizit.

## Capability-Policy-Matrix

| Capability-Gruppe | Reads | Writes |
|---|---|---|
| `query`, `explain`, `review`, `describe`, `test` | Repo-Dateien, `.forge/index.json`, `.forge/graph.json`, optionale Framework-Refs/-Docs | keine |
| `ask*` | Frage + optionale docs/web retrieval (policy-gesteuert) | keine |
| `doctor`, `config validate`, `runs`, `logs`, `get` | Konfiguration sowie Run-/Log-Artefakte | keine |
| `index` | Repo-Dateien + Cache-Artefakte | `.forge/index.json`, `.forge/graph.json` |
| `session`, `set` | Runtime-/Session-Quellen | Session-/Runtime-Setting-Dateien |
| `init` | Zielpfad/Templates | `.forge/*` Bootstrap-Dateien |

## Auditierbarkeit

- Contracts: `--output-format json`
- Run-Historie: `forge runs ...`
- Protocol-Events/Stats: `forge logs ...`
- Explizite Warnungen und Fallback-Gruende in Sections
