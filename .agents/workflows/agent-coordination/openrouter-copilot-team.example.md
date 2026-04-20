# OpenRouter plus Copilot team workflow

This starter example shows one way to coordinate a Copilot-led team with lower-cost external worker
lanes. Adapt the lanes, models, and checkpoints to the target repository instead of treating this
as a fixed required process.

## Goal

Coordinate a mixed team where Copilot owns repo-aware editing and final judgment, while external
workers handle low-cost scouting, summarization, and draft generation.

## Phases

1. Define the task and split it into explicit lanes.
2. Route scouting and inventory work to the cheapest reliable models.
3. Route focused edits to a stronger coding lane with local tool access.
4. Run validation and drift checks in a separate validator lane.
5. Escalate architecture, security, or release judgment to the final reviewer lane.

## Lane matrix

| Lane | Mission | First-choice model | Escalation model | Output |
| --- | --- | --- | --- | --- |
| Coordinator | own scope, sequence work, resolve collisions | Copilot `gpt-5.4` | `claude-sonnet-4.6` | assignments and merge decisions |
| Scout | inventory, upstream comparison, search summaries | `gemini-2.5-flash-lite` or `qwen3-coder` | `deepseek-v3.2` | gap report or comparison notes |
| Implementer | focused edits and bounded refactors | Copilot `gpt-5.3-codex` | `gpt-5.1-codex-mini` | repo changes |
| Validator | run commands and inspect diffs | cheap Copilot task lane | `gpt-4.1` | check results and drift findings |
| Reviewer | architecture, security, final release judgment | `claude-sonnet-4.6` | `claude-opus-4.7` | accept or escalate decision |

## Handoffs

- The coordinator lane defines ownership before any worker starts.
- The scout lane hands off a concise report, not raw exploration noise.
- The implementer lane starts only after scope and file boundaries are clear.
- The validator lane reports what passed, what failed, and what needs escalation.
- The reviewer lane decides whether the work is complete or must loop back.

## Checkpoints

- Repo-local versus user-local Copilot authority is explicit.
- Cheap workers are not used as final reviewers.
- File ownership is clear before parallel edits begin.
- Validation happens before final review.

## Adaptation notes

- Repositories can swap model vendors while keeping the same lane structure.
- Repositories can collapse lanes when the task is small, but should keep final review explicit.
- Repositories with MCP wrappers can map the scout lane to those wrappers without changing the core
  workflow.
