# Kernbefehle

Diese Seite dokumentiert die wichtigsten Befehle und zentrale Parameter.

## Allgemeine Parameter

- `--repo-root <path>`
- `--env-file <path>`
- `--output-format text|json`
- `--view compact|standard|full`
- `--details`
- `--llm-mode auto|off|force`
- `--llm-provider`, `--llm-model`, `--llm-base-url`, `--llm-timeout-s`
- `--llm-output-language <lang|auto>`
- `--query-input-mode planner|exact`

## Query und Ask

- `forge query [--framework-profile <id>] <frage>`
- `forge ask <frage>`
- `forge ask:repo <frage>`
- `forge ask:docs <frage>`
- `forge ask:latest <frage>`

## Explain und Analysemodi

- `forge explain [--focus ...] [--direction out|in] [--source-scope ...] <target>`
- `forge review <target>`
- `forge describe [target]`
- `forge test <target>`

`review`, `describe`, `test`, `explain` unterstuetzen auch `--from-run <id>` und `--confirm-transition`.

## Betrieb und Diagnostik

- `forge init ...`
- `forge index`
- `forge doctor [--check-llm-endpoint]`
- `forge config validate`
- `forge runs ...`
- `forge logs ...`

## Runtime/Session-Steuerung

- `forge session new|use|list|show|clear-context|end ...`
- `forge set [--scope session|repo|user] <key> <value>`
- `forge get [--scope ...] [--resolved] [--source] [key]`

Fuer Scope-/Precedence-Details siehe [Runtime-Settings & Sessions](runtime-settings-and-sessions.md).
