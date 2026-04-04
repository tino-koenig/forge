from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Evidence:
    path: Path
    line: int
    text: str


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


@dataclass
class SymbolFact:
    name: str
    kind: str
    evidence: Evidence
    confidence: str


def confidence_for_hits(hit_count: int) -> str:
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
        (re.compile(r"\bappend_protocol_events\("), "log_file", ".forge/logs/events.jsonl", "append_protocol_events(...)", "high"),
        (re.compile(r"\bappend_run\("), "artifact_file", "run_history", "append_run(...)", "medium"),
        (re.compile(r"\.write_text\("), "artifact_file", "file_write", "write_text(...)", "high"),
        (re.compile(r"\.write_bytes\("), "artifact_file", "file_write", "write_bytes(...)", "high"),
        (
            re.compile(r"\.open\(\s*[^,]+,\s*['\"](?:w|a|x|wb|ab|xb)['\"]"),
            "artifact_file",
            "file_open_write",
            "open(..., write-mode)",
            "medium",
        ),
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


def extract_symbol_facts(rel_target: Path, content: str) -> list[SymbolFact]:
    items: list[SymbolFact] = []
    seen: set[tuple[str, str]] = set()
    for idx, raw in enumerate(content.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped:
            continue
        m_class = re.match(r"^class\s+([A-Za-z_][A-Za-z0-9_]*)\b", stripped)
        if m_class:
            name = m_class.group(1)
            marker = ("class", name)
            if marker not in seen:
                seen.add(marker)
                items.append(
                    SymbolFact(
                        name=name,
                        kind="class",
                        evidence=Evidence(path=rel_target, line=idx, text=stripped),
                        confidence="high",
                    )
                )
            continue
        m_def = re.match(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)\b", stripped)
        if m_def:
            name = m_def.group(1)
            marker = ("function", name)
            if marker not in seen:
                seen.add(marker)
                items.append(
                    SymbolFact(
                        name=name,
                        kind="function",
                        evidence=Evidence(path=rel_target, line=idx, text=stripped),
                        confidence="high",
                    )
                )
    return items[:24]
