from __future__ import annotations

import re
import shlex
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from core.capability_model import CommandRequest, Profile
from core.effects import ExecutionSession
from core.repo_io import iter_repo_files, read_text_file


@dataclass
class TestTarget:
    path: Path
    content: str
    source: str  # file | symbol


@dataclass
class TestConventions:
    framework: str
    naming_style: str
    assertion_style: str
    likely_test_dir: str


def parse_payload(payload: str) -> tuple[str, list[str]]:
    tokens = shlex.split(payload)
    target_tokens: list[str] = []
    explicit_cases: list[str] = []

    idx = 0
    while idx < len(tokens):
        token = tokens[idx]
        if token in {"--case", "-c"}:
            idx += 1
            case_parts: list[str] = []
            while idx < len(tokens) and tokens[idx] not in {"--case", "-c"} and not tokens[idx].startswith("--case="):
                case_parts.append(tokens[idx])
                idx += 1
            if case_parts:
                explicit_cases.append(" ".join(case_parts))
            continue
        if token.startswith("--case="):
            explicit_cases.append(token.split("=", 1)[1])
            idx += 1
            continue
        target_tokens.append(token)
        idx += 1

    raw_target = " ".join(target_tokens).strip() if target_tokens else payload.strip()
    inline = re.findall(r"(?:case:|edge case:)\s*([^\n,;]+)", payload, re.IGNORECASE)
    explicit_cases.extend([item.strip() for item in inline if item.strip()])
    # Dedupe preserving order.
    deduped: list[str] = []
    seen: set[str] = set()
    for case in explicit_cases:
        if case in seen:
            continue
        seen.add(case)
        deduped.append(case)
    return raw_target, deduped


def resolve_target(repo_root: Path, raw_target: str, session: ExecutionSession) -> TestTarget | None:
    candidate = Path(raw_target)
    abs_path = candidate.resolve() if candidate.is_absolute() else (repo_root / candidate).resolve()

    try:
        abs_path.relative_to(repo_root)
    except ValueError:
        abs_path = Path()

    if abs_path and abs_path.is_file():
        content = read_text_file(abs_path, session)
        if content is not None:
            return TestTarget(path=abs_path, content=content, source="file")

    symbol = raw_target.strip()
    if not symbol:
        return None
    def_patterns = [f"def {symbol}(", f"class {symbol}(", f"class {symbol}:"]
    best_path: Path | None = None
    best_content: str | None = None
    best_score = 0
    for path in iter_repo_files(repo_root, session):
        content = read_text_file(path, session)
        if not content:
            continue
        score = sum(content.count(pat) for pat in def_patterns) * 100 + content.count(symbol)
        if score > best_score:
            best_score = score
            best_path = path
            best_content = content
    if best_path is None or best_content is None:
        return None
    return TestTarget(path=best_path, content=best_content, source="symbol")


def find_test_files(repo_root: Path, session: ExecutionSession) -> list[Path]:
    tests: list[Path] = []
    for path in iter_repo_files(repo_root, session):
        rel = path.relative_to(repo_root)
        name = rel.name.lower()
        in_test_dir = rel.parts and rel.parts[0].lower() in {"test", "tests"}
        named_as_test = name.startswith("test_") or name.endswith("_test.py")
        if in_test_dir or named_as_test:
            tests.append(path)
    return tests


def detect_conventions(repo_root: Path, session: ExecutionSession) -> TestConventions:
    test_files = find_test_files(repo_root, session)
    if not test_files:
        return TestConventions(
            framework="pytest",
            naming_style="test_<unit>.py",
            assertion_style="assert",
            likely_test_dir="tests/",
        )

    framework_counter: Counter[str] = Counter()
    naming_counter: Counter[str] = Counter()
    assertion_counter: Counter[str] = Counter()
    directory_counter: Counter[str] = Counter()

    for path in test_files[:80]:
        rel = path.relative_to(repo_root)
        name = rel.name
        content = read_text_file(path, session) or ""
        directory_counter[str(rel.parent)] += 1

        if name.startswith("test_"):
            naming_counter["test_<unit>.py"] += 1
        if name.endswith("_test.py"):
            naming_counter["<unit>_test.py"] += 1

        if re.search(r"^\s*import\s+pytest|^\s*from\s+pytest\s+import", content, re.MULTILINE):
            framework_counter["pytest"] += 1
        if re.search(r"^\s*import\s+unittest|^\s*from\s+unittest\s+import", content, re.MULTILINE):
            framework_counter["unittest"] += 1

        if "self.assert" in content:
            assertion_counter["self.assert*"] += 1
        if re.search(r"^\s*assert\s+", content, re.MULTILINE):
            assertion_counter["assert"] += 1

    framework = framework_counter.most_common(1)[0][0] if framework_counter else "pytest"
    naming_style = naming_counter.most_common(1)[0][0] if naming_counter else "test_<unit>.py"
    assertion_style = assertion_counter.most_common(1)[0][0] if assertion_counter else "assert"
    likely_test_dir = directory_counter.most_common(1)[0][0] if directory_counter else "tests"
    if likely_test_dir == ".":
        likely_test_dir = "tests"

    return TestConventions(
        framework=framework,
        naming_style=naming_style,
        assertion_style=assertion_style,
        likely_test_dir=f"{likely_test_dir}/" if not likely_test_dir.endswith("/") else likely_test_dir,
    )


