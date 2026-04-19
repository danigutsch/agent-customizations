---
name: dotnet-aspire-apphost
description: Guidance for focused .NET Aspire AppHost orchestration. Use when designing AppHost resource models, wiring services with WithReference or WaitFor, reviewing AppHost project boundaries, or keeping business logic and service defaults out of the AppHost layer.
---

# Dotnet Aspire AppHost

Use this skill when the task is about the narrow orchestration role of the .NET Aspire AppHost.

## When to Use This Skill

- The user wants to review or design the AppHost resource model
- The user needs help wiring projects, databases, caches, or other resources through the AppHost
- The user needs to decide whether something belongs in the AppHost or in a service project
- The user is reviewing `WithReference`, `WaitFor`, or logical resource naming
- The user wants AppHost guidance that is narrower than broad Aspire setup content

## Prerequisites

- The AppHost project or intended AppHost layout can be inspected.
- The services or resources under orchestration are known.
- The problem is about AppHost composition rather than general Aspire installation.

## Workflow

### 1. Identify the orchestration surface

- List the resources the AppHost needs to compose.
- Separate those resources from ordinary service implementation code.

### 2. Review the relationships

- Check `WithReference` usage and logical naming.
- Use `WaitFor` only where startup ordering matters materially.

### 3. Protect the boundary

- Move application logic, shared policies, and service behavior out of the AppHost when they do not
  belong there.
- Keep shared defaults with service projects or shared defaults libraries.

### 4. Validate the model

- Review the AppHost as an architecture map.
- Confirm the orchestration model stays readable and minimal.

## Related guidance

- Pair with [CI Workflows](../ci-workflows/SKILL.md) when AppHost validation or orchestration checks
  need pipeline integration.
- Pair with [Repository Setup](../repository-setup/SKILL.md) when the repository layout around AppHost
  and service projects needs clarification.

## Gotchas

- **Do not turn the AppHost into a business-logic project.**
- **Do not hardcode service URLs when Aspire references should carry the wiring.**
- **Do not overuse `WaitFor` as a blanket startup-order tool.**
- **Do not confuse this capability with the broad setup-generated Aspire skill.**

## References

- [Dotnet Aspire AppHost guidance](../../instructions/dotnet-aspire-apphost.instructions.md)
- [Dotnet Aspire AppHost agent](../../agents/dotnet-aspire-apphost.agent.md)
