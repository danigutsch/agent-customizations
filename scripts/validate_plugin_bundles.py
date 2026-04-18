#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import TypeGuard, TypedDict, cast


class PluginSchema(TypedDict):
    required: list[str]
    properties: dict[str, object]


class InstallConfig(TypedDict, total=False):
    strategy: str
    layoutRoot: str
    notes: list[str]


class ContentEntry(TypedDict, total=False):
    path: str
    kind: str
    required: bool
    description: str


class PluginManifest(TypedDict, total=False):
    schemaVersion: str
    id: str
    version: str
    displayName: str
    description: str
    bundleType: str
    tags: list[str]
    maturity: str
    install: InstallConfig
    contents: list[ContentEntry]
    documentation: list[str]
    examples: list[str]
    changelog: str
    dependencies: list[dict[str, object]]
    compatibility: dict[str, object]


ROOT = Path(__file__).resolve().parents[1]
PLUGINS_DIR = ROOT / ".agents" / "plugins"
SCHEMA_PATH = PLUGINS_DIR / "plugin-bundle.schema.json"
PLUGIN_MANIFEST_NAME = "plugin.json"
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
PLUGIN_ID_PATTERN = re.compile(r"^[a-z0-9-]+$")
VALID_CONTENT_KINDS = {
    "agent",
    "instruction",
    "skill",
    "reference",
    "prompt",
    "hook",
    "mcp",
    "workflow",
    "asset",
    "doc",
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def relative_path_text(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def resolve_repo_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        raise ValueError(f"paths must be repository-relative, got absolute path: {path_text}")
    resolved = (ROOT / path).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"paths must stay inside the repository root: {path_text}") from exc
    return resolved


def add_error(errors: list[str], plugin_name: str, message: str) -> None:
    errors.append(f"{plugin_name}: {message}")


def is_string_list(value: object) -> TypeGuard[list[str]]:
    if not isinstance(value, list):
        return False

    items = cast(list[object], value)
    return all(isinstance(item, str) for item in items)


def is_string_key_dict(value: object) -> TypeGuard[dict[str, object]]:
    if not isinstance(value, dict):
        return False

    mapping = cast(dict[object, object], value)
    return all(isinstance(key, str) for key in mapping)


def as_plugin_schema(value: object) -> PluginSchema | None:
    if not is_string_key_dict(value):
        return None

    required = value.get("required")
    properties = value.get("properties")
    if not is_string_list(required) or not is_string_key_dict(properties):
        return None

    return cast(PluginSchema, value)


def as_plugin_manifest(value: object) -> PluginManifest | None:
    if not is_string_key_dict(value):
        return None

    return cast(PluginManifest, value)


def validate_required_fields(
    plugin_name: str,
    manifest: PluginManifest,
    schema: PluginSchema,
    errors: list[str],
) -> None:
    required_fields = set(schema["required"])
    allowed_fields = set(schema["properties"].keys())

    missing = sorted(required_fields - set(manifest.keys()))
    unexpected = sorted(set(manifest.keys()) - allowed_fields)

    for field in missing:
        add_error(errors, plugin_name, f"missing required field '{field}'")
    for field in unexpected:
        add_error(errors, plugin_name, f"unexpected field '{field}'")


def validate_scalar_fields(plugin_name: str, manifest: PluginManifest, errors: list[str]) -> None:
    plugin_id = manifest.get("id")
    version = manifest.get("version")
    schema_version = manifest.get("schemaVersion")
    bundle_type = manifest.get("bundleType")
    maturity = manifest.get("maturity")

    if not isinstance(plugin_id, str) or not PLUGIN_ID_PATTERN.fullmatch(plugin_id):
        add_error(errors, plugin_name, "field 'id' must match ^[a-z0-9-]+$")
    if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
        add_error(errors, plugin_name, "field 'version' must match semantic version format X.Y.Z")
    if not isinstance(schema_version, str) or not SEMVER_PATTERN.fullmatch(schema_version):
        add_error(errors, plugin_name, "field 'schemaVersion' must match semantic version format X.Y.Z")
    if bundle_type != "capability-pack":
        add_error(errors, plugin_name, "field 'bundleType' must be 'capability-pack'")
    if maturity is not None and maturity not in {"experimental", "beta", "stable"}:
        add_error(errors, plugin_name, "field 'maturity' must be experimental, beta, or stable")


def validate_install(plugin_name: str, manifest: PluginManifest, errors: list[str]) -> None:
    install = manifest.get("install")
    if install is None:
        add_error(errors, plugin_name, "field 'install' must be an object")
        return

    if install.get("strategy") != "copy-files":
        add_error(errors, plugin_name, "install.strategy must be 'copy-files'")
    if not isinstance(install.get("layoutRoot"), str) or not install.get("layoutRoot"):
        add_error(errors, plugin_name, "install.layoutRoot must be a non-empty string")
    notes = cast(object, install.get("notes"))
    if notes is not None and not is_string_list(notes):
        add_error(errors, plugin_name, "install.notes must be an array when provided")


def validate_path_list(
    plugin_name: str,
    field_name: str,
    values: list[str] | None,
    errors: list[str],
    referenced_plugin_files: set[Path],
) -> None:
    if not values:
        add_error(errors, plugin_name, f"field '{field_name}' must be a non-empty array")
        return

    seen: set[str] = set()
    for value in values:
        if value in seen:
            add_error(errors, plugin_name, f"field '{field_name}' contains duplicate path '{value}'")
            continue
        seen.add(value)
        try:
            resolved = resolve_repo_path(value)
        except ValueError as exc:
            add_error(errors, plugin_name, str(exc))
            continue
        if not resolved.exists():
            add_error(errors, plugin_name, f"{field_name} path does not exist: {value}")
            continue
        if resolved.is_file() and PLUGINS_DIR in resolved.parents:
            referenced_plugin_files.add(resolved)


def validate_contents(
    plugin_name: str,
    manifest: PluginManifest,
    errors: list[str],
) -> None:
    contents = manifest.get("contents")
    if not contents:
        add_error(errors, plugin_name, "field 'contents' must be a non-empty array")
        return

    seen_paths: set[str] = set()
    for entry in contents:
        validate_contents_entry(plugin_name, entry, seen_paths, errors)


def validate_contents_entry(
    plugin_name: str,
    entry: ContentEntry,
    seen_paths: set[str],
    errors: list[str],
) -> None:
    path_text = entry.get("path")
    if not isinstance(path_text, str):
        add_error(errors, plugin_name, "each contents entry needs a string 'path'")
        return

    if path_text in seen_paths:
        add_error(errors, plugin_name, f"contents contains duplicate path '{path_text}'")
        return
    seen_paths.add(path_text)

    validate_contents_metadata(plugin_name, entry, path_text, errors)
    validate_contents_path(plugin_name, path_text, errors)


def validate_contents_metadata(
    plugin_name: str,
    entry: ContentEntry,
    path_text: str,
    errors: list[str],
) -> None:
    kind = entry.get("kind")
    required = entry.get("required")

    if kind not in VALID_CONTENT_KINDS:
        add_error(errors, plugin_name, f"contents kind is invalid for path '{path_text}'")

    if not isinstance(required, bool):
        add_error(errors, plugin_name, f"contents.required must be boolean for path '{path_text}'")


def validate_contents_path(
    plugin_name: str,
    path_text: str,
    errors: list[str],
) -> None:
    try:
        resolved = resolve_repo_path(path_text)
    except ValueError as exc:
        add_error(errors, plugin_name, str(exc))
        return

    if not resolved.exists():
        add_error(errors, plugin_name, f"contents path does not exist: {path_text}")


def validate_changelog(
    plugin_name: str,
    manifest: PluginManifest,
    errors: list[str],
    referenced_plugin_files: set[Path],
) -> None:
    changelog = manifest.get("changelog")
    if changelog is None:
        return

    try:
        changelog_path = resolve_repo_path(changelog)
    except ValueError as exc:
        add_error(errors, plugin_name, str(exc))
        return

    if not changelog_path.exists():
        add_error(errors, plugin_name, f"changelog path does not exist: {changelog}")
        return

    referenced_plugin_files.add(changelog_path)
    changelog_text = changelog_path.read_text(encoding="utf-8")
    version = manifest.get("version")

    if "## Unreleased" not in changelog_text and "## [Unreleased]" not in changelog_text:
        add_error(errors, plugin_name, "changelog must contain an 'Unreleased' section")
    if (
        isinstance(version, str)
        and f"## {version}" not in changelog_text
        and f"## [{version}]" not in changelog_text
    ):
        add_error(errors, plugin_name, f"changelog must contain a section for version {version}")


def validate_plugin_directory(
    plugin_dir: Path,
    manifest: PluginManifest,
    errors: list[str],
) -> None:
    plugin_name = plugin_dir.name
    plugin_id = manifest.get("id")
    referenced_plugin_files: set[Path] = {plugin_dir / PLUGIN_MANIFEST_NAME}

    if plugin_id != plugin_name:
        add_error(errors, plugin_name, f"plugin id '{plugin_id}' must match directory name '{plugin_name}'")

    readme_path = plugin_dir / "README.md"
    examples_dir = plugin_dir / "examples"

    if not readme_path.exists():
        add_error(errors, plugin_name, "plugin directory must contain README.md")
    else:
        referenced_plugin_files.add(readme_path)

    if not examples_dir.exists() or not examples_dir.is_dir():
        add_error(errors, plugin_name, "plugin directory must contain an examples/ folder")

    validate_path_list(plugin_name, "documentation", manifest.get("documentation"), errors, referenced_plugin_files)
    validate_path_list(plugin_name, "examples", manifest.get("examples"), errors, referenced_plugin_files)
    validate_changelog(plugin_name, manifest, errors, referenced_plugin_files)

    for plugin_file in plugin_dir.rglob("*"):
        if not plugin_file.is_file():
            continue
        if plugin_file.name == PLUGIN_MANIFEST_NAME:
            continue
        if plugin_file not in referenced_plugin_files:
            add_error(
                errors,
                plugin_name,
                f"plugin file is not referenced by documentation, examples, or changelog: {relative_path_text(plugin_file)}",
            )


def validate_manifest(plugin_dir: Path, schema: PluginSchema, errors: list[str]) -> None:
    plugin_name = plugin_dir.name
    manifest_path = plugin_dir / PLUGIN_MANIFEST_NAME

    if not manifest_path.exists():
        add_error(errors, plugin_name, f"plugin directory is missing {PLUGIN_MANIFEST_NAME}")
        return

    try:
        manifest_data = load_json(manifest_path)
    except json.JSONDecodeError as exc:
        add_error(errors, plugin_name, f"{PLUGIN_MANIFEST_NAME} is not valid JSON: {exc}")
        return

    manifest = as_plugin_manifest(manifest_data)
    if manifest is None:
        add_error(errors, plugin_name, "plugin.json root must be an object")
        return

    validate_required_fields(plugin_name, manifest, schema, errors)
    validate_scalar_fields(plugin_name, manifest, errors)
    validate_install(plugin_name, manifest, errors)
    validate_contents(plugin_name, manifest, errors)
    validate_plugin_directory(plugin_dir, manifest, errors)


def main() -> int:
    try:
        schema_data = load_json(SCHEMA_PATH)
    except FileNotFoundError:
        print(f"Schema file not found: {SCHEMA_PATH}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"Schema file is not valid JSON: {exc}", file=sys.stderr)
        return 1

    schema = as_plugin_schema(schema_data)
    if schema is None:
        print(f"Schema file does not match the expected top-level shape: {SCHEMA_PATH}", file=sys.stderr)
        return 1

    plugin_dirs = sorted(
        path
        for path in PLUGINS_DIR.iterdir()
        if path.is_dir() and (path / PLUGIN_MANIFEST_NAME).exists()
    )

    if not plugin_dirs:
        print("No plugin bundles found.")
        return 0

    errors: list[str] = []
    for plugin_dir in plugin_dirs:
        validate_manifest(plugin_dir, schema, errors)

    if errors:
        print("Plugin bundle validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(plugin_dirs)} plugin bundle(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
