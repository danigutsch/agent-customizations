# Advanced Issue Search

The issue-search surface supports GitHub's issue query format for cross-repo searches, including
date ranges, metadata filters, and text search. Choose the simplest search path that can answer the
question before reaching for advanced search.

## When to use search vs list vs advanced search

There are three ways to find issues, each with different capabilities:

| Capability | Repo list | Issue search | Advanced search (`gh api`) |
| --- | --- | --- | --- |
| **Scope** | Single repo only | Cross-repo, cross-org | Cross-repo, cross-org |
| **Issue field filters** (`field.priority:P0`) | No | No | **Yes** |
| **Issue type filter** (`type:Bug`) | No | Yes | Yes |
| **Boolean logic** | No | Implicit AND only | **Yes** |
| **Label/state/date filters** | Yes | Yes | Yes |
| **Assignee/author/mentions** | No | Yes | Yes |
| **Negation** (`-label:x`, `no:label`) | No | Yes | Yes |
| **Text search** | No | Yes | Yes |
| **How to call** | Repo list tool | Issue search tool | `gh api` with `advanced_search=true` |

**Decision guide:**

- **Single repo, simple state or label filters:** use repo-scoped listing.
- **Cross-repo text, author, assignee, or type filters:** use issue search.
- **Issue field filters or explicit boolean logic:** use advanced REST or GraphQL search.

## Query syntax

The query is a string of search terms and qualifiers. A space between terms is implicit AND.

### Scoping

```text
repo:owner/repo
org:github
user:octocat
in:title
in:body
in:comments
```

### State and close reason

```text
is:open
is:closed
reason:completed
reason:"not planned"
```

### People

```text
author:username
assignee:username
mentions:username
commenter:username
involves:username
author:@me
team:org/team
```

### Labels, milestones, projects, and types

```text
label:"bug"
label:bug label:priority
label:bug,enhancement
-label:wontfix
milestone:"v2.0"
project:github/57
type:"Bug"
```

### Missing metadata

```text
no:label
no:milestone
no:assignee
no:project
```

### Dates

All date qualifiers support `>`, `<`, `>=`, `<=`, and range (`..`) operators with ISO 8601 values:

```text
created:>2026-01-01
updated:>=2026-03-01
closed:2026-01-01..2026-02-01
created:<2026-01-01
```

### Linked content

```text
linked:pr
-linked:pr
linked:issue
```

### Numeric filters

```text
comments:>10
comments:0
interactions:>100
reactions:>50
```

### Boolean logic and nesting

Use `AND`, `OR`, and parentheses:

```text
label:bug AND assignee:octocat
assignee:octocat OR assignee:hubot
(type:"Bug" AND label:P1) OR (type:"Feature" AND label:P1)
-author:app/dependabot
```

## Common query patterns

**Unassigned bugs:**

```text
repo:owner/repo type:"Bug" no:assignee is:open
```

**Issues closed this week:**

```text
repo:owner/repo is:closed closed:>=2026-03-01
```

**Stale open issues:**

```text
repo:owner/repo is:open updated:<2026-01-01
```

**Open issues without a linked PR:**

```text
repo:owner/repo is:open -linked:pr
```

**Issues I am involved in across an org:**

```text
org:github involves:@me is:open
```

## Issue field search

> **Reliability warning:** Field-value search remains inconsistent across API surfaces. Prefer the
> GraphQL bulk-read approach from [issue-fields.md](issue-fields.md) when correctness matters.

Issue fields can be searched through advanced search mode with dot-notation qualifiers:

```bash
gh api "search/issues?q=org:github+field.priority:P0+type:Epic+is:open&advanced_search=true" \
  --jq '.items[] | "#\(.number): \(.title)"'
```

### Field qualifiers

```text
field.priority:P0
field.target-date:>=2026-04-01
has:field.priority
no:field.priority
```

Use the field slug form: lowercase with hyphens instead of spaces.

## Limits

- Query text: max **256 characters** excluding operators and qualifiers
- Boolean operators: max **5** AND, OR, or NOT operators
- Results: max **1,000**
- Field search requires `advanced_search=true` for REST or `ISSUE_ADVANCED` in GraphQL
