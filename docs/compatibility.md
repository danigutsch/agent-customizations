# Compatibility

This repository uses `.agents/` as the canonical source of truth for reusable customization assets.

GitHub Copilot does **not** treat `.agents/` as a native universal discovery root, so compatibility
depends on syncing or exporting selected assets into Copilot-supported locations.

## Copilot

### Supported compatibility targets

#### Scope matters as much as path

Some surfaces work well from user-level directories, some are primarily workspace-level, and some
have client-specific behavior. The export story is therefore a **scope and format mapping**, not
just a path mapping.

#### Compatibility matrix

| Surface | Canonical source here | Broad workspace target | User-level target | Format notes |
| --- | --- | --- | --- | --- |
| Agents | `.agents/agents/*.agent.md` | `.github/agents/` | `~/.copilot/agents/` | Same Markdown format |
| Path-specific instructions | `.agents/instructions/**/*.instructions.md` | `.github/instructions/` | `~/.copilot/instructions/` in VS Code | Same Markdown format |
| Repo-wide instructions | not generated from capability files | `.github/copilot-instructions.md` | `$HOME/.copilot/copilot-instructions.md` in CLI | Separate always-on file type |
| Prompts | `.agents/prompts/*.prompt.md` | `.github/prompts/` | VS Code profile storage, not a stable `~/.copilot` path | Same Markdown format, workspace export only |
| Skills | `.agents/skills/<skill>/SKILL.md` | `.github/skills/` if needed | `~/.copilot/skills/` | `.agents/skills/` is already a native project skill location |
| Hooks | `.agents/hooks/` hook-pack directories | `.github/hooks/` | `~/.copilot/hooks/` in VS Code | Hook packs can include JSON, shell, Markdown, or small helper assets |
| MCP assets | `.agents/mcp/` | client-specific config | client-specific config | Not a file mirror |
| Workflows | `.agents/workflows/` | no documented native root | no documented native root | Not a Copilot file surface |
| Plugins | `.agents/plugins/` | plugin packaging, not direct discovery | plugin packaging, not direct discovery | Metadata layer, not native discovery |

The main repo-level exports that matter for Copilot compatibility are:

```text
.github/agents/
.github/instructions/
.github/prompts/
.github/hooks/
```

Skills are the main exception because Copilot already recognizes project skills in:

```text
.agents/skills/
```

### Export strategy

The repository now supports two export modes:

1. **User scope**
   - target root: `~/.copilot/`
   - best for: personal agents, personal skills, and VS Code-specific user instructions/hooks
   - warning: the canonical tracked source remains under `.agents/`; these user-level files live
     outside the repository and are normally not Git-tracked
2. **Workspace scope**
     - target root: a repository root
     - best for: `.github/` exports needed by workspace-only features such as prompts or explicit
       project-level override scenarios
     - default behavior: keep user-level `~/.copilot/*` as the active runtime for overlapping
       surfaces and skip surfaces that the target repository already exposes natively from `.agents/`

The generic export script is:

```bash
python3 scripts/sync_copilot_exports.py
```

When a plugin bundle exists, prefer exporting by plugin so the synced files stay aligned the same
way the bundle was packaged:

```bash
python3 scripts/sync_copilot_exports.py --scope workspace --runtime-authority workspace --target-root /path/to/repo --plugin source-generation
python3 scripts/sync_copilot_exports.py --scope user --plugin vertical-slice-architecture
python3 scripts/sync_copilot_exports.py --scope workspace --runtime-authority workspace --target-root /path/to/repo
```

Use `--surface ...` as the lower-level fallback when no plugin bundle exists yet.

For workspace syncs, the generic exporter defaults to **user-level runtime authority**. Plain
workspace syncs therefore avoid mirroring overlapping runtime surfaces such as agents,
instructions, skills, and hooks into `.github/*` unless you explicitly choose workspace authority
or request specific surfaces.

