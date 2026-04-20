#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ID_PATTERN = re.compile(r"^[a-z0-9-]+$")
VERSION_HEADING_PREFIXES = ("## ", "## [")


@dataclass(frozen=True)
class ReleaseResult:
    plugin_id: str
    previous_version: str
    next_version: str
    tag_name: str
    manifest_path: Path
    changelog_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare a plugin bundle release by bumping the manifest version and promoting the "
            "changelog's Unreleased section."
        )
    )
    parser.add_argument(
        "--plugin", required=True, help="Plugin id / directory name under .agents/plugins."
    )
    parser.add_argument(
        "--bump",
        required=True,
        choices=["major", "minor", "patch"],
        help="Semantic version bump to apply.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=ROOT,
        help="Repository root. Defaults to this repository.",
    )
    parser.add_argument(
        "--release-date",
        default=datetime.now(UTC).date().isoformat(),
        help="Release date to record in the changelog. Defaults to today's UTC date.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the next version and tag without writing files.",
    )
    parser.add_argument(
        "--github-output",
        type=Path,
        help="Optional GITHUB_OUTPUT path for workflow outputs.",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise RuntimeError(f"Plugin manifest must be a JSON object: {path}")
    return data


def resolve_plugin_dir(repo_root: Path, plugin_id: str) -> Path:
    if not PLUGIN_ID_PATTERN.fullmatch(plugin_id):
        raise RuntimeError("Plugin id must match ^[a-z0-9-]+$.")

    plugins_dir = (repo_root / ".agents" / "plugins").resolve()
    plugin_dir = (plugins_dir / plugin_id).resolve()

    try:
        plugin_dir.relative_to(plugins_dir)
    except ValueError as exc:
        raise RuntimeError(
            f"Plugin id '{plugin_id}' resolves outside the plugin directory: {plugin_dir}"
        ) from exc

    return plugin_dir


def parse_version(version: str) -> tuple[int, int, int]:
    try:
        major_text, minor_text, patch_text = version.split(".")
        return int(major_text), int(minor_text), int(patch_text)
    except ValueError as exc:
        raise RuntimeError(f"Unsupported semantic version: {version}") from exc


def bump_version(version: str, bump: str) -> str:
    major, minor, patch = parse_version(version)
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def trim_blank_edges(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def trim_leading_blanks(lines: list[str]) -> list[str]:
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    return lines[index:]


def release_heading(next_version: str, changelog_text: str, release_date: str) -> str:
    if "## [" in changelog_text:
        return f"## [{next_version}] - {release_date}"
    return f"## {next_version} - {release_date}"


def promote_unreleased(changelog_path: Path, next_version: str, release_date: str) -> str:
    changelog_text = changelog_path.read_text(encoding="utf-8")
    lines = changelog_text.splitlines()

    unreleased_index = None
    for index, line in enumerate(lines):
        if line in {"## Unreleased", "## [Unreleased]"}:
            unreleased_index = index
            break
    if unreleased_index is None:
        raise RuntimeError(f"Changelog is missing an Unreleased section: {changelog_path}")

    next_section_index = len(lines)
    for index in range(unreleased_index + 1, len(lines)):
        if lines[index].startswith(VERSION_HEADING_PREFIXES):
            next_section_index = index
            break

    unreleased_body = trim_blank_edges(lines[unreleased_index + 1 : next_section_index])
    if not unreleased_body:
        raise RuntimeError(
            f"Changelog Unreleased section has no release notes to promote: {changelog_path}"
        )

    new_heading = release_heading(next_version, changelog_text, release_date)
    new_lines = lines[: unreleased_index + 1]
    new_lines.extend(["", new_heading, ""])
    new_lines.extend(unreleased_body)

    remaining_lines = trim_leading_blanks(lines[next_section_index:])
    if remaining_lines:
        new_lines.append("")
        new_lines.extend(remaining_lines)

    return "\n".join(new_lines) + "\n"


def prepare_release(
    repo_root: Path,
    plugin_id: str,
    bump: str,
    release_date: str,
    *,
    dry_run: bool,
) -> ReleaseResult:
    plugin_dir = resolve_plugin_dir(repo_root, plugin_id)
    manifest_path = plugin_dir / "plugin.json"
    changelog_path = plugin_dir / "CHANGELOG.md"

    if not manifest_path.exists():
        raise RuntimeError(f"Plugin manifest not found: {manifest_path}")
    if not changelog_path.exists():
        raise RuntimeError(f"Plugin changelog not found: {changelog_path}")

    manifest = load_manifest(manifest_path)
    manifest_plugin_id = manifest.get("id")
    if manifest_plugin_id != plugin_id:
        raise RuntimeError(
            f"Plugin manifest id '{manifest_plugin_id}' does not match requested plugin '{plugin_id}'"
        )

    previous_version = manifest.get("version")
    if not isinstance(previous_version, str):
        raise RuntimeError(f"Plugin manifest version must be a string: {manifest_path}")

    next_version = bump_version(previous_version, bump)
    tag_name = f"plugins/{plugin_id}/v{next_version}"
    new_changelog_text = promote_unreleased(changelog_path, next_version, release_date)

    if not dry_run:
        manifest["version"] = next_version
        manifest_path.write_text(f"{json.dumps(manifest, indent=2)}\n", encoding="utf-8")
        changelog_path.write_text(new_changelog_text, encoding="utf-8")

    return ReleaseResult(
        plugin_id=plugin_id,
        previous_version=previous_version,
        next_version=next_version,
        tag_name=tag_name,
        manifest_path=manifest_path,
        changelog_path=changelog_path,
    )


def write_github_output(path: Path, result: ReleaseResult) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"plugin={result.plugin_id}\n")
        handle.write(f"previous_version={result.previous_version}\n")
        handle.write(f"version={result.next_version}\n")
        handle.write(f"tag={result.tag_name}\n")
        handle.write(f"manifest_path={result.manifest_path.as_posix()}\n")
        handle.write(f"changelog_path={result.changelog_path.as_posix()}\n")


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    result = prepare_release(
        repo_root,
        args.plugin,
        args.bump,
        args.release_date,
        dry_run=args.dry_run,
    )

    if args.github_output is not None:
        write_github_output(args.github_output, result)

    print(f"plugin={result.plugin_id}")
    print(f"previous_version={result.previous_version}")
    print(f"version={result.next_version}")
    print(f"tag={result.tag_name}")
    print(f"manifest_path={result.manifest_path.as_posix()}")
    print(f"changelog_path={result.changelog_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
