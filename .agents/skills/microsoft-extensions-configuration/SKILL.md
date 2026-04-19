---
name: microsoft-extensions-configuration
description: 'Configure Microsoft.Extensions options and configuration with strongly typed binding, startup validation, named options, and the right IOptions lifetime. Use when working on appsettings binding, IValidateOptions, ValidateOnStart, or clean fail-fast configuration patterns in .NET apps.'
---

# Microsoft Extensions Configuration

Use this skill when the task is about `Microsoft.Extensions.Configuration` and the Options pattern
in .NET applications.

## When to Use This Skill

- User wants to bind configuration sections to strongly typed settings classes
- User wants configuration validation to fail fast at startup
- User wants to implement or fix `IValidateOptions<T>`
- User wants to choose between `IOptions<T>`, `IOptionsSnapshot<T>`, and `IOptionsMonitor<T>`
- User wants named options or `PostConfigure` patterns
- User wants validator tests or cleaner configuration consumption patterns

## Prerequisites

- The relevant settings classes, registration code, and appsettings files can be inspected.
- The application startup path is known well enough to place options registration and validation in
  the correct composition location.

## Workflow

### 1. Model the settings type

- Prefer a dedicated settings class with a clear section-name constant or equivalent convention.
- Keep the shape aligned with the real config section instead of compensating with ad-hoc mapping.
- Use deliberate defaults only when they are genuinely safe.

### 2. Bind through the options pipeline

- Prefer `AddOptions<T>()` and `BindConfiguration()` for the standard registration path.
- Keep registration in startup or DI composition code instead of spreading it through services.
- Keep configuration consumers strongly typed whenever practical.

### 3. Add the right validation layer

- Use Data Annotations for simple required/range/format checks.
- Use `IValidateOptions<T>` for cross-property rules, conditional rules, and validation with
  dependencies.
- Prefer `ValidateOnStart()` when invalid configuration should stop the app before runtime traffic.
- See [advanced-patterns.md](./references/advanced-patterns.md) for dependency-aware validators,
  named options, and validator testing patterns.

### 4. Pick the right options lifetime

- Use `IOptions<T>` for effectively static singleton-style reads.
- Use `IOptionsSnapshot<T>` for scoped request-time reads.
- Use `IOptionsMonitor<T>` when singleton/background services need updates or change callbacks.

### 5. Avoid common configuration anti-patterns

- Replace repeated `configuration["Section:Key"]` usage in services when a settings type is more
  maintainable.
- Avoid constructor-only validation as the sole guard if the options pipeline should own validation.
- Keep environment-specific secrets or user-local values out of shared examples and committed config.

## Related guidance

- Pair this with [CI workflows](../ci-workflows/SKILL.md) when startup validation or configuration
  tests should be enforced in CI.

## Gotchas

- **Do not skip `ValidateOnStart()` by accident** when the goal is fail-fast startup validation.
- **Do not throw from `IValidateOptions<T>` for normal validation failures**; return a failure result
  instead so errors aggregate cleanly.
- **Do not choose the wrong options lifetime**; the lifetime must match reload expectations and the
  consuming service shape.
- **Do not normalize everything with silent defaults** when missing required configuration should be
  explicit.

## References

- [Microsoft Extensions Configuration instructions](../../instructions/microsoft-extensions-configuration.instructions.md)
- [Microsoft Extensions Configuration agent](../../agents/microsoft-extensions-configuration.agent.md)
- Local advanced patterns reference:
  [advanced-patterns.md](./references/advanced-patterns.md)
- Upstream source adapted from:
  <https://github.com/Aaronontheweb/dotnet-skills/tree/master/skills/microsoft-extensions-configuration>
