---
description: 'Standards for repository setup covering structure, baseline documentation, validation, and CI-ready foundations.'
applyTo: 'README.md, AGENTS.md, .gitignore, docs/**/*.md, scripts/**/*, templates/**/*, examples/**/*, .github/**/*, .agents/**/*'
---

# Repository Setup Standards

Use these rules when the task involves creating or improving repository foundations rather than a
single feature implementation.

## Repository purpose and structure

- Make the repository purpose explicit near the top of the README.
- Prefer a small set of top-level folders with clear responsibilities.
- Keep reusable assets grouped by type or capability rather than mixing unrelated concerns.
- Avoid creating folders that have no near-term purpose.
- Keep repository-specific guidance explicit and keep reusable guidance generic.

## Documentation expectations

- Ensure the repository has a clear top-level explanation of what it contains and what it does not.
- Add baseline repository health files when they materially clarify contribution and ownership
  expectations: typically `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, and `CODE_OF_CONDUCT.md`.
- Keep repository-wide operating rules in a dedicated guidance file when the repository has custom
  structure or contributor expectations.
- Document validation and maintenance expectations when the repository depends on custom scripts or
  repository-specific checks.
- Avoid overlapping docs that restate the same rules with different wording.

## Asset and folder expectations

- Keep examples, templates, scripts, and docs in dedicated folders when they are part of the
  repository model.
- Prefer naming that explains purpose over naming that reflects one tool vendor.
- When the repository groups reusable capability slices, document how those slices should be
  reviewed and maintained.

## Validation expectations

- Prefer repository-local validation scripts for checks that contributors are expected to run often.
- Keep validation commands lightweight and discoverable.
- Use existing build, test, lint, or schema-validation tools when they already fit the repository.
- Do not rely on manual review alone for structured assets that can be validated automatically.

## CI and automation expectations

- Define the minimum useful validation path for the repository:
  restore/build/test for code repositories, or schema/script/content validation for customization
  repositories.
- Keep CI aligned with the real maintenance surface of the repository.
- Reuse repository-local validation commands in CI rather than duplicating logic in many places.
- Prefer reusable workflow patterns only after the repository-local command surface is clear.

## Pairing focused slices

- Pair with `ci-workflows` for workflow design and validation automation.
- Pair with `editorconfig` for shared repo editor defaults and file-type-specific indentation rules.
- Pair with `python-quality` when Python scripts or tooling are part of the repository foundation.
- Pair with `ruff-python` and `pyright-python` when the repository needs shared Python quality rules.
- Pair with `git-hooks` when local hooks should mirror the documented validation path.

## Anti-patterns to avoid

- Adding generic boilerplate files that do not match the repository purpose
- Hiding important maintenance steps in tribal knowledge
- Using many overlapping docs for the same repository rules
- Creating structure that optimizes for hypothetical future needs instead of current clarity
- Adding automation before defining what should actually be validated

## Verification

- Confirm the repository purpose and top-level layout are easy to understand.
- Confirm the main maintenance and validation steps are documented.
- Confirm repository-local scripts and docs match the actual structure on disk.
