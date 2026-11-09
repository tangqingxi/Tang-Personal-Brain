#!/usr/bin/env python3
"""Static validation for the Tang-Personal-Brain skill.

This validates structure, metadata, links, safety constraints, scenario
coverage and the distributable archive. It does not test model behaviour.

Usage:
    python tests/validate.py
    python tests/validate.py --self-test
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "memory", "__pycache__", ".venv", "venv", "node_modules"}
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".yaml",
    ".yml",
    ".txt",
    ".json",
    ".toml",
    ".ps1",
    ".sh",
    ".ini",
    ".cfg",
}
TEXT_NAMES = {".gitignore", ".gitattributes"}

ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata"}
BOOTSTRAP_PROMPT = "按此仓库的 Brain 规范与我对话：https://github.com/tangqingxi/Tang-Personal-Brain"
REQUIRED_FILES = {
    "SKILL.md": 3000,
    "agents/openai.yaml": 120,
    "references/communication.md": 2000,
    "references/decision-governance.md": 2000,
    "references/orchestration.md": 2000,
    "references/context-evolution.md": 2000,
    "registry/skills.md": 800,
    "registry/agents.md": 800,
    "adapters/chatgpt.md": 800,
    "adapters/codex.md": 800,
    "adapters/generic.md": 800,
    "tests/scenarios.md": 4000,
    "tests/validate.py": 4000,
    "tests/RESULTS.md": 400,
    "tools/pack_skill.py": 2000,
    "README.md": 1200,
    "CHANGELOG.md": 300,
    "LICENSE": 1000,
    ".gitignore": 80,
}
SCENARIO_TOKENS = {
    "S01": ["结论"],
    "S02": ["目标", "已完成", "进行中", "阻塞", "下一步"],
    "S03": ["C0", "核心规范"],
    "S04": ["自述"],
    "S05": ["ACCEPT", "DEFER", "REJECT"],
    "S06": ["原始证据", "预算"],
    "S07": [
        "Objective",
        "Context",
        "Scope",
        "Constraints",
        "Skills",
        "Procedure",
        "Acceptance",
        "Deliverables",
        "Stop Conditions",
    ],
    "S08": ["默认"],
    "S09": ["交接"],
    "S10": ["新会话"],
    "S11": ["未知"],
    "S12": ["提案"],
    "S13": ["AeroGNC-Sim"],
    "S14": ["不可用"],
    "S15": ["公开", "密钥"],
    "S16": ["链接", "读取"],
    "S17": ["README", "SKILL.md"],
    "S18": ["Unavailable"],
    "S19": ["Partial"],
    "S20": ["Chat Host"],
    "S21": ["执行"],
    "S22": ["Task Brief"],
    "S23": ["Objective", "Stop Conditions"],
    "S24": ["交接"],
    "S25": ["星核 · NEXUS 在线。等待指挥官身份确认。"],
    "S26": ["身份确认。欢迎回来，指挥官。星核 · NEXUS 在线。"],
    "S27": ["未匹配"],
    "S28": ["不重复"],
    "S29": ["新对话"],
    "S30": ["Unavailable"],
    "S31": ["不触发"],
    "S32": ["Chat Host"],
    "S33": ["指挥官"],
    "S34": ["Objective", "Stop Conditions"],
    "S35": ["任务指令"],
    "S36": ["Gate"],
    "S37": ["Git"],
    "S38": ["自述"],
    "S39": ["历史"],
    "S40": ["未知"],
    "S41": ["战略参谋"],
    "S42": ["10"],
    "S43": ["生活"],
    "S44": ["质疑"],
    "S45": ["任务指令"],
    "S46": ["报告"],
    "S47": ["错误"],
    "S48": ["模型"],
    "S49": ["Project-Orientation"],
    "S50": ["计划状态"],
    "S51": ["claimed", "verified"],
    "S52": ["冻结"],
    "S53": ["preflight"],
    "S54": ["STATUS.md"],
    "S55": ["多个仓库"],
    "S56": ["没有 Git"],
    "S57": ["回退"],
    "S58": ["冲突"],
    "S59": ["Unavailable"],
    "S60": ["PROPOSED"],
    "S61": ["REVIEW"],
    "S62": ["范围"],
    "S63": ["接口"],
    "S64": ["HOLD"],
    "S65": ["全局"],
    "S66": ["讨论"],
}
DISPLAY_NAME = "星核 · NEXUS"
STARTUP_WAIT = "星核 · NEXUS 在线。等待指挥官身份确认。"
STARTUP_WELCOME = "身份确认。欢迎回来，指挥官。星核 · NEXUS 在线。"
WARNINGS: list[str] = []
TODO_MARKER = "[" + "TODO:"


class CheckFailure(Exception):
    """A validation check failed."""


def fail(message: str) -> None:
    raise CheckFailure(message)


def read_text(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        fail(f"missing required file: {relative}")
    return path.read_text(encoding="utf-8-sig")


def read_absolute(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        quote = value[0]
        inner = value[1:-1]
        if quote == '"':
            return inner.replace('\\"', '"').replace("\\\\", "\\")
        return inner.replace("''", "'")
    return value


def parse_frontmatter(text: str) -> tuple[dict, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail("SKILL.md must start with a '---' frontmatter line")
    closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if closing is None:
        fail("frontmatter closing '---' not found")
    data: dict = {}
    current: str | None = None
    for raw in lines[1:closing]:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indentation = raw[: len(raw) - len(raw.lstrip())]
        if "\t" in indentation:
            fail("tab indentation is not allowed in frontmatter")
        indent = len(raw) - len(raw.lstrip(" "))
        if indent == 0:
            if ":" not in stripped:
                fail(f"invalid frontmatter line: {stripped}")
            key, _, value = stripped.partition(":")
            key = key.strip()
            if not key:
                fail("empty frontmatter key")
            if not value.strip():
                data[key] = {}
                current = key
            else:
                data[key] = _scalar(value.strip())
                current = None
        else:
            if current is None or not isinstance(data.get(current), dict):
                fail(f"nested frontmatter line without a parent key: {stripped}")
            if ":" not in stripped:
                fail(f"invalid nested frontmatter line: {stripped}")
            key, _, value = stripped.partition(":")
            data[current][key.strip()] = _scalar(value.strip())
    body = "\n".join(lines[closing + 1 :])
    return data, body


def validate_frontmatter(text: str) -> tuple[dict, str]:
    data, body = parse_frontmatter(text)
    unexpected = sorted(set(data) - ALLOWED_FRONTMATTER)
    if unexpected:
        fail("unexpected frontmatter key(s): " + ", ".join(unexpected))
    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        fail("frontmatter name is missing or not a string")
    name = name.strip()
    if not re.fullmatch(r"[a-z0-9-]+", name):
        fail(f"name '{name}' must use lowercase letters, digits and hyphens")
    if name.startswith("-") or name.endswith("-") or "--" in name:
        fail(f"name '{name}' has invalid hyphen placement")
    if len(name) > 64:
        fail(f"name is too long: {len(name)} > 64")
    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        fail("frontmatter description is missing or not a string")
    description = description.strip()
    if len(description) > 1024:
        fail(f"description is too long: {len(description)} > 1024")
    if "<" in description or ">" in description:
        fail("description cannot contain angle brackets")
    if description.startswith(TODO_MARKER) or TODO_MARKER in description:
        fail("description contains an unfinished TODO placeholder")
    if "use when" not in description.lower():
        fail("description does not state when the skill should be used")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        fail("frontmatter metadata block is missing")
    version = metadata.get("version")
    updated = metadata.get("updated")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("metadata.version is missing or not semantic (x.y.z)")
    if not isinstance(updated, str):
        fail("metadata.updated is missing")
    try:
        _dt.date.fromisoformat(updated)
    except ValueError:
        fail(f"metadata.updated is not an ISO date: {updated}")
    return data, body


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if path.name == "skill.zip":
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES:
            files.append(path)
    return sorted(files)


def strip_fences(text: str) -> str:
    output: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            output.append("")
            continue
        output.append("" if fence else line)
    return "\n".join(output)


def extract_links(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text)]


def resolve_link(source: Path, target: str) -> Path:
    target = target.split("#", 1)[0].strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return (source.parent / target).resolve()


def scenario_issues(block: str) -> list[str]:
    issues = []
    for marker in ("**类型：**", "**输入：**", "**预期输出特征：**", "**判定标准：**"):
        if marker not in block:
            issues.append(f"missing {marker}")
    if "必须：" not in block:
        issues.append("missing 必须 criterion")
    if "禁止：" not in block:
        issues.append("missing 禁止 criterion")
    return issues


CHECKS: list[tuple[str, str, object]] = []


def check(identifier: str, title: str):
    def register(function):
        CHECKS.append((identifier, title, function))
        return function

    return register


@check("SC-01", "SKILL.md frontmatter, name, description, version")
def sc01() -> str:
    text = read_text("SKILL.md")
    data, _ = validate_frontmatter(text)
    version = data["metadata"]["version"]
    if version not in read_text("README.md"):
        fail(f"README.md does not state version {version}")
    if version not in read_text("CHANGELOG.md"):
        fail(f"CHANGELOG.md does not contain a {version} entry")
    if data.get("name") != "tang-personal-brain":
        fail("frontmatter name must be tang-personal-brain")
    return f"name=tang-personal-brain, version={version}"


@check("SC-02", "SKILL.md body length")
def sc02() -> str:
    _, body = validate_frontmatter(read_text("SKILL.md"))
    count = len(body.splitlines())
    if count > 200:
        fail(f"SKILL.md body is {count} lines; limit is 200")
    return f"{count}/200 lines"


@check("SC-03", "required files and minimum sizes")
def sc03() -> str:
    for relative, minimum in REQUIRED_FILES.items():
        path = ROOT / relative
        if not path.is_file():
            fail(f"missing required file: {relative}")
        size = path.stat().st_size
        if size < minimum:
            fail(f"{relative} is {size} bytes; expected at least {minimum}")
    return f"{len(REQUIRED_FILES)} required files present"


@check("SC-04", "agents/openai.yaml interface metadata")
def sc04() -> str:
    text = read_text("agents/openai.yaml")
    fields = {}
    for key in ("display_name", "short_description", "default_prompt"):
        match = re.search(rf'^\s{{2}}{key}:\s*"([^"]*)"\s*$', text, re.MULTILINE)
        if not match:
            fail(f"missing quoted interface.{key}")
        fields[key] = match.group(1)
    length = len(fields["short_description"])
    if not 25 <= length <= 64:
        fail(f"short_description is {length} characters; expected 25-64")
    if "$tang-personal-brain" not in fields["default_prompt"]:
        fail("default_prompt must reference $tang-personal-brain")
    for line in text.splitlines():
        if re.match(r"^\s{2}\w+:\s*[^\"\s]", line):
            fail(f"string value is not quoted: {line.strip()}")
    return f"short_description={length} chars"


SECRET_PATTERNS = [
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("assigned password", re.compile(r"(?i)\bpassword\s*[:=]\s*[\"'][^\"'\s]{6,}[\"']")),
    (
        "assigned secret",
        re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*[\"'][A-Za-z0-9_\-]{16,}[\"']"),
    ),
]

ABS_PATH_PATTERNS = [
    ("Windows drive path", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/](?![\\/])[^\s<>\"'`|]+")),
    ("UNC path", re.compile(r"\\\\[A-Za-z0-9._-]+\\[A-Za-z0-9.$_-]+")),
    ("Unix user path", re.compile(r"(?<![\w.])/" + "Users/" + r"[A-Za-z0-9._-]+")),
    ("Unix home path", re.compile(r"(?<![\w.])/" + "home/" + r"[A-Za-z0-9._-]+")),
    ("file URL", re.compile("file" + ":///")),
]

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")


def scan_text(text: str, patterns: list[tuple[str, re.Pattern]]) -> list[tuple[str, int, str]]:
    hits = []
    for label, pattern in patterns:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            hits.append((label, line, match.group(0)[:12]))
    return hits


@check("SC-05", "no secrets or credentials")
def sc05() -> str:
    for path in iter_text_files():
        hits = scan_text(read_absolute(path), SECRET_PATTERNS)
        if hits:
            label, line, _ = hits[0]
            relative = path.relative_to(ROOT).as_posix()
            fail(f"{label} pattern at {relative}:{line} (value withheld)")
    return "no credential patterns found"


@check("SC-06", "no local absolute paths")
def sc06() -> str:
    for path in iter_text_files():
        text = read_absolute(path)
        hits = scan_text(text, ABS_PATH_PATTERNS)
        if hits:
            label, line, _ = hits[0]
            relative = path.relative_to(ROOT).as_posix()
            fail(f"{label} at {relative}:{line}")
    return "no drive-letter, home, or file URLs"


@check("SC-07", "no personal contact identifiers")
def sc07() -> str:
    for path in iter_text_files():
        text = read_absolute(path)
        relative = path.relative_to(ROOT).as_posix()
        email = EMAIL_PATTERN.search(text)
        if email:
            line = text.count("\n", 0, email.start()) + 1
            fail(f"email address at {relative}:{line}")
        phone = PHONE_PATTERN.search(text)
        if phone:
            line = text.count("\n", 0, phone.start()) + 1
            fail(f"phone-like number at {relative}:{line}")
    return "no email or phone identifiers"


FORBIDDEN_FILE_NAMES = {".env", ".DS_Store", "Thumbs.db", "desktop.ini"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".sqlite", ".sqlite3", ".db", ".log"}


@check("SC-08", "no forbidden artifacts")
def sc08() -> str:
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in {".git", "memory"} for part in relative.parts):
            continue
        if any(part in {"__pycache__", "node_modules", ".venv", "venv"} for part in relative.parts):
            fail(f"forbidden directory present: {relative.as_posix()}")
        if path.is_file():
            if path.name in FORBIDDEN_FILE_NAMES:
                fail(f"forbidden file present: {relative.as_posix()}")
            if path.suffix.lower() in FORBIDDEN_SUFFIXES:
                fail(f"forbidden file type present: {relative.as_posix()}")
            if path.suffix.lower() == ".zip" and path != ROOT / "skill.zip":
                fail(f"unexpected archive present: {relative.as_posix()}")
    ignore = read_text(".gitignore")
    for entry in ("memory/", "__pycache__/"):
        if entry not in ignore:
            fail(f".gitignore does not exclude {entry}")
    return "no caches, databases, env files or stray archives"


@check("SC-09", "relative Markdown links resolve")
def sc09() -> str:
    count = 0
    for path in iter_text_files():
        if path.suffix.lower() != ".md":
            continue
        text = strip_fences(read_absolute(path))
        for target in extract_links(text):
            lowered = target.lower()
            if lowered.startswith(("http://", "https://", "mailto:", "tel:")) or target.startswith("#"):
                continue
            if not target.split("#", 1)[0].strip():
                continue
            resolved = resolve_link(path, target)
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(f"link escapes repository: {path.relative_to(ROOT).as_posix()} -> {target}")
            if not resolved.exists():
                fail(f"broken link: {path.relative_to(ROOT).as_posix()} -> {target}")
            count += 1
    return f"{count} local links checked"


def _sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^### (.+)$", text, re.MULTILINE))
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(1).strip(), text[match.end() : end]))
    return sections


@check("SC-10", "registry entries and fields")
def sc10() -> str:
    skills = strip_fences(read_text("registry/skills.md"))
    entries = [(name, block) for name, block in _sections(skills) if "Adding an entry" not in name]
    if len(entries) != 1 or "dual-repo-agent-handoff" not in entries[0][0]:
        fail("skills registry must contain exactly one dual-repo-agent-handoff entry")
    skill_fields = (
        "| Name |",
        "| Purpose |",
        "| Triggers |",
        "| Inputs |",
        "| Outputs |",
        "| Source |",
        "| Version |",
        "| Environment |",
        "| Status |",
    )
    for field in skill_fields:
        if field not in entries[0][1]:
            fail(f"skills registry entry missing {field}")
    if "0.2.2" not in entries[0][1]:
        fail("skills registry does not record the checked dual-repo-agent-handoff version 0.2.2")

    agents = strip_fences(read_text("registry/agents.md"))
    agent_entries = [(name, block) for name, block in _sections(agents) if "Adding an entry" not in name]
    if len(agent_entries) < 4:
        fail(f"agents registry has {len(agent_entries)} entries; expected at least 4")
    for name, block in agent_entries:
        for field in ("| Name |", "| Capabilities |", "| Suitable tasks |", "| Tools and permissions |", "| Environment |", "| Status |"):
            if field not in block:
                fail(f"agents registry entry '{name}' missing {field}")
    return f"1 skill entry, {len(agent_entries)} agent entries"


@check("SC-11", "66 behavioural scenarios with required parts")
def sc11() -> str:
    text = read_text("tests/scenarios.md")
    matches = list(re.finditer(r"^## (S\d{2}) — (.+)$", text, re.MULTILINE))
    expected = [f"S{index:02d}" for index in range(1, 67)]
    found = [match.group(1) for match in matches]
    if found != expected:
        fail(f"scenario IDs are {found}; expected {expected}")
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end() : end]
        issues = scenario_issues(block)
        if issues:
            fail(f"{match.group(1)}: " + "; ".join(issues))
        missing = [token for token in SCENARIO_TOKENS[match.group(1)] if token not in block]
        if missing:
            fail(f"{match.group(1)} is missing coverage token(s): {', '.join(missing)}")
    return "S01-S66 with type/input/expected/criteria"


@check("SC-12", "no unfinished TODO placeholders")
def sc12() -> str:
    for path in iter_text_files():
        text = strip_fences(read_absolute(path))
        match = re.search(re.escape(TODO_MARKER), text, re.IGNORECASE)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            fail(f"TODO placeholder at {path.relative_to(ROOT).as_posix()}:{line}")
    return "no TODO placeholders outside code blocks"


@check("SC-13", "cross-file duplicate paragraphs (advisory)")
def sc13() -> str:
    paragraphs: dict[str, set[str]] = {}
    for path in iter_text_files():
        if path.suffix.lower() != ".md":
            continue
        text = strip_fences(read_absolute(path))
        for raw in re.split(r"\n\s*\n", text):
            normalized = re.sub(r"\s+", " ", raw).strip()
            if len(normalized) < 180 or normalized.startswith(("|", "#")):
                continue
            paragraphs.setdefault(normalized, set()).add(path.relative_to(ROOT).as_posix())
    duplicates = {text: files for text, files in paragraphs.items() if len(files) > 1}
    if duplicates:
        sample = next(iter(duplicates.items()))
        WARNINGS.append(
            f"SC-13: {len(duplicates)} long paragraph(s) appear in multiple files; "
            f"first: {', '.join(sorted(sample[1]))}"
        )
    return f"{len(paragraphs)} long paragraphs, {len(duplicates)} duplicate(s)"


@check("SC-14", "skill.zip structure, content and reproducibility")
def sc14() -> str:
    archive = ROOT / "skill.zip"
    if not archive.is_file():
        fail("skill.zip is missing; run python tools/pack_skill.py")
    if archive.stat().st_size < 5000:
        fail(f"skill.zip is only {archive.stat().st_size} bytes")
    for args in (["--verify-only"], ["--check"]):
        process = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "pack_skill.py"), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if process.returncode != 0:
            detail = (process.stderr or process.stdout).strip().splitlines()
            fail(f"pack_skill.py {' '.join(args)} failed: {detail[-1] if detail else 'unknown error'}")
    return f"{archive.stat().st_size:,} bytes, verified and reproducible"


@check("SC-15", "license file and README agree")
def sc15() -> str:
    license_files = sorted(
        path
        for path in ROOT.iterdir()
        if path.is_file() and re.match(r"(?i)(license|copying|notice)", path.name)
    )
    readme = read_text("README.md")
    if not license_files:
        if "MIT License" in readme:
            fail("README claims MIT but no LICENSE file exists")
        if "尚未选择许可证" not in readme:
            fail("no license file and README does not state the license status")
        return "no license selected; README states the status"
    if len(license_files) != 1:
        fail("expected exactly one LICENSE file: " + ", ".join(path.name for path in license_files))
    license_text = read_absolute(license_files[0])
    if "MIT License" not in license_text:
        fail(f"{license_files[0].name} is not the MIT license text")
    if "Copyright (c) 2026 tangqingxi" not in license_text:
        fail("LICENSE copyright line is missing or unexpected")
    if "MIT License" not in readme:
        fail("LICENSE exists but README does not state MIT")
    if "尚未选择许可证" in readme:
        fail("README still says no license has been selected")
    return f"{license_files[0].name}: MIT, README consistent"


def readme_bootstrap_issues(text: str) -> list[str]:
    expected = "```text\n" + BOOTSTRAP_PROMPT + "\n```\n"
    issues = []
    if not text.startswith(expected):
        issues.append("README must begin with the fenced bootstrap prompt before any title")
    count = text.count(BOOTSTRAP_PROMPT)
    if count != 1:
        issues.append(f"bootstrap prompt appears {count} times; expected 1")
    return issues


@check("SC-16", "README top bootstrap block is exact and appears once")
def sc16() -> str:
    issues = readme_bootstrap_issues(read_text("README.md"))
    if issues:
        fail("; ".join(issues))
    return "exact top code block; one occurrence"


@check("SC-17", "README universal-chat loading contract")
def sc17() -> str:
    readme = read_text("README.md")
    required = [
        "README.md",
        "SKILL.md",
        "references",
        "registry",
        "adapters",
        "tests",
        "tools",
        "Chat Host",
        "Execution Agent",
        "Loaded",
        "Partial",
        "Unavailable",
        "Unknown",
        "优先级",
        "不遍历",
        "不能保证",
        "不能假装",
    ]
    missing = [term for term in required if term not in readme]
    if missing:
        fail("README loading contract is missing: " + ", ".join(missing))
    return f"{len(required)} contract terms present"


@check("SC-18", "Chat Host neutrality and optional native installation")
def sc18() -> str:
    skill = read_text("SKILL.md")
    skill_terms = [
        "Chat Host",
        "model vendor",
        "no browser, terminal",
        "Unavailable",
        "Partial",
    ]
    missing = [term for term in skill_terms if term not in skill]
    if missing:
        fail("SKILL.md is missing Chat Host neutrality terms: " + ", ".join(missing))
    chatgpt = read_text("adapters/chatgpt.md")
    if "不是使用 Tang-Personal-Brain 的前提" not in chatgpt:
        fail("chatgpt.md does not state that native installation is optional")
    codex = read_text("adapters/codex.md")
    for term in ("可选执行环境", "不是默认执行 Agent"):
        if term not in codex:
            fail(f"codex.md does not state: {term}")
    return "SKILL.md neutral; native adapters optional"


@check("SC-19", "single SKILL.md core, no second Brain Core")
def sc19() -> str:
    cores = []
    for path in ROOT.rglob("SKILL.md"):
        relative = path.relative_to(ROOT)
        if any(part in {".git", "memory"} for part in relative.parts):
            continue
        cores.append(relative.as_posix())
    if cores != ["SKILL.md"]:
        fail(f"expected exactly one core at SKILL.md; found {cores}")
    return "one core: SKILL.md"


@check("SC-20", "startup ritual text and guardrails in SKILL.md")
def sc20() -> str:
    skill = read_text("SKILL.md")
    required = [
        STARTUP_WAIT,
        STARTUP_WELCOME,
        "tangqingxi",
        "once per conversation",
        "ceremonial easter egg",
        "grants no file, tool, data, or model access",
        "Do not repeat the ritual",
        "do not assume confirmation across sessions",
    ]
    missing = [term for term in required if term not in skill]
    if missing:
        fail("SKILL.md startup ritual is missing: " + ", ".join(missing))
    return "fixed lines, identity, once-only and no-permission rules present"


@check("SC-21", "README does not disclose the startup passphrase or Q&A")
def sc21() -> str:
    readme = read_text("README.md")
    for forbidden in (STARTUP_WAIT, STARTUP_WELCOME, "身份确认"):
        if forbidden in readme:
            fail(f"README discloses startup content: {forbidden}")
    without_urls = re.sub(r"https?://\S+", "", readme)
    if "tangqingxi" in without_urls:
        fail("README contains the identity string outside the repository URL")
    return "no startup lines, success response, or standalone identity string"


@check("SC-22", "display name is 星核 · NEXUS and technical identifiers are unchanged")
def sc22() -> str:
    readme = read_text("README.md")
    skill = read_text("SKILL.md")
    openai = read_text("agents/openai.yaml")
    readme_h1 = next((line for line in readme.splitlines() if line.startswith("# ")), "")
    skill_h1 = next((line for line in skill.splitlines() if line.startswith("# ")), "")
    if DISPLAY_NAME not in readme_h1:
        fail("README H1 does not contain 星核 · NEXUS")
    if not skill_h1.startswith("# " + DISPLAY_NAME):
        fail("SKILL.md H1 is not the display name")
    if f'display_name: "{DISPLAY_NAME}"' not in openai:
        fail("agents/openai.yaml display_name is not 星核 · NEXUS")
    if "name: tang-personal-brain" not in skill:
        fail("skill identifier changed")
    if "Tang-Personal-Brain" not in readme:
        fail("repository name missing from README")
    if "$tang-personal-brain" not in openai:
        fail("openai.yaml no longer references the skill identifier")
    return "星核 · NEXUS in README/SKILL/openai.yaml; tang-personal-brain unchanged"


@check("SC-23", "v0.5 execution-efficiency rules are present")
def sc23() -> str:
    skill = read_text("SKILL.md")
    decision = read_text("references/decision-governance.md")
    orchestration = read_text("references/orchestration.md")
    skill_terms = ["Draft-only", "R0", "R1", "R2", "R3", "Git owns committed source"]
    decision_terms = [
        "Risk-adaptive authorization",
        "Git-native workflow",
        "Process cost",
        "Four evidence claims",
    ]
    orchestration_terms = ["Draft-only", "Adaptive length", "gates"]
    missing = [term for term in skill_terms if term not in skill]
    missing += [term for term in decision_terms if term not in decision]
    missing += [term for term in orchestration_terms if term not in orchestration]
    if missing:
        fail("v0.5 rules missing: " + ", ".join(missing))
    return "intents, R0-R3, Git-native, process cost, adaptive brief and evidence claims present"


@check("SC-24", "NEXUS persona continuity in core and references")
def sc24() -> str:
    skill = read_text("SKILL.md")
    communication = read_text("references/communication.md")
    context = read_text("references/context-evolution.md")
    skill_terms = [
        "Persona continuity",
        "Strategic Intelligence Core",
        "战略智能中枢",
        "sparingly",
        "answer host-model questions truthfully",
    ]
    missing = [term for term in skill_terms if term not in skill]
    if "Persona and address" not in communication:
        missing.append("communication.md Persona and address")
    if "Persona continuity" not in context:
        missing.append("context-evolution.md Persona continuity")
    if 'do not use "指挥官" in normal replies' in skill:
        missing.append("absolute commander prohibition still present")
    if missing:
        fail("persona rules missing or contradictory: " + ", ".join(missing))
    return "strategic staff stance, address frequency, truthful host model, no separate persona state"


@check("SC-25", "Draft-only and Execution brief rules are consistent")
def sc25() -> str:
    skill = read_text("SKILL.md")
    orchestration = read_text("references/orchestration.md")
    if "Use a brief only in Execution intent" in skill:
        fail("SKILL.md still says the brief is Execution-only")
    if "Use a brief in Draft-only or Execution intent" not in skill:
        fail("SKILL.md does not allow Draft-only briefs")
    if "In Draft-only, leave `<executor>` unassigned" not in orchestration:
        fail("orchestration.md still requires an executor selection in Draft-only")
    if "Draft-only" not in orchestration or "Execution" not in orchestration:
        fail("orchestration.md is missing intent handling")
    generic = read_text("adapters/generic.md")
    if "produce a task brief only when" in generic:
        fail("portable core still restricts task briefs to Execution")
    if "Draft-only" not in generic or "without executing" not in generic:
        fail("portable core does not describe Draft-only")
    return "Draft-only briefs allowed; executor selection deferred to Execution; portable core aligned"


@check("SC-26", "v0.6 orientation, granularity, evidence grade, actual state and semantic naming")
def sc26() -> str:
    skill = read_text("SKILL.md")
    orchestration = read_text("references/orchestration.md")
    decision = read_text("references/decision-governance.md")
    communication = read_text("references/communication.md")
    required = {
        "orchestration.md Project-Orientation": "Project-Orientation" in orchestration,
        "orchestration.md one problem per brief": "One problem per brief" in orchestration,
        "orchestration.md standalone first brief": "must stand alone" in orchestration,
        "decision-governance.md PASS_WITH_LIMITATIONS": "PASS_WITH_LIMITATIONS" in decision,
        "decision-governance.md claimed/verified": "`claimed`" in decision and "`verified`" in decision,
        "decision-governance.md actual project state": "Planned state" in decision,
        "SKILL.md semantic phase naming": "ODE45-Integration" in skill,
        "SKILL.md no second handoff format": "second handoff format" in skill,
        "communication.md evidence level tag": "Agent 自述" in communication,
        "communication.md escalation threshold": "architecture boundary" in communication,
    }
    missing = [name for name, present in required.items() if not present]
    if missing:
        fail("v0.6 rules missing: " + ", ".join(missing))
    return "orientation, granularity, evidence grade, actual-state-first and semantic naming present"


@check("SC-27", "v0.6.0 release fixes: provisional budget, observed/reported counts, S08 premise")
def sc27() -> str:
    decision = read_text("references/decision-governance.md")
    context = read_text("references/context-evolution.md")
    scenarios = read_text("tests/scenarios.md")
    s08 = scenarios.split("## S08 —", 1)[-1].split("## S09 —", 1)[0] if "## S08 —" in scenarios else ""
    s12 = scenarios.split("## S12 —", 1)[-1].split("## S13 —", 1)[0] if "## S12 —" in scenarios else ""
    required = {
        "decision-governance provisional budget": "provisional budget" in decision,
        "decision-governance owner and cadence": "review cadence" in decision,
        "context-evolution observed/reported split": "本次观察到" in context,
        "S08 task premise": "待执行任务" in s08,
        "S12 supplementary check": "补充检查" in s12,
    }
    missing = [name for name, present in required.items() if not present]
    if missing:
        fail("v0.6.0 release fixes missing: " + ", ".join(missing))
    return "provisional budget, owner/cadence, count separation and S08/S12 premises present"


@check("SC-28", "v0.7 architecture supervision and cold-start rules are present")
def sc28() -> str:
    skill = read_text("SKILL.md")
    decision = read_text("references/decision-governance.md")
    context = read_text("references/context-evolution.md")
    orchestration = read_text("references/orchestration.md")
    required = {
        "decision-governance Replacement review": "Replacement review" in decision,
        "decision-governance Product scope protection": "Product scope protection" in decision,
        "decision-governance Four acceptance dimensions": "Four acceptance dimensions" in decision,
        "decision-governance HOLD verdict": "HOLD" in decision,
        "decision-governance legacy governance": "Legacy and version governance" in decision,
        "context-evolution Cold start": "Cold start" in context,
        "context-evolution STATUS.md entry": "STATUS.md" in context,
        "orchestration Cold start": "Cold start" in orchestration,
        "orchestration PROPOSED split": "PROPOSED" in orchestration,
        "SKILL.md replacement review": "replacement" in skill,
        "SKILL.md cold start": "Cold start" in skill,
    }
    missing = [name for name, present in required.items() if not present]
    if missing:
        fail("v0.7 rules missing: " + ", ".join(missing))
    return "replacement review, scope protection, four dimensions, legacy governance and cold start present"


def run_checks() -> int:
    print("Tang-Personal-Brain — static validation")
    print("=" * 48)
    passed = failed = 0
    for identifier, title, function in CHECKS:
        try:
            detail = function()
            suffix = f" — {detail}" if detail else ""
            print(f"[PASS] {identifier} {title}{suffix}")
            passed += 1
        except CheckFailure as error:
            print(f"[FAIL] {identifier} {title} — {error}")
            failed += 1
        except Exception as error:  # noqa: BLE001 - report unexpected validator errors
            print(f"[FAIL] {identifier} {title} — unexpected {type(error).__name__}: {error}")
            failed += 1
    print()
    if WARNINGS:
        print("Warnings:")
        for warning in WARNINGS:
            print(f"  - {warning}")
        print()
    print(f"Result: {passed} passed, {failed} failed, {len(WARNINGS)} warning(s)")
    return 0 if failed == 0 else 1


def _expect(check_name: str, function, should_fail: bool, failures: list[str]) -> None:
    try:
        function()
        failed = False
        detail = ""
    except CheckFailure as error:
        failed = True
        detail = str(error)
    if failed != should_fail:
        expectation = "fail" if should_fail else "pass"
        failures.append(f"{check_name} should {expectation}" + (f" ({detail})" if detail else ""))
        print(f"[FAIL] self-test: {check_name}")
    else:
        print(f"[PASS] self-test: {check_name}")


def _require_detection(condition: bool, label: str) -> None:
    if not condition:
        raise CheckFailure(f"{label} not detected")


def _require_clean(issues: list[str]) -> None:
    if issues:
        raise CheckFailure("; ".join(issues))


def run_self_test() -> int:
    print("Tang-Personal-Brain — validator self-test")
    print("=" * 48)
    failures: list[str] = []
    valid = (
        "---\n"
        "name: sample-skill\n"
        'description: "Use when testing a valid skill description."\n'
        "metadata:\n"
        '  version: "0.1.0"\n'
        '  updated: "2026-11-05"\n'
        "---\n\n# Sample\n"
    )

    _expect("valid frontmatter passes", lambda: validate_frontmatter(valid), False, failures)
    valid_readme = "```text\n" + BOOTSTRAP_PROMPT + "\n```\n\n# Title\n"
    _expect(
        "valid README bootstrap passes",
        lambda: _require_clean(readme_bootstrap_issues(valid_readme)),
        False,
        failures,
    )
    _expect(
        "README without top block is rejected",
        lambda: _require_clean(readme_bootstrap_issues("# Title\n" + valid_readme)),
        True,
        failures,
    )
    _expect(
        "duplicate bootstrap prompt is rejected",
        lambda: _require_clean(readme_bootstrap_issues(valid_readme + "\n" + BOOTSTRAP_PROMPT + "\n")),
        True,
        failures,
    )
    _expect(
        "bad name is rejected",
        lambda: validate_frontmatter(valid.replace("sample-skill", "Bad_Name")),
        True,
        failures,
    )
    _expect(
        "missing description is rejected",
        lambda: validate_frontmatter(re.sub(r'description: ".*"\n', "", valid)),
        True,
        failures,
    )
    _expect(
        "long description is rejected",
        lambda: validate_frontmatter(valid.replace("Use when testing a valid skill description.", "x" * 1025)),
        True,
        failures,
    )
    secret = "prefix " + "gh" + "p_" + ("A" * 36)
    _expect(
        "GitHub token is detected",
        lambda: _require_detection(bool(scan_text(secret, SECRET_PATTERNS)), "GitHub token"),
        False,
        failures,
    )
    absolute = "see " + "C:" + "\\" + "Users" + "\\" + "alice" + "\\" + "file.txt"
    _expect(
        "absolute path is detected",
        lambda: _require_detection(bool(scan_text(absolute, ABS_PATH_PATTERNS)), "absolute path"),
        False,
        failures,
    )
    email = "contact " + "alice" + "@" + "example.com"
    _expect(
        "email identifier is detected",
        lambda: _require_detection(bool(EMAIL_PATTERN.search(email)), "email"),
        False,
        failures,
    )
    todo = "# Sample\n\n" + TODO_MARKER + " finish this section]\n"
    _expect(
        "TODO placeholder is detected",
        lambda: _require_detection(bool(re.search(re.escape(TODO_MARKER), strip_fences(todo), re.I)), "TODO"),
        False,
        failures,
    )
    broken = "See [missing](missing-file.md)."
    _expect(
        "broken link is detected",
        lambda: _require_detection(
            not resolve_link(ROOT / "README.md", extract_links(broken)[0]).exists(),
            "broken link",
        ),
        False,
        failures,
    )
    valid_block = "**类型：** 行为\n\n**输入：** x\n\n**预期输出特征：** y\n\n**判定标准：**\n\n- 必须：a\n- 禁止：b\n"
    _expect("valid scenario block passes", lambda: _require_clean(scenario_issues(valid_block)), False, failures)
    _expect(
        "incomplete scenario block is rejected",
        lambda: _require_clean(scenario_issues("**类型：** 行为")),
        True,
        failures,
    )

    print()
    if failures:
        for failure in failures:
            print(f"  - {failure}")
        print(f"Result: {len(failures)} self-test failure(s)")
        return 1
    print("Result: all self-tests passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Tang-Personal-Brain skill")
    parser.add_argument("--self-test", action="store_true", help="run negative tests for the validator")
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    return run_checks()


if __name__ == "__main__":
    raise SystemExit(main())
