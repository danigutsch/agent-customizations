---
description: 'Standards for database access performance covering EF Core tracking discipline, projections, row limits, batching, N+1 avoidance, and deliberate EF Core versus Dapper choices.'
applyTo: '**/*.cs, **/*.csproj'
---

# Database Performance Standards

Use these rules when the task involves .NET data-access performance, query shape, ORM behavior, or
read/write data-store boundaries.

## Read and write boundaries

- Prefer specialized read models or projections instead of reusing mutation-focused entities for all
  read scenarios.
- Keep write paths focused on commands, validation, and persistence intent.
- Use purpose-built read/write store interfaces when they make query optimization clearer and easier
  to maintain.
- Avoid generic repositories that hide query shape, limits, and loading behavior.

## Query shape

- Project only the columns needed for the consumer; do not load full entities by default.
- Apply explicit row limits or pagination to read APIs.
- Prefer `AsNoTracking()` for ordinary read-only EF Core queries.
- Use `AsTracking()` only where tracked state is intentionally required for mutation.

## Related data loading

- Avoid N+1 access patterns caused by per-row follow-up queries.
- Use includes, projection, or batch queries when related data must be fetched together.
- Avoid cartesian explosions from multiple includes by using `AsSplitQuery()` or tighter projection.
- Keep joins in SQL rather than reconstructing them in application memory from separate large
  datasets.

## ORM selection

- Use EF Core where aggregate updates, tracked entities, or normal CRUD workflows benefit from it.
- Use Dapper or explicit SQL when a complex read query is clearer and more efficient as a direct
  projection.
- A mixed approach is acceptable when read and write paths have different performance needs.

## Materialization and result shape

- Materialize to the smallest useful DTO or summary model for the caller.
- Return read-only collection contracts from read APIs when the result is already materialized.
- Keep ordering, filtering, and pagination explicit in the query rather than post-processing large
  in-memory datasets.

## Anti-patterns

- Do not expose unbounded `GetAll()` style reads on large datasets.
- Do not use tracked EF Core reads by default.
- Do not perform application-side joins over large independently fetched datasets.
- Do not load broad entity graphs when a focused projection or summary would do.

## Verification

- Confirm read APIs are bounded by limit, pagination, or a naturally small domain constraint.
- Confirm read-only EF Core queries use `AsNoTracking()` unless tracking is intentional.
- Confirm related-data loading avoids N+1 and cartesian-explosion behavior.
- Confirm the chosen EF Core, Dapper, or mixed approach matches the actual workload.
