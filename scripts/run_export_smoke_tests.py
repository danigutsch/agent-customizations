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
HOOKS_DIR = "hooks"
GIT_HOOKS = "git-hooks"
HOOKS_README = "README.md"
PRE_COMMIT_EXAMPLE = "pre-commit-fast-checks.example.sh"
PLUGIN_ROOT = ROOT / ".agents" / "plugins"
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
TEMP_HOOK_PLUGIN = "temp-hook-plugin"


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


def init_workspace_native_skills(path: Path) -> None:
    native_skill_dir = path / ".agents" / SKILLS_DIR / SOURCE_GENERATION
    native_skill_dir.mkdir(parents=True, exist_ok=True)
    (native_skill_dir / SKILL_FILE).write_text("native skill\n", encoding="utf-8")


def sync_exports(*args: str) -> None:
    run([sys.executable, str(SYNC_SCRIPT), *args], cwd=ROOT)


def create_temp_hook_plugin() -> Path:
    plugin_dir = PLUGIN_ROOT / TEMP_HOOK_PLUGIN
    plugin_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schemaVersion": "1.0.0",
        "id": TEMP_HOOK_PLUGIN,
        "contents": [{"path": ".agents/hooks/git-hooks"}],
    }
    (plugin_dir / "plugin.json").write_text(f"{json.dumps(manifest, indent=2)}\n", encoding="utf-8")
    return plugin_dir


def test_workspace_plugin_export() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir) / "workspace-plugin"
        init_workspace_repo(repo_root)

        sync_exports(
            "--scope",
            "workspace",
            "--runtime-authority",
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
            "--runtime-authority",
            "workspace",
            "--target-root",
            str(repo_root),
            "--plugin",
            "source-generation",
        )
        sync_exports(
            "--scope",
            "workspace",
            "--runtime-authority",
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


def test_user_hook_export() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        user_root = Path(temp_dir) / "copilot-user-hooks"
        user_root.mkdir(parents=True, exist_ok=True)

        sync_exports(
            "--scope",
            "user",
            "--target-root",
            str(user_root),
            "--surface",
            "hooks",
        )

        assert_exists(user_root / HOOKS_DIR / GIT_HOOKS / HOOKS_README)
        assert_exists(user_root / HOOKS_DIR / GIT_HOOKS / PRE_COMMIT_EXAMPLE)

        state_path = user_root / STATE_FILE_NAME
        state = load_sync_state(state_path)
        managed_files = state["managed_files"]
        if GIT_HOOKS not in managed_files["hooks"]:
            raise AssertionError("Expected git-hooks directory in user hook export state")


def test_user_hook_plugin_export() -> None:
    plugin_dir = create_temp_hook_plugin()
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            user_root = Path(temp_dir) / "copilot-user-hook-plugin"
            user_root.mkdir(parents=True, exist_ok=True)

            sync_exports(
                "--scope",
                "user",
                "--target-root",
                str(user_root),
                "--plugin",
                TEMP_HOOK_PLUGIN,
            )

            assert_exists(user_root / HOOKS_DIR / GIT_HOOKS / HOOKS_README)
            assert_exists(user_root / HOOKS_DIR / GIT_HOOKS / PRE_COMMIT_EXAMPLE)

            state_path = user_root / STATE_FILE_NAME
            state = load_sync_state(state_path)
            managed_files = state["managed_files"]
            if GIT_HOOKS not in managed_files["hooks"]:
                raise AssertionError(
                    "Expected git-hooks directory in user hook plugin export state"
                )
    finally:
        if plugin_dir.exists():
            for child in plugin_dir.iterdir():
                child.unlink()
            plugin_dir.rmdir()


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


def test_workspace_hook_export_with_workspace_authority() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir) / "workspace-hooks"
        init_workspace_repo(repo_root)

        sync_exports(
            "--scope",
            "workspace",
            "--runtime-authority",
            "workspace",
            "--target-root",
            str(repo_root),
            "--surface",
            "hooks",
        )

        assert_exists(repo_root / DOT_GITHUB / HOOKS_DIR / GIT_HOOKS / HOOKS_README)
        assert_exists(repo_root / DOT_GITHUB / HOOKS_DIR / GIT_HOOKS / PRE_COMMIT_EXAMPLE)