def likely_test_path(repo_root: Path, target: TestTarget, conventions: TestConventions) -> str:
    rel = target.path.relative_to(repo_root)
    base = rel.stem
    test_dir = conventions.likely_test_dir.strip("/")
    if not test_dir:
        test_dir = "tests"
    if conventions.naming_style == "<unit>_test.py":
        file_name = f"{base}_test.py"
    else:
        file_name = f"test_{base}.py"
    return f"{test_dir}/{file_name}"


def extract_units(content: str, max_items: int) -> list[str]:
    units = re.findall(r"^\s*(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", content, re.MULTILINE)
    deduped: list[str] = []
    seen: set[str] = set()
    for unit in units:
        if unit in seen:
            continue
        seen.add(unit)
        deduped.append(unit)
    return deduped[:max_items]


def derive_cases(target: TestTarget, explicit_cases: list[str], profile: Profile) -> list[str]:
    cases: list[str] = []
    for item in explicit_cases:
        cases.append(f"requested: {item}")

    units = extract_units(target.content, max_items=6 if profile != Profile.SIMPLE else 3)
    if not units:
        units = [target.path.stem]

    for unit in units:
        cases.append(f"{unit}: happy path returns expected result")
        cases.append(f"{unit}: invalid input handling")

    if re.search(r"\braise\b|\bValueError\b|\bException\b", target.content):
        cases.append("error path: expected exception is raised with invalid state/input")
    if re.search(r"[<>]=?|==|!=|\bmin\b|\bmax\b|\bboundary\b", target.content):
        cases.append("boundary values: lower/upper threshold behavior")
    if re.search(r"\bNone\b|\bnull\b|\boptional\b", target.content, re.IGNORECASE):
        cases.append("null/None behavior for optional values")

    # Dedupe preserving order.
    deduped: list[str] = []
    seen: set[str] = set()
    for case in cases:
        key = case.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(case)

    if profile == Profile.SIMPLE:
        return deduped[:6]
    if profile == Profile.STANDARD:
        return deduped[:10]
    return deduped[:14]


def build_draft_skeleton(target: TestTarget, conventions: TestConventions, cases: list[str], profile: Profile) -> str:
    rel_name = target.path.stem
    test_names: list[str] = []
    for case in cases[: (3 if profile == Profile.STANDARD else 5)]:
        slug = re.sub(r"[^a-z0-9]+", "_", case.lower()).strip("_")
        test_names.append(f"test_{slug[:50]}")

    if conventions.framework == "unittest":
        pass_method = "    pass\n"
        methods = "\n".join(
            [
                f"    def {name}(self):\n"
                "        # Arrange\n"
                "        # Act\n"
                "        # Assert\n"
                "        self.fail('Implement test')\n"
                for name in test_names
            ]
        )
        return (
            "import unittest\n\n"
            f"class Test{rel_name.title().replace('_', '')}(unittest.TestCase):\n"
            f"{methods or pass_method}"
        )

    placeholder = "def test_placeholder():\n    assert False\n"
    body = "\n".join(
        [
            f"def {name}():\n"
            "    # Arrange\n"
            "    # Act\n"
            "    # Assert\n"
            "    assert False  # replace with real assertion\n"
            for name in test_names
        ]
    )
    return f"# Draft tests for {target.path.name}\n\n{body or placeholder}"


def run(request: CommandRequest, args, session: ExecutionSession) -> int:
    repo_root = Path(args.repo_root).resolve()
    raw_target, explicit_cases = parse_payload(request.payload)
    target = resolve_target(repo_root, raw_target, session)

    print("=== FORGE TEST ===")
    print(f"Profile: {request.profile.value}")
    print(f"Target: {request.payload}")
    if explicit_cases:
        print(f"Explicit requested cases: {', '.join(explicit_cases)}")

    if target is None:
        print("\n--- Summary ---")
        print("Target could not be resolved to a readable file or symbol.")
        print("\n--- Next Step ---")
        print('Run: forge query "where is the relevant logic implemented?"')
        return 0

    conventions = detect_conventions(repo_root, session)
    test_location = likely_test_path(repo_root, target, conventions)
    cases = derive_cases(target, explicit_cases, request.profile)

    print("\n--- Summary ---")
    resolved = target.path.relative_to(repo_root)
    print(f"Drafted test plan for {resolved} ({target.source}).")

    print("\n--- Likely Test Location ---")
    print(test_location)

    print("\n--- Existing Test Conventions ---")
    print(f"Framework: {conventions.framework}")
    print(f"Naming: {conventions.naming_style}")
    print(f"Assertions: {conventions.assertion_style}")
    print(f"Primary test dir: {conventions.likely_test_dir}")

    print("\n--- Proposed Test Cases ---")
    for idx, case in enumerate(cases, start=1):
        print(f"{idx}. {case}")

    if request.profile in {Profile.STANDARD, Profile.DETAILED}:
        skeleton = build_draft_skeleton(target, conventions, cases, request.profile)
        print("\n--- Draft Test Skeleton ---")
        print("```python")
        print(skeleton)
        print("```")

    print("\n--- Next Step ---")
    print(f"Run: forge explain {resolved}")
    return 0
