# Describe Symbol Evidence Is Not Anchored to the Requested Symbol

## Problem

For symbol targets, describe evidence is taken from the beginning of the resolved file and may not include the requested symbol definition.

## Evidence

- `collect_describe_evidence` iterates from line 1 over `target.content` and truncates at 8 lines.
- Code path: `/Users/tino/PhpstormProjects/forge/modes/describe.py` (`collect_describe_evidence`).
- Repro:
  - `python3 forge.py --llm-provider mock --output-format json --view full describe log_llm_event`
  - Result: evidence lines show module imports/headers; requested symbol line is absent.

## Required behavior

- For symbol targets, evidence must include at least one anchor line for the matched definition/signature.
- Summary wording should be constrained by symbol-anchored evidence.

## Done criteria

- Symbol-target evidence includes symbol definition/signature line by default.
- Missing symbol anchor forces lower confidence / explicit uncertainty note.
- Regression tests validate symbol-evidence anchoring.

## Linked Features

- [Feature 093 - Describe Symbol-Anchor Evidence Contract](/Users/tino/PhpstormProjects/forge/docs/features/093-describe-symbol-anchor-evidence-contract.md)

## Implemented Behavior (Current)

- Describe now includes deterministic symbol-anchor evidence for symbol targets by prioritizing matching definition/signature lines.
- Symbol-target outputs now keep evidence grounded in requested-symbol anchors instead of only leading file header lines.
- Missing symbol anchor now adds explicit uncertainty note to reduce overconfidence.
- Regression coverage added via `gate_describe_symbol_anchor_evidence`.

## How To Validate Quickly

- Run:
  - `python3 scripts/run_quality_gates.py`
- Verify:
  - `gate_describe_symbol_anchor_evidence` passes.

## Known Limits / Notes

- Symbol anchor detection is pattern-based and relies on readable source content in the resolved file.
