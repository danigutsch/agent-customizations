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
| `csharp-api-design` | C# API shape, validation boundary, and compatibility guidance | A .NET codebase needs clearer factory methods, result shapes, DTO-versus-domain boundaries, extension points, or additive API evolution guidance | `csharp-type-design-performance`, `aspnet-api-contracts`, `grpc-protobuf-contracts` | No |
| `project-structure` | Repository, solution, and project-structure guidance | A codebase needs clearer ownership boundaries, project layout, shared-code discipline, or test alignment across repository structure | `repository-setup`, `vertical-slice-architecture`, `package-management` | No |
| `package-management` | Package, SDK, and restore-policy guidance | A repo needs clearer central package management, `global.json` policy, lock-file flow, dependency ownership, or cautious upgrade governance | `repository-setup`, `ci-workflows`, `devcontainers-smoke` | No |
| `slopwatch` | Low-signal bloat, duplication, and AI-sprawl review guidance | A repo needs help spotting duplicated helpers, speculative abstractions, noisy docs, or generated-looking sprawl before it becomes a maintained pattern | `docs-and-scripts-quality`, `tool-generated-file-provenance`, `repository-setup` | No |
| `crap-analysis` | Complexity-plus-coverage hotspot review guidance | A repo needs to find and reduce risky code where branching complexity and weak test protection combine into maintainability risk | `xunit-v3-mtp-test-stack`, `slopwatch`, `dotnet-performance-analyst` | No |
| `dotnet-concurrency-specialist` | End-to-end .NET concurrency system review guidance | A .NET system needs broader review of hosted services, queues, throughput limits, scoped service usage, shutdown, or worker observability beyond code-level primitives alone | `csharp-concurrency-patterns`, `microsoft-extensions-dependency-injection`, `database-performance`, `opentelemetry-dotnet` | No |
| `database-performance` | Query-shape, projection, batching, and EF Core versus Dapper guidance | A .NET data-access layer needs better read/write boundaries, tracking discipline, or query performance | `csharp-type-design-performance`, `csharp-concurrency-patterns`, `microsoft-extensions-dependency-injection` | No |
| `mkdocs-specialist` | MkDocs and Material for MkDocs site guidance | A repo needs a Markdown-first docs portal, `mkdocs.yml` cleanup, explicit navigation, lightweight validation, or git-host pages/docs publishing guidance | `docs-and-scripts-quality`, `repository-setup`, `ci-workflows` | No |
| `dotnet-performance-analyst` | Profiling, benchmark interpretation, and regression analysis | Performance measurements need interpretation and high-value bottlenecks need ranking | `dotnet-benchmark-designer`, `database-performance`, `csharp-concurrency-patterns` | No |
| `dotnet-benchmark-designer` | Benchmark strategy and measurement-harness design | A .NET performance question needs a reliable benchmark or measurement approach | `dotnet-performance-analyst`, `csharp-type-design-performance`, `database-performance` | No |
| `copilot-compatibility-exports` | Canonical-to-compatible export mapping for Copilot assets | A repo needs to map canonical `.agents` assets into `.github/*` or `~/.copilot/*` safely | `plugin-bundles`, `repository-setup`, `mcp-servers` | No |
| `plugin-bundles` | Plugin manifest, changelog, example, and validator-backed packaging guidance | Capability bundles need explicit packaging contracts, validation, or release metadata | `copilot-compatibility-exports`, `repository-setup` | No |
| `tool-generated-file-provenance` | Baseline-driven provenance and drift inspection for generator-owned files | A repo needs to separate curated assets from tool-generated outputs and report drift conservatively | `copilot-compatibility-exports`, `repository-setup` | No |
| `docs-and-scripts-quality` | Repo docs quality, helper-script maintenance, and local validation workflow alignment | README, maintenance docs, hooks, or helper scripts need quality improvements tied to real repo checks | `repository-setup`, `git-hooks`, `python-quality`, `mkdocs-specialist` | No |
| `foss-compatibility` | Open-source license compatibility, obligations, provenance, and escalation guidance | A repo needs to assess whether imported open-source assets can be adopted or redistributed safely and what follow-up is required | `repository-setup`, `tool-generated-file-provenance` | No |
| `license-checking` | Automated license inventory, policy gates, SBOM workflows, and review routing | A repo needs repeatable license scanning, explicit allow-deny-review policy checks, or CI-local license gates | `foss-compatibility`, `ci-workflows`, `repository-setup` | No |
| `devcontainers-smoke` | Devcontainer smoke-validation and contributor-path guidance | A repo needs a shared local-and-CI smoke path for `.devcontainer/**`, lifecycle hooks, toolchain verification, optional deeper in-container validation, or supplemental workflow coverage for environment drift | `ci-workflows`, `repository-setup`, `docs-and-scripts-quality` | No |
| `dotnet-aspire-apphost` | Narrow .NET Aspire AppHost orchestration guidance | A distributed .NET app needs clearer AppHost resource modeling, service references, startup ordering, or AppHost boundary discipline | `repository-setup`, `ci-workflows`, `opentelemetry-dotnet` | No |
| `aspnet-api-contracts` | ASP.NET HTTP API contract design guidance | An ASP.NET API needs clearer route shape, DTO boundaries, typed results, ProblemDetails behavior, OpenAPI metadata, versioning, or contract-test strategy | `repository-setup`, `ci-workflows`, `xunit-v3-mtp-test-stack` | No |
| `event-sourcing-projections` | Event-sourced projection and read-model guidance | A system needs clearer projection lifecycles, read-model boundaries, checkpointing, replay safety, rebuild workflow, multi-stream views, or projection-runner operations | `xunit-v3-mtp-test-stack`, `database-performance`, `opentelemetry-dotnet`, `aspnet-api-contracts` | No |
| `github-issues` | GitHub issue authoring, updates, dependencies, fields, and project-aware issue workflows | A repo needs structured GitHub issue creation, issue-type discipline, sub-issues, dependency links, issue fields, or project-item updates | `workflow-packs`, `agent-coordination`, `repository-setup` | No |
| `grpc-protobuf-contracts` | gRPC and Protocol Buffers contract design and evolution guidance | A repo needs safer `.proto` schemas, package versioning, streaming RPC choices, or clearer contract ownership boundaries | `repository-setup`, `ci-workflows` | No |
| `opentelemetry-dotnet` | OpenTelemetry setup and instrumentation guidance for .NET | A .NET app needs cohesive logs, metrics, and traces, consistent resource identity, semantic conventions, exporter boundaries, source-generated logging, or strongly typed metrics guidance | `dotnet-aspire-apphost`, `ci-workflows`, `repository-setup` | No |
| `xunit-v3-mtp-test-stack` | xUnit v3 plus Microsoft.Testing.Platform test-stack guidance for .NET | A .NET repo needs clearer xUnit v3 runner choice, MTP command shape, filtering, coverage, fixture, or troubleshooting guidance | `ci-workflows`, `repository-setup`, `dotnet-aspire-apphost` | No |
| `snapshot-testing` | Snapshot and approval testing guidance for stable reviewed output contracts | A repo needs Verify-style approval tests, `.verified.*` versus `.received.*` discipline, output scrubbing, or CI-friendly review flow for rendered, serialized, generated, or API-surface output | `xunit-v3-mtp-test-stack`, `aspnet-api-contracts`, `event-sourcing-projections` | No |
| `source-generation` | Roslyn source generator design, setup, testing, and packaging | C# source generators need design, migration, diagnostics, tests, or pack guidance | `repository-setup`, `ci-workflows`, `vertical-slice-architecture` | Yes |
| `vertical-slice-architecture` | Domain-first vertical slice design and migration guidance | A codebase needs clearer slice boundaries, migration steps, or slice-aligned tests | `repository-setup`, `ci-workflows`, `python-quality`, `source-generation` | Yes |
| `workflow-packs` | Reusable multi-step workflow packs and handoff assets | A repo needs repeatable workflow phases, checkpoints, or adaptation examples | `repository-setup`, `ci-workflows`, `mcp-servers` | No |
| `agent-coordination` | Multi-agent control-plane guidance for lanes, routing, handoffs, and escalation | A repo needs a reusable coordinator-plus-workers model with explicit lane ownership, Copilot versus external-worker boundaries, or cost-aware model routing | `workflow-packs`, `copilot-compatibility-exports`, `repository-setup`, `mcp-servers` | No |

