---
description: 'Guidance for slopwatch review: low-signal bloat, duplication, speculative abstractions, and AI-generated sprawl.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/slopwatch.agent.md, .agents/skills/slopwatch/**, .agents/instructions/slopwatch.instructions.md'
---

# Slopwatch Guidance

Use these rules when the task is about reviewing or reducing low-signal repository sprawl.

## Core model

- Slop is surface area that costs maintenance without carrying enough value.
- Prefer local pattern comparison over abstract purity tests.
- Distinguish curated source from generated or imported scaffolding before judging churn.
- Prefer deletion, narrowing, or reuse before adding another abstraction.

## Review rules

- Look for duplication, speculative helpers, wrapper layers, and broad low-value expansion.
- Treat "AI-shaped" change patterns as signals to inspect, not as proof on their own.
- Keep one clear workflow or path where the repo currently has many overlapping variants.
- Avoid making the cleanup itself cleverer than the original problem.

## Boundary rules

- Keep generated or imported scaffolding outside the maintained source set unless the repo explicitly
  owns it.
- Pair structural cleanup with policy updates when drift keeps recurring.
- Do not collapse valuable explicitness just to reduce line count.

## Verification

- Confirm the maintained surface is smaller, clearer, or more reusable after cleanup.
- Confirm duplication or speculative abstractions were removed or justified.
- Confirm generated-versus-curated ownership is explicit where it matters.
