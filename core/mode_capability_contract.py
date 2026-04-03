"""Central mode capability contract and enforcement helpers."""

from __future__ import annotations

from dataclasses import dataclass

from core.capability_model import CAPABILITY_POLICIES, Capability, EffectClass, EffectViolationError


MODE_ACTION_MATRIX: dict[Capability, frozenset[str]] = {
    capability: frozenset(effect.value for effect in policy.allowed_effects)
    for capability, policy in CAPABILITY_POLICIES.items()
}


@dataclass(frozen=True)
class PolicyViolationEvent:
    phase: str
    capability: str
    blocked_action: str
    allowed_actions: list[str]
    detail: str | None = None

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "phase": self.phase,
            "capability": self.capability,
            "blocked_action": self.blocked_action,
            "allowed_actions": self.allowed_actions,
        }
        if self.detail:
            payload["detail"] = self.detail
        return payload


def evaluate_action_eligibility(
    *,
    capability: Capability,
    action: str,
    phase: str,
    detail: str | None = None,
) -> PolicyViolationEvent | None:
    allowed = MODE_ACTION_MATRIX.get(capability, frozenset())
    if action in allowed:
        return None
    return PolicyViolationEvent(
        phase=phase,
        capability=capability.value,
        blocked_action=action,
        allowed_actions=sorted(allowed),
        detail=detail,
    )


def require_action_eligibility(
    *,
    capability: Capability,
    action: str,
    phase: str,
    detail: str | None = None,
) -> None:
    violation = evaluate_action_eligibility(capability=capability, action=action, phase=phase, detail=detail)
    if violation is None:
        return
    message = (
        f"Policy violation at {phase}: capability '{violation.capability}' "
        f"cannot perform action '{violation.blocked_action}'. "
        f"Allowed actions: {', '.join(violation.allowed_actions)}."
    )
    if violation.detail:
        message = f"{message} Detail: {violation.detail}"
    raise EffectViolationError(message)


def effect_to_action(effect: EffectClass) -> str:
    return effect.value
