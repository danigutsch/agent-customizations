# agent-customizations

Reusable AI agent customization assets.

This repository is intended to hold shared, tool-agnostic customization content under a single
`.agents/` root.

It includes reusable assets such as:

- agents
- instructions
- prompts
- skills
- hooks
- MCP-related assets
- workflow packs
- plugin-related assets
- supporting documentation
- lightweight maintenance scripts

## Structure

```text
agent-customizations/
  .agents/
    agents/
    instructions/
    prompts/
    skills/
    hooks/
    mcp/
    workflows/
    plugins/
  docs/
  examples/
  scripts/
  templates/
```

## Repository purpose

Use this repository for customizations that are reusable across multiple projects.

Keep project-specific guidance in the target repository instead, especially:

- repository `AGENTS.md` files
- prompts tied to repo-specific workflows
- architecture or coding rules that only make sense inside one codebase

## Notes on hooks and MCP

- **Hooks** are good candidates for this repository as reusable assets, templates, and examples.
- **MCP** is also a good fit here for reusable server code, manifests, setup docs, and tool
  examples.
- Live MCP registration in a client such as Copilot CLI is still a runtime concern, but the
  reusable MCP assets absolutely belong in a shared repository like this one.

## Plugin bundles

Use `.agents/plugins/` for **versioned capability bundles** when a grouped slice has matured past
simple file curation.

A grouped slice is a good plugin candidate when:

1. the files form one clear capability bundle
2. they are meant to be installed together
3. they have shared docs, examples, or other supporting assets
4. reuse across multiple repositories or users is expected
5. versioned distribution matters more than ad hoc file copying

Plugins in this repository are **packaging metadata over existing `.agents` slices**, not a second
source of truth. The slice files still live under `.agents/agents/`, `.agents/instructions/`,
`.agents/skills/`, and related folders. The plugin directory declares how those files travel
together as one reusable pack.

## Layout rule

Use `.agents/` as the canonical home for customization assets in this repository.

- Put reusable agent definitions in `.agents/agents/`
- Put reusable instructions in `.agents/instructions/`
- Put reusable prompt files in `.agents/prompts/`
- Put reusable skills in `.agents/skills/`
- Put reusable hooks in `.agents/hooks/`
- Put reusable MCP assets in `.agents/mcp/`
- Put reusable workflow packs in `.agents/workflows/`
- Put reusable plugin-oriented assets and bundle manifests in `.agents/plugins/`

## Initial direction

The first migration targets are the shared or generic assets currently living outside product
repositories, plus generic assets that should be removed from product repositories and centralized
here.
