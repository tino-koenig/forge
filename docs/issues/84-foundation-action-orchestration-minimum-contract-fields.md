# Foundation Action Orchestration Minimum Contract Fields

## Problem

Foundation action orchestration currently does not enforce a stable minimum contract for `action_orchestration` outputs in `available` and `fallback` states.

As a result, payloads can be considered structurally acceptable even when essential core fields are missing. This leaves downstream consumers with under-specified orchestration data and weakens the output contract at exactly the point where orchestration state should already be explicit.

## Why this matters

- Downstream consumers can receive ambiguous or incomplete orchestration outputs.
- Contract validation becomes too permissive for states that should already expose core orchestration meaning.
- Missing essential fields shift failure detection from contract validation to later runtime handling.
- Auditability and review quality decline when the minimum orchestration intent is not guaranteed.

## Evidence

- `action_orchestration` currently lacks a sufficiently enforced minimum required field set for at least `available` and `fallback` outputs.
- Validation is not currently strict enough to guarantee that those states always expose their minimum core structure.
- This creates a contract gap distinct from the separate builder/validator mismatch tracked elsewhere.

## Required behavior

- `action_orchestration` must define a canonical minimum required field set for `available` and `fallback` states.
- Validation must fail deterministically when any required core field for those states is missing.
- Missing-field diagnostics must identify the exact absent field or fields.
- The minimum contract must be enforced consistently across all relevant validation paths.

## Done criteria

- The minimum required core fields for `available` and `fallback` are explicitly documented in the canonical contract.
- Validation rejects payloads missing any required minimum field for those states.
- Regression coverage includes at least:
  - valid `available` payload at minimum contract shape
  - valid `fallback` payload at minimum contract shape
  - invalid `available` payload missing a required core field
  - invalid `fallback` payload missing a required core field
- Diagnostics name the missing field set precisely.

## Scope

This issue is limited to minimum contract enforcement for `action_orchestration` outputs in `available` and `fallback` states.

It does not cover broader contract redesign, new orchestration states, or the separate builder/validator inconsistency issue.

## Implemented Behavior (Current)

- The validator now enforces a canonical minimum field set for `action_orchestration` when section status is `available` or `fallback`.
- Required minimum fields are:
  - `status`
  - `done_reason`
- Missing required fields emit deterministic diagnostics with code `action_orchestration_minimum_fields_missing`, including the exact missing field names.
- Existing normative-value checks for `decision`, `control_signal`, and `done_reason` remain unchanged.

## Suggested implementation direction

- Define the canonical minimum required field set per relevant orchestration state.
- Enforce those requirements in the canonical validation layer rather than through path-specific assumptions.
- Reuse the same contract definition everywhere minimum-shape validation is needed.
- Keep optional and extended orchestration metadata out of the minimum contract unless strictly required.

## How To Validate Quickly

1. Construct minimal valid `action_orchestration` payloads for both `available` and `fallback`.
2. Confirm both validate successfully.
3. Remove each required field one at a time.
4. Confirm validation fails deterministically and names the missing field.

## Known Limits / Notes

- This issue establishes baseline minimum contract correctness only.
- It should not expand the contract beyond what is necessary for core orchestration meaning.
- Builder/validator contract alignment is tracked separately and should remain separate from this minimum-field enforcement work.
