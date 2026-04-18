---
description: 'Analyze or create a Roslyn source generator with clear contract, setup, testing, and packaging guidance.'
name: 'source-generation'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the generator goal, trigger contract, current project layout, and the problem to solve.'
---

# Source Generation

## Mission

Use the source-generation slice to design, review, scaffold, or repair a Roslyn source generator
with aligned setup, testing, and packaging guidance.

## Scope and Preconditions

- Use this prompt when the work involves `IIncrementalGenerator`, generator packaging, generator
  tests, local consumer wiring, or generated output problems.
- Read the current generator project, tests, and any local consumer wiring before proposing changes.
- If the task is primarily educational, explain the incremental pipeline clearly and keep the
  explanation tied to the current generator contract.

## Inputs

- Goal: ${input:goal:What should the generator do?}
- Current layout: ${input:layout:What projects or folders are involved?}
- Main issue: ${input:issue:What is broken, missing, or unclear?}

## Workflow

1. Inspect the current generator contract, project shape, and test coverage.
2. Clarify the discovery mechanism, eligible symbols, generated artifacts, and diagnostics.
3. Decide whether the task needs:
   setup help, generator logic changes, testing updates, packaging guidance, or CI validation.
4. Apply the source-generation agent, instruction, and skill guidance together:
   - `../agents/source-generation.agent.md`
   - `../instructions/source-generation.instructions.md`
   - `../skills/source-generation/SKILL.md`
5. If setup or lifecycle work is involved, use the skill references for:
   - project setup
   - testing and CI
6. Produce focused changes or recommendations without expanding into unrelated repository concerns.

## Output Expectations

- Summarize the generator contract in use.
- Summarize the project/setup implications when relevant.
- Show the implementation or refactoring guidance.
- Include testing and validation expectations.
- Call out packaging or CI considerations only when they are part of the task.

## Quality Assurance

- Keep the generator additive-only.
- Keep output deterministic.
- Prefer diagnostics over hidden failures.
- Keep parser/model/emitter responsibilities clear.
- Do not recommend runtime-reflection workarounds for compile-time generation.
