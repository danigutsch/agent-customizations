#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import TypeGuard, TypedDict, cast


class SyncState(TypedDict):
    managed_files: dict[str, list[str]]


class SurfaceSpec(TypedDict):
    source: Path
    target: Path
    mode: str
    pattern: str


ROOT = Path(__file__).resolve().parents[1]
AGENTS_ROOT = ROOT / ".agents"
DEFAULT_COPILOT_ROOT = Path.home() / ".copilot"
STATE_FILE_NAME = ".agent-customizations-sync-state.json"

SURFACES: dict[str, SurfaceSpec] = {
    "agents": {
        "source": AGENTS_ROOT / "agents",
        "target": DEFAULT_COPILOT_ROOT / "agents",
        "mode": "files",
        "pattern": "*.agent.md",
    },
    "instructions": {
        "source": AGENTS_ROOT / "instructions",
        "target": DEFAULT_COPILOT_ROOT / "instructions",
        "mode": "files",
        "pattern": "**/*.instructions.md",
    },
    "skills": {
        "source": AGENTS_ROOT / "skills",
        "target": DEFAULT_COPILOT_ROOT / "skills",
        "mode": "directories",
        "pattern": "*",
    },
    "hooks": {
        "source": AGENTS_ROOT / "hooks",
        "target": DEFAULT_COPILOT_ROOT / "hooks",
        "mode": "files",
        "pattern": "**/*.json",
    },
}


def is_string_list(value: object) -> TypeGuard[list[str]]:
    if not isinstance(value, list):
        return False

    items = cast(list[object], value)
    return all(isinstance(item, str) for item in items)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync supported .agents surfaces into user-level ~/.copilot compatibility locations."
    )
    parser.add_argument(
        "--copilot-root",
        type=Path,
        default=DEFAULT_COPILOT_ROOT,
        help="User-level Copilot root directory. Defaults to ~/.copilot.",
    )
    parser.add_argument(
        "--surface",
        action="append",
        choices=sorted(SURFACES.keys()),
        help="Sync only specific surfaces. Can be repeated.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without copying or deleting files.",
    )
    parser.add_argument(
        "--no-delete-stale",
        action="store_true",
        help="Keep stale files and folders that were previously synced but no longer exist in the source.",
    )
    return parser.parse_args()


def load_state(path: Path) -> SyncState:
    if not path.exists():
        return {"managed_files": {}}

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        return {"managed_files": {}}

    raw_state = cast(dict[object, object], data)
    managed_files = raw_state.get("managed_files", {})
    if not isinstance(managed_files, dict):
        return {"managed_files": {}}

    typed_state: dict[str, list[str]] = {}
    for key, value in cast(dict[object, object], managed_files).items():
        if isinstance(key, str) and is_string_list(value):
            typed_state[key] = value

    return {"managed_files": typed_state}


def write_state(path: Path, state: SyncState, dry_run: bool) -> None:
    if dry_run:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")


def selected_surfaces(requested: list[str] | None) -> list[str]:
    if not requested:
        return list(SURFACES.keys())
    return requested


def relative_to(source_root: Path, path: Path) -> str:
    return path.relative_to(source_root).as_posix()


def collect_surface_entries(spec: SurfaceSpec) -> list[tuple[Path, str]]:
    source_root = spec["source"]
    if not source_root.exists():
        return []

    if spec["mode"] == "files":
        entries = sorted(path for path in source_root.glob(spec["pattern"]) if path.is_file())
    else:
        entries = sorted(path for path in source_root.glob(spec["pattern"]) if path.is_dir())

    return [(entry, relative_to(source_root, entry)) for entry in entries]


def sync_file(source: Path, target: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"Would copy {source} -> {target}")
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    print(f"Copied {source} -> {target}")


def sync_directory(source: Path, target: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"Would sync directory {source} -> {target}")
        return

    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    print(f"Synced directory {source} -> {target}")


def remove_stale_path(target: Path, dry_run: bool) -> None:
    if not target.exists():
        return

    if dry_run:
        print(f"Would remove stale synced path {target}")
        return

    if target.is_dir():
        shutil.rmtree(target)
    else:
        target.unlink()
    print(f"Removed stale synced path {target}")


def sync_surface(
    surface: str,
    spec: SurfaceSpec,
    previous_managed: list[str],
    dry_run: bool,
    delete_stale: bool,
) -> list[str]:
    entries = collect_surface_entries(spec)
    source_root = spec["source"]
    target_root = spec["target"]

    current_managed = [relative_path for _, relative_path in entries]
    for source_entry, relative_path in entries:
        target_path = target_root / relative_path
        if spec["mode"] == "files":
            sync_file(source_entry, target_path, dry_run)
        else:
            sync_directory(source_entry, target_path, dry_run)

    if delete_stale:
        stale_paths = sorted(set(previous_managed) - set(current_managed))
        for stale_path in stale_paths:
            remove_stale_path(target_root / stale_path, dry_run)

    if entries:
        print(f"Prepared {len(entries)} {surface} entries from {source_root} -> {target_root}")
    else:
        print(f"No {surface} entries found under {source_root}")

    return current_managed


def main() -> int:
    args = parse_args()
    copilot_root = args.copilot_root.expanduser().resolve()
    state_path = copilot_root / STATE_FILE_NAME
    state = load_state(state_path)

    requested_surfaces = selected_surfaces(args.surface)
    updated_state: dict[str, list[str]] = dict(state["managed_files"])

    for surface in requested_surfaces:
        base_spec = SURFACES[surface]
        spec: SurfaceSpec = {
            "source": base_spec["source"],
            "target": copilot_root / base_spec["target"].name,
            "mode": base_spec["mode"],
            "pattern": base_spec["pattern"],
        }
        previous_managed = state["managed_files"].get(surface, [])
        updated_state[surface] = sync_surface(
            surface,
            spec,
            previous_managed,
            args.dry_run,
            not args.no_delete_stale,
        )

    write_state(state_path, {"managed_files": updated_state}, args.dry_run)

    if args.dry_run:
        print(f"Dry run complete for surfaces: {', '.join(requested_surfaces)}")
    else:
        print(f"Synced surfaces: {', '.join(requested_surfaces)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
