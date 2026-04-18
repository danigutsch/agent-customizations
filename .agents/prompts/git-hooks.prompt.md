---
description: 'Design or improve lightweight repository Git hooks that complement the documented local validation path.'
name: 'git-hooks'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the current hook setup, local commands, and the hook behavior you want.'
---

# Git Hooks

## Mission

Use the `git-hooks` slice to create or improve local Git hooks that provide fast feedback without
becoming the repository's only validation path.

## Scope & Preconditions

- Use this prompt when the task is about `pre-commit`, `commit-msg`, or related local hook flows.
- Inspect the current local command surface before deciding what belongs in hooks.
- Keep hooks fast, optional, and easy to explain.

## Inputs

- Current hooks: ${input:hooks:What hooks or hook framework are in use today?}
- Local validation commands: ${input:localChecks:What commands should contributors run locally?}
- Gap to fix: ${input:gap:What hook behavior or setup problem should be solved?}

## Workflow

1. Inspect current hook files, scripts, and documented local validation commands.
2. Decide which checks are cheap enough for hook execution.
3. Apply the `git-hooks` guidance together:
   - `../agents/git-hooks.agent.md`
   - `../instructions/git-hooks.instructions.md`
   - `../skills/git-hooks/SKILL.md`
4. Pair with adjacent slices when relevant:
   - `../skills/python-quality/SKILL.md`
   - `../skills/ruff-python/SKILL.md`
   - `../skills/pyright-python/SKILL.md`
   - `../skills/ci-workflows/SKILL.md`
5. Keep hooks as thin wrappers over repository-local commands.

## Output Expectations

- Summarize the current hook state and gap.
- Propose or implement the hook changes.
- Explain how the hooks align with local commands and CI.

## Quality Assurance

- Do not make hooks slow enough that contributors disable them by default.
- Do not hide required validation exclusively in hooks.
- Keep installation and bypass behavior explicit.
