---
description: 'Create or improve repository foundations with clear structure, documentation, validation, and CI-ready setup.'
name: 'repository-setup'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the repository purpose, current structure, and the setup gaps you want to fix.'
---

# Repository Setup

## Mission

Use the repository-setup slice to initialize or improve repository structure, documentation,
validation, and contributor-facing operating guidance.

## Scope and Preconditions

- Use this prompt when the task is about repository foundations rather than one product feature.
- Inspect the current top-level structure, README, guidance files, scripts, and validation surface
  before recommending changes.
- Keep the setup proportional to the repository purpose.

## Inputs

- Repository purpose: ${input:purpose:What is this repository for?}
- Current structure: ${input:structure:What top-level folders and files already exist?}
- Main gap: ${input:gap:What setup, docs, validation, or CI issue should be fixed?}

## Workflow

1. Inspect the current repository purpose, layout, and contributor surface.
2. Identify the missing or weak foundations:
   structure, README, guidance, validation scripts, templates, examples, or CI expectations.
3. Apply the repository-setup agent, instruction, and skill guidance together:
   - `../agents/repository-setup.agent.md`
   - `../instructions/repository-setup.instructions.md`
   - `../skills/repository-setup/SKILL.md`
4. Use the skill references when the task needs help with:
   - repository foundations
   - validation and CI design
5. Prefer repository-local validation commands over hidden or duplicated automation logic.
6. Keep the outcome aligned with the repository purpose instead of adding generic boilerplate.

## Output Expectations

- Summarize the repository purpose and main setup gap.
- Propose or implement the structure and documentation changes.
- Call out validation and CI implications.
- Keep the result maintainable and easy for contributors to follow.

## Quality Assurance

- Do not add folders or files without a clear role.
- Do not leave maintenance expectations implicit.
- Do not design CI before defining the local validation path.
- Keep reusable and repo-specific guidance clearly separated.
