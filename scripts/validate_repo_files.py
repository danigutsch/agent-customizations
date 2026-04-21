#!/usr/bin/env python3

from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", "__pycache__", "node_modules", "tmp", "temp"}
INLINE_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
INLINE_CODE_PATTERN = re.compile(r"`[^`]*`")
IGNORED_LINK_PREFIXES = ("#", "http://", "https://", "mailto:", "tel:", "data:", "ftp:")


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def iter_files(pattern: str) -> list[Path]:
    return sorted(path for path in ROOT.rglob(pattern) if path.is_file() and not should_skip(path))


def validate_toml(errors: list[str]) -> None:
    for path in iter_files("*.toml"):
        try:
            with path.open("rb") as handle:
                tomllib.load(handle)
        except tomllib.TOMLDecodeError as exc:
            errors.append(f"TOML parse error in {path.relative_to(ROOT)}: {exc}")


def validate_json(errors: list[str]) -> None:
    for path in iter_files("*.json"):
        try:
            with path.open("r", encoding="utf-8") as handle:
                json.load(handle)
        except json.JSONDecodeError as exc:
            errors.append(f"JSON parse error in {path.relative_to(ROOT)}: {exc}")


def validate_python(errors: list[str]) -> None:
    for path in iter_files("*.py"):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"Python compile error in {path.relative_to(ROOT)}: {exc.msg}")


def validate_markdown(errors: list[str]) -> None:
    try:
        subprocess.run(["npm", "run", "--silent", "lint:markdown"], cwd=ROOT, check=True)
    except FileNotFoundError:
        errors.append(
            "Missing required tool: npm. Install Node.js/npm first, then run `make install-dev` "
            "before repository validation."
        )
    except subprocess.CalledProcessError as exc:
        errors.append(f"Markdown lint failed with exit code {exc.returncode}.")


def strip_inline_code(text: str) -> str:
    return INLINE_CODE_PATTERN.sub("", text)


def extract_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if not target:
        return ""
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")].strip()
    return target.split(maxsplit=1)[0]


def resolve_markdown_target(source_path: Path, target: str) -> Path | None:
    if target.startswith("/"):
        resolved = (ROOT / target.lstrip("/")).resolve()
    else:
        resolved = (source_path.parent / target).resolve()

    try:
        resolved.relative_to(ROOT)
    except ValueError:
        return None
    return resolved


def toggles_fenced_code_block(line: str) -> bool:
    return line.lstrip().startswith("```")


def is_ignored_markdown_target(target: str) -> bool:
    return not target or target.startswith(IGNORED_LINK_PREFIXES)


def markdown_link_errors(path: Path, line_number: int, raw_line: str) -> list[str]:
    errors: list[str] = []
    line = strip_inline_code(raw_line)

    for match in INLINE_LINK_PATTERN.finditer(line):
        target = extract_link_target(match.group(1))
        if is_ignored_markdown_target(target):
            continue

        path_text, _, _fragment = target.partition("#")
        if not path_text:
            continue

        resolved = resolve_markdown_target(path, path_text)
        if resolved is None or not resolved.exists():
            errors.append(
                f"Markdown link target does not exist in {path.relative_to(ROOT)}:{line_number}: {path_text}"
            )

    return errors


def validate_markdown_links(errors: list[str]) -> None:
    for path in iter_files("*.md"):
        try:
            contents = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"Could not read Markdown file {path.relative_to(ROOT)}: {exc}")
            continue

        in_fence = False
        for line_number, raw_line in enumerate(contents.splitlines(), start=1):
            if toggles_fenced_code_block(raw_line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            errors.extend(markdown_link_errors(path, line_number, raw_line))


def validate_generated_readme(errors: list[str]) -> None:
    try:
        subprocess.run(
            [sys.executable, "scripts/sync_readme_plugin_changelog.py", "--check"],
            cwd=ROOT,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        errors.append(f"README plugin changelog sync check failed with exit code {exc.returncode}.")


def main() -> int:
    errors: list[str] = []
    validate_toml(errors)
    validate_json(errors)
    validate_python(errors)
    validate_markdown(errors)
    validate_markdown_links(errors)
    validate_generated_readme(errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Repository file validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
