#!/usr/bin/env sh
set -eu

# Starter lightweight pre-commit hook wrapper.
# Replace the command below with the repository's real fast pre-commit entrypoint.
# Avoid pointing ordinary pre-commit hooks at the heaviest full-repo validation command by default.

make hook-pre-commit
