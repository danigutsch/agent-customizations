---
description: 'Guidance for multi-agent coordination, lane ownership, handoffs, escalation, and cost-aware model routing across Copilot and external model backends.'
applyTo: 'docs/**/*.md, .agents/agents/agent-coordination.agent.md, .agents/prompts/agent-coordination.prompt.md, .agents/skills/agent-coordination/**, .agents/workflows/agent-coordination/**/*'
---

# Agent Coordination Guidance

Use these rules when the task is about coordinating multiple agents or model lanes rather than
solving one task with one worker.

## Core model

- Treat coordination as a control-plane problem: lane ownership, routing, handoffs, escalation, and
  checkpoints.
- Route work by task class first, then choose the cheapest reliable model for that lane.
- Keep tool-heavy repository edits and final merge judgment in the strongest repo-aware execution
  environment.
- Keep one active authority per repository for Copilot runtime assets whenever overlapping user and
  repo surfaces would create ambiguity, defaulting to user-level assets unless repo-level overrides
  are intentionally chosen.

## Lane and ownership rules

- Keep the lane set small and explicit, such as coordinator, scout, implementer, validator,
  reviewer, and documentation.
- Give each lane a clear mission, expected output, and completion checkpoint.
- Do not run parallel lanes that mutate the same files without explicit ownership or merge rules.
- Keep cheap scouting and extraction work separate from final review and release judgment.

## Routing and escalation rules

- Default to low-cost models for inventory, extraction, search summaries, and alternative drafts.
- Use balanced models for implementation and synthesis that must be useful on the first pass.
- Reserve premium models for coordination, conflict resolution, architecture review, security
  review, and final release decisions.
- Make escalation triggers explicit, especially for security, cross-repository coordination,
  conflicting recommendations, or high-cost changes.

## Handoff and checkpoint rules

- Keep handoffs explicit about inputs, outputs, and when the next lane may start.
- Make validation checkpoints visible near the lane they protect.
- Prefer small reviewable outputs over large opaque agent batches.
- Keep fallback paths clear when a cheap lane produces low-confidence results.

## Copilot and external worker rules

- Use Copilot-native agents for repo-local editing, command execution, and final review when those
  tasks depend on tool access and current workspace state.
- Use external model workers for low-cost scouting, inventory, drift analysis, and draft
  transformations when those tasks do not require direct local edits.
- Document repo-local versus user-local Copilot authority decisions whenever duplicate runtime
  definitions exist, with user-level treated as the default and repo-level as an explicit
  alternative.

## Workflow-pack rules

- When coordination guidance is meant to be reused, include workflow assets that show phases,
  handoffs, checkpoints, and adaptation notes.
- Keep workflow examples generic rather than tied to one repository's business behavior.
- Keep model-routing examples illustrative and updateable rather than pretending to be permanent
  price guarantees.

## Verification

- Confirm the lane model is understandable without hidden context.
- Confirm handoffs and escalation triggers are explicit.
- Confirm the chosen models match the intended cost, speed, and quality tier for each lane.
- Confirm no repository is left with two equally authoritative Copilot runtime surfaces by accident.
