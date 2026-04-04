# Related-File Selection for Review Is Too Lexical and Can Add Noise

## Problem

Related-file expansion for review relies on simple stem substring matching and can include weakly related files.

## Evidence

- `find_related_files` in `core/analysis_primitives.py` uses `stem in rel.stem` lexical matching.
- Review uses this expansion in standard/detailed profiles.
- This can pull in files by naming coincidence rather than architectural relation.

## Required behavior

- Related-file selection should use stronger deterministic signals (imports, directory locality, index metadata) before lexical fallback.
- Noise from weak lexical collisions should be reduced.

## Done criteria

- Related-file ranking uses a weighted signal model beyond stem containment.
- Review outputs show clearer relation rationale for included files.
- Regression tests cover noisy-name collision cases.

## Linked Features

- [Feature 089 - Related-Target Retrieval Foundation for Review and Explain](/Users/tino/PhpstormProjects/forge/docs/features/089-related-target-retrieval-foundation-for-review-and-explain.md)
