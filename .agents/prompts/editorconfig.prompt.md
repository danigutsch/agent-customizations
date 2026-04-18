---
description: 'Create or improve a repo .editorconfig with clear defaults and targeted overrides.'
name: 'editorconfig'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'Describe the repo file types, current .editorconfig, and the formatting issue to fix.'
---

# EditorConfig

## Mission

Use the `editorconfig` slice to create or refine a repository `.editorconfig` that gives contributors
clear, portable editor defaults.

## Scope & Preconditions

- Use this prompt when the task is about shared whitespace, indentation, line-ending, or
  file-type-specific editor defaults.
- Inspect the repo's actual file types and current `.editorconfig` before adding overrides.
- Keep `.editorconfig` aligned with the repo's formatter and linter configuration.

## Inputs

- Repo file types: ${input:fileTypes:What file types does the repository contain?}
- Current config: ${input:config:What .editorconfig or formatting rules already exist?}
- Gap to fix: ${input:gap:What formatting or consistency problem should be solved?}

## Workflow

1. Inspect the current `.editorconfig`, repo file types, and related formatting tools.
2. Identify the smallest useful default rule set and the narrow overrides that matter.
3. Apply the `editorconfig` guidance together:
   - `../agents/editorconfig.agent.md`
   - `../instructions/editorconfig.instructions.md`
   - `../skills/editorconfig/SKILL.md`
4. Pair with focused slices when relevant:
   - `../skills/repository-setup/SKILL.md`
   - `../skills/python-quality/SKILL.md`
   - `../skills/ruff-python/SKILL.md`
5. Keep the final config easy to explain and maintain.

## Output Expectations

- Summarize the current `.editorconfig` state and the gap.
- Propose or implement the rule changes.
- Explain any important default or override decisions.
- Note any interactions with other repo formatting tools.

## Quality Assurance

- Do not add overrides for file types the repo does not use.
- Do not use `.editorconfig` to duplicate tool-specific formatting policy unnecessarily.
- Keep defaults broad and exceptions narrow.
