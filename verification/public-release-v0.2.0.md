# Public release receipt — v0.2.0

Observed on 2026-08-03.

## Public surfaces

- Repository: https://github.com/Stunspot/agent-swarm-orchestration — unauthenticated HTTP 200
- Pages: https://stunspot.github.io/agent-swarm-orchestration/ — build `built` at `17ca9cb71a4e457e86f260e94cc630d01abaa76e`, unauthenticated HTTP 200
- Release: https://github.com/Stunspot/agent-swarm-orchestration/releases/tag/v0.2.0 — published, unauthenticated HTTP 200
- README, Pages hero, and social-card assets: unauthenticated HTTP 200
- Marketplace manifest: public raw readback succeeded

## Installation receipt

The following command installed the public marketplace into an isolated `CODEX_HOME`:

```text
codex plugin marketplace add Stunspot/agent-swarm-orchestration --ref main --sparse .agents --sparse plugins/agent-swarm-orchestration
codex plugin add agent-swarm-orchestration@cd-agent-swarm-orchestration
```

Codex then listed `agent-swarm-orchestration@cd-agent-swarm-orchestration` version 0.2.0 as installed and enabled. The disposable installation home was removed and cleanup was verified.

A full-repository marketplace checkout first exposed Windows path-length and finalization failures in Codex's deep staging path. The retained evidence directory was shortened without changing its file bytes, and the customer command now uses Codex's documented sparse checkout so build evidence is not treated as runtime cargo.

## Release custody

- Public main: `17ca9cb71a4e457e86f260e94cc630d01abaa76e`
- Protected v0.2.0 tag: `e027f2ee7a32d51b1d912ff70e8c24f916b03eb8`
- Plugin ZIP SHA-256: `9967e0bf25d54a066ca97f62bb6b154b2a432f379863ac27ebea6f90bffa581f`
- Standalone and Claude ZIP SHA-256: `fc83930051e3df3470c090e5767f87d85dcdf8fcd16ae7508015c7323ce1e3e3`
- Runtime fingerprint: `8833af967b1faf2f1b1b92a5eda54129579a995c91965b73883bc1f8272768b5`
- Hesperos documentation fingerprint: `0b8b1ba1e8e82fc768a459b56028789c986052e7c1611731e734926659a81e8a`

The protected tag anchors the original reviewed release assets. Public marketplace installation follows `main`, whose post-public changes are limited to byte-preserving evidence-path shortening, verified Windows-safe installation guidance, refreshed documentation custody, and this publication receipt. The plugin archive bytes and runtime fingerprint did not change.

## Residual nonclaims

This receipt does not establish fresh-task skill invocation, live Claude activation, OpenAI directory approval, assistive-technology conformance, broad collaboration behavior, or customer outcomes.
