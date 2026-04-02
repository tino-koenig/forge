from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from core.capability_model import CommandRequest, EffectClass, Profile
from core.effects import ExecutionSession
from core.repo_io import iter_repo_files, read_text_file


@dataclass
class DescribeTarget:
    kind: str  # repo | directory | file | symbol
    path: Path | None
    source: str


LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "React JSX",
    ".tsx": "React TSX",
    ".php": "PHP",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".rb": "Ruby",
    ".md": "Markdown",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".toml": "TOML",
    ".json": "JSON",
}


def load_index(repo_root: Path, session: ExecutionSession) -> dict[str, object] | None:
    index_path = repo_root / ".forge" / "index.json"
    if not index_path.exists():
        return None
    session.record_effect(EffectClass.READ_ONLY, f"read index {index_path}")
    try:
        raw = index_path.read_text(encoding="utf-8")
        return json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def resolve_target(repo_root: Path, raw_target: str, session: ExecutionSession) -> DescribeTarget:
    if not raw_target.strip():
        return DescribeTarget(kind="repo", path=repo_root, source="implicit")

    candidate = Path(raw_target.strip())
    abs_path = candidate.resolve() if candidate.is_absolute() else (repo_root / candidate).resolve()

    try:
        abs_path.relative_to(repo_root)
    except ValueError:
        abs_path = Path()

    if abs_path and abs_path.is_dir():
        return DescribeTarget(kind="directory", path=abs_path, source="path")
    if abs_path and abs_path.is_file():
        return DescribeTarget(kind="file", path=abs_path, source="path")

    # Symbol fallback
    symbol = raw_target.strip()
    definition_patterns = [f"def {symbol}(", f"class {symbol}(", f"class {symbol}:"]
    best_path: Path | None = None
    best_score = 0
    for path in iter_repo_files(repo_root, session):
        content = read_text_file(path, session)
        if not content:
            continue
        definition_hits = sum(content.count(pat) for pat in definition_patterns)
        mentions = content.count(symbol)
        score = definition_hits * 100 + mentions
        if score > best_score:
            best_score = score
            best_path = path
    if best_path is not None:
        return DescribeTarget(kind="symbol", path=best_path, source="symbol")

    return DescribeTarget(kind="repo", path=repo_root, source="fallback")


def collect_file_paths(repo_root: Path, session: ExecutionSession) -> list[Path]:
    return iter_repo_files(repo_root, session)


def list_directory_files(directory: Path, repo_root: Path, session: ExecutionSession) -> list[Path]:
    session.record_effect(EffectClass.READ_ONLY, f"scan directory {directory}")
    paths: list[Path] = []
    for path in directory.rglob("*"):
        if not path.is_file():
            continue
        try:
            path.relative_to(repo_root)
        except ValueError:
            continue
        paths.append(path)
    return paths


def detect_languages(files: list[Path]) -> list[str]:
    counter: Counter[str] = Counter()
    for path in files:
        lang = LANGUAGE_BY_EXTENSION.get(path.suffix.lower())
        if lang:
            counter[lang] += 1
    return [lang for lang, _count in counter.most_common(6)]


def detect_framework_hints(files: list[Path], repo_root: Path, session: ExecutionSession, limit: int) -> list[str]:
    hints: list[str] = []
    patterns = [
        ("argparse", re.compile(r"^\s*(?:from|import)\s+argparse\b", re.MULTILINE)),
        ("pytest", re.compile(r"^\s*(?:from|import)\s+pytest\b", re.MULTILINE)),
        ("flask", re.compile(r"^\s*(?:from|import)\s+flask\b", re.MULTILINE)),
        ("fastapi", re.compile(r"^\s*(?:from|import)\s+fastapi\b", re.MULTILINE)),
        ("django", re.compile(r"^\s*(?:from|import)\s+django\b", re.MULTILINE)),
        ("react", re.compile(r"\bfrom\s+['\"]react['\"]|^\s*import\s+react\b", re.IGNORECASE | re.MULTILINE)),
        ("sqlalchemy", re.compile(r"^\s*(?:from|import)\s+sqlalchemy\b", re.MULTILINE)),
    ]
    found: set[str] = set()
    code_ext = {".py", ".js", ".jsx", ".ts", ".tsx", ".php"}
    scoped_files = [path for path in files if path.suffix.lower() in code_ext][:limit]
    for path in scoped_files:
        content = read_text_file(path, session)
        if not content:
            continue
        for label, pattern in patterns:
            if label in found:
                continue
            if pattern.search(content):
                found.add(label)
                hints.append(label)
    return hints


