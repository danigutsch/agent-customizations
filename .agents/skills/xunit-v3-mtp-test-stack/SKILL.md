---
name: xunit-v3-mtp-test-stack
description: Guidance for xUnit v3 on Microsoft.Testing.Platform in .NET repositories. Use when setting the repo test runner, choosing xUnit v3 MTP package variants, writing `dotnet test --project` or `--solution` commands, using xUnit filter switches, configuring MTP-native coverage, designing assembly fixtures, or troubleshooting zero-test and unsupported-switch failures.
---

# Xunit V3 Mtp Test Stack

Use this skill when the task is about the xUnit v3 plus Microsoft.Testing.Platform stack rather
than general testing advice alone.

## When to Use This Skill

- The user needs to set up or review xUnit v3 on Microsoft.Testing.Platform
- The user needs to choose between xUnit v3 MTP package variants or runner modes
- The user needs reliable `dotnet test --project` or `dotnet test --solution` command guidance
- The user needs xUnit v3 filter guidance for MTP
- The user needs MTP-native coverage or diagnostic command guidance
- The user needs fixture or parallelization guidance for xUnit v3 test assemblies
- The user needs help choosing constructor, class, collection, or assembly
  fixture scope for a .NET test suite
- The user needs troubleshooting for zero tests discovered, invalid switches, or mixed runner setups

## Prerequisites

- The repository test-runner choice can be inspected in repo configuration or test projects.
- At least one test project or contributor doc can be inspected for current command patterns.
- The task is specifically about xUnit v3 plus MTP behavior, not just generic assertion style.

## Workflow

### 1. Confirm the runner contract

- Check whether the repository opts into Microsoft.Testing.Platform globally or per project.
- Check whether the repo intentionally pins an xUnit v3 MTP package variant such as
  `xunit.v3.mtp-v2`.

### 2. Normalize the command shape

- Prefer `dotnet test --project <path-to-csproj>` for targeted runs.
- Prefer `dotnet test --solution <path-to-sln-or-slnx>` for full-suite runs.
- Avoid positional-path guidance when the task is specifically about MTP command clarity.

### 3. Choose the right filters and platform options

- Prefer `--filter-class`, `--filter-method`, `--filter-namespace`, and `--filter-trait`.
- Use `--minimum-expected-tests` for narrow filtered runs.
- Start troubleshooting with `--list-tests`, then `--help`, then `--info`.

### 4. Keep coverage and diagnostics MTP-native

- Prefer MTP-native coverage extensions and command shapes.
- Be explicit when coverage output is written per test project and later aggregated.

### 5. Design fixtures for parallel-safe suites

- Prefer xUnit v3 assembly fixtures when one shared app or resource should serve the whole
  assembly.
- Choose constructor context, class fixture, collection fixture, or assembly
  fixture based on the real sharing boundary and setup cost.
- Keep serial collections narrow and intentional.
- Prefer test-owned data creation over shared mutable seeded data when parallelism matters.

## Related guidance

- Pair with [CI Workflows](../ci-workflows/SKILL.md) when test commands and coverage should be
  automated in CI.
- Pair with [Dotnet Aspire AppHost](../dotnet-aspire-apphost/SKILL.md) when infrastructure tests
  depend on Aspire-managed resources.

## Gotchas

- **Do not use legacy VSTest filter syntax for xUnit v3 on MTP.**
- **Do not assume old `dotnet test <path>` examples communicate the intended MTP command shape.**
- **Do not collapse an entire suite into serial execution when assembly fixtures and a small serial
  collection would preserve parallelism.**
- **Do not assume solution-level coverage produces one merged file automatically.**

## References

- [Xunit v3 mtp test stack guidance](../../instructions/xunit-v3-mtp-test-stack.instructions.md)
- [Xunit v3 mtp test stack agent](../../agents/xunit-v3-mtp-test-stack.agent.md)
