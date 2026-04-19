---
description: 'Guidance for event-sourced projections: read-model boundaries, checkpointing, replay safety, consistency choices, rebuilds, and operational observability.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/event-sourcing-projections.agent.md, .agents/skills/event-sourcing-projections/**, .agents/instructions/event-sourcing-projections.instructions.md'
---

# Event Sourcing Projections Guidance

Use these rules when the task is about event-sourced read models, projection runners, replay safety,
or projection operations.

## Core model

- Treat projections as read-side derivations from event history, not as an alternate write model.
- Keep projection lifecycles explicit: inline, async, or live/on-demand.
- Keep read-model ownership, checkpoint identity, and consistency guarantees visible to maintainers
  and consumers.
- Prefer deterministic projection behavior that can be rebuilt from the event log.

## Read-model rules

- Define read models for explicit query or reporting needs.
- Keep projection-owned view types separate from event payloads and command-side entities.
- Prefer one focused projection per consumer-facing concern over one broad denormalizer for unrelated
  queries.
- Be explicit when a projection is single-stream versus multi-stream.

## Consistency and lifecycle rules

- Use inline projections only when the read model must be transactionally current with the event
  write.
- Use async projections when the system can tolerate eventual consistency and benefits from lower
  write-path cost or easier background recovery.
- Use live projections when a view is occasional enough that persisted storage is unnecessary.
- Document the chosen consistency model so downstream APIs and UIs do not over-promise freshness.

## Ordering and replay rules

- Process events in stable order with an explicit cursor, position, or checkpoint contract.
- Keep projection handlers replay-safe and deterministic across repeated runs.
- Assume projection rebuilds and checkpoint resets will happen over the lifetime of the system.
- Avoid projection logic that depends on incidental runtime state that cannot be reconstructed later.

## Checkpoint and rebuild rules

- Persist a stable projection name and enough checkpoint metadata to reason about progress.
- Keep checkpoint advancement monotonic and reject backwards movement.
- Treat rebuild workflows as a supported maintenance path, not a manual emergency-only procedure.
- Prefer projection state that can be recreated from stored events over projection state that requires
  hidden side inputs.

## Cross-stream and view-shape rules

- Prefer single-stream aggregation when one stream fully owns the read model.
- Use multi-stream projections deliberately when the view combines facts from multiple streams.
- Keep stream-selection rules and projection identities explicit when cross-stream joins are needed.
- Be careful with create-versus-update behavior so late events do not accidentally create malformed
  view records.

## Observability and operations rules

- Add readiness, lag, or runner-state signals for background projection infrastructure.
- Expose projection failures, rebuild activity, and lag through logs, metrics, traces, or health
  checks when the system depends on projection freshness.
- Keep projection runner naming and health-check terminology stable and easy to correlate with stored
  checkpoints.

## Testing rules

- Unit test projection handlers with representative event sequences.
- Add integration coverage for rebuilds, checkpoint resets, or projection-runner recovery when the
  system persists read models.
- Prefer focused assertions about read-model invariants and checkpoint progress over broad opaque
  storage snapshots.

## Marten-inspired optional practices

- Consider using explicit lifecycle vocabulary such as inline, async, and live projections even in
  non-Marten systems.
- Consider first-class multi-stream projection guidance instead of leaving cross-stream views as ad hoc
  exceptions.
- Consider update-only semantics where update events must not create a new read model if the base view
  does not already exist.
- Consider live aggregation for rare or investigative queries instead of persisting every derived view.
- Consider daemon-style projection processing and rebuild control as explicit operational surfaces.

## Verification

- Confirm the read-model boundary and lifecycle are explicit.
- Confirm checkpointing and replay behavior are monotonic and rebuild-safe.
- Confirm eventual-consistency projections are observable enough for operators and consumers.
- Confirm unit and rebuild tests cover the main event sequences and recovery paths.
