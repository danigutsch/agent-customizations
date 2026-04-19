---
description: 'Guidance for open-source license compatibility review, SPDX usage, provenance recording, and escalation of non-automatable compliance questions.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/foss-compatibility.agent.md, .agents/skills/foss-compatibility/**, .agents/instructions/foss-compatibility.instructions.md'
---

# FOSS Compatibility Guidance

Use these rules when the task is about whether open-source assets can be adopted, redistributed, or
packaged together in this repository or downstream repositories.

## Core model

- Separate **inventory facts** from the **compatibility judgment**.
- Record provenance and governing-license evidence before recommending adoption.
- Treat compatibility analysis as broader than automated license detection.

## Compatibility rules

- Evaluate the actual adoption path: reference, copy, vendor, redistribute, or package together.
- Be explicit about uncertainty rather than implying a license combination is automatically safe.
- Distinguish permissive, reciprocal, and custom-license cases instead of flattening them into one
  workflow.

## Obligations

- Record attribution, license-text, NOTICE, and source-availability obligations when they apply.
- Use SPDX identifiers or SPDX-style license expressions when machine-readable license metadata is
  added.
- Do not treat a top-level repository license as sufficient evidence for imported third-party assets.

## Provenance

- Keep source URL, source path, and adoption rationale with imported or adapted material.
- Preserve enough provenance to re-check the upstream source later.
- Make ownership boundaries explicit when generated or vendored files are involved.

## Escalation

- Escalate ambiguous or high-impact cases instead of papering them over with generic best-practice
  wording.
- Escalate when provenance is weak, the governing license is unclear, or redistribution obligations are
  materially uncertain.
- Keep the escalation trigger explicit in docs so maintainers know when automation stops being enough.

## Verification

- Confirm the guidance distinguishes compatibility review from automated license checking.
- Confirm imported assets have provenance information or an explicit gap noted.
- Confirm obligations are named concretely rather than implied vaguely.
- Confirm ambiguity is surfaced as a review item rather than turned into a false pass.
