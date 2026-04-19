---
name: database-performance
description: 'Improve .NET database access performance using projection-first reads, row limits, batching, EF Core tracking discipline, and deliberate EF Core versus Dapper choices. Use when fixing slow queries, N+1 problems, oversized entity loads, or read/write store shape.'
---

# Database Performance

Use this skill when the task is about database access performance, query shape, or read/write data
store boundaries in .NET applications.

## When to Use This Skill

- User is optimizing slow database queries or ORM-heavy code
- User needs guidance on EF Core versus Dapper for a read path
- User is fighting N+1 queries, cartesian explosions, or oversized entity graphs
- User needs row limits, pagination, or projection-first read APIs
- User is separating read and write store responsibilities

## Prerequisites

- The relevant data-access code, read models, store interfaces, and query patterns can be inspected.
- The main bottleneck is understood well enough to tell whether the issue is tracking, query count,
  projection size, join shape, or abstraction choice.

## Workflow

### 1. Inspect the current data-access shape

- Identify the read and write paths involved.
- Check whether queries are tracked, unbounded, or loading more data than the caller needs.
- Find N+1 loops, application-side joins, and repeated materialization.

### 2. Choose the data-access approach deliberately

- Keep EF Core where tracked writes and normal aggregate workflows fit well.
- Use Dapper or explicit SQL where a read-heavy projection is clearer and faster.
- Keep read and write models separate when that makes the data-access boundary cleaner.

### 3. Fix query shape first

- Add projection, limits, pagination, and `AsNoTracking()` where appropriate.
- Remove N+1 patterns with includes, batching, or explicit SQL joins.
- See [advanced-patterns.md](./references/advanced-patterns.md) for projection-first reads, split
  queries, batched reads, and EF Core versus Dapper examples.

### 4. Keep result shape intentional

- Return summary or detail DTOs sized for the actual use case.
- Avoid exposing broad entity graphs across read boundaries.
- Keep ordering and filtering in the database rather than after pulling large result sets.

### 5. Avoid common database-performance mistakes

- Do not leave unbounded reads in list or search paths.
- Do not default to tracked EF Core reads.
- Do not rely on generic repositories that hide query performance.
- Do not join large datasets in application code when the database can do it directly.

## Related guidance

- Pair this with [C# Type Design Performance](../csharp-type-design-performance/SKILL.md) when DTO
  shape, collection contracts, or materialization behavior affect the hot path.

## Gotchas

- **Do not use `Include` everywhere by reflex**; projection is often cheaper and clearer.
- **Do not return full entities for list views** that only need summaries.
- **Do not hide query limits**; make them explicit at the API boundary.
- **Do not force one ORM everywhere** when read and write paths have different needs.

## References

- [Database Performance instructions](../../instructions/database-performance.instructions.md)
- [Database Performance agent](../../agents/database-performance.agent.md)
- Local advanced patterns reference:
  [advanced-patterns.md](./references/advanced-patterns.md)
- Upstream source adapted from:
  <https://github.com/Aaronontheweb/dotnet-skills/tree/master/skills/database-performance>
