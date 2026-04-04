# Runtime Settings via `forge set/get`

## Description

This feature introduces explicit runtime-setting commands to configure Forge behavior without editing TOML manually.

Primary goals:
- provide a human-friendly runtime control surface (`set`, `get`)
- keep settings explicit, inspectable, and reversible
- preserve strict safety boundaries (for example: query stays read-only)

## Problem

Current behavior is controlled by a mix of CLI flags, environment variables, and TOML config.
That is powerful but not ergonomic for iterative daily usage.

Need:
- quick mode switches (`output`, `llm`, `execution`, `access`)
- discoverable current state (`forge get ...`)
- deterministic precedence and source visibility

## Concept

### Command model

Introduce two top-level commands:
- `forge set <key> <value> [--scope session|repo|user]`
- `forge get [key] [--scope ...] [--resolved] [--source]`

Default scope:
- `set`: `session`
- `get`: resolved effective values

### Naming model (recommended)

Use canonical dotted keys internally and in docs:
- `output.format`
- `output.view`
- `llm.mode`
- `llm.model`
- `execution.profile`
- `access.web`
- `access.write`

Provide ergonomic aliases for CLI input:
- `output` -> composite alias (maps to format/view presets)
- `llm` -> alias for `llm.mode`
- `execution` -> alias for `execution.profile`
- `access web` -> alias for `access.web`
- `access write` -> alias for `access.write`

### Preset and alias mapping

Examples (user-friendly):
- `forge set output human`
- `forge set output json`
- `forge set output exhaustive`

Canonical mapping:
- `output=human` -> `output.format=text`, `output.view=standard`
- `output=json` -> `output.format=json`
- `output=exhaustive` -> `output.format=text`, `output.view=full`

LLM examples:
- `forge set llm off` -> `llm.mode=off`
- `forge set llm on` -> `llm.mode=auto` (safe alias)
- `forge set llm force` -> `llm.mode=force`
- `forge set llm model local/mistral` -> `llm.model=local/mistral`

Execution examples:
- `forge set execution fast`
- `forge set execution balanced`
- `forge set execution intensive`

Suggested profile semantics:
- `fast`: lower budgets, minimal expansion
- `balanced`: current default behavior
- `intensive`: higher budgets, deeper passes

Access examples:
- `forge set access web on|off`
- `forge set access write on|off`

## Safety and policy boundaries

Hard guarantees:
- `query` capability remains read-only regardless of runtime setting values.
- `access.write=on` does not enable writes in capabilities that are contractually read-only.
- runtime settings cannot bypass mode transition policy or capability contracts.

Validation rules:
- reject unknown keys/values with actionable error
- show accepted values and closest key suggestions
- normalize aliases to canonical keys in storage/output

## Scope and persistence model

Three scopes:
- `session`: ephemeral for current shell/process context
- `repo`: persisted under `.forge/runtime.toml` (team-visible optional file)
- `user`: persisted in user-level Forge config location

Precedence (highest to lowest):
1. explicit CLI flags
2. `session` runtime settings
3. `repo` runtime settings
4. `user` runtime settings
5. existing `.forge/config*.toml`
6. built-in defaults

`forge get --source` should show where each effective value came from.

## `forge get` output shape

Examples:
- `forge get`
- `forge get output`
- `forge get llm.mode`
- `forge get --resolved --source`

Recommended output contract section:
- `settings.current` (resolved values)
- `settings.sources` (per-key source)
- `settings.aliases_applied` (normalization trace)

## Design recommendations

Preferred solution:
- introduce a dedicated runtime settings resolver layer used by CLI bootstrap and modes
- keep alias parsing in CLI adapter, keep canonical schema in core
- expose a deterministic key registry (single source of truth)

Strong alternative:
- implement only preset-level toggles first (`output`, `llm`, `execution`), add dotted keys later
- lower initial complexity, but weaker extensibility

Why preferred solution:
- avoids future key-fragmentation and special-case growth
- supports both novice-friendly aliases and advanced explicit controls
- aligns with Forge principle: explicit over implicit

## Non-goals

- no hidden background automation
- no capability-specific magic keys without schema registration
- no override path that weakens read-only guarantees

## Rollout plan

1. foundation: key registry + resolver + precedence model
2. `forge get` (read-only introspection)
3. `forge set` for `output.*`, `llm.*`
4. `execution.profile` integration into existing budgets
5. `access.*` integration with explicit policy enforcement traces

## Definition of Done

- `forge set/get` commands exist with canonical key model and aliases
- precedence and source tracking are deterministic and visible
- output/llm/execution/access families supported as specified
- safety boundaries are enforced (query remains read-only)
- docs include key registry, value matrix, and migration notes
