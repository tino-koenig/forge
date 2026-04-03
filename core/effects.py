"""Effect enforcement for capability execution."""

from __future__ import annotations

from dataclasses import dataclass, field

from core.capability_model import (
    CommandRequest,
    EffectClass,
)
from core.mode_capability_contract import effect_to_action, require_action_eligibility


@dataclass
class ExecutionSession:
    request: CommandRequest
    effective_effects: set[EffectClass] = field(default_factory=set)

    def record_effect(self, effect: EffectClass, detail: str = "") -> None:
        require_action_eligibility(
            capability=self.request.capability,
            action=effect_to_action(effect),
            phase="executor",
            detail=detail or None,
        )
        self.effective_effects.add(effect)
