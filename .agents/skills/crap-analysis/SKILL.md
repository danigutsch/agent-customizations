---
name: crap-analysis
description: Guidance for complexity-plus-coverage hotspot review. Use when ranking risky methods or classes, planning focused refactors, using coverage reports to find fragile code, or excluding generated surfaces that would distort maintainability analysis.
---

# Crap Analysis

Use this skill when the task is about complexity and weak test protection creating maintainability
risk.

## When to Use This Skill

- The user needs to find risky complex code with poor coverage
- The user needs to prioritize cleanup without rewriting everything
- The user needs to interpret coverage reports as part of hotspot analysis
- The user needs to exclude generated or non-owned files from the ranking

## Prerequisites

- The hotspot code and current test/coverage context can be inspected.
- The task is about maintainability risk, not just raw performance or style.

## Workflow

### 1. Identify the hotspot

- Look for branching-heavy code with weak coverage or fragile tests.
- Confirm the code is actually maintained and in scope.

### 2. Rank by real risk

- Consider change frequency, business importance, and failure impact.
- Do not rank by one metric alone.

### 3. Choose the smallest effective fix

- Extract or simplify the riskiest logic.
- Add focused tests around the branches that matter most.

## Related guidance

- Pair with [Xunit V3 Mtp Test Stack](../xunit-v3-mtp-test-stack/SKILL.md) when the hotspot needs
  focused .NET coverage work.
- Pair with [Slopwatch](../slopwatch/SKILL.md) when duplication or wrapper sprawl also drives the
  risk.

## Gotchas

- **Do not optimize the metric instead of the code.**
- **Do not rank generated or excluded files the same way as maintained source.**
- **Do not turn one hotspot review into a broad rewrite campaign.**

## References

- [Crap analysis guidance](../../instructions/crap-analysis.instructions.md)
- [Crap analysis agent](../../agents/crap-analysis.agent.md)
