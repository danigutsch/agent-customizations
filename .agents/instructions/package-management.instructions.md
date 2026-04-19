---
description: 'Guidance for package management: central versioning, SDK pinning, lock files, restore policy, and dependency-governance flow.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/package-management.agent.md, .agents/skills/package-management/**, .agents/instructions/package-management.instructions.md'
---

# Package Management Guidance

Use these rules when the task is about dependency and SDK policy rather than one isolated package
change.

## Core model

- Keep package versions, SDK pinning, and restore policy under one explicit ownership model.
- Prefer central management for routine shared dependencies.
- Treat lock files and restore settings as part of the contract for reproducible builds.
- Keep dependency automation reviewable and policy-driven.

## Version-ownership rules

- Prefer central package version files when the repo has adopted them.
- Keep transitive pinning explicit when it is intentionally used.
- Document project-specific exceptions instead of silently bypassing central ownership.
- Keep analyzer, tooling, runtime, and test dependencies explicit about why they belong where they do.

## SDK and restore rules

- Pin the SDK in `global.json` when the repository expects aligned local and CI behavior.
- Keep roll-forward policy explicit.
- Regenerate and verify lock files when dependency resolution changes.
- Keep locked and unlocked restore expectations documented for local versus CI use.

## Governance rules

- Use dependency automation to propose updates, not to bypass review.
- Group updates conservatively when the repository prefers lower churn.
- Review major upgrades and transitive graph changes deliberately.

## Verification

- Confirm package and SDK ownership are explicit.
- Confirm lock-file and restore policy match the documented workflow.
- Confirm project-specific dependency exceptions are intentional and documented.
- Confirm dependency automation aligns with the repository's review policy.
