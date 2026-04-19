---
description: 'Guidance for end-to-end .NET concurrency design: hosted services, queues, resource limits, shutdown, and concurrency observability.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/dotnet-concurrency-specialist.agent.md, .agents/skills/dotnet-concurrency-specialist/**, .agents/instructions/dotnet-concurrency-specialist.instructions.md'
---

# Dotnet Concurrency Specialist Guidance

Use these rules when the task is about broader .NET concurrency system design rather than one
isolated code-level pattern.

## Core model

- Review concurrent flows end to end: ingress, buffering, execution, downstream calls, and shutdown.
- Treat throughput, resource limits, and observability as part of the design, not afterthoughts.
- Keep this slice distinct from `csharp-concurrency-patterns`, which stays focused on code-level
  coordination primitives.

## Design rules

- Bound concurrency based on downstream capacity and runtime constraints.
- Keep queue ownership, retries, batching, and backpressure explicit.
- Create DI scopes deliberately inside concurrent workers when scoped services are involved.
- Respect DB, HTTP, and thread-pool limits instead of assuming async alone removes bottlenecks.

## Operational rules

- Make graceful stop, queue draining, and partial-failure handling explicit.
- Expose backlog, lag, retry, and failure signals so operations can see concurrency distress.
- Keep resource and lifetime ownership visible in code and docs.

## Verification

- Confirm the whole worker or pipeline boundary is understood.
- Confirm throughput limits and downstream bottlenecks are explicit.
- Confirm shutdown and draining behavior are correct.
- Confirm observability is strong enough to diagnose backlog or concurrency failures.
