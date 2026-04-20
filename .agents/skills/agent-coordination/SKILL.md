---
name: agent-coordination
description: Coordinate multi-agent work with explicit lanes, task routing, dispatch, subagent handoffs, escalation, and cost-aware model selection. Use when a user asks for agent coordination, a router, orchestrator, dispatcher, planner-plus-workers setup, parallel agents, specialist subagents, model-routing policy, or Copilot versus external model backend boundaries.
---

# Agent Coordination

Use this skill when the task is about a reusable multi-agent operating model rather than one
specialist agent working alone.

## When to Use This Skill

- The user wants a coordinator plus specialist-worker setup
- The user asks for a router, orchestrator, dispatcher, or control-plane for agents
- The user wants parallel agents, subagents, delegated workers, or planner-plus-workers execution
- The task needs lane ownership, handoffs, or escalation rules
- The user wants cheap models for scouting and stronger models for final review
- The workflow splits work between Copilot-native agents and external model backends
- The repository needs a documented parallel team operating model

## Common trigger phrases

- `agent coordination`
- `subagents`
- `parallel agents`
- `agent router`
- `task dispatch`
- `planner and workers`
- `orchestrator`
- `escalation policy`
- `model routing`
- `Copilot vs OpenRouter`

## Prerequisites

- The repository's current agent, skill, workflow, or export model can be inspected
- The main work lanes are known or can be derived
- The task is about coordination policy, not only one model recommendation in isolation

## Workflow

### 1. Define the lane model

- Choose a small explicit set of lanes such as coordinator, scout, implementer, validator,
  reviewer, and documentation.
- Give each lane a clear purpose and output.

### 2. Route by task class

- Use cheap models first for scouting, extraction, and draft transformation.
- Use stronger balanced models for implementation and meaningful synthesis.
- Reserve premium models for merge decisions, architecture review, and hard escalations.

### 3. Make handoffs visible

- State what a lane hands off and when the next lane may start.
- Keep checkpoints near the lane they protect.

### 4. Keep runtime authority explicit

- Prefer repo-local Copilot assets for project-specific work.
- Keep user-local assets only for truly global non-overlapping guidance.

## Related guidance

- Pair with [Workflow Packs](../workflow-packs/SKILL.md) when the coordination model should ship as a
  reusable phased workflow.
- Pair with [Copilot Compatibility Exports](../copilot-compatibility-exports/SKILL.md) when runtime
  authority depends on exported versus canonical assets.
- Pair with [Repository Setup](../repository-setup/SKILL.md) when the operating model needs to become
  part of repo guidance.
- Pair with [MCP Servers](../mcp-servers/SKILL.md) when external workers depend on MCP assets or
  wrappers.

## Gotchas

- **Do not let two lanes mutate the same files without ownership rules.**
- **Do not use a free scouting model as the final security or release reviewer.**
- **Do not keep repo-local and user-local Copilot assets equally authoritative for one project.**
- **Do not hide escalation rules inside vague prose.**

## References

- [Agent coordination guidance](../../instructions/agent-coordination.instructions.md)
- [Agent coordination agent](../../agents/agent-coordination.agent.md)
- [Agent coordination workflow assets](../../workflows/agent-coordination/README.md)
