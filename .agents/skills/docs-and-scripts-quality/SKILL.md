---
name: docs-and-scripts-quality
description: Guidance for repository documentation quality, helper script maintenance, and local validation workflow alignment. Use when improving Markdown docs, repo maintenance scripts, hooks, or the documented contributor check path without inventing a new quality stack.
---

# Docs and Scripts Quality

Use this skill when the task is about keeping docs, scripts, and the documented local validation path
coherent.

## When to Use This Skill

- The user wants to improve maintenance docs or README guidance
- The user is changing repository helper scripts and wants the docs to stay accurate
- The user is updating hooks or local validation flow
- The user wants docs and script quality guidance that matches the repository's real checks
- The user wants to reduce drift between commands, hooks, and documentation

## Prerequisites

- The relevant docs, scripts, or hook entrypoints can be inspected.
- The repository's current validation commands are known.
- The quality issue can be addressed with existing repo tooling.

## Workflow

### 1. Inspect the operating surface

- Read the docs, scripts, hook entrypoints, and validation commands together.
- Treat them as one contributor-facing workflow.

### 2. Prefer the existing checks

- Reuse the repository's current validation commands when they already cover the change.
- Add new tooling only when the repo has intentionally adopted it.

### 3. Keep docs and scripts aligned

- Update command examples when script or make entrypoints change.
- Keep hook behavior aligned with the documented local quality path.

### 4. Validate against the real workflow

- Use the existing repo commands to confirm the updated docs and scripts still match reality.

## Related guidance

- Pair with [Python quality](../python-quality/SKILL.md), [Ruff Python](../ruff-python/SKILL.md), or
  [Pyright Python](../pyright-python/SKILL.md) when the change is mainly about Python script quality.
- Pair with [Git hooks](../git-hooks/SKILL.md) when hook behavior should change with the local
  validation flow.
- Pair with [DocFX Specialist](../../agents/docfx-specialist.agent.md) when the docs quality problem
  is DocFX-specific rather than repo-wide.

## Gotchas

- **Do not document commands the repo does not have**.
- **Do not invent a parallel quality workflow**.
- **Do not let hooks diverge from the documented local checks**.
- **Do not weaken existing checks to make one change easier**.

## References

- [Docs and scripts quality guidance](../../instructions/docs-and-scripts-quality.instructions.md)
- [Docs and scripts quality agent](../../agents/docs-and-scripts-quality.agent.md)
- [Slice inventory](../../../docs/SLICES.md)
