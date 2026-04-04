from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from core.analysis_primitives import (
    ResolvedTarget,
    find_related_files,
    load_index_entry_map,
    load_index_path_class_map,
    path_class_weight,
    prioritize_paths_by_index,
    resolve_file_or_symbol_target,
)
from core.capability_model import CommandRequest, Profile
from core.effects import ExecutionSession
from core.llm_integration import maybe_refine_summary, provenance_section, resolve_settings
from core.output_contracts import build_contract, emit_contract_json
from core.output_views import is_compact, is_full, resolve_view
from core.repo_io import read_text_file
from core.run_reference import RunReferenceError, resolve_from_run_payload


@dataclass
class Evidence:
    path: Path
    line: int
    text: str


@dataclass
class InferencePoint:
    inference_id: str
    inference: str
    evidence_ids: list[str]
    rationale: str
    confidence: str


@dataclass
class SettingsInfluence:
    setting_key: str
    input_channel: str
    effect_summary: str
    evidence: Evidence
    confidence: str


@dataclass
class DefaultValueSignal:
    name: str
    value_repr: str
    activation_condition: str
    evidence: Evidence
    confidence: str


@dataclass
class LLMParticipation:
    stage: str
    kind: str
    evidence: Evidence
    confidence: str


@dataclass
class OutputSurface:
    surface: str
    path_or_section: str
    producer: str
    evidence: Evidence
    confidence: str


BEHAVIOR_SIGNAL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("guard_return", re.compile(r"^\s*if\s+not\s+.+:\s*$")),
    ("filesystem_mkdir", re.compile(r"\.mkdir\(")),
    ("filesystem_write", re.compile(r"\.write_text\(")),
    ("file_append", re.compile(r"\.open\(\s*[\"']a[\"']")),
    ("serialization_json", re.compile(r"\bjson\.dumps\(")),
    ("secret_redaction", re.compile(r"\.pop\(\s*[\"'](api_key|authorization|prompt|user_prompt|system_prompt)[\"']")),
]


ROLE_MARKERS = {
    "entrypoint": ["if __name__ == \"__main__\":", "argparse.ArgumentParser(", "main("],
    "configuration": [".yml", ".yaml", ".toml", ".ini", "config", "settings"],
    "support code": ["helper", "util", "common", "shared", "support"],
}


def classify_role(rel_path: Path, content: str, index_entry: dict[str, object] | None) -> tuple[str, str]:
    lowered_path = str(rel_path).lower()
    lowered_content = content.lower()

    if any(marker in content for marker in ROLE_MARKERS["entrypoint"]):
        return "entrypoint", "contains explicit startup/CLI entry markers"

    if "config" in lowered_path or any(ext in lowered_path for ext in [".yml", ".yaml", ".toml", ".ini"]):
        return "configuration", "path/extension suggests configuration data"

    if index_entry:
        path_class = index_entry.get("path_class")
        if isinstance(path_class, str) and path_class_weight(path_class) >= 3:
            return "implementation", "indexed as structurally preferred path"
        symbols = index_entry.get("top_level_symbols")
        if isinstance(symbols, list) and symbols:
            if len(symbols) >= 3:
                return "implementation", "contains multiple top-level symbols"

    if any(marker in lowered_path or marker in lowered_content for marker in ROLE_MARKERS["support code"]):
        return "support code", "path/content suggests helper or utility responsibilities"

    return "implementation", "default classification from executable/source structure"


def gather_evidence_for_target(
    target: ResolvedTarget,
    request: CommandRequest,
) -> list[Evidence]:
    lines = target.content.splitlines()
    evidence: list[Evidence] = []
    rel_path = target.path

    if target.source == "symbol":
        symbol = request.payload.strip()
        symbol_patterns = [
            re.compile(rf"^\s*def\s+{re.escape(symbol)}\s*\("),
            re.compile(rf"^\s*class\s+{re.escape(symbol)}\s*[\(:]"),
        ]
        for idx, line in enumerate(lines, start=1):
            if any(pattern.search(line) for pattern in symbol_patterns):
                evidence.append(Evidence(path=rel_path, line=idx, text=line.strip()))
                for extra in range(1, 3):
                    if idx - 1 + extra < len(lines):
                        evidence.append(
                            Evidence(
                                path=rel_path,
                                line=idx + extra,
                                text=lines[idx - 1 + extra].strip(),
                            )
                        )
                break

    structural_patterns = [
        re.compile(r"^\s*class\s+\w+"),
        re.compile(r"^\s*def\s+\w+"),
        re.compile(r"^\s*import\s+"),
        re.compile(r"^\s*from\s+\w+\s+import\s+"),
        re.compile(r"if __name__ == [\"']__main__[\"']"),
    ]
    for idx, line in enumerate(lines, start=1):
        if any(pattern.search(line) for pattern in structural_patterns):
            evidence.append(Evidence(path=rel_path, line=idx, text=line.strip()))
        if len(evidence) >= 10:
            break

    if request.profile == Profile.SIMPLE:
        return evidence[:5]
    if request.profile == Profile.STANDARD:
        return evidence[:8]
    return evidence[:12]


