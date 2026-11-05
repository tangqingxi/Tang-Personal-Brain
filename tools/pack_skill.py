#!/usr/bin/env python3
"""Build and verify the distributable Tang-Personal-Brain skill bundle.

The bundle root is ``tang-personal-brain/`` and contains only files a host
needs to load the skill. Repository-only material (tests, tools, git data,
private memory) is excluded.

Usage:
    python tools/pack_skill.py
    python tools/pack_skill.py --verify-only
    python tools/pack_skill.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = "tang-personal-brain"
INCLUDE_FILES = ("SKILL.md", "README.md", "CHANGELOG.md")
INCLUDE_DIRS = ("agents", "references", "registry", "adapters")
EXCLUDED_PARTS = {"__pycache__", ".git", "memory", "tests", "tools", "dist"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".tmp"}
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


class PackError(RuntimeError):
    """Raised when the bundle cannot be built or verified."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _excluded(relative: Path) -> bool:
    return any(part in EXCLUDED_PARTS for part in relative.parts) or relative.suffix in EXCLUDED_SUFFIXES


def collect_files(root: Path = ROOT) -> list[Path]:
    """Return the source files that belong in the distributed bundle."""
    files: list[Path] = []
    for name in INCLUDE_FILES:
        path = root / name
        if not path.is_file():
            raise PackError(f"missing bundle file: {name}")
        files.append(path)
    for directory in INCLUDE_DIRS:
        base = root / directory
        if not base.is_dir():
            raise PackError(f"missing bundle directory: {directory}/")
        for path in base.rglob("*"):
            if path.is_file() and not _excluded(path.relative_to(root)):
                files.append(path)
    return sorted(set(files), key=lambda item: item.relative_to(root).as_posix())


def build_zip(output: Path, root: Path = ROOT) -> list[Path]:
    """Write a deterministic bundle zip and return its source files."""
    files = collect_files(root)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    try:
        with zipfile.ZipFile(
            temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            for path in files:
                relative = path.relative_to(root).as_posix()
                info = zipfile.ZipInfo(f"{BUNDLE}/{relative}", date_time=FIXED_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o644 << 16
                archive.writestr(info, path.read_bytes(), compresslevel=9)
        temporary.replace(output)
    finally:
        if temporary.exists():
            temporary.unlink()
    return files


def verify_zip(zip_path: Path, root: Path = ROOT) -> tuple[list[str], int, str]:
    """Check structure and byte equality against the repository sources."""
    zip_path = Path(zip_path)
    problems: list[str] = []
    if not zip_path.is_file():
        return [f"missing archive: {zip_path.name}"], 0, ""

    files = collect_files(root)
    expected = {
        f"{BUNDLE}/{path.relative_to(root).as_posix()}": sha256_file(path)
        for path in files
    }
    try:
        with zipfile.ZipFile(zip_path) as archive:
            broken = archive.testzip()
            if broken is not None:
                problems.append(f"corrupt entry: {broken}")
            names = archive.namelist()
            if len(names) != len(set(names)):
                problems.append("duplicate archive entries")
            for name in names:
                if not name.startswith(BUNDLE + "/"):
                    problems.append(f"entry outside bundle root: {name}")
                parts = Path(name).parts
                if any(part in EXCLUDED_PARTS for part in parts):
                    problems.append(f"excluded path in archive: {name}")
                if Path(name).suffix in EXCLUDED_SUFFIXES:
                    problems.append(f"excluded file type in archive: {name}")
            actual = {
                name: hashlib.sha256(archive.read(name)).hexdigest() for name in names
            }
    except zipfile.BadZipFile as error:
        return [f"invalid zip: {error}"], 0, ""

    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed = sorted(
        name for name in expected if name in actual and expected[name] != actual[name]
    )
    if missing:
        problems.append("missing entries: " + ", ".join(missing))
    if extra:
        problems.append("unexpected entries: " + ", ".join(extra))
    if changed:
        problems.append("content differs from source: " + ", ".join(changed))
    if f"{BUNDLE}/SKILL.md" not in actual:
        problems.append(f"SKILL.md is not at {BUNDLE}/SKILL.md")
    return problems, len(actual), sha256_file(zip_path)


def print_summary(zip_path: Path, files: int, digest: str) -> None:
    print(f"Bundle: {BUNDLE}")
    print(f"Files:  {files}")
    print(f"Zip:    {zip_path.name} ({zip_path.stat().st_size:,} bytes)")
    print(f"SHA256: {digest}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default=str(ROOT / "skill.zip"),
        help="archive path (default: skill.zip at repository root)",
    )
    parser.add_argument(
        "--verify-only", action="store_true", help="verify the existing archive"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="rebuild into a temporary file and compare with the existing archive",
    )
    args = parser.parse_args(argv)
    output = Path(args.output)

    try:
        if args.verify_only:
            if not output.is_file():
                print(f"FAIL: {output.name} does not exist", file=sys.stderr)
                return 1
            problems, count, digest = verify_zip(output)
            if problems:
                for problem in problems:
                    print(f"FAIL: {problem}", file=sys.stderr)
                return 1
            print_summary(output, count, digest)
            print("Verify: OK")
            return 0

        if args.check:
            if not output.is_file():
                print(f"FAIL: {output.name} does not exist", file=sys.stderr)
                return 1
            with tempfile.TemporaryDirectory() as temporary:
                rebuilt = Path(temporary) / output.name
                build_zip(rebuilt)
                rebuilt_digest = sha256_file(rebuilt)
                existing_digest = sha256_file(output)
            if rebuilt_digest != existing_digest:
                print(
                    "FAIL: archive is not reproducible; rebuild changes bytes",
                    file=sys.stderr,
                )
                print(f"  existing: {existing_digest}", file=sys.stderr)
                print(f"  rebuilt:  {rebuilt_digest}", file=sys.stderr)
                return 1
            problems, count, digest = verify_zip(output)
            if problems:
                for problem in problems:
                    print(f"FAIL: {problem}", file=sys.stderr)
                return 1
            print_summary(output, count, digest)
            print("Reproducible: OK")
            print("Verify: OK")
            return 0

        files = build_zip(output)
        problems, count, digest = verify_zip(output)
        if problems:
            for problem in problems:
                print(f"FAIL: {problem}", file=sys.stderr)
            return 1
        print_summary(output, count, digest)
        print(f"Source files: {len(files)}")
        print("Verify: OK")
        return 0
    except PackError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
