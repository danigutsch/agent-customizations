# Pull request template

## Summary

- Describe the change and the maintenance problem it solves.

## Changed surfaces

- [ ] `.agents/agents/`
- [ ] `.agents/instructions/`
- [ ] `.agents/prompts/`
- [ ] `.agents/skills/`
- [ ] `.agents/hooks/`
- [ ] `.agents/mcp/`
- [ ] `.agents/workflows/`
- [ ] `.agents/plugins/`
- [ ] `.github/` compatibility exports
- [ ] `docs/`
- [ ] `scripts/`

## Validation

- [ ] `make check`
- [ ] Focused command(s) only, with reason:
- [ ] Not run, with reason:

## Compatibility impact

- [ ] No compatibility-path changes
- [ ] Changes `.github/` export behavior
- [ ] Changes user-scope `~/.copilot/` behavior
- [ ] Changes ignore/configuration expectations

## Plugin and version impact

- [ ] No plugin changes
- [ ] Plugin manifest updated
- [ ] Plugin README/examples updated
- [ ] Plugin changelog updated
- [ ] Plugin version bumped

## Checklist

- [ ] Documentation updated where behavior or workflow changed
- [ ] Slice completeness reviewed intentionally
- [ ] Related issue linked, if applicable
