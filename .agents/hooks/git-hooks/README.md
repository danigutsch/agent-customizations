# Git hooks assets

Reusable hook assets for the `git-hooks` slice live here.

## Contents

- `pre-commit-fast-checks.example.sh` — starter example hook wrapper for a cheap local pre-commit
  entrypoint

## Notes

- Treat these as adaptation starters, not as recommended final hook implementations.
- Point wrappers at a fast repository-local pre-commit command such as `make hook-pre-commit`, not at
  the heaviest validation entrypoint by default.
- Keep hook assets thin and aligned with repository-local commands where possible.
