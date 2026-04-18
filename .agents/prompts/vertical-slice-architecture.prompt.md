---
description: 'Review or adopt domain-first vertical slice architecture with clear slice ownership and migration guidance.'
name: 'vertical-slice-architecture'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the current structure, target domain, and the slice ownership or migration problem.'
---

# Vertical Slice Architecture

## Mission

Use the vertical-slice-architecture slice to review, introduce, or migrate toward domain-first
vertical slices with clear ownership for behavior, tests, and boundaries.

## Scope and Preconditions

- Use this prompt when the work is about slice boundaries, domain-first organization, migration away
  from layered structure, or reducing coupling between use cases.
- Inspect the current folder, namespace, endpoint, handler, and test layout before recommending a
  structure change.
- Keep the scope incremental unless the user explicitly wants a larger redesign.

## Inputs

- Current structure: ${input:structure:How is the code organized now?}
- Target domain or scope: ${input:domain:Which domain, bounded context, or use cases matter here?}
- Main problem: ${input:issue:What ownership, coupling, or migration issue should be fixed?}

## Workflow

1. Inspect the current structure and identify domain boundaries and coupling points.
2. Define the owning domain and candidate slice boundaries in business or use-case terms.
3. Apply the vertical-slice agent, instruction, and skill guidance together:
   - `../agents/vertical-slice-architecture.agent.md`
   - `../instructions/vertical-slice-architecture.instructions.md`
   - `../skills/vertical-slice-architecture/SKILL.md`
4. Prefer domain-first organization instead of a generic top-level `Features/` bucket.
5. Decide what should remain local to a slice and what, if anything, is truly cross-cutting.
6. Recommend or implement migration steps that preserve behavior and testability.

## Output Expectations

- Summarize the current structural problem.
- Propose the target slice boundaries and ownership.
- Explain shared-code decisions and trade-offs.
- Include testing alignment and migration guidance.
- Keep the advice specific to the current domain and use cases.

## Quality Assurance

- Do not recreate layer-first structure under a new folder name.
- Keep endpoints and controllers thin.
- Accept small duplication when it improves slice clarity.
- Avoid premature shared abstractions.
- Prefer incremental migration over broad rewrites.
