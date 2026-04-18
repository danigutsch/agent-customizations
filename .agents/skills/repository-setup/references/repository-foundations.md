# Repository Foundations

Use this reference when the task is about choosing or correcting the basic structure and
documentation surface of a repository.

## Top-level structure

Prefer a small set of top-level folders with clear meanings.

Typical responsibilities:

- `docs/` for durable documentation
- `examples/` for example adaptations or sample usage
- `scripts/` for lightweight maintenance and validation helpers
- `templates/` for starter assets contributors are expected to copy or extend
- focused asset roots such as `.agents/` when the repository stores structured customization assets

## Documentation baseline

For most reusable repositories, the minimum useful documentation surface is:

1. a README that explains the repository purpose and structure
2. repository-wide guidance for contributors when the repository has custom rules
3. references or examples when contributors are expected to reuse patterns repeatedly

For repos with mixed text file types, shared editor defaults in `.editorconfig` are often part of that
baseline because they reduce cross-editor inconsistency without replacing language-specific tools.

## Naming and responsibility

- Prefer names that describe purpose instead of a single client or platform.
- Keep one clear purpose per file or folder.
- Avoid overlapping folders that could both plausibly hold the same assets.
- Make the source of truth explicit when the repository also contains packaging or distribution
  layers.

## Common problems

| Problem | Likely cause | Fix |
| --- | --- | --- |
| The repository feels hard to navigate | Top-level folders overlap or are under-explained | Reduce overlap and document folder responsibilities in the README |
| Contributors add files in inconsistent places | The structure is implied, not documented | Add repository-wide guidance and examples |
| The README is vague | Purpose and boundaries are not stated clearly | State what belongs in the repo and what does not |
| Packaging metadata drifts from source assets | Source of truth is unclear | Document the canonical asset location explicitly |
