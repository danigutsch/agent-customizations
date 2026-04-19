---
description: 'Guidance for devcontainer smoke validation: shared local-and-CI scripts, non-interactive checks, lifecycle coverage, failure diagnostics, and supplemental workflow boundaries.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/devcontainers-smoke.agent.md, .agents/skills/devcontainers-smoke/**, .agents/instructions/devcontainers-smoke.instructions.md'
---

# Devcontainers Smoke Guidance

Use these rules when the task is about validating a documented devcontainer workflow rather than
general container authoring.

## Core model

- Treat devcontainer smoke validation as a reproducibility check for the supported contributor
  environment.
- Prefer one shared validation script for local and CI use.
- Keep smoke validation non-interactive and aligned with the actual lifecycle hooks the container
  path depends on.
- Separate low-cost frequent smoke checks from heavier in-container validation.

## Support-path rules

- Document which devcontainer workflow is supported and what contributor path it covers.
- Keep prerequisites explicit, including editor/runtime requirements and host-resource expectations
  when they materially affect success.
- Verify the environment contract the devcontainer claims to provide rather than only whether the
  container build succeeds.

## Shared-script rules

- Prefer a repository-owned smoke script that CI invokes directly.
- Keep workflow YAML thin when a shared script can own the validation logic.
- Let the configured devcontainer lifecycle hooks run so the smoke path matches real usage.
- Keep the script safe to run from a clean checkout and explicit about required host commands.

## Validation-mode rules

- Keep the default smoke path low-cost enough for regular CI and local use.
- Add a deeper mode only when the repository benefits from occasionally running tests or other heavy
  checks inside the temporary container.
- Make mode selection explicit through script flags or workflow inputs rather than hidden branching.

## Diagnostics and cleanup rules

- Write logs to a predictable repository-owned output folder.
- Clean up temporary containers automatically unless the user explicitly opts to keep them.
- Upload or preserve logs on CI failure so contributors can debug the same path locally.
- Keep metadata such as container IDs or selected modes available when that improves diagnostics.

## Trigger and governance rules

- Trigger CI smoke runs from `.devcontainer/**` and other inputs that materially affect the
  containerized environment.
- Keep supplemental devcontainer validation separate from the primary merge gate unless the
  repository intentionally promotes it.
- Treat Dev Container CLI version changes and feature updates as validation-worthy environment
  changes.
- Consider dependency-governance tooling for the `devcontainers` ecosystem when the repo uses
  feature references in `devcontainer.json`.

## Verification

- Confirm contributors and CI use the same smoke command path.
- Confirm the smoke path runs the real lifecycle hooks and verifies the promised toolchains.
- Confirm the workflow trigger surface matches the files that actually affect the environment.
- Confirm smoke logs and cleanup behavior are explicit.
- Confirm any deeper validation mode is intentionally separate from the default smoke path.
