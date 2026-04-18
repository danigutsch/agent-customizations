# Slice Inventory

This document is the quick index for the reusable slices under `.agents/`.

## Current slices

| Slice | Purpose | Use when | Pairs well with | Plugin bundle |
| --- | --- | --- | --- | --- |
| `repository-setup` | Repository foundations, layout, contributor guidance, and validation surfaces | The repo structure, docs, validation commands, or setup baseline need work | `ci-workflows`, `editorconfig`, `python-quality` | No |
| `ci-workflows` | CI workflow creation, refinement, and local-to-CI command mapping | A repo needs GitHub Actions or equivalent workflow design aligned with local checks | `python-quality`, `ruff-python`, `pyright-python`, `git-hooks` | No |
| `editorconfig` | Shared editor defaults across mixed file types | `.editorconfig` should be created, reviewed, or aligned with repo formatting tools | `repository-setup`, `python-quality`, `ruff-python` | No |
| `python-quality` | Shared Python quality baseline and tool coordination | Python tooling, `pyproject.toml`, repo checks, or contributor guidance need cleanup | `editorconfig`, `ruff-python`, `pyright-python`, `ci-workflows`, `git-hooks` | No |
| `ruff-python` | Ruff linting and formatting guidance | Ruff rules, excludes, commands, hooks, or CI usage need work | `python-quality`, `editorconfig`, `pyright-python`, `ci-workflows` | No |
| `pyright-python` | Shared Pyright and Pylance type-checking rules | Type-checking scope, excludes, or strictness need refinement | `python-quality`, `ruff-python`, `ci-workflows` | No |
| `git-hooks` | Lightweight local Git hook design | Fast local checks should run before commits without replacing CI | `ci-workflows`, `python-quality`, `ruff-python`, `pyright-python` | No |
| `mcp-servers` | Reusable MCP server assets, wrappers, and setup guidance | A repo needs portable MCP manifests, wrappers, or host adaptation notes | `repository-setup`, `ci-workflows`, `workflow-packs` | No |
| `source-generation` | Roslyn source generator design, setup, testing, and packaging | C# source generators need design, migration, diagnostics, tests, or pack guidance | `repository-setup`, `ci-workflows`, `vertical-slice-architecture` | Yes |
| `vertical-slice-architecture` | Domain-first vertical slice design and migration guidance | A codebase needs clearer slice boundaries, migration steps, or slice-aligned tests | `repository-setup`, `ci-workflows`, `python-quality`, `source-generation` | Yes |
| `workflow-packs` | Reusable multi-step workflow packs and handoff assets | A repo needs repeatable workflow phases, checkpoints, or adaptation examples | `repository-setup`, `ci-workflows`, `mcp-servers` | No |

## Common combinations

| Goal | Recommended slices |
| --- | --- |
| Python repository baseline | `repository-setup` + `editorconfig` + `python-quality` + `ruff-python` + `pyright-python` |
| Python repo with enforcement | `repository-setup` + `python-quality` + `ruff-python` + `pyright-python` + `git-hooks` + `ci-workflows` |
| MCP-ready repo baseline | `repository-setup` + `mcp-servers` + `ci-workflows` |
| New generator repo | `repository-setup` + `source-generation` + `ci-workflows` |
| Architecture cleanup with delivery guardrails | `vertical-slice-architecture` + `repository-setup` + `ci-workflows` |
| Reusable rollout or delivery flow | `workflow-packs` + `repository-setup` + `ci-workflows` |

## Selection guidance

- Start with `repository-setup` when the problem is repo-wide.
- Add `editorconfig` when mixed text file types need consistent editor defaults.
- Add `python-quality` when the repo needs a coordinated Python baseline.
- Add `ruff-python` or `pyright-python` when the task is tool-specific rather than baseline-wide.
- Add `git-hooks` when local convenience checks should complement CI.
- Add `mcp-servers` when reusable MCP assets or setup guidance need to be curated.
- Add `ci-workflows` when the local validation path should be wrapped in automation.
- Add `workflow-packs` when multi-step reusable workflows need explicit phases and checkpoints.
- Use bundled slices when the capability is naturally adopted as one unit.