## Common combinations

| Goal | Recommended capabilities |
| --- | --- |
| Python repository baseline | `repository-setup` + `editorconfig` + `python-quality` + `ruff-python` + `pyright-python` |
| Python repo with enforcement | `repository-setup` + `python-quality` + `ruff-python` + `pyright-python` + `git-hooks` + `ci-workflows` |
| MCP-ready repo baseline | `repository-setup` + `mcp-servers` + `ci-workflows` |
| New generator repo | `repository-setup` + `source-generation` + `ci-workflows` |
| Architecture cleanup with delivery guardrails | `vertical-slice-architecture` + `repository-setup` + `ci-workflows` |
| Stable C# API surface | `csharp-api-design` + `csharp-type-design-performance` + `repository-setup` |
| Repo and solution layout review | `project-structure` + `repository-setup` + `vertical-slice-architecture` |
| .NET dependency governance baseline | `package-management` + `repository-setup` + `ci-workflows` |
| Reusable rollout or delivery flow | `workflow-packs` + `repository-setup` + `ci-workflows` |
| GitHub issue-driven planning and tracking | `github-issues` + `workflow-packs` + `agent-coordination` |
| Parallel agent team baseline | `agent-coordination` + `workflow-packs` + `copilot-compatibility-exports` + `repository-setup` |
| Canonical asset repo with compatibility mirrors | `repository-setup` + `copilot-compatibility-exports` + `plugin-bundles` + `tool-generated-file-provenance` |
| Repo docs and helper-script maintenance | `repository-setup` + `docs-and-scripts-quality` + `git-hooks` + `python-quality` |
| Low-signal change cleanup | `slopwatch` + `docs-and-scripts-quality` + `tool-generated-file-provenance` |
| Maintainability hotspot reduction | `crap-analysis` + `xunit-v3-mtp-test-stack` + `dotnet-performance-analyst` |
| Open-source intake or redistribution review | `foss-compatibility` + `repository-setup` + `tool-generated-file-provenance` |
| Automated open-source license governance | `license-checking` + `foss-compatibility` + `ci-workflows` + `repository-setup` |
| Documented containerized contributor path | `devcontainers-smoke` + `repository-setup` + `ci-workflows` + `docs-and-scripts-quality` |
| Markdown-first docs portal | `mkdocs-specialist` + `docs-and-scripts-quality` + `ci-workflows` |
| Aspire orchestration boundary review | `dotnet-aspire-apphost` + `repository-setup` + `ci-workflows` |
| ASP.NET API contract review | `aspnet-api-contracts` + `repository-setup` + `ci-workflows` + `xunit-v3-mtp-test-stack` |
| Event-sourced read-model design | `event-sourcing-projections` + `xunit-v3-mtp-test-stack` + `database-performance` + `opentelemetry-dotnet` |
| Contract-first gRPC API design | `grpc-protobuf-contracts` + `repository-setup` + `ci-workflows` |
| .NET concurrency system review | `dotnet-concurrency-specialist` + `csharp-concurrency-patterns` + `database-performance` + `opentelemetry-dotnet` |
| .NET observability foundation | `opentelemetry-dotnet` + `repository-setup` + `ci-workflows` |
| .NET xUnit v3 plus MTP baseline | `xunit-v3-mtp-test-stack` + `repository-setup` + `ci-workflows` |
| Approval testing for output contracts | `snapshot-testing` + `xunit-v3-mtp-test-stack` + `aspnet-api-contracts` |
| .NET performance and measurement work | `csharp-type-design-performance` + `csharp-concurrency-patterns` + `database-performance` + `dotnet-performance-analyst` + `dotnet-benchmark-designer` |

