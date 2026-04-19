---
description: 'Guidance for inspecting tool-generated files, bundled baselines, provenance markers, and conservative drift reporting.'
applyTo: 'README.md, docs/compatibility.md, scripts/check_tool_file_versions.py, scripts/tool_file_baselines.json, .agents/agents/tool-generated-file-provenance.agent.md, .agents/skills/tool-generated-file-provenance/**'
---

# Tool-Generated File Provenance Guidance

Use these rules when the task is about generator-owned files, provenance inspection, baseline updates,
or drift reporting.

## Core model

- Keep curated repository assets separate from tool-generated downstream files.
- Treat provenance as evidence-based rather than assumption-based.
- Keep checker behavior, baseline data, and policy docs aligned.

## Classification rules

- Distinguish current baseline matches, historical matches, modified files, and unknown files.
- Use conservative language when the evidence is incomplete.
- Do not imply a file is curated just because it appears in a Copilot-facing location.

## Baseline handling

- Keep baseline manifests explicit about source, source path, and upstream reference.
- Update baselines deliberately when upstream generated output changes.
- Preserve historical variants when that helps explain expected drift without weakening current-match
  checks.

## Remediation rules

- Prefer rerunning the owning tool when a file is generator-owned.
- Do not recommend manual edits as the first remedy for tool-generated outputs.
- Make ownership boundaries explicit when a downstream repo mixes curated and generated files.

## Verification

- Confirm provenance docs match the actual checker behavior.
- Confirm baseline records still match known generator outputs.
- Confirm drift wording stays conservative and evidence-backed.
- Confirm remediation guidance names the owning tool or refresh flow when known.
