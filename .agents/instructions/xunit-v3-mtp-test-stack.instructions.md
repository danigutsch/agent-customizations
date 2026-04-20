---
description: 'Guidance for xUnit v3 plus Microsoft.Testing.Platform in .NET repositories: runner selection, command shape, filters, coverage, fixtures, and troubleshooting.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/xunit-v3-mtp-test-stack.agent.md, .agents/skills/xunit-v3-mtp-test-stack/**, .agents/instructions/xunit-v3-mtp-test-stack.instructions.md'
---

# Xunit V3 Mtp Test Stack Guidance

Use these rules when the task is about xUnit v3 test stacks built on Microsoft.Testing.Platform.

## Core model

- Treat xUnit v3 and Microsoft.Testing.Platform as one explicit stack choice.
- Prefer named `dotnet test --project` and `dotnet test --solution` commands in guidance and docs.
- Treat `dotnet test` as an orchestrator whose available test switches depend on the registered
  MTP extensions in the test project.
- Keep stack guidance explicit about the MTP major version when the repo pins one through
  `xunit.v3.mtp-v1` or `xunit.v3.mtp-v2`.
- Prefer guidance that preserves MTP's determinism model: compile-time extension
  registration, explicit command shape, and reproducible local-versus-CI runs.

## Runner and package rules

- Confirm whether the repository opts into Microsoft.Testing.Platform through `global.json`,
  project settings, or both before changing test guidance.
- Prefer explicit package references when the repo wants to pin an MTP major version.
- Keep VSTest compatibility packages only when the supported tooling still requires them.
- Do not assume that every xUnit v3 repository wants the same runner mode or migration timing.

## Command and filter rules

- Prefer `dotnet test --project <path-to-csproj>` for targeted runs.
- Prefer `dotnet test --solution <path-to-sln-or-slnx>` for repo-wide runs.
- Prefer xUnit v3 filter switches such as `--filter-class`, `--filter-method`,
  `--filter-namespace`, and `--filter-trait`.
- Do not recommend legacy VSTest filter syntax like `--filter "FullyQualifiedName~..."` for MTP
  guidance.
- Use `--minimum-expected-tests` on narrow filtered runs when accidental zero-test discovery would
  be costly.

## Coverage and diagnostics rules

- Prefer MTP-native coverage extensions and command examples.
- Be explicit when solution-level coverage writes one predictable coverage file per test project
  rather than one merged file.
- Prefer `--list-tests`, `--help`, and `--info` before guessing at unsupported switches.
- Use MTP diagnostic output when discovery or execution remains unclear after the standard checks.

## Fixture and parallelization rules

- Prefer xUnit v3 assembly fixtures when one shared infrastructure instance should serve the whole
  test assembly without suppressing normal parallelization.
- Prefer constructor context for per-test setup, class fixtures for one-class
  sharing, and collection fixtures for several classes that truly need one
  shared expensive context.
- Keep explicit serial collections narrow and intentional.
- Prefer test-owned data creation and helper APIs over mutation of shared seeded data when
  parallel-safe execution matters.
- Keep fixture choice aligned with the actual resource-sharing model instead of copying older
  collection-fixture habits mechanically.
- Remember that assembly fixtures do not disable parallel execution on their
  own; assembly-wide fixtures and helpers must be concurrency-safe or paired
  with narrow serial collections.

## Test-stack boundary rules

- Keep this guidance focused on xUnit v3 plus Microsoft.Testing.Platform, not on generic test style
  advice that belongs elsewhere.
- Document behavioral versus infrastructure test-project boundaries when they materially affect
  fixtures, data ownership, and command usage.
- Keep browser, component, BDD, and architecture test projects aligned to the same MTP command and
  troubleshooting model when they run on the same stack.
- When suite guidance discusses entry points, prefer public HTTP or published
  messaging edges for integration tests and user-visible seams for browser
  tests rather than internal implementation hooks.

## Verification

- Confirm the repository runner contract is explicit and internally consistent.
- Confirm command examples use named `--project` or `--solution` arguments.
- Confirm filter guidance uses xUnit v3 plus MTP switches rather than VSTest syntax.
- Confirm coverage guidance reflects actual MTP output behavior.
- Confirm fixture guidance preserves parallelism unless serialization is intentionally required.
