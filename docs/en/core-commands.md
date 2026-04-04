# Core Commands

This page documents the most used commands and key parameters.

## Global parameters

- `--repo-root <path>`
- `--env-file <path>`
- `--output-format text|json`
- `--view compact|standard|full`
- `--details`
- `--llm-mode auto|off|force`
- `--llm-provider`, `--llm-model`, `--llm-base-url`, `--llm-timeout-s`
- `--llm-output-language <lang|auto>`
- `--query-input-mode planner|exact`

## Query and Ask

- `forge query [--framework-profile <id>] <question>`
- `forge ask <question>`
- `forge ask:repo <question>`
- `forge ask:docs <question>`
- `forge ask:latest <question>`

## Explain and analysis modes

- `forge explain [--focus ...] [--direction out|in] [--source-scope ...] <target>`
- `forge review <target>`
- `forge describe [target]`
- `forge test <target>`

`review`, `describe`, `test`, `explain` also support `--from-run <id>` and `--confirm-transition`.

## Operations and diagnostics

- `forge init ...`
- `forge index`
- `forge doctor [--check-llm-endpoint]`
- `forge config validate`
- `forge runs ...`
- `forge logs ...`

## Runtime/session control

- `forge session new|use|list|show|clear-context|end ...`
- `forge set [--scope session|repo|user] <key> <value>`
- `forge get [--scope ...] [--resolved] [--source] [key]`

For full scope/precedence details, see [Runtime Settings & Sessions](runtime-settings-and-sessions.md).
