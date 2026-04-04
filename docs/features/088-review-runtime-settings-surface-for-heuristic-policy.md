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
