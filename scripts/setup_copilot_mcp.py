#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TypedDict, cast

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COPILOT_ROOT = Path.home() / ".copilot"
DEFAULT_MANIFEST_ROOT = ROOT / ".agents" / "mcp" / "mcp-servers"
CONFIG_FILE_NAME = "mcp-config.json"


class ManifestData(TypedDict, total=False):
    name: str
    transport: str
    type: str
    command: str
    args: list[str]
    env: dict[str, str]
    url: str
    headers: dict[str, str]
    tools: list[str]
    notes: list[str]


class RenderedServer(TypedDict, total=False):
    type: str
    command: str
    args: list[str]
    env: dict[str, str]
    url: str
    headers: dict[str, str]
    tools: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install or update Copilot CLI MCP server configuration from reusable repo manifests."
    )
    parser.add_argument(
        "--manifest-root",
        type=Path,
        default=DEFAULT_MANIFEST_ROOT,
        help="Directory containing reusable MCP manifest files. Defaults to .agents/mcp/mcp-servers.",
    )
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        type=Path,
        help="Specific manifest file to install. Can be repeated. Defaults to all non-example manifests under --manifest-root.",
    )
    parser.add_argument(
        "--include-examples",
        action="store_true",
        help="Include *.example.json manifests during automatic discovery.",
    )
    parser.add_argument(
        "--copilot-root",
        type=Path,
        default=DEFAULT_COPILOT_ROOT,
        help="Copilot home directory. Defaults to ~/.copilot.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned config changes without writing ~/.copilot/mcp-config.json.",
    )
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path.expanduser().resolve()
    return (ROOT / path).resolve()


def discover_manifests(manifest_root: Path, include_examples: bool) -> list[Path]:
    manifests = sorted(path for path in manifest_root.glob("*.json") if path.is_file())
    if include_examples:
        return manifests
    return [path for path in manifests if not path.name.endswith(".example.json")]


def selected_manifests(args: argparse.Namespace) -> list[Path]:
    if args.manifest:
        manifests = [resolve_path(path) for path in args.manifest]
    else:
        manifests = discover_manifests(resolve_path(args.manifest_root), args.include_examples)

    if not manifests:
        raise RuntimeError(
            "No installable MCP manifests found. Add a concrete .json manifest under "
            ".agents/mcp/mcp-servers/ or pass --manifest for a specific file."
        )

    seen: set[Path] = set()
    unique_manifests: list[Path] = []
    for manifest in manifests:
        if manifest in seen:
            continue
        if not manifest.exists():
            raise RuntimeError(f"MCP manifest not found: {manifest}")
        unique_manifests.append(manifest)
        seen.add(manifest)
    return unique_manifests


def load_manifest(path: Path) -> ManifestData:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise RuntimeError(f"MCP manifest must be a JSON object: {path}")

    raw_data = cast(dict[object, object], data)
    manifest = cast(ManifestData, raw_data)
    return manifest


def require_string(value: object, field_name: str, path: Path) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"{field_name} must be a non-empty string in {path}")
    return value


def require_string_list(value: object, field_name: str, path: Path) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise RuntimeError(f"{field_name} must be a list of strings in {path}")
    return list(cast(list[str], value))


def optional_string_dict(value: object, field_name: str, path: Path) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise RuntimeError(f"{field_name} must be an object with string values in {path}")

    typed: dict[str, str] = {}
    for key, item in cast(dict[object, object], value).items():
        if not isinstance(key, str) or not isinstance(item, str):
            raise RuntimeError(
                f"{field_name} must be an object with string keys and values in {path}"
            )
        typed[key] = item
    return typed


def optional_string_list(
    value: object,
    field_name: str,
    path: Path,
    *,
    default: list[str],
) -> list[str]:
    if value is None:
        return list(default)
    return require_string_list(value, field_name, path)


def normalize_transport(value: str) -> str:
    transport = value.strip().lower()
    if transport not in {"local", "stdio", "http", "sse"}:
        raise RuntimeError(f"Unsupported MCP transport/type: {value}")
    return transport


def render_server_config(
    manifest: ManifestData, path: Path
) -> tuple[str, RenderedServer, list[str]]:
    name = require_string(manifest.get("name"), "name", path)
    transport = normalize_transport(
        require_string(manifest.get("transport") or manifest.get("type"), "transport", path)
    )
    tools = optional_string_list(manifest.get("tools"), "tools", path, default=["*"])
    notes = (
        optional_string_list(manifest.get("notes"), "notes", path, default=[])
        if "notes" in manifest
        else []
    )

    rendered: RenderedServer = {
        "type": transport,
        "tools": tools,
    }

    if transport in {"local", "stdio"}:
        rendered["command"] = require_string(manifest.get("command"), "command", path)
        rendered["args"] = require_string_list(manifest.get("args", []), "args", path)
        rendered["env"] = optional_string_dict(manifest.get("env"), "env", path)
    else:
        rendered["url"] = require_string(manifest.get("url"), "url", path)
        rendered["headers"] = optional_string_dict(manifest.get("headers"), "headers", path)

    return name, rendered, notes


def load_existing_config(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"mcpServers": {}}

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise RuntimeError(f"Copilot MCP config must be a JSON object: {path}")

    config = cast(dict[str, object], data)
    servers = config.get("mcpServers")
    if servers is None:
        config["mcpServers"] = {}
        return config
    if not isinstance(servers, dict):
        raise RuntimeError(f"mcpServers must be a JSON object in {path}")
    return config


def write_config(path: Path, config: dict[str, object], dry_run: bool) -> None:
    if dry_run:
        print(f"Would write Copilot MCP config to {path}")
        print(json.dumps(config, indent=2))
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2)
        handle.write("\n")
    print(f"Updated Copilot MCP config at {path}")


def warn_for_user_level_config(path: Path) -> None:
    print(
        "Warning: MCP setup writes to "
        f"{path}. This is user-level configuration outside the repository and is normally not "
        "Git-tracked.",
        file=sys.stderr,
    )


def main() -> int:
    args = parse_args()
    config_path = args.copilot_root.expanduser().resolve() / CONFIG_FILE_NAME
    warn_for_user_level_config(config_path)

    try:
        manifests = selected_manifests(args)
        config = load_existing_config(config_path)
        servers = cast(dict[str, object], config["mcpServers"])
    except (RuntimeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    applied_notes: list[tuple[str, list[str]]] = []
    changed_names: list[str] = []

    try:
        for manifest_path in manifests:
            manifest = load_manifest(manifest_path)
            name, rendered, notes = render_server_config(manifest, manifest_path)
            current = servers.get(name)
            if current != rendered:
                servers[name] = rendered
                changed_names.append(name)
                print(f"Prepared MCP server '{name}' from {manifest_path.relative_to(ROOT)}")
            else:
                print(
                    f"MCP server '{name}' is already up to date from {manifest_path.relative_to(ROOT)}"
                )

            if notes:
                applied_notes.append((name, notes))
    except (RuntimeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    write_config(config_path, config, args.dry_run)

    if changed_names:
        print(f"Configured MCP servers: {', '.join(changed_names)}")
    else:
        print("No MCP server changes were needed")

    for name, notes in applied_notes:
        print(f"Notes for {name}:")
        for note in notes:
            print(f"  - {note}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
