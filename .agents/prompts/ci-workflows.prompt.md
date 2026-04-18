---
description: 'Design or improve a repository CI workflow that creates and runs the real local validation path.'
name: 'ci-workflows'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the repository, current local checks, and the CI workflow gap to fix.'
---

# CI Workflows

## Mission

Use the `ci-workflows` slice to create or improve repository CI workflows that reinforce the real
local validation path.

## Scope & Preconditions

- Use this prompt when the task is about CI workflow design or validation automation.
- Inspect the current local validation commands before editing workflow files.
- Keep CI proportional to the repository's actual risk and maintenance surface.

## Inputs

- Repository purpose: ${input:purpose:What is this repository for?}
- Local validation path: ${input:localChecks:What commands should contributors run locally?}
- CI gap: ${input:gap:What workflow or validation gap should be fixed?}

## Workflow

1. Inspect the current workflow files, scripts, and documented local validation path.
2. Identify which checks truly belong in CI.
3. Apply the `ci-workflows` guidance together:
   - `../agents/ci-workflows.agent.md`
   - `../instructions/ci-workflows.instructions.md`
   - `../skills/ci-workflows/SKILL.md`
4. Pair with focused slices when relevant:
   - `../skills/python-quality/SKILL.md`
   - `../skills/ruff-python/SKILL.md`
   - `../skills/pyright-python/SKILL.md`
   - `../skills/git-hooks/SKILL.md`
5. Keep workflow logic thin when repository-local scripts already express the real checks.

## Output Expectations

- Summarize the current local validation path and the workflow gap.
- Propose or implement the workflow changes.
- Explain the command mapping between local validation and CI.
- Call out any permission, cache, or matrix decisions that matter.

## Quality Assurance

- Do not add CI checks that contributors cannot reproduce locally.
- Do not overcomplicate the workflow for a small repository.
- Keep the workflow readable and easy to maintain.
