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
- The repository already has the docs, scripts, or hooks being aligned; this skill is for
  maintenance and drift cleanup rather than initial repo structure setup.

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
- If one narrow generated README section is the clearest way to avoid drift, keep the generation
  scope explicit and validate it through the repository's existing check path.
- If the repository wants shareable local Git guidance, prefer a tracked opt-in config file plus one
  setup command over duplicating long manual `git config` sequences in docs.

### 4. Validate against the real workflow

- Use the existing repo commands to confirm the updated docs and scripts still match reality.

## Related guidance

- Pair with [Python quality](../python-quality/SKILL.md), [Ruff Python](../ruff-python/SKILL.md), or
  [Pyright Python](../pyright-python/SKILL.md) when the change is mainly about Python script quality.
- Pair with [Git hooks](../git-hooks/SKILL.md) when hook behavior should change with the local
  validation flow.
- Pair with [MkDocs Specialist](../../agents/mkdocs-specialist.agent.md) when the docs quality problem
  is MkDocs-site-specific rather than repo-wide.

## Gotchas

- **Do not document commands the repo does not have**.
- **Do not invent a parallel quality workflow**.
- **Do not let hooks diverge from the documented local checks**.
- **Do not auto-generate broad docs surfaces when one small owned section is enough**.
- **Do not weaken existing checks to make one change easier**.
- **Do not use this for first-time repo structure or baseline setup**; use `repository-setup` for
  that.

## References

- [Docs and scripts quality guidance](../../instructions/docs-and-scripts-quality.instructions.md)
- [Docs and scripts quality agent](../../agents/docs-and-scripts-quality.agent.md)
- [Capability inventory](../../../docs/CAPABILITIES.md)
