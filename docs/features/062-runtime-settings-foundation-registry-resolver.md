# Runtime Settings Foundation: Registry, Resolver, Source Tracing

## Description

This feature defines the technical foundation required by Feature 061 (`forge set/get`).

Primary goals:
- centralize runtime setting definitions in one registry
- resolve effective values deterministically across scopes and sources
- expose machine-readable source tracing for every resolved key

## Dependency

Depends on / enables:
- Feature 061 (`Runtime Settings via forge set/get`)

## Scope

Implement shared core primitives (no full UX command surface yet):
- canonical runtime key registry
- alias normalization and value parsing helpers
- multi-scope resolver with stable precedence
- structured source-trace output

## Registry model

Introduce a registry module (for example `core/runtime_settings_registry.py`) with:
- `key`: canonical dotted id (for example `output.format`)
- `type`: `enum|bool|string|int|float`
- `allowed_values` / validator
- `default`
- `scope_support`: `session|repo|user` flags
- `description`
- optional alias list and alias transformer

Required initial registry keys:
- `output.format` (`text|json`)
- `output.view` (`compact|standard|full`)
- `llm.mode` (`off|auto|force`)
- `llm.model` (`string`)
- `execution.profile` (`fast|balanced|intensive`)
- `access.web` (`on|off`)
- `access.write` (`on|off`)

## Resolver model

Introduce a resolver module (for example `core/runtime_settings_resolver.py`) with:
- scope loading (`session`, `.forge/runtime.toml`, user config path)
- normalization to canonical keys
- merge by deterministic precedence
- integration hooks for existing config/CLI flow

Required precedence (highest -> lowest):
1. explicit CLI flags
2. session scope
3. repo scope
4. user scope
5. existing `.forge/config*.toml`
6. defaults from registry

## Source tracing contract

Resolver output must include:
- `values`: resolved canonical key/value map
- `sources`: per-key source (`cli|session|repo|user|toml|default`)
- `normalization`: alias-to-canonical mapping trace
- `warnings`: unknown keys, invalid values, dropped entries

This output is consumed by future `forge get --source` and can be reused by diagnostics.

## Validation rules

- unknown keys are rejected at write-time and reported at read-time
- invalid values are rejected with accepted-value hints
- unsupported scope for a key is rejected
- alias expansion is deterministic and visible in normalization trace

## Storage model

Repo scope file:
- `.forge/runtime.toml`

User scope file:
- recommended path under user Forge home (to be finalized in implementation)

Session scope:
- ephemeral in-process cache (no hidden background daemon)

## Integration points

- CLI bootstrap should call resolver once and pass resolved runtime settings into request/build context.
- Existing config resolution (for example LLM config) should accept optional runtime overrides from resolver output.
- Capability execution contract should optionally include runtime-setting provenance in full/debug views.

## Non-goals

- no full `forge set/get` UX in this feature (handled by Feature 061)
- no capability-specific behavior changes beyond override wiring
- no weakening of mode/capability safety contracts

## Rollout plan

1. registry schema and canonical key definitions
2. resolver with precedence and source tracing
3. loader/writer stubs for session/repo/user scopes
4. wiring into existing config resolution path
5. tests for precedence, alias normalization, invalid input handling

## Definition of Done

- canonical key registry exists and is used by resolver
- resolver returns deterministic values + per-key source tracing
- scope handling works for `session`, `repo`, and `user`
- precedence order is covered by tests
- foundation is ready for Feature 061 command UX implementation
