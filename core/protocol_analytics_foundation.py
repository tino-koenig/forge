"""Shared protocol-event analytics and filtering helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def parse_iso(value: object) -> datetime:
    if not isinstance(value, str):
        return datetime.min.replace(tzinfo=timezone.utc)
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_iso_filter(value: object, *, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"invalid {field} filter: expected ISO-8601 timestamp")
    parsed = parse_iso(value)
    if parsed == datetime.min.replace(tzinfo=timezone.utc):
        raise ValueError(f"invalid {field} filter: expected ISO-8601 timestamp")
    return parsed


def sort_events(events: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(events, key=lambda item: parse_iso(item.get("timestamp")))


def safe_int(value: object) -> int | None:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def terminal_duration(event: dict[str, object]) -> int:
    duration = event.get("duration_ms")
    if isinstance(duration, int) and duration >= 0:
        return duration
    return 0


def provider_of(event: dict[str, object]) -> str | None:
    metadata = event.get("metadata")
    if not isinstance(metadata, dict):
        return None
    provider = metadata.get("provider")
    if isinstance(provider, str) and provider.strip():
        return provider.strip()
    return None


def model_of(event: dict[str, object]) -> str | None:
    metadata = event.get("metadata")
    if not isinstance(metadata, dict):
        return None
    model = metadata.get("model")
    if isinstance(model, str) and model.strip():
        return model.strip()
    return None


def apply_filters(events: list[dict[str, object]], args) -> list[dict[str, object]]:
    filtered = list(events)
    since_raw = getattr(args, "since", None)
    until_raw = getattr(args, "until", None)
    since = parse_iso_filter(since_raw, field="--since") if since_raw is not None else None
    until = parse_iso_filter(until_raw, field="--until") if until_raw is not None else None
    if since is not None and until is not None and since > until:
        raise ValueError("invalid time filters: --since must be <= --until")

    run_id_filter = getattr(args, "logs_run_id", None)
    if run_id_filter is not None:
        filtered = [item for item in filtered if safe_int(item.get("run_id")) == int(run_id_filter)]
    capability_filter = getattr(args, "logs_capability", None)
    if isinstance(capability_filter, str) and capability_filter.strip():
        cap = capability_filter.strip().lower()
        filtered = [item for item in filtered if str(item.get("capability", "")).lower() == cap]
    step_type_filter = getattr(args, "logs_step_type", None)
    if isinstance(step_type_filter, str) and step_type_filter.strip():
        step_type = step_type_filter.strip().lower()
        filtered = [item for item in filtered if str(item.get("step_type", "")).lower() == step_type]
    status_filter = getattr(args, "logs_status", None)
    if isinstance(status_filter, str) and status_filter.strip():
        status = status_filter.strip().lower()
        filtered = [item for item in filtered if str(item.get("status", "")).lower() == status]
    provider_filter = getattr(args, "logs_provider", None)
    if isinstance(provider_filter, str) and provider_filter.strip():
        provider_norm = provider_filter.strip().lower()
        filtered = [item for item in filtered if (provider_of(item) or "").lower() == provider_norm]
    model_filter = getattr(args, "logs_model", None)
    if isinstance(model_filter, str) and model_filter.strip():
        model_norm = model_filter.strip().lower()
        filtered = [item for item in filtered if (model_of(item) or "").lower() == model_norm]
    if since is not None:
        filtered = [item for item in filtered if parse_iso(item.get("timestamp")) >= since]
    if until is not None:
        filtered = [item for item in filtered if parse_iso(item.get("timestamp")) <= until]
    return filtered


def count_by(events: list[dict[str, object]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event in events:
        value = str(event.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[0]))


def percentile(sorted_values: list[int], p: float) -> int:
    if not sorted_values:
        return 0
    if len(sorted_values) == 1:
        return sorted_values[0]
    idx = int(round((len(sorted_values) - 1) * p))
    if idx < 0:
        idx = 0
    if idx >= len(sorted_values):
        idx = len(sorted_values) - 1
    return sorted_values[idx]


def stats_payload(events: list[dict[str, object]]) -> dict[str, object]:
    terminal = [event for event in events if str(event.get("status")) in {"completed", "failed", "fallback"}]
    durations = sorted(terminal_duration(item) for item in terminal)
    slowest = sorted(terminal, key=terminal_duration, reverse=True)[:5]
    llm_terminal = [event for event in terminal if str(event.get("step_type")) == "llm"]
    fallback_rate = (
        sum(1 for event in terminal if str(event.get("status")) == "fallback") / len(terminal)
        if terminal
        else 0.0
    )
    provider_model_snapshot: dict[str, int] = {}
    for event in llm_terminal:
        provider = provider_of(event) or "unknown_provider"
        model = model_of(event) or "unknown_model"
        key = f"{provider}:{model}"
        provider_model_snapshot[key] = provider_model_snapshot.get(key, 0) + 1
    return {
        "event_count": len(events),
        "counts_by_step_type": count_by(events, "step_type"),
        "counts_by_status": count_by(events, "status"),
        "duration_ms": {
            "p50": percentile(durations, 0.50),
            "p95": percentile(durations, 0.95),
        },
        "slowest_steps": [
            {
                "event_id": item.get("event_id"),
                "run_id": item.get("run_id"),
                "step_name": item.get("step_name"),
                "step_type": item.get("step_type"),
                "status": item.get("status"),
                "duration_ms": terminal_duration(item),
            }
            for item in slowest
        ],
        "fallback_rate": round(fallback_rate, 6),
        "provider_model_usage": dict(sorted(provider_model_snapshot.items(), key=lambda item: item[0])),
    }


def build_run_totals(events: list[dict[str, object]]) -> dict[str, int]:
    terminal = [event for event in events if str(event.get("status")) in {"completed", "failed", "fallback"}]
    return {
        "total_events": len(events),
        "total_duration_ms": sum(terminal_duration(event) for event in terminal),
        "llm_step_count": sum(1 for event in terminal if str(event.get("step_type")) == "llm"),
        "fallback_count": sum(1 for event in terminal if str(event.get("status")) == "fallback"),
        "failed_count": sum(1 for event in terminal if str(event.get("status")) == "failed"),
    }
