#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import TypedDict, TypeGuard, cast


class SyncState(TypedDict):
    managed_files: dict[str, list[str]]


class SurfaceSpec(TypedDict):
    source: Path
    mode: str
    pattern: str
    user_target: str | None
    workspace_target: str | None


class PluginContentItem(TypedDict):
    path: str


class PluginManifest(TypedDict):
    id: str
    contents: list[PluginContentItem]


ROOT = Path(__file__).resolve().parents[1]
AGENTS_ROOT = ROOT / ".agents"
DEFAULT_COPILOT_ROOT = Path.home() / ".copilot"
PLUGIN_ROOT = AGENTS_ROOT / "plugins"
STATE_FILE_NAME = "agent-customizations-sync-state.json"
EXCLUDE_START = "# BEGIN agent-customizations exports"
EXCLUDE_END = "# END agent-customizations exports"
NATIVE_PROJECT_SURFACES: dict[str, Path] = {
    "skills": Path(".agents/skills"),
}

SURFACES: dict[str, SurfaceSpec] = {
    "agents": {
        "source": AGENTS_ROOT / "agents",
        "mode": "files",
        "pattern": "*.agent.md",
        "user_target": "agents",
        "workspace_target": ".github/agents",
    },
    "instructions": {
        "source": AGENTS_ROOT / "instructions",
        "mode": "files",
        "pattern": "**/*.instructions.md",
        "user_target": "instructions",
        "workspace_target": ".github/instructions",
    },
    "prompts": {
        "source": AGENTS_ROOT / "prompts",
        "mode": "files",
        "pattern": "**/*.prompt.md",
        "user_target": None,
        "workspace_target": ".github/prompts",
    },
    "skills": {
        "source": AGENTS_ROOT / "skills",
        "mode": "directories",
        "pattern": "*",
        "user_target": "skills",
        "workspace_target": ".github/skills",
    },
    "hooks": {
        "source": AGENTS_ROOT / "hooks",
        "mode": "directories",
        "pattern": "*",
        "user_target": "hooks",
        "workspace_target": ".github/hooks",
    },
}

USER_OVERLAP_WORKSPACE_SURFACES = frozenset(
    surface
    for surface, spec in SURFACES.items()
    if spec["user_target"] is not None and spec["workspace_target"] is not None
)


def is_string_list(value: object) -> TypeGuard[list[str]]:
    if not isinstance(value, list):
        return False

    items = cast(list[object], value)
    return all(isinstance(item, str) for item in items)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync canonical .agents assets into Copilot-native user or workspace locations."
    )
    parser.add_argument(
        "--scope",
        choices=["user", "workspace"],
        default="user",
        help="Export scope. User syncs into ~/.copilot. Workspace syncs into .github/ under a target repo.",
    )
    parser.add_argument(
        "--target-root",
        type=Path,
        help="Target root. Defaults to ~/.copilot for user scope or the current directory for workspace scope.",
    )
    parser.add_argument(
        "--plugin",
        action="append",
        default=[],
        metavar="PLUGIN_ID",
        help="Sync files listed by one or more plugin manifests. Can be repeated.",
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
        "--runtime-authority",
        choices=["user", "workspace"],
        default="user",
        help=(
            "For workspace scope, choose whether overlapping runtime surfaces default to user-level "
            "~/.copilot exports or workspace-level .github exports. Explicit --surface selections still "
            "win."
        ),
    )
    parser.add_argument(
        "--no-delete-stale",
        action="store_true",
        help="Keep stale files or directories that were previously synced but no longer exist in the source.",
    )
    parser.add_argument(
        "--write-git-exclude",
        action="store_true",
        help="For workspace scope, write generated export paths into .git/info/exclude.",
    )
    return parser.parse_args()


def resolve_target_root(args: argparse.Namespace) -> Path:
    if args.target_root is not None:
        return args.target_root.expanduser().resolve()

    if args.scope == "user":
        return DEFAULT_COPILOT_ROOT.resolve()

    return Path.cwd().resolve()


def supported_surfaces(scope: str) -> list[str]:
    key = f"{scope}_target"
    return [name for name, spec in SURFACES.items() if spec[key] is not None]


