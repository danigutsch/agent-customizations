---
description: 'Guidance for automatable license inventory, policy gates, SBOM outputs, and review boundaries for open-source compliance workflows.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/license-checking.agent.md, .agents/skills/license-checking/**, .agents/instructions/license-checking.instructions.md'
---

# License Checking Guidance

Use these rules when the task is about automating license inventory, policy checks, SBOM generation,
or CI/local enforcement for open-source dependencies and imported assets.

## Core model

- Treat license checking as an **automation and inventory** problem first.
- Keep machine-readable policy outcomes explicit: allowed, denied, and review-required.
- Route ambiguous or high-impact results into broader compatibility review instead of pretending the
  checker is the whole answer.

## Inventory rules

- Prefer resolved dependency coverage over manifest-only guesses when lockfiles or packaged artifacts
  exist.
- Include direct and transitive dependencies where the ecosystem makes that possible.
- Call out incomplete coverage when a tool cannot see vendored files, built images, or runtime-added
  dependencies.

## Policy and gating

- Keep policy rules durable and reviewable rather than burying them in ad hoc script logic.
- Treat unknown, missing, or custom-license metadata as triage signals rather than silent passes.
- Make failure, warning, and review-required paths explicit so maintainers know what blocks release and
  what enters review.

## SBOM guidance

- Prefer SPDX or CycloneDX for machine-readable SBOM artifacts.
- Generate SBOMs from the resolved or built dependency graph when the tooling supports that.
- Keep release association and retention expectations explicit when documenting SBOM workflows.

## Boundary with FOSS compatibility

- Use `license-checking` for automated inventory and policy checks.
- Use `foss-compatibility` when the result still needs interpretation about redistribution,
  obligations, or mixed-license compatibility.
- Do not let the automated gate imply that broader legal or distribution questions are closed.

## Verification

- Confirm the guidance covers lockfiles or resolved dependency sources where relevant.
- Confirm policy outcomes are explicit and machine-readable.
- Confirm unknown or missing license data is surfaced rather than silently allowed.
- Confirm the docs explain when a finding moves from automation into broader review.
