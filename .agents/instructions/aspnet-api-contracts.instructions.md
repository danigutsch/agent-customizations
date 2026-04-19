---
description: 'Guidance for ASP.NET API contract design: explicit DTOs, typed results, ProblemDetails, OpenAPI, versioning, and contract-focused validation.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/aspnet-api-contracts.agent.md, .agents/skills/aspnet-api-contracts/**, .agents/instructions/aspnet-api-contracts.instructions.md'
---

# Aspnet API Contracts Guidance

Use these rules when the task is about ASP.NET HTTP API contract design rather than general
application setup.

## Core model

- Treat routes, request DTOs, response DTOs, and error payloads as an explicit public contract.
- Keep Minimal API and controller guidance focused on the contract surface, not on broad application
  scaffolding.
- Prefer contract types and response unions that make endpoint behavior obvious to both OpenAPI and
  tests.
- Keep OpenAPI, `ProblemDetails`, and versioning choices aligned with the actual API audience.

## Contract rules

- Define public request and response DTOs explicitly.
- Do not expose domain or persistence models as the default HTTP contract.
- Keep route templates resource-oriented and endpoint names stable.
- Keep list, detail, mutation, and error responses intentional rather than incidental.

## Result-shape rules

- Prefer `TypedResults` over untyped `Results` in Minimal APIs when metadata and testability matter.
- Use `Results<T1, TN>` for multi-shape Minimal API handlers so the contract stays explicit.
- In controllers, prefer `ActionResult<T>` or explicit result types when they improve contract
  clarity.
- Do not leave response metadata implicit when the API is meant to be documented or consumed
  externally.

## ProblemDetails and validation rules

- Add `AddProblemDetails()` when the API needs consistent RFC 7807-style error payloads.
- Prefer centralized mapping helpers for validation, not-found, and conflict outcomes.
- Keep validation and domain-failure mapping explicit and repeatable across endpoints.

## OpenAPI and versioning rules

- Add OpenAPI support deliberately and keep endpoint metadata aligned with the public surface.
- Use endpoint grouping and document grouping intentionally when multiple API audiences or versions
  exist.
- Prefer build-time OpenAPI generation when the document itself is a reviewable contract artifact.
- Prefer runtime OpenAPI endpoints when discoverability or local inspection matters more.

## Testing and snapshot rules

- Use focused assertions for status codes, key DTO fields, and `ProblemDetails` fields.
- Use snapshot testing for deterministic contract artifacts such as generated OpenAPI documents when
  whole-surface drift matters.
- Do not rely on snapshots alone when a smaller invariant assertion would be clearer.

## Verification

- Confirm routes, DTOs, and result shapes match the intended public contract.
- Confirm `ProblemDetails` behavior is explicit and centralized.
- Confirm OpenAPI metadata reflects the actual endpoint surface.
- Confirm contract tests and any snapshots validate stable artifacts rather than incidental noise.