def has_native_project_surface(target_root: Path, surface: str) -> bool:
    native_root = NATIVE_PROJECT_SURFACES.get(surface)
    if native_root is None:
        return False

    return (target_root / native_root).exists()


def selected_surfaces(
    scope: str,
    target_root: Path,
    runtime_authority: str,
    requested: list[str] | None,
) -> tuple[list[str], list[str], list[str]]:
    available = supported_surfaces(scope)
    if not requested:
        skipped_authority = sorted(
            surface
            for surface in available
            if scope == "workspace"
            and runtime_authority == "user"
            and surface in USER_OVERLAP_WORKSPACE_SURFACES
        )
        skipped_native = sorted(
            surface
            for surface in available
            if scope == "workspace" and has_native_project_surface(target_root, surface)
        )
        skipped = set(skipped_authority) | set(skipped_native)
        return (
            [surface for surface in available if surface not in skipped],
            skipped_native,
            skipped_authority,
        )

    unsupported = sorted(surface for surface in requested if surface not in available)
    if unsupported:
        unsupported_list = ", ".join(unsupported)
        raise ValueError(f"Unsupported surfaces for {scope} scope: {unsupported_list}")

    return requested, [], []


def load_plugin_manifest(plugin_id: str) -> PluginManifest:
    manifest_path = PLUGIN_ROOT / plugin_id / "plugin.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Plugin manifest not found: {manifest_path}")

    with manifest_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise ValueError(f"Plugin manifest is not a JSON object: {manifest_path}")

    raw_manifest = cast(dict[object, object], data)
    manifest_id = raw_manifest.get("id")
    raw_contents = raw_manifest.get("contents")

    if not isinstance(manifest_id, str):
        raise ValueError(f"Plugin manifest id is invalid: {manifest_path}")
    if not isinstance(raw_contents, list):
        raise ValueError(f"Plugin manifest contents are invalid: {manifest_path}")

    contents: list[PluginContentItem] = []
    for item in raw_contents:
        if not isinstance(item, dict):
            continue
        raw_item = cast(dict[object, object], item)
        item_path = raw_item.get("path")
        if isinstance(item_path, str):
            contents.append({"path": item_path})

    return {"id": manifest_id, "contents": contents}


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


def get_target_subdir(spec: SurfaceSpec, scope: str) -> str:
    target = spec[f"{scope}_target"]
    if target is None:
        raise ValueError(f"Surface is not supported for {scope} scope.")
    return target


def collect_entries(spec: SurfaceSpec) -> list[tuple[Path, str]]:
    source_root = spec["source"]
    if not source_root.exists():
        return []

    if spec["mode"] == "files":
        matches = sorted(path for path in source_root.glob(spec["pattern"]) if path.is_file())
    else:
        matches = sorted(path for path in source_root.glob(spec["pattern"]) if path.is_dir())

    return [(path, path.relative_to(source_root).as_posix()) for path in matches]


def plugin_entry_for(path_text: str, scope: str) -> tuple[str, Path, str] | None:
    path = ROOT / path_text
    for surface, spec in SURFACES.items():
        if spec[f"{scope}_target"] is None:
            continue

        source_root = spec["source"]
        try:
            relative_path = path.relative_to(source_root)
        except ValueError:
            continue

        return surface, path, relative_path.as_posix()

    return None


def collect_plugin_entries(
    plugin_ids: list[str],
    scope: str,
    surfaces: list[str],
) -> dict[str, list[tuple[Path, str]]]:
    planned: dict[str, dict[str, Path]] = {surface: {} for surface in surfaces}

    for plugin_id in plugin_ids:
        manifest = load_plugin_manifest(plugin_id)
        for item in manifest["contents"]:
            entry = plugin_entry_for(item["path"], scope)
            if entry is None:
                continue

            surface, source_path, relative_path = entry
            if surface not in planned or not source_path.exists():
                continue
            planned[surface][relative_path] = source_path

    return {
        surface: [
            (source_path, relative_path)
            for relative_path, source_path in sorted(entries.items())
            if not any(
                parent.as_posix() in entries and entries[parent.as_posix()].is_dir()
                for parent in Path(relative_path).parents
                if parent != Path(".")
            )
        ]
        for surface, entries in planned.items()
    }