It also skips native project surfaces that the target repository already exposes from `.agents/`.
Today that mainly means:

- skip `.github/skills/` when the target repository already has `.agents/skills/`
- still allow `.github/agents/` and related workspace exports when you explicitly choose
  `--runtime-authority workspace` or request the relevant surfaces

Narrower compatibility helpers remain available:

- `python3 scripts/sync_copilot_user_level.py`
- `python3 scripts/sync_copilot_agents.py`

### What is not auto-generated

The repository does **not** auto-generate these compatibility targets:

- `.github/copilot-instructions.md`
- MCP assets
- workflows
- plugins

Why:

- Repo-wide instructions are a different surface than capability-scoped `.instructions.md` files.
- Prompt files are user-profile assets in VS Code, but not through a stable documented
  `~/.copilot/prompts/` filesystem location.
- MCP, workflows, and plugins are configuration-driven or packaging-oriented rather than simple file
  mirrors.
- Forcing unofficial user-level layouts would make the repository less portable and more brittle.

### Sync workflow

Run the generic export script for user-level sync:

```bash
python3 scripts/sync_copilot_exports.py --scope user
```

The script warns before writing user-level files because the canonical tracked source remains under
`.agents/`, while `~/.copilot/*` is normally outside the repository and not Git-tracked.
If you point user scope at a custom target inside a Git repository, it also checks whether the
destination export paths are already Git-tracked there.

Run the generic export script for workspace sync:

```bash
python3 scripts/sync_copilot_exports.py --scope workspace --target-root /path/to/repo
```

This keeps user-level `~/.copilot/*` as the default active runtime and exports only non-overlapping
workspace surfaces by default.
The exporter also checks whether the destination `.github/*` paths are already Git-tracked in the
target repository and reports that before writing.

When a repository needs repo-level overrides or a pinned local runtime layer, opt into workspace
authority:

```bash
python3 scripts/sync_copilot_exports.py --scope workspace --runtime-authority workspace --target-root /path/to/repo
```

Examples:

```bash
python3 scripts/sync_copilot_exports.py --scope user --dry-run
python3 scripts/sync_copilot_exports.py --scope workspace --target-root ../some-repo --dry-run
python3 scripts/sync_copilot_exports.py --scope workspace --runtime-authority workspace --target-root ../some-repo --dry-run
python3 scripts/sync_copilot_exports.py --scope workspace --target-root ../some-repo --surface prompts
python3 scripts/sync_copilot_exports.py --scope workspace --target-root ../some-repo --surface skills
python3 scripts/sync_copilot_exports.py --scope workspace --target-root ../some-repo --plugin source-generation
python3 scripts/sync_copilot_exports.py --scope workspace --target-root ../some-repo --write-git-exclude
```

For agents only:

```bash
python3 scripts/sync_copilot_agents.py
```

### Source-of-truth rule

When an exported file exists in both places:

- edit the canonical version under `.agents/`
- rerun the export script
- do not hand-edit generated copies under `~/.copilot/` or `.github/`
- treat `.github/*` compatibility copies as generated output, not as a second maintained source

### Tool-provided special cases

Some ecosystems install or generate agent-facing files in the same broad locations that this
repository uses for curated reusable assets. Those files should be treated as **tool-provided project
context**, not automatically as canonical capabilities from this repository.

#### Aspire

- Aspire's official agent setup flow is `aspire agent init`.
- Aspire documents that this command installs an Aspire skill file at
  `.github/skills/aspire/SKILL.md`.
- Aspire also documents that this skill file replaces older `AGENTS.md` guidance in Aspire-created
  projects.

Implication for this repository:

- a downstream repo's broad `aspire` skill may be **setup-provided baseline context**
- do **not** add Aspire-generated skill files to this repository as curated assets
- keep only reusable commands, guidance, and tooling that help downstream repositories run
  `aspire agent init` or refresh those files
