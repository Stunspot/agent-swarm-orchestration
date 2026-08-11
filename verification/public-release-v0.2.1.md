# Public release receipt - v0.2.1

Observed on 2026-08-11 after publication and Pages deployment.

## Exact public state

- Repository: https://github.com/Stunspot/agent-swarm-orchestration - unauthenticated HTTP 200
- Public main commit inspected: `2b7792180f4987274b7116524f2d7a6e6b845550`
- Release: https://github.com/Stunspot/agent-swarm-orchestration/releases/tag/v0.2.1 - published, not draft or prerelease, targeting the inspected main commit
- Pages: https://stunspot.github.io/agent-swarm-orchestration/ - GitHub status `built`, source `main:/docs`, HTTPS enforced
- Pages deployment run: https://github.com/Stunspot/agent-swarm-orchestration/actions/runs/31533175523 - success at the inspected main commit
- Line-ending policy run: https://github.com/Stunspot/agent-swarm-orchestration/actions/runs/31533177053 - success at the inspected main commit

## Complete live repository readback

All 19 customer documents declared by `documentation-manifest.json`, `docs/index.html`, `docs/style.css`, and all five public visual assets returned HTTP 200 from public `main`. All 26 downloaded files were SHA-256 identical to the reviewed local files.

The complete live Pages HTML was read. Its product, audience, capabilities, non-capabilities, installation, verification, first-run, workflows, configuration, troubleshooting, cleanup, privacy/security, evidence, support, contribution, license, and terms sections were present. All eight internal navigation fragments resolved to an element ID. All 18 non-fragment links returned HTTP 200; `releases/latest` resolved to v0.2.1.

Live presentation wiring:

- title: `Agent Swarm Orchestration - Parallel cognition, one accountable root`
- Open Graph title: `Agent Swarm Orchestration`
- Open Graph description: `Parallel cognition. One accountable root.`
- Open Graph image: https://stunspot.github.io/agent-swarm-orchestration/assets/aso-social-card.png

## Live visual assets

The final image pixels were reviewed before publication. The deployed/downloaded bytes were then compared with those exact reviewed files:

| Role | Live asset | SHA-256 | Result |
|---|---|---|---|
| README hero | https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/main/docs/assets/aso-readme-banner.png | `9ecb7dfe388499dbe64aad0e3a50c63233a0a2b20f8159d3261e00a1e7a91d23` | exact match |
| Pages hero | https://stunspot.github.io/agent-swarm-orchestration/assets/aso-pages-hero.png | `6f1471f9f73e0a036c434a7c53b7708c7e23a169518f00ec3bd76cc80207b0f3` | exact match |
| Social/Open Graph card | https://stunspot.github.io/agent-swarm-orchestration/assets/aso-social-card.png | `430ada4de217194c5bd54c564f082c9e35a0d6c70c1e5b3b8cf949a70b0a8759` | exact match; exact product title and identifying line are visibly present |
| Plugin icon | https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/main/plugins/agent-swarm-orchestration/assets/aso-icon.png | `8be44db4ba287f4145d7de76ecd3f30fa4bf1b68f7778fe6282edb470704e245` | exact match |
| Plugin listing image | https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/main/plugins/agent-swarm-orchestration/assets/aso-social-card.png | `e0b8e89ecf3ebf020718748a36cbfeea62fbf216e8c8d2723cc8aec2a3fb7071` | exact match |

No screenshot is used as evidence. Pixel judgments are recorded in `verification/visual-review-v0.2.1.json`; live identity is established by exact downloaded-byte equality.

## Public installation

The documented public marketplace commands were exercised in an isolated Codex home:

```text
codex plugin marketplace add Stunspot/agent-swarm-orchestration --ref main --sparse .agents --sparse plugins/agent-swarm-orchestration
codex plugin add agent-swarm-orchestration@cd-agent-swarm-orchestration
codex plugin list
```

Codex 0.144.5 reported `agent-swarm-orchestration@cd-agent-swarm-orchestration` version 0.2.1 as `installed, enabled`. The isolated home was removed and cleanup was verified.

The first disposable attempt used a long workspace-adjacent home and failed before registration because Codex's Windows staging finalization encountered OS error 32: an exclusive handle remained open in `.tmp/marketplaces/...`. Guarded cleanup succeeded. The repair was a short system-temporary Codex home outside the watched workspace; the same public sparse-install command then completed. Codex warned that it would not create PATH aliases under a temporary home, which does not affect plugin installation or enablement.

## Published release assets

All five assets were downloaded from the public v0.2.1 release and hashed:

- `Plugin-Agent-Swarm-Orchestration-v0.2.1.zip`: `2e8d9cae8227735d08290baf132a3a43f435b0e2bad12b7e9add978ec65e9aa9`
- `Skill-agent-swarm-orchestration-v0.2.1.zip`: `53a657c1883949d0c6b1e088f2b850c9973a59428f14e4aa8317a2ae3ae85f94`
- `agent-swarm-orchestration-v0.2.1.zip`: `53a657c1883949d0c6b1e088f2b850c9973a59428f14e4aa8317a2ae3ae85f94`
- `archive-custody.json`: `de6cdbc3826158e32deb9d8113a17c4882c9cde7e05bb6986c1340282aa663ab`
- `checksums.sha256`: `194d598bb71049a2ca2eb0c1fe9e0015ea548e5de0608b725ddb470657fafbdb`

## Evidence boundaries

This receipt establishes public construction, publication, linked-document availability, exact visual-asset deployment, release-asset integrity, Codex marketplace discovery, installation, and enablement for v0.2.1. It does not establish fresh-task invocation, live Claude activation, universal model transfer, assistive-technology conformance, broad collaboration behavior, or customer outcomes.
