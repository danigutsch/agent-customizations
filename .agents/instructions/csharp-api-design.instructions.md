---
description: 'Guidance for C# API design: type boundaries, result and validation shape, extension points, and compatibility-aware evolution.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/csharp-api-design.agent.md, .agents/skills/csharp-api-design/**, .agents/instructions/csharp-api-design.instructions.md'
---

# Csharp Api Design Guidance

Use these rules when the task is about designing or reviewing C# API shape rather than general code
style.

## Core model

- Treat API design as a boundary decision: domain, application, transport, or reusable public
  surface.
- Keep type shape, validation, and failure behavior explicit at that boundary.
- Prefer additive evolution over casual breaking changes when a surface may already be consumed.
- Keep transport, domain, and persistence types intentionally separate.

## Type-shape rules

- Use records, classes, readonly value types, and result wrappers deliberately based on semantics.
- Prefer immutable message-style types for commands, queries, DTOs, and integration events when that
  matches the boundary.
- Prefer domain types that own invariants rather than passive property bags with external validation.
- Seal concrete implementations that are not intended extension points.

## Validation and result rules

- Prefer explicit creation or update entry points that validate invariants.
- Keep repeated validation rules centralized so error messages and statuses stay consistent.
- Prefer result-returning APIs when business validation failures are part of normal control flow.
- Avoid layering extra value objects or builders unless the call-site complexity truly justifies them.

## Compatibility and evolution rules

- Prefer new overloads, new types, and opt-in behavior over modifying existing public signatures.
- Distinguish source, binary, and wire compatibility when the API crosses package or process
  boundaries.
- Use obsolescence and migration periods before removals on consumed public surfaces.

## Boundary rules

- Keep DTOs and wire models separate from domain entities.
- Keep commands and queries explicit when the API boundary is application-facing rather than
  transport-only.
- Prefer focused interfaces when external implementations are expected.
- Avoid broad "god" abstractions that become hard to evolve safely.

## Verification

- Confirm the boundary and intended audience of the API are explicit.
- Confirm creation, validation, and failure behavior are predictable.
- Confirm concrete types are sealed unless they are deliberate extension points.
- Confirm any evolution path is additive or clearly documented as breaking.
