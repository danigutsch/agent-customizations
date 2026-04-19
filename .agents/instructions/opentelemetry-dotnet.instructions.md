---
description: 'Guidance for OpenTelemetry in .NET: cohesive logs, metrics, and traces, resource metadata, semantic conventions, exporter boundaries, and keeping telemetry setup out of business logic.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/opentelemetry-dotnet.agent.md, .agents/skills/opentelemetry-dotnet/**, .agents/instructions/opentelemetry-dotnet.instructions.md'
---

# Opentelemetry Dotnet Guidance

Use these rules when the task is about configuring or reviewing OpenTelemetry in .NET applications or
shared defaults.

## Core model

- Use .NET's native telemetry primitives with OpenTelemetry collecting and exporting from them.
- Keep logs, metrics, and traces aligned as one observability story rather than three isolated
  configuration islands.
- Configure resource identity and signal setup early in startup or shared defaults.
- Keep business logic unaware of exporter and backend configuration.
- Centralize reusable telemetry names, outcomes, and exception conventions in shared observability
  types rather than scattering strings across services.

## Resource rules

- Configure service name, version, and related resource metadata centrally.
- Prefer configuration or shared defaults over duplicating identity literals across services.
- Keep resource identity stable enough for cross-service correlation.

## Instrumentation rules

- Prefer automatic instrumentation for common frameworks before layering in custom instrumentation.
- Use `ActivitySource`, `Meter`, and logging deliberately for app-specific telemetry.
- Be explicit about which signals are enabled and why.
- Prefer source-generated `LoggerMessage` patterns for high-frequency structured logging paths when
  they improve consistency and performance.
- Consider strongly typed metrics source generation when related metrics should share one compile-time
  safe tag model.
- Prefer paired `ActivitySource`, `Meter`, and source-generated logging guidance for one workflow when
  all three signals matter.

## Semantic conventions

- Reuse OpenTelemetry semantic conventions when they already cover the operation.
- Keep custom attributes narrow and consistent when no standard key exists.
- Avoid telemetry naming drift between services that should be comparable.

## Exporter boundary

- Keep OTLP or vendor exporter configuration in startup composition or shared defaults.
- Treat exporters as pluggable outputs, not as business-code dependencies.
- Use local diagnostic exporters for verification without letting them define the final design.

## Testing guidance

- Verify logs, metrics, and traces together for the same workflow when observability is part of the
  contract.
- Call out process-wide listener state when tests need serialization or isolation.
- Assert semantic-convention-aligned tags and exception events, not only signal presence.

## Verification

- Confirm resource identity is configured centrally.
- Confirm signal wiring reflects the intended traces, metrics, and logs.
- Confirm the logging, metrics, and tracing guidance stays cohesive rather than fragmenting by signal.
- Confirm exporter setup stays outside business logic.
- Confirm custom telemetry uses semantic conventions where available.
- Confirm reusable telemetry names and conventions are centralized instead of duplicated.
