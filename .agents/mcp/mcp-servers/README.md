# MCP servers assets

Reusable MCP server assets for the `mcp-servers` slice live here.

## Contents

- `stdio-python-server.example.json` — starter example reusable MCP server manifest shape

## Notes

- Keep secrets and machine-specific paths out of committed assets.
- Treat examples as adaptation starters, not universal drop-in configs.
- Keep transport, runtime, and host assumptions explicit so consumers can adapt them intentionally.