def _extract_symbol_block(content: str, symbol: str) -> list[str]:
    if not symbol.strip():
        return []
    lines = content.splitlines()
    def_pattern = re.compile(rf"^(\s*)(def|class)\s+{re.escape(symbol)}\b")
    start_idx = -1
    indent = 0
    for idx, line in enumerate(lines):
        match = def_pattern.search(line)
        if not match:
            continue
        start_idx = idx
        indent = len(match.group(1))
        break
    if start_idx < 0:
        return []
    block: list[str] = []
    for idx in range(start_idx, len(lines)):
        line = lines[idx]
        if idx > start_idx and line.strip():
            current_indent = len(line) - len(line.lstrip(" "))
            if current_indent <= indent:
                break
        block.append(line)
    return block


def build_behavior_signals(target: ResolvedTarget, request: CommandRequest) -> list[str]:
    source_lines = target.content.splitlines()
    if target.source == "symbol":
        symbol_lines = _extract_symbol_block(target.content, request.payload.strip())
        if symbol_lines:
            source_lines = symbol_lines

    signals: list[str] = []
    seen: set[str] = set()
    for line in source_lines:
        stripped = line.strip()
        if not stripped:
            continue
        lowered = stripped.lower()
        for signal_id, pattern in BEHAVIOR_SIGNAL_PATTERNS:
            if not pattern.search(stripped):
                continue
            if signal_id == "guard_return" and stripped.endswith(":"):
                rendered = f"{stripped} return ..."
            elif signal_id == "filesystem_mkdir":
                rendered = "creates directories via mkdir(...)"
            elif signal_id == "filesystem_write":
                rendered = "writes file content via write_text(...)"
            elif signal_id == "file_append":
                rendered = "appends to a file via open('a', ...)"
            elif signal_id == "serialization_json":
                rendered = "serializes event payload via json.dumps(...)"
            elif signal_id == "secret_redaction":
                rendered = "redacts sensitive keys before writing"
            else:
                rendered = stripped
            key = rendered.lower()
            if key in seen:
                continue
            seen.add(key)
            signals.append(rendered)
            break
        if len(signals) >= 6:
            break

    if "repo_root / \".forge\" / \"logs\"" in target.content:
        anchor = "targets local log path under .forge/logs"
        if anchor not in signals:
            signals.append(anchor)
    if "llm_observability.jsonl" in target.content.lower():
        anchor = "writes observability events to llm_observability.jsonl"
        if anchor not in signals:
            signals.append(anchor)
    return signals[:8]


def _confidence_for_hits(hit_count: int) -> str:
    if hit_count >= 3:
        return "high"
    if hit_count >= 1:
        return "medium"
    return "low"


def extract_settings_influences(rel_target: Path, content: str) -> list[SettingsInfluence]:
    influences: list[SettingsInfluence] = []
    seen: set[tuple[str, str, int]] = set()
    lines = content.splitlines()

    cli_arg_re = re.compile(r"add_argument\(\s*[\"'](--[a-zA-Z0-9_-]+)[\"']")
    getattr_re = re.compile(r"getattr\(\s*args\s*,\s*[\"']([a-zA-Z0-9_:-]+)[\"']")
    env_re = re.compile(r"os\.environ\.get\(\s*[\"']([A-Z0-9_]+)[\"']")
    nested_toml_re = re.compile(r"_nested_get\([^,]+,\s*[\"']([^\"']+)[\"']\)")
    settings_attr_re = re.compile(r"\bsettings\.([a-zA-Z_][a-zA-Z0-9_]*)\b")

    for idx, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped:
            continue

        for match in cli_arg_re.finditer(stripped):
            key = match.group(1).lstrip("-")
            marker = (key, "cli", idx)
            if marker in seen:
                continue
            seen.add(marker)
            influences.append(
                SettingsInfluence(
                    setting_key=key,
                    input_channel="cli",
                    effect_summary=f"CLI flag '--{key}' influences behavior.",
                    evidence=Evidence(path=rel_target, line=idx, text=stripped),
                    confidence="high",
                )
            )

        for match in getattr_re.finditer(stripped):
            key = match.group(1)
            marker = (key, "cli", idx)
            if marker in seen:
                continue
            seen.add(marker)
            influences.append(
                SettingsInfluence(
                    setting_key=key,
                    input_channel="cli",
                    effect_summary=f"Reads argument field 'args.{key}'.",
                    evidence=Evidence(path=rel_target, line=idx, text=stripped),
                    confidence="medium",
                )
            )

        for match in env_re.finditer(stripped):
            key = match.group(1)
            marker = (key, "env", idx)
            if marker in seen:
                continue
            seen.add(marker)
            influences.append(
                SettingsInfluence(
                    setting_key=key,
                    input_channel="env",
                    effect_summary=f"Reads environment variable '{key}'.",
                    evidence=Evidence(path=rel_target, line=idx, text=stripped),
                    confidence="high",
                )
            )

        for match in nested_toml_re.finditer(stripped):
            key = match.group(1)
            marker = (key, "toml", idx)
            if marker in seen:
                continue
            seen.add(marker)
            influences.append(
                SettingsInfluence(
                    setting_key=key,
                    input_channel="toml",
                    effect_summary=f"Reads config path '{key}' from TOML payload.",
                    evidence=Evidence(path=rel_target, line=idx, text=stripped),
                    confidence="high",
                )
            )

        for match in settings_attr_re.finditer(stripped):
            key = match.group(1)
            marker = (key, "code", idx)
            if marker in seen:
                continue
            seen.add(marker)
            influences.append(
                SettingsInfluence(
                    setting_key=key,
                    input_channel="code",
                    effect_summary=f"Uses resolved settings field 'settings.{key}'.",
                    evidence=Evidence(path=rel_target, line=idx, text=stripped),
                    confidence="medium",
                )
            )

    # Deduplicate by (setting_key, input_channel) while keeping strongest confidence/evidence.
    by_key: dict[tuple[str, str], SettingsInfluence] = {}
    for item in influences:
        key = (item.setting_key, item.input_channel)
        existing = by_key.get(key)
        if existing is None:
            by_key[key] = item
            continue
        if existing.confidence == "high":
            continue
        if item.confidence == "high":
            by_key[key] = item
    ordered = list(by_key.values())
    ordered.sort(key=lambda x: (x.input_channel, x.setting_key))
    return ordered[:20]


