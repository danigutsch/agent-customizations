---
name: python-quality
description: 'Establish or improve a Python repo quality baseline. Use for pyproject layout, shared tooling, ignore rules, local checks, and Python standards.'
---

# Python Quality

Use this skill when the task is about the shared Python quality baseline for a repository.

## When to Use This Skill

- User wants to add or clean up Python tooling
- User wants a better `pyproject.toml` baseline
- User wants shared Python validation commands and docs
- User wants linting, type checking, tests, and ignore rules to work together cleanly

## Prerequisites

- The repository's Python surface is known or can be inspected.
- Existing config, scripts, and contributor docs can be reviewed.

## Workflow

### 1. Inspect the real Python surface

- Identify whether Python is used for scripts, tooling, packages, tests, or automation glue.
- Keep the baseline proportional to that usage.

### 2. Choose a small tool set

- Prefer a clear configuration shape over many overlapping tools.
- Make the local command surface explicit and repository-local.

### 3. Align the whole repository

- Keep `.gitignore`, docs, hooks, and CI aligned with the same Python scope.
- Avoid editor-only conventions when the repository needs shared rules.
- Align Python file defaults with `.editorconfig` when the repo uses shared editor rules.

## Related guidance

- Pair this with [Ruff Python](../ruff-python/SKILL.md) for linting and formatting.
- Pair this with [Pyright Python](../pyright-python/SKILL.md) for type checking.
- Pair this with [EditorConfig](../editorconfig/SKILL.md) when the Python baseline should align with
  repo-wide editor defaults.
- Pair this with [CI workflows](../ci-workflows/SKILL.md) or
  [Git hooks](../git-hooks/SKILL.md) when the baseline should be enforced automatically.

## Gotchas

- **Do not add tools just because they are popular** — each tool needs a clear role.
- **Do not assume package-publishing needs** — many repositories only need a script and automation baseline.
- **Do not let docs, config, and CI drift apart** — the baseline should look the same everywhere.

## References

- [Python quality instructions](../../instructions/python-quality.instructions.md)
- [Python quality agent](../../agents/python-quality.agent.md)
