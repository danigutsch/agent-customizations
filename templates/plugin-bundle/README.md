# Plugin bundle template

Use this template when a grouped slice has become a versioned capability bundle.

## Checklist

- Confirm the files form one clear capability bundle.
- Confirm they are intended to be installed together.
- Confirm the bundle has shared docs, examples, or supporting assets.
- Confirm reuse across repositories or users is expected.
- Confirm versioned distribution is more useful than file-by-file copying.

## Required files

- `plugin.json`
- `README.md`
- `CHANGELOG.md`
- `examples/`

## Notes

- Keep `.agents/` as the source of truth for the actual slice files.
- Use the plugin directory only for packaging metadata, bundle-specific docs, and examples.
- Keep file lists explicit in the manifest.
