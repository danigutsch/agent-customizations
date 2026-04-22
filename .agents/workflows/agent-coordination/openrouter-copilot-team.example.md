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
| Scout | inventory, upstream comparison, search summaries | `qwen/qwen3-coder:free` | `nvidia/nemotron-3-super-120b-a12b:free` | gap report or comparison notes |
| Implementer | focused edits and bounded refactors | Copilot `gpt-5.3-codex` | `gpt-5.1-codex-mini` | repo changes |
| Validator | run commands and inspect diffs | cheap Copilot task lane | `gpt-4.1` | check results and drift findings |
| Reviewer | architecture, security, final release judgment | `claude-sonnet-4.6` | `claude-opus-4.7` | accept or escalate decision |

## Current free-model recommendation snapshot

This snapshot reflects the OpenRouter free-model catalog and public benchmark or recommendation
signal reviewed in April 2026. Treat it as a starting point to revisit, not a permanent truth.

- `qwen/qwen3-coder:free` is the default scout lane because OpenRouter positions it for agentic
  coding, tool use, and long-context repository reasoning.
- `nvidia/nemotron-3-super-120b-a12b:free` is the main hard-reasoning escalation because the
  OpenRouter free-model collection highlights AIME 2025, TerminalBench, and SWE-Bench Verified.
- `openai/gpt-oss-120b:free` is the alternate deep-reasoning or tool-use fallback when Nemotron
  capacity is tight or another reasoning style is useful.
- `z-ai/glm-4.5-air:free` is a strong synthesis or agent fallback because OpenRouter describes it
  as purpose-built for agent-centric applications with controllable reasoning modes.
- `google/gemma-4-31b-it:free` is the stable documentation or general chat fallback because
  OpenRouter highlights its 256K context, tool use, multimodal support, and strong reasoning.
- `openrouter/free` is useful for casual experimentation, but avoid it for reproducible lane policy
  because the routed backend can change underneath the workflow.

## Copilot CLI BYOK setup notes

If a repository adapts this workflow to GitHub Copilot CLI with a custom OpenRouter provider, treat
the lane model IDs in this document as **provider wire models**, not automatically as the safest
internal Copilot model identifiers.

- Prefer the split Copilot CLI provider configuration when the OpenRouter model ID is not part of
  Copilot's built-in catalog or when the provider model includes suffixes such as `:free`.
- Set `COPILOT_PROVIDER_MODEL_ID` to a well-known Copilot model ID so the CLI can keep stable
  internal defaults for prompting, tool support, and token sizing.
- Set `COPILOT_PROVIDER_WIRE_MODEL` to the actual OpenRouter model ID that should be sent to the
  provider.
- Avoid relying on a raw OpenRouter model such as `z-ai/glm-4.5-air:free` as the only
  `COPILOT_MODEL` value in Copilot CLI BYOK setups because Copilot may treat it as both the
  internal model key and the provider wire model.
- Keep OpenRouter reasoning controls in the provider request layer, where supported, instead of
  trying to encode them as Copilot model-option keys.

Example Copilot CLI environment shape:

```bash
export COPILOT_PROVIDER_TYPE="openai"
export COPILOT_PROVIDER_BASE_URL="https://openrouter.ai/api/v1"
export COPILOT_PROVIDER_API_KEY="YOUR_OPENROUTER_API_KEY"
export COPILOT_PROVIDER_MODEL_ID="gpt-5.4"
export COPILOT_PROVIDER_WIRE_MODEL="z-ai/glm-4.5-air:free"
unset COPILOT_MODEL
```

For GPT-5-family wire models, also set `COPILOT_PROVIDER_WIRE_API="responses"` when the provider
expects the Responses API. For non-GPT-5 OpenAI-compatible models, the default chat/completions
wire behavior is usually the safer starting point.

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
- Repositories that want deterministic free-model behavior should pin explicit OpenRouter model IDs
  instead of relying on `openrouter/free`.
- Repositories can collapse lanes when the task is small, but should keep final review explicit.
- Repositories with MCP wrappers can map the scout lane to those wrappers without changing the core
  workflow.
