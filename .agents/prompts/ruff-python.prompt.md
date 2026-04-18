---
description: 'Configure Ruff for repository Python linting and formatting with clear commands and focused rules.'
name: 'ruff-python'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the current Ruff setup, Python files, and lint or format behavior you want.'
---

# Ruff Python

## Mission

Use the `ruff-python` slice to configure or refine Ruff as the repository's Python lint and formatting
baseline.

## Scope & Preconditions

- Use this prompt when the task is about Ruff configuration, commands, rules, or excludes.
- Inspect the current Python scope and existing config before changing Ruff behavior.
- Keep rule choices intentional and maintainable.

## Inputs

- Python files: ${input:pythonFiles:Which Python files or directories should Ruff cover?}
- Current Ruff config: ${input:config:What Ruff config or commands already exist?}
- Gap to fix: ${input:gap:What lint, format, or CI behavior should change?}

## Workflow

1. Inspect current Python files, existing Ruff settings, and related docs or CI.
2. Decide the intended command surface:
   `ruff check`, `ruff format`, or both.
3. Apply the `ruff-python` guidance together:
   - `../agents/ruff-python.agent.md`
   - `../instructions/ruff-python.instructions.md`
   - `../skills/ruff-python/SKILL.md`
4. Pair with adjacent slices when relevant:
   - `../skills/editorconfig/SKILL.md`
   - `../skills/python-quality/SKILL.md`
   - `../skills/pyright-python/SKILL.md`
   - `../skills/ci-workflows/SKILL.md`
   - `../skills/git-hooks/SKILL.md`
5. Keep excludes and automation aligned with the repository's real generated or compatibility outputs.

## Output Expectations

- Summarize the current Ruff setup and gap.
- Propose or implement the config and command changes.
- Explain any important rule, exclude, or automation decisions.

## Quality Assurance

- Do not add large rule sets without a maintenance reason.
- Do not use per-file ignores as the default escape hatch.
- Keep local and CI usage consistent.
