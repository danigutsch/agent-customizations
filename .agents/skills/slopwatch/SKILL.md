---
name: slopwatch
description: Guidance for detecting low-signal bloat and AI-generated sprawl. Use when reviewing duplicated helpers, speculative abstractions, noisy docs, broad wrapper layers, or imported scaffolding that may not belong in the maintained source set.
---

# Slopwatch

Use this skill when the task is about reducing low-signal sprawl rather than about one specific
technology stack.

## When to Use This Skill

- The user wants a change reviewed for duplication or unnecessary abstraction
- The user suspects AI-generated bloat or wrapper sprawl
- The user needs to decide whether scaffolding should stay generated or become curated
- The user wants to simplify docs, scripts, or code without losing the real workflow

## Prerequisites

- The changed files and nearby established patterns can be inspected.
- The main issue is maintainability and signal-to-noise, not only formatting.

## Workflow

### 1. Compare with local patterns

- Inspect the nearest maintained local pattern before judging the change.
- Look for surface growth that does not buy meaningful clarity or capability.

### 2. Classify the slop

- Duplication
- speculative abstraction
- wrapper layering
- noisy documentation
- generated or imported scaffolding treated as curated

### 3. Reduce without overengineering

- Prefer deletion, narrowing, or reuse.
- Keep the simplest clear maintained shape.

## Related guidance

- Pair with [Docs And Scripts Quality](../docs-and-scripts-quality/SKILL.md) when the drift is mainly
  in maintenance docs or helper scripts.
- Pair with [Tool Generated File Provenance](../tool-generated-file-provenance/SKILL.md) when the
  real issue is curated-versus-generated ownership.

## Gotchas

- **Do not confuse explicitness with slop automatically.**
- **Do not replace bloat with a clever abstraction that is harder to follow.**
- **Do not assume imported scaffolding belongs in the maintained source set.**

## References

- [Slopwatch guidance](../../instructions/slopwatch.instructions.md)
- [Slopwatch agent](../../agents/slopwatch.agent.md)
