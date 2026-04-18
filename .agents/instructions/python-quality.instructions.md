---
description: 'Standards for lightweight Python quality baselines using shared repo config, explicit commands, and balanced tooling.'
applyTo: 'pyproject.toml, .gitignore, README.md, scripts/**/*.py, docs/**/*.md, .github/workflows/**/*.yml, .github/workflows/**/*.yaml'
---

# Python Quality Standards

Use these rules when the task is about establishing or improving the Python quality baseline for a
repository.

## Baseline shape

- Prefer one clear repository-local configuration shape for Python tools.
- Use `pyproject.toml` as the shared tool configuration surface when it fits the repository.
- Keep Python version targeting explicit when tool behavior depends on it.

## Tooling expectations

- Choose a small, compatible tool set rather than several overlapping tools.
- Keep linting, type checking, tests, and validation commands easy to discover.
- Prefer repository-local commands or scripts over editor-only expectations.

## Repository alignment

- Match the Python baseline to the repository's real Python usage:
  scripts, tooling, packages, tests, or automation glue.
- Keep `.gitignore`, CI, and contributor docs aligned with the Python tool surface.
- Avoid packaging or publishing boilerplate unless the repository actually needs it.

## Pairing guidance

- Pair with `editorconfig` when Python file defaults should align with repo-wide editor rules.
- Pair with `ruff-python` when the repository needs a lint or format baseline.
- Pair with `pyright-python` when the repository needs shared type-checking rules.
- Pair with `ci-workflows` when the baseline should be enforced automatically.

## Verification

- Confirm the Python baseline is documented and runnable locally.
- Confirm config files, ignore rules, and CI reflect the same scope.
- Confirm the tool set is intentional and not redundant.
