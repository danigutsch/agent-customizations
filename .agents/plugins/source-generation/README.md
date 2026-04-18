# Source Generation plugin bundle

This bundle packages the source-generation slice as one reusable capability pack.

## What ships together

- source-generation agent
- source-generation instruction
- source-generation prompt
- source-generation skill
- project setup reference
- testing and CI reference

## Why this is a plugin bundle

- The files form one clear capability bundle around Roslyn source generator lifecycle work.
- They are intended to be installed together so role, rules, and skill routing stay aligned.
- They include shared documentation and a bundle example.
- The slice is expected to be reused across repositories that build or maintain generators.
- Versioned distribution is more useful than copying individual files ad hoc.

## Installation intent

Install every file listed in [plugin.json](./plugin.json) under the target repository's `.agents`
layout. Do not install only the agent or only the skill unless you intentionally want an incomplete
experience.

## Compatibility notes

- Assumes `.agents/` is the target layout root.
- Assumes the consumer repository uses C# and Roslyn source generators.
- Keeps packaging metadata separate from the slice source files.

## Example

- [New generator solution example](./examples/new-generator-solution.md)
