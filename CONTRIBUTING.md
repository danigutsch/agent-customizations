# Contributing

## Workflow

1. Read `README.md` and `AGENTS.md` before making repository-wide changes.
2. Treat `.agents/` as the source of truth for curated customization assets.
3. Avoid editing generated or mirrored compatibility outputs first when a canonical `.agents/`
   source exists.
4. Keep changes focused and update nearby docs when contributor expectations or maintenance steps
   change.
5. Prefer adapting an existing upstream capability shape before inventing a new local variant.
6. Open a pull request with a clear summary of the change, why it belongs in this repository, and
   any validation you ran.

## Validation

Run the repository baseline before opening a pull request:

```bash
make check
```

This is the required local baseline. The `Validate repository` workflow runs the same `make check`
command plus a diff-aware plugin version-bump guard in CI.

That baseline includes repository-local Markdown link validation through
`scripts/validate_repo_files.py`, so dead relative docs links should fail before merge.

Pull requests also run the `Dependency Review` workflow, which inspects manifest and lockfile diffs
for newly introduced vulnerable dependencies.
Workflow edits under `.github/workflows/**` or `.github/actions/**` also run the `Actionlint`
workflow, which catches workflow syntax, expression, and embedded shell issues before they land on
`main`.
Pull requests also run the `Secret Scan` workflow, which scans the repository for committed secrets
and keeps a SARIF artifact even when code-scanning upload is skipped for fork pull requests.

Dependabot is configured to stay low-noise: monthly runs, one open version-update PR per ecosystem,
and grouped minor and patch updates. Review action-update PRs against both the release notes and the
resolved pinned SHA. For major action or package upgrades, check the migration guidance before
merging.

If you change Python scripts, format them before committing:

```bash
make format
```

Helpful focused commands:

- `make validate-repo`
- `make lint-markdown`
- `make sync-readme-plugin-changelog`
- `make check-plugin-version-bumps BASE_REF=origin/main HEAD_REF=HEAD`
- `make validate-plugins`
- `make smoke-exports`
- `make sync-user`
- `make sync-workspace`
- `make setup-mcp MANIFEST=.agents/mcp/mcp-servers/my-server.json`

Optional local convenience:

- `make setup-git-config` to opt into the repository's tracked local Git defaults, including the
  lightweight pre-commit hook path and `.git-blame-ignore-revs`, while also applying the shared
  safe global Git defaults used in local docs
- `make install-hooks` if you only want the lightweight pre-commit hook path without the broader
  local Git defaults
- the tracked repository-specific config lives in [`./.gitconfig.shared`](./.gitconfig.shared)

Do not add narrower quality gates unless they solve a real recurring problem in the maintained
surface. For this repository, likely future additions are `slopwatch`, `license-checking`, and
`crap-analysis` when the repository grows enough to justify them.

`Actionlint` and `Secret Scan` are focused supplemental workflows, not replacements for the main
repository baseline.
When the repo adopts focused workflow tooling with a useful local CLI, prefer a thin local
entrypoint over copying long commands into docs or pull request comments. For this repo:

```bash
make lint-workflows
make scan-secrets
```

Those commands stay outside `make check` unless the repository intentionally promotes them into the
required baseline.
Run them when the corresponding local CLI is available on your `PATH`.

When a pull request changes a shipped plugin bundle surface, run the diff-aware version guard before
opening the PR:

```bash
make check-plugin-version-bumps BASE_REF=origin/main HEAD_REF=HEAD
```

If plugin release metadata changes, refresh the narrow generated README release-summary section:

```bash
make sync-readme-plugin-changelog
```

## Contribution boundaries

- Keep reusable assets generic unless a file is explicitly an example.
- Do not commit secrets, machine-specific paths, or one-off local setup artifacts.
- Do not add duplicate capabilities or overlapping docs when an existing capability already owns the
  problem.
- When changing compatibility behavior, update the related scripts and docs together.

## Community expectations

By participating in this repository, you agree to follow the expectations in
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