def top_directories(files: list[Path], repo_root: Path, depth: int = 1) -> list[tuple[str, int]]:
    counter: Counter[str] = Counter()
    for path in files:
        rel = path.relative_to(repo_root)
        parts = rel.parts
        if not parts:
            continue
        key = "." if len(parts) == 1 else "/".join(parts[:depth])
        counter[key] += 1
    return counter.most_common(8)


def find_important_files(files: list[Path], repo_root: Path) -> list[Path]:
    important_names = {
        "readme.md",
        "license",
        "pyproject.toml",
        "package.json",
        "forge.py",
        "main.py",
        "setup.py",
    }
    important: list[Path] = []
    for path in files:
        rel = path.relative_to(repo_root)
        name = rel.name.lower()
        if name in important_names:
            important.append(rel)
        elif len(rel.parts) <= 2 and ("cli" in name or "main" in name):
            important.append(rel)
    # dedupe preserving order
    seen: set[Path] = set()
    result: list[Path] = []
    for path in important:
        if path in seen:
            continue
        seen.add(path)
        result.append(path)
    return result[:10]


def infer_repo_summary(
    repo_root: Path,
    files: list[Path],
    languages: list[str],
    session: ExecutionSession,
) -> str:
    readme = repo_root / "README.md"
    if readme.exists():
        text = read_text_file(readme, session)
        if text:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            for line in lines:
                if line.startswith("# "):
                    continue
                if len(line) > 30:
                    return line
    if not files:
        return "Repository currently has no readable source files."
    lang_part = ", ".join(languages) if languages else "mixed languages"
    return f"Repository appears to be a {lang_part} project with {len(files)} readable files."


def infer_target_summary(target: DescribeTarget, repo_root: Path, session: ExecutionSession) -> str:
    if target.path is None:
        return "Target could not be resolved."
    rel = target.path.relative_to(repo_root)
    if target.kind == "directory":
        return f"{rel} is a directory-level subsystem with grouped repository content."
    if target.kind == "symbol":
        return f"{target.kind} target resolves to {rel}, likely containing the requested logic."
    content = read_text_file(target.path, session)
    if not content:
        return f"{rel} is a file target."
    line_count = len(content.splitlines())
    if "argparse" in content:
        return f"{rel} appears to define CLI behavior and argument handling."
    if "class " in content or "def " in content:
        return f"{rel} is implementation-oriented source code ({line_count} lines)."
    return f"{rel} is a project file ({line_count} lines)."


def print_repo_description(
    repo_root: Path,
    files: list[Path],
    request: CommandRequest,
    session: ExecutionSession,
) -> str | None:
    languages = detect_languages(files)
    frameworks = detect_framework_hints(files, repo_root, session, limit=80 if request.profile != Profile.SIMPLE else 25)
    directories = top_directories(files, repo_root)
    important = find_important_files(files, repo_root)
    summary = infer_repo_summary(repo_root, files, languages, session)

    print("\n--- Summary ---")
    print(summary)

    print("\n--- Key Components ---")
    if directories:
        for directory, count in directories[:6]:
            print(f"- {directory}: {count} files")
    else:
        print("- No major directories detected")

    print("\n--- Technologies ---")
    print(f"Languages: {', '.join(languages) if languages else 'unknown'}")
    print(f"Framework hints: {', '.join(frameworks) if frameworks else 'none detected'}")

    print("\n--- Important Files ---")
    if important:
        for path in important:
            print(f"- {path}")
    else:
        print("- No obvious entry files detected")

    if request.profile in {Profile.STANDARD, Profile.DETAILED}:
        print("\n--- Architecture Notes ---")
        if any(path.relative_to(repo_root).parts and path.relative_to(repo_root).parts[0] == "cmd" for path in files):
            print("- CLI-oriented structure detected (`cmd/` present).")
        if any(path.relative_to(repo_root).parts and path.relative_to(repo_root).parts[0] == "modes" for path in files):
            print("- Capability-style mode separation detected (`modes/` present).")
        if any(path.relative_to(repo_root).parts and path.relative_to(repo_root).parts[0] == "core" for path in files):
            print("- Shared core logic appears centralized in `core/`.")

    if request.profile == Profile.DETAILED:
        print("\n--- README Draft Snippet ---")
        print(
            "This repository provides a structured toolchain focused on explicit capabilities, "
            "with readable command flows and audit-friendly outputs."
        )

    return str(important[0]) if important else None


