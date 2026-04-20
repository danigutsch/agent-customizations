---
description: 'Guidance for GitHub issue authoring, updates, issue types, dependencies, fields, and project-aware issue workflows.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/github-issues.agent.md, .agents/skills/github-issues/**'
---

# GitHub Issues Guidance

Use these rules when the task is about creating, refining, updating, or organizing GitHub issues and
their related metadata.

## Core model

- Treat the issue title, body, type, labels, assignees, dependencies, and project placement as one
  coherent issue contract.
- Prefer issue types for primary categorization when the organization has them enabled.
- Prefer reusable body templates so created issues are readable, actionable, and easy to execute.
- Keep issue-owned metadata separate from project-owned metadata.

## Authoring rules

- Write short, specific, action-oriented titles.
- Keep titles free of redundant prefixes such as `[Bug]` when the issue type already captures the
  category.
- Match the body shape to the request:
  bug report, feature request, or task.
- Include acceptance criteria or an execution checklist when the issue is meant to drive follow-on
  implementation.
- Link related issues explicitly instead of leaving relationships implicit in prose.

## Metadata rules

- Prefer `type` over equivalent labels such as `bug` or `enhancement` when the repository or
  organization exposes issue types.
- Use labels for orthogonal routing signals such as priority, area, onboarding friendliness, or
  documentation scope.
- Use issue fields for metadata that should travel with the issue across projects.
- Use project fields only for project-scoped workflow state such as status or iteration.
- Prefer formal sub-issue and dependency relationships over plain-text "blocked by" notes when the
  platform supports them.

## Tooling rules

- Prefer GitHub read tools or MCP wrappers for discovery before mutating issues.
- Use `gh api` or GraphQL directly when issue creation, updates, dependencies, fields, or project
  mutations are not covered by higher-level wrappers.
- Read the current issue before patching it so unchanged fields are preserved deliberately.
- Use explicit REST or GraphQL payloads for typed values that the CLI's `-f` string encoding would
  otherwise mangle.

## Search and discovery rules

- Use simple repo-scoped listing for straightforward state or label filters.
- Use issue search for cross-repo text, author, assignee, label, milestone, or issue-type queries.
- Use advanced REST or GraphQL search only when explicit boolean logic or field-value filtering is
  required.
- Be conservative with field-value search syntax and prefer GraphQL bulk reads when API search
  support is inconsistent.

## Workflow rules

- Confirm repository context before creating or updating an issue.
- Discover available issue types, fields, labels, milestones, and project fields before assuming
  names or values.
- Ask for missing critical details when the user wants a concrete issue created and the missing
  information would materially affect the final issue contract.
- Confirm the resulting issue URL or updated issue number after the change is applied.

## Verification

- Confirm the issue title and body match the requested intent.
- Confirm issue type, labels, assignees, milestone, and field updates reflect actual available
  metadata.
- Confirm sub-issue, dependency, and project-item relationships were applied to the intended issue.
- Confirm the final workflow uses existing GitHub primitives instead of inventing repo-local issue
  conventions.
