---
description: 'Guidance for MkDocs and Material for MkDocs configuration, navigation, content structure, and validation.'
applyTo: 'mkdocs.yml, docs/**/*.md, .agents/agents/mkdocs-specialist.agent.md, .agents/skills/mkdocs-specialist/**'
---

# MkDocs Specialist Guidance

Use these rules when the task is specifically about MkDocs site structure, configuration, or
validation rather than generic Markdown maintenance alone.

## Core model

- Treat MkDocs as the active documentation-site path when a repository wants a lightweight,
  Markdown-first portal.
- Keep the docs site easy to read in raw Markdown as well as in the rendered site.
- Prefer repository-local docs commands when the repository already wraps the correct MkDocs build
  path.

## Configuration and navigation rules

- Keep `mkdocs.yml` explicit about site navigation, theme choice, and plugin usage.
- Prefer a deliberate `nav:` structure over opaque or highly automated docs discovery in curated
  repositories.
- Keep theme and plugin choices minimal; add Material-specific features only when they clearly improve
  navigation or maintainability.

## Authoring and structure rules

- Keep landing pages concise and oriented around the repository's main tasks and sections.
- Prefer relative Markdown links so content remains portable between GitHub rendering and MkDocs.
- Keep docs organization aligned with the repository's real contributor workflow instead of forcing a
  portal taxonomy first.

## Validation and publishing rules

- Prefer `mkdocs build --strict` when the repository adopts MkDocs validation directly.
- Keep git-host pages/docs workflows as thin wrappers around the same local build path contributors use.
- Treat site URL, repository URL, and deployment details as explicit config rather than assumptions.

## Verification

- Confirm navigation still matches the intended docs structure.
- Confirm relative links and referenced pages resolve through the repository's real MkDocs build path.
- Confirm theme or plugin changes stay justified and documented by the repo's actual docs needs.
