---
name: microsoft-extensions-dependency-injection
description: 'Organize Microsoft.Extensions.DependencyInjection registrations with clear Add* extension methods, correct singleton/scoped/transient lifetimes, explicit scope creation, and reusable startup wiring. Use when cleaning up Program.cs, fixing DI lifetime bugs, or making registration reusable in tests.'
---

# Microsoft Extensions Dependency Injection

Use this skill when the task is about `Microsoft.Extensions.DependencyInjection` registration shape,
service lifetimes, or explicit scope management in .NET applications.

## When to Use This Skill

- User wants to organize or clean up a large `Program.cs` registration block
- User wants feature-scoped `Add*` extension methods
- User wants help choosing singleton, scoped, or transient lifetimes
- User needs to fix scoped-in-singleton or background-service scope issues
- User wants production DI composition to be reusable in tests
- User wants cleaner library integration with `IServiceCollection`

## Prerequisites

- The relevant startup composition code, service registrations, and consumer lifetimes can be
  inspected.
- The feature or module boundaries are known well enough to group related registrations cleanly.

## Workflow

### 1. Inspect the current registration surface

- Identify where registrations currently live.
- Find large flat registration blocks, unclear boundaries, and lifetime mismatches.
- Check whether background services or other singleton flows are resolving scoped services.

### 2. Group registrations into explicit composition methods

- Prefer `Add{Feature}Services()` or similarly clear extension methods.
- Keep the extension method next to the feature it wires.
- Keep startup composition readable and layer-aware without adding unnecessary abstraction.

### 3. Choose lifetimes intentionally

- Use singleton for stateless, thread-safe shared services.
- Use scoped for request or unit-of-work state.
- Use transient for lightweight short-lived helpers.
- Make scope creation explicit when the runtime does not provide one automatically.

### 4. Reuse composition in tests

- Reuse the same registration extensions in tests when possible.
- Override only infrastructure seams or external dependencies that differ in test scenarios.
- See [advanced-patterns.md](./references/advanced-patterns.md) for testing reuse, keyed/factory
  registration, and scope-management examples.

### 5. Avoid common DI anti-patterns

- Do not leave unrelated registrations mixed together in large startup files.
- Do not capture scoped dependencies in singleton constructors.
- Do not hide important configuration inputs or conditional behavior inside vague helpers.

## Related guidance

- Pair this with [Microsoft Extensions Configuration](../microsoft-extensions-configuration/SKILL.md)
  when options binding and DI composition are designed together.

## Gotchas

- **Do not inject scoped services into singletons without creating scopes at the point of use**.
- **Do not default every service to scoped**; the right lifetime depends on state and usage.
- **Do not create vague `AddServices()` methods** that obscure feature boundaries.
- **Do not duplicate production registration logic in tests** if the same extension methods can be
  reused safely.

## References

- [Microsoft Extensions Dependency Injection instructions](../../instructions/microsoft-extensions-dependency-injection.instructions.md)
- [Microsoft Extensions Dependency Injection agent](../../agents/microsoft-extensions-dependency-injection.agent.md)
- Local advanced patterns reference:
  [advanced-patterns.md](./references/advanced-patterns.md)
- Upstream source adapted from:
  <https://github.com/Aaronontheweb/dotnet-skills/tree/master/skills/microsoft-extensions-dependency-injection>
