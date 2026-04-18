# New generator solution example

Use the full Source Generation plugin bundle when you want all of these to land together in a
repository:

- a source-generation specialist agent
- source-generation implementation rules
- a discoverable skill entry point
- setup guidance for generator, consumer, and test projects
- testing and CI guidance for lifecycle validation

## Example target shape

```text
.agents/
  agents/
    source-generation.agent.md
  instructions/
    source-generation.instructions.md
  skills/
    source-generation/
      SKILL.md
      references/
        project-setup.md
        testing-and-ci.md
```

## Why install as a bundle

Installing the files together keeps:

- the agent focused on source-generation lifecycle tasks
- the instruction focused on durable constraints
- the skill focused on discovery and routing
- the detailed setup and CI guidance in references instead of bloating the main skill
