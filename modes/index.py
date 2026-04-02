from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path

from core.capability_model import CommandRequest, EffectClass
from core.effects import ExecutionSession
from core.repo_io import write_forge_file


HARD_IGNORE = {
    ".git",
    ".forge",
    "__pycache__",
    ".idea",
    ".venv",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
    "htmlcov",
}

INDEX_EXCLUDE = {"vendor"}
LOW_PRIORITY = {"docs", "scripts", "examples"}
PREFERRED = {"src", "tests", "configuration"}


def classify_relative_path(relative: Path) -> tuple[str, str]:
    """Return (path_class, index_participation_state)."""
    lowered_parts = [part.lower() for part in relative.parts]
    if any(part in HARD_IGNORE for part in lowered_parts):
        return "hard_ignore", "excluded"
    if any(part in INDEX_EXCLUDE for part in lowered_parts):
        return "index_exclude", "excluded"
    if any(part in LOW_PRIORITY for part in lowered_parts):
        return "low_priority", "included"
    if any(part in PREFERRED for part in lowered_parts):
        return "preferred", "included"
    return "normal", "included"


def extract_python_symbols(path: Path) -> list[str]:
    symbols: list[str] = []
    if path.suffix.lower() != ".py":
        return symbols
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if line.startswith("def ") or line.startswith("class "):
                name = stripped.split("(", 1)[0].split(":", 1)[0]
                symbols.append(name.replace("def ", "").replace("class ", "").strip())
    except (OSError, UnicodeDecodeError):
        return []
    return symbols[:50]


def optional_file_hash(path: Path) -> str | None:
    try:
        size = path.stat().st_size
        if size > 1_000_000:
            return None
        digest = hashlib.sha1(path.read_bytes()).hexdigest()
        return digest
    except OSError:
        return None


def extension_guess(path: Path) -> str:
    return path.suffix.lower().lstrip(".") if path.suffix else "none"


def build_file_entry(root: Path, path: Path) -> dict[str, object]:
    rel_path = path.relative_to(root)
    path_class, state = classify_relative_path(rel_path)
    stat = path.stat()
    return {
        "path": str(rel_path),
        "kind": "file",
        "extension": extension_guess(path),
        "size": stat.st_size,
        "mtime": int(stat.st_mtime),
        "hash": optional_file_hash(path),
        "top_level_symbols": extract_python_symbols(path),
        "path_class": path_class,
        "index_participation_state": state,
    }


def build_directory_entry(root: Path, path: Path) -> dict[str, object]:
    rel_path = path.relative_to(root) if path != root else Path(".")
    path_class, state = classify_relative_path(rel_path)
    depth = 0 if rel_path == Path(".") else len(rel_path.parts)
    child_files = 0
    child_dirs = 0
    ext_counter: Counter[str] = Counter()
    try:
        for child in path.iterdir():
            rel_child = child.relative_to(root)
            child_class, _state = classify_relative_path(rel_child)
            if child_class in {"hard_ignore", "index_exclude"}:
                continue
            if child.is_dir():
                child_dirs += 1
            elif child.is_file():
                child_files += 1
                ext_counter[extension_guess(child)] += 1
    except OSError:
        pass

    dominant = [ext for ext, _count in ext_counter.most_common(5)]
    return {
        "path": str(rel_path),
        "kind": "directory",
        "depth": depth,
        "child_file_count": child_files,
        "child_directory_count": child_dirs,
        "dominant_extensions": dominant,
        "path_class": path_class,
        "index_participation_state": state,
    }


def should_index(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    path_class, _state = classify_relative_path(rel)
    return path_class not in {"hard_ignore", "index_exclude"}


def build_index(repo_root: Path, request: CommandRequest, session: ExecutionSession) -> dict[str, object]:
    session.record_effect(EffectClass.READ_ONLY, "scan repository for index")
    files: list[dict[str, object]] = []
    directories: list[dict[str, object]] = [build_directory_entry(repo_root, repo_root)]
    for current_root, dir_names, file_names in os.walk(repo_root, topdown=True):
        current_path = Path(current_root)
        rel_current = current_path.relative_to(repo_root) if current_path != repo_root else Path(".")

        # Prune traversals for hard-ignore and index_exclude directories.
        kept_dirs: list[str] = []
        for dir_name in dir_names:
            rel_dir = rel_current / dir_name if rel_current != Path(".") else Path(dir_name)
            path_class, _state = classify_relative_path(rel_dir)
            if path_class in {"hard_ignore", "index_exclude"}:
                continue
            kept_dirs.append(dir_name)
        dir_names[:] = kept_dirs

        if current_path != repo_root and should_index(current_path, repo_root):
            directories.append(build_directory_entry(repo_root, current_path))

        for file_name in file_names:
            file_path = current_path / file_name
            if should_index(file_path, repo_root):
                files.append(build_file_entry(repo_root, file_path))

    return {
        "version": 1,
        "capability": request.capability.value,
        "profile": request.profile.value,
        "root": str(repo_root),
        "entries": {
            "directories": directories,
            "files": files,
        },
        "counts": {
            "directories": len(directories),
            "files": len(files),
        },
    }


def run(request: CommandRequest, args, session: ExecutionSession) -> int:
    repo_root = Path(args.repo_root).resolve()
    print("=== FORGE INDEX ===")
    print(f"Profile: {request.profile.value}")
    if request.payload:
        print(f"Operation: {request.payload}")
    print(f"Root: {repo_root}")

    data = build_index(repo_root=repo_root, request=request, session=session)
    target = write_forge_file(
        root=repo_root,
        relative_path="index.json",
        content=json.dumps(data, indent=2, sort_keys=True),
        session=session,
    )
    print(f"Wrote index: {target}")
    print(
        "Indexed entries: "
        f"{data['counts']['directories']} directories, {data['counts']['files']} files"
    )
    return 0
