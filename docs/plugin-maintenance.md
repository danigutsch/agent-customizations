# Plugin bundle maintenance

Plugin bundles should be maintained like lightweight packages, not like loose folders.

## Core maintenance principles

- Treat the manifest and distributed file list as the plugin's public packaging contract.
- Use JSON Schema to make the contract explicit and machine-checkable.
- Use Semantic Versioning for bundle versions.
- Keep a human-readable changelog for each independently versioned plugin.
- Make validation cheap enough to run locally and in CI.

## What should be validated automatically

At minimum, validate these on every change:

1. The manifest parses and matches the repository contract.
2. Required manifest fields are present and well-formed.
3. The plugin directory name matches the plugin id.
4. Every path listed in `contents`, `documentation`, `examples`, and `changelog` exists.
5. Bundle-specific docs and examples are explicitly referenced, not left orphaned in the plugin
   folder.
6. The changelog contains an `Unreleased` section and the current manifest version.

These checks prevent the most common maintenance failures:

- broken installation metadata
- renamed files not reflected in the manifest
- examples or docs that silently drift out of the bundle contract
- version bumps without release notes

## Versioning guidance

Use Semantic Versioning for each plugin bundle:

- **Major** for breaking compatibility or packaging contract changes
- **Minor** for backward-compatible additions
- **Patch** for backward-compatible fixes and metadata corrections

If a bundle version has been released, do not change its contents in place. Publish a new version
instead.

## Changelog guidance

Keep one changelog per plugin once bundles can evolve independently.

- Keep `Unreleased` at the top.
- Group changes under categories such as `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and
  `Security`.
- Move `Unreleased` notes into a versioned section when you cut a release.
- Keep changelog entries human-readable and focused on notable bundle changes, not raw commit logs.

## Recommended workflow

1. Update the capability files under `.agents/`.
2. Update the plugin manifest if the distributed contract changed.
3. Update the plugin changelog.
4. Run `python3 scripts/validate_plugin_bundles.py`.
5. Run the diff-aware version guard against your base branch.
6. Only then cut or tag the new bundle version.

The repository-local helper keeps the manifest version and changelog promotion aligned:

```bash
make release-plugin PLUGIN=source-generation BUMP=patch
```

It bumps the plugin manifest version, promotes the current `Unreleased` changelog notes into a dated
release section, and prints the git tag name to use for that bundle release.

Before you cut a release, verify that any shipped plugin-surface change is paired with the expected
version bump:

```bash
make check-plugin-version-bumps BASE_REF=origin/main HEAD_REF=HEAD
```

The guard follows the established dependency-free versioning model for this repository:

- Semantic Versioning for the bundle version
- Keep a Changelog with an `Unreleased` section for upcoming notes
- git tags for released bundle versions

## Automation options

The repository includes a lightweight validator script:

```bash
python3 scripts/validate_plugin_bundles.py
```

Use it in any automation layer you already trust:

- pre-commit or pre-push hooks
- CI jobs
- reusable workflow wrappers
- release pipelines

The repository also includes a manual GitHub Actions workflow, `Release plugin bundle`, that reuses
the same script for CI-driven commit and tag creation.

If you later use GitHub Actions, reusable workflows are a reasonable way to centralize this check
across repositories, but the validator itself stays tool-neutral and can run anywhere Python 3 is
available.

## References

- Semantic Versioning: <https://semver.org/>
- Keep a Changelog: <https://keepachangelog.com/en/1.1.0/>
- JSON Schema: <https://json-schema.org/>
- GitHub Actions reusable workflows:
  <https://docs.github.com/en/actions/using-workflows/reusing-workflows>
