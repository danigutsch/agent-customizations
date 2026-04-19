---
name: tool-generated-file-provenance
description: Guidance for inspecting tool-generated files, bundled baselines, provenance markers, and conservative drift classification. Use when checking whether downstream Copilot-facing files are curated or generator-owned, when updating baseline manifests, or when troubleshooting provenance reports.
---

# Tool-Generated File Provenance

Use this skill when the task is about determining whether a downstream file is generator-owned,
curated, or drifting away from a known generated baseline.

## When to Use This Skill

- The user wants to inspect Aspire- or Spec Kit-style generated files
- The user needs to update or interpret bundled baseline manifests
- The user wants to know whether a Copilot-facing file should be treated as curated or generated
- The user is debugging drift or provenance output from the checker
- The user needs ownership-boundary guidance for downstream generated files

## Prerequisites

- The candidate file or repo can be inspected.
- The provenance checker or baseline manifest is available.
- The ownership question is clear enough to classify conservatively.

## Workflow

### 1. Identify the candidate ownership model

- Decide whether the file is likely curated, generated, or ambiguous.
- Do not collapse those cases together.

### 2. Gather provenance evidence

- Inspect markers, baseline matches, version signals, filenames, and git state together.
- Treat missing evidence as meaningful uncertainty.

### 3. Classify drift conservatively

- Distinguish current, historical, modified, and unknown states.
- Avoid stronger language than the evidence supports.

### 4. Recommend the correct refresh path

- Prefer rerunning the owning generator when the file is tool-generated.
- Use documentation updates or baseline updates only when the underlying ownership model is clear.

## Related guidance

- Pair with [Copilot compatibility exports](../copilot-compatibility-exports/SKILL.md) when generated
  files appear in compatibility mirror locations.
- Pair with [Repository setup](../repository-setup/SKILL.md) when a repo needs clearer policy on
  curated versus generator-owned assets.

## Gotchas

- **Do not assume generated files are curated assets**.
- **Do not overstate provenance confidence**.
- **Do not prefer manual edits over rerunning the owning generator**.
- **Do not treat unknown as outdated**.

## References

- [Compatibility documentation](../../../docs/compatibility.md)
- [Tool-generated file provenance guidance](../../instructions/tool-generated-file-provenance.instructions.md)
- [Tool-generated file provenance agent](../../agents/tool-generated-file-provenance.agent.md)
