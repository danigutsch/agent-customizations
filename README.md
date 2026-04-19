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

For this repository, the recommended packaging split is:

- use **`pipx`** for standalone developer tools such as `ruff` and `pyright`
- use **`pip`** only inside a project virtual environment when you are managing project-local Python
  dependencies

Install the local Python tools once:

```bash
make install-dev
```

On Debian/Ubuntu and other PEP 668 environments, install `pipx` first instead of using system `pip`
for user installs:

```bash
sudo apt-get install -y pipx
```

Then make sure `~/.local/bin` is on your `PATH`.

On Windows, install `pipx` with the Python launcher and add its bin directory to your `PATH`:

```powershell
py -m pip install --user pipx
py -m pipx ensurepath
```

If you want to use the `Makefile` on Windows, run it from an environment that provides GNU Make, such
as Git Bash, MSYS2, or WSL. Otherwise, run the underlying commands directly.

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
- `make smoke-exports`
- `make inspect-tool-files TARGET_ROOT=/path/to/repo`
- `make sync-user`
- `make sync-workspace`
- `make configure-global-ignore`
- `make setup-mcp MANIFEST=.agents/mcp/mcp-servers/my-server.json`

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

## MCP setup

The repository keeps reusable MCP manifests under `.agents/mcp/mcp-servers/` and always provides a
script-driven Copilot CLI setup path.

1. Copy an example manifest to a concrete `.json` file and replace placeholder values.
2. Run the setup script to merge the manifest into `~/.copilot/mcp-config.json`.

```bash
python3 scripts/setup_copilot_mcp.py --manifest .agents/mcp/mcp-servers/my-server.json
```

If you prefer the repository `Makefile` entrypoint:

```bash
make setup-mcp MANIFEST=.agents/mcp/mcp-servers/my-server.json
```

The setup script can also auto-discover all non-example manifests under `.agents/mcp/mcp-servers/`
when you omit `--manifest`.

## Plugin bundles

Use `.agents/plugins/` for **versioned capability bundles** when a grouped capability has matured past
simple file curation.

A grouped capability is a good plugin candidate when:

1. the files form one clear capability bundle
2. they are meant to be installed together
3. they have shared docs, examples, or other supporting assets
4. reuse across multiple repositories or users is expected
5. versioned distribution matters more than ad hoc file copying

Plugins in this repository are **packaging metadata over existing `.agents` capabilities**, not a second
source of truth. The capability files still live under `.agents/agents/`, `.agents/instructions/`,
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
- generate `.github/*` compatibility copies only through the sync scripts when needed
- treat generated `.github/*` compatibility copies as non-canonical output, not tracked repo content
- keep those generated `.github/*` copies ignored through global Git ignore policy rather than a
  repository `.gitignore` rule

Some downstream projects also contain **tool-provided agent assets** that are not part of this
repository's curated capability inventory. In particular, Aspire can install its own broad `aspire`
skill through `aspire agent init`, and Spec Kit can generate `speckit`-prefixed Copilot assets and
related context files through its integration setup. This repository's policy is to **not** add
those generated Aspire or Spec Kit files as curated assets here. At most, document the commands and
tooling needed to generate or refresh them in downstream repositories.

To inspect a downstream repository for these tool-provided files and report provenance,
bundled-baseline matches, version-signal, and drift information:

```bash
python3 scripts/check_tool_file_versions.py --repo /path/to/repo
python3 scripts/check_tool_file_versions.py --repo /path/to/repo --format json
```

The checker includes bundled upstream baselines for the current Aspire skill file and the current
Spec Kit Copilot outputs, including both `--script sh` and `--script ps` agent variants where the
generated content differs.

For the current compatibility model and sync workflow, see
[docs/compatibility.md](./docs/compatibility.md).

## Capability surface review

When adding or modifying a capability, review **every** capability surface before considering the work
complete:

1. `agents/`
2. `instructions/`
3. `prompts/`
4. `skills/`
5. `hooks/`
6. `mcp/`
7. `workflows/`
8. `plugins/`

Do not assume a capability needs every file type, but do make an explicit decision for each one.
For most reusable capabilities, `agents`, `instructions`, `skills`, and often `prompts` are the starting
set. Add hooks, MCP assets, workflows, or plugins only when they clearly add value.
When concrete repository wiring depends on a reusable capability, refine the relevant capability guidance
first and then implement the repository-specific wiring.

## Initial direction

The first migration targets are the shared or generic assets currently living outside product
repositories, plus generic assets that should be removed from product repositories and centralized
here.
