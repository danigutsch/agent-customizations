---
description: 'Standards for lightweight repository CI workflows that create, refine, and run real local validation commands.'
applyTo: '.github/workflows/**/*.yml, .github/workflows/**/*.yaml, scripts/**/*, README.md, docs/**/*.md'
---

# CI Workflows Standards

Use these rules when the task is about creating or refining repository CI workflows.

## Core principles

- Make CI a wrapper around the repository's real local validation path.
- Prefer one understandable validation workflow over many overlapping workflows.
- Keep the workflow explicit about runtime setup, checkout, and validation commands.
- Design workflows to cover creation and maintenance concerns, not just the final validation step.

## Workflow design

- Use official setup actions for the runtime or toolchain when they exist.
- Keep repository-specific logic in scripts when that logic would otherwise be repeated in workflow
  YAML.
- For supplemental checks with real local value, prefer a thin repository-local command such as a
  `make` target or small script, while leaving CI-only bootstrap details in workflow YAML.
- Add matrices only when version or platform coverage is a real repository requirement.
- Keep caching simple and only when it saves meaningful time.

## Permissions and triggers

- Use the narrowest permissions that let the workflow do its job.
- Prefer pull request, push, and manual dispatch triggers for baseline validation workflows.
- Avoid secrets for checks that should work on normal contributor branches and pull requests.

## Python-specific guidance

- Use `actions/setup-python` when the workflow depends on Python.
- Keep the Python version explicit in workflow configuration.
- Reuse repository-local Ruff, Pyright, test, or validation commands rather than re-specifying tool
  behavior in the workflow.

## Verification

- Confirm contributors can map each CI step to a local command.
- Confirm workflow permissions are not broader than needed.
- Confirm failures point to a small number of understandable checks.
