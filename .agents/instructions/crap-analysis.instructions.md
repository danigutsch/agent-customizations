---
description: 'Guidance for complexity-plus-coverage risk review, hotspot ranking, targeted cleanup, and excluding misleading generated surfaces.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/crap-analysis.agent.md, .agents/skills/crap-analysis/**, .agents/instructions/crap-analysis.instructions.md'
---

# Crap Analysis Guidance

Use these rules when the task is about maintainability hotspots where complexity and low coverage
combine into elevated risk.

## Core model

- Complexity becomes more dangerous when tests do not protect the behavior.
- Rank hotspots by risk, not by metric value alone.
- Prefer small targeted cleanup plus focused tests over broad rewrites.
- Keep generated or excluded code out of the ranking when it is not part of the maintained source
  set.

## Review rules

- Identify methods, classes, or components with complicated branching and weak test coverage.
- Consider business criticality and change frequency when prioritizing hotspots.
- Treat coverage reports and hosted quality gates as supporting evidence, not the only truth.
- Do not use maintainability metrics to justify speculative architectural rewrites.

## Improvement rules

- Prefer extracting decision points, reducing nesting, and clarifying branch boundaries.
- Add targeted tests for risky paths before or alongside refactoring.
- Keep each change small enough to revalidate with the repository's existing tooling.

## Verification

- Confirm the hotspot is curated maintained code, not generated or excluded surface.
- Confirm the cleanup reduces practical change risk, not only metric values.
- Confirm focused tests now cover the branches that made the hotspot risky.
