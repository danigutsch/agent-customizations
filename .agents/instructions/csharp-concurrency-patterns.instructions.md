---
description: 'Standards for C# and .NET concurrency covering async task coordination, channels, bounded parallelism, cancellation, and shared-state minimization.'
applyTo: '**/*.cs, **/*.csproj'
---

# C# Concurrency Patterns Standards

Use these rules when the task involves asynchronous coordination, background work, producer /
consumer pipelines, or shared-state concurrency decisions in C# or .NET.

## Concurrency model selection

- Prefer plain `async` / `await` for ordinary I/O-bound concurrency before introducing heavier
  abstractions.
- Prefer `Task.WhenAll` or `Task.WhenAny` for coordinating independent async operations.
- Prefer `Parallel.ForEachAsync` for bounded fan-out over collections when controlled parallelism is
  needed.
- Prefer `System.Threading.Channels` for producer / consumer, work-queue, or serialized-consumer
  patterns.
- Escalate to more specialized frameworks only when the built-in primitives clearly stop fitting the
  problem.

## Cancellation and shutdown

- Accept and pass through `CancellationToken` in long-running, repeated, or externally controlled
  async work.
- Check cancellation at loop boundaries and before expensive repeated work.
- Keep shutdown behavior explicit for queues, background services, and periodic workers.
- Complete writers or stop producers deliberately so consumers can drain and exit cleanly.

## Shared state

- Prefer immutable data, local ownership, partitioning, or serialized message handling over shared
  mutable state.
- Use concurrent collections only when shared access is unavoidable and the collection semantics
  match the real access pattern.
- Use `lock` only for simple, short-lived critical sections when higher-level designs do not fit.
- Keep synchronization boundaries narrow and easy to reason about.

## Throughput and coordination

- Bound concurrency intentionally based on downstream limits such as APIs, databases, or CPU.
- Make ordering guarantees explicit when parallel work is recombined.
- Add buffering or backpressure only when producers and consumers run at meaningfully different
  speeds.
- Avoid starting unbounded background tasks that are difficult to observe, cancel, or await.

## Background and periodic work

- Prefer clear async loops or `PeriodicTimer` over manual thread management.
- Keep each iteration small, cancellable, and explicit about scope lifetime and error handling.
- Separate queue ingestion from queue consumption when producers and consumers need different
  lifecycles.

## Anti-patterns

- Do not block on async work with `.Result`, `.Wait()`, or similar sync-over-async patterns.
- Do not use manual `Thread` creation when task-based or hosted-service abstractions fit.
- Do not mix multiple concurrency models in the same flow without a strong reason.
- Do not ignore queue completion, draining, or cancellation in background processors.

## Verification

- Confirm the chosen abstraction matches the actual concurrency problem.
- Confirm cancellation is propagated through repeated and long-running work.
- Confirm shared mutable state is minimized or protected with the smallest workable mechanism.
- Confirm throughput limits, ordering, and shutdown behavior are explicit.