def print_target_description(
    target: DescribeTarget,
    repo_root: Path,
    request: CommandRequest,
    session: ExecutionSession,
) -> None:
    if target.path is None:
        print("\n--- Summary ---")
        print("Target could not be resolved.")
        return

    rel = target.path.relative_to(repo_root)
    print("\n--- Summary ---")
    print(infer_target_summary(target, repo_root, session))

    files: list[Path]
    if target.kind == "directory":
        files = list_directory_files(target.path, repo_root, session)
    else:
        files = [target.path]

    languages = detect_languages(files)
    print("\n--- Key Components ---")
    if target.kind == "directory":
        subdirs = Counter(p.relative_to(target.path).parts[0] for p in files if len(p.relative_to(target.path).parts) > 1)
        if subdirs:
            for name, count in subdirs.most_common(6):
                print(f"- {name}: {count} files")
        else:
            print("- Target directory has mostly flat file structure.")
    else:
        content = read_text_file(target.path, session) or ""
        defs = re.findall(r"^\s*(?:def|class)\s+([A-Za-z0-9_]+)", content, flags=re.MULTILINE)
        if defs:
            for name in defs[:8]:
                print(f"- symbol: {name}")
        else:
            print("- No top-level definitions detected.")

    print("\n--- Technologies ---")
    print(f"Languages: {', '.join(languages) if languages else 'unknown'}")

    if request.profile in {Profile.STANDARD, Profile.DETAILED}:
        print("\n--- Important Files ---")
        if target.kind == "directory":
            important = find_important_files(files, repo_root)
            if important:
                for item in important[:8]:
                    print(f"- {item}")
            else:
                print("- No conventional entry/config files found in target.")
        else:
            print(f"- {rel}")

    if request.profile == Profile.DETAILED:
        print("\n--- Architecture Notes ---")
        if target.kind == "symbol":
            print("- Target was resolved via symbol matching; verify semantic intent with `forge explain`.")
        elif target.kind == "directory":
            print("- Directory-level description is based on file distribution and naming patterns.")
        else:
            print("- File-level description is based on structural tokens and naming conventions.")


def run(request: CommandRequest, args, session: ExecutionSession) -> int:
    repo_root = Path(args.repo_root).resolve()
    target = resolve_target(repo_root, request.payload, session)

    print("=== FORGE DESCRIBE ===")
    print(f"Profile: {request.profile.value}")
    if request.payload:
        print(f"Target: {request.payload}")

    index = None
    if request.profile in {Profile.STANDARD, Profile.DETAILED}:
        index = load_index(repo_root, session)
    if index is not None:
        print("Index: loaded .forge/index.json")
    elif request.profile in {Profile.STANDARD, Profile.DETAILED}:
        print("Index: not available, scanning repository directly")

    next_step: str | None = None
    if target.kind == "repo":
        files = collect_file_paths(repo_root, session)
        next_step = print_repo_description(repo_root, files, request, session)
    else:
        print_target_description(target, repo_root, request, session)

    print("\n--- Next Step ---")
    if target.kind == "repo":
        if next_step:
            print(f"Run: forge explain {next_step}")
        else:
            print('Run: forge query "where is the main entrypoint"')
    elif target.path is not None:
        rel = target.path.relative_to(repo_root)
        print(f"Run: forge explain {rel}")
    return 0
