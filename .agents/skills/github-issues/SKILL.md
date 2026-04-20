---
name: github-issues
description: 'Create, update, search, and organize GitHub issues. Use when the task involves issue bodies, issue types, labels, dependencies, fields, or project items.'
---

# GitHub Issues

Use this skill when the task is about creating, refining, updating, or organizing GitHub issues and
their related metadata.

## When to Use This Skill

- The user wants to create a bug report, feature request, or task issue
- The user wants to update an existing issue title, body, state, labels, assignees, or milestone
- The user needs issue types, issue fields, dependencies, or sub-issue relationships managed
- The user needs an issue added to or updated inside a GitHub Project
- The user needs complex issue search or reporting across repositories

## Prerequisites

- The target GitHub repository is known.
- The environment has an authenticated GitHub CLI when write operations are required.
- The available labels, issue types, fields, milestones, or project metadata can be discovered when
  the task depends on them.

## Tool model

### Read operations

Prefer GitHub read tools or MCP wrappers for:

- issue details
- issue comments
- issue labels
- sub-issue reads
- search and list operations
- project discovery and project-item reads

### Write operations

Use `gh api` or GraphQL for:

- creating issues
- updating issues
- adding issue comments
- creating sub-issue and dependency links
- setting issue fields
- adding or updating project items

> `gh issue create` is fine for simple issue creation, but prefer `gh api` when you need issue
> types or more explicit payload control.

## Recommended workflow

1. **Determine the action**: create, refine, update, search, or report.
2. **Gather context**: confirm repository, inspect related issues, and discover available metadata.
3. **Choose a body shape**: use the matching template from [templates.md](./references/templates.md).
4. **Execute with the right surface**:
   read tools for discovery, `gh api` or GraphQL for mutations.
5. **Confirm the result**: report the issue URL or updated issue number.

## Creating issues

Use `gh api` when you need issue types or structured payload control:

```bash
gh api repos/{owner}/{repo}/issues \
  -X POST \
  -f title="Issue title" \
  -f body="Issue body in markdown" \
  -f type="Bug" \
  --jq '{number, html_url}'
```

### Optional parameters

```text
-f type="Bug"                    # Issue type (Bug, Feature, Task, Epic, ...)
-f labels[]="high-priority"      # Repeat for multiple labels
-f assignees[]="username"        # Repeat for multiple assignees
-f milestone=1                   # Milestone number
```

### Issue type guidance

- Prefer issue types over equivalent labels when the organization exposes them.
- Discover available types before assuming names.
- Keep titles free of redundant prefixes such as `[Bug]` when an issue type is set.

See [issue-types.md](./references/issue-types.md).

## Body structure

Use the matching template from [templates.md](./references/templates.md):

| Intent | Template |
| --- | --- |
| Bug, broken behavior, regression | Bug report |
| Feature, enhancement, new capability | Feature request |
| Task, chore, refactor, maintenance work | Task |

## Updating issues

Patch only the fields you actually intend to change:

```bash
gh api repos/{owner}/{repo}/issues/{number} \
  -X PATCH \
  -f state=closed \
  -f title="Updated title" \
  --jq '{number, html_url}'
```

Prefer reading the current issue first so the update stays scoped.

## Extended capabilities

Load the narrower reference only when the task needs it:

| Capability | Use when | Reference |
| --- | --- | --- |
| Advanced search | Complex boolean search, cross-repo reporting, issue-type search, or field filters | [search.md](./references/search.md) |
| Sub-issues | Parent-child work breakdown or nested planning | [sub-issues.md](./references/sub-issues.md) |
| Dependencies | Blocked-by or blocking relationships | [dependencies.md](./references/dependencies.md) |
| Issue types | Type discovery or explicit type mutations | [issue-types.md](./references/issue-types.md) |
| Projects V2 | Adding issues to projects or updating project-item fields | [projects.md](./references/projects.md) |
| Issue fields | Issue-level dates, priority, text, number, or single-select metadata | [issue-fields.md](./references/issue-fields.md) |
| Images | Programmatic image embedding in issue bodies or comments | [images.md](./references/images.md) |

## Gotchas

- **Do not assume the repo uses labels as its primary category system**; issue types may already be
  available.
- **Do not use `gh api -f` for typed JSON bodies that must stay numeric**; use `--input` when the
  API requires integers.
- **Do not rely on advanced field-value search as the only discovery path**; GraphQL reads are often
  more reliable.
- **Do not patch existing issues blindly**; read first, then update only the intended fields.

## References

- [GitHub issues guidance](../../instructions/github-issues.instructions.md)
- [GitHub issues agent](../../agents/github-issues.agent.md)
- Official GitHub custom-agent documentation:
  <https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents>
- Official GitHub agent-skills documentation:
  <https://docs.github.com/en/copilot/concepts/agents/about-agent-skills>
- Agent Skills standard:
  <https://agentskills.io>
- Upstream source adapted from:
  <https://github.com/github/awesome-copilot/tree/main/skills/github-issues>
