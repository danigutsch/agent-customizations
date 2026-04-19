---
name: mkdocs-specialist
description: Guidance for MkDocs and Material for MkDocs sites. Use when working on `mkdocs.yml`, docs navigation, Markdown landing pages, lightweight docs-site validation, or git-host pages/docs publishing for a Markdown-first repository.
---

# MkDocs Specialist

Use this skill when the task is about a MkDocs documentation site rather than general docs cleanup.

## When to Use This Skill

- The repository uses or is adopting MkDocs
- The task involves `mkdocs.yml`, `nav:`, theme choices, or Material for MkDocs features
- The user needs a Markdown-first docs portal that stays lightweight
- The user needs MkDocs validation or git-host pages/docs publishing guidance tied to the repository's real docs workflow

## Prerequisites

- The docs tree and current site configuration can be inspected
- The repository's current local docs command or CI workflow can be identified
- The task is actually about site structure or MkDocs behavior rather than generic Markdown editing

## Workflow

### 1. Confirm the site shape

- Inspect `mkdocs.yml`, the docs tree, and the landing pages together
- Keep the site structure aligned with the repository's real docs ownership boundaries

### 2. Keep navigation explicit

- Prefer a deliberate `nav:` over highly implicit structure in curated repositories
- Keep landing pages short, navigable, and task-oriented

### 3. Stay lightweight

- Prefer minimal plugins and theme features
- Use Material for MkDocs where the richer UI clearly improves maintainability or discoverability

### 4. Validate with the real repo command

- Reuse the repository's existing build or preview command when it already wraps MkDocs correctly
- Prefer `mkdocs build --strict` when the repo uses raw MkDocs validation

## Related guidance

- Pair with [Docs and scripts quality](../docs-and-scripts-quality/SKILL.md) when docs-site changes
  also affect contributor docs, hooks, or maintenance scripts.
- Pair with [Repository setup](../repository-setup/SKILL.md) when the site structure is part of a
  broader repo baseline change.

## Gotchas

- **Do not over-automate navigation in a curated docs repo.**
- **Do not add heavy plugins without a clear repository need.**
- **Do not optimize the site at the expense of raw Markdown readability.**
- **Do not assume git-host URLs, pages/docs settings, or deployment branches that the repository has not defined.**

## References

- [MkDocs specialist guidance](../../instructions/mkdocs-specialist.instructions.md)
- [MkDocs specialist agent](../../agents/mkdocs-specialist.agent.md)
