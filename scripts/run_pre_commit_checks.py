#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_EXTENSIONS = {".json", ".jsonc", ".md", ".toml", ".yaml", ".yml"}
REPO_VALIDATION_FILES = {
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "pyproject.toml",
}


def run(command: list[str]) -> None:
    try:
        subprocess.run(command, cwd=ROOT, check=True)
    except FileNotFoundError as exc:
        missing_tool = command[0]
        print(
            f"Missing required tool: {missing_tool}. Run `make install-dev` before using the hook.",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc


def staged_files() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def needs_repo_validation(paths: list[Path]) -> bool:
    return any(
        path.name in REPO_VALIDATION_FILES
        or path.suffix in CONFIG_EXTENSIONS
        or path.parts[0] in {".github", "docs"}
        for path in paths
    )


def needs_plugin_validation(paths: list[Path]) -> bool:
    return any(path.parts[:2] == (".agents", "plugins") for path in paths if len(path.parts) >= 2)


def staged_script_python_files(paths: list[Path]) -> list[str]:
    return [
        path.as_posix()
        for path in paths
        if path.suffix == ".py" and len(path.parts) >= 1 and path.parts[0] == "scripts"
    ]


def main() -> None:
    paths = staged_files()
    if not paths:
        print("No staged files to validate.")
        return

    python_files = staged_script_python_files(paths)
    if python_files:
        run(["python3", "-m", "ruff", "check", *python_files])
        run(["python3", "-m", "pyright", "scripts"])

    if needs_repo_validation(paths):
        run(["python3", "scripts/validate_repo_files.py"])

    if needs_plugin_validation(paths):
        run(["python3", "scripts/validate_plugin_bundles.py"])


if __name__ == "__main__":
    main()
