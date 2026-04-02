from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from core.capability_model import CommandRequest, EffectClass, Profile
from core.effects import ExecutionSession
from core.repo_io import iter_repo_files, read_text_file


@dataclass
class Evidence:
    path: Path
    line: int
    text: str


@dataclass
class ExplainTarget:
    path: Path
    content: str
    source: str


ROLE_MARKERS = {
    "entrypoint": ["if __name__ == \"__main__\":", "argparse.ArgumentParser(", "main("],
    "configuration": [".yml", ".yaml", ".toml", ".ini", "config", "settings"],
    "support code": ["helper", "util", "common", "shared", "support"],
}


def load_index_file_entries(repo_root: Path, session: ExecutionSession) -> dict[str, dict[str, object]]:
    index_path = repo_root / ".forge" / "index.json"
    if not index_path.exists():
        return {}

    session.record_effect(EffectClass.READ_ONLY, f"read index data {index_path}")
    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}

    files = payload.get("entries", {}).get("files", [])
    if not isinstance(files, list):
        return {}

    by_path: dict[str, dict[str, object]] = {}
    for entry in files:
        if not isinstance(entry, dict):
            continue
        rel = entry.get("path")
        if isinstance(rel, str):
            by_path[rel] = entry
    return by_path


def resolve_as_file_target(repo_root: Path, raw_target: str, session: ExecutionSession) -> ExplainTarget | None:
    candidate = Path(raw_target)
    if candidate.is_absolute():
        abs_path = candidate.resolve()
    else:
        abs_path = (repo_root / candidate).resolve()

    try:
        abs_path.relative_to(repo_root)
    except ValueError:
        return None

    if not abs_path.is_file():
        return None

    content = read_text_file(abs_path, session)
    if content is None:
        return None
    return ExplainTarget(path=abs_path, content=content, source="file")


def resolve_as_symbol_target(repo_root: Path, symbol: str, session: ExecutionSession) -> ExplainTarget | None:
    if not symbol.strip():
        return None

    name = symbol.strip()
    definition_patterns = [
        f"def {name}(",
        f"class {name}(",
        f"class {name}:",
    ]
    mention_pattern = name

    best_path: Path | None = None
    best_content: str | None = None
    best_score = 0

    for path in iter_repo_files(repo_root, session):
        content = read_text_file(path, session)
        if not content:
            continue

        definition_hits = sum(content.count(pattern) for pattern in definition_patterns)
        mention_hits = content.count(mention_pattern)
        score = (definition_hits * 100) + mention_hits

        if score > best_score and score > 0:
            best_path = path
            best_content = content
            best_score = score

    if best_path is None or best_content is None:
        return None
    return ExplainTarget(path=best_path, content=best_content, source="symbol")


def classify_role(rel_path: Path, content: str, index_entry: dict[str, object] | None) -> tuple[str, str]:
    lowered_path = str(rel_path).lower()
    lowered_content = content.lower()

    if any(marker in content for marker in ROLE_MARKERS["entrypoint"]):
        return "entrypoint", "contains explicit startup/CLI entry markers"

    if "config" in lowered_path or any(ext in lowered_path for ext in [".yml", ".yaml", ".toml", ".ini"]):
        return "configuration", "path/extension suggests configuration data"

    if index_entry:
        symbols = index_entry.get("top_level_symbols")
        if isinstance(symbols, list) and symbols:
            if len(symbols) >= 3:
                return "implementation", "contains multiple top-level symbols"

    if any(marker in lowered_path or marker in lowered_content for marker in ROLE_MARKERS["support code"]):
        return "support code", "path/content suggests helper or utility responsibilities"

    return "implementation", "default classification from executable/source structure"


def gather_evidence_for_target(
    target: ExplainTarget,
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


def find_related_files(repo_root: Path, target_rel: Path, session: ExecutionSession) -> list[Path]:
    stem = target_rel.stem.lower()
    if not stem:
        return []
    related: list[Path] = []
    for path in iter_repo_files(repo_root, session):
        rel = path.relative_to(repo_root)
        if rel == target_rel:
            continue
        if stem in rel.stem.lower():
            related.append(rel)
        if len(related) >= 5:
            break
    return related


def uncertainty_notes(target: ExplainTarget, evidence: list[Evidence], profile: Profile) -> list[str]:
    notes: list[str] = []
    if target.source == "symbol":
        notes.append("target was resolved via best-effort symbol matching across files")
    if len(evidence) < 3:
        notes.append("limited structural evidence found in target")
    if profile == Profile.SIMPLE:
        notes.append("simple profile uses target-local analysis only")
    return notes


def print_explanation(
    request: CommandRequest,
    repo_root: Path,
    target: ExplainTarget,
    role: str,
    rationale: str,
    evidence: list[Evidence],
    related: list[Path],
    uncertainties: list[str],
) -> None:
    rel_target = target.path.relative_to(repo_root)
    print("=== FORGE EXPLAIN ===")
    print(f"Profile: {request.profile.value}")
    print(f"Target: {request.payload}")
    print(f"Resolved target: {rel_target} ({target.source})")

    print("\n--- Summary ---")
    print(f"{rel_target} is primarily {role}.")

    print("\n--- Role Classification ---")
    print(f"Role: {role}")
    print(f"Reason: {rationale}")

    print("\n--- Evidence ---")
    if not evidence:
        print("No concrete evidence extracted.")
    for item in evidence:
        path_display = item.path.relative_to(repo_root)
        print(f"{path_display}:{item.line}: {item.text}")

    if request.profile in {Profile.STANDARD, Profile.DETAILED}:
        print("\n--- Related Files ---")
        if related:
            for rel in related:
                print(rel)
        else:
            print("No related files found.")

    print("\n--- Uncertainty ---")
    if uncertainties:
        for note in uncertainties:
            print(f"- {note}")
    else:
        print("No major uncertainty flags from current read pass.")


def run(request: CommandRequest, args, session: ExecutionSession) -> int:
    repo_root = Path(args.repo_root).resolve()
    raw_target = request.payload.strip()

    target = resolve_as_file_target(repo_root, raw_target, session)
    if target is None:
        target = resolve_as_symbol_target(repo_root, raw_target, session)

    if target is None:
        print("=== FORGE EXPLAIN ===")
        print(f"Profile: {request.profile.value}")
        print(f"Target: {request.payload}")
        print("\n--- Summary ---")
        print("Target could not be resolved to a readable file or known symbol.")
        print("\n--- Uncertainty ---")
        print("- no matching file path under repo root")
        print("- no symbol-like match found in readable text files")
        return 0

    rel_target = target.path.relative_to(repo_root)
    index_entries = {}
    if request.profile in {Profile.STANDARD, Profile.DETAILED}:
        index_entries = load_index_file_entries(repo_root, session)
    index_entry = index_entries.get(str(rel_target))

    role, rationale = classify_role(rel_target, target.content, index_entry)
    evidence = gather_evidence_for_target(target, request)
    related: list[Path] = []
    if request.profile in {Profile.STANDARD, Profile.DETAILED}:
        related = find_related_files(repo_root, rel_target, session)
    uncertainties = uncertainty_notes(target, evidence, request.profile)

    print_explanation(
        request=request,
        repo_root=repo_root,
        target=target,
        role=role,
        rationale=rationale,
        evidence=evidence,
        related=related,
        uncertainties=uncertainties,
    )
    return 0
