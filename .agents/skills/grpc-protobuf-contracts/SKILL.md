---
name: grpc-protobuf-contracts
description: Guidance for gRPC and Protocol Buffers contract design. Use when reviewing .proto schemas, field numbering, reserved tags or names, package versioning, unary versus streaming RPC shape, or keeping generated code and service implementation separate from the canonical contract.
---

# Grpc Protobuf Contracts

Use this skill when the task is about `.proto` schemas and gRPC contract design rather than general
service implementation.

## When to Use This Skill

- The user wants to design or review a `.proto` contract
- The user needs help with field numbering, reserved tags, enum evolution, or package versioning
- The user needs to decide between unary and streaming RPC shapes
- The user wants to keep generated code and service implementation separate from the canonical
  contract
- The user is planning a breaking change and needs to know whether versioning is safer than mutation

## Prerequisites

- The `.proto` files or intended contract surface can be inspected.
- The consumers or services of the contract are known well enough to reason about compatibility.
- The task is about contract design, not only server implementation.

## Workflow

### 1. Identify the contract boundary

- List the services, messages, enums, and packages that define the public surface.
- Treat `.proto` files as the source of truth for the contract.

### 2. Review evolution safety

- Check field numbers, reserved tags, reserved names, and enum defaults.
- Prefer additive changes and versioned packages over in-place breaking edits.

### 3. Review service shape

- Decide whether RPCs should be unary, client-streaming, server-streaming, or bidirectional.
- Keep the contract centered on network interaction rather than internal implementation flow.

### 4. Protect separation of concerns

- Keep generated code downstream from the contract.
- Keep server-specific behavior and business logic out of the contract layer.

## Related guidance

- Pair with [CI Workflows](../ci-workflows/SKILL.md) when generation or compatibility checks need
  pipeline wiring.
- Pair with [Repository Setup](../repository-setup/SKILL.md) when contract folder layout or ownership
  needs clarification.

## Gotchas

- **Do not reuse field numbers or deleted enum values.**
- **Do not assume simultaneous client and server rollout makes breaking changes safe.**
- **Do not let generated code become the contract source of truth.**
- **Do not bury breaking changes in a package that should have been versioned.**

## References

- [Grpc protobuf contracts guidance](../../instructions/grpc-protobuf-contracts.instructions.md)
- [Grpc protobuf contracts agent](../../agents/grpc-protobuf-contracts.agent.md)
