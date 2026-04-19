---
description: 'Guidance for project structure: repository layout, project ownership boundaries, shared-code discipline, and test alignment.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/project-structure.agent.md, .agents/skills/project-structure/**, .agents/instructions/project-structure.instructions.md'
---

# Project Structure Guidance

Use these rules when the task is about repository, solution, or project layout.

## Core model

- Structure should communicate ownership and dependency direction.
- Prefer explicit project boundaries where change rate, packaging, or runtime role differs.
- Prefer fewer projects only when the reduced count does not hide real responsibility boundaries.
- Keep tests and tooling aligned with the production structure they support.

## Layout rules

- Keep top-level folders explicit and stable.
- Keep source, tests, docs, scripts, and tooling in clearly named locations.
- Avoid "shared" or "common" projects as dumping grounds for unrelated utilities.
- Separate generators, analyzers, code fixes, and packaging projects when their build and release
  concerns differ.

## Ownership rules

- Keep bounded contexts or feature ownership visible in the layout.
- Keep contracts explicit rather than hiding them inside infrastructure projects.
- Merge projects only when the existing split no longer earns its maintenance cost.
- Split projects when packaging, runtime role, or ownership genuinely differs.

## Test-alignment rules

- Keep test-project names and placement aligned with the production code they verify.
- Separate behavioral, infrastructure, browser, or tooling tests only when their execution model
  differs materially.

## Verification

- Confirm ownership boundaries are obvious from the layout.
- Confirm shared code is truly shared and not a convenience dump.
- Confirm test and tooling projects map cleanly to the production structure.
- Confirm the project count is justified by real boundaries, not ceremony.
