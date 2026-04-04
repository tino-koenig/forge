# Status Index

Forge provides generated indexes for quick status lookup:

- Features: `docs/status/features-index.md`
- Issues: `docs/status/issues-index.md`

Build or refresh:

```bash
python3 scripts/status_index.py build
```

Quick lookup:

```bash
python3 scripts/status_index.py feature 019
python3 scripts/status_index.py issue 12
```

Manual status data lives in:

- `docs/status/status-overrides.toml`

Rules:

- `defined_on` is auto-derived from git add date of the spec file unless overridden.
- `status` is manual (`defined`, `in_progress`, `implemented` for features; `open`, `in_progress`, `implemented` for issues).
- `implemented_on` is manual and should be set when complete.

Issue/Feature traceability rule:

- Every open issue should reference implementing feature(s) in a `## Linked Features` section.
- Every feature that addresses known issues should reference them in a `## Addresses Issues` section.
- Mark an issue as `implemented` only after linked feature implementation is complete and the issue done criteria are validated.
