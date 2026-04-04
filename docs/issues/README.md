# Issues

Optional issue specs can be stored here as markdown files:

- `1-short-title.md`
- `12-query-output-evidence.md`
- `101-provider-timeout-handling.md`

The status index reads these files and combines them with
`docs/status/status-overrides.toml`.

Recommended first line:

- `# <Issue title>`

## Feature linking (required)

- Link each issue to one or more implementing feature specs via a `## Linked Features` section.
- Use absolute doc links to `docs/features/<id>-...md`.
- An issue is considered solved only after the linked feature(s) are implemented and verified against the issue's done criteria.
