# Repository Validation and CI

Use this reference when the task is about how contributors validate repository changes and how CI
should reinforce that validation.

## Start with the local validation path

Define the smallest useful local command surface first.

Examples:

- build and test commands for code repositories
- schema validation for structured metadata
- linting for docs or config when those are core repository assets
- custom repository scripts when repeated checks are too easy to forget

## CI should wrap local validation

Prefer CI that runs the same checks contributors can run locally.

- keep logic in repository-local scripts when the check is repository-specific
- avoid duplicating complex validation logic directly in workflow files
- document the expected local command in the README or repository guidance

When the repository's local validation path depends on focused tooling, pair this guidance with the
matching slice:

- `ci-workflows` for workflow design
- `python-quality` for the shared Python baseline
- `ruff-python` for lint or formatting
- `pyright-python` for type checking
- `git-hooks` for fast local hook feedback

## Validation priorities

Choose validation based on repository risk:

1. syntax and schema correctness
2. build or generation correctness
3. tests for behavior or contract stability
4. packaging validation when the repository distributes installable assets

## Common problems

| Problem | Likely cause | Fix |
| --- | --- | --- |
| CI is hard to understand | Validation logic is duplicated in workflows | Move repository-specific checks into scripts |
| Contributors skip important checks | Validation steps are undocumented or expensive | Make the main command explicit and lightweight |
| Automation exists but misses drift | The validation surface is incomplete | Add checks for the real repository contracts |
| The repository has workflows but no clear local path | CI was designed first | Define and document the local validation path first |
