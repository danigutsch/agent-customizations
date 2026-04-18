# Source Generator Testing and CI

Use this reference when the task is about test strategy, snapshot coverage, repeated-run
stability, or CI validation for a Roslyn source generator project.

## Test strategy

Cover the generator from multiple angles:

- generated output tests for expected emitted members and files
- diagnostic tests for invalid inputs and precise locations
- edge-case tests for generics, nested types, nullability, and partial declarations
- repeated-run or stability tests when hint naming, ordering, or caching behavior matters

Prefer focused assertion tests for small invariants and use snapshot or golden-file tests when
the generated source is large enough that broad structure matters more than line-by-line hand
assertions.

## Snapshot testing guidance

Snapshot testing is useful when:

- generated source bodies are large or highly structured
- you want to review broad contract changes in diffs
- deterministic ordering and formatting are already enforced

Snapshot testing is not enough on its own:

- keep explicit tests for diagnostics
- keep explicit tests for key API invariants
- avoid snapshots that include volatile content or unstable ordering

## Local validation flow

Typical local validation flow:

1. Restore the solution.
2. Build the generator and any local consumer project.
3. Run the generator test project.
4. Inspect generated files or test output when shape or diagnostics do not match expectations.
5. Run `dotnet pack` if package delivery is part of the workflow.

## CI baseline

For most repositories, the minimum useful CI validation is:

1. set up the required .NET SDK
2. restore dependencies
3. build the solution or relevant projects
4. run generator tests
5. optionally pack the generator package when the repository publishes packages

Keep the workflow focused on validating the generator lifecycle rather than duplicating every
repository-wide build concern.

## CI design notes

- Prefer a single build-and-test path that exercises both the generator and its tests.
- Publish test results or failure artifacts when they materially help diagnose generator failures.
- Add a pack step when package layout is part of the contract.
- Reuse existing repository CI guidance for broader workflow structure and permissions.

## Common problems

| Problem | Likely cause | Fix |
| --- | --- | --- |
| Tests pass locally but fail in CI | SDK, path, or package assumptions differ | Pin the required SDK and keep paths deterministic |
| Snapshot churn is high | Output ordering or formatting is unstable | Sort deterministically and remove volatile values |
| Packaging issues appear only after release | Pack is not validated in CI | Add a pack validation step before publishing |
| Diagnostics regress without notice | Only snapshot tests exist | Add focused diagnostic assertions alongside snapshots |

## Related references

- [Project setup](./project-setup.md)
- [Source generation skill](../SKILL.md)
