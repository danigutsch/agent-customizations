#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGINS_DIR = ROOT / ".agents" / "plugins"
README_PATH = ROOT / "README.md"
START_MARKER = "<!-- BEGIN GENERATED PLUGIN CHANGELOG -->"
END_MARKER = "<!-- END GENERATED PLUGIN CHANGELOG -->"
RELEASE_HEADING_PATTERN = re.compile(
    r"^##\s+\[?(?P<version>\d+\.\d+\.\d+)\]?\s+-\s+(?P<date>\d{4}-\d{2}-\d{2})$"
)


@dataclass(frozen=True)
class PluginReleaseSummary:
    display_name: str
    plugin_id: str
    version: str
    release_date: str
    highlights: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Refresh the narrow README plugin changelog section from plugin manifests and "
            "their current released changelog entries."
        )
    )
    parser.add_argument(
        "--readme-path",
        type=Path,
        default=README_PATH,
        help="README file to update. Defaults to this repository README.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the generated README section is out of date instead of writing changes.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected a JSON object: {path}")
    return data


def resolve_repo_file(path_text: str, *, label: str) -> Path:
    candidate = Path(path_text)
    if candidate.is_absolute():
        raise RuntimeError(f"{label} must stay inside the repository root: {path_text}")

    resolved = (ROOT / candidate).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError(f"{label} must stay inside the repository root: {path_text}") from exc

    if not resolved.is_file():
        raise RuntimeError(f"{label} must resolve to an existing file: {path_text}")
    return resolved


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_plugin_summaries() -> list[PluginReleaseSummary]:
    summaries: list[PluginReleaseSummary] = []
    for manifest_path in sorted(PLUGINS_DIR.glob("*/plugin.json")):
        manifest = load_json(manifest_path)
        plugin_id = require_string(manifest, "id", manifest_path)
        display_name = require_string(manifest, "displayName", manifest_path)
        version = require_string(manifest, "version", manifest_path)
        changelog_value = require_string(manifest, "changelog", manifest_path)
        changelog_path = resolve_repo_file(changelog_value, label="Plugin changelog path")
        summaries.append(
            PluginReleaseSummary(
                display_name=display_name,
                plugin_id=plugin_id,
                version=version,
                release_date=release_date_for_version(changelog_path, version),
                highlights=release_highlights_for_version(changelog_path, version),
            )
        )
    return summaries


def require_string(manifest: dict[str, object], key: str, path: Path) -> str:
    value = manifest.get(key)
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"Expected non-empty string field '{key}' in {path}")
    return value


def changelog_lines(changelog_path: Path) -> list[str]:
    return changelog_path.read_text(encoding="utf-8").splitlines()


def release_section_lines(changelog_path: Path, version: str) -> list[str]:
    lines = changelog_lines(changelog_path)
    release_start = None

    for index, line in enumerate(lines):
        match = RELEASE_HEADING_PATTERN.match(line)
        if match is not None and match.group("version") == version:
            release_start = index
            break

    if release_start is None:
        raise RuntimeError(
            f"Could not find release heading for version {version} in {changelog_path}"
        )

    release_end = len(lines)
    for index in range(release_start + 1, len(lines)):
        if lines[index].startswith("## "):
            release_end = index
            break

    return lines[release_start:release_end]


def release_date_for_version(changelog_path: Path, version: str) -> str:
    heading = release_section_lines(changelog_path, version)[0]
    match = RELEASE_HEADING_PATTERN.match(heading)
    if match is None:
        raise RuntimeError(f"Malformed release heading for version {version} in {changelog_path}")
    return match.group("date")


def release_highlights_for_version(changelog_path: Path, version: str) -> tuple[str, ...]:
    highlights = [
        line[2:].strip()
        for line in release_section_lines(changelog_path, version)[1:]
        if line.startswith("- ")
    ]
    if not highlights:
        raise RuntimeError(
            f"Expected at least one release highlight for version {version} in {changelog_path}"
        )
    return tuple(highlights[:2])


def render_section(summaries: list[PluginReleaseSummary]) -> str:
    lines = [
        START_MARKER,
        "| Plugin | Current version | Latest release | Highlights |",
        "| --- | --- | --- | --- |",
    ]

    for summary in sorted(summaries, key=lambda item: item.display_name.casefold()):
        highlights = "<br>".join(f"- {highlight}" for highlight in summary.highlights)
        lines.append(
            f"| {summary.display_name} | `{summary.version}` | {summary.release_date} | {highlights} |"
        )

    lines.append(END_MARKER)
    return "\n".join(lines)


def replace_generated_section(readme_text: str, generated_section: str) -> str:
    start_index = readme_text.find(START_MARKER)
    end_index = readme_text.find(END_MARKER)

    if start_index == -1 or end_index == -1 or end_index < start_index:
        raise RuntimeError("README.md is missing the generated plugin changelog markers.")

    end_index += len(END_MARKER)
    return readme_text[:start_index] + generated_section + readme_text[end_index:]


def main() -> int:
    args = parse_args()
    readme_path = args.readme_path.resolve()
    readme_text = readme_path.read_text(encoding="utf-8")
    generated_section = render_section(load_plugin_summaries())
    updated_readme = replace_generated_section(readme_text, generated_section)

    if args.check:
        if updated_readme != readme_text:
            print(
                "README plugin changelog section is out of date. "
                "Run `make sync-readme-plugin-changelog`.",
                file=sys.stderr,
            )
            return 1
        print("README plugin changelog section is up to date.")
        return 0

    if updated_readme != readme_text:
        readme_path.write_text(updated_readme, encoding="utf-8")
        print(f"Updated {display_path(readme_path)}")
        return 0

    print(f"No changes needed for {display_path(readme_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
