#!/usr/bin/env python3

from __future__ import annotations

import json
import py_compile
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", "__pycache__", "tmp", "temp"}


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


def main() -> int:
    errors: list[str] = []
    validate_toml(errors)
    validate_json(errors)
    validate_python(errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Repository file validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
