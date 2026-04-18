# Repository slice delivery workflow

This starter example shows one way to deliver a reusable repository slice in small, reviewable
batches. Adapt the phases and validation points to the target repository instead of treating this as
a fixed required process.

## Goal

Deliver a reusable repository slice in small, reviewable batches.

## Phases

1. Clarify the target slice and its boundaries.
2. Inspect existing reusable assets and local repo conventions.
3. Implement one atomic batch.
4. Validate the affected local commands and focused checks.
5. Commit the batch before moving to the next slice.

## Checkpoints

- The slice has a clear purpose and scope.
- Related surfaces have been reviewed intentionally.
- Validation steps are explicit and reproducible.
