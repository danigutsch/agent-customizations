---
name: csharp-type-design-performance
description: 'Design .NET types and APIs for performance using sealed classes, readonly value types, allocation-aware method shapes, deferred enumeration, and deliberate collection choices. Use when choosing between class and struct, reducing allocations, or reviewing hot-path API shape.'
---

# C# Type Design Performance

Use this skill when the task is about performance-aware type shape, API boundaries, or allocation
behavior in C# and .NET.

## When to Use This Skill

- User is choosing between class, struct, record, or record struct
- User wants to reduce allocations or improve hot-path API shape
- User is deciding whether a class should be sealed
- User needs guidance on collection return types or premature materialization
- User is considering `ValueTask`, spans, pooling, or frozen collections

## Prerequisites

- The relevant types, public APIs, collection boundaries, and allocation-sensitive paths can be
  inspected.
- The code path is understood well enough to distinguish semantic design needs from speculative
  micro-optimization.

## Workflow

### 1. Start with semantics before micro-optimization

- Decide whether the type represents identity semantics, value semantics, or pure behavior.
- Seal classes unless inheritance is an intentional part of the contract.
- Prefer immutable value types only when the size and usage pattern justify them.

### 2. Shape APIs deliberately

- Prefer static pure functions when no instance state or polymorphism is needed.
- Keep dependencies explicit and public mutability boundaries narrow.
- Return read-only or immutable collections from API boundaries.

### 3. Control enumeration and materialization

- Defer `.ToList()` or equivalent materialization until the code truly needs it.
- Avoid repeated enumeration and multiple materializations in one flow.
- See [advanced-patterns.md](./references/advanced-patterns.md) for value-type, enumeration,
  `ValueTask`, and buffer-oriented examples.

### 4. Use lower-level performance tools carefully

- Use `ValueTask` only where synchronous completion is common enough to matter.
- Use spans, memory, pooling, or frozen collections only when they materially improve the real path.
- Keep maintenance cost in view when introducing lower-level abstractions.

### 5. Avoid common type-performance mistakes

- Do not leave accidental inheritance points in performance-sensitive code.
- Do not model ordinary mutable domain objects as structs.
- Do not expose mutable internal collections directly.
- Do not cargo-cult allocation optimizations into non-critical paths.

## Related guidance

- Pair this with [C# Concurrency Patterns](../csharp-concurrency-patterns/SKILL.md) when hot-path
  allocations affect async throughput or queue processing.

## Gotchas

- **Do not use `ValueTask` by default**; `Task` is often the clearer choice.
- **Do not use mutable structs** as everyday application models.
- **Do not return mutable implementation collections** from public APIs.
- **Do not add spans or pooling** unless the path truly benefits from lower-level control.

## References

- [C# Type Design Performance instructions](../../instructions/csharp-type-design-performance.instructions.md)
- [C# Type Design Performance agent](../../agents/csharp-type-design-performance.agent.md)
- Local advanced patterns reference:
  [advanced-patterns.md](./references/advanced-patterns.md)
- Upstream source adapted from:
  <https://github.com/Aaronontheweb/dotnet-skills/tree/master/skills/csharp-type-design-performance>
