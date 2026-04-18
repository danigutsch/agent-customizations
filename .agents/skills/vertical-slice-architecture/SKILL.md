---
name: vertical-slice-architecture
description: 'Plan, review, and adopt vertical slice architecture for domain-first structure, slice boundaries, testing alignment, and migration.'
---

# Vertical Slice Architecture

Use this skill when the task is about moving toward domain-first structure with use-case slices,
clarifying slice ownership, or reviewing whether an application is really organized around vertical
slices.

## When to Use This Skill

- User asks to introduce or review vertical slice architecture
- User wants to migrate from controller-service-repository layering toward domain-first structure
- User wants clearer ownership for handlers, validators, DTOs, endpoints, or tests
- User wants to reduce accidental coupling between unrelated features
- User wants guidance on where shared code belongs in a slice-oriented design

## Prerequisites

- The current structure can be inspected:
  folders, namespaces, endpoints, handlers, tests, and common cross-cutting services.
- The target business capability, bounded context, or migration scope is known or can be defined.

## Workflow

### 1. Inspect the current structure

- Identify where domains or bounded contexts are currently split by technical layer.
- Find coupling points:
  shared services, cross-feature dependencies, and unclear ownership.
- Note how tests are currently organized and whether they follow business behavior or technical layers.

### 2. Define candidate slice boundaries

- Prefer business or use-case names over technical nouns.
- Place each slice inside the domain or bounded context that owns the behavior.
- Avoid defaulting to a repo-wide `Features/` folder unless `Features` is genuinely the domain name.
- Let each slice own the types needed to complete one use case end to end.
- Keep endpoints or controllers thin and explicit about which slice they call.

### 3. Decide what stays local and what can be shared

- Keep request or command types, validators, handlers, endpoint glue, and tests close to the slice.
- Extract shared code only when it represents a stable cross-cutting concept.
- Accept small duplication when it preserves slice independence and clarity.

### 4. Migrate incrementally

- Move one use case or one narrow vertical at a time.
- Preserve behavior while clarifying ownership.
- Keep transitional boundaries explicit so old and new structures are both understandable.

### 5. Validate the shape

- Confirm each use case has a clear home.
- Confirm tests align with the owning slice.
- Confirm shared code is genuinely cross-cutting rather than a generic dumping ground.

## Related guidance

- If the application also depends on generated APIs or compile-time code generation, pair this with
  [Source generation](../source-generation/SKILL.md).

## Gotchas

- **A `Features` folder is not enough** — and in many codebases it is the wrong top-level shape.
  Prefer domain-first ownership, then place slices within each domain.
- **Do not extract shared abstractions too early** — small duplication is often cheaper than
  coupling slices through a generic helper.
- **Do not require a library just to claim the pattern** — MediatR, CQRS helpers, or custom buses
  are optional, not the architecture itself.
- **Do not migrate everything at once** — large rewrites usually increase ambiguity and risk.

## Troubleshooting

| Issue | Likely cause | What to do |
| --- | --- | --- |
| Slices still feel coupled | Shared services own too much behavior | Move use-case logic back into the owning slices and shrink shared abstractions |
| Tests are hard to map to features | Tests still follow technical layers | Reorganize tests around use cases, handlers, and endpoints |
| Generic `Features` folder became a dumping ground | Real ownership was by domain, not by a shared feature bucket | Reorganize by domain first, then keep slices inside the owning domain |
| Migration keeps stalling | Scope is too large | Move one narrow use case at a time and preserve behavior during each step |

## References

- [Vertical slice architecture instructions](../../instructions/vertical-slice-architecture.instructions.md)
- [Vertical slice architecture agent](../../agents/vertical-slice-architecture.agent.md)
