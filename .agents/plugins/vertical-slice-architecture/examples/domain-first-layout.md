# Domain-first layout example

Use the full Vertical Slice Architecture plugin bundle when you want all of these to land together
in a repository:

- a vertical-slice specialist agent
- reusable rules for domain-first slice ownership
- a discoverable skill entry point for migration and review work

## Example target shape

```text
.agents/
  agents/
    vertical-slice-architecture.agent.md
  instructions/
    vertical-slice-architecture.instructions.md
  skills/
    vertical-slice-architecture/
      SKILL.md
```

## Example application shape

```text
src/
  Sales/
    CreateOrder/
    CancelOrder/
  Catalog/
    GetProduct/
  Identity/
    RegisterUser/
```

The bundle exists to reinforce domain-first ownership and keep the three customization surfaces in
sync.