## Selection guidance

- Start with `repository-setup` when the problem is repo-wide.
- Add `editorconfig` when mixed text file types need consistent editor defaults.
- Add `python-quality` when the repo needs a coordinated Python baseline.
- Add `ruff-python` or `pyright-python` when the task is tool-specific rather than baseline-wide.
- Add `git-hooks` when local convenience checks should complement CI.
- Add `github-issues` when GitHub issue bodies, issue types, labels, sub-issues, dependencies, issue
  fields, or project-item updates need focused guidance.
- Add `mcp-servers` when reusable MCP assets or setup guidance need to be curated.
- Add `copilot-compatibility-exports` when canonical assets need a clear compatibility mirror model.
- Add `plugin-bundles` when capabilities are packaged and versioned as explicit bundle contracts.
- Add `tool-generated-file-provenance` when generated downstream files must stay separate from curated assets.
- Add `foss-compatibility` when imported open-source assets need compatibility review, obligations tracking, or escalation guidance.
- Add `license-checking` when dependency or asset inventories need repeatable automated license checks, policy gates, or SBOM outputs.
- Add `csharp-api-design` when C# factory methods, result shapes, DTO-versus-domain boundaries, extension points, or additive API evolution need focused review.
- Add `project-structure` when repository, solution, or project layout needs clearer ownership boundaries and test alignment.
- Add `package-management` when package versions, SDK pins, lock files, or restore policy need one coherent dependency-governance model.
- Add `slopwatch` when low-signal bloat, duplication, speculative abstractions, or AI-generated sprawl need focused cleanup.
- Add `crap-analysis` when complexity and weak coverage together make a maintained code path risky.
- Add `dotnet-concurrency-specialist` when a hosted service, queue, or pipeline needs broader concurrency review beyond code-level primitive choice.
- Add `devcontainers-smoke` when a repository needs one shared local-and-CI smoke path for its documented devcontainer workflow, lifecycle hooks, toolchain
  checks, or supplemental drift validation.
