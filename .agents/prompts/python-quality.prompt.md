---
description: 'Establish or improve a lightweight Python quality baseline for a repository.'
name: 'python-quality'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the Python surface in the repo and the quality baseline you want to improve.'
---

# Python Quality

## Mission

Use the `python-quality` slice to define or improve the shared Python quality baseline for a
repository.

## Scope & Preconditions

- Use this prompt when the task is about Python tooling, shared config, or validation expectations.
- Inspect how Python is used in the repository before adding tools or config.
- Keep the baseline proportional to the repository's actual Python surface.

## Inputs

- Python surface: ${input:pythonSurface:What Python files or directories exist?}
- Current baseline: ${input:baseline:What Python tooling or config already exists?}
- Gap to fix: ${input:gap:What quality or maintenance problem should be solved?}

## Workflow

1. Inspect current Python files, config files, ignore rules, and docs.
2. Identify the smallest useful shared baseline for the repository.
3. Apply the `python-quality` guidance together:
   - `../agents/python-quality.agent.md`
   - `../instructions/python-quality.instructions.md`
   - `../skills/python-quality/SKILL.md`
4. Pair with focused slices when relevant:
   - `../skills/editorconfig/SKILL.md`
   - `../skills/ruff-python/SKILL.md`
   - `../skills/pyright-python/SKILL.md`
   - `../skills/ci-workflows/SKILL.md`
   - `../skills/git-hooks/SKILL.md`
5. Keep local commands, CI, and docs aligned with the same Python scope.

## Output Expectations

- Summarize the current Python quality surface and the gap.
- Propose or implement the baseline changes.
- Call out the local command surface contributors should use.
- Note any CI or hook implications.

## Quality Assurance

- Do not add overlapping tools without a clear reason.
- Do not optimize for package publishing if the repo is mostly scripts.
- Keep the baseline understandable to contributors.
