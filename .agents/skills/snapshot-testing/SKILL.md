---
name: snapshot-testing
description: Guidance for snapshot and approval testing, especially Verify-style baselines in .NET repositories. Use when reviewing rendered output, serialized payloads, HTTP responses, generated code, or public API surfaces that should be protected by human-approved snapshot files.
---

# Snapshot Testing

Use this skill when the task is about approval-style output verification rather than generic test
runner setup.

## When to Use This Skill

- The user wants approval tests for rendered HTML, emails, generated code, or serialized output
- The user wants to protect public API surface shape with reviewed baseline files
- The user needs guidance for `.verified.*` and `.received.*` handling
- The user needs help making snapshot output deterministic with scrubbers or normalization
- The user needs CI behavior for snapshot failures that stays reviewable and non-interactive

## Prerequisites

- The current test framework or snapshot tooling can be inspected
- The repository's `.gitignore`, CI path, and baseline-file conventions can be inspected
- The task benefits from output-shape approval rather than narrow logic assertions alone

## Workflow

### 1. Confirm snapshot testing is the right fit

- Prefer snapshots for output contracts such as rendered content, API text surfaces, or generated files
- Prefer explicit assertions for calculations, branching behavior, and simple value checks

### 2. Keep approved files and review artifacts separate

- Commit approved `.verified.*` files
- Ignore `.received.*` files
- Keep snapshot locations predictable inside the test project

### 3. Stabilize the output first

- Scrub or normalize timestamps, GUIDs, random data, tokens, and nondeterministic ordering
- Avoid approving baselines that churn between identical runs

### 4. Align the approval flow with the repo

- Reuse the repository's current test command and CI path
- Keep CI non-interactive and artifact-friendly when snapshots fail
- Treat baseline approval as a human review step

## Related guidance

- Pair with [Xunit v3 mtp test stack](../xunit-v3-mtp-test-stack/SKILL.md) when the repository also
  needs .NET runner or test-command guidance.
- Pair with [Aspnet API contracts](../aspnet-api-contracts/SKILL.md) when snapshot tests protect HTTP
  response or contract shape.
- Pair with [Event sourcing projections](../event-sourcing-projections/SKILL.md) when snapshot tests
  protect projection output or read-model shape.

## Gotchas

- **Do not replace clear logic assertions with giant snapshots.**
- **Do not commit `.received.*` files.**
- **Do not approve unstable output before adding scrubbers or deterministic ordering.**
- **Do not widen snapshot guidance into full test-platform setup unless that is the actual task.**

## References

- [Snapshot testing guidance](../../instructions/snapshot-testing.instructions.md)
- [Snapshot testing agent](../../agents/snapshot-testing.agent.md)
