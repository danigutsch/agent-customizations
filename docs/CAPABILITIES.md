# Capability Index

This document is the quick index for the reusable customization capabilities curated under `.agents/`.

In this repository, **capability** is the public-facing term. A capability may be implemented through
one or more capability surfaces such as an agent, instruction, skill, prompt, hook, workflow, or
plugin bundle.

## Current capabilities

| Capability | Purpose | Use when | Pairs well with | Plugin bundle |
| --- | --- | --- | --- | --- |
| `repository-setup` | Repository foundations, layout, contributor guidance, and validation surfaces | The repo structure, docs, validation commands, or setup baseline need work | `ci-workflows`, `editorconfig`, `python-quality` | No |
| `ci-workflows` | CI workflow creation, refinement, and local-to-CI command mapping | A repo needs GitHub Actions or equivalent workflow design aligned with local checks | `python-quality`, `ruff-python`, `pyright-python`, `git-hooks` | No |
| `editorconfig` | Shared editor defaults across mixed file types | `.editorconfig` should be created, reviewed, or aligned with repo formatting tools | `repository-setup`, `python-quality`, `ruff-python` | No |
| `python-quality` | Shared Python quality baseline and tool coordination | Python tooling, `pyproject.toml`, repo checks, or contributor guidance need cleanup | `editorconfig`, `ruff-python`, `pyright-python`, `ci-workflows`, `git-hooks` | No |
| `ruff-python` | Ruff linting and formatting guidance | Ruff rules, excludes, commands, hooks, or CI usage need work | `python-quality`, `editorconfig`, `pyright-python`, `ci-workflows` | No |
| `pyright-python` | Shared Pyright and Pylance type-checking rules | Type-checking scope, excludes, or strictness need refinement | `python-quality`, `ruff-python`, `ci-workflows` | No |
| `git-hooks` | Lightweight local Git hook design | Fast local checks should run before commits without replacing CI | `ci-workflows`, `python-quality`, `ruff-python`, `pyright-python` | No |
| `mcp-servers` | Reusable MCP server assets, wrappers, and setup guidance | A repo needs portable MCP manifests, wrappers, or host adaptation notes | `repository-setup`, `ci-workflows`, `workflow-packs` | No |
| `microsoft-extensions-configuration` | Options binding, configuration layering, validation, and configuration shape guidance | A .NET app needs clearer `IOptions*`, config binding, or startup validation rules | `microsoft-extensions-dependency-injection`, `repository-setup` | No |
| `microsoft-extensions-dependency-injection` | Service registration boundaries, lifetime discipline, and composition-root guidance | A .NET app's DI setup, service registration shape, or lifetime boundaries need work | `microsoft-extensions-configuration`, `repository-setup`, `csharp-concurrency-patterns` | No |
| `csharp-concurrency-patterns` | Async coordination, bounded concurrency, channels, and shared-state discipline | A .NET codebase needs clearer concurrency, queueing, cancellation, or background work patterns | `microsoft-extensions-dependency-injection`, `database-performance`, `csharp-type-design-performance` | No |
| `csharp-type-design-performance` | Allocation-aware type and API design for .NET | Type shape, API boundaries, collections, or allocation-sensitive paths need cleanup | `csharp-concurrency-patterns`, `database-performance` | No |
| `database-performance` | Query-shape, projection, batching, and EF Core versus Dapper guidance | A .NET data-access layer needs better read/write boundaries, tracking discipline, or query performance | `csharp-type-design-performance`, `microsoft-extensions-dependency-injection` | No |
| `docfx-specialist` | DocFX structure, navigation, xrefs, and validation workflow guidance | A repo uses DocFX and needs help with docs layout, build warnings, or API-reference integration | `docs-and-scripts-quality` | No |
| `dotnet-performance-analyst` | Profiling, benchmark interpretation, and regression analysis | Performance measurements need interpretation and high-value bottlenecks need ranking | `dotnet-benchmark-designer`, `database-performance`, `csharp-concurrency-patterns` | No |
| `dotnet-benchmark-designer` | Benchmark strategy and measurement-harness design | A .NET performance question needs a reliable benchmark or measurement approach | `dotnet-performance-analyst`, `csharp-type-design-performance`, `database-performance` | No |
| `copilot-compatibility-exports` | Canonical-to-compatible export mapping for Copilot assets | A repo needs to map canonical `.agents` assets into `.github/*` or `~/.copilot/*` safely | `plugin-bundles`, `repository-setup`, `mcp-servers` | No |
| `plugin-bundles` | Plugin manifest, changelog, example, and validator-backed packaging guidance | Capability bundles need explicit packaging contracts, validation, or release metadata | `copilot-compatibility-exports`, `repository-setup` | No |
| `tool-generated-file-provenance` | Baseline-driven provenance and drift inspection for generator-owned files | A repo needs to separate curated assets from tool-generated outputs and report drift conservatively | `copilot-compatibility-exports`, `repository-setup` | No |
| `docs-and-scripts-quality` | Repo docs quality, helper-script maintenance, and local validation workflow alignment | README, maintenance docs, hooks, or helper scripts need quality improvements tied to real repo checks | `repository-setup`, `git-hooks`, `python-quality`, `docfx-specialist` | No |
| `foss-compatibility` | Open-source license compatibility, obligations, provenance, and escalation guidance | A repo needs to assess whether imported open-source assets can be adopted or redistributed safely and what follow-up is required | `repository-setup`, `tool-generated-file-provenance` | No |
| `license-checking` | Automated license inventory, policy gates, SBOM workflows, and review routing | A repo needs repeatable license scanning, explicit allow-deny-review policy checks, or CI-local license gates | `foss-compatibility`, `ci-workflows`, `repository-setup` | No |
| `source-generation` | Roslyn source generator design, setup, testing, and packaging | C# source generators need design, migration, diagnostics, tests, or pack guidance | `repository-setup`, `ci-workflows`, `vertical-slice-architecture` | Yes |
| `vertical-slice-architecture` | Domain-first vertical slice design and migration guidance | A codebase needs clearer slice boundaries, migration steps, or slice-aligned tests | `repository-setup`, `ci-workflows`, `python-quality`, `source-generation` | Yes |
| `workflow-packs` | Reusable multi-step workflow packs and handoff assets | A repo needs repeatable workflow phases, checkpoints, or adaptation examples | `repository-setup`, `ci-workflows`, `mcp-servers` | No |

