---
name: copilot-compatibility-exports
description: Canonical-to-compatible export guidance for Copilot customization assets. Use when deciding how `.agents` content maps into `.github/*` or `~/.copilot/*`, when debugging sync behavior, when documenting generated export copies, or when keeping canonical assets and compatibility mirrors from drifting.
---

# Copilot Compatibility Exports

Use this skill when the task is about how reusable Copilot assets are exported from a canonical
location into workspace or user-level compatibility targets.

## When to Use This Skill

- The user wants to know which surfaces should export to `.github/*` or `~/.copilot/*`
- The user is adding a new slice and needs to know whether it should be mirrored
- The user is debugging sync behavior, stale exports, or source-of-truth drift
- The user wants compatibility documentation for agents, instructions, prompts, skills, or hooks
- The user needs guidance on ignore strategy for generated compatibility copies

## Prerequisites

- The canonical asset location is known.
- The target scope is known or can be inferred.
- The repository's export scripts or compatibility docs can be inspected.

## Workflow

### 1. Identify the canonical surface

- Confirm where the maintained asset lives.
- Treat the canonical location as authoritative when a mirror also exists.

### 2. Confirm supported target scope

- Decide whether the surface supports workspace scope, user scope, both, or neither.
- Call out when a surface is only partially portable across Copilot clients.

### 3. Choose the export boundary

- Prefer plugin-scoped export when a plugin bundle already defines the intended bundle boundary.
- Use surface-scoped export when a plugin bundle does not exist yet.

### 4. Keep generated copies disposable

- Rerun sync instead of hand-editing exported copies.
- Remove stale mirrors through the normal sync and cleanup flow.

### 5. Document the portability limits

- Be explicit about unsupported or special-case surfaces.
- Do not imply a stable target path where the platform does not document one.

## Related guidance

- Pair with [Repository setup](../repository-setup/SKILL.md) when a repo needs its canonical versus
  generated asset model made explicit.
- Pair with [MCP servers](../mcp-servers/SKILL.md) when compatibility questions overlap with MCP
  setup or host-specific configuration.

## Gotchas

- **Do not treat generated exports as source**.
- **Do not assume every surface mirrors the same way**.
- **Do not invent user-level paths for prompts or other unstable surfaces**.
- **Do not hide tracked-file caveats** when an ignore strategy will not work as expected.

## References

- [Compatibility documentation](../../../docs/compatibility.md)
- [Compatibility export guidance](../../instructions/copilot-compatibility-exports.instructions.md)
- [Copilot compatibility exports agent](../../agents/copilot-compatibility-exports.agent.md)
