# Vertical Slice Architecture plugin bundle

This bundle packages the vertical-slice-architecture slice as one reusable capability pack.

## What ships together

- vertical-slice-architecture agent
- vertical-slice-architecture instruction
- vertical-slice-architecture skill

## Why this is a plugin bundle

- The files form one clear capability bundle around domain-first vertical slice work.
- They are intended to be installed together so planning, standards, and skill routing stay aligned.
- They include shared documentation and a bundle example.
- The slice is expected to be reused across repositories that are migrating away from layer-first
  structures.
- Versioned distribution is more useful than copying one file at a time.

## Installation intent

Install every file listed in [plugin.json](./plugin.json) under the target repository's `.agents`
layout.

## Compatibility notes

- Assumes `.agents/` is the target layout root.
- Assumes the adopting repository wants domain-first structure instead of a generic top-level
  `Features/` folder.

## Example

- [Domain-first layout example](./examples/domain-first-layout.md)
