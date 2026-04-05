# Observability Foundation Parallel Core Bootstrap

## Description

Implement Foundation 11 as a new parallel core observability foundation with typed structured events, stable run correlation, redaction safeguards, and deterministic run summaries derived from events.

## Spec

- Add `ObsEvent`, `ObsContext`, `ObsRunSummary`.
- Add core APIs:
  - `obs_start_run(context) -> run_id`
  - `obs_log_event(event)`
  - `obs_end_run(run_id, summary) -> ObsRunSummary`
- Keep event payload structured and reject free-text primary payloads.
- Enforce required event metadata and correlation fields.
- Enforce redaction status contract (`not_needed|applied|blocked|failed`) and secret masking guarantees.
- Keep level/sampling (`minimal|standard|debug`) without dropping mandatory correlation and diagnosis fields.
- Derive run summary strictly from emitted events.
- Keep telemetry locally available for a defined retention window.

## Definition of Done

- Foundation module exists at `core/observability_foundation.py`.
- Event contract and redaction rules are validated by model checks.
- Run-level telemetry correlation works across run/stage/action/decision/policy/budget events.
- Deterministic event shaping and summary derivation are covered by unit tests.

## Implemented Behavior (Current)

- Added parallel observability core with:
  - typed event/context/summary models
  - versioned event contract fields
  - event type catalog for run/stage/action/decision/policy/budget
  - structured event builder API with correlation enforcement
  - in-memory local store with retention pruning
  - run summary derivation from recorded event history
- Added redaction validation for sensitive fields and redaction version requirements.
- Added sampling detail reduction (`minimal|standard|debug`) that preserves required diagnostics/correlation fields.

## How To Validate Quickly

1. Run `python3 -m unittest tests/test_observability_foundation.py`.
2. Confirm mandatory event fields and correlation checks are enforced.
3. Confirm redaction violations are rejected.
4. Confirm run summaries (duration, action counts, reasons, budgets) are derived from events.

## Known Limits / Notes

- This implementation is intentionally parallel and not yet wired into existing mode runtime pipelines.
- Storage backend is intentionally local in-memory for foundation bootstrap; external sinks/export remain deferred.
