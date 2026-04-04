# Named Session Context with Auto-Create and TTL

## Description

This feature introduces named Forge sessions with automatic session creation, explicit session switching, and bounded context retention.

Primary goals:
- persist session-scoped runtime settings across CLI invocations
- allow explicit multi-session workflows (`new`, `use`, `list`, `show`)
- retain lightweight session context with explicit inactivity expiry

## Problem

`session` scope is currently process-local by nature and does not survive one-shot CLI execution.
Users need a practical way to keep a working context across multiple commands without writing everything to repo/user scope.

## Scope

Add a session management command group and named-session persistence:
- auto-create an active session when none exists
- `forge session new <name>` creates and activates a session
- `forge session use <name>` switches active session
- session-scoped settings and context survive between commands
- inactivity TTL handling (default: 60 minutes)

## Command model

### Session commands

- `forge session` -> show active session summary
- `forge session new <name> [--ttl-minutes <n>]` -> create + activate
- `forge session use <name>` -> switch active session
- `forge session list` -> list available sessions with last activity and expiry
- `forge session show [<name>]` -> detailed metadata/context/settings
- `forge session clear-context [<name>]` -> clear retained context only
- `forge session end [<name>]` -> close session and remove active binding if needed

### Auto-create behavior

On any command that consumes runtime settings:
- if no active valid session exists, Forge creates one automatically
- generated name example: `auto-20260404-153012`
- auto-created session becomes active

## Stored session data

Per named session:
- `name`
- `created_at`
- `last_activity_at`
- `expires_at` (derived from `last_activity_at + ttl`)
- `ttl_minutes` (default 60)
- `runtime_settings` (canonical key/value map for session scope)
- `context` (bounded structured context, see below)
- `meta` (version, source markers)

### Context retention model

Retained context is explicit, bounded, and inspectable.
Suggested initial fields:
- recent capabilities (bounded list)
- recent user question summaries (short)
- active framework profile hint
- selected output/llm/execution/access preferences

Hard limits:
- bounded size (count + chars)
- no large raw file dumps
- no hidden prompt transcripts

## TTL and validity

Default inactivity TTL:
- 60 minutes between commands

Rules:
- every successful command touching a session updates `last_activity_at`
- if now > `expires_at`, session is considered expired
- expired session is not auto-reactivated unless explicitly requested
- `forge session use <expired>` returns a clear expiry prompt/error with revive option

Optional behavior:
- `forge session use <name> --revive` resets activity window

## Storage model

Recommended repo-local storage:
- `.forge/sessions/index.json` (active pointer + registry)
- `.forge/sessions/<name>.json` (session payload)

Alternative user-level storage can be added later; repo-local is preferred for transparency.

## Resolver integration

Session source becomes explicit in runtime precedence:
1. explicit CLI flags
2. active named session settings
3. repo scope runtime settings
4. user scope runtime settings
5. `.forge/config*.toml`
6. defaults

`forge get --source` must expose `session:<name>` as source where applicable.

## Safety boundaries

Hard guarantees:
- session context cannot bypass capability contracts
- `query` remains read-only regardless of session settings
- session context remains inspectable and clearable

## Non-goals

- no chat-agent autonomy layer
- no opaque conversation transcript engine
- no unbounded memory retention

## Rollout plan

1. session persistence schema + active pointer
2. `forge session new/use/list/show` command set
3. auto-create logic on command bootstrap
4. TTL expiry/validation and revive flow
5. context retention with strict bounds
6. integration into runtime settings resolver source tracing

## Definition of Done

- Forge auto-creates an active named session when needed
- `forge session new` creates and activates; `forge session use` switches reliably
- session settings/context persist across command invocations
- inactivity TTL (default 60 min) is enforced deterministically
- source tracing shows session contribution in resolved settings
- session data is inspectable and can be cleared/ended explicitly

## Implemented Behavior (Current)

- Added repo-local named session storage:
  - `.forge/sessions/index.json` (active pointer + session registry)
  - `.forge/sessions/<name>.json` (session payload)
- Added session lifecycle command group:
  - `forge session` (active status; auto-create if missing/invalid)
  - `forge session new <name> [--ttl-minutes <n>]`
  - `forge session use <name> [--revive]`
  - `forge session list`
  - `forge session show [<name>]`
  - `forge session clear-context [<name>]`
  - `forge session end [<name>]`
- Runtime-consuming commands now auto-ensure an active valid session; expired/missing active sessions trigger deterministic auto-create (`auto-YYYYMMDD-HHMMSS`).
- TTL model:
  - default inactivity TTL is 60 minutes
  - `session use <name>` fails on expired sessions unless `--revive` is provided
- Context retention is bounded and inspectable:
  - recent capabilities
  - recent question summaries (bounded length/count)
  - active framework profile hint
  - preference snapshot keys
- Runtime resolver integration:
  - active session `runtime_settings` are loaded as session-scope values
  - source tracing exposes named source (`session:<name>`) for those keys

## How To Use

```bash
forge session
forge session new work --ttl-minutes 120
forge session use work
forge session list
forge session show work
forge session clear-context work
forge session end work
```

Expired session behavior:

```bash
forge session use work
# -> error if expired
forge session --revive use work
```

## Known Limits / Notes

- Session-scoped runtime setting mutation via `forge set/get` UX is delivered in feature 061; in this feature, session runtime values are persisted/consumed but not yet managed by dedicated set/get commands.
- Session storage is repo-local by design for transparency and inspectability.
- Session context remains bounded and intentionally avoids prompt transcript persistence.
