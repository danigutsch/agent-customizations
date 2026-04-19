---
name: devcontainers-smoke
description: Guidance for smoke-validating a documented devcontainer workflow. Use when creating or reviewing `.devcontainer/**` support guidance, shared local-and-CI smoke scripts, lifecycle-hook validation, optional deeper in-container test modes, failure-log capture, or supplemental CI workflows for devcontainer drift.
---

# Devcontainers Smoke

Use this skill when the task is about validating and maintaining a documented devcontainer workflow
rather than about general container setup alone.

## When to Use This Skill

- The user needs a reproducible smoke-validation path for a devcontainer workflow
- The user needs one script that both contributors and CI can run
- The user needs to verify lifecycle hooks and basic toolchains inside a temporary devcontainer
- The user needs to separate low-cost smoke checks from deeper in-container validation
- The user needs failure logs, cleanup, or keep-container behavior for devcontainer debugging
- The user needs a supplemental workflow that reacts to devcontainer and bootstrap drift

## Prerequisites

- The repository has a documented or intended `.devcontainer/**` path that can be inspected.
- The current lifecycle commands or bootstrap steps are known well enough to validate.
- The task is about the smoke-validation model, not only about editing editor extensions or image
  contents.

## Workflow

### 1. Identify the supported devcontainer path

- Read the contributor guidance, `.devcontainer/devcontainer.json`, lifecycle hooks, and any
  smoke-validation scripts together.
- Define the minimum environment contract the devcontainer promises.

### 2. Keep one shared smoke path

- Prefer one repository-owned script for local and CI use.
- Let the real lifecycle hooks run during validation instead of simulating only part of the path.
- Verify the promised toolchains or runtime dependencies inside the container.

### 3. Split smoke from deeper validation

- Keep the default path fast enough for routine use.
- Add an explicit deeper mode when the repository benefits from running tests or heavier checks
  inside the temporary container.
- Use schedule or manual workflow inputs for the deeper mode when that keeps CI cost reasonable.

### 4. Make failures easy to inspect

- Write logs to a predictable output folder.
- Clean up by default, but allow an explicit keep-container option for post-failure debugging.
- Upload logs on CI failure so contributors can reproduce the same path locally.

## Related guidance

- Pair with [Ci Workflows](../ci-workflows/SKILL.md) when the smoke path needs a supplemental
  workflow, path filters, schedule, or dispatch input model.
- Pair with [Repository Setup](../repository-setup/SKILL.md) when the repo needs broader contributor
  guidance around its supported development environments.
- Pair with [Docs And Scripts Quality](../docs-and-scripts-quality/SKILL.md) when troubleshooting
  docs and helper scripts need maintenance together.

## Gotchas

- **Do not let CI and local devcontainer validation drift into separate implementations.**
- **Do not treat a successful container build as proof that the contributor workflow actually works.**
- **Do not run the heavy path on every change if the repo only needs a low-cost drift check most of the time.**
- **Do not hide logs or cleanup behavior when startup failures are hard to reproduce.**

## References

- [Devcontainers smoke guidance](../../instructions/devcontainers-smoke.instructions.md)
- [Devcontainers smoke agent](../../agents/devcontainers-smoke.agent.md)
