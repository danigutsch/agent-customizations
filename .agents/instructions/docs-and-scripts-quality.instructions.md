---
description: 'Guidance for documentation and script quality work that should stay aligned with the repository’s existing Markdown, hook, and script validation workflow.'
applyTo: 'README.md, docs/**/*.md, scripts/**/*, .markdownlint.json, .githooks/*, Makefile, .agents/agents/docs-and-scripts-quality.agent.md, .agents/skills/docs-and-scripts-quality/**'
---

# Docs and Scripts Quality Guidance

Use these rules when the task is about documentation quality, script maintenance, or the local
validation workflow that covers them.

## Core model

- Keep docs and scripts aligned with the repository's real contributor workflow.
- Prefer existing validation commands over inventing a parallel quality stack.
- Treat maintenance docs, helper scripts, and local hook behavior as one operating surface.

## Documentation rules

- Keep command examples aligned with real script or `make` entrypoints.
- Prefer concise, non-duplicated maintenance guidance.
- Keep Markdown aligned with the repository's configured lint rules and authoring conventions.
- Prefer narrow generated README sections with explicit ownership markers when one small derived view
  prevents documentation drift better than repeated manual edits.

## Script rules

- Keep scripts explicit about inputs, behavior, and failure modes.
- Prefer the repository's current Python quality tooling for Python scripts.
- Keep hook scripts thin when a repository-local script already owns the real logic.
- When a script owns a generated docs section, pair it with an existing repo validation path so drift
  is caught automatically instead of relying on contributor memory.

## Validation rules

- Use the repository's existing validation commands when they already cover the change.
- Do not document or depend on checks that the repository does not actually run.
- Keep docs, hooks, and validation scripts aligned when a local workflow changes.

## Verification

- Confirm changed docs reflect the real repository commands.
- Confirm changed scripts still fit the existing local validation path.
- Confirm Markdown and script changes respect the repository's configured quality tools.
- Confirm hook behavior still delegates to the intended repository-local validation entrypoint.
