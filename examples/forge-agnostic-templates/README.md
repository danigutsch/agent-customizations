# Forge-agnostic templates example

This starter example shows the intended pattern for portable repository-host templates in this
repository.

## Canonical source

- Keep reusable issue and pull-request template content under `templates/`.

## Export targets

- Sync or copy host-specific discovered files only in the target repository:
  - `.github/ISSUE_TEMPLATE/`
  - `.github/pull_request_template.md`
  - `.gitlab/issue_templates/`
  - `.gitlab/merge_request_templates/`
  - `.gitea/ISSUE_TEMPLATE/`
  - `.gitea/PULL_REQUEST_TEMPLATE.md`

## Why

- `templates/` stays forge-agnostic and reusable.
- Host-native directories remain compatibility targets rather than the source of truth.
- The target repository still needs to decide which host-specific exports it actually wants to
  generate.
