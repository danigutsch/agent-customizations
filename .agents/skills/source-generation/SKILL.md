---
name: source-generation
description: 'Design, test, package, and debug Roslyn source generators. Use for setup, consumer wiring, diagnostics, snapshots, CI, and output fixes.'
---

# Source Generation

Use this skill for C# Roslyn source generator work, especially when the task involves
`IIncrementalGenerator`, generator architecture, project setup, diagnostics, testing,
packaging, or CI validation.

## When to Use This Skill

- User asks to create or extend a Roslyn source generator
- User asks how to structure a generator solution or bootstrap a new project
- User asks how to wire a local consumer or demo project to a generator during development
- User asks to migrate a classic generator to `IIncrementalGenerator`
- User reports wrong, missing, or unstable generated output
- User wants better diagnostics, hint names, or deterministic generation
- User wants source generator tests, snapshot coverage, performance fixes, or NuGet packaging guidance
- User wants CI validation for restore, build, test, or pack flows around a generator package

## Prerequisites

- A generator contract is known or can be defined:
  trigger attribute/convention, eligible symbols, expected output, and diagnostics.
- The .NET SDK and package restore work for the relevant solution or project.
- If the task is performance-sensitive, a reproducible baseline exists
  (slow IDE experience, slow builds, unstable output, or failing tests).

## Workflow

### 1. Define the contract first

- Identify the trigger mechanism:
  marker attribute, additional file, analyzer config option, or explicit convention.
- List exactly which symbols are eligible and which are not.
- Define the emitted artifacts, hint-name strategy, and diagnostic behavior.
- Keep the generator additive-only. Generators add source; they do not rewrite user code.

### 2. Set up the solution shape when needed

- Prefer a solution that keeps the generator project, a local consumer or demo project,
  and a dedicated test project close together.
- Wire local consumers with analyzer-style project references so the generator runs during
  normal development builds.
- Treat packaging and CI as part of the lifecycle when the generator is meant for reuse.
- See [Project setup reference](./references/project-setup.md) for the recommended structure.

### 3. Shape the incremental pipeline

- Prefer `IIncrementalGenerator` unless legacy compatibility is explicitly required.
- Use `ForAttributeWithMetadataName` when attributes can drive discovery.
- Keep syntax predicates cheap and move semantic work into transforms.
- Model the pipeline as small, cacheable stages:
  discovery, projection, normalization, emission, diagnostics.

### 4. Normalize to equatable models

- Extract only the data needed for generation.
- Prefer immutable, value-equatable models (`record`, `record struct`,
  or explicit comparers when collections are involved).
- Prefer `var` for local declarations when the initializer already makes the type obvious. Switch to
  an explicit local type only when it improves readability.
- Avoid carrying `ISymbol`, `SyntaxNode`, `Location`, or semantic models
  through long-lived pipeline models.
- Keep ordering explicit and stable before emission.

### 5. Emit deterministic code

- Separate parsing/model creation from emission.
- Use stable hint names, namespaces, accessibility, and nullable context.
- Prefer writing source text directly rather than building syntax trees
  and calling `NormalizeWhitespace`.
- Generate the smallest useful API surface.

### 6. Add diagnostics and consumer ergonomics

- Report actionable diagnostics with stable IDs and precise locations.
- Use `RegisterPostInitializationOutput` when the generator needs to provide
  marker attributes or helper types.
- Flow optional build configuration through analyzer config options or MSBuild
  properties only when code-based configuration is insufficient.
- Think through packaging and consumer experience:
  package references, marker attributes, defaults, and breaking changes.

### 7. Test and verify

- Add positive-generation tests, invalid-input diagnostic tests,
  and edge cases such as nested types, generics, and nullability.
- Prefer snapshot or golden-file tests for larger generated outputs that need broad structural
  coverage, but keep focused assertion tests for diagnostics and critical invariants.
- Add stability checks when output ordering, hint naming, or caching is important.
- Build and run the relevant tests.
- Inspect generated files when the output shape does not match expectations.
- See [Testing and CI reference](./references/testing-and-ci.md) for lifecycle validation.

## Related skills

- If the work also restructures application code into feature-first boundaries,
  pair this with [Vertical slice architecture](../vertical-slice-architecture/SKILL.md).

## Gotchas

- **Generators are additive only** — do not design them as code rewriters or pseudo-language
  features. Roslyn source generators add code; they do not mutate existing source.
- **Do not keep `ISymbol` or `SyntaxNode` in long-lived models** — this breaks incrementality,
  equality, and can retain expensive compilation state.
- **Do not do semantic work in syntax predicates** — keep predicates cheap and move real work
  into transforms to protect IDE responsiveness.
- **Do not rely on indirect interface/base-type scanning** — broad inheritance scans are a known
  performance trap for generators and are explicitly discouraged in Roslyn guidance.
- **Do not depend on enumeration order** — dictionary iteration and unstable collections will
  produce noisy diffs and flaky tests unless you sort explicitly.
- **Do not use timestamps, machine paths, or random values in generated code** — output must be
  deterministic for cache hits, reviewability, and reproducible builds.

## Troubleshooting

| Issue | Likely cause | What to do |
| --- | --- | --- |
| Generator emits nothing | Discovery contract is wrong or too strict | Re-check trigger attribute/convention and verify eligible symbols reach the transform |
| Generator reruns too often | Non-equatable models or unstable data | Replace symbols/nodes with value data, add comparers, and remove volatile fields |
| Output order changes between runs | Unstable collection ordering | Sort inputs before emission and centralize hint-name generation |
| Diagnostics appear on the wrong code | Missing or incorrect location mapping | Report diagnostics with the exact symbol or syntax location the user needs to fix |
| IDE feels slow while typing | Too much work in syntax filtering or broad semantic scans | Use `ForAttributeWithMetadataName`, cheap predicates, and smaller immutable models |
| Packaged generator causes duplicate helper types | Marker/helper types are emitted without isolation strategy | Use post-initialization output plus embedded attributes or ship shared marker types intentionally |
| Consumer project does not run the local generator | Project reference is not wired as an analyzer | Use analyzer-style project reference metadata and rebuild the consumer project |
| Snapshot tests are noisy | Output includes unstable ordering or volatile text | Sort deterministically first and keep snapshots focused on stable generated structure |
| CI passes build but misses generator regressions | Workflow does not run generator tests or pack validation | Include restore, build, test, and pack validation where package delivery matters |

## References

- Local lifecycle setup reference:
  [project-setup.md](./references/project-setup.md)
- Local testing and CI reference:
  [testing-and-ci.md](./references/testing-and-ci.md)
- Roslyn incremental generators design:
  <https://github.com/dotnet/roslyn/blob/main/docs/features/incremental-generators.md>
- Roslyn incremental generators cookbook:
  <https://github.com/dotnet/roslyn/blob/main/docs/features/incremental-generators.cookbook.md>
- Aaron Powell's Roslyn incremental generator specialist:
  <https://github.com/Aaronontheweb/dotnet-skills/blob/master/agents/roslyn-incremental-generator-specialist.md>
