# MCP servers assets

Reusable MCP server assets for the `mcp-servers` slice live here.

## Contents

- `stdio-python-server.example.json` — starter stdio manifest shape for a portable local Python MCP server

## Setup with script

This repository's local setup path for Copilot CLI MCP servers is script-first.

1. Copy an example manifest to a concrete `.json` file and replace the placeholder values.
2. Run the setup script or `make` target to merge that manifest into `~/.copilot/mcp-config.json`.

```bash
cp .agents/mcp/mcp-servers/stdio-python-server.example.json \
  .agents/mcp/mcp-servers/my-python-server.json
python3 scripts/setup_copilot_mcp.py --manifest .agents/mcp/mcp-servers/my-python-server.json
```

Or use the `Makefile` entrypoint:

```bash
make setup-mcp MANIFEST=.agents/mcp/mcp-servers/my-python-server.json
```

If you omit `--manifest`, the setup script discovers all non-example `.json` manifests under this
folder and installs or updates them together.

## Notes

- Keep secrets and machine-specific paths out of committed assets.
- Treat examples as adaptation starters, not universal drop-in configs.
- Keep transport, runtime, and host assumptions explicit so consumers can adapt them intentionally.
