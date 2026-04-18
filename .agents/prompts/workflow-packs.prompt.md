---
description: 'Design or refine reusable workflow packs and agentic workflow assets.'
name: 'workflow-packs'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the workflow goal, the major phases, and what reusable workflow asset is needed.'
---

# Workflow Packs

## Mission

Use the `workflow-packs` slice to create or refine reusable multi-step workflow assets.

## Scope & Preconditions

- Use this prompt when the task is about reusable workflow packs, handoff-oriented flows, or workflow examples.
- Inspect the current workflow docs and repository structure before proposing changes.
- Keep reusable workflow structure separate from repository-specific examples.

## Inputs

- Workflow goal: ${input:goal:What repeatable workflow should this pack support?}
- Main phases: ${input:phases:What are the key phases or checkpoints?}
- Adaptation target: ${input:target:How should another repository adapt this workflow?}

## Workflow

1. Inspect current workflow-related assets and repository guidance.
2. Clarify the workflow goal, phases, handoffs, and validation points.
3. Apply the `workflow-packs` guidance together:
   - `../agents/workflow-packs.agent.md`
   - `../instructions/workflow-packs.instructions.md`
   - `../skills/workflow-packs/SKILL.md`
4. Pair with adjacent slices when relevant:
   - `../skills/repository-setup/SKILL.md`
   - `../skills/ci-workflows/SKILL.md`
   - `../skills/mcp-servers/SKILL.md`
5. Add or refine reusable examples that show local adaptation.

## Output Expectations

- Summarize the workflow goal and phases.
- Show the reusable workflow asset or example.
- Explain adaptation and validation notes.

## Quality Assurance

- Do not confuse reusable workflow structure with one repository's product behavior.
- Keep handoffs and validation explicit.
- Keep examples lightweight and clearly illustrative.
