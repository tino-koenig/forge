# Describe Symbol-Anchor Evidence Contract

## Description

Ensure describe symbol outputs are anchored to the requested symbol evidence, not only file-level leading lines.

## Addresses Issues

- [Issue 36 - Describe Symbol Evidence Is Not Anchored to the Requested Symbol](/Users/tino/PhpstormProjects/forge/docs/issues/36-describe-symbol-evidence-is-not-anchored-to-the-requested-symbol.md)

## Spec

- For symbol targets, include at least one evidence line containing the matched symbol definition/signature.
- Surface uncertainty when only weak symbol mentions exist.
- Keep deterministic evidence extraction order and limits.

## Definition of Done

- Symbol-target evidence includes symbol definition/signature anchor by default.
- Weak matches are explicitly labeled as low confidence.
- Regression tests validate evidence anchoring and uncertainty behavior.
