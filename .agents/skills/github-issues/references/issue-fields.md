# Issue Fields (GraphQL, Private Preview)

> **Private preview:** Issue fields are currently in private preview. Request access at
> <https://github.com/orgs/community/discussions/175366>.

Issue fields are custom metadata defined at the organization level and set per issue. Common
examples include start date, target date, priority, impact, or effort.

All issue-field queries and mutations require the `GraphQL-Features: issue_fields` HTTP header.

## Why use issue fields

- Issue fields travel with the issue across projects and views.
- Project fields are project-scoped, so use them only for project-local workflow state.
- Issue fields are the better fit for stable issue-owned metadata.

## Discovering available fields

```graphql
# Header: GraphQL-Features: issue_fields
{
  organization(login: "OWNER") {
    issueFields(first: 30) {
      nodes {
        __typename
        ... on IssueFieldDate { id name }
        ... on IssueFieldText { id name }
        ... on IssueFieldNumber { id name }
        ... on IssueFieldSingleSelect { id name options { id name color } }
      }
    }
  }
}
```

Field types include `IssueFieldDate`, `IssueFieldText`, `IssueFieldNumber`, and
`IssueFieldSingleSelect`.

## Reading field values on an issue

```graphql
# Header: GraphQL-Features: issue_fields
{
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 123) {
      issueFieldValues(first: 20) {
        nodes {
          __typename
          ... on IssueFieldDateValue {
            value
            field { ... on IssueFieldDate { id name } }
          }
          ... on IssueFieldTextValue {
            value
            field { ... on IssueFieldText { id name } }
          }
          ... on IssueFieldNumberValue {
            value
            field { ... on IssueFieldNumber { id name } }
          }
          ... on IssueFieldSingleSelectValue {
            name
            color
            field { ... on IssueFieldSingleSelect { id name } }
          }
        }
      }
    }
  }
}
```

## Setting field values

Use `setIssueFieldValue` to set one or more fields at once.

```graphql
# Header: GraphQL-Features: issue_fields
mutation {
  setIssueFieldValue(input: {
    issueId: "ISSUE_NODE_ID"
    issueFields: [
      { fieldId: "IFD_xxx", dateValue: "2026-04-15" }
      { fieldId: "IFT_xxx", textValue: "some text" }
      { fieldId: "IFN_xxx", numberValue: 3.0 }
      { fieldId: "IFSS_xxx", singleSelectOptionId: "OPTION_ID" }
    ]
  }) {
    issue { id title }
  }
}
```

Each field entry takes a `fieldId` plus exactly one value parameter:

| Field type | Value parameter | Format |
| --- | --- | --- |
| Date | `dateValue` | ISO 8601 date string |
| Text | `textValue` | String |
| Number | `numberValue` | Float |
| Single select | `singleSelectOptionId` | Option ID |

To clear a value, set `delete: true` instead of a value parameter.

## Example

```bash
gh api graphql \
  -H "GraphQL-Features: issue_fields" \
  -f query='
mutation {
  setIssueFieldValue(input: {
    issueId: "I_kwDOxxx"
    issueFields: [
      { fieldId: "IFD_startDate", dateValue: "2026-04-01" }
      { fieldId: "IFD_targetDate", dateValue: "2026-04-30" }
      { fieldId: "IFSS_priority", singleSelectOptionId: "OPTION_P1" }
    ]
  }) {
    issue { id title }
  }
}'
```

## Searching by field values

The most reliable path is to fetch issues through GraphQL and filter by `issueFieldValues`.
Qualifier-based field search remains inconsistent across environments.
