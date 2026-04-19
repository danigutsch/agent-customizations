---
name: foss-compatibility
description: Guidance for open-source compatibility review. Use when deciding whether licenses can coexist, when recording SPDX identifiers or provenance for imported assets, when checking attribution or NOTICE obligations, or when a compliance question needs explicit escalation instead of a simple scanner result.
---

# FOSS Compatibility

Use this skill when the task is about whether open-source assets can be adopted or redistributed
safely and what obligations follow from that decision.

## When to Use This Skill

- The user wants to know whether an imported asset or dependency is compatible with the repo's
  licensing and distribution model
- The user needs guidance on attribution, NOTICE, or other redistribution obligations
- The user is recording provenance for imported files, templates, or vendored content
- The user needs SPDX-oriented license naming or metadata guidance
- The user needs to know when a compliance issue should be escalated instead of handled as routine
  automation

## Prerequisites

- The candidate asset, dependency, or import source can be inspected.
- Some license evidence exists, or the gap is explicitly identified.
- The adoption path is known or can be inferred well enough to distinguish use from redistribution.

## Workflow

### 1. Gather the facts

- Identify the component, file family, or imported content under review.
- Record the available license evidence and provenance evidence separately.

### 2. Determine the adoption context

- Distinguish between referencing, copying, vendoring, packaging, and redistributing.
- Treat downstream generated output as part of the context when it materially affects obligations.

### 3. Name the obligations

- Record license-text, attribution, NOTICE, or source-availability obligations explicitly.
- Use SPDX identifiers when the task involves machine-readable license metadata.

### 4. Decide whether the issue is routine or escalated

- Keep straightforward cases concise.
- Escalate ambiguous, reciprocal, mixed-license, or weak-provenance cases instead of flattening them
  into a normal import path.

## Related guidance

- Pair with [Tool-Generated File Provenance](../tool-generated-file-provenance/SKILL.md) when the
  ownership and upstream origin of files are part of the compliance question.
- Pair with [Repository Setup](../repository-setup/SKILL.md) when durable repository policy or
  contributor guidance needs to be added.

## Gotchas

- **Do not treat scanner output as the whole compliance story.**
- **Do not ignore provenance gaps.**
- **Do not assume one repository license covers imported third-party content.**
- **Do not hide uncertainty when escalation is the safer answer.**

## References

- [FOSS compatibility guidance](../../instructions/foss-compatibility.instructions.md)
- [FOSS compatibility agent](../../agents/foss-compatibility.agent.md)
