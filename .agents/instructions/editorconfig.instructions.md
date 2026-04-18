---
description: 'Standards for EditorConfig files that define clear repo-wide text defaults and focused file-type overrides.'
applyTo: '.editorconfig, README.md, docs/**/*.md, scripts/**/*, .github/**/*, .agents/**/*'
---

# EditorConfig Standards

Use these rules when the task is about creating or refining `.editorconfig`.

## Core principles

- Treat `.editorconfig` as the shared baseline for whitespace, indentation, line endings, and final
  newlines.
- Keep the file small, readable, and ordered from broad defaults to narrow overrides.
- Use EditorConfig to complement language-specific tools, not replace them.

## Structure

- Put `root = true` at the top when the repository owns the top-most EditorConfig.
- Use a broad default section such as `[*]` for shared text-file behavior.
- Add later sections only for file types that need different behavior.

## Common rule choices

- Keep `charset`, `end_of_line`, and `insert_final_newline` explicit when the repo depends on them.
- Use `trim_trailing_whitespace = false` for Markdown when the repo permits intentional soft breaks.
- Set `indent_style` and `indent_size` only where the repository needs clear indentation defaults.
- Preserve tab-based indentation for formats like `Makefile` when those files exist.

## Repo alignment

- Keep `.editorconfig` aligned with Ruff, Markdown linting, JSON or YAML formatting, and any other
  repo validation rules.
- Do not add sections for file types the repo does not contain unless they are about to be introduced.
- Prefer one shared `.editorconfig` over several overlapping formatting sources.

## Verification

- Confirm the rules match the real file types in the repository.
- Confirm the defaults do not conflict with other configured formatters or linters.
- Confirm any exceptions are narrow and easy to explain.
