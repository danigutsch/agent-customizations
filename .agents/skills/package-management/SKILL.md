---
name: package-management
description: Guidance for package and SDK management. Use when reviewing central package version files, `global.json`, lock-file policy, restore flow, project-specific dependency exceptions, or cautious dependency-governance automation in a repository.
---

# Package Management

Use this skill when the task is about dependency policy and restore reproducibility rather than one
package bump alone.

## When to Use This Skill

- The user needs to review central package version management
- The user needs SDK pinning or `global.json` guidance
- The user needs lock-file update and verification rules
- The user needs to decide whether a dependency belongs centrally or in one project
- The user needs cautious dependency-governance automation guidance

## Prerequisites

- The repository's package files, SDK pin, and restore commands can be inspected.
- The task is mainly about dependency ownership and policy.

## Workflow

### 1. Identify the source of truth

- Check where package versions and SDK versions are owned.
- Check whether the repo uses lock files and different local-versus-CI restore modes.

### 2. Keep policy aligned

- Align central package versions, restore commands, and contributor docs.
- Document project-specific exceptions instead of letting them drift silently.

### 3. Review update flow

- Treat automation as proposal generation, not automatic acceptance.
- Keep major upgrades and lock-file refreshes visible and reviewable.

## Related guidance

- Pair with [Ci Workflows](../ci-workflows/SKILL.md) when restore and lock verification should run in
  CI.
- Pair with [Repository Setup](../repository-setup/SKILL.md) when dependency policy must be part of
  contributor guidance.

## Gotchas

- **Do not split version ownership across many places without a reason.**
- **Do not forget lock-file policy when changing package resolution.**
- **Do not treat automated update PRs as self-approving.**

## References

- [Package management guidance](../../instructions/package-management.instructions.md)
- [Package management agent](../../agents/package-management.agent.md)
