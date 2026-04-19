---
description: 'Guidance for plugin bundle manifests, distributed file contracts, changelogs, examples, and validator-backed packaging rules.'
applyTo: 'README.md, docs/plugin-maintenance.md, .agents/plugins/**/*.json, .agents/plugins/**/*.md, templates/plugin-bundle/**, scripts/validate_plugin_bundles.py, .agents/agents/plugin-bundles.agent.md, .agents/skills/plugin-bundles/**, .agents/instructions/plugin-bundles.instructions.md'
---

# Plugin Bundles Guidance

Use these rules when the task is about versioned plugin bundles under `.agents/plugins/`.

## Core model

- Treat plugin bundles as lightweight packaging contracts, not as the canonical source of capability
  content.
- Keep the manifest and distributed file list explicit and machine-checkable.
- Keep bundle-local docs, examples, and changelog aligned with the manifest.
- Use validator-backed checks instead of manual review alone for bundle-shape correctness.

## Bundle contract rules

- Keep the plugin id, directory name, and manifest metadata aligned.
- Keep `contents`, `documentation`, `examples`, and `changelog` explicit in the manifest.
- Do not leave bundle-local files unreferenced when they are part of the maintained bundle surface.
- Keep paths repository-relative and inside the repository root.

## Versioning and changelog rules

- Use semantic versioning for bundle versions.
- Keep an `Unreleased` section at the top of each plugin changelog.
- Keep a versioned changelog section for the current manifest version.
- Do not change a released bundle contract in place without a new version.

## Validation rules

- Prefer the repository validator as the authority for manifest-shape and path-existence checks.
- Keep the JSON schema, validator, templates, and docs aligned when the contract evolves.
- Validate directory-name matching, required fields, content kinds, and referenced file existence.
- Validate that plugin-local docs and examples are referenced explicitly rather than left orphaned.

## Packaging boundary rules

- Keep `.agents/` as the source of truth for the actual capability files a bundle distributes.
- Use the plugin directory only for packaging metadata, bundle-local docs, changelog, and examples.
- Keep plugin-bundle guidance separate from compatibility exports and provenance tracking even when
  they pair closely.

## Verification

- Confirm the manifest matches the current schema and validator expectations.
- Confirm every referenced path exists and belongs to the intended bundle contract.
- Confirm changelog structure includes `Unreleased` and the current version section.
- Confirm plugin-local docs and examples are referenced explicitly from the manifest.
