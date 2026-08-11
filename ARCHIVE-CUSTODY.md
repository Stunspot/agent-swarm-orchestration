# Agent Swarm Orchestration archive custody

Agent Swarm Orchestration is one single-skill Augment with several channel-specific release objects. A transport object is not a different product, and a successful upload does not prove installation or invocation.

| Object | Canonical release artifact | Use |
|---|---|---|
| Codex marketplace plugin | `release-assets/v0.2.0/Plugin-Agent-Swarm-Orchestration-v0.2.0.zip` | Installable plugin with manifest, listing assets, license pointer, and one skill |
| Standalone skill | `release-assets/v0.2.0/Skill-agent-swarm-orchestration-v0.2.0.zip` | Portable one-skill installation and recovery |
| Claude upload | `claude-ai/agent-swarm-orchestration-v0.2.0.zip` | Byte-matched one-skill upload archive |
| Source repository | Git tag `v0.2.0` and GitHub source archives | Product source, docs, evals, retained verification, and provenance |

`release-assets/v0.2.0/archive-custody.json` records archive hashes, sizes, member counts, source-tree digests, and path rules. `release-assets/v0.2.0/checksums.sha256` is a detached human-readable checksum list.

Every ZIP must use forward-slash member paths, one intended top-level product folder, UTF-8/LF for governed text where canonicalization is applied, and no OS metadata or unrelated build evidence. Extraction parity is checked against the named source tree at release construction.

The version 0.2.0 archives are frozen historical custody objects. Later documentation or presentation changes on `main` do not rewrite those archives. Current validation therefore checks each frozen archive against its recorded SHA-256, size, member count, top-level path, and embedded runtime bytes; it does not require mutable listing artwork on `main` to remain byte-identical to the historical plugin ZIP.

Static parity does not establish marketplace registration, Claude activation, public release availability, or customer first value. Those states require separate destination and host receipts.