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
