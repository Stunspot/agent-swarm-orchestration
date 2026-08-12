# Host and distribution matrix

Version 0.2.2 keeps created, packaged, installed, discoverable, invoked, healthy, published, and independently verified as separate evidence states. The runtime bytes and retained behavioral fingerprint are unchanged from 0.1.0; this patch release repairs documentation and presentation custody.

| Surface | Supplied object | Current static state | Live evidence boundary |
|---|---|---|---|
| Codex marketplace | `plugins/agent-swarm-orchestration/` | Plugin manifest, distinct listing image, icon, license pointer, and one self-contained skill are packaged at 0.2.2 | The retained v0.2.1 install observation does not establish installation, discovery, invocation, or health for v0.2.2 |
| Standalone Codex | `release/codex/agent-swarm-orchestration/` and the versioned skill archive | Runtime tree is byte-matched to canonical and packaged under one top-level folder | Existing behavioral qualification is decision-only; universal discovery, invocation, and live tool behavior are not established |
| Claude / one-skill upload | `release/claude/agent-swarm-orchestration/` and `claude-ai/agent-swarm-orchestration-v0.2.2.zip` | Byte-matched skill folder and archive are packaged | Live upload, discovery, invocation, and behavior remain untested until observed in a named Claude host |
| GitHub release | `release-assets/v0.2.2/` | Plugin and skill archives, custody JSON, and checksums are supplied without changing frozen v0.2.0 or v0.2.1 artifacts | Publication and downloaded-byte readback remain not tested until the v0.2.2 release exists |
| GitHub Pages | `docs/` | Complete customer journey, useful navigation, and role-specific visual wiring are supplied | The v0.2.2 deployment, navigation, and public asset bytes remain not tested until publication |

## Presentation surfaces

| Role | Asset | Composition and text contract |
|---|---|---|
| README hero | `docs/assets/aso-readme-banner.png` (1280x640) | Text-free branching topology composed for the repository introduction |
| Pages hero | `docs/assets/aso-pages-hero.png` (1600x900) | Text-free worker-lane convergence composed for the wide landing-page hero |
| Social / Open Graph card | `docs/assets/aso-social-card.png` (1730x909) | Generated frontal-convergence composition with the exact product title and “Parallel cognition without custody loss.” inside the safe area |
| Plugin listing image | `plugins/agent-swarm-orchestration/assets/aso-social-card.png` (1586x992) | Generated top-down topology composition with the exact product title and “Choose the smallest swarm that earns itself.” |

## Runtime dependencies

The skill has no mandatory third-party runtime dependency. Python 3 is required only for the optional Swarm Plan validator.

The package does not include agent-spawning, messaging, waiting, interruption, file, browser, repository, network, or external-action tools. It inspects and uses only the controls exposed by the current host task.

## Tool-contract drift

Host tool names, schemas, concurrency limits, context forks, waiting semantics, interruption behavior, and lifecycle states may change. The skill's source-and-currentness register requires live inspection before relying on a named primitive.

## Evidence vocabulary

- **Created:** bytes or an external object exist.
- **Packaged:** the intended bytes and metadata are assembled into a distribution artifact.
- **Installed:** a package was placed or registered in the host.
- **Discoverable:** the host lists or resolves it.
- **Invoked:** a task actually applied it.
- **Healthy:** the exercised behavior met its acceptance condition.
- **Published:** a public destination exposes it.
- **Verified:** an independent check supports the named claim.

One state does not silently imply the next.
