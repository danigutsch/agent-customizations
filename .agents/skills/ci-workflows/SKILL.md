---
name: ci-workflows
description: 'Design or improve repo CI workflows. Use for GitHub Actions that create and run local lint, type-check, test, package, or repo checks.'
---

# CI Workflows

Use this skill when the task is about repository CI workflow design rather than a single application
feature.

## When to Use This Skill

- User asks to add, review, or improve CI workflows
- User wants pull requests validated automatically
- User wants local repository checks mapped into GitHub Actions
- User wants workflow permissions, caching, or matrices reviewed

## Prerequisites

- The repository's local validation commands are known or can be discovered.
- The current workflow files or CI gaps can be inspected.

## Workflow

### 1. Start from the local validation path

- Identify the real commands contributors should run locally.
- Keep repository-specific validation logic in scripts when that logic is more than a few shell lines.

### 2. Build the smallest useful workflow

- Prefer one clear validation workflow for baseline repository health.
- Use official setup actions for the runtime or toolchain.
- For supplemental checks with useful local CLI value, prefer a thin repo-local command entrypoint
  and keep CI-only bootstrap or upload details in workflow YAML.
- Add matrices only when version or platform coverage is truly required.
- Keep workflow creation concerns explicit:
  naming, triggers, permissions, runner choice, and local-to-CI command mapping.

### 3. Keep the workflow safe and understandable

- Use the narrowest permissions that still let the workflow run.
- Avoid secret-dependent checks for ordinary contribution validation.
- Make failures easy to map back to a local command.

## Related guidance

- Pair this with [Python quality](../python-quality/SKILL.md) for the overall Python baseline.
- Pair this with [Ruff Python](../ruff-python/SKILL.md) or
  [Pyright Python](../pyright-python/SKILL.md) when CI validates those tools.
- Pair this with [Git hooks](../git-hooks/SKILL.md) when local hooks and CI should share commands.

## Gotchas

- **Do not design CI first** — define the local command surface before wrapping it in automation.
- **Do not duplicate complex logic in workflow YAML** — keep repository-specific checks in scripts.
- **Do not add matrices by reflex** — each axis adds maintenance cost.

## References

- [CI workflows instructions](../../instructions/ci-workflows.instructions.md)
- [CI workflows agent](../../agents/ci-workflows.agent.md)
