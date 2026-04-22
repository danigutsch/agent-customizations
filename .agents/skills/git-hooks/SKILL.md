---
name: git-hooks
description: 'Design lightweight repo Git hooks. Use for pre-commit, commit-msg, optional hook frameworks, fast local checks, and alignment with CI.'
---

# Git Hooks

Use this skill when the task is about repository-local Git hooks rather than server-side automation.

## When to Use This Skill

- User wants to add or improve `pre-commit` or `commit-msg` hooks
- User wants fast local quality checks before commits
- User wants hook behavior aligned with CI and documented local commands
- User wants hook setup without heavy or fragile automation

## Prerequisites

- The repository's local validation commands are known or can be inspected.
- Existing hooks, hook scripts, or hook framework choices can be reviewed.

## Workflow

### 1. Start from cheap local checks

- Identify checks that are fast enough for normal commit flow.
- Keep hooks as wrappers over repository-local commands where possible.

### 2. Choose the right hook type

- Prefer `pre-commit` for lint, syntax, and focused repository validation.
- Use `commit-msg` only when message policy materially matters.

### 3. Keep hooks optional but useful

- Document installation and bypass behavior.
- Treat hooks as a convenience layer, not the only required validation.
- Align hook commands with CI when possible.
- If the repository already uses a tracked opt-in local Git config include, it may bootstrap the
  hook path, but the setup step should stay explicit in docs.

## Related guidance

- Pair this with [CI workflows](../ci-workflows/SKILL.md) so hooks and CI reuse the same commands.
- Pair this with [Python quality](../python-quality/SKILL.md),
  [Ruff Python](../ruff-python/SKILL.md), or [Pyright Python](../pyright-python/SKILL.md)
  when Python checks belong in hooks.

## Gotchas

- **Do not put slow checks in ordinary hooks**.
- **Do not make hooks the only place required validation runs**.
- **Do not rely on hidden machine state or network access for basic hook execution**.

## References

- [Git hooks instructions](../../instructions/git-hooks.instructions.md)
- [Git hooks agent](../../agents/git-hooks.agent.md)
