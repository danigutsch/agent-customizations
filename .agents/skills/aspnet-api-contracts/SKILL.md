---
name: aspnet-api-contracts
description: Guidance for ASP.NET HTTP API contract design. Use when reviewing Minimal API or controller route shape, request and response DTOs, typed results, ProblemDetails payloads, OpenAPI document shape, versioning, or snapshot-friendly contract validation for ASP.NET APIs.
---

# Aspnet API Contracts

Use this skill when the task is about ASP.NET HTTP contract design rather than broad application
setup.

## When to Use This Skill

- The user needs to design or review an ASP.NET Minimal API or controller contract
- The user needs clearer request and response DTO boundaries
- The user needs typed result guidance for Minimal APIs
- The user needs consistent `ProblemDetails` or validation payload shape
- The user needs OpenAPI or versioning guidance for an ASP.NET API
- The user needs focused contract tests or snapshot coverage for ASP.NET API drift

## Prerequisites

- The API routes, DTOs, or intended contract surface can be inspected.
- The task is about the HTTP contract, not only internal service implementation.
- The API documentation or error-shape expectations are known well enough to reason about stability.

## Workflow

### 1. Identify the public HTTP contract

- List the routes, methods, DTOs, status codes, and error shapes that define the surface.
- Decide whether Minimal APIs or controllers fit the surrounding application shape best.

### 2. Make result types explicit

- Prefer `TypedResults` and `Results<T1, TN>` when Minimal API response shape should be self-describing.
- Keep controller action return types aligned with the actual public contract.

### 3. Centralize errors and documentation

- Use `AddProblemDetails()` and explicit mapping helpers when the API needs stable RFC 7807-style
  errors.
- Add OpenAPI support and keep endpoint names, summaries, and descriptions aligned with the route
  surface.

### 4. Validate the contract

- Use focused assertions for important status-code and payload invariants.
- Consider snapshots for deterministic OpenAPI documents or other stable contract artifacts.

## Related guidance

- Pair with [Xunit V3 Mtp Test Stack](../xunit-v3-mtp-test-stack/SKILL.md) when API contract tests,
  OpenAPI snapshots, or `ProblemDetails` checks need explicit test-stack guidance.
- Pair with [Grpc Protobuf Contracts](../grpc-protobuf-contracts/SKILL.md) when HTTP and gRPC
  contracts are being shaped together.
- Pair with [CI Workflows](../ci-workflows/SKILL.md) when contract checks need CI automation.

## Gotchas

- **Do not let internal models become the HTTP contract by accident.**
- **Do not leave multiple response shapes implicit when typed results can document them.**
- **Do not hand-shape error payloads differently on every endpoint.**
- **Do not use snapshots as the only proof of API correctness.**

## References

- [Aspnet api contracts guidance](../../instructions/aspnet-api-contracts.instructions.md)
- [Aspnet api contracts agent](../../agents/aspnet-api-contracts.agent.md)
