---
name: editorconfig
description: 'Create or improve repo EditorConfig defaults. Use for .editorconfig structure, text defaults, indentation overrides, and formatter alignment.'
---

# EditorConfig

Use this skill when the task is about a repository `.editorconfig` rather than a language-specific
formatter alone.

## When to Use This Skill

- User wants to add or clean up `.editorconfig`
- User wants consistent editor defaults across file types
- User wants indentation or whitespace rules aligned with repo tooling
- User wants `.editorconfig` reviewed alongside Ruff, Markdown, JSON, or YAML formatting

## Prerequisites

- The repository's file types can be inspected.
- The current `.editorconfig` and related formatting tools are known or discoverable.

## Workflow

### 1. Inspect the real file surface

- Identify which file types are common in the repo.
- Keep overrides tied to files that actually exist or are about to be introduced.

### 2. Define the baseline first

- Start with broad defaults for text files:
  encoding, line endings, final newline behavior, and trailing whitespace handling.
- Add focused overrides later for Markdown, Python, JSON, YAML, Makefiles, or other formats that
  need different indentation or trimming behavior.

### 3. Keep tool boundaries clear

- Let `.editorconfig` own editor defaults.
- Let tool-specific formatters own language or syntax formatting details.
- Keep the two aligned so contributors do not get conflicting signals.

## Related guidance

- Pair this with [Repository setup](../repository-setup/SKILL.md) when `.editorconfig` is part of a
  broader repo foundation update.
- Pair this with [Python quality](../python-quality/SKILL.md) or
  [Ruff Python](../ruff-python/SKILL.md) when Python files are part of the repo baseline.

## Gotchas

- **Do not overload `.editorconfig`** — it is a baseline, not a full formatter replacement.
- **Do not add speculative file sections** — keep the file grounded in the repo's actual contents.
- **Do not forget rule order** — later matching sections override earlier ones.

## References

- [EditorConfig instructions](../../instructions/editorconfig.instructions.md)
- [EditorConfig agent](../../agents/editorconfig.agent.md)
