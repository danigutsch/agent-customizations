---
description: 'Guidance for plugin bundle manifests, changelogs, examples, schema alignment, and validator-backed maintenance.'
applyTo: '.agents/plugins/**/*.json, docs/plugin-maintenance.md, templates/plugin-bundle/**, scripts/validate_plugin_bundles.py, .agents/agents/plugin-bundles.agent.md, .agents/skills/plugin-bundles/**'
---

# Plugin Bundle Guidance

Use these rules when the task is about plugin bundle metadata, validation, docs, examples, or
release-readiness.

## Core model

- Treat plugin bundles as a distribution layer over canonical `.agents/` assets, not as a parallel
  source of truth.
- Treat the manifest as the explicit packaging contract for the bundle.
- Keep the validator, schema, and documented expectations aligned.

## Manifest and contract rules

- Keep the bundle id aligned with the directory name.
- Keep the manifest version and schema version explicit and well-formed.
- Keep `contents`, `documentation`, `examples`, and `changelog` paths valid and repository-relative.
- Do not leave distributed files implied by convention if the bundle contract expects them explicitly.

## Versioning and changelog

- Use semantic versioning for bundle versions.
- Keep `Unreleased` at the top of plugin changelogs.
- Update the changelog when a bundle version or packaging contract changes.
- Describe notable bundle changes clearly rather than mirroring raw commit text.

## Examples and docs

- Keep plugin-local docs and examples explicitly referenced from the bundle contract.
- Do not leave plugin content orphaned in the bundle folder.
- Keep examples focused on how the bundle is adopted or used.

## Validation

- Use the repository's existing plugin bundle validator for manifest checks.
- Keep schema and validator behavior in sync when the contract evolves.
- Confirm that all referenced files exist before treating a bundle change as complete.

## Verification

- Confirm the manifest parses and matches the documented contract.
- Confirm the bundle directory, manifest id, and referenced files stay aligned.
- Confirm changelog and version changes move together.
- Confirm plugin docs and examples remain part of the bundle contract rather than stray files.
