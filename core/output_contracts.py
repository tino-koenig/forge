"""Canonical output contract helpers for Forge capabilities."""

from __future__ import annotations

import json
from typing import Any


def build_contract(
    *,
    capability: str,
    profile: str,
    summary: str,
    evidence: list[dict[str, Any]],
    uncertainty: list[str],
    next_step: str,
    sections: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "capability": capability,
        "profile": profile,
        "summary": summary,
        "evidence": evidence,
        "uncertainty": uncertainty,
        "next_step": next_step,
    }
    if sections:
        payload["sections"] = sections
    return payload


def emit_contract_json(contract: dict[str, Any]) -> None:
    print(json.dumps(contract, indent=2, sort_keys=True))