def extract_default_values(rel_target: Path, content: str) -> list[DefaultValueSignal]:
    defaults: list[DefaultValueSignal] = []
    seen: set[tuple[str, str, int]] = set()
    lines = content.splitlines()

    const_re = re.compile(r"^([A-Z][A-Z0-9_]{2,})\s*=\s*(.+)$")
    or_default_re = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*_([a-zA-Z]+)_or_default\([^,]+,\s*([^)]+)\)")
    getattr_default_re = re.compile(r"getattr\(\s*args\s*,\s*[\"']([a-zA-Z0-9_:-]+)[\"']\s*,\s*([^)]+)\)")

    for idx, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped:
            continue

        m_const = const_re.match(stripped)
        if m_const:
            name = m_const.group(1)
            value = m_const.group(2).strip()
            marker = (name, value, idx)
            if marker not in seen:
                seen.add(marker)
                defaults.append(
                    DefaultValueSignal(
                        name=name,
                        value_repr=value,
                        activation_condition="used when no overriding input is applied",
                        evidence=Evidence(path=rel_target, line=idx, text=stripped),
                        confidence="medium",
                    )
                )

        m_or = or_default_re.search(stripped)
        if m_or:
            name = m_or.group(1)
            value = m_or.group(3).strip()
            marker = (name, value, idx)
            if marker not in seen:
                seen.add(marker)
                defaults.append(
                    DefaultValueSignal(
                        name=name,
                        value_repr=value,
                        activation_condition="applies when parsed input is missing/invalid",
                        evidence=Evidence(path=rel_target, line=idx, text=stripped),
                        confidence="high",
                    )
                )

        m_getattr = getattr_default_re.search(stripped)
        if m_getattr:
            name = m_getattr.group(1)
            value = m_getattr.group(2).strip()
            marker = (name, value, idx)
            if marker not in seen:
                seen.add(marker)
                defaults.append(
                    DefaultValueSignal(
                        name=name,
                        value_repr=value,
                        activation_condition="used when CLI attribute is absent",
                        evidence=Evidence(path=rel_target, line=idx, text=stripped),
                        confidence="medium",
                    )
                )

    defaults.sort(key=lambda x: x.name)
    return defaults[:24]