- narrower Aspire-focused capabilities should only be added here when they are independently curated
  reusable assets, not copies of setup-generated files

References:

- <https://aspire.dev/get-started/ai-coding-agents/>
- <https://aspire.dev/reference/cli/commands/aspire-agent-init/>

#### Spec Kit

- Spec Kit's `Specify CLI` bootstraps projects with templates, directory structure, and AI agent
  integrations.
- The official `spec-kit` agent guide documents that integrations are generated from
  `src/specify_cli/integrations/<key>/`.
- Its Copilot integration is explicitly a custom setup that creates `speckit.*.agent.md` command
  files, companion `.prompt.md` files, and `.vscode/settings.json`, with
  `.github/copilot-instructions.md` used as the Copilot context file.

Implication for this repository:

- `speckit`-prefixed files in downstream repos are usually **tool-generated Spec Kit workflow
  assets**, not curated reusable capabilities from this repository
- do **not** add those generated Spec Kit files to this repository as curated assets
- keep only reusable commands, guidance, and tooling that help downstream repositories generate or
  refresh them
- do not mistake Spec Kit's generated agent scaffolding for this repository's canonical `.agents/`
  inventory

References:

- <https://github.com/github/spec-kit/blob/main/AGENTS.md>

### Ignore strategy for generated workspace exports

In this repository, workspace exports under `.github/*` are treated as generated compatibility files
rather than tracked repo content. The preferred default is:

- use a global ignore so the policy stays consistent across repositories that generate the same
  Copilot compatibility paths
- do not add repository `.gitignore` rules just to hide generated `.github/*` compatibility output

The main caveat is not compatibility with Git or Copilot, but that ignore rules do **not** affect
files that are already tracked.

Example:

```bash
git config --global core.excludesFile ~/.config/git/ignore
```

The repository includes a helper script that:

- ensures `core.excludesFile` is set if missing
- writes a managed block into the global ignore file
- warns if a selected repository already tracks files in the ignored export paths

Example:

```bash
python3 scripts/configure_global_copilot_gitignore.py --repo ../ViajantesTurismo
```

By default this manages the common hidden customization roots and standalone agent-specific
instruction files used by this repository's workflow and the broader agent-tool ecosystem:

```text
**/.agents/
**/.claude/
**/.codex/
**/.continue/
**/.cursor/
**/.github/copilot-instructions.md
**/.github/agents/
**/.github/instructions/
**/.github/prompts/
**/.github/skills/
**/.github/hooks/
**/CLAUDE.md
**/GEMINI.md
**/.copilot/agents/
**/.copilot/instructions/
**/.copilot/skills/
**/.copilot/hooks/
**/.roo/
**/.windsurf/
```

You can still pass repeated `--surface ...` flags when you want the compatibility warnings scoped to
specific workspace export surfaces, but the managed ignore block now covers all known hidden
customization directories by default.

### Maintenance expectations

- Keep `.agents/` canonical.
- Treat `~/.copilot/` and generated `.github/` exports as compatibility targets only.
- If a synced asset is removed or renamed under `.agents/`, rerun the sync script so stale synced
  copies can be removed.
- If future Copilot documentation provides stable user-level filesystem targets for other surfaces,
  this compatibility layer can be expanded intentionally.

### References

- VS Code custom agents:
  <https://code.visualstudio.com/docs/copilot/customization/custom-agents>
- GitHub custom agents:
  <https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents>
- VS Code custom instructions:
  <https://code.visualstudio.com/docs/copilot/customization/custom-instructions>
- VS Code prompt files:
  <https://code.visualstudio.com/docs/copilot/customization/prompt-files>
- VS Code agent skills:
  <https://code.visualstudio.com/docs/copilot/customization/agent-skills>
- VS Code hooks:
  <https://code.visualstudio.com/docs/copilot/customization/customization-overview#_hooks-experimental>
- Copilot CLI overview:
  <https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli>
