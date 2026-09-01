# Agent Swarm Orchestration 0.3.0 — local release state

**State:** public-release-candidate, locally built and checkpointed
**Date:** 2026-09-01
**Runtime fingerprint:** `ec4fd5afdee16512cb1561639521844d07a11300975633447766e419bc8886ca`

Version 0.3.0 completes the organization-design upgrade described in `agent-swarm-orchestration-vnext-organization-architecture.md`. The canonical 26-file runtime is mirrored exactly into the Codex plugin, standalone Codex, and standalone Claude trees.

The deterministic release builder produces the governed plugin ZIP, standalone skill ZIP, byte-identical Claude ZIP, archive-custody JSON, aggregate checksums, and the edition-selected skill ZIP's checksum and verification companions under the versioned 0.3.0 paths.

Acceptance requires the existing public-release and documentation validators, Skill Creator structural validation, runtime parity, vNext eval-contract validation, relevant repository/runtime tests, diff hygiene, and frozen v0.2.3 baseline hashes to pass. Exact command results, ZIP digests, source file count/tree digest, and the local release commit are recorded in the external edition handoff packet after the checkpoint is created.

The vNext live-control cases and role-synergy ablations remain specified but not run. Prior runtime behavior does not transfer to this fingerprint. No clean-host installation, discovery, invocation, Claude activation, tag, push, GitHub release publication, Pages deployment, retail-shelf replacement, or public readback is claimed by this local transaction.

Historical `verification/v0.3.0-dev/` remains the pre-release source-development record. Frozen v0.2.3 assets and receipts remain unchanged; its tag and later reconciled baseline bytes are preserved as distinct custody facts.