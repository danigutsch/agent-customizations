---
description: 'Guidance for gRPC and Protocol Buffers contract design, schema evolution safety, package versioning, and separation of .proto contracts from implementation.'
applyTo: 'README.md, docs/CAPABILITIES.md, .agents/agents/grpc-protobuf-contracts.agent.md, .agents/skills/grpc-protobuf-contracts/**, .agents/instructions/grpc-protobuf-contracts.instructions.md'
---

# Grpc Protobuf Contracts Guidance

Use these rules when the task is about designing or reviewing `.proto` contracts, gRPC service
surfaces, or schema evolution safety.

## Core model

- Treat `.proto` files as the canonical contract surface.
- Keep generated code and service implementation downstream from the contract, not the source of
  truth.
- Design for version skew: clients and servers do not update in lockstep.

## Evolution rules

- Never reuse field numbers.
- Reserve deleted field numbers, field names, and enum values.
- Prefer additive evolution and versioned packages for breaking changes.
- Treat field-type changes, repeated/scalar changes, and enum churn as compatibility-sensitive.

## Service and message design

- Choose unary and streaming RPC shapes deliberately.
- Keep contracts transport-oriented and implementation-independent.
- Prefer well-known protobuf types when they match the domain more clearly than ad hoc fields.
- Keep enum zero values explicit and unspecified by default.

## Package and file structure

- Use stable package naming with explicit version suffixes for public contracts.
- Keep contract files small and reviewable enough to evolve safely.
- Keep language-generation options aligned with the target ecosystems without letting them dominate
  the contract design.

## Verification

- Confirm the guidance protects against field-number reuse and unsafe schema evolution.
- Confirm the contract remains distinct from implementation guidance.
- Confirm versioning and reservation guidance is explicit where relevant.
- Confirm the documented validation path uses existing generation or build flows when available.
