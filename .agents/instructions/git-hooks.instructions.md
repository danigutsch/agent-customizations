---
description: 'Standards for lightweight Git hook design that complements CI without becoming the only validation path.'
applyTo: '.agents/hooks/**/*, .githooks/**/*, .pre-commit-config.yaml, scripts/**/*, README.md, docs/**/*.md'
---

# Git Hooks Standards

Use these rules when the task is about designing or refining repository Git hooks.

## Hook role

- Treat hooks as a convenience layer for fast local feedback, not as the only validation path.
- Keep hooks thin and delegate real work to repository-local commands or scripts.
- Prefer checks that are cheap enough for normal developer flow.

## Hook selection

- Use `pre-commit` for fast checks such as lint, syntax, or focused repo validation.
- Use `commit-msg` only when commit message policy materially matters to the repository.
- Avoid putting long-running integration or network-dependent checks in ordinary hooks.

## Installation and maintenance

- Make hook installation and opt-in behavior explicit in repository docs.
- Keep hook scripts portable and easy to inspect.
- Align hooks with the same commands CI uses where practical.
- When the repository wants one documented local setup step, a tracked opt-in Git config include may
  bootstrap `core.hooksPath`, but keep that setup explicit and reviewable.

## Verification

- Confirm hooks fail fast and point to an understandable local command.
- Confirm contributors can still validate manually without relying on hooks.
- Confirm hook behavior is documented and does not depend on hidden machine state.
