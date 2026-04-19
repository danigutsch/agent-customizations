---
name: plugin-bundles
description: Maintenance guidance for plugin bundle manifests, distributed file contracts, changelogs, examples, and validator-backed packaging rules. Use when creating or updating `.agents/plugins/*` bundles, changing plugin metadata, or debugging bundle validation failures.
---

# Plugin Bundles

Use this skill when the task is about how a capability is packaged and distributed as a plugin bundle
rather than how the canonical capability content itself is authored.

## When to Use This Skill

- The user is creating or changing a plugin bundle manifest
- The user needs to update a plugin bundle changelog or examples
- The user is debugging plugin bundle validation failures
- The user wants to understand what a plugin bundle should list explicitly
- The user wants export or packaging boundaries to follow a bundle contract

## Prerequisites

- The relevant bundle folder or manifest can be inspected.
- The canonical assets being packaged are known.
- The repository validator is available.

## Workflow

### 1. Inspect the packaging contract

- Read the manifest, changelog, and plugin-local docs or examples together.
- Treat them as one maintenance surface.

### 2. Confirm the distributed boundary

- Keep the bundle id, directory name, and distributed file list aligned.
- Be explicit about what the bundle ships.

### 3. Update release metadata deliberately

- Use semantic versioning for the bundle.
- Update the changelog when the packaging contract changes.

### 4. Validate before treating the bundle as ready

- Run the repository plugin validator.
- Fix missing paths, orphaned docs, or schema drift before release work continues.

## Related guidance

- Pair with [Copilot compatibility exports](../copilot-compatibility-exports/SKILL.md) when a bundle
  should drive export selection.
- Pair with [Repository setup](../repository-setup/SKILL.md) when a repo needs a clearer packaging
  and maintenance model.

## Gotchas

- **Do not treat plugin metadata as the source of truth.**
- **Do not version-bump without changelog updates.**
- **Do not leave docs or examples unreferenced.**
- **Do not skip validator-backed checks** when changing the bundle contract.

## References

- [Plugin bundle maintenance](../../../docs/plugin-maintenance.md)
- [Plugin bundle guidance](../../instructions/plugin-bundles.instructions.md)
- [Plugin bundles agent](../../agents/plugin-bundles.agent.md)
