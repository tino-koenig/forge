"""Run history persistence for Forge capability executions."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from core.step_protocol import normalize_protocol_events


def history_path(repo_root: Path) -> Path:
    return repo_root / ".forge" / "runs.jsonl"


def _read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []


def load_runs(repo_root: Path) -> list[dict[str, Any]]:
    path = history_path(repo_root)
    records: list[dict[str, Any]] = []
    for raw in _read_lines(path):
        raw = raw.strip()
        if not raw:
            continue
        try:
            item = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            records.append(item)
    return records


def get_run(repo_root: Path, run_id: int) -> dict[str, Any] | None:
    for record in load_runs(repo_root):
        if int(record.get("id", -1)) == run_id:
            return record
    return None


def last_run(repo_root: Path) -> dict[str, Any] | None:
    records = load_runs(repo_root)
    if not records:
        return None
    return records[-1]


def append_run(
    repo_root: Path,
    *,
    request: dict[str, Any],
    execution: dict[str, Any],
    output: dict[str, Any],
) -> int:
    path = history_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    records = load_runs(repo_root)
    next_id = (int(records[-1].get("id", 0)) + 1) if records else 1
    execution_payload = dict(execution)
    execution_payload["protocol_events"] = normalize_protocol_events(
        run_id=next_id,
        capability=str(request.get("capability") or "unknown"),
        events=execution_payload.get("protocol_events") if isinstance(execution_payload.get("protocol_events"), list) else [],
    )
    record = {
        "id": next_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request": request,
        "execution": execution_payload,
        "output": output,
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True))
        fh.write("\n")
    return next_id
