---
description: 'Guidance for exporting canonical .agents assets into Copilot-compatible workspace and user targets with scope-aware mapping, native-surface skips, and generated-output discipline.'
applyTo: 'README.md, docs/compatibility.md, scripts/sync_copilot_exports.py, scripts/run_export_smoke_tests.py, .agents/agents/copilot-compatibility-exports.agent.md, .agents/skills/copilot-compatibility-exports/**, .agents/instructions/copilot-compatibility-exports.instructions.md'
---

# Copilot Compatibility Exports Guidance

Use these rules when the task is about exporting canonical `.agents` assets into Copilot-compatible
locations.

## Core model

- Treat `.agents/` as the canonical source of truth.
- Treat compatibility exports under `.github/*` and `~/.copilot/*` as generated outputs.
- Model compatibility as a scope-aware mapping of surfaces, not as a flat copy of one directory tree.
- Keep canonical sources, generated copies, and sync-state tracking aligned.

## Scope and surface rules

- Be explicit about which surfaces support workspace export, user export, or both.
- Keep workspace exports rooted under `.github/` in the target repository when that surface is
  supported.
- Keep user exports rooted under `~/.copilot/` when that surface is supported.
- Do not assume prompts, repo-wide instructions, MCP assets, workflows, or plugins follow the same
  compatibility model as agents and instructions.

## Native-surface rules

- Skip workspace exports for surfaces the target repository already exposes natively from `.agents/`
  when the repository behavior is documented and test-backed.
- Keep that skip behavior conservative and explicit.
- Do not duplicate native skills into `.github/skills/` by default when the target repo already has
  `.agents/skills/`.

## Export-selection rules

- Prefer plugin-driven export selection when plugin manifests already define the distributed file
  boundary.
- Use surface-level export selection as the fallback when no plugin bundle exists yet.
- Keep plugin manifests, export behavior, and generated output aligned when both are in play.

## Generated-output rules

- Edit canonical `.agents/*` files first and rerun sync instead of hand-editing exported copies.
- Keep stale-output cleanup stateful so removed or replaced files do not linger silently.
- Keep generated workspace exports ignored by default when the repository policy treats them as
  compatibility output rather than tracked source.

## Verification

- Confirm the documented compatibility matrix matches the actual sync script behavior.
- Confirm workspace and user export examples use the real supported CLI options.
- Confirm native-surface skip behavior is covered by smoke tests.
- Confirm generated-output discipline is stated clearly enough that consumers do not maintain two
  sources of truth.
