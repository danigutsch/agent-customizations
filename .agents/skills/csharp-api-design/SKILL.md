---
name: csharp-api-design
description: Guidance for C# API shape and evolution. Use when designing or reviewing factory methods, result-returning APIs, DTO and domain boundaries, records versus classes, extension points, or compatibility-sensitive public surfaces in .NET code.
---

# Csharp Api Design

Use this skill when the task is about C# API shape and boundary design rather than broad coding
standards.

## When to Use This Skill

- The user needs to design or review a public or domain-facing C# API
- The user needs to decide between records, classes, readonly value types, or result wrappers
- The user needs clearer factory-method or validation entry-point guidance
- The user needs DTO, command, query, and domain boundaries to stay explicit
- The user needs compatibility-aware API evolution guidance for a reusable surface

## Prerequisites

- The current public types, factories, DTOs, or intended consumer boundary can be inspected.
- The main concern is API shape and evolution, not only formatting or naming style.

## Workflow

### 1. Identify the boundary

- Decide whether the surface is domain, application, transport, or reusable public API.
- Keep the intended consumer explicit.

### 2. Make validation and failure shape explicit

- Prefer factories or clear update methods when invariants must hold.
- Keep result and error patterns consistent across similar APIs.

### 3. Choose type shapes deliberately

- Use records for immutable message-like contracts when that improves clarity.
- Use sealed classes or readonly value types when identity, mutability, or value semantics require
  them.
- Keep extension points deliberate instead of accidental.

### 4. Plan for evolution

- Prefer additive evolution for already-consumed surfaces.
- Call out when compatibility is source-only, binary-sensitive, or wire-sensitive.

## Related guidance

- Pair with [Csharp Type Design Performance](../csharp-type-design-performance/SKILL.md) when API
  shape also affects allocation and ownership.
- Pair with [Aspnet API Contracts](../aspnet-api-contracts/SKILL.md) when the boundary is also an
  HTTP contract.
- Pair with [Grpc Protobuf Contracts](../grpc-protobuf-contracts/SKILL.md) when the API is also a
  wire contract.

## Gotchas

- **Do not turn this into a generic coding-standards checklist.**
- **Do not let transport and domain models merge by accident.**
- **Do not leave concrete types unsealed without an extension model.**
- **Do not introduce extra wrapper types unless the complexity really earns them.**

## References

- [Csharp api design guidance](../../instructions/csharp-api-design.instructions.md)
- [Csharp api design agent](../../agents/csharp-api-design.agent.md)
- Upstream naming adapted from:
  <https://github.com/Aaronontheweb/dotnet-skills/tree/master/skills/csharp-api-design>