def copy_file(source: Path, target: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"Would copy {source} -> {target}")
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    print(f"Copied {source} -> {target}")


def copy_directory(source: Path, target: Path, dry_run: bool) -> None:
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


def paths_overlap(path_text: str, other_path_text: str) -> bool:
    path = Path(path_text)
    other_path = Path(other_path_text)
    return path == other_path or path in other_path.parents or other_path in path.parents


def stale_paths_to_remove(
    previous_managed: list[str],
    current_managed: list[str],
) -> list[str]:
    current_set = set(current_managed)
    return sorted(
        stale_path
        for stale_path in set(previous_managed) - current_set
        if not any(paths_overlap(stale_path, current_path) for current_path in current_managed)
    )


def resolve_git_dir(workspace_root: Path) -> Path | None:
    dot_git = workspace_root / ".git"
    if dot_git.is_dir():
        return dot_git
    if not dot_git.is_file():
        return None

    content = dot_git.read_text(encoding="utf-8").strip()
    prefix = "gitdir: "
    if not content.startswith(prefix):
        return None

    return (workspace_root / content[len(prefix) :]).resolve()


def resolve_git_repo_root(path: Path) -> Path | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(f"Failed to inspect Git repository for {path}: {exc}") from exc
    if completed.returncode != 0:
        return None
    return Path(completed.stdout.strip()).resolve()


def git_ls_files(repo_root: Path, relative_path: Path) -> list[str]:
    pathspec = relative_path.as_posix().rstrip("/")
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "ls-files", "--", pathspec],
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(f"Failed to inspect Git-tracked paths under {repo_root}: {exc}") from exc

    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        details = f": {stderr}" if stderr else ""
        raise RuntimeError(
            f"Failed to inspect Git-tracked paths under {repo_root} for {pathspec} "
            f"(exit code {completed.returncode}){details}"
        )

    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def is_git_tracked(repo_root: Path, target_path: Path) -> bool:
    try:
        relative_path = target_path.resolve().relative_to(repo_root)
    except ValueError:
        return False

    pathspec = relative_path.as_posix().rstrip("/")
    tracked_paths = git_ls_files(repo_root, relative_path)
    return any(
        tracked_path == pathspec or tracked_path.startswith(f"{pathspec}/")
        for tracked_path in tracked_paths
    )


def warn_for_git_tracking(scope: str, target_root: Path, surfaces: list[str]) -> None:
    repo_root = resolve_git_repo_root(target_root)
    if repo_root is None:
        return

    tracked_paths: list[str] = []
    untracked_paths: list[str] = []
    for surface in surfaces:
        target_base = target_root / get_target_subdir(SURFACES[surface], scope)
        try:
            display_path = target_base.resolve().relative_to(repo_root).as_posix()
        except ValueError:
            continue

        if is_git_tracked(repo_root, target_base):
            tracked_paths.append(display_path)
        else:
            untracked_paths.append(display_path)

    if tracked_paths:
        print(
            "Warning: export destination path(s) are already Git-tracked in "
            f"{repo_root}: {', '.join(sorted(tracked_paths))}",
            file=sys.stderr,
        )

    if untracked_paths:
        print(
            "Note: export destination path(s) are inside Git repository "
            f"{repo_root} but are not currently Git-tracked: {', '.join(sorted(untracked_paths))}",
            file=sys.stderr,
        )


def state_path_for(scope: str, target_root: Path) -> Path:
    if scope == "user":
        return target_root / STATE_FILE_NAME

    git_dir = resolve_git_dir(target_root)
    if git_dir is not None:
        return git_dir / "info" / STATE_FILE_NAME

    return target_root / ".github" / f".{STATE_FILE_NAME}"


