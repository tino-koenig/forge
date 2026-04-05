# Runtime Settings Foundation Parallel Core Bootstrap

## Description

Implement Foundation 04 as a new parallel core runtime-settings foundation with typed resolution, source-priority handling, validation, and structured diagnostics.

## Spec

- Add typed runtime setting contract for `int|float|bool|enum|str`.
- Resolve with strict source priority `cli > local > repo > default`.
- Keep unknown keys runtime-tolerant but diagnostically visible.
- Fall back to lower-priority source or default on invalid input.
- Emit stable diagnostic codes.
- Use central registry as the only source for defaults, bounds, and allowed values.

## Definition of Done

- `SettingSpec`, `ResolvedSetting`, and `SettingDiagnostic` are implemented.
- Central registry exists and drives resolver behavior.
- `resolve_setting` and `resolve_settings` work deterministically.
- Unit tests cover priority, fallback, unknown keys, bound/enum validation, diagnostics, and determinism.

## Implemented Behavior (Current)

- Added new parallel foundation modules:
  - `core/runtime_settings_foundation.py`
  - `core/runtime_settings_foundation_registry.py`
- Resolver supports `int|float|bool|enum|str` with deterministic source precedence and stable diagnostics.
- Invalid values produce diagnostics and fall back to lower-priority sources, then default (when allowed).
- Unknown keys are ignored for effective runtime value but diagnosed with `unknown_key`.

## How To Validate Quickly

1. Run `python3 -m unittest tests/test_runtime_settings_foundation.py`.
2. Verify assertions for source precedence and invalid-input fallback diagnostics.
3. Verify enum/bound handling and deterministic repeated resolution outputs.

## Known Limits / Notes

- This change is intentionally parallel and does not wire existing modes to the new resolver.
- Extended types and context-coupled effectiveness from Foundation 04 V2 are intentionally deferred.
