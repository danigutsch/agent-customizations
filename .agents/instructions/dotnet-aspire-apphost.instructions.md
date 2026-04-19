---
description: 'Guidance for narrow .NET Aspire AppHost orchestration: resource modeling, references, startup ordering, and keeping service logic out of the AppHost.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/dotnet-aspire-apphost.agent.md, .agents/skills/dotnet-aspire-apphost/**, .agents/instructions/dotnet-aspire-apphost.instructions.md'
---

# Dotnet Aspire AppHost Guidance

Use these rules when the task is specifically about designing or reviewing the .NET Aspire AppHost
layer rather than broad Aspire setup or tool-generated baseline assets.

## Core model

- Treat the AppHost as the code-first orchestration boundary for the distributed application.
- Keep the AppHost focused on resources, relationships, and startup wiring.
- Keep business logic, feature rules, and service implementation details out of the AppHost.

## Resource modeling rules

- Model databases, caches, services, and supporting infrastructure as explicit resources when the
  AppHost is responsible for orchestrating them.
- Use logical resource names consistently.
- Distinguish between Aspire resource references and normal code-level project references.

## Wiring rules

- Prefer `WithReference` for service discovery and connection wiring when Aspire already supports the
  relationship.
- Use `WaitFor` only for real startup dependencies; do not blanket-sequence every resource.
- Avoid manual endpoint duplication when the AppHost can project the relationship more directly.

## Boundary rules

- Keep shared cross-cutting behavior in service projects or shared defaults rather than in the
  AppHost.
- Treat tool-generated broad Aspire skill content as baseline project context, not as this
  capability's source material.
- Keep this capability narrower than general Aspire platform setup guidance.

## Verification

- Confirm the guidance keeps the AppHost orchestration-focused.
- Confirm references and startup ordering reflect real dependencies.
- Confirm the AppHost guidance stays distinct from broad Aspire setup-generated assets.
- Confirm service-level behavior is pushed back to service projects or shared defaults where
  appropriate.
