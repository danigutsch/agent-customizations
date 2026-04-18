---
description: 'Design or refine reusable MCP server assets, wrappers, and setup guidance.'
name: 'mcp-servers'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the MCP server asset, transport, hosts to support, and what reusable guidance is needed.'
---

# MCP Servers

## Mission

Use the `mcp-servers` slice to create or refine reusable MCP server assets and setup guidance.

## Scope & Preconditions

- Use this prompt when the task is about reusable MCP server manifests, wrappers, setup notes, or examples.
- Inspect the current repository structure and existing compatibility assets before proposing changes.
- Keep portability and host-specific limits explicit.

## Inputs

- Asset goal: ${input:goal:What reusable MCP asset or guidance should be created?}
- Transport/runtime: ${input:transport:What transport or runtime constraints matter?}
- Target hosts: ${input:hosts:Which hosts or clients should the asset support?}

## Workflow

1. Inspect the current MCP asset layout, if any.
2. Clarify whether the work is about manifests, wrappers, setup docs, or example assets.
3. Apply the `mcp-servers` guidance together:
   - `../agents/mcp-servers.agent.md`
   - `../instructions/mcp-servers.instructions.md`
   - `../skills/mcp-servers/SKILL.md`
4. Pair with adjacent slices when relevant:
   - `../skills/repository-setup/SKILL.md`
   - `../skills/ci-workflows/SKILL.md`
   - `../skills/workflow-packs/SKILL.md`
5. Keep reusable assets separate from host-specific examples where possible.

## Output Expectations

- Summarize the reusable MCP asset being created or changed.
- Describe host-specific assumptions and limits.
- Show the asset, wrapper, or documentation changes.
- Include validation or maintenance notes when relevant.

## Quality Assurance

- Do not hardcode secrets or machine-local paths.
- Do not pretend one host-specific config is universally portable.
- Keep examples obviously illustrative.
