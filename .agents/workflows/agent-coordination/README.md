# Agent coordination workflow assets

Reusable workflow assets for the `agent-coordination` capability live here.

## Contents

- `openrouter-copilot-team.example.md` — starter phased workflow for a Copilot-led team that routes
  cheap scout work to external models and keeps final review in a stronger repo-aware lane
- `routing-policy-rollout.example.md` — starter workflow for adopting one lane policy, fallback set,
  free-model rule set, and escalation cap model across a repository

## Notes

- Keep lanes, handoffs, and escalation rules explicit.
- Keep examples reusable and easy to adapt across repositories.
- Treat model picks as a policy snapshot that repositories can tune locally.
