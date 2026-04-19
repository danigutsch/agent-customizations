---
name: event-sourcing-projections
description: Guidance for event-sourced read models and projection operations. Use when designing or reviewing projection handlers, read-model boundaries, checkpoint storage, replay safety, rebuild workflows, eventual-consistency behavior, single-stream or multi-stream views, or Marten-style projection lifecycles.
---

# Event Sourcing Projections

Use this skill when the task is about event-sourced projections and read models rather than general
event-sourcing theory alone.

## When to Use This Skill

- The user needs to design or review an event-sourced read model
- The user needs guidance for projection checkpoints, replay, or rebuild workflows
- The user needs to choose between inline, async, and live projection styles
- The user needs to design single-stream or multi-stream projection boundaries
- The user needs projection-runner readiness, lag, or operational guidance
- The user needs focused tests for projection correctness or rebuild recovery

## Prerequisites

- The event types, projection handlers, or intended read models can be inspected.
- The consistency expectations for the consumer-facing read model are known well enough to evaluate.
- The task is specifically about projection behavior, not only command or aggregate design.

## Workflow

### 1. Identify the read model and event sources

- List the read model or query surface the projection serves.
- Identify which event streams or event types legitimately feed that view.
- Decide whether the projection is single-stream or multi-stream.

### 2. Choose the lifecycle honestly

- Use inline projections when the read model must be current in the same write transaction.
- Use async projections when eventual consistency is acceptable and background recovery matters.
- Use live projections when the query is rare or exploratory enough that persisted storage is not
  worth the complexity.

### 3. Make replay and checkpoint behavior explicit

- Persist a stable projection name and monotonic checkpoint.
- Keep handlers deterministic so rebuilds converge to the same state.
- Treat checkpoint reset and replay as supported workflows, not only disaster recovery.

### 4. Validate the operational surface

- Expose projection lag, runner health, or readiness when consumers depend on freshness.
- Keep rebuild and recovery procedures documented and testable.
- Add focused tests for representative event sequences and at least one rebuild path when state is
  persisted.

### 5. Document optional Marten-style upgrades

- Call out practices that Marten models explicitly even if the current repo does not.
- Examples include inline versus async versus live lifecycle taxonomy, first-class multi-stream
  projections, update-only projection semantics, and daemon-style async projection operations.

## Related guidance

- Pair with [Xunit V3 Mtp Test Stack](../xunit-v3-mtp-test-stack/SKILL.md) when replay, rebuild, or
  checkpoint logic needs .NET test-stack guidance.
- Pair with [Database Performance](../database-performance/SKILL.md) when projection-backed read
  models or denormalized views need query-shape tuning.
- Pair with [Aspnet API Contracts](../aspnet-api-contracts/SKILL.md) when projection-backed read
  models are exposed through HTTP endpoints.
- Pair with [Opentelemetry Dotnet](../opentelemetry-dotnet/SKILL.md) when projection runners need
  better lag, failure, or rebuild observability.

## Gotchas

- **Do not let eventually consistent read models pretend they are transactionally current.**
- **Do not hide rebuild requirements until after a projection becomes operationally critical.**
- **Do not assume a single projection should satisfy every reporting view.**
- **Do not let update events create malformed views when the base record should have existed first.**
- **Do not treat Marten-specific terminology as mandatory if the underlying pattern is what matters.**

## References

- [Event sourcing projections guidance](../../instructions/event-sourcing-projections.instructions.md)
- [Event sourcing projections agent](../../agents/event-sourcing-projections.agent.md)
