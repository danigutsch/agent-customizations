---
name: license-checking
description: Guidance for automated open-source license inventory and policy checks. Use when setting up dependency or asset license scans, defining allow-deny-review rules, generating SPDX or CycloneDX SBOMs, checking lockfile coverage, or wiring license gates into local and CI workflows.
---

# License Checking

Use this skill when the task is about automating license inventory, policy enforcement, or SBOM
generation for open-source dependencies and imported assets.

## When to Use This Skill

- The user wants a repeatable license scan for dependencies, vendored files, or packaged outputs
- The user needs allow, deny, or review-required policy gates
- The user needs SPDX- or CycloneDX-based SBOM workflow guidance
- The user wants local or CI license checks that cover resolved dependencies rather than only
  manifests
- The user needs to distinguish automatable checks from cases that must be escalated for broader
  compatibility review

## Prerequisites

- The dependency or asset scope can be identified.
- The manifests, lockfiles, or artifacts to inventory can be inspected.
- The review boundary is clear enough to separate automated checks from broader legal analysis.

## Workflow

### 1. Define the inventory scope

- Decide whether the workflow covers source manifests, lockfiles, vendored files, release artifacts,
  or multiple layers.
- Prefer resolved dependency coverage when the ecosystem supports it.

### 2. Define the policy outcomes

- Keep categories explicit: allowed, denied, and needs review.
- Treat unknown or missing license metadata as triage input, not an automatic pass.

### 3. Produce machine-readable artifacts

- Prefer SPDX or CycloneDX when SBOM output is part of the workflow.
- Keep the generated artifact tied to the build or release context that produced it.

### 4. Connect the review boundary

- Let automation route non-routine findings.
- Hand broader compatibility, redistribution, or obligations questions to
  [FOSS Compatibility](../foss-compatibility/SKILL.md).

## Related guidance

- Pair with [FOSS Compatibility](../foss-compatibility/SKILL.md) when the check result still needs
  interpretation about obligations or redistribution.
- Pair with [CI Workflows](../ci-workflows/SKILL.md) when the checking flow needs pipeline wiring.

## Gotchas

- **Do not scan manifests only when lockfiles exist.**
- **Do not treat unknown-license findings as harmless.**
- **Do not confuse policy automation with final compatibility judgment.**
- **Do not hide coverage gaps in the scan story.**

## References

- [License checking guidance](../../instructions/license-checking.instructions.md)
- [License checking agent](../../agents/license-checking.agent.md)
