---
name: workflow-packs
description: 'Design reusable workflow packs. Use for multi-step handoff flows, validation checkpoints, rollout-style workflows, and repository adaptation examples.'
---

# Workflow Packs

Use this skill when the task is about reusable workflow packs rather than a one-off implementation plan for a single repository.

## When to Use This Skill

- User wants a reusable multi-step workflow pack
- User wants handoff-oriented workflow assets or examples
- User wants validation checkpoints embedded in a reusable flow
- User wants workflow docs that can be adapted by other repositories

## Prerequisites

- The workflow goal and main phases are known or can be clarified.
- The repository's current workflow guidance can be inspected.

## Workflow

### 1. Define the reusable flow

- List the workflow goal, phases, inputs, outputs, and checkpoints.
- Keep the structure reusable across repositories when possible.

### 2. Separate reuse from adaptation

- Keep the workflow pack generic.
- Add small examples that show how another repository would adapt it locally.

### 3. Make handoffs and validation explicit

- Document where humans, agents, or automation need to hand off.
- Keep validation checkpoints visible and understandable.

## Related guidance

- Pair this with [Repository setup](../repository-setup/SKILL.md) when the workflow pack supports repo operations.
- Pair this with [CI workflows](../ci-workflows/SKILL.md) when workflow steps should map to automation.
- Pair this with [MCP servers](../mcp-servers/SKILL.md) when workflow packs depend on MCP assets.

## Gotchas

- **Do not bake product-specific logic into a reusable workflow pack**.
- **Do not hide required handoffs or checkpoints**.
- **Do not make adaptation details implicit**.

## References

- [Workflow packs instructions](../../instructions/workflow-packs.instructions.md)
- [Workflow packs agent](../../agents/workflow-packs.agent.md)