def sync_surface(
    scope: str,
    target_root: Path,
    surface: str,
    spec: SurfaceSpec,
    previous_managed: list[str],
    dry_run: bool,
    delete_stale: bool,
) -> list[str]:
    target_base = target_root / get_target_subdir(spec, scope)
    entries = collect_entries(spec)
    current_managed = [relative_path for _, relative_path in entries]

    for source_entry, relative_path in entries:
        target_path = target_base / relative_path
        if spec["mode"] == "files":
            copy_file(source_entry, target_path, dry_run)
        else:
            copy_directory(source_entry, target_path, dry_run)

    if delete_stale:
        stale_paths = stale_paths_to_remove(previous_managed, current_managed)
        for stale_path in stale_paths:
            remove_stale_path(target_base / stale_path, dry_run)

    if entries:
        print(f"Prepared {len(entries)} {surface} entries -> {target_base}")
    else:
        print(f"No {surface} entries found under {spec['source']}")

    return current_managed


def sync_plugin_surface(
    scope: str,
    target_root: Path,
    surface: str,
    spec: SurfaceSpec,
    entries: list[tuple[Path, str]],
    previous_managed: list[str],
    dry_run: bool,
    delete_stale: bool,
) -> list[str]:
    target_base = target_root / get_target_subdir(spec, scope)
    current_managed = [relative_path for _, relative_path in entries]

    for source_entry, relative_path in entries:
        if source_entry.is_dir():
            copy_directory(source_entry, target_base / relative_path, dry_run)
        else:
            copy_file(source_entry, target_base / relative_path, dry_run)

    if delete_stale:
        stale_paths = stale_paths_to_remove(previous_managed, current_managed)
        for stale_path in stale_paths:
            remove_stale_path(target_base / stale_path, dry_run)

    if entries:
        print(f"Prepared {len(entries)} plugin-managed {surface} item(s) -> {target_base}")
    else:
        print(f"No plugin-managed {surface} entries selected")

    return current_managed


def clear_skipped_surface(
    scope: str,
    target_root: Path,
    surface: str,
    spec: SurfaceSpec,
    previous_managed: list[str],
    dry_run: bool,
    delete_stale: bool,
) -> list[str]:
    if delete_stale:
        target_base = target_root / get_target_subdir(spec, scope)
        for stale_path in sorted(set(previous_managed)):
            remove_stale_path(target_base / stale_path, dry_run)
        print(f"Skipped {surface}; removed previously managed target entries")
        return []

    print(f"Skipped {surface}; preserving previously managed target entries")
    return previous_managed


def git_exclude_block(surfaces: list[str]) -> str:
    lines = [EXCLUDE_START]
    for surface in surfaces:
        target = SURFACES[surface]["workspace_target"]
        if target is not None:
            lines.append(f"/{target}/")
    lines.append(EXCLUDE_END)
    return "\n".join(lines) + "\n"


def surfaces_with_managed_workspace_entries(managed_files: dict[str, list[str]]) -> list[str]:
    return sorted(
        surface
        for surface, entries in managed_files.items()
        if entries and SURFACES.get(surface, {}).get("workspace_target") is not None
    )


def update_git_exclude(workspace_root: Path, surfaces: list[str], dry_run: bool) -> None:
    git_dir = resolve_git_dir(workspace_root)
    if git_dir is None:
        raise FileNotFoundError(f"No .git directory found under workspace root: {workspace_root}")

    exclude_path = git_dir / "info" / "exclude"
    existing = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""

    start_index = existing.find(EXCLUDE_START)
    end_index = existing.find(EXCLUDE_END)
    if start_index != -1 and end_index != -1:
        end_index += len(EXCLUDE_END)
        trimmed = existing[:start_index].rstrip()
        suffix = existing[end_index:].lstrip("\n")
        existing = f"{trimmed}\n\n{suffix}".strip()

    block = git_exclude_block(surfaces).strip()
    updated = block if not existing else f"{existing.rstrip()}\n\n{block}"
    updated += "\n"

    if dry_run:
        print(f"Would update {exclude_path} with managed workspace export patterns")
        return

    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    exclude_path.write_text(updated, encoding="utf-8")
    print(f"Updated {exclude_path} with managed workspace export patterns")


