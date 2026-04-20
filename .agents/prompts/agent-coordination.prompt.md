---
description: 'Design or refine a reusable multi-agent router or orchestrator model with explicit lanes, dispatch, subagent handoffs, and model-routing policy.'
name: 'agent-coordination'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the router goal, subagents or parallel lanes, Copilot versus external workers, model budget, and dispatch, escalation, or handoff rules you want to coordinate.'
---

# Agent Coordination

## Mission

Use the `agent-coordination` capability to design or refine a reusable multi-agent operating model.

## Scope & Preconditions

- Use this prompt when the task is about coordinator-plus-worker routing, handoffs, or escalation.
- Inspect the current agent, skill, export, and workflow guidance before proposing changes.
- Keep lane ownership, authority boundaries, and checkpoints explicit.

## Inputs

- Team goal: ${input:goal:What should this coordinated agent team accomplish?}
- Lanes: ${input:lanes:What lanes or specialist roles should exist?}
- Runtime split: ${input:runtime:How should work split between Copilot and external model backends?}
- Budget policy: ${input:budget:What cost or speed constraints should routing respect?}

## Workflow

1. Inspect the current coordination, workflow, and export guidance in the repository.
2. Clarify the lane model, outputs, and handoff checkpoints.
3. Apply the `agent-coordination` guidance together:
   - `../agents/agent-coordination.agent.md`
   - `../instructions/agent-coordination.instructions.md`
   - `../skills/agent-coordination/SKILL.md`
4. Pair with adjacent slices when relevant:
   - `../skills/workflow-packs/SKILL.md`
   - `../skills/copilot-compatibility-exports/SKILL.md`
   - `../skills/repository-setup/SKILL.md`
   - `../skills/mcp-servers/SKILL.md`
5. Add or refine reusable workflow assets and routing notes.

## Output Expectations

- Summarize the lane model and ownership boundaries.
- Show the first-choice and escalation model for each lane.
- Explain the Copilot versus external-worker split.
- Make handoffs, checkpoints, and open authority decisions explicit.

## Quality Assurance

- Do not let cost optimization hide review and escalation duties.
- Do not leave repo-local versus user-local authority ambiguous.
- Keep routing examples updateable and clearly illustrative.
