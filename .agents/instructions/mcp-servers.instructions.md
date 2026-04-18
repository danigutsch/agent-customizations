---
description: 'Standards for reusable MCP server manifests, wrappers, setup notes, and portability guidance.'
applyTo: '.agents/mcp/**/*, **/mcp*.json, **/.mcp.json, docs/**/*.md, README.md, scripts/**/*'
---

# MCP Servers Standards

Use these rules when the task is about creating or refining reusable MCP server assets.

## Scope and purpose

- Treat reusable MCP assets as infrastructure guidance, not one-off machine setup.
- Keep transport, runtime, and host assumptions explicit.
- Separate reusable manifests or wrappers from product-specific examples.

## Asset design

- Prefer explicit manifests, wrapper scripts, and setup notes over undocumented conventions.
- Keep launcher commands, required binaries, and environment variables clear.
- Use example values only when they are obviously placeholders.
- Keep secrets and machine-specific paths out of committed reusable assets.

## Portability

- Document which parts are portable across hosts and which need host-specific adaptation.
- Avoid naming that assumes one AI platform if the asset is conceptually reusable.
- Keep host-specific examples in example files or docs instead of baking them into the reusable asset itself.

## Maintenance

- Make the consumer-facing setup path easy to inspect and copy.
- Prefer lightweight examples that demonstrate intent without adding fragile runtime assumptions.
- Align reusable MCP assets with the repository's general source-of-truth rules.

## Verification

- Confirm assets do not require hidden local state.
- Confirm paths and environment variables are clear and shareable.
- Confirm examples stay obviously illustrative rather than pretending to be universally plug-and-play.
