---
name: opentelemetry-dotnet
description: Guidance for OpenTelemetry in .NET applications. Use when configuring logs, metrics, and traces together, setting resource metadata like service identity, choosing automatic versus manual instrumentation, wiring OTLP or other exporters, using source-generated logging or strongly typed metrics, or keeping telemetry setup in startup/shared defaults instead of business logic.
---

# Opentelemetry Dotnet

Use this skill when the task is about OpenTelemetry setup in .NET rather than vendor-specific APM
configuration alone.

## When to Use This Skill

- The user wants to configure OpenTelemetry logs, metrics, or traces in a .NET app
- The user needs to set service identity or other resource metadata consistently
- The user needs to choose between automatic and manual instrumentation
- The user needs guidance on OTLP or other exporter boundaries
- The user needs guidance on source-generated logging or strongly typed metrics in the same
  observability model
- The user needs to centralize observability names, exception conventions, or shared telemetry helpers
- The user wants telemetry setup to live in startup or shared defaults instead of domain code

## Prerequisites

- The .NET application startup or shared-defaults configuration can be inspected.
- The desired telemetry signals are known well enough to reason about coverage.
- The task is about .NET OpenTelemetry setup, not only backend-specific dashboard usage.

## Workflow

### 1. Identify the signal boundary

- Decide whether traces, metrics, logs, or multiple signals are in scope.
- Keep the signals aligned intentionally rather than configuring each one in isolation.

### 2. Configure resource identity

- Set service identity and related metadata centrally.
- Keep the identity model consistent across services that belong together.

### 3. Choose instrumentation shape

- Start with automatic instrumentation for supported frameworks.
- Add custom `ActivitySource`, `Meter`, or logging usage only where the application needs domain
  telemetry beyond the automatic baseline.
- Prefer source-generated `LoggerMessage` logging and strongly typed metrics when they improve
  consistency for repeated instrumentation patterns.
- Centralize reusable telemetry names and conventions so features do not invent their own strings.

### 4. Protect the exporter boundary

- Keep exporters in startup or shared defaults.
- Treat exporter choice as replaceable infrastructure.

### 5. Validate the observability surface

- Check that logs, metrics, and traces tell one coherent story for the workflow.
- Verify custom source names, meters, tags, and exception conventions are registered and reusable.
- When tests are involved, account for process-wide listener state explicitly.

## Related guidance

- Pair with [Dotnet Aspire AppHost](../dotnet-aspire-apphost/SKILL.md) when shared defaults and local
  orchestration are part of the telemetry story.
- Pair with [CI Workflows](../ci-workflows/SKILL.md) when telemetry checks need pipeline integration.

## Gotchas

- **Do not put exporter configuration in business logic.**
- **Do not skip resource identity and then expect good correlation.**
- **Do not duplicate custom instrumentation where framework instrumentation already exists.**
- **Do not invent custom attribute names before checking semantic conventions.**
- **Do not let logging, metrics, and traces drift into unrelated patterns when they describe the same
  service behavior.**
- **Do not scatter metric names, activity names, event IDs, or outcome values across unrelated files.**

## References

- [Opentelemetry dotnet guidance](../../instructions/opentelemetry-dotnet.instructions.md)
- [Opentelemetry dotnet agent](../../agents/opentelemetry-dotnet.agent.md)
