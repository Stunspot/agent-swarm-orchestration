# Host and distribution matrix

Version 0.2.0 keeps package presence, installation, discovery, invocation, tool availability, and healthy behavior as separate evidence states.

| Surface | Supplied object | Static package state | Live state established by this release |
|---|---|---|---|
| Codex marketplace | `plugins/agent-swarm-orchestration/` | Plugin manifest, listing assets, and one self-contained skill are packaged | Publication and install readback are release gates; broad customer activation is not established |
| Standalone Codex | `release/codex/agent-swarm-orchestration/` | Runtime tree preserved and validated | Existing qualification is decision-only; universal live tool behavior is not established |
| Claude / one-skill upload | `release/claude/agent-swarm-orchestration/` and `claude-ai/` | Byte-matched skill folder and archive are packaged | Live upload, discovery, and invocation remain untested until observed |
| GitHub release | `release-assets/v0.2.0/` | Governed archives and checksums are generated during release | Asset publication and download readback require separate receipts |
| GitHub Pages | `docs/` | Accessible static source, 1600×900 hero, and 1200×630 share card are supplied | Deployment and public URL readback require separate receipts |

## Runtime dependencies

The skill has no mandatory third-party runtime dependency. Python 3 is required only for the optional Swarm Plan validator.

The package does not include agent-spawning, messaging, waiting, interruption, file, browser, repository, network, or external-action tools. It inspects and uses only the controls exposed by the current host task.

## Tool-contract drift

Host tool names, schemas, concurrency limits, context forks, waiting semantics, interruption behavior, and lifecycle states may change. The skill's source-and-currentness register requires live inspection before relying on a named primitive.

## Evidence vocabulary

- **Created:** bytes or an external object exist.
- **Installed:** a package was placed or registered in the host.
- **Discoverable:** the host lists or resolves it.
- **Invoked:** a task actually applied it.
- **Healthy:** the exercised behavior met its acceptance condition.
- **Published:** a public destination exposes it.
- **Verified:** an independent check supports the named claim.

One state does not silently imply the next.
