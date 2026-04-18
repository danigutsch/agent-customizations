# Plugin bundles

Use plugin bundles when a grouped `.agents` slice has become a reusable, versioned capability pack.

## When to create a plugin bundle

Create a plugin bundle only when all of these are true:

1. The files form one clear capability bundle.
2. They are meant to be installed together.
3. They have shared docs, examples, or supporting assets.
4. You expect reuse across multiple repositories or users.
5. You want versioned distribution, not just file copying.

If a slice is still changing shape, keep it as grouped files only and wait before adding a plugin.

## Design rules

- Keep `.agents/` as the source of truth for reusable assets.
- Treat the plugin directory as packaging metadata and installation guidance.
- Package one capability per plugin.
- Keep manifests neutral and tool-agnostic.
- Prefer explicit file lists over implicit folder copying.
- Use semantic versioning for the bundle version.
- Add a focused README for install intent, scope, and compatibility notes.

## Why some slices are bundled and others are not

Bundle a slice when the capability is typically installed and versioned as one unit.

Bundle when:

- the slice is domain-specific and reused as a whole
- the surfaces are tightly coupled and expected to ship together
- examples, docs, and setup guidance are part of one capability pack

Leave slices unbundled when:

- they are meant for flexible composition with other slices
- repos are expected to mix and match them based on current tooling
- bundling would over-prescribe one opinionated setup

In this repository, `source-generation` and `vertical-slice-architecture` are bundled because they
behave like cohesive capability packs. Foundation slices such as `python-quality`, `ruff-python`,
`pyright-python`, `editorconfig`, `git-hooks`, and `ci-workflows` stay unbundled so adopters can
compose only the parts they need.

## Required bundle shape

Each plugin bundle should use this structure:

```text
.agents/plugins/<plugin-id>/
  plugin.json
  README.md
  examples/
```

Optional supporting assets can live under:

```text
.agents/plugins/<plugin-id>/assets/
```

## Required manifest fields

- `schemaVersion`
- `id`
- `version`
- `displayName`
- `description`
- `bundleType`
- `install`
- `contents`
- `documentation`
- `examples`

Use [plugin-bundle.schema.json](./plugin-bundle.schema.json) as the contract for new manifests.

## Versioning rules

- Use semantic versioning for `version`.
- Bump the major version for breaking packaging or compatibility changes.
- Bump the minor version for new files, examples, or capabilities added compatibly.
- Bump the patch version for metadata corrections or non-breaking documentation updates.

Treat the plugin manifest and distributed file set as the bundle's public packaging contract. Once a
bundle version is released, do not silently change the contents of that version. Publish a new
version instead.

## Packaging guidance

- `contents` should list every distributed file explicitly.
- `documentation` should point to both the slice entry points and any bundle-specific README.
- `examples` should point to small, stable examples that help adopters understand installation or
  usage shape.
- `dependencies` should be explicit and minimal.
- `compatibility` should describe assumptions about layout roots or host expectations without tying
  the manifest to one client.

## Maintenance rules

- Validate every plugin manifest against the repository contract before merging changes.
- Detect drift between `plugin.json` and the real files on disk:
  referenced files must exist, plugin directory names must match plugin ids, and bundle examples and
  documentation should stay explicitly listed.
- Update the plugin version and changelog together whenever distributed behavior changes.
- Keep an `Unreleased` section in each plugin changelog, then move those notes into a versioned
  section at release time.
- Prefer one changelog per plugin once plugin versions can move independently.
- Make validation cheap enough to run locally and in CI.

## Automation

Run the repository validator locally or in CI:

```bash
python3 scripts/validate_plugin_bundles.py
```

The validator checks manifest shape, required paths, changelog presence, and basic drift between a
plugin's metadata and its files.

For detailed maintenance guidance, see [docs/plugin-maintenance.md](../../docs/plugin-maintenance.md).
