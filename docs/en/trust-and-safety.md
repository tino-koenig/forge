# Trust & Safety

Forge keeps capability boundaries explicit.

## Capability policy matrix

| Capability group | Reads | Writes |
|---|---|---|
| `query`, `explain`, `review`, `describe`, `test` | repo files, `.forge/index.json`, `.forge/graph.json`, optional framework refs/docs | none |
| `ask*` | question + optional docs/web retrieval (policy controlled) | none |
| `doctor`, `config validate`, `runs`, `logs`, `get` | config and run/log artifacts | none |
| `index` | repository files + cached artifacts | `.forge/index.json`, `.forge/graph.json` |
| `session`, `set` | runtime/session sources | session/runtime setting files |
| `init` | target path/templates | `.forge/*` bootstrap files |

## Auditability

- Contracts: `--output-format json`
- Run history: `forge runs ...`
- Protocol events/stats: `forge logs ...`
- Explicit warnings and fallback reasons in sections