def extract_llm_participation(rel_target: Path, content: str) -> list[LLMParticipation]:
    patterns: list[tuple[re.Pattern[str], str, str, str]] = [
        (re.compile(r"\bresolve_settings\("), "llm_config_resolution", "required", "high"),
        (re.compile(r"\bmaybe_plan_query_terms\("), "query_planner", "optional", "high"),
        (re.compile(r"\bmaybe_orchestrate_query_actions\("), "query_orchestrator", "optional", "high"),
        (re.compile(r"\bmaybe_refine_summary\("), "summary_refinement", "optional", "high"),
        (re.compile(r"\b_openai_compatible_complete\("), "provider_completion_call", "optional", "high"),
        (re.compile(r"\bpolicy_for\("), "policy_gate", "disabled_by_policy", "medium"),
        (re.compile(r"fallback_reason"), "fallback_path", "fallback", "medium"),
        (re.compile(r"\bllm_outcome\.usage\b"), "llm_usage_reporting", "optional", "medium"),
    ]
    items: list[LLMParticipation] = []
    seen: set[tuple[str, int]] = set()
    for idx, raw in enumerate(content.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped:
            continue
        for pattern, stage, kind, confidence in patterns:
            if not pattern.search(stripped):
                continue
            marker = (stage, idx)
            if marker in seen:
                continue
            seen.add(marker)
            items.append(
                LLMParticipation(
                    stage=stage,
                    kind=kind,
                    evidence=Evidence(path=rel_target, line=idx, text=stripped),
                    confidence=confidence,
                )
            )
            break
    dedup: dict[str, LLMParticipation] = {}
    for item in items:
        existing = dedup.get(item.stage)
        if existing is None:
            dedup[item.stage] = item
            continue
        if existing.confidence == "high":
            continue
        if item.confidence == "high":
            dedup[item.stage] = item
    ordered = list(dedup.values())
    ordered.sort(key=lambda x: x.stage)
    return ordered[:20]


def extract_output_surfaces(rel_target: Path, content: str) -> list[OutputSurface]:
    patterns: list[tuple[re.Pattern[str], str, str, str, str]] = [
        (re.compile(r"\bprint\("), "console", "stdout", "print(...)", "high"),
        (re.compile(r"\bemit_contract_json\("), "json_contract", "contract_json", "emit_contract_json(...)", "high"),
        (re.compile(r"\bwrite_forge_file\("), "artifact_file", ".forge artifact", "write_forge_file(...)", "high"),
        (re.compile(r"\blog_llm_event\("), "log_file", ".forge/logs/llm_observability.jsonl", "log_llm_event(...)", "high"),
        (re.compile(r"\bappend_run\("), "artifact_file", "run_history", "append_run(...)", "medium"),
        (re.compile(r"\.jsonl"), "log_file", "jsonl output", "path includes .jsonl", "medium"),
        (re.compile(r"\.forge/"), "artifact_file", ".forge/*", "path includes .forge/", "medium"),
    ]
    items: list[OutputSurface] = []
    seen: set[tuple[str, str]] = set()
    for idx, raw in enumerate(content.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped:
            continue
        for pattern, surface, path_or_section, producer, confidence in patterns:
            if not pattern.search(stripped):
                continue
            marker = (surface, path_or_section)
            if marker in seen:
                continue
            seen.add(marker)
            items.append(
                OutputSurface(
                    surface=surface,
                    path_or_section=path_or_section,
                    producer=producer,
                    evidence=Evidence(path=rel_target, line=idx, text=stripped),
                    confidence=confidence,
                )
            )
            break
    items.sort(key=lambda x: (x.surface, x.path_or_section))
    return items[:20]


def build_focus_answer(
    *,
    focus: str,
    rel_target: Path,
    settings_influences: list[SettingsInfluence],
    default_values: list[DefaultValueSignal],
    llm_participation: list[LLMParticipation],
    output_surfaces: list[OutputSurface],
) -> str | None:
    if focus == "settings":
        if not settings_influences:
            return f"No clear settings inputs were detected for {rel_target} in the current static read."
        channels = sorted({item.input_channel for item in settings_influences})
        return (
            f"{rel_target} is influenced by {len(settings_influences)} detected settings inputs "
            f"across channels: {', '.join(channels)}."
        )
    if focus == "defaults":
        if not default_values:
            return f"No explicit in-code default values were detected for {rel_target} in the current static read."
        high_count = sum(1 for item in default_values if item.confidence == "high")
        confidence = _confidence_for_hits(high_count)
        return (
            f"{rel_target} defines {len(default_values)} detected default values/signals; "
            f"overall default-detection confidence is {confidence}."
        )
    if focus == "llm":
        if not llm_participation:
            return f"No explicit LLM participation markers were detected for {rel_target}."
        kinds = sorted({item.kind for item in llm_participation})
        return (
            f"{rel_target} shows {len(llm_participation)} LLM participation stages "
            f"with kinds: {', '.join(kinds)}."
        )
    if focus == "outputs":
        if not output_surfaces:
            return f"No explicit output surfaces were detected for {rel_target}."
        surfaces = sorted({item.surface for item in output_surfaces})
        return (
            f"{rel_target} exposes {len(output_surfaces)} output surfaces across: "
            f"{', '.join(surfaces)}."
        )
    return None


def build_deterministic_summary(
    *,
    rel_target: Path,
    role: str,
    target: ResolvedTarget,
    request: CommandRequest,
    behavior_signals: list[str],
) -> str:
    if target.source == "symbol":
        symbol = request.payload.strip()
        if behavior_signals:
            joined = "; ".join(behavior_signals[:4])
            return f"{rel_target} defines {symbol} and appears to: {joined}."
        return f"{rel_target} defines {symbol} and is primarily {role}."
    if behavior_signals:
        joined = "; ".join(behavior_signals[:3])
        return f"{rel_target} is primarily {role} and appears to: {joined}."
    return f"{rel_target} is primarily {role}."


def uncertainty_notes(target: ResolvedTarget, evidence: list[Evidence], profile: Profile) -> list[str]:
    notes: list[str] = []
    if target.source == "symbol":
        notes.append("target was resolved via best-effort symbol matching across files")
    if len(evidence) < 3:
        notes.append("limited structural evidence found in target")
    if profile == Profile.SIMPLE:
        notes.append("simple profile uses target-local analysis only")
    return notes


def build_evidence_facts(repo_root: Path, evidence: list[Evidence]) -> list[dict[str, object]]:
    facts: list[dict[str, object]] = []
    for idx, item in enumerate(evidence, start=1):
        fact_id = f"E{idx}"
        rel_path = item.path.relative_to(repo_root)
        facts.append(
            {
                "id": fact_id,
                "path": str(rel_path),
                "line": item.line,
                "fact": item.text,
            }
        )
    return facts


def build_inference_points(
    *,
    role: str,
    rationale: str,
    evidence_facts: list[dict[str, object]],
    profile: Profile,
) -> list[InferencePoint]:
    evidence_ids = [str(item.get("id")) for item in evidence_facts if isinstance(item.get("id"), str)]
    strong = len(evidence_ids) >= 6
    medium = len(evidence_ids) >= 3
    if strong:
        level = "high"
        confidence_reason = "multiple structural evidence anchors are present"
    elif medium:
        level = "medium"
        confidence_reason = "some evidence anchors are present, but coverage is limited"
    else:
        level = "low"
        confidence_reason = "few direct evidence anchors were found"

    points: list[InferencePoint] = [
        InferencePoint(
            inference_id="I1",
            inference=f"Primary role hypothesis: this target is {role}.",
            evidence_ids=evidence_ids[:6],
            rationale=rationale,
            confidence=level,
        )
    ]
    if profile in {Profile.STANDARD, Profile.DETAILED}:
        points.append(
            InferencePoint(
                inference_id="I2",
                inference="The current role classification is based on visible structural markers, not runtime behavior.",
                evidence_ids=evidence_ids[:4],
                rationale="classification uses path/content/index signals from the resolved target",
                confidence="medium" if evidence_ids else "low",
            )
        )
    if profile == Profile.DETAILED:
        points.append(
            InferencePoint(
                inference_id="I3",
                inference="Related-file context may adjust interpretation boundaries for this target.",
                evidence_ids=evidence_ids[:3],
                rationale="related files are detected via deterministic repo-local matching",
                confidence="medium" if len(evidence_ids) >= 3 else "low",
            )
        )
    # Keep rationale from evidence-density computation visible by appending to first point.
    points[0].rationale = f"{points[0].rationale}; {confidence_reason}"
    return points


def build_role_hypothesis_alternatives(
    *,
    role: str,
    profile: Profile,
    evidence_facts: list[dict[str, object]],
) -> list[dict[str, object]]:
    if profile != Profile.DETAILED:
        return []
    evidence_density = len(evidence_facts)
    alternatives: list[dict[str, object]] = []
    if role != "implementation":
        alternatives.append(
            {
                "role": "implementation",
                "rationale": "target may still contain executable/source logic despite current primary role",
                "confidence": "medium" if evidence_density >= 5 else "low",
            }
        )
    if role != "support code":
        alternatives.append(
            {
                "role": "support code",
                "rationale": "helper/utility markers can overlap with implementation structure",
                "confidence": "low",
            }
        )
    return alternatives[:3]


def print_explanation(
    request: CommandRequest,
    repo_root: Path,
    target: ResolvedTarget,
    role: str,
    rationale: str,
    summary: str,
    evidence: list[Evidence],
    related: list[Path],
    uncertainties: list[str],
    index_status: str | None,
    next_step: str,
    view: str,
    inference_points: list[InferencePoint],
    behavior_signals: list[str],
    focus_answer: str | None,
    settings_influences: list[SettingsInfluence],
    default_values: list[DefaultValueSignal],
    explain_focus: str,
    llm_participation: list[LLMParticipation],
    output_surfaces: list[OutputSurface],
) -> None:
    def _display_path(path: Path) -> Path:
        try:
            return path.relative_to(repo_root)
        except ValueError:
            return path

    rel_target = target.path.relative_to(repo_root)
    print("=== FORGE EXPLAIN ===")
    print(f"Profile: {request.profile.value}")
    print(f"Target: {request.payload}")
    if index_status:
        print(f"Index: {index_status}")
    print(f"Resolved target: {rel_target} ({target.source})")

    print("\n--- Summary ---")
    print(summary)

    if is_full(view):
        print("\n--- Role Classification ---")
        print(f"Role: {role}")
        print(f"Reason: {rationale}")

    print("\n--- Evidence ---")
    if not evidence:
        print("No concrete evidence extracted.")
    evidence_limit = 2 if is_compact(view) else 3 if view == "standard" else len(evidence)
    for item in evidence[:evidence_limit]:
        path_display = _display_path(item.path)
        print(f"{path_display}:{item.line}: {item.text}")

    if is_full(view):
        print("\n--- Behavior Signals ---")
        if behavior_signals:
            for item in behavior_signals:
                print(f"- {item}")
        else:
            print("No clear behavior signals extracted from current target window.")

    if focus_answer:
        print("\n--- Focus Answer ---")
        print(focus_answer)
        if is_full(view):
            if explain_focus == "settings":
                print("\n--- Settings Influences ---")
                if settings_influences:
                    for item in settings_influences[:20]:
                        print(
                            f"- {item.setting_key} [{item.input_channel}] "
                            f"confidence={item.confidence} "
                            f"@ {_display_path(item.evidence.path)}:{item.evidence.line}"
                        )
                        print(f"  {item.effect_summary}")
                else:
                    print("No settings influences detected.")
            if explain_focus == "defaults":
                print("\n--- Default Values ---")
                if default_values:
                    for item in default_values[:20]:
                        print(
                            f"- {item.name}={item.value_repr} "
                            f"confidence={item.confidence} "
                            f"@ {_display_path(item.evidence.path)}:{item.evidence.line}"
                        )
                        print(f"  activation: {item.activation_condition}")
                else:
                    print("No default values detected.")
            if explain_focus == "llm":
                print("\n--- LLM Participation ---")
                if llm_participation:
                    for item in llm_participation[:20]:
                        print(
                            f"- {item.stage} kind={item.kind} confidence={item.confidence} "
                            f"@ {_display_path(item.evidence.path)}:{item.evidence.line}"
                        )
                else:
                    print("No LLM participation markers detected.")
            if explain_focus == "outputs":
                print("\n--- Output Surfaces ---")
                if output_surfaces:
                    for item in output_surfaces[:20]:
                        print(
                            f"- {item.surface} [{item.path_or_section}] producer={item.producer} "
                            f"confidence={item.confidence} "
                            f"@ {_display_path(item.evidence.path)}:{item.evidence.line}"
                        )
                else:
                    print("No output surfaces detected.")

    print("\n--- Inference ---")
    inference_limit = 1 if is_compact(view) else 2 if view == "standard" else len(inference_points)
    for point in inference_points[:inference_limit]:
        print(f"- {point.inference}")
        if is_full(view):
            print(f"  rationale: {point.rationale}")

    print("\n--- Confidence ---")
    confidence_limit = 1 if is_compact(view) else 2 if view == "standard" else len(inference_points)
    for point in inference_points[:confidence_limit]:
        print(f"- {point.inference_id}: {point.confidence}")
        if is_full(view):
            print(f"  rationale: {point.rationale}")

    if request.profile in {Profile.STANDARD, Profile.DETAILED} and is_full(view):
        print("\n--- Related Files ---")
        if related:
            related_limit = len(related)
            for rel in related[:related_limit]:
                print(rel)
        else:
            print("No related files found.")

    print("\n--- Uncertainty ---")
    if uncertainties:
        notes = uncertainties if is_full(view) else uncertainties[:1]
        for note in notes:
            print(f"- {note}")
    else:
        print("No major uncertainty flags from current read pass.")

    print("\n--- Next Step ---")
    print(next_step)


def run(request: CommandRequest, args, session: ExecutionSession) -> int:
    view = resolve_view(args)
    repo_root = Path(args.repo_root).resolve()
    explain_focus = str(getattr(args, "explain_focus", "overview") or "overview")
    explain_focus_source = str(getattr(args, "explain_focus_source", "default") or "default")
    explain_command = str(getattr(args, "explain_command", "explain") or "explain")
    try:
        resolved_payload, from_run_meta = resolve_from_run_payload(
            repo_root=repo_root,
            requested_capability=request.capability,
            explicit_payload=request.payload,
            from_run_id=getattr(args, "from_run", None),
            confirm_transition=bool(getattr(args, "confirm_transition", False)),
        )
    except RunReferenceError as exc:
        contract = build_contract(
            capability=request.capability.value,
            profile=request.profile.value,
            summary="Run reference could not be resolved.",
            evidence=[],
            uncertainty=[str(exc)],
            next_step="Run: forge runs list",
            sections={"status": "from_run_resolution_failed"},
        )
        if args.output_format == "json":
            emit_contract_json(contract)
            return 1
        print(f"Run reference error: {exc}")
        return 1

    request = CommandRequest(capability=request.capability, profile=request.profile, payload=resolved_payload)
    raw_target = request.payload.strip()

    target = resolve_file_or_symbol_target(repo_root, raw_target, session)

    if target is None:
        summary = "Target could not be resolved to a readable file or known symbol."
        uncertainty = [
            "no matching file path under repo root",
            "no symbol-like match found in readable text files",
        ]
        next_step = 'Run: forge query "where is this symbol defined?"'
        contract = build_contract(
            capability=request.capability.value,
            profile=request.profile.value,
            summary=summary,
            evidence=[],
            uncertainty=uncertainty,
            next_step=next_step,
            sections={"role_classification": None, "related_files": []},
        )
        if args.output_format == "json":
            emit_contract_json(contract)
            return 0
        print("=== FORGE EXPLAIN ===")
        print(f"Profile: {request.profile.value}")
        print(f"Target: {request.payload}")
        print("\n--- Summary ---")
        print(summary)
        print("\n--- Uncertainty ---")
        for note in uncertainty:
            print(f"- {note}")
        print("\n--- Next Step ---")
        print(next_step)
        return 0

    rel_target = target.path.relative_to(repo_root)
    index_entries = {}
    path_classes: dict[str, str] = {}
    index_status: str | None = None
    if request.profile in {Profile.STANDARD, Profile.DETAILED}:
        index_entries = load_index_entry_map(repo_root, session)
        path_classes = load_index_path_class_map(repo_root, session)
        if path_classes:
            index_status = "loaded .forge/index.json"
        else:
            index_status = "not available, using direct repository scan only"
    index_entry = index_entries.get(str(rel_target))

    role, rationale = classify_role(rel_target, target.content, index_entry)
    evidence = gather_evidence_for_target(target, request)
    related: list[Path] = []
    if request.profile in {Profile.STANDARD, Profile.DETAILED}:
        related_rel = find_related_files(repo_root, rel_target, session, limit=10)
        related_abs = [repo_root / rel for rel in related_rel]
        prioritized = prioritize_paths_by_index(
            repo_root,
            related_abs,
            path_classes,
            exclude_non_index_participating=True,
        )
        if not prioritized:
            prioritized = related_abs
        related = [path.relative_to(repo_root) for path in prioritized[:5]]
    uncertainties = uncertainty_notes(target, evidence, request.profile)
    next_step = f"Run: forge review {rel_target}"
    evidence_payload = [
        {
            "path": str(item.path.relative_to(repo_root)),
            "line": item.line,
            "text": item.text,
            "source_type": "repo",
            "source_origin": "repo",
            "framework_id": None,
            "framework_version": None,
        }
        for item in evidence
    ]
    evidence_facts = build_evidence_facts(repo_root, evidence)
    behavior_signals = build_behavior_signals(target, request)
    settings_influences = (
        extract_settings_influences(rel_target, target.content) if explain_focus == "settings" else []
    )
    default_values = extract_default_values(rel_target, target.content) if explain_focus == "defaults" else []
    llm_participation = extract_llm_participation(rel_target, target.content) if explain_focus == "llm" else []
    output_surfaces = extract_output_surfaces(rel_target, target.content) if explain_focus == "outputs" else []
    focus_answer = build_focus_answer(
        focus=explain_focus,
        rel_target=rel_target,
        settings_influences=settings_influences,
        default_values=default_values,
        llm_participation=llm_participation,
        output_surfaces=output_surfaces,
    )
    inference_points = build_inference_points(
        role=role,
        rationale=rationale,
        evidence_facts=evidence_facts,
        profile=request.profile,
    )
    role_hypothesis_alternatives = build_role_hypothesis_alternatives(
        role=role,
        profile=request.profile,
        evidence_facts=evidence_facts,
    )
    sections = {
        "explain": {
            "command": explain_command,
            "focus": explain_focus,
            "focus_source": explain_focus_source,
        },
        "role_classification": {"role": role, "reason": rationale},
        "related_files": [str(path) for path in related],
        "resolved_target": str(rel_target),
        "resolved_target_source": {
            "source_type": "repo",
            "source_origin": "repo",
            "framework_id": None,
            "framework_version": None,
        },
        "evidence_facts": evidence_facts,
        "inference_points": [
            {
                "id": point.inference_id,
                "inference": point.inference,
                "evidence_ids": point.evidence_ids,
                "rationale": point.rationale,
            }
            for point in inference_points
        ],
        "confidence": [
            {
                "inference_id": point.inference_id,
                "level": point.confidence,
                "rationale": point.rationale,
            }
            for point in inference_points
        ],
        "behavior_signals": behavior_signals,
    }
    if explain_focus == "settings":
        sections["direct_answer"] = focus_answer
        sections["settings_influences"] = [
            {
                "setting_key": item.setting_key,
                "input_channel": item.input_channel,
                "effect_summary": item.effect_summary,
                "evidence": {
                    "path": str(item.evidence.path),
                    "line": item.evidence.line,
                    "text": item.evidence.text,
                },
                "confidence": item.confidence,
            }
            for item in settings_influences
        ]
    if explain_focus == "defaults":
        sections["direct_answer"] = focus_answer
        sections["default_values"] = [
            {
                "name": item.name,
                "value_repr": item.value_repr,
                "activation_condition": item.activation_condition,
                "evidence": {
                    "path": str(item.evidence.path),
                    "line": item.evidence.line,
                    "text": item.evidence.text,
                },
                "confidence": item.confidence,
            }
            for item in default_values
        ]
    if explain_focus == "llm":
        sections["direct_answer"] = focus_answer
        sections["llm_participation"] = [
            {
                "stage": item.stage,
                "kind": item.kind,
                "evidence": {
                    "path": str(item.evidence.path),
                    "line": item.evidence.line,
                    "text": item.evidence.text,
                },
                "confidence": item.confidence,
            }
            for item in llm_participation
        ]
    if explain_focus == "outputs":
        sections["direct_answer"] = focus_answer
        sections["output_surfaces"] = [
            {
                "surface": item.surface,
                "path_or_section": item.path_or_section,
                "producer": item.producer,
                "evidence": {
                    "path": str(item.evidence.path),
                    "line": item.evidence.line,
                    "text": item.evidence.text,
                },
                "confidence": item.confidence,
            }
            for item in output_surfaces
        ]
    if role_hypothesis_alternatives:
        sections["role_hypothesis_alternatives"] = role_hypothesis_alternatives
    if from_run_meta:
        sections.update(from_run_meta)
    if focus_answer:
        deterministic_summary = focus_answer
    else:
        deterministic_summary = build_deterministic_summary(
            rel_target=rel_target,
            role=role,
            target=target,
            request=request,
            behavior_signals=behavior_signals,
        )
    llm_settings = resolve_settings(args, repo_root)
    llm_outcome = maybe_refine_summary(
        capability=request.capability,
        profile=request.profile,
        task=request.payload,
        deterministic_summary=deterministic_summary,
        evidence=evidence_payload,
        settings=llm_settings,
        repo_root=repo_root,
    )
    summary = llm_outcome.summary
    uncertainties.extend(llm_outcome.uncertainty_notes)
    sections["llm_usage"] = llm_outcome.usage
    sections["provenance"] = provenance_section(
        llm_used=bool(llm_outcome.usage.get("used")),
        evidence_count=len(evidence_payload),
    )

    contract = build_contract(
        capability=request.capability.value,
        profile=request.profile.value,
        summary=summary,
        evidence=evidence_payload,
        uncertainty=uncertainties,
        next_step=next_step,
        sections=sections,
    )
    if args.output_format == "json":
        emit_contract_json(contract)
        return 0

    print_explanation(
        request=request,
        repo_root=repo_root,
        target=target,
        role=role,
        rationale=rationale,
        summary=summary,
        evidence=evidence,
        related=related,
        uncertainties=uncertainties,
        index_status=index_status,
        next_step=next_step,
        view=view,
        inference_points=inference_points,
        behavior_signals=behavior_signals,
        focus_answer=focus_answer,
        settings_influences=settings_influences,
        default_values=default_values,
        explain_focus=explain_focus,
        llm_participation=llm_participation,
        output_surfaces=output_surfaces,
    )
    if is_full(view):
        print("\n--- Explain ---")
        print(f"Command: {explain_command}")
        print(f"Focus: {explain_focus}")
        print(f"Focus source: {explain_focus_source}")
    if from_run_meta:
        print("\n--- From Run ---")
        print(f"Source run id: {from_run_meta['source_run_id']}")
        print(f"Source capability: {from_run_meta['source_run_capability']}")
        print(f"Strategy: {from_run_meta['resolved_from_run_strategy']}")
        print(f"Resolved payload: {from_run_meta['resolved_from_run_payload']}")
        if "transition_source_mode" in from_run_meta and "transition_target_mode" in from_run_meta:
            print(f"Transition: {from_run_meta['transition_source_mode']} -> {from_run_meta['transition_target_mode']}")
            print(f"Transition policy: {from_run_meta.get('transition_policy_reason', 'n/a')}")
        gate_decisions = from_run_meta.get("transition_gate_decisions", [])
        if is_full(view) and isinstance(gate_decisions, list):
            print("Transition gates:")
            for item in gate_decisions:
                if not isinstance(item, dict):
                    continue
                print(
                    f"- {item.get('gate', '?')}: {item.get('status', '?')} "
                    f"({item.get('detail', 'no detail')})"
                )
    if is_full(view):
        print("\n--- LLM Usage ---")
        print(f"Policy: {llm_outcome.usage['policy']}")
        print(f"Mode: {llm_outcome.usage['mode']}")
        print(f"Used: {llm_outcome.usage['used']}")
        print(f"Provider: {llm_outcome.usage['provider'] or 'none'}")
        print(f"Base URL: {llm_outcome.usage['base_url'] or 'none'}")
        print(f"Model: {llm_outcome.usage['model'] or 'none'}")
        print(f"Output language: {llm_outcome.usage.get('output_language') or 'auto'}")
        if llm_outcome.usage.get("fallback_reason"):
            print(f"Fallback: {llm_outcome.usage['fallback_reason']}")
        print("\n--- Provenance ---")
        print(f"Evidence items: {len(evidence_payload)}")
        print(
            "Inference source: "
            + ("deterministic heuristics + LLM" if llm_outcome.usage["used"] else "deterministic heuristics")
        )
    return 0
