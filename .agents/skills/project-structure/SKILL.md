---
name: project-structure
description: Guidance for repository and solution structure. Use when reviewing folder layout, project boundaries, bounded-context ownership, shared-project sprawl, generator or tooling project placement, or test-project alignment in a codebase.
---

# Project Structure

Use this skill when the task is about repository or solution layout rather than one isolated code
change.

## When to Use This Skill

- The user needs to review or redesign repository layout
- The user needs clearer project ownership boundaries
- The user needs to decide whether to split, merge, or move projects
- The user needs test-project layout to align better with production structure
- The user needs guidance for shared tooling or generator project placement

## Prerequisites

- The current folder and project structure can be inspected.
- The main ownership or dependency problem is known well enough to evaluate.

## Workflow

### 1. Identify the ownership map

- Determine the main bounded contexts, features, runtime roles, or tooling surfaces.
- Check whether the current layout makes those easy to see.

### 2. Review project boundaries

- Keep contracts, infrastructure, domain, application, and tooling boundaries explicit when they
  truly differ.
- Avoid convenience-driven shared projects that accumulate unrelated code.

### 3. Align tests and tooling

- Keep tests close in naming and intent to the production projects they verify.
- Split test or tooling projects only when the execution model really differs.

## Related guidance

- Pair with [Repository Setup](../repository-setup/SKILL.md) when the structure question is
  repository-wide.
- Pair with [Vertical Slice Architecture](../vertical-slice-architecture/SKILL.md) when feature
  boundaries should drive the layout.
- Pair with [Package Management](../package-management/SKILL.md) when structure and dependency
  ownership need to move together.

## Gotchas

- **Do not optimize for project-count reduction alone.**
- **Do not create shared projects that hide ownership.**
- **Do not let tooling and tests drift away from the code they support.**

## References

- [Project structure guidance](../../instructions/project-structure.instructions.md)
- [Project structure agent](../../agents/project-structure.agent.md)
