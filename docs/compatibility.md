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
| Repo-wide instructions | not generated from slice files | `.github/copilot-instructions.md` | `$HOME/.copilot/copilot-instructions.md` in CLI | Separate always-on file type |
| Prompts | `.agents/prompts/*.prompt.md` | `.github/prompts/` | VS Code profile storage, not a stable `~/.copilot` path | Same Markdown format, workspace export only |
| Skills | `.agents/skills/<skill>/SKILL.md` | `.github/skills/` if needed | `~/.copilot/skills/` | `.agents/skills/` is already a native project skill location |
| Hooks | `.agents/hooks/*.json` | `.github/hooks/` | `~/.copilot/hooks/` in VS Code | Same JSON format, workspace target is the broadest portable option |
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
2. **Workspace scope**
   - target root: a repository root
   - best for: `.github/` exports needed by repo-scoped Copilot features, especially prompts and hooks

The generic export script is:

```bash
python3 scripts/sync_copilot_exports.py
```

When a plugin bundle exists, prefer exporting by plugin so the synced files stay aligned the same
way the bundle was packaged:

```bash
python3 scripts/sync_copilot_exports.py --scope workspace --target-root /path/to/repo --plugin source-generation
python3 scripts/sync_copilot_exports.py --scope user --plugin vertical-slice-architecture
```

Use `--surface ...` as the lower-level fallback when no plugin bundle exists yet.

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

- Repo-wide instructions are a different surface than slice-scoped `.instructions.md` files.
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

Run the generic export script for workspace sync:

```bash
python3 scripts/sync_copilot_exports.py --scope workspace --target-root /path/to/repo
```

This exports supported `.agents/` surfaces into Copilot-native locations for that repository.

Examples:

```bash
python3 scripts/sync_copilot_exports.py --scope user --dry-run
python3 scripts/sync_copilot_exports.py --scope workspace --target-root ../some-repo --dry-run
python3 scripts/sync_copilot_exports.py --scope workspace --target-root ../some-repo --surface prompts
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

### Ignore strategy for generated workspace exports

If you treat workspace exports as generated compatibility files rather than tracked repo content, the
safest default is:

- use `--write-git-exclude` to write managed patterns into `.git/info/exclude` for that repo
- use a global ignore only if you are intentionally standardizing generated Copilot export folders
  across your own repositories

If you are standardizing on generated `.github/...` Copilot exports across your repos, a global
ignore is reasonable. The main caveat is not compatibility with Git or Copilot, but that ignore
rules do **not** affect files that are already tracked.

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

By default this manages the common hidden customization roots used by this repository's workflow and
the broader agent-tool ecosystem:

```text
**/.agents/
**/.claude/
**/.codex/
**/.continue/
**/.cursor/
**/.github/agents/
**/.github/instructions/
**/.github/prompts/
**/.github/skills/
**/.github/hooks/
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
- Treat `~/.copilot/` and generated `.github/` exports as compatibility targets.
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
