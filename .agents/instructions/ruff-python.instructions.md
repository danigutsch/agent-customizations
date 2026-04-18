---
description: 'Standards for configuring Ruff as a fast Python lint and formatting baseline.'
applyTo: 'pyproject.toml, ruff.toml, .ruff.toml, scripts/**/*.py, .github/workflows/**/*.yml, .github/workflows/**/*.yaml, README.md'
---

# Ruff Python Standards

Use these rules when the task is about configuring or refining Ruff for a repository.

## Configuration

- Prefer shared Ruff configuration in `pyproject.toml` when the repository already uses it.
- Keep line length, target version, and exclude behavior explicit when they differ from Ruff defaults.
- Let Ruff own linting and formatting only when that matches the repository's chosen tool set.

## Rule design

- Start with a focused rule baseline and expand intentionally.
- Prefer fixing root causes over adding many per-file ignores.
- Use per-file ignores sparingly and document why they are needed when they are not obvious.

## Commands and automation

- Keep the local command surface explicit:
  `ruff check`, `ruff format`, or their `--check` forms.
- Reuse those same commands in hooks or CI rather than inventing alternate logic.
- Respect generated or compatibility-output folders in exclude settings when they should not be linted.

## Verification

- Confirm Ruff covers the intended files and skips the intended generated files.
- Confirm local and CI command usage are consistent.
- Confirm the rule set is maintainable for the repository's contributors.