- Add `mkdocs-specialist` when a repository wants a Markdown-first docs site with explicit `mkdocs.yml`
  navigation, lightweight validation, or git-host pages/docs publishing guidance.
- Add `dotnet-aspire-apphost` when Aspire AppHost orchestration, references, startup ordering, or AppHost boundaries need focused review.
- Add `aspnet-api-contracts` when an ASP.NET API needs focused review of route shape, DTO boundaries, typed results, ProblemDetails behavior, OpenAPI metadata,
  versioning, or contract-test strategy.
- Add `event-sourcing-projections` when event-sourced read models need focused review of projection lifecycle, checkpointing, replay safety, rebuild workflow,
multi-stream views, or operational readiness.
- Add `grpc-protobuf-contracts` when `.proto` schemas, gRPC service contracts, or contract-evolution rules need focused review.
- Add `opentelemetry-dotnet` when .NET logs, metrics, and traces need to stay cohesive or when resource metadata, exporter boundaries, source-generated logging,
  or strongly typed metrics need focused review.
- Add `xunit-v3-mtp-test-stack` when a .NET repository needs focused xUnit v3 plus Microsoft.Testing.Platform guidance for runner choice, command shape,
  filters, coverage, fixtures, or troubleshooting.
- Add `snapshot-testing` when rendered output, serialized payloads, generated code, HTTP responses, or public API surfaces need reviewed baseline files,
  scrubbers for dynamic values, and a CI-friendly approval workflow.
- Add `docs-and-scripts-quality` when maintenance docs, helper scripts, and local checks need to stay aligned.
- Add `ci-workflows` when the local validation path should be wrapped in automation.
- Add `workflow-packs` when multi-step reusable workflows need explicit phases and checkpoints.
- Add `agent-coordination` when a repository needs explicit multi-agent lanes, handoffs, model
  routing, escalation rules, or Copilot versus external-worker boundaries.
- Use bundled capabilities when the capability is naturally adopted as one unit.
