# Routing policy rollout workflow

This starter example shows one way to turn a model-routing idea into one reusable operating policy.
Adapt the lanes, model names, and checkpoints to the target repository instead of treating this as a
fixed required process.

## Goal

Adopt one explicit routing policy so cheap scout lanes stay cheap, stronger review lanes stay
intentional, and Copilot versus external-worker boundaries remain stable over time.

## Inputs

- the lane set the repository wants to use
- the default runtime authority, usually user-level `~/.copilot/*`
- the allowed model families for each lane
- any repositories that need repo-level `.github/*` override behavior

## Phases

1. Define the lane set and runtime-authority default.
2. Assign one default model, one fallback set, and one escalation cap per lane.
3. Decide when free models are allowed and when they are forbidden.
4. Publish the routing policy in one reusable config example and one short workflow note.
5. Validate that local sync and review guidance still match the chosen authority model.

## Lane policy checklist

| Lane | Must define |
| --- | --- |
| Coordinator | default model, strong fallback, hard escalation path |
| Scout | cheap default, paid fallback, maximum allowed escalation |
| Implementer | repo-aware coding default, higher-cost fallback, explicit escalation approval rule |
| Validator | low-cost deterministic default, readable fallback, validation checkpoint output |
| Reviewer | strong default, hard escalation ceiling, merge-readiness rule |
| Documentation | cheap drafting default, stronger final polish fallback |

## Checkpoints

- The default runtime authority is explicit.
- Free models are limited to scout-like or disposable work.
- Every lane has a known ceiling instead of open-ended escalation.
- Reviewer or coordinator approval is required before premium escalation.
- Repo-level overrides are documented as exceptions, not the default.

## Adaptation notes

- A small repository can collapse scout and validator into one lane if ownership stays explicit.
- A repository with local MCP wrappers can keep the same policy structure and only swap runtime
  labels or model names.
- A repository that does not use OpenRouter can still keep the same fallback and escalation logic
  with different providers.
