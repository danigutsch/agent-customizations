---
description: 'Standards for Microsoft.Extensions.DependencyInjection covering registration organization, Add* extension methods, service lifetimes, scopes, and testable composition.'
applyTo: '**/*.cs, **/*.csproj'
---

# Microsoft Extensions Dependency Injection Standards

Use these rules when the task involves `Microsoft.Extensions.DependencyInjection`, service
registration organization, lifetimes, or scope management.

## Registration organization

- Prefer explicit `Add*` extension methods to group related registrations by feature or layer when
  registration blocks grow large.
- Keep extension methods near the services they register so composition stays discoverable.
- Keep `Program.cs` or equivalent startup composition readable and intentionally structured.
- Use names such as `AddUserServices()` or `AddEmailServices()` that communicate what is being
  registered.

## Lifetimes

- Use singleton for stateless, thread-safe, shared services.
- Use scoped for per-request or per-unit-of-work services such as repositories and database contexts.
- Use transient for lightweight short-lived helpers or validators.
- Choose lifetimes intentionally based on state ownership, reuse, and thread-safety.

## Scope management

- Do not inject scoped services directly into singleton services unless the design explicitly creates
  scopes when those services are resolved.
- In background services, hosted services, actors, or other singleton-driven flows, create scopes
  explicitly when scoped services are required.
- Keep scope boundaries obvious at the point of work execution.

## Extension-method design

- Return `IServiceCollection` so registration methods compose fluently.
- Accept important configuration inputs explicitly rather than burying them as hidden assumptions.
- Use layered composition only when it clarifies boundaries instead of adding indirection for its own
  sake.

## Testing and reuse

- Prefer reusing production `Add*` registration methods in tests and overriding only test-specific
  dependencies.
- Keep registration code modular enough that tests can compose a near-production service collection
  without duplicating setup logic.

## Anti-patterns

- Do not leave large, flat registration lists in `Program.cs` when boundaries are unclear.
- Do not create vague registration methods such as `AddServices()` that hide what is being wired.
- Do not capture scoped dependencies in singleton constructors.
- Do not hide critical configuration or lifetime assumptions inside registration helpers.

## Verification

- Confirm registrations are grouped by meaningful boundaries.
- Confirm chosen lifetimes match actual state and usage patterns.
- Confirm scoped services are resolved within valid scopes in non-request execution paths.
- Confirm tests can reuse the same registration composition without excessive duplication.
