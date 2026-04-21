#!/usr/bin/env python3

from __future__ import annotations

import argparse
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED_CONFIG_NAME = ".gitconfig.shared"
GLOBAL_DEFAULTS: tuple[tuple[str, str], ...] = (
    ("pull.rebase", "true"),
    ("rebase.autoStash", "true"),
    ("rebase.updateRefs", "true"),
    ("fetch.prune", "true"),
    ("merge.conflictstyle", "zdiff3"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Apply safe global Git defaults and opt into this repository's tracked local Git "
            "defaults by adding a local include for .gitconfig.shared."
        )
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=ROOT,
        help="Repository root. Defaults to this repository.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing local Git config.",
    )
    return parser.parse_args()


def run_git_command(
    repo_root: Path, args: list[str], *, check: bool = True
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and completed.returncode != 0:
        stderr = completed.stderr.strip()
        command = " ".join(["git", *args])
        raise RuntimeError(f"Command failed ({command}): {stderr}")
    return completed


def run_global_git_command(
    args: list[str], *, check: bool = True
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if check and completed.returncode != 0:
        stderr = completed.stderr.strip()
        command = " ".join(["git", *args])
        raise RuntimeError(f"Command failed ({command}): {stderr}")
    return completed


def git_dir(repo_root: Path) -> Path:
    completed = run_git_command(repo_root, ["rev-parse", "--git-dir"])
    git_dir_path = Path(completed.stdout.strip())
    if git_dir_path.is_absolute():
        return git_dir_path
    return (repo_root / git_dir_path).resolve()


def resolve_include_path(path_text: str, config_dir: Path) -> Path:
    include_path = Path(path_text).expanduser()
    if include_path.is_absolute():
        return include_path.resolve()
    return (config_dir / include_path).resolve()


def configured_include_paths(repo_root: Path, config_dir: Path) -> set[Path]:
    completed = run_git_command(
        repo_root,
        ["config", "--local", "--get-all", "include.path"],
        check=False,
    )
    if completed.returncode != 0:
        return set()

    return {
        resolve_include_path(line.strip(), config_dir)
        for line in completed.stdout.splitlines()
        if line.strip()
    }


def ensure_global_defaults(dry_run: bool) -> None:
    for key, desired_value in GLOBAL_DEFAULTS:
        completed = run_global_git_command(["config", "--global", "--get", key], check=False)
        current_value = completed.stdout.strip() if completed.returncode == 0 else None
        if current_value == desired_value:
            print(f"Global Git config already sets {key}={desired_value}")
            continue

        if dry_run:
            print(f"Would set git config --global {key} {desired_value}")
            continue

        run_global_git_command(["config", "--global", key, desired_value])
        print(f"Set git config --global {key} {desired_value}")


def ensure_local_include(repo_root: Path, shared_config: Path, dry_run: bool) -> None:
    config_dir = git_dir(repo_root)
    configured_paths = configured_include_paths(repo_root, config_dir)
    if shared_config in configured_paths:
        print(f"Local Git config already includes {shared_config}")
        return

    if dry_run:
        print(f"Would add local include.path {shared_config}")
        return

    run_git_command(repo_root, ["config", "--local", "--add", "include.path", str(shared_config)])
    print(f"Added local include.path {shared_config}")


def ensure_pre_commit_is_executable(path: Path, dry_run: bool) -> None:
    if not path.exists():
        raise RuntimeError(f"Pre-commit hook not found: {path}")

    current_mode = path.stat().st_mode
    executable_bits = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    if current_mode & executable_bits == executable_bits:
        print(f"Pre-commit hook already executable: {path}")
        return

    if dry_run:
        print(f"Would mark pre-commit hook executable: {path}")
        return

    path.chmod(current_mode | executable_bits)
    print(f"Marked pre-commit hook executable: {path}")


def warn_for_non_tracked_git_config(repo_root: Path, shared_config: Path) -> None:
    git_config_path = git_dir(repo_root) / "config"
    print(
        "Warning: this setup updates "
        f"{git_config_path} and global Git config. Those config files are outside normal repository "
        "tracking. The tracked repo-specific defaults live at "
        f"{shared_config}.",
        file=sys.stderr,
    )


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    shared_config = repo_root / SHARED_CONFIG_NAME
    if not shared_config.exists():
        raise RuntimeError(f"Shared Git config not found: {shared_config}")

    warn_for_non_tracked_git_config(repo_root, shared_config)
    ensure_global_defaults(args.dry_run)
    ensure_local_include(repo_root, shared_config, args.dry_run)
    ensure_pre_commit_is_executable(repo_root / ".githooks" / "pre-commit", args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
