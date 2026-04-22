#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from sync_copilot_exports import SURFACES, supported_surfaces

BLOCK_START = "# BEGIN agent-customizations global ignores"
BLOCK_END = "# END agent-customizations global ignores"
KNOWN_CUSTOMIZATION_PATTERNS = [
    "**/.agents/",
    "**/.claude/",
    "**/.codex/",
    "**/.continue/",
    "**/.cursor/",
    "**/.github/copilot-instructions.md",
    "**/.github/agents/",
    "**/.github/instructions/",
    "**/.github/prompts/",
    "**/.github/skills/",
    "**/.github/hooks/",
    "**/CLAUDE.md",
    "**/GEMINI.md",
    "**/.copilot/agents/",
    "**/.copilot/instructions/",
    "**/.copilot/skills/",
    "**/.copilot/hooks/",
    "**/.roo/",
    "**/.windsurf/",
]
KNOWN_TRACKED_PATHS = [
    ".agents",
    ".claude",
    ".codex",
    ".continue",
    ".cursor",
    ".github/copilot-instructions.md",
    ".github/agents",
    ".github/instructions",
    ".github/prompts",
    ".github/skills",
    ".github/hooks",
    "CLAUDE.md",
    "GEMINI.md",
    ".copilot/agents",
    ".copilot/instructions",
    ".copilot/skills",
    ".copilot/hooks",
    ".roo",
    ".windsurf",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ensure a global gitignore exists for generated Copilot export folders."
    )
    parser.add_argument(
        "--surface",
        action="append",
        choices=sorted(supported_surfaces("workspace")),
        help="Workspace export surfaces to include in compatibility warnings. Defaults to all workspace surfaces.",
    )
    parser.add_argument(
        "--repo",
        action="append",
        default=[],
        type=Path,
        help="Repository root to check for compatibility warnings. Can be repeated.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing config or files.",
    )
    return parser.parse_args()


def selected_surfaces(requested: list[str] | None) -> list[str]:
    return requested if requested else sorted(supported_surfaces("workspace"))


def default_excludes_file() -> Path:
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home:
        return Path(xdg_config_home).expanduser() / "git" / "ignore"
    return Path.home() / ".config" / "git" / "ignore"


def run_git_command(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def configured_excludes_file() -> Path | None:
    result = run_git_command(["config", "--global", "--get", "core.excludesFile"])
    if result.returncode != 0:
        return None

    value = result.stdout.strip()
    if not value:
        return None

    return Path(value).expanduser()


def ensure_git_config(path: Path, dry_run: bool) -> None:
    configured = configured_excludes_file()
    if configured is not None:
        print(f"Global core.excludesFile already set to {configured}")
        return

    if dry_run:
        print(f"Would set git config --global core.excludesFile {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    result = run_git_command(["config", "--global", "core.excludesFile", str(path)])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Failed to set core.excludesFile")
    print(f"Set git config --global core.excludesFile {path}")


def ignore_patterns(surfaces: list[str]) -> list[str]:
    patterns = list(KNOWN_CUSTOMIZATION_PATTERNS)
    for surface in surfaces:
        target = SURFACES[surface]["workspace_target"]
        if target is not None:
            pattern = f"**/{target}/"
            if pattern not in patterns:
                patterns.append(pattern)
    return patterns


def managed_block(surfaces: list[str]) -> str:
    lines = [
        BLOCK_START,
        "# Generated and agent-specific customization paths managed by agent-customizations.",
    ]
    lines.extend(ignore_patterns(surfaces))
    lines.append(BLOCK_END)
    return "\n".join(lines) + "\n"


def upsert_block(path: Path, surfaces: list[str], dry_run: bool) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    start_index = existing.find(BLOCK_START)
    end_index = existing.find(BLOCK_END)
    if start_index != -1 and end_index != -1:
        end_index += len(BLOCK_END)
        prefix = existing[:start_index].rstrip()
        suffix = existing[end_index:].lstrip("\n")
        existing = f"{prefix}\n\n{suffix}".strip()

    block = managed_block(surfaces).strip()
    updated = block if not existing else f"{existing.rstrip()}\n\n{block}"
    updated += "\n"

    if dry_run:
        print(f"Would update global ignore file {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(updated, encoding="utf-8")
    print(f"Updated global ignore file {path}")


def repo_root(path: Path) -> Path | None:
    result = run_git_command(["-C", str(path), "rev-parse", "--show-toplevel"])
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def tracked_paths(root: Path, surfaces: list[str]) -> dict[str, list[str]]:
    tracked: dict[str, list[str]] = {}
    for tracked_path in KNOWN_TRACKED_PATHS:
        result = run_git_command(["-C", str(root), "ls-files", "--", tracked_path])
        files = [line for line in result.stdout.splitlines() if line.strip()]
        if files:
            tracked[tracked_path] = files

    for surface in surfaces:
        target = SURFACES[surface]["workspace_target"]
        if target is None:
            continue
        result = run_git_command(["-C", str(root), "ls-files", "--", target])
        files = [line for line in result.stdout.splitlines() if line.strip()]
        if files:
            tracked[f"surface:{surface}"] = files
    return tracked


def warn_for_repo(path: Path, surfaces: list[str]) -> None:
    root = repo_root(path)
    if root is None:
        print(
            f"Warning: {path} is not a Git repository. Skipping compatibility checks.",
            file=sys.stderr,
        )
        return

    tracked = tracked_paths(root, surfaces)
    if not tracked:
        print(f"{root}: no tracked files found in the selected exported Copilot paths")
        return

    print(f"Warning: {root} already tracks files in ignored export paths.", file=sys.stderr)
    print("Global ignore will not affect tracked files. Review these paths:", file=sys.stderr)
    for tracked_key, files in tracked.items():
        label = tracked_key.removeprefix("surface:")
        print(f"  - {label}:", file=sys.stderr)
        for file_path in files[:10]:
            print(f"    {file_path}", file=sys.stderr)
        if len(files) > 10:
            print(f"    ... and {len(files) - 10} more", file=sys.stderr)


def warn_for_global_ignore(path: Path, dry_run: bool) -> None:
    action = "would write to" if dry_run else "writes to"
    print(
        f"Warning: global ignore configuration {action} "
        f"{path}. This lives outside the repository and is normally not Git-tracked.",
        file=sys.stderr,
    )


def main() -> int:
    args = parse_args()
    surfaces = selected_surfaces(args.surface)
    excludes_file = configured_excludes_file() or default_excludes_file()
    warn_for_global_ignore(excludes_file, args.dry_run)

    try:
        ensure_git_config(excludes_file, args.dry_run)
        upsert_block(excludes_file, surfaces, args.dry_run)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    for repo in args.repo:
        warn_for_repo(repo.expanduser().resolve(), surfaces)

    if args.dry_run:
        print(f"Dry run complete for global ignore surfaces: {', '.join(surfaces)}")
    else:
        print(f"Configured global ignore surfaces: {', '.join(surfaces)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