## Common combinations

| Goal | Recommended capabilities |
| --- | --- |
| Python repository baseline | `repository-setup` + `editorconfig` + `python-quality` + `ruff-python` + `pyright-python` |
| Python repo with enforcement | `repository-setup` + `python-quality` + `ruff-python` + `pyright-python` + `git-hooks` + `ci-workflows` |
| MCP-ready repo baseline | `repository-setup` + `mcp-servers` + `ci-workflows` |
| New generator repo | `repository-setup` + `source-generation` + `ci-workflows` |
| Architecture cleanup with delivery guardrails | `vertical-slice-architecture` + `repository-setup` + `ci-workflows` |
| Reusable rollout or delivery flow | `workflow-packs` + `repository-setup` + `ci-workflows` |
| Canonical asset repo with compatibility mirrors | `repository-setup` + `copilot-compatibility-exports` + `plugin-bundles` + `tool-generated-file-provenance` |
| Repo docs and helper-script maintenance | `repository-setup` + `docs-and-scripts-quality` + `git-hooks` + `python-quality` |
| Open-source intake or redistribution review | `foss-compatibility` + `repository-setup` + `tool-generated-file-provenance` |
| Automated open-source license governance | `license-checking` + `foss-compatibility` + `ci-workflows` + `repository-setup` |
| .NET performance and measurement work | `csharp-type-design-performance` + `csharp-concurrency-patterns` + `database-performance` + `dotnet-performance-analyst` + `dotnet-benchmark-designer` |

## Selection guidance

- Start with `repository-setup` when the problem is repo-wide.
- Add `editorconfig` when mixed text file types need consistent editor defaults.
- Add `python-quality` when the repo needs a coordinated Python baseline.
- Add `ruff-python` or `pyright-python` when the task is tool-specific rather than baseline-wide.
- Add `git-hooks` when local convenience checks should complement CI.
- Add `mcp-servers` when reusable MCP assets or setup guidance need to be curated.
- Add `copilot-compatibility-exports` when canonical assets need a clear compatibility mirror model.
- Add `plugin-bundles` when capabilities are packaged and versioned as explicit bundle contracts.
- Add `tool-generated-file-provenance` when generated downstream files must stay separate from curated assets.
- Add `foss-compatibility` when imported open-source assets need compatibility review, obligations tracking, or escalation guidance.
- Add `license-checking` when dependency or asset inventories need repeatable automated license checks, policy gates, or SBOM outputs.
- Add `docs-and-scripts-quality` when maintenance docs, helper scripts, and local checks need to stay aligned.
- Add `ci-workflows` when the local validation path should be wrapped in automation.
- Add `workflow-packs` when multi-step reusable workflows need explicit phases and checkpoints.
- Use bundled capabilities when the capability is naturally adopted as one unit.
