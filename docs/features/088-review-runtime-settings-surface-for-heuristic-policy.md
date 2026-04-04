# Review Runtime Settings Surface for Heuristic Policy

## Description

Expose key review heuristic thresholds and caps as runtime settings.

## Addresses Issues

- [Issue 31 - Review Heuristics and Thresholds Are Hardcoded, Not Configurable](/Users/tino/PhpstormProjects/forge/docs/issues/31-review-heuristics-and-thresholds-are-hardcoded-not-configurable.md)

## Spec

- Add canonical settings (examples):
  - `review.large_file.medium_threshold`
  - `review.large_file.high_threshold`
  - `review.findings.max_items`
  - `review.related.max_targets`
  - `review.evidence.max_per_finding`
- Resolve via runtime settings precedence with source tracing.

## Definition of Done

- Hardcoded review policy constants are replaced by resolved settings defaults.
- Effective values can be inspected via `forge get --source`.
- Regression tests validate overridden settings behavior.

## Implemented Behavior (Current)

- Added canonical runtime settings for review policy:
  - `review.large_file.medium_threshold`
  - `review.large_file.high_threshold`
  - `review.findings.max_items`
  - `review.related.max_targets`
  - `review.evidence.max_per_finding`
- Review now resolves these settings via runtime precedence and exposes effective values/sources in `sections.review_policy`.
- Applied settings to runtime behavior:
  - large-file severity thresholds
  - findings output cap
  - related-target cap (profile cap remains upper bound)
  - per-finding evidence cap
- Added regression gate `gate_review_runtime_policy_settings`.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_review_runtime_policy_settings` passes.

## Known Limits / Notes

- Existing detector-internal per-pattern limits stay conservative; runtime evidence policy is applied as a final per-finding cap in output.
