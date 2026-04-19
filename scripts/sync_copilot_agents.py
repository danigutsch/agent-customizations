#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import TypedDict, TypeGuard, cast


class SyncState(TypedDict):
    managed_files: list[str]


ROOT = Path(__file__).resolve().parents[1]
SOURCE_AGENTS_DIR = ROOT / ".agents" / "agents"
DEFAULT_TARGET_DIR = Path.home() / ".copilot" / "agents"
STATE_FILE_NAME = ".agents-sync-state.json"
AGENT_SUFFIX = ".agent.md"


def is_string_list(value: object) -> TypeGuard[list[str]]:
    if not isinstance(value, list):
        return False

    items = cast(list[object], value)
    return all(isinstance(item, str) for item in items)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync canonical .agents custom agents into ~/.copilot/agents for native Copilot discovery."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_TARGET_DIR,
        help="Target directory for synced Copilot agents. Defaults to ~/.copilot/agents.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=SOURCE_AGENTS_DIR,
        help="Source directory containing canonical .agent.md files. Defaults to .agents/agents.",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="AGENT_ID",
        help="Sync only specific agent ids, such as 'source-generation'. Can be repeated.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without copying or deleting files.",
    )
    parser.add_argument(
        "--no-delete-stale",
        action="store_true",
        help="Keep stale files that were previously synced but no longer exist in the source.",
    )
    return parser.parse_args()


def load_state(path: Path) -> SyncState:
    if not path.exists():
        return {"managed_files": []}

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        return {"managed_files": []}

    state = cast(dict[object, object], data)
    managed_files = state.get("managed_files", [])
    if not is_string_list(managed_files):
        return {"managed_files": []}

    return {"managed_files": managed_files}


def write_state(path: Path, managed_files: list[str], dry_run: bool) -> None:
    if dry_run:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump({"managed_files": managed_files}, handle, indent=2)
        handle.write("\n")


def collect_source_agents(source_dir: Path, only: list[str]) -> list[Path]:
    if not source_dir.exists():
        raise FileNotFoundError(f"Source agents directory does not exist: {source_dir}")

    candidates = sorted(path for path in source_dir.glob(f"*{AGENT_SUFFIX}") if path.is_file())
    if not only:
        return candidates

    allowed = set(only)
    filtered = [path for path in candidates if path.name.removesuffix(AGENT_SUFFIX) in allowed]
    missing = sorted(allowed - {path.name.removesuffix(AGENT_SUFFIX) for path in filtered})
    if missing:
        missing_list = ", ".join(missing)
        raise FileNotFoundError(f"Requested agent ids not found in source: {missing_list}")

    return filtered


def sync_agent(source: Path, target: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"Would copy {source} -> {target}")
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    print(f"Copied {source} -> {target}")


def delete_stale_agents(target_dir: Path, stale_files: list[str], dry_run: bool) -> None:
    for file_name in stale_files:
        target_path = target_dir / file_name
        if not target_path.exists():
            continue
        if dry_run:
            print(f"Would remove stale synced agent {target_path}")
            continue
        target_path.unlink()
        print(f"Removed stale synced agent {target_path}")


def main() -> int:
    args = parse_args()
    source_dir = args.source.resolve()
    target_dir = args.target.expanduser().resolve()
    state_path = target_dir / STATE_FILE_NAME

    try:
        source_agents = collect_source_agents(source_dir, args.only)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    current_managed_files = [agent.name for agent in source_agents]
    previous_state = load_state(state_path)
    stale_files = sorted(set(previous_state["managed_files"]) - set(current_managed_files))

    for source_agent in source_agents:
        sync_agent(source_agent, target_dir / source_agent.name, args.dry_run)

    if not args.no_delete_stale:
        delete_stale_agents(target_dir, stale_files, args.dry_run)

    write_state(state_path, current_managed_files, args.dry_run)

    summary_target = str(target_dir)
    if args.dry_run:
        print(f"Dry run complete for {len(source_agents)} agent(s) -> {summary_target}")
    else:
        print(f"Synced {len(source_agents)} agent(s) -> {summary_target}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
