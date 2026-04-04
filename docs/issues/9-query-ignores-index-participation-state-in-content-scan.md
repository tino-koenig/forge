# Query Ignores Index Participation State in Content Scan

## Problem

`forge query` scans repository file content via `iter_repo_files(...)` and then ranks matches even when a path is marked `index_exclude` in the index.

Observed behavior:
- `modes/index.py` classifies `vendor/` as `index_exclude`.
- `modes/query.py` content retrieval still scans all repo files returned by `core/repo_io.py::iter_repo_files`.
- Paths not present in index default to `path_class="normal"` in ranking.
- In practice, `vendor/*` content can appear in top results for code-location questions although it is excluded from index participation.

This breaks the intended separation between index participation and default relevance behavior and causes noisy ranking.

## Required behavior

- When index data is available, default query content scanning should honor index participation:
  - `hard_ignore` and `index_exclude` should not be treated as normal default candidates.
- Inclusion of `index_exclude` paths should be explicit (for example via future flag or explicit source scope).
- Ranking should not silently up-classify non-indexed paths to `normal` when index metadata is present.

## Done criteria

- Query retrieval defaults align with index participation semantics when `.forge/index.json` exists.
- `vendor/` noise does not appear in default top results in a regression fixture where `vendor` contains high lexical overlap.
- A quality gate covers this behavior.
