# Framework Graph Refs Accept Invalid Payloads

## Problem

Framework graph references are accepted as long as JSON parses to a dict. Required graph schema fields are not validated.

Observed behavior:
- `load_framework_graph_references` accepts payload like `{"foo": 1}` as loaded.
- Query output reports `framework_graph_refs_loaded` including invalid refs.
- No warning indicates schema invalidity, so graph provenance is overstated.

## Required behavior

- Validate framework graph payloads with the same minimal contract used for repo graph loading.
- Reject invalid payloads and emit explicit warnings per ref.
- Ensure `framework_graph_refs_loaded` includes only valid/usable refs.

## Done criteria

- Invalid framework graph JSON objects are excluded from loaded refs.
- Warnings indicate `invalid schema/version` with ref id and path.
- Regression gate covers malformed-but-dict payload acceptance bug.
