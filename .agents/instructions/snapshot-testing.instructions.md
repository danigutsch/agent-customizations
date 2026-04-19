---
description: 'Guidance for snapshot and approval testing, including baseline files, scrubbing, review flow, and CI behavior.'
applyTo: 'tests/**/*, **/*.verified.*, **/*.received.*, .gitignore, .gitattributes, .agents/agents/snapshot-testing.agent.md, .agents/skills/snapshot-testing/**'
---

# Snapshot Testing Guidance

Use these rules when the task is about snapshot or approval testing rather than generic unit-test
style.

## Core model

- Use snapshot testing when output shape matters more than one isolated scalar value.
- Treat approved snapshot files as durable contracts that deserve human review.
- Prefer repository-consistent approval tooling over inventing a new snapshot framework mid-task.

## Fit rules

- Prefer snapshots for rendered HTML, serialized payloads, HTTP responses, generated code, or public
  API surfaces.
- Prefer explicit assertions for business rules, calculations, and narrow behavioral checks.
- Pair snapshots with focused assertions when one or two invariants should remain immediately visible.

## Baseline rules

- Commit approved `.verified.*` files to source control.
- Ignore `.received.*` files and similar review artifacts.
- Keep snapshot file locations predictable, usually under one explicit test-project snapshot folder.
- Use descriptive test names because they often shape the approved file names.

## Stability rules

- Scrub timestamps, GUIDs, random values, tokens, and machine-specific paths before approving
  baselines.
- Make ordering deterministic before snapshotting collections or generated output.
- Avoid approving snapshots that differ on every run; fix the volatility first.

## CI and maintenance rules

- Keep CI non-interactive for snapshot failures and prefer artifact upload or diff output over silent
  overwrites.
- Treat baseline approval as an explicit review action, not an automatic test-side effect.
- Prefer one snapshot approach per repository or test stack unless the repo already documents multiple
  distinct patterns.

## Verification

- Confirm the task really benefits from snapshot testing.
- Confirm `.received.*` artifacts remain ignored and approved snapshot files remain reviewable.
- Confirm scrubbers and ordering controls make repeated runs stable.
- Confirm CI behavior matches the repository's existing test and artifact workflow.
