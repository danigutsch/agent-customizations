---
name: dotnet-concurrency-specialist
description: Guidance for end-to-end .NET concurrency design. Use when reviewing hosted services, background queues, channel pipelines, scoped-service usage inside concurrent work, throughput limits, shutdown and draining behavior, or observability for worker backlog and retries.
---

# Dotnet Concurrency Specialist

Use this skill when the task is about concurrency at the .NET system level rather than about one
isolated async primitive.

## When to Use This Skill

- The user needs to review a hosted service, worker, queue, or background pipeline
- The user needs to reason about concurrency with DB, HTTP, or external resource limits
- The user needs shutdown, draining, or retry behavior to be explicit
- The user needs backlog, lag, or retry observability for concurrent workers
- The user needs a broader review than `csharp-concurrency-patterns` alone

## Prerequisites

- The current worker, queue, or background-processing flow can be inspected.
- The task is about overall concurrency behavior, not only one method-level async choice.

## Workflow

### 1. Map the full flow

- Identify ingress, buffering, execution, downstream calls, and exit.
- Find the real bottlenecks and resource ceilings.

### 2. Review lifetime and throughput

- Make DI scopes, DB usage, HTTP concurrency, and retries explicit.
- Bound concurrency and buffering intentionally.

### 3. Review shutdown and observability

- Confirm graceful stop and draining behavior.
- Add or review backlog, lag, retry, and failure telemetry.

## Related guidance

- Pair with [Csharp Concurrency Patterns](../csharp-concurrency-patterns/SKILL.md) when primitive
  choice is still the main question.
- Pair with [Microsoft Extensions Dependency Injection](../microsoft-extensions-dependency-injection/SKILL.md)
  when scoped service usage inside workers needs review.
- Pair with [Opentelemetry Dotnet](../opentelemetry-dotnet/SKILL.md) when worker health and lag need
  stronger telemetry.

## Gotchas

- **Do not stop at method-level async cleanup when the real problem is pipeline design.**
- **Do not ignore resource ceilings such as DB connections or rate limits.**
- **Do not forget queue draining and shutdown.**

## References

- [Dotnet concurrency specialist guidance](../../instructions/dotnet-concurrency-specialist.instructions.md)
- [Dotnet concurrency specialist agent](../../agents/dotnet-concurrency-specialist.agent.md)
