---
description: 'Standards for reusable workflow packs, handoff-oriented workflow assets, and adaptation guidance.'
applyTo: '.agents/workflows/**/*, docs/**/*.md, README.md'
---

# Workflow Packs Standards

Use these rules when the task is about creating or refining reusable workflow packs.

## Workflow purpose

- Keep workflow packs reusable across repositories whenever possible.
- Make the workflow goal, phases, inputs, outputs, and checkpoints explicit.
- Separate reusable workflow structure from repository-specific examples.

## Workflow design

- Prefer clearly named phases over vague step lists.
- Keep prerequisites, handoffs, and validation checkpoints close to the relevant steps.
- Make it obvious which parts are reusable and which need local adaptation.

## Adaptation guidance

- Include small examples that show how a repository would adopt the workflow.
- Avoid embedding product-specific assumptions in the reusable pack itself.
- Document portability limits and required local decisions.

## Maintenance

- Keep workflow packs lightweight enough to review and update.
- Favor readability and reuse over over-automating every step.
- Align workflow packs with the repository's other slice and packaging rules.

## Verification

- Confirm the workflow pack can be understood without hidden context.
- Confirm examples remain illustrative rather than pretending to be universal.
- Confirm validation checkpoints are explicit.
