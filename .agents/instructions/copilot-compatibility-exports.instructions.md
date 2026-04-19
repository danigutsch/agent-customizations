---
description: 'Guidance for canonical-to-compatible Copilot export flows, including source-of-truth rules, scope mapping, sync behavior, and generated-export handling.'
applyTo: 'docs/compatibility.md, scripts/sync_copilot*.py, scripts/configure_global_copilot_gitignore.py, .agents/agents/copilot-compatibility-exports.agent.md, .agents/skills/copilot-compatibility-exports/**'
---

# Copilot Compatibility Export Guidance

Use these rules when the task is about exporting canonical Copilot customization assets into
workspace or user-level compatibility locations.

## Core model

- Keep one canonical source of truth for reusable assets.
- Treat exported `.github/*` and `~/.copilot/*` copies as compatibility targets, not a second
  maintained authoring surface.
- Keep source-of-truth and export rules explicit in docs and scripts.

## Scope mapping

- Treat compatibility as both a **scope** decision and a **path** decision.
- Document whether a surface supports workspace scope, user scope, both, or neither.
- Do not imply support for undocumented or unstable user-level filesystem targets.
- Be explicit when a surface is configuration-driven rather than file-mirrored.

## Export behavior

- Prefer plugin-scoped export when a plugin bundle already defines the intended asset set.
- Use surface-scoped export as the lower-level fallback.
- Keep dry-run support available for inspection and troubleshooting.
- Make stale-export cleanup part of the normal sync workflow when canonical assets move or disappear.

## Generated copies

- Do not hand-edit generated exports when a canonical asset exists.
- Do not describe generated exports as canonical examples.
- Keep ignore guidance aligned with the generated-output policy.
- Warn when tracked files limit what an ignore strategy can accomplish.

## Surface-specific cautions

- Skills may already be discoverable from a native project skill root.
- Prompts are mainly workspace-scoped because stable user-level filesystem targets are not broadly
  documented.
- Repo-wide Copilot instruction files are a separate surface from slice-scoped instruction files.
- MCP assets, workflows, and plugins often need configuration or packaging guidance instead of a
  simple export mirror.

## Verification

- Confirm the documented mapping matches the actual sync script behavior.
- Confirm the supported surfaces match the targets used in exports.
- Confirm examples use existing commands rather than speculative wrappers.
- Confirm generated copies can be recreated from canonical assets without manual repair.
