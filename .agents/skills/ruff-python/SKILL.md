---
name: ruff-python
description: 'Configure Ruff for repo Python linting and formatting. Use for rules, excludes, pyproject config, local commands, hooks, and CI integration.'
---

# Ruff Python

Use this skill when the task is about using Ruff as the repository's Python lint or formatting tool.

## When to Use This Skill

- User wants to add Ruff to a repository
- User wants to refine Ruff rules, excludes, or command usage
- User wants Ruff integrated with hooks or CI
- User wants a faster Python lint baseline with shared config

## Prerequisites

- The repository's Python files and current tool config can be inspected.
- The intended local command surface is known or can be defined.

## Workflow

### 1. Inspect the current state

- Identify current Python files, Ruff config, and any overlapping tools.
- Decide whether Ruff is lint-only or lint-plus-format.

### 2. Keep the config intentional

- Start from a focused rule baseline.
- Keep excludes aligned with generated, vendored, or compatibility-output folders.
- Use per-file ignores sparingly.

### 3. Align automation

- Reuse the same Ruff commands in hooks and CI.
- Keep the contributor command surface explicit.
- Keep Ruff's Python formatting role aligned with repo-wide editor defaults from `.editorconfig`.

## Related guidance

- Pair this with [Python quality](../python-quality/SKILL.md) for the full repo baseline.
- Pair this with [EditorConfig](../editorconfig/SKILL.md) when indentation, line endings, and final
  newlines should align with the repo baseline.
- Pair this with [Pyright Python](../pyright-python/SKILL.md) when linting and type checking both
  matter.
- Pair this with [CI workflows](../ci-workflows/SKILL.md) or
  [Git hooks](../git-hooks/SKILL.md) for enforcement.

## Gotchas

- **Do not enable many rule families by habit** — treat rule growth as a maintenance decision.
- **Do not hide excludes in many places** — keep the skip surface understandable.
- **Do not let hook and CI commands drift from local usage**.

## References

- [Ruff Python instructions](../../instructions/ruff-python.instructions.md)
- [Ruff Python agent](../../agents/ruff-python.agent.md)
