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

If you change Python scripts, format them before committing:

```bash
make format
```

Helpful focused commands:

- `make validate-repo`
- `make validate-plugins`
- `make smoke-exports`
- `make sync-user`
- `make sync-workspace`
- `make setup-mcp MANIFEST=.agents/mcp/mcp-servers/my-server.json`

## Contribution boundaries

- Keep reusable assets generic unless a file is explicitly an example.
- Do not commit secrets, machine-specific paths, or one-off local setup artifacts.
- Do not add duplicate capabilities or overlapping docs when an existing capability already owns the
  problem.
- When changing compatibility behavior, update the related scripts and docs together.

## Community expectations

By participating in this repository, you agree to follow the expectations in
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
