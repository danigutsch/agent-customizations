# Source Generator Project Setup

Use this reference when the task is about creating, wiring, or packaging a Roslyn source
generator solution.

## Recommended solution layout

Prefer a solution shape that keeps the generator lifecycle obvious:

- `src/<Name>.Generator/` for the generator or analyzer package project
- `samples/<Name>.Demo/` or `test/<Name>.Consumer/` for a local consumer or demo project
- `test/<Name>.Generator.Tests/` for generator output and diagnostic tests
- optional release or packaging assets only when the repository actually publishes a package

Keep the generator project separate from the consuming application so analyzer-style references
and packaging behavior stay explicit.

## Project creation flow

1. Create the solution and generator class library.
2. Choose a compatible target framework and Roslyn package baseline for analyzer packaging.
3. Add a local consumer or demo project so the generated output can be observed during normal
   builds.
4. Add a dedicated test project for generated output, diagnostics, repeated-run stability, and
   edge cases.
5. Keep package metadata and release settings in the generator project or dedicated build files,
   not scattered across the consumer project.

## Local development wiring

When the goal is to run a generator from another project in the same solution, prefer a
project reference that behaves like an analyzer reference instead of a normal compile-time
library reference.

Typical pattern:

```xml
<ProjectReference Include="..\MyGenerator\MyGenerator.csproj"
                  OutputItemType="Analyzer"
                  ReferenceOutputAssembly="false" />
```

This keeps the generator active during normal builds without pulling its assembly into the
consumer application's runtime references.

## Setup guidance

- Prefer `IIncrementalGenerator` for new work.
- Keep generator-only dependencies minimal.
- Keep marker attributes and helper types deliberate:
  either embed them through post-initialization output or ship them intentionally.
- Keep consumer configuration explicit through attributes, conventions, or analyzer config values.

## Packaging guidance

- Package the generator as an analyzer or source-generator package, not as a normal runtime-only
  library.
- Avoid packaging decisions that accidentally expose generator implementation assemblies as normal
  application references.
- Keep runtime dependencies and generation-time dependencies distinct.
- If the package should not ship the normal build output, configure the project accordingly and
  validate the pack result before publishing.

## Common setup problems

| Problem | Likely cause | Fix |
| --- | --- | --- |
| Consumer project does not trigger generation | Project reference is treated as a normal reference | Use analyzer-style project reference metadata |
| Generator works locally but package consumer fails | Pack output does not preserve analyzer packaging behavior | Validate `dotnet pack` output and package layout |
| Duplicate marker attributes appear | Helper types are emitted more than once | Centralize helper emission and choose one strategy |
| Generator is hard to debug | No local consumer or demo project exists | Add a small consumer project dedicated to development |

## Related references

- [Testing and CI](./testing-and-ci.md)
- [Source generation skill](../SKILL.md)
