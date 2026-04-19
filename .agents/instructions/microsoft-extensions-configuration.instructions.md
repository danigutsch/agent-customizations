---
description: 'Standards for Microsoft.Extensions configuration and options covering strongly typed binding, validation, startup behavior, and options lifetimes.'
applyTo: '**/*.cs, **/*.csproj, **/appsettings*.json'
---

# Microsoft Extensions Configuration Standards

Use these rules when the task involves `Microsoft.Extensions.Configuration`, the Options pattern,
or startup validation of configuration-bound settings.

## Configuration modeling

- Prefer strongly typed settings classes over repeated string-key configuration access in services.
- Give settings classes an explicit section-name constant or equally clear binding convention.
- Keep defaults intentional. Do not hide missing required values with placeholder defaults that make
  failures harder to diagnose.
- Keep nested configuration shapes explicit when the configuration structure is hierarchical.

## Binding and registration

- Prefer `AddOptions<T>()` plus `BindConfiguration()` when the project already uses the standard
  options pipeline.
- Keep binding registration close to application startup or DI composition code.
- Keep section paths stable and easy to discover from the settings type.

## Validation

- Use Data Annotations for simple required, range, and format rules.
- Use `IValidateOptions<T>` for cross-property validation, conditional validation, or validation
  that depends on injected services such as `IHostEnvironment`.
- Prefer `.ValidateOnStart()` when invalid configuration should stop the app during startup rather
  than fail later in business logic.
- Return `ValidateOptionsResult.Fail(...)` from validators instead of throwing exceptions for normal
  validation failures.

## Options lifetime

- Use `IOptions<T>` for singleton-style consumers that do not need runtime reload behavior.
- Use `IOptionsSnapshot<T>` for scoped consumers in web request pipelines.
- Use `IOptionsMonitor<T>` for singleton or background services that need change notifications or
  current values over time.
- Make the lifetime choice explicit when it affects correctness or reload semantics.

## Named options and post-configuration

- Use named options only when the repository truly needs multiple independently configured instances
  of the same settings type.
- Use `PostConfigure` for normalization or derived defaults that should happen after binding and
  before validation completes.
- Keep name-specific validation explicit and easy to trace.

## Anti-patterns

- Do not scatter `configuration["Section:Key"]` access throughout services when options binding is a
  better fit.
- Do not rely on constructor guard clauses as the primary configuration validation mechanism when the
  options pipeline can own validation centrally.
- Do not silently tolerate malformed critical configuration in production paths.

## Verification

- Confirm the settings class matches the real configuration structure.
- Confirm startup validation behavior matches the intended failure model.
- Confirm the selected options lifetime matches the consuming service lifetime and reload needs.
- Confirm validator logic is covered by focused tests when the rules are more than simple annotations.
