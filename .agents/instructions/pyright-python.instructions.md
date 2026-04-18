---
description: 'Standards for Pyright or Pylance configuration covering scope, excludes, strictness, and shareable type-checking rules.'
applyTo: 'pyproject.toml, pyrightconfig.json, scripts/**/*.py, .github/workflows/**/*.yml, .github/workflows/**/*.yaml, README.md'
---

# Pyright Python Standards

Use these rules when the task is about configuring Pyright or refining shared Python type-checking
behavior.

## Configuration shape

- Prefer `[tool.pyright]` in `pyproject.toml` when the repository already centralizes Python tool
  config there.
- Use `pyrightconfig.json` only when a dedicated config file is clearly easier to maintain.
- Keep shared paths relative to the repository.

## Scope and strictness

- Keep `include` and `exclude` aligned with the repository's real Python analysis surface.
- Preserve default-style excludes when they help avoid noise from caches and dependency folders.
- Use targeted strictness and rule tuning rather than escalating every repository to maximum strictness.

## Environment guidance

- Do not store user-specific virtual environment paths in shared config.
- Make non-standard import roots explicit when the repository depends on them.
- Keep CI and local type-checking pointed at the same analysis boundary.

## Verification

- Confirm Pyright analyzes the intended files and avoids irrelevant folders.
- Confirm config stays shareable across contributors and machines.
- Confirm strictness and diagnostics match the repository's maintenance goals.
