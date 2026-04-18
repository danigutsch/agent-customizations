---
name: mcp-servers
description: 'Design reusable MCP server assets. Use for manifests, launcher wrappers, stdio or HTTP setup guidance, host-specific adaptation notes, and portable examples.'
---

# MCP Servers

Use this skill when the task is about reusable Model Context Protocol server assets rather than one repository's one-off local setup.

## When to Use This Skill

- User wants reusable MCP server manifests or wrapper scripts
- User wants setup guidance for stdio or HTTP MCP servers
- User wants examples that show how a repo would adopt or distribute an MCP server
- User wants host-specific notes without making the asset single-host by default

## Prerequisites

- The MCP asset goal is known or can be clarified.
- The transport or runtime constraints are understood.
- The repository structure for reusable assets can be inspected.

## Workflow

### 1. Clarify the reusable asset

- Determine whether the task is about a manifest, launcher wrapper, setup note, or example asset.
- Keep reusable infrastructure separate from host-specific setup details where possible.

### 2. Keep portability explicit

- List required binaries, paths, environment variables, and transport assumptions.
- Explain what works across hosts and what still needs per-host adaptation.

### 3. Add illustrative examples

- Use examples to show how a consumer repository would adopt the asset.
- Keep placeholders obvious and avoid embedding secrets or machine-specific values.

## Related guidance

- Pair this with [Repository setup](../repository-setup/SKILL.md) when MCP assets are part of a repo baseline.
- Pair this with [CI workflows](../ci-workflows/SKILL.md) when reusable MCP assets should be validated automatically.
- Pair this with [Workflow packs](../workflow-packs/SKILL.md) when the MCP asset belongs to a broader workflow pack.

## Gotchas

- **Do not hardcode secrets or machine-specific paths**.
- **Do not assume one host is the only consumer** unless the task explicitly requires it.
- **Do not hide portability limits** behind vague documentation.

## References

- [MCP servers instructions](../../instructions/mcp-servers.instructions.md)
- [MCP servers agent](../../agents/mcp-servers.agent.md)
