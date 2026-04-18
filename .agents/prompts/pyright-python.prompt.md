---
description: 'Configure Pyright or Pylance type checking with a clear scope, excludes, and strictness model.'
name: 'pyright-python'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the current Pyright setup, analysis scope, and the type-checking gap to fix.'
---

# Pyright Python

## Mission

Use the `pyright-python` slice to configure or refine shared Python type checking with Pyright or
Pylance.

## Scope & Preconditions

- Use this prompt when the task is about Pyright config, analysis scope, or shared type-checking
  rules.
- Inspect the current Python layout and imports before changing strictness or excludes.
- Keep shared config portable across contributors and machines.

## Inputs

- Analysis scope: ${input:scope:Which files or directories should Pyright analyze?}
- Current config: ${input:config:What Pyright or pyproject configuration already exists?}
- Gap to fix: ${input:gap:What type-checking problem should be solved?}

## Workflow

1. Inspect current Python files, import layout, and shared type-checking config.
2. Decide whether config belongs in `pyproject.toml` or a dedicated Pyright file.
3. Apply the `pyright-python` guidance together:
   - `../agents/pyright-python.agent.md`
   - `../instructions/pyright-python.instructions.md`
   - `../skills/pyright-python/SKILL.md`
4. Pair with adjacent slices when relevant:
   - `../skills/python-quality/SKILL.md`
   - `../skills/ruff-python/SKILL.md`
   - `../skills/ci-workflows/SKILL.md`
5. Keep include, exclude, and strictness choices aligned with the repository's actual Python surface.

## Output Expectations

- Summarize the current type-checking state and gap.
- Propose or implement the config changes.
- Explain the analysis boundary and strictness decisions.

## Quality Assurance

- Do not bake user-specific environment paths into shared config.
- Do not widen the analysis scope without a reason.
- Keep local and CI type-checking aligned.