def sync_selected_surfaces(
    args: argparse.Namespace,
    target_root: Path,
    surfaces: list[str],
    plugin_entries: dict[str, list[tuple[Path, str]]],
    state: SyncState,
) -> dict[str, list[str]]:
    updated_state: dict[str, list[str]] = dict(state["managed_files"])

    for surface in surfaces:
        if args.plugin:
            updated_state[surface] = sync_plugin_surface(
                args.scope,
                target_root,
                surface,
                SURFACES[surface],
                plugin_entries.get(surface, []),
                state["managed_files"].get(surface, []),
                args.dry_run,
                not args.no_delete_stale,
            )
        else:
            updated_state[surface] = sync_surface(
                args.scope,
                target_root,
                surface,
                SURFACES[surface],
                state["managed_files"].get(surface, []),
                args.dry_run,
                not args.no_delete_stale,
            )

    return updated_state


def warn_for_user_scope(target_root: Path) -> None:
    print(
        "Warning: user scope writes under "
        f"{target_root}. The canonical tracked sources stay under {AGENTS_ROOT}, while these "
        "user-level copies live outside the repository and are normally not Git-tracked.",
        file=sys.stderr,
    )


def warn_for_selected_surfaces(
    args: argparse.Namespace,
    target_root: Path,
    surfaces: list[str],
    skipped_native: list[str],
    skipped_authority: list[str],
) -> None:
    if args.scope == "user":
        warn_for_user_scope(target_root)

    try:
        warn_for_git_tracking(args.scope, target_root, surfaces)
    except RuntimeError as exc:
        print(f"Warning: unable to check Git tracking status: {exc}", file=sys.stderr)

    if skipped_authority:
        skipped_list = ", ".join(skipped_authority)
        print(
            "Skipping overlapping workspace runtime surfaces because runtime authority defaults to "
            f"user-level ~/.copilot: {skipped_list}"
        )

    if skipped_native:
        skipped_list = ", ".join(skipped_native)
        print(
            f"Skipping native project surfaces already readable from .agents in {target_root}: {skipped_list}"
        )


def load_plugin_entries_or_exit(
    plugin_ids: list[str], scope: str, surfaces: list[str]
) -> dict[str, list[tuple[Path, str]]] | None:
    if not plugin_ids:
        return {}

    try:
        return collect_plugin_entries(plugin_ids, scope, surfaces)
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return None


def update_git_exclude_or_exit(
    args: argparse.Namespace, target_root: Path, updated_state: dict[str, list[str]]
) -> bool:
    if not args.write_git_exclude:
        return True

    try:
        update_git_exclude(
            target_root,
            surfaces_with_managed_workspace_entries(updated_state),
            args.dry_run,
        )
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return False

    return True


def main() -> int:
    args = parse_args()
    target_root = resolve_target_root(args)

    try:
        surfaces, skipped_native, skipped_authority = selected_surfaces(
            args.scope,
            target_root,
            args.runtime_authority,
            args.surface,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    warn_for_selected_surfaces(args, target_root, surfaces, skipped_native, skipped_authority)

    if args.write_git_exclude and args.scope != "workspace":
        print("--write-git-exclude is only supported for workspace scope.", file=sys.stderr)
        return 1

    state_path = state_path_for(args.scope, target_root)
    state = load_state(state_path)
    plugin_entries = load_plugin_entries_or_exit(args.plugin, args.scope, surfaces)
    if plugin_entries is None:
        return 1

    updated_state = sync_selected_surfaces(args, target_root, surfaces, plugin_entries, state)
    for skipped_surface in sorted(set(skipped_native) | set(skipped_authority)):
        updated_state[skipped_surface] = clear_skipped_surface(
            args.scope,
            target_root,
            skipped_surface,
            SURFACES[skipped_surface],
            state["managed_files"].get(skipped_surface, []),
            args.dry_run,
            not args.no_delete_stale,
        )

    if not update_git_exclude_or_exit(args, target_root, updated_state):
        return 1

    write_state(state_path, {"managed_files": updated_state}, args.dry_run)

    if args.dry_run:
        print(f"Dry run complete for {args.scope} scope: {', '.join(surfaces)}")
    else:
        print(f"Synced {args.scope} scope surfaces: {', '.join(surfaces)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
