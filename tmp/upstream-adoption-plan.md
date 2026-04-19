# Upstream adoption plan

## Goal

Adopt the highest-value ideas from `github/awesome-copilot`, `Aaronontheweb/dotnet-skills`,
`agent-customizations`, and `ViajantesTurismo` into a reusable model that works for this repository,
for `ViajantesTurismo`, and for future repositories without forcing every repo to carry the same
surface area.

## Principles

- Keep `.agents/` as the canonical source of truth and treat `.github/*` as compatibility mirrors.
- Prefer one clear local validation command and make CI a thin wrapper over it.
- Add visible repository signals only when they map to a real maintained surface.
- Reuse portable capability slices, then add repo-specific overlays only where the target repository
  genuinely differs.

## Best ideas to bring forward

### From awesome-copilot

- Strong README positioning near the top of the repo.
- Better discoverability for capability categories and where to browse them.
- Visible repository signals such as workflow badges once a stable public remote exists.
- Focused validation workflows for high-risk maintained surfaces when one baseline workflow stops
  being enough.

### From dotnet-skills

- Strong packaging and installation guidance for downstream consumers.
- Clear specialist positioning for domain-heavy capabilities.
- Better release-oriented framing when a reusable capability set is mature enough to distribute.

### From this repository

- Canonical-first asset layout under `.agents/`.
- Sync-based compatibility model for `.github/*`.
- Lightweight repo validation through `make check`.
- Cross-surface capability taxonomy in `docs/CAPABILITIES.md`.

### From ViajantesTurismo

- Real downstream pressure from a production-style .NET repository.
- Evidence for which reusable capabilities matter most in a consumer repo:
  source generation, xUnit v3 plus Microsoft.Testing.Platform, API contracts, repository setup,
  package management, and CI guidance.
- A good proving ground for deciding which assets stay generic versus which belong in a
  project-specific repo.

## Rollout plan for this repository

1. Add visible CI status once the public GitHub remote is established.
2. Keep README local-to-CI mapping explicit and concise.
3. Continue filling canonical `.agents/*` surfaces first when a capability already has only a mirror
   or only a skill.
4. Add narrower workflows only when a maintained surface repeatedly breaks outside the baseline
   `make check` path.

## Rollout plan for ViajantesTurismo

1. Start with a small imported capability set:
   `repository-setup`, `ci-workflows`, `xunit-v3-mtp-test-stack`, `source-generation`,
   `aspnet-api-contracts`, and `package-management`.
2. Keep ViajantesTurismo-specific architecture and domain rules in its own repo guidance rather than
   upstreaming them here immediately.
3. Use the repo as a validation target for downstream adoption friction:
   missing instructions, unclear setup steps, test-runner assumptions, and source-generator
   discoverability issues.
4. Upstream only the patterns that prove reusable across more than one consumer repository.

## Rollout plan for future repositories

1. Start with the smallest reusable baseline:
   README guidance, canonical `.agents` assets, local validation command, and one CI workflow.
2. Add specialized capabilities based on actual repository needs instead of importing the full
   catalog.
3. Prefer plugin bundles only after a capability bundle has proven stable and versioned distribution
   matters.
4. Document local adoption choices so downstream repos do not drift into silent forks of the same
   capability.

## Candidate next improvements

- Add a real workflow badge to `README.md` once the remote URL is known.
- Consider a release or packaging path only after more canonical capability surfaces are filled in.
- Add docs that explain how to consume this repository from downstream repos like ViajantesTurismo
  without copying everything.