def test_workspace_default_skips_native_skill_surface() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir) / "workspace-native-skills"
        init_workspace_repo(repo_root)
        init_workspace_native_skills(repo_root)

        sync_exports(
            "--scope",
            "workspace",
            "--runtime-authority",
            "workspace",
            "--target-root",
            str(repo_root),
        )

        assert_missing(repo_root / DOT_GITHUB / SKILLS_DIR / SOURCE_GENERATION / SKILL_FILE)
        assert_exists(repo_root / DOT_GITHUB / "agents" / SOURCE_GENERATION_AGENT)
        assert_exists(repo_root / DOT_GITHUB / "prompts" / SOURCE_GENERATION_PROMPT)


def test_workspace_default_prefers_user_runtime_authority() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir) / "workspace-user-default"
        init_workspace_repo(repo_root)

        sync_exports(
            "--scope",
            "workspace",
            "--target-root",
            str(repo_root),
        )

        assert_exists(repo_root / DOT_GITHUB / "prompts" / SOURCE_GENERATION_PROMPT)
        assert_missing(repo_root / DOT_GITHUB / "agents" / SOURCE_GENERATION_AGENT)
        assert_missing(repo_root / DOT_GITHUB / "instructions" / SOURCE_GENERATION_INSTRUCTION)
        assert_missing(repo_root / DOT_GITHUB / SKILLS_DIR / SOURCE_GENERATION / SKILL_FILE)


def test_workspace_default_cleans_up_previous_runtime_exports() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir) / "workspace-cleanup"
        init_workspace_repo(repo_root)

        sync_exports(
            "--scope",
            "workspace",
            "--runtime-authority",
            "workspace",
            "--target-root",
            str(repo_root),
        )
        sync_exports(
            "--scope",
            "workspace",
            "--target-root",
            str(repo_root),
        )

        assert_exists(repo_root / DOT_GITHUB / "prompts" / SOURCE_GENERATION_PROMPT)
        assert_missing(repo_root / DOT_GITHUB / "agents" / SOURCE_GENERATION_AGENT)
        assert_missing(repo_root / DOT_GITHUB / "instructions" / SOURCE_GENERATION_INSTRUCTION)
        assert_missing(repo_root / DOT_GITHUB / SKILLS_DIR / SOURCE_GENERATION / SKILL_FILE)


def test_workspace_default_preserves_previous_runtime_exports_when_stale_cleanup_disabled() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir) / "workspace-preserve-stale"
        init_workspace_repo(repo_root)

        sync_exports(
            "--scope",
            "workspace",
            "--runtime-authority",
            "workspace",
            "--target-root",
            str(repo_root),
        )
        sync_exports(
            "--scope",
            "workspace",
            "--target-root",
            str(repo_root),
            "--no-delete-stale",
        )

        assert_exists(repo_root / DOT_GITHUB / "agents" / SOURCE_GENERATION_AGENT)
        assert_exists(repo_root / DOT_GITHUB / "instructions" / SOURCE_GENERATION_INSTRUCTION)
        assert_exists(repo_root / DOT_GITHUB / SKILLS_DIR / SOURCE_GENERATION / SKILL_FILE)

        state_path = repo_root / ".git" / "info" / STATE_FILE_NAME
        state = load_sync_state(state_path)
        managed_files = state["managed_files"]
        if SOURCE_GENERATION_AGENT not in managed_files["agents"]:
            raise AssertionError(
                "Expected source-generation agent to remain tracked when stale cleanup is disabled"
            )

        sync_exports(
            "--scope",
            "workspace",
            "--target-root",
            str(repo_root),
        )

        assert_missing(repo_root / DOT_GITHUB / "agents" / SOURCE_GENERATION_AGENT)
        assert_missing(repo_root / DOT_GITHUB / "instructions" / SOURCE_GENERATION_INSTRUCTION)
        assert_missing(repo_root / DOT_GITHUB / SKILLS_DIR / SOURCE_GENERATION / SKILL_FILE)


def main() -> None:
    test_workspace_plugin_export()
    test_workspace_plugin_stale_cleanup()
    test_user_plugin_export()
    test_user_hook_export()
    test_user_hook_plugin_export()
    test_workspace_surface_export()
    test_workspace_hook_export_with_workspace_authority()
    test_workspace_default_skips_native_skill_surface()
    test_workspace_default_prefers_user_runtime_authority()
    test_workspace_default_cleans_up_previous_runtime_exports()
    test_workspace_default_preserves_previous_runtime_exports_when_stale_cleanup_disabled()
    print("Export smoke tests passed.")


if __name__ == "__main__":
    main()
