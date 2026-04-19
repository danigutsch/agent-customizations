#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import TypedDict

ROOT = Path(__file__).resolve().parents[1]
SYNC_SCRIPT = ROOT / "scripts" / "sync_copilot_exports.py"
STATE_FILE_NAME = "agent-customizations-sync-state.json"
EXCLUDE_START = "# BEGIN agent-customizations exports"
DOT_GITHUB = ".github"
SKILLS_DIR = "skills"
SKILL_FILE = "SKILL.md"
SOURCE_GENERATION = "source-generation"
SOURCE_GENERATION_AGENT = "source-generation.agent.md"
SOURCE_GENERATION_INSTRUCTION = "source-generation.instructions.md"
SOURCE_GENERATION_PROMPT = "source-generation.prompt.md"
VERTICAL_SLICE_ARCHITECTURE = "vertical-slice-architecture"
VERTICAL_SLICE_ARCHITECTURE_AGENT = "vertical-slice-architecture.agent.md"
VERTICAL_SLICE_ARCHITECTURE_INSTRUCTION = "vertical-slice-architecture.instructions.md"
VERTICAL_SLICE_ARCHITECTURE_PROMPT = "vertical-slice-architecture.prompt.md"


class SyncState(TypedDict):
    managed_files: dict[str, list[str]]


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=True,
    )


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"Expected path to exist: {path}")


def assert_missing(path: Path) -> None:
    if path.exists():
        raise AssertionError(f"Expected path to be absent: {path}")


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_sync_state(path: Path) -> SyncState:
    data = load_json(path)
    if not isinstance(data, dict):
        raise AssertionError(f"Expected sync state JSON object: {path}")

    managed_files = data.get("managed_files")
    if not isinstance(managed_files, dict):
        raise AssertionError(f"Expected managed_files object in sync state: {path}")

    typed_managed_files: dict[str, list[str]] = {}
    for key, value in managed_files.items():
        if not isinstance(key, str) or not isinstance(value, list):
            raise AssertionError(f"Expected string keys and list values in sync state: {path}")
        if not all(isinstance(item, str) for item in value):
            raise AssertionError(f"Expected managed_files lists of strings in sync state: {path}")
        typed_managed_files[key] = value

    return {"managed_files": typed_managed_files}


def init_workspace_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "-q", str(path)])


def sync_exports(*args: str) -> None:
    run([sys.executable, str(SYNC_SCRIPT), *args], cwd=ROOT)


def test_workspace_plugin_export() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir) / "workspace-plugin"
        init_workspace_repo(repo_root)

        sync_exports(
            "--scope",
            "workspace",
            "--target-root",
            str(repo_root),
            "--plugin",
            "source-generation",
            "--write-git-exclude",
        )

        assert_exists(repo_root / DOT_GITHUB / "agents" / SOURCE_GENERATION_AGENT)
        assert_exists(repo_root / DOT_GITHUB / "instructions" / SOURCE_GENERATION_INSTRUCTION)
        assert_exists(repo_root / DOT_GITHUB / "prompts" / SOURCE_GENERATION_PROMPT)
        assert_exists(repo_root / DOT_GITHUB / SKILLS_DIR / SOURCE_GENERATION / SKILL_FILE)
        assert_exists(
            repo_root
            / DOT_GITHUB
            / SKILLS_DIR
            / SOURCE_GENERATION
            / "references"
            / "project-setup.md"
        )

        state_path = repo_root / ".git" / "info" / STATE_FILE_NAME
        state = load_sync_state(state_path)
        managed_files = state["managed_files"]
        if SOURCE_GENERATION_AGENT not in managed_files["agents"]:
            raise AssertionError("Expected source-generation agent in workspace state")
        if SOURCE_GENERATION_PROMPT not in managed_files["prompts"]:
            raise AssertionError("Expected source-generation prompt in workspace state")

        exclude_text = (repo_root / ".git" / "info" / "exclude").read_text(encoding="utf-8")
        if EXCLUDE_START not in exclude_text:
            raise AssertionError("Expected managed export block in .git/info/exclude")


def test_workspace_plugin_stale_cleanup() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir) / "workspace-stale"
        init_workspace_repo(repo_root)

        sync_exports(
            "--scope",
            "workspace",
            "--target-root",
            str(repo_root),
            "--plugin",
            "source-generation",
        )
        sync_exports(
            "--scope",
            "workspace",
            "--target-root",
            str(repo_root),
            "--plugin",
            "vertical-slice-architecture",
        )

        assert_missing(repo_root / DOT_GITHUB / "agents" / SOURCE_GENERATION_AGENT)
        assert_missing(repo_root / DOT_GITHUB / "prompts" / SOURCE_GENERATION_PROMPT)
        assert_missing(
            repo_root
            / DOT_GITHUB
            / SKILLS_DIR
            / SOURCE_GENERATION
            / "references"
            / "testing-and-ci.md"
        )
        assert_exists(repo_root / DOT_GITHUB / "agents" / VERTICAL_SLICE_ARCHITECTURE_AGENT)
        assert_exists(
            repo_root / DOT_GITHUB / "instructions" / VERTICAL_SLICE_ARCHITECTURE_INSTRUCTION
        )
        assert_exists(
            repo_root / DOT_GITHUB / SKILLS_DIR / VERTICAL_SLICE_ARCHITECTURE / SKILL_FILE
        )


def test_user_plugin_export() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        user_root = Path(temp_dir) / "copilot-user"
        user_root.mkdir(parents=True, exist_ok=True)

        sync_exports(
            "--scope",
            "user",
            "--target-root",
            str(user_root),
            "--plugin",
            "source-generation",
        )

        assert_exists(user_root / "agents" / SOURCE_GENERATION_AGENT)
        assert_exists(user_root / "instructions" / SOURCE_GENERATION_INSTRUCTION)
        assert_exists(user_root / SKILLS_DIR / SOURCE_GENERATION / SKILL_FILE)
        assert_missing(user_root / "prompts" / SOURCE_GENERATION_PROMPT)

        state_path = user_root / STATE_FILE_NAME
        state = load_sync_state(state_path)
        managed_files = state["managed_files"]
        if SOURCE_GENERATION_AGENT not in managed_files["agents"]:
            raise AssertionError("Expected source-generation agent in user state")
        if "prompts" in managed_files:
            raise AssertionError("Expected prompt surface to be absent for user exports")


def test_workspace_surface_export() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir) / "workspace-surface"
        init_workspace_repo(repo_root)

        sync_exports(
            "--scope",
            "workspace",
            "--target-root",
            str(repo_root),
            "--surface",
            "prompts",
        )

        assert_exists(repo_root / DOT_GITHUB / "prompts" / SOURCE_GENERATION_PROMPT)
        assert_exists(repo_root / DOT_GITHUB / "prompts" / VERTICAL_SLICE_ARCHITECTURE_PROMPT)
        assert_missing(repo_root / DOT_GITHUB / "agents" / SOURCE_GENERATION_AGENT)


def main() -> None:
    test_workspace_plugin_export()
    test_workspace_plugin_stale_cleanup()
    test_user_plugin_export()
    test_workspace_surface_export()
    print("Export smoke tests passed.")


if __name__ == "__main__":
    main()
