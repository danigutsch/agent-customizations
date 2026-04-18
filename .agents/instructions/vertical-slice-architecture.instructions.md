---
description: 'Standards for vertical slice architecture covering domain-first organization, slice ownership, testing alignment, and migration.'
applyTo: '**/Domains/**/*.{cs,csproj,md}, **/Domain*/**/*.{cs,csproj,md}, **/Slices/**/*.{cs,csproj,md}, **/*Slice*.{cs,md}, **/Endpoints/**/*.{cs,md}'
---

# Vertical Slice Architecture Standards

Use these rules when the task involves domain-first organization, vertical slice boundaries, or
incremental migration away from layer-first structures.

## Scope and structure

- Organize by domain, bounded context, or business capability before organizing by technical layer.
- Place slices inside the domain that owns the behavior instead of defaulting to a repo-wide
  `Features/` folder.
- Prefer action-oriented slice names such as `CreateBooking`, `CancelReservation`, or
  `GetInvoice`.
- Let each slice own the request or command models, handlers, validators, endpoint glue, and tests
  needed to complete one use case end to end.
- Keep infrastructure and composition-root code explicit, but do not let shared infrastructure
  become the default home for application behavior.

## Slice ownership rules

- Keep each slice understandable in isolation.
- Keep controllers, endpoints, or minimal API handlers thin and explicit about which slice they
  invoke.
- Prefer local models inside a slice unless a shared type represents a stable, truly cross-cutting
  concept.
- Avoid shared service abstractions created only to remove small duplication across slices.

## Shared code and cross-cutting concerns

- Extract shared code only when multiple slices depend on the same stable concept.
- Keep validation, authorization, telemetry, and persistence seams visible.
- Do not hide important behavior in generic helper layers when a slice-specific type would be
  clearer.
- Accept small duplication when it preserves slice independence and readability.

## Testing expectations

- Align tests with slice boundaries.
- Prefer handler tests, endpoint tests, and integration tests that make the owning slice obvious.
- Avoid large shared test helper layers unless the reuse is stable and clearly beneficial.
- Keep migration-safe coverage around moved endpoints and handlers when refactoring from layered
  structures.

## Migration guidance

- Prefer incremental migration over big-bang rewrites.
- Move one use case or closely related group of use cases at a time.
- Preserve external behavior while clarifying ownership and dependencies.
- Keep old and new structures understandable during transition; do not leave ambiguous ownership.

## Related guidance

- If a slice depends on generated APIs or compile-time conventions, pair this with
  [source-generation instructions](./source-generation.instructions.md) for the generator-specific
  rules rather than duplicating those constraints here.

## Anti-patterns to avoid

- Recreating the same layer-first structure under a `Features` folder
- Using a generic top-level `Features/` folder when the real ownership is domain-specific
- Introducing a mediator, bus, or abstraction as a hard requirement when the project does not need
  it
- Centralizing domain logic in shared services that own too many unrelated use cases
- Splitting a single use case across many folders just to satisfy old architectural conventions

## Verification

- Confirm each modified use case has a clear owning slice.
- Confirm endpoints, handlers, validators, and tests align with that ownership.
- Confirm extracted shared code is genuinely cross-cutting and not just premature deduplication.
