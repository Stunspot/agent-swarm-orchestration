# Archive custody and recovery

Version 0.3.0 is a new runtime release candidate, not a wrapper around the earlier 0.1.0 runtime. It adds new archives and leaves prior release assets, tags, checksums, and receipts intact.

| Artifact | Current location | Recovery purpose |
|---|---|---|
| Codex marketplace plugin | `release-assets/v0.3.0/Plugin-Agent-Swarm-Orchestration-v0.3.0.zip` | Plugin wrapper, listing assets, manifest, license pointer, and one self-contained skill |
| Standalone skill | `release-assets/v0.3.0/Skill-agent-swarm-orchestration-v0.3.0.zip` | Portable Codex or Agent Skills installation and downstream edition input |
| Claude upload | `claude-ai/agent-swarm-orchestration-v0.3.0.zip` | Byte-identical one-skill archive for Claude-compatible upload |
| Aggregate custody | `release-assets/v0.3.0/archive-custody.json` and `checksums.sha256` | Archive path, hash, size, member count, source-tree digest, and detached checksum custody |
| Integration companion | `Skill-agent-swarm-orchestration-v0.3.0.zip.sha256` and `Skill-agent-swarm-orchestration-v0.3.0-VERIFY.txt` | Exact identity and cross-platform verification instructions for the edition-selected skill ZIP |
| Source checkpoint | Local release commit named in the handoff packet | Binds the repository state from which the candidate was built; no tag, push, or public release is implied |

## Verify an archive

From `release-assets/v0.3.0`, compare the file's SHA-256 with `checksums.sha256`. For the standalone skill ZIP, the adjacent `.sha256` and `-VERIFY.txt` files provide the same expected digest and PowerShell plus `shasum` commands.

Then inspect the archive:

- every member uses a forward-slash path;
- no member is absolute, duplicated, or escapes through `..`;
- every member lives under one top-level `agent-swarm-orchestration/` directory;
- `SKILL.md` sits directly inside that directory;
- the extracted tree matches the governed source tree exactly.

A matching digest proves exact archive byte identity. It does not establish installation, discovery, invocation, healthy behavior, edition integration, or publication.

## Historical 0.2.3 boundary

The `v0.2.3` Git tag points to its original tagged commit. Later repository reconciliation produced the v0.2.3 archive bytes frozen by the current baseline hashes. Those are distinct custody facts. Version 0.3.0 preserves both; it does not move the tag or rewrite either history into the other.

The frozen baseline remains under `release-assets/v0.2.3/` and `claude-ai/agent-swarm-orchestration-v0.2.3.zip`. Its exact hashes are checked before 0.3.0 acceptance.

## Recover or roll back

Record the installed path, host version, package version, local modifications, and active worker or external-action state. Package rollback does not undo agent work, commits, deployments, or external actions.

Remove only the exact failed installation or plugin registration, then restore a previously verified archive. Reload the host if required, confirm discovery, and run the first-invocation check in `INSTALLATION.md`. Keep extracted backups outside the active destination and preserve local modifications before replacement.