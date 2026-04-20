#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PLUGINS_ROOT = Path(".agents/plugins")
PLUGIN_MANIFEST_NAME = "plugin.json"
UNRELEASED_HEADINGS = {"## Unreleased", "## [Unreleased]"}


@dataclass(frozen=True)
class PluginState:
    plugin_id: str
    version: str | None
    manifest_contract: str
    surface_paths: frozenset[str]
    changelog_path: str | None
    stripped_changelog: str | None


@dataclass(frozen=True)
class PluginDiffFacts:
    surface_paths: frozenset[str]
    changelog_paths: frozenset[str]
    changed_non_changelog_paths: frozenset[str]
    version_before: str | None
    version_after: str | None
    version_changed: bool
    manifest_contract_changed: bool
    changelog_changed: bool
    unreleased_only_changelog_change: bool
    distributed_surface_changed: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Require plugin bundle version bumps when a distributed bundle surface changes "
            "between two git refs."
        )
    )
    parser.add_argument("--base", required=True, help="Base git ref to compare from.")
    parser.add_argument("--head", required=True, help="Head git ref to compare to.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=ROOT,
        help="Repository root. Defaults to this repository.",
    )
    return parser.parse_args()


def git(
    repo_root: Path, *args: str, check: bool = True, allow_failure: bool = False
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    if check and completed.returncode != 0 and not allow_failure:
        stderr = completed.stderr.strip()
        command = " ".join(["git", *args])
        raise RuntimeError(f"Command failed ({command}): {stderr}")

    return completed


def resolve_compare_base(repo_root: Path, base_ref: str, head_ref: str) -> str:
    completed = git(repo_root, "merge-base", base_ref, head_ref)
    return completed.stdout.strip()


def list_plugin_ids(repo_root: Path, ref: str) -> set[str]:
    completed = git(
        repo_root,
        "ls-tree",
        "-r",
        "--name-only",
        ref,
        "--",
        PLUGINS_ROOT.as_posix(),
        allow_failure=True,
        check=False,
    )
    if completed.returncode != 0:
        return set()

    root_depth = len(PLUGINS_ROOT.parts)
    expected_depth = root_depth + 2  # plugin_id + manifest filename

    plugin_ids: set[str] = set()
    for path_text in completed.stdout.splitlines():
        path = Path(path_text)
        if len(path.parts) != expected_depth:
            continue
        if path.parts[:root_depth] != PLUGINS_ROOT.parts:
            continue
        if path.name != PLUGIN_MANIFEST_NAME:
            continue
        plugin_ids.add(path.parts[root_depth])
    return plugin_ids


def read_text_at_ref(repo_root: Path, ref: str, path_text: str) -> str | None:
    completed = git(
        repo_root,
        "show",
        f"{ref}:{path_text}",
        allow_failure=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout


def load_manifest_at_ref(repo_root: Path, ref: str, plugin_id: str) -> dict[str, Any] | None:
    manifest_path = PLUGINS_ROOT / plugin_id / PLUGIN_MANIFEST_NAME
    manifest_text = read_text_at_ref(repo_root, ref, manifest_path.as_posix())
    if manifest_text is None:
        return None

    try:
        manifest = json.loads(manifest_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Plugin manifest is not valid JSON at {ref}:{manifest_path.as_posix()}"
        ) from exc

    if not isinstance(manifest, dict):
        raise RuntimeError(
            f"Plugin manifest must be a JSON object at {ref}:{manifest_path.as_posix()}"
        )

    return manifest


def iter_manifest_content_paths(manifest: dict[str, Any]) -> set[str]:
    contents = manifest.get("contents")
    if not isinstance(contents, list):
        return set()

    paths: set[str] = set()
    for entry in contents:
        if not isinstance(entry, dict):
            continue
        path_text = entry.get("path")
        if isinstance(path_text, str):
            paths.add(path_text)
    return paths


def iter_manifest_string_list(manifest: dict[str, Any], field_name: str) -> set[str]:
    values = manifest.get(field_name)
    if not isinstance(values, list):
        return set()

    return {value for value in values if isinstance(value, str)}


def surface_paths_from_manifest(plugin_id: str, manifest: dict[str, Any]) -> frozenset[str]:
    surface_paths = iter_manifest_content_paths(manifest)
    surface_paths.update(iter_manifest_string_list(manifest, "documentation"))
    surface_paths.update(iter_manifest_string_list(manifest, "examples"))

    changelog_path = manifest.get("changelog")
    if isinstance(changelog_path, str):
        surface_paths.add(changelog_path)

    surface_paths.add((PLUGINS_ROOT / plugin_id / "README.md").as_posix())
    return frozenset(surface_paths)


def normalize_manifest_contract(manifest: dict[str, Any]) -> str:
    normalized = dict(manifest)
    normalized.pop("version", None)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"))


def strip_unreleased_section(changelog_text: str) -> str:
    lines = changelog_text.splitlines()
    stripped_lines: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        if line in UNRELEASED_HEADINGS:
            index += 1
            while index < len(lines) and not lines[index].startswith("## "):
                index += 1
            continue
        stripped_lines.append(line)
        index += 1

    return "\n".join(stripped_lines).strip()


def load_plugin_state(repo_root: Path, ref: str, plugin_id: str) -> PluginState | None:
    manifest = load_manifest_at_ref(repo_root, ref, plugin_id)
    if manifest is None:
        return None

    version = manifest.get("version")
    if version is not None and not isinstance(version, str):
        raise RuntimeError(f"Plugin version must be a string at {ref}:{plugin_id}")

    changelog_path = manifest.get("changelog")
    if changelog_path is not None and not isinstance(changelog_path, str):
        raise RuntimeError(f"Plugin changelog path must be a string at {ref}:{plugin_id}")

    changelog_text = None
    if isinstance(changelog_path, str):
        changelog_text = read_text_at_ref(repo_root, ref, changelog_path)

    return PluginState(
        plugin_id=plugin_id,
        version=version,
        manifest_contract=normalize_manifest_contract(manifest),
        surface_paths=surface_paths_from_manifest(plugin_id, manifest),
        changelog_path=changelog_path if isinstance(changelog_path, str) else None,
        stripped_changelog=(
            strip_unreleased_section(changelog_text) if changelog_text is not None else None
        ),
    )


def changed_files(repo_root: Path, base_ref: str, head_ref: str) -> set[str]:
    completed = git(repo_root, "diff", "--name-only", base_ref, head_ref, "--")
    return {line for line in completed.stdout.splitlines() if line}


def describe_paths(paths: set[str]) -> str:
    return ", ".join(sorted(paths))


def collect_surface_paths(
    base_state: PluginState | None, head_state: PluginState | None
) -> frozenset[str]:
    surface_paths: set[str] = set()
    if base_state is not None:
        surface_paths.update(base_state.surface_paths)
    if head_state is not None:
        surface_paths.update(head_state.surface_paths)
    return frozenset(surface_paths)


def collect_changelog_paths(
    base_state: PluginState | None, head_state: PluginState | None
) -> frozenset[str]:
    paths = {
        path
        for path in (
            base_state.changelog_path if base_state is not None else None,
            head_state.changelog_path if head_state is not None else None,
        )
        if path is not None
    }
    return frozenset(paths)


def has_unreleased_only_changelog_change(
    base_state: PluginState | None, head_state: PluginState | None, changelog_changed: bool
) -> bool:
    if not changelog_changed or base_state is None or head_state is None:
        return False
    return base_state.stripped_changelog == head_state.stripped_changelog


def has_distributed_surface_change(
    base_state: PluginState | None,
    head_state: PluginState | None,
    manifest_contract_changed: bool,
    changed_non_changelog_paths: frozenset[str],
    changelog_changed: bool,
    unreleased_only_changelog_change: bool,
) -> bool:
    return (
        base_state is None
        or head_state is None
        or manifest_contract_changed
        or bool(changed_non_changelog_paths)
        or (changelog_changed and not unreleased_only_changelog_change)
    )


def collect_plugin_diff_facts(
    base_state: PluginState | None, head_state: PluginState | None, diff_paths: set[str]
) -> PluginDiffFacts:
    surface_paths = collect_surface_paths(base_state, head_state)
    changelog_paths = collect_changelog_paths(base_state, head_state)
    changed_non_changelog_paths = frozenset((diff_paths & surface_paths) - changelog_paths)

    version_before = base_state.version if base_state is not None else None
    version_after = head_state.version if head_state is not None else None
    manifest_contract_before = base_state.manifest_contract if base_state is not None else None
    manifest_contract_after = head_state.manifest_contract if head_state is not None else None

    changelog_changed = bool(diff_paths & changelog_paths)
    unreleased_only_changelog_change = has_unreleased_only_changelog_change(
        base_state, head_state, changelog_changed
    )
    manifest_contract_changed = manifest_contract_before != manifest_contract_after

    return PluginDiffFacts(
        surface_paths=surface_paths,
        changelog_paths=changelog_paths,
        changed_non_changelog_paths=changed_non_changelog_paths,
        version_before=version_before,
        version_after=version_after,
        version_changed=version_before != version_after,
        manifest_contract_changed=manifest_contract_changed,
        changelog_changed=changelog_changed,
        unreleased_only_changelog_change=unreleased_only_changelog_change,
        distributed_surface_changed=has_distributed_surface_change(
            base_state,
            head_state,
            manifest_contract_changed,
            changed_non_changelog_paths,
            changelog_changed,
            unreleased_only_changelog_change,
        ),
    )


def version_bump_reasons(
    base_state: PluginState | None, head_state: PluginState | None, facts: PluginDiffFacts
) -> list[str]:
    reasons: list[str] = []
    if facts.manifest_contract_changed:
        reasons.append("plugin manifest contract changed")
    if facts.changed_non_changelog_paths:
        reasons.append(
            f"shipped files changed: {describe_paths(set(facts.changed_non_changelog_paths))}"
        )
    if facts.changelog_changed and not facts.unreleased_only_changelog_change:
        reasons.append("released changelog content changed outside Unreleased")
    if base_state is None:
        reasons.append("plugin bundle was added")
    if head_state is None:
        reasons.append("plugin bundle was removed")
    return reasons


def check_plugin(
    plugin_id: str,
    base_state: PluginState | None,
    head_state: PluginState | None,
    diff_paths: set[str],
) -> list[str]:
    errors: list[str] = []

    if base_state is None and head_state is None:
        return errors

    facts = collect_plugin_diff_facts(base_state, head_state, diff_paths)

    if facts.distributed_surface_changed and not facts.version_changed:
        reasons = version_bump_reasons(base_state, head_state, facts)
        reason_text = "; ".join(reasons) if reasons else "distributed plugin surface changed"
        errors.append(
            f"{plugin_id}: distributed surface changed without a version bump ({reason_text})."
        )

    if facts.version_changed and not facts.changelog_changed:
        errors.append(
            f"{plugin_id}: version changed from {facts.version_before or '<missing>'} to "
            f"{facts.version_after or '<missing>'} without a changelog update."
        )

    return errors


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    compare_base = resolve_compare_base(repo_root, args.base, args.head)
    diff_paths = changed_files(repo_root, compare_base, args.head)

    plugin_ids = list_plugin_ids(repo_root, compare_base) | list_plugin_ids(repo_root, args.head)
    errors: list[str] = []

    for plugin_id in sorted(plugin_ids):
        base_state = load_plugin_state(repo_root, compare_base, plugin_id)
        head_state = load_plugin_state(repo_root, args.head, plugin_id)
        errors.extend(check_plugin(plugin_id, base_state, head_state, diff_paths))

    if errors:
        print("Plugin version bump guard failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Plugin version bump guard passed "
        f"({compare_base}..{args.head}, checked {len(plugin_ids)} plugin bundle(s))."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
