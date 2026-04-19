---
name: csharp-concurrency-patterns
description: 'Choose practical .NET concurrency patterns using async/await, task coordination, channels, bounded parallelism, and minimal shared mutable state. Use when fixing async orchestration, background queues, cancellation, race conditions, or deciding whether locks are really necessary.'
---

# C# Concurrency Patterns

Use this skill when the task is about concurrency design, async coordination, background processing,
or shared-state safety in C# and .NET.

## When to Use This Skill

- User needs help choosing between `async` / `await`, task coordination, channels, or bounded
  parallelism
- User has a background worker, queue processor, or repeated polling loop to clean up
- User is dealing with race conditions, shared mutable state, or lock-heavy code
- User needs cancellation and shutdown to behave correctly in concurrent flows
- User wants to control throughput, buffering, or backpressure instead of starting unbounded work

## Prerequisites

- The current async entry points, background loops, producer / consumer flows, and shared-state
  boundaries can be inspected.
- The main constraint is understood well enough to tell whether the problem is I/O wait, CPU work,
  queueing, or state ownership.

## Workflow

### 1. Start with the smallest workable abstraction

- Prefer plain `async` / `await` for everyday I/O-bound concurrency.
- Use `Task.WhenAll` or `Task.WhenAny` when coordinating independent operations.
- Escalate only when the problem is clearly queueing, bounded fan-out, or shared-state ownership.

### 2. Choose the coordination model deliberately

- Use `Parallel.ForEachAsync` for bounded parallel processing over a collection.
- Use `Channel<T>` when producers and consumers need decoupling, buffering, or serialized
  consumption.
- See [advanced-patterns.md](./references/advanced-patterns.md) for channels, throttled fan-out,
  periodic work, and serialized shared-state examples.

### 3. Make cancellation and shutdown explicit

- Pass `CancellationToken` through all long-running and repeated async work.
- Keep queue completion, consumer draining, and background-worker exit behavior explicit.
- Do not leave orphaned tasks or infinite loops that cannot stop cleanly.

### 4. Minimize shared mutable state

- Prefer immutable messages, partitioned ownership, or serialized processing to broad locking.
- Use concurrent collections only when their semantics match the real access pattern.
- Keep any unavoidable lock short, obvious, and narrowly scoped.

### 5. Verify throughput and ordering behavior

- Bound concurrency based on the downstream bottleneck.
- Decide whether ordering matters before parallelizing work.
- Add buffering or backpressure intentionally rather than by accident.

## Related guidance

- Pair this with
  [Microsoft Extensions Dependency Injection](../microsoft-extensions-dependency-injection/SKILL.md)
  when hosted services or queue consumers need explicit scopes.

## Gotchas

- **Do not block on async work** with `.Result`, `.Wait()`, or sync-over-async wrappers.
- **Do not use locks as the default tool** when message passing or local ownership would remove the
  race entirely.
- **Do not start unbounded parallel work** just because operations are async.
- **Do not forget queue completion and cancellation** in background processors.

## References

- [C# Concurrency Patterns instructions](../../instructions/csharp-concurrency-patterns.instructions.md)
- [C# Concurrency Patterns agent](../../agents/csharp-concurrency-patterns.agent.md)
- Local advanced patterns reference:
  [advanced-patterns.md](./references/advanced-patterns.md)
- Upstream source adapted from:
  <https://github.com/Aaronontheweb/dotnet-skills/tree/master/skills/csharp-concurrency-patterns>
