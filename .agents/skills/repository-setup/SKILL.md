---
name: repository-setup
description: 'Create or improve repo foundations. Use for structure, README, guidance files, validation scripts, CI setup, templates, examples, and upkeep.'
---

# Repository Setup

Use this skill when the task is about establishing or improving the foundations of a repository
rather than implementing a single product feature.

## When to Use This Skill

- User asks to initialize or reorganize a repository
- User wants a clearer README, top-level structure, or contributor guidance
- User wants validation or CI expectations made explicit
- User wants reusable docs, templates, scripts, or examples arranged coherently
- User wants repository setup that is portable and maintainable

## Prerequisites

- The repository purpose is known or can be inferred.
- The current top-level structure can be inspected.
- Existing validation, build, or maintenance commands are known or discoverable.

## Workflow

### 1. Clarify the repository model

- Identify what the repository stores, what it should not store, and who will maintain it.
- Decide whether the repository is product-specific, reusable, or mixed.
- Keep the top-level explanation aligned with that purpose.

### 2. Shape the top-level structure

- Keep the main folders few, explicit, and purpose-driven.
- Place docs, examples, scripts, templates, and reusable assets where contributors can find them.
- Avoid silent overlap between similarly named folders or files.
- See [Repository foundations](./references/repository-foundations.md).

### 3. Make the operating surface explicit

- Ensure repository-wide guidance is documented.
- Document how contributors validate changes.
- Add lightweight scripts when repeated manual checks would be error-prone.
- See [Validation and CI](./references/validation-and-ci.md).

### 4. Keep automation proportional

- Prefer one clear local command over many hidden steps.
- Treat CI as a wrapper around the real repository-local validation path.
- Add reusable automation only after the local validation path is stable.

## Related guidance

- If the repository organizes reusable capability slices, pair this with slice-specific setup such as
  [Source generation](../source-generation/SKILL.md) or
  [Vertical slice architecture](../vertical-slice-architecture/SKILL.md) where appropriate.
- Pair this with [CI workflows](../ci-workflows/SKILL.md) when the work includes workflow creation,
  automation, or validation orchestration.
- Pair this with [EditorConfig](../editorconfig/SKILL.md) when the work includes shared editor
  defaults across mixed file types.
- Pair this with [Python quality](../python-quality/SKILL.md),
  [Ruff Python](../ruff-python/SKILL.md), and
  [Pyright Python](../pyright-python/SKILL.md) when Python tooling is part of the repository
  baseline.
- Pair this with [Git hooks](../git-hooks/SKILL.md) when local hook setup should complement CI and
  repository-local validation.

## Gotchas

- **Do not optimize for every possible future tool** — start with the repository's current purpose.
- **Do not scatter repository rules** — put core operating guidance where contributors will actually
  look.
- **Do not add CI first** — define the local validation path before wrapping it in automation.
- **Do not confuse reusable assets with repo-specific rules** — keep the boundary explicit.

## References

- [Repository foundations](./references/repository-foundations.md)
- [Validation and CI](./references/validation-and-ci.md)
- [Repository setup instructions](../../instructions/repository-setup.instructions.md)
- [Repository setup agent](../../agents/repository-setup.agent.md)
