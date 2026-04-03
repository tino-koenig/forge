"""Shared read-only analysis primitives used by multiple capabilities."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from core.capability_model import EffectClass
from core.effects import ExecutionSession
from core.repo_io import iter_repo_files, read_text_file


@dataclass
class ResolvedTarget:
    path: Path
    content: str
    source: str  # file | symbol | related
    kind: str = "file"  # file | symbol | directory | repo


@dataclass
class LineEvidence:
    path: Path
    line: int
    text: str


PATH_CLASS_WEIGHTS = {
    "preferred": 3,
    "normal": 0,
    "low_priority": -1,
    "index_exclude": -3,
    "hard_ignore": -5,
}


def load_index_payload(repo_root: Path, session: ExecutionSession) -> dict[str, object] | None:
    index_path = repo_root / ".forge" / "index.json"
    if not index_path.exists():
        return None

    session.record_effect(EffectClass.READ_ONLY, f"read index {index_path}")
    try:
        return json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def load_index_entry_map(repo_root: Path, session: ExecutionSession) -> dict[str, dict[str, object]]:
    payload = load_index_payload(repo_root, session)
    if payload is None:
        return {}

    files = payload.get("entries", {}).get("files", [])
    if not isinstance(files, list):
        return {}

    mapping: dict[str, dict[str, object]] = {}
    for entry in files:
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        if isinstance(path, str):
            mapping[path] = entry
    return mapping


def load_index_path_class_map(repo_root: Path, session: ExecutionSession) -> dict[str, str]:
    entries = load_index_entry_map(repo_root, session)
    mapping: dict[str, str] = {}
    for path, entry in entries.items():
        path_class = entry.get("path_class", "normal")
        if isinstance(path_class, str):
            mapping[path] = path_class
    return mapping


def path_class_weight(path_class: str) -> int:
    return PATH_CLASS_WEIGHTS.get(path_class, 0)


def index_allows_path(path_class: str) -> bool:
    return path_class not in {"index_exclude", "hard_ignore"}


def path_class_for(path: Path, repo_root: Path, path_classes: dict[str, str]) -> str:
    rel = str(path.relative_to(repo_root))
    return path_classes.get(rel, "normal")


def resolve_repo_path(repo_root: Path, raw_target: str) -> Path | None:
    token = raw_target.strip()
    if not token:
        return None

    candidate = Path(token)
    abs_path = candidate.resolve() if candidate.is_absolute() else (repo_root / candidate).resolve()
    try:
        abs_path.relative_to(repo_root)
    except ValueError:
        return None
    return abs_path


def resolve_file_or_symbol_target(repo_root: Path, raw_target: str, session: ExecutionSession) -> ResolvedTarget | None:
    abs_path = resolve_repo_path(repo_root, raw_target)
    if abs_path is not None and abs_path.is_file():
        content = read_text_file(abs_path, session)
        if content is not None:
            return ResolvedTarget(path=abs_path, content=content, source="file", kind="file")

    symbol = raw_target.strip()
    if not symbol:
        return None

    definition_patterns = [f"def {symbol}(", f"class {symbol}(", f"class {symbol}:"]
    best_path: Path | None = None
    best_content: str | None = None
    best_score = 0

    for path in iter_repo_files(repo_root, session):
        content = read_text_file(path, session)
        if not content:
            continue

        definition_hits = sum(content.count(pattern) for pattern in definition_patterns)
        mention_hits = content.count(symbol)
        score = (definition_hits * 100) + mention_hits
        if score > best_score:
            best_score = score
            best_path = path
            best_content = content

    if best_path is None or best_content is None:
        return None
    return ResolvedTarget(path=best_path, content=best_content, source="symbol", kind="symbol")


def resolve_describe_target(repo_root: Path, raw_target: str, session: ExecutionSession) -> ResolvedTarget:
    if not raw_target.strip():
        return ResolvedTarget(path=repo_root, content="", source="implicit", kind="repo")

    abs_path = resolve_repo_path(repo_root, raw_target)
    if abs_path is not None and abs_path.is_dir():
        return ResolvedTarget(path=abs_path, content="", source="path", kind="directory")
    if abs_path is not None and abs_path.is_file():
        content = read_text_file(abs_path, session) or ""
        return ResolvedTarget(path=abs_path, content=content, source="path", kind="file")

    symbol_target = resolve_file_or_symbol_target(repo_root, raw_target, session)
    if symbol_target is not None:
        symbol_target.kind = "symbol"
        return symbol_target

    return ResolvedTarget(path=repo_root, content="", source="fallback", kind="repo")


def find_related_files(repo_root: Path, target_rel: Path, session: ExecutionSession, limit: int = 5) -> list[Path]:
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
        if len(related) >= limit:
            break
    return related


def prioritize_paths_by_index(
    repo_root: Path,
    paths: list[Path],
    path_classes: dict[str, str],
    *,
    exclude_non_index_participating: bool,
) -> list[Path]:
    if not path_classes:
        return paths

    weighted: list[tuple[int, Path]] = []
    for path in paths:
        path_class = path_class_for(path, repo_root, path_classes)
        if exclude_non_index_participating and not index_allows_path(path_class):
            continue
        weighted.append((path_class_weight(path_class), path))

    weighted.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in weighted]


def collect_line_evidence(path: Path, content: str, pattern: re.Pattern[str], limit: int = 4) -> list[LineEvidence]:
    evidence: list[LineEvidence] = []
    for idx, line in enumerate(content.splitlines(), start=1):
        if pattern.search(line):
            evidence.append(LineEvidence(path=path, line=idx, text=line.strip()))
        if len(evidence) >= limit:
            break
    return evidence


def list_directory_files(directory: Path, repo_root: Path, session: ExecutionSession) -> list[Path]:
    session.record_effect(EffectClass.READ_ONLY, f"scan directory {directory}")
    results: list[Path] = []
    for path in directory.rglob("*"):
        if not path.is_file():
            continue
        try:
            path.relative_to(repo_root)
        except ValueError:
            continue
        results.append(path)
    return results
