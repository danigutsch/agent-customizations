# Agent Customizations Plan

This file tracks work specific to the `agent-customizations` repository.

## Scope

- canonical reusable asset library under `.agents/`
- export and compatibility model
- shared repo quality and maintenance work
- repo-specific documentation and governance gaps

## Current state

- Shared customizations repository created: `agent-customizations`
- `.agents/` established as the canonical source of truth
- Compatibility exports treated as generated output via sync scripts
- Baseline maintenance in place:
  - local task entrypoints
  - CI validation workflow
  - CODEOWNERS
  - export smoke tests
  - slice inventory and compatibility docs
- Hotspot audit complete
- First two upstream `dotnet-skills` review batches complete and classified in
  `tmp/customization-inventory.md`
- Permanent docs record the special status of Aspire-generated and Spec Kit-generated files
- `scripts/check_tool_file_versions.py` and `scripts/tool_file_baselines.json` provide a read-only
  provenance and baseline checker for downstream tool-generated files

## Completed slices

Implemented in the canonical repo and synced downstream:

1. `microsoft-extensions-configuration`
2. `microsoft-extensions-dependency-injection`
3. `csharp-concurrency-patterns`
4. `csharp-type-design-performance`
5. `database-performance`
6. `dotnet-performance-analyst`
7. `dotnet-benchmark-designer`
8. `docfx-specialist`
9. `copilot-compatibility-exports`

## Execution rules for slices

- Inspect upstream shape first and preserve provenance.
- Review all slice surfaces explicitly: agents, instructions, prompts, skills, hooks, MCP,
  workflows, and plugins.
- Add only the surfaces that the capability genuinely needs.
- Update durable docs only when the slice changes repo-wide guidance or inventory expectations.
- After each slice implementation, sync the workspace export to `../ViajantesTurismo`.
- After each slice implementation, sync the user-level export.
- Compare canonical `.agents/` content with the corresponding files in `../ViajantesTurismo`.
- If `../ViajantesTurismo` differs in a way that is not following best practices, call that out
  explicitly.
- If the difference is only opinion or style, prefer the `../ViajantesTurismo` version and align to
  it rather than forcing a local preference.
- After each slice implementation and sync, force-stage that slice in git because canonical
  `.agents/` paths are gitignored and do not appear normally in the working tree view.

## Repo-specific active backlog

### Immediate next slice

1. `plugin-bundles`

### Canonical repo slices

1. `plugin-bundles`
2. `tool-generated-file-provenance`
3. `docs-and-scripts-quality`

### Quality and maintenance backlog

- Normalize agent frontmatter
- Normalize instruction frontmatter
- Normalize prompt frontmatter
- Normalize skill frontmatter
- Ensure naming is consistent and predictable
- Ensure descriptions explain what files do and when to use them
- Ensure tools are least-privilege where appropriate
- Ensure cross-links are correct
- Ensure markdown is lint-friendly
- Ensure imported files document source provenance
- Merge or deprecate overlapping assets that remain after the recorded hotspot decisions
- Add curated `awesome-copilot` imports only for gaps that survive overlap review
- Add reference docs and examples for imported assets where they materially help adoption
- Add a script to inventory all customizations
- Add a script to validate frontmatter
- Add a script to detect duplicate names
- Add a script to flag likely overlap by name or category
- Add a lightweight review cadence
- Add deprecation policy docs
- Add upstream provenance docs
- Refresh indexes and docs after the next slice wave lands

## Repo-specific issues to fix soon

- Add a clear root `LICENSE` for `agent-customizations` if it is still missing.

## Notes

- `.agents/` remains the canonical source of truth for curated reusable assets.
- Generated Aspire and Spec Kit outputs remain excluded from curated slice inventory here.
- `tmp/customization-inventory.md` stays the detailed evidence base, but not the active roadmap.
