---
description: 'Standards for C# Roslyn source generators covering setup, incrementality, diagnostics, testing, packaging, and CI validation.'
applyTo: '**/*Generator*.{cs,csproj}, **/Generators/**/*.{cs,csproj,props,targets}, **/SourceGeneration/**/*.{cs,csproj,props,targets}'
---

# C# Source Generation Standards

Use these rules only when the task involves a Roslyn source generator, analyzer package,
or supporting generator infrastructure.

## Scope and architecture

- Define the generator contract before coding:
  trigger mechanism, eligible symbols, emitted artifacts, diagnostics, and compatibility rules.
- Keep source generation additive-only. Do not treat generators as code rewriters or custom
  language features.
- Prefer `IIncrementalGenerator`; use legacy `ISourceGenerator` only when compatibility
  requirements make it necessary.
- When the task includes bootstrapping or lifecycle work, prefer a solution shape that keeps the
  generator project, a local consumer or demo project, and a dedicated test project close together.
- Separate discovery, projection, normalization, emission, and diagnostics.
- For larger generators, prefer parser/emitter separation and role-based files over one large,
  mixed-responsibility implementation.

## Project setup and local wiring

- Prefer a dedicated generator project over mixing generator logic into the consumer application.
- Keep a local consumer or demo project available when active generator development needs fast
  feedback on emitted source.
- When wiring a local consumer to a generator project, prefer analyzer-style project references so
  the generator runs during ordinary builds without becoming a normal runtime reference.
- Keep package metadata and generator-specific build behavior in the generator project or closely
  related build files.
- If the repository also uses feature-first application organization, keep generator infrastructure
  separate from application slices and pair with
  [vertical-slice-architecture instructions](./vertical-slice-architecture.instructions.md) only
  where generated APIs affect slice boundaries.

## Incremental pipeline rules

- Prefer `SyntaxProvider.ForAttributeWithMetadataName` when an attribute can drive discovery.
- Keep syntax predicates cheap and structural only.
- Move semantic binding into transform steps.
- Call `Collect()` only after projecting to compact immutable models.
- Flow configuration as data through the pipeline instead of branching inside the emitter.
- Propagate `CancellationToken` through expensive parsing and emission work.

## Model and equality rules

- Intermediate models must be immutable and value-equatable.
- Prefer `record` or `record struct` for generator models.
- Prefer `var` for local declarations when the initializer already makes the type obvious. Use an
  explicit local type only when it materially improves readability or is required by the API shape.
- Do not carry `ISymbol`, `SyntaxNode`, `Location`, `Compilation`, or semantic models in
  long-lived pipeline data.
- Extract stable identifiers instead:
  metadata names, fully qualified names, booleans, enums, normalized strings.
- Use explicit comparers when a model contains collections or when default equality is not enough.
- Do not use mutable shared state, static caches, or hidden side channels.

## Emission rules

- Emit deterministic source:
  stable hint names, explicit ordering, explicit namespaces, and stable formatting.
- Prefer writing source text directly over constructing syntax trees and calling
  `NormalizeWhitespace`.
- Use fully qualified type names when generation crosses namespaces or ambiguous usings.
- Preserve nullability context and accessibility correctness in generated members.
- Generate the smallest API surface that satisfies the contract.
- Centralize hint-name generation and keep it stable across versions.

## Diagnostics and UX

- Report user-correctable issues as diagnostics, not thrown exceptions.
- Use stable diagnostic IDs with a package-level prefix.
- Include a precise location whenever one is available.
- Keep messages concise, actionable, and specific about how to fix the input.
- Use `RegisterPostInitializationOutput` for embedded marker attributes or helper types when
  consumers should not author them manually.
- Prefer explicit code configuration (attributes, partial types, conventions) over opaque build
  properties when either approach would work.

## Performance and safety rules

- Do not scan the entire compilation for indirect interface implementation or deep inheritance
  patterns unless there is no cheaper contract.
- Do not perform broad semantic work for symbols that the user did not explicitly opt into.
- Do not emit timestamps, machine-specific paths, or other volatile values.
- Do not rely on dictionary enumeration order or unstable collection order.
- Do not over-generate: emit only for symbols that match the contract.

## Testing expectations

- Add or update tests for:
  - expected generated output
  - invalid input diagnostics
  - edge cases such as nested types, generics, partial types, and nullability
- Prefer snapshot or golden-file tests for larger generated source bodies.
- Use snapshot tests only after making output deterministic enough to avoid noisy churn.
- Keep focused assertion tests for diagnostics and important API invariants even when snapshots are
  used.
- Add stability checks when ordering, hint naming, or caching behavior matters.
- Verify the same inputs produce the same generated output across repeated runs.
- Keep test inputs minimal and representative.

## Packaging and consumer ergonomics

- Target a broadly compatible framework for generator packages unless the project has a stricter
  requirement.
- Keep dependencies minimal and appropriate for analyzer/source-generator packaging.
- Avoid packaging the generator as if it were a normal runtime dependency for consumers.
- Document or encode marker attributes, defaults, and configuration flow clearly.
- Treat contract changes as versioned behavior changes; avoid silent breaking changes in emitted
  API shape or diagnostics.
- Ensure generated APIs are discoverable and predictable for consuming projects.

## CI validation expectations

- At minimum, validate restore, build, and generator tests after changes.
- Add pack validation when the repository publishes or distributes the generator as a package.
- Keep CI guidance generator-focused here; use repository-wide GitHub Actions instructions for
  broader workflow structure, security, and deployment concerns.

## Anti-patterns to avoid

- Storing `ISymbol` or `SyntaxNode` in model types
- Using mutable `List<T>` or arrays in model equality without an explicit comparer strategy
- Doing semantic analysis inside syntax predicates
- Building emitted code from syntax trees just to stringify them
- Using generator output to hide complex runtime reflection or DI magic
- Emitting hidden failures instead of diagnostics
- Wiring the consumer project with an ordinary reference when analyzer-style behavior is required
- Relying on snapshot tests alone to prove generator correctness

## Verification

- Build the relevant generator and consumer test projects after changes.
- Inspect generated files when diagnosing incorrect output.
- Verify that the generator still behaves deterministically and only reacts to intended inputs.
