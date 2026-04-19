---
name: copilot-compatibility-exports
description: Guidance for syncing canonical `.agents` assets into Copilot-compatible `.github/*` and `~/.copilot/*` targets. Use when mapping agents, instructions, prompts, skills, or hooks across user versus workspace scope, skipping native project surfaces, choosing plugin-driven export selection, or troubleshooting export drift and stale generated copies.
---

# Copilot Compatibility Exports

Use this skill when the task is about how canonical assets are exported for Copilot compatibility
rather than how those assets are authored.

## When to Use This Skill

- The user needs to map canonical `.agents` assets into `.github/*` or `~/.copilot/*`
- The user needs to choose between workspace and user export scope
- The user needs to understand which surfaces are supported for export
- The user needs guidance on skipping native project surfaces like `.agents/skills/`
- The user needs plugin-driven export selection
- The user needs troubleshooting for stale generated copies or sync drift

## Prerequisites

- The canonical source surface can be inspected under `.agents/`.
- The export script or compatibility docs can be inspected.
- The task is about compatibility exports, not about plugin packaging alone or tool-generated file
  provenance alone.

## Workflow

### 1. Confirm the canonical source and target scope

- Start from the canonical `.agents` surface.
- Decide whether the target is workspace scope or user scope.

### 2. Apply the supported surface mapping

- Map the surface to the correct `.github/*` or `~/.copilot/*` target only when that export is
  supported.
- Keep exceptions explicit for surfaces that are not simple file mirrors.

### 3. Check for native project surfaces

- Skip redundant workspace exports when the target repo already exposes a surface natively from
  `.agents/`.
- Keep that behavior conservative and grounded in documented repo behavior.

### 4. Prefer plugin-driven export selection when available

- Use plugin manifests when a capability already defines a packaging boundary.
- Fall back to surface-based export selection when no plugin exists yet.

### 5. Treat synced targets as generated outputs

- Edit canonical files first, then rerun sync.
- Use the repository validation and export smoke tests to confirm behavior.

## Related guidance

- Pair with [Plugin Bundles](../plugin-bundles/SKILL.md) when bundle contents should drive export
  selection.
- Pair with [Repository Setup](../repository-setup/SKILL.md) when the repo needs the canonical versus
  generated model documented clearly.

## Gotchas

- **Do not hand-edit generated `.github/*` or `~/.copilot/*` copies.**
- **Do not assume every surface supports both user and workspace export.**
- **Do not duplicate native project skills into `.github/skills/` by default.**
- **Do not confuse export selection with plugin packaging or provenance tracking.**

## References

- [Compatibility guide](../../../docs/compatibility.md)
- [Copilot compatibility exports guidance](../../instructions/copilot-compatibility-exports.instructions.md)
- [Copilot compatibility exports agent](../../agents/copilot-compatibility-exports.agent.md)
