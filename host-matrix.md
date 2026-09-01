# Host and distribution matrix

Version 0.3.0 keeps created, packaged, checkpointed, installed, discoverable, invoked, healthy, integrated, published, and independently verified as separate states. The local release candidate carries the new 26-file organization-design runtime; earlier 0.1.0/0.2.3 behavioral evidence does not transfer to it.

| Surface | Supplied object | Current static state | Live evidence boundary |
|---|---|---|---|
| Codex marketplace | `plugins/agent-swarm-orchestration/` | Plugin manifest, listing image, icon, license pointer, and one self-contained 0.3.0 skill; registered by `.agents/plugins/marketplace.json` | Local packaging does not establish marketplace publication, installation, discovery, invocation, or health |
| Standalone Codex | `release/codex/agent-swarm-orchestration/` and `release-assets/v0.3.0/Skill-agent-swarm-orchestration-v0.3.0.zip` | Runtime tree is byte-matched to canonical and packaged under one top-level folder | Host discovery, routing, collaboration-tool execution, and useful behavior require separate observation |
| Claude / one-skill upload | `release/claude/agent-swarm-orchestration/` and `claude-ai/agent-swarm-orchestration-v0.3.0.zip` | Byte-matched skill folder and archive; archive bytes match the standalone skill ZIP | Upload, discovery, invocation, and behavior remain untested until observed in a named Claude host |
| Local release custody | `release-assets/v0.3.0/` | Plugin and skill archives, custody JSON, aggregate checksums, skill-ZIP checksum sidecar, and verification instructions | A matching digest establishes byte identity only |
| GitHub release | No 0.3.0 release object is claimed by this local candidate | Prepared source and archives may support a later authorized release | Tagging, push, publication, and downloaded-byte readback are separate external actions |
| GitHub Pages | `docs/` | 0.3.0 product language, reader journey, navigation, and retained visuals are supplied | Deployment, public navigation, and public asset bytes require live observation after publication |
| Nova Free / Nova Emergent | Immutable component packet handed to the edition owner | Integration is a downstream edition transaction, not a component-repository side effect | Edition catalogs, copied trees, rebuilt packages, and final ZIPs require edition-owned verification |

## Presentation surfaces

| Role | Asset | Contract |
|---|---|---|
| README hero | `docs/assets/aso-readme-banner.png` (1280×640) | Text-free branching topology for the repository introduction |
| Pages hero | `docs/assets/aso-pages-hero.png` (1600×900) | Text-free worker-lane convergence for the landing page |
| Social / Open Graph card | `docs/assets/aso-social-card.jpg` (1730×909) | Existing product title and “Parallel cognition. One accountable root.” |
| Plugin listing image | `plugins/agent-swarm-orchestration/assets/aso-social-card.png` (1586×992) | Existing product title and “Choose the smallest swarm that earns itself.” |

The 0.3.0 release retains these reviewed bytes rather than pretending every semantic improvement demands another bee portrait.

## Runtime dependencies and tool drift

The skill has no mandatory third-party runtime dependency. Python 3 is required only for the optional Swarm Plan validator. It includes no agent-spawning, messaging, waiting, interruption, file, browser, network, or external-action tools; it uses only the controls exposed by the current host.

Host tool names, schemas, concurrency limits, context forks, waiting semantics, interruption behavior, and lifecycle states may change. The skill's source-and-currentness register requires live inspection before relying on a named primitive.

## Evidence vocabulary

**Created** means bytes or an object exist. **Packaged** means intended bytes and metadata were assembled. **Checkpointed** means a local commit binds repository state. **Installed** means a package was placed or registered. **Discoverable** means the host resolves it. **Invoked** means a task applied it. **Healthy** means exercised behavior met acceptance. **Integrated** means an edition selected and rebuilt it. **Published** means a public destination exposes it. **Verified** means a separate credible check supports the named predicate.

One state does not silently imply the next.