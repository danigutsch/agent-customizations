---
name: pyright-python
description: 'Configure Pyright or Pylance for repo Python type checking. Use for scope, strictness, import resolution, pyproject settings, and CI integration.'
---

# Pyright Python

Use this skill when the task is about shared Python type-checking behavior with Pyright or Pylance.

## When to Use This Skill

- User wants to add or improve Pyright config
- User wants to reduce noisy Python diagnostics
- User wants clearer include, exclude, or strictness boundaries
- User wants shared type-checking behavior in local workflows and CI

## Prerequisites

- The repository's Python files and import layout can be inspected.
- Existing Pyright, `pyproject.toml`, or editor diagnostics are available.

## Workflow

### 1. Define the analysis boundary

- Identify which files should be analyzed and which should not.
- Keep shared paths relative and repository-local.

### 2. Choose the configuration shape

- Use `[tool.pyright]` in `pyproject.toml` when the repository centralizes Python tool config there.
- Use a dedicated config file only when it is clearly easier to maintain.

### 3. Tune strictness intentionally

- Preserve default-style excludes that reduce noise from caches and dependencies.
- Use targeted strictness or rule changes instead of blanket escalation when needed.
- Keep local and CI analysis pointed at the same boundary.

## Related guidance

- Pair this with [Python quality](../python-quality/SKILL.md) for the broader repo baseline.
- Pair this with [Ruff Python](../ruff-python/SKILL.md) when linting and type checking both matter.
- Pair this with [CI workflows](../ci-workflows/SKILL.md) when Pyright should gate pull requests.

## Gotchas

- **Do not encode user-specific virtual environment paths in shared config**.
- **Do not widen analysis until caches and generated folders become noise**.
- **Do not assume strict-everywhere is the right starting point**.

## References

- [Pyright Python instructions](../../instructions/pyright-python.instructions.md)
- [Pyright Python agent](../../agents/pyright-python.agent.md)
