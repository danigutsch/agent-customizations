# Projects V2

GitHub Projects V2 is managed through GraphQL. Prefer higher-level project tools for reads when
they exist, then fall back to `gh api graphql` for mutations or more reliable discovery.

## Preferred workflow

1. **Find the project**.
2. **Discover fields** so you have the field IDs and option IDs.
3. **Find the item** for the issue or add the issue to the project.
4. **Mutate** the project item or field value.

## Finding a project by name

> **Known issue:** name search is keyword-based, not exact-match based, so common words can produce
> many false positives.

Use this priority order:

### 1. Direct lookup if you know the number

```bash
gh api graphql -f query='{
  organization(login: "ORG") {
    projectV2(number: 42) { id title }
  }
}' --jq '.data.organization.projectV2'
```

### 2. Reverse lookup from a known issue

```bash
gh api graphql -f query='{
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 123) {
      projectItems(first: 10) {
        nodes {
          id
          project { number title id }
        }
      }
    }
  }
}' --jq '.data.repository.issue.projectItems.nodes[] | {number: .project.number, title: .project.title, id: .project.id}'
```

### 3. GraphQL name search with client-side filtering

```bash
gh api graphql -f query='{
  organization(login: "ORG") {
    projectsV2(first: 100, query: "search term") {
      nodes { number title id }
    }
  }
}' --jq '.data.organization.projectsV2.nodes[] | select(.title | test("(?i)^exact name$"))'
```

## OAuth scopes

| Operation | Required scope |
| --- | --- |
| Read projects, fields, items | `read:project` |
| Add, update, or delete items | `project` |

To add the write scope:

```bash
gh auth refresh -h github.com -s project
```

## Common GraphQL operations

**Find a project and its Status field options:**

```bash
gh api graphql -f query='
{
  organization(login: "ORG") {
    projectV2(number: 5) {
      id
      title
      field(name: "Status") {
        ... on ProjectV2SingleSelectField {
          id
          options { id name }
        }
      }
    }
  }
}' --jq '.data.organization.projectV2'
```

**List all fields:**

```bash
gh api graphql -f query='
{
  node(id: "PROJECT_ID") {
    ... on ProjectV2 {
      fields(first: 20) {
        nodes {
          ... on ProjectV2Field { id name }
          ... on ProjectV2SingleSelectField { id name options { id name } }
          ... on ProjectV2IterationField { id name configuration { iterations { id startDate } } }
        }
      }
    }
  }
}' --jq '.data.node.fields.nodes'
```

**Update a field value:**

```bash
gh api graphql -f query='
mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: "PROJECT_ID"
    itemId: "ITEM_ID"
    fieldId: "FIELD_ID"
    value: { singleSelectOptionId: "OPTION_ID" }
  }) {
    projectV2Item { id }
  }
}'
```

**Add an item:**

```bash
gh api graphql -f query='
mutation {
  addProjectV2ItemById(input: {
    projectId: "PROJECT_ID"
    contentId: "ISSUE_OR_PR_NODE_ID"
  }) {
    item { id }
  }
}'
```

**Delete an item:**

```bash
gh api graphql -f query='
mutation {
  deleteProjectV2Item(input: {
    projectId: "PROJECT_ID"
    itemId: "ITEM_ID"
  }) {
    deletedItemId
  }
}'
```

## Finding an issue's project item ID

When you know the issue but need its item ID:

```bash
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 123) {
      projectItems(first: 5) {
        nodes {
          id
          project { title number }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2SingleSelectField { name } }
              }
            }
          }
        }
      }
    }
  }
}' --jq '.data.repository.issue.projectItems.nodes'
```
