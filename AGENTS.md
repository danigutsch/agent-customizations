# AGENTS.md

Repository guidance for `agent-customizations`.

## Scope

- Applies to the whole repository.
- Prefer generic, reusable guidance over tool-vendor-specific assumptions.

## Content rules

- Keep assets reusable across repositories unless a file is explicitly placed in an example or
  product-specific area.
- Prefer neutral naming that does not assume a single AI platform.
- Before creating a new slice, inspect relevant patterns in upstream sources already used by this
  repository, especially `github/awesome-copilot` and `Aaronontheweb/dotnet-skills`.
- Prefer adapting an existing upstream slice shape and name when one already fits the capability.
  For example, if an upstream repo already uses `editorconfig`, prefer that over inventing a new
  local variant.
- If no upstream pattern fits cleanly, document that gap and keep the new slice name as close as
  possible to established naming conventions instead of creating a highly repo-specific label.
- Keep one clear purpose per file and avoid near-duplicate variants with different names.
- Document provenance when adapting or importing content from upstream sources.
- When an asset supersedes another one, record that in docs instead of leaving silent overlap.

## Structure rules

- `.agents/` is the canonical root for reusable customization assets in this repository.
- `.agents/agents/` contains reusable custom agent definitions.
- `.agents/instructions/` contains reusable instruction files.
- `.agents/prompts/` contains reusable prompt files or prompt packs.
- `.agents/skills/` contains reusable skills and their references or assets.
- `.agents/hooks/` contains reusable hook configurations, scripts, and examples.
- `.agents/mcp/` contains reusable MCP server assets, manifests, wrappers, and setup guidance.
- `.agents/workflows/` contains reusable workflow packs or agentic workflow assets.
- `.agents/plugins/` contains plugin-oriented assets or packaging metadata when relevant.
  Treat plugin bundles as a distribution layer over existing slices, not as a parallel source of
  truth.
- `docs/` contains inventory, taxonomy, migration, and maintenance documentation.
- `examples/` contains product-specific or tool-specific adaptation examples.
- `scripts/` contains lightweight maintenance and validation helpers.
- `templates/` contains starter templates for new assets.

## Quality rules

- Prefer concise frontmatter descriptions that explain both what an asset does and when to use it.
- Keep cross-links relative and repository-local.
- Avoid adding assets that duplicate an existing capability unless there is a clear specialization.
- Favor curation over volume: only keep assets worth maintaining.
- For new slices, do not create from scratch if an upstream pattern already covers the same
  capability. Reuse the upstream capability boundary, naming style, and file shape first, then adapt
  only what this repository truly needs.
- For plugin bundles, keep a small manifest plus a focused README.
- A plugin should package one clear capability bundle and explicitly list the files it distributes.
- When adding or modifying a slice, review `agents`, `instructions`, `prompts`, `skills`, `hooks`,
  `mcp`, `workflows`, and `plugins` explicitly, even if the final decision is that some surfaces are
  not needed.
- Prefer deliberate omission over accidental omission: if a slice lacks prompts, hooks, MCP assets,
  workflows, or plugin packaging, that should be because the capability does not need them yet.
