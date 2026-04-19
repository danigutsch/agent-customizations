---
description: 'Standards for C# and .NET type design performance covering sealed classes, readonly value types, allocation-aware APIs, collection boundaries, and enumeration behavior.'
applyTo: '**/*.cs, **/*.csproj'
---

# C# Type Design Performance Standards

Use these rules when the task involves type shape, API boundaries, collection design, or
allocation-sensitive patterns in C# or .NET.

## Type selection

- Prefer `sealed` classes for concrete implementations that are not intentional extension points.
- Prefer `readonly struct` or `readonly record struct` for small immutable value types with value
  semantics.
- Prefer classes for larger objects, shared references, or mutable state with identity semantics.
- Avoid mutable structs for general-purpose domain or application modeling.

## Method and API shape

- Prefer static pure functions when behavior does not rely on instance state or polymorphism.
- Keep dependencies explicit instead of hiding them behind incidental object state.
- Keep public API boundaries intentional about mutability, ownership, and enumeration behavior.
- Return read-only or immutable collection views from public boundaries rather than mutable
  implementation collections.

## Enumeration and materialization

- Defer materialization until the code truly needs a realized collection.
- Avoid repeated enumeration or multiple unnecessary `.ToList()` calls in the same flow.
- Choose the return shape deliberately:
  `IReadOnlyList<T>` for materialized ordered data, `IReadOnlyCollection<T>` for size-focused
  contracts, and `IEnumerable<T>` only when laziness is genuinely useful and safe.
- Keep ordering and re-enumeration costs explicit when returning lazy sequences.

## Allocation-sensitive patterns

- Use `Task` by default for asynchronous APIs; use `ValueTask` only when synchronous completion is
  common enough to justify it.
- Use `Span<T>` or `Memory<T>` only where low-level parsing, buffer slicing, or copy reduction is a
  real concern.
- Use array pooling or frozen collections when the workload justifies the added complexity and the
  lifecycle is clear.
- Favor simple, correct code over speculative allocation tuning outside verified hot paths.

## Immutability and ownership

- Keep immutable value types truly immutable.
- Avoid exposing mutable internal collections or buffers directly.
- Prefer copying or read-only wrappers at boundaries where ownership must stay internal.

## Anti-patterns

- Do not leave unsealed classes open for inheritance without a deliberate extension model.
- Do not use mutable structs with settable fields or properties as everyday domain types.
- Do not return `List<T>` or other mutable implementation types from public APIs without a specific
  reason.
- Do not introduce `ValueTask`, spans, or pooling as cargo-cult optimizations.

## Verification

- Confirm the chosen type shape matches the intended semantics.
- Confirm public collection boundaries do not leak mutable internal state.
- Confirm materialization and enumeration happen only where needed.
- Confirm low-level performance tools are used only where the path justifies their complexity.
