# agent-customizations

Reusable AI agent customization assets.

This repository is intended to hold shared, tool-agnostic customization content under a single
`.agents/` root.

It includes reusable assets such as:

- agents
- instructions
- prompts
- skills
- hooks and hook examples
- MCP-related assets, manifests, wrappers, and setup docs
- workflow packs
- plugin-related assets
- supporting documentation
- lightweight maintenance scripts

## Structure

```text
agent-customizations/
  .github/
    workflows/
    copilot-instructions.md
  .githooks/
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

## Quality baseline

This repository keeps a small cross-file-type quality baseline:

- **Python**: Ruff is the default linter and formatter baseline for `scripts/`, with Pyright settings
  defined alongside it in `pyproject.toml`.
- **Markdown**: `.markdownlint.json` keeps markdownlint aligned with the repository's authoring rules.
- **JSON and YAML**: `.editorconfig` sets UTF-8, LF endings, final newlines, and 2-space indentation.
- **Text and binary files**: `.gitattributes` normalizes line endings and marks common binary asset
  types as non-text.

When Ruff is available locally, the expected Python workflow is:

```bash
ruff check scripts
ruff format scripts
```

The lightweight repository validation command is:

```bash
python3 scripts/validate_repo_files.py
```

## Local maintenance workflow

Use the `Makefile` as the main local entrypoint for routine repository work.

Install the local Python tools once:

```bash
make install-dev
```

Run the full repository baseline locally:

```bash
make check
```

Format the maintained Python scripts:

```bash
make format
```

Helpful maintenance commands:

- `make validate-repo`
- `make validate-plugins`
- `make sync-user`
- `make sync-workspace`
- `make configure-global-ignore`

To enable the lightweight pre-commit hook for this repository:

```bash
make install-hooks
```

The hook runs focused staged-file checks only. CI remains the authoritative full validation path.

## Repository purpose

Use this repository for customizations that are reusable across multiple projects.

Keep project-specific guidance in the target repository instead, especially:

- repository `AGENTS.md` files
- prompts tied to repo-specific workflows
- architecture or coding rules that only make sense inside one codebase

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

## Compatibility

`.agents/` is the source of truth in this repository, but GitHub Copilot does not natively use
`.agents/` as its primary discovery root.

### Copilot

For native Copilot discovery:

- workspace agents use `.github/agents/`
- workspace path-specific instructions use `.github/instructions/`
- workspace prompts use `.github/prompts/`
- workspace hooks use `.github/hooks/`
- user-level agents use `~/.copilot/agents/`
- user-level skills use `~/.copilot/skills/`
- user-level instructions and hooks are client-specific rather than universally portable
- prompts do not have a stable documented `~/.copilot` filesystem mirror
- `.agents/skills/` is already a native project skill location for Copilot-aware clients

This repository prefers **source-of-truth first, compatibility second**:

- maintain canonical assets under `.agents/`
- sync to Copilot-native locations when needed

For the current compatibility model and sync workflow, see
[docs/compatibility.md](./docs/compatibility.md).

## Slice completeness review

When adding or modifying a slice, review **every** slice surface before considering the work
complete:

1. `agents/`
2. `instructions/`
3. `prompts/`
4. `skills/`
5. `hooks/`
6. `mcp/`
7. `workflows/`
8. `plugins/`

Do not assume a slice needs every file type, but do make an explicit decision for each one.
For most reusable slices, `agents`, `instructions`, `skills`, and often `prompts` are the starting
set. Add hooks, MCP assets, workflows, or plugins only when they clearly add value.

## Initial direction

The first migration targets are the shared or generic assets currently living outside product
repositories, plus generic assets that should be removed from product repositories and centralized
here.
