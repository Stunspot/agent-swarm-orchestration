# Archive custody and recovery

Version 0.2.2 is a documentation and presentation patch release around the unchanged runtime fingerprint. Frozen v0.2.0 and v0.2.1 archives, checksums, custody JSON, tags, and verification records remain untouched.

| Artifact | Current location | Recovery purpose |
|---|---|---|
| Codex marketplace plugin | `release-assets/v0.2.2/Plugin-Agent-Swarm-Orchestration-v0.2.2.zip` | Installable plugin with corrected listing assets, manifest, license pointer, and one self-contained skill |
| Standalone skill | `release-assets/v0.2.2/Skill-agent-swarm-orchestration-v0.2.2.zip` | Portable one-skill installation and recovery |
| Claude upload | `claude-ai/agent-swarm-orchestration-v0.2.2.zip` | Byte-matched one-skill upload archive |
| Source repository | Git tag `v0.2.2` after publication | Current product source, docs, evals, generated presentation assets, receipts, and provenance |

`release-assets/v0.2.2/archive-custody.json` records archive hashes, sizes, member counts, source-tree digests, and path rules. `release-assets/v0.2.2/checksums.sha256` is the detached human-readable checksum list.

## Verify an archive

From the repository root, compare the downloaded file's SHA-256 digest with the matching line in `release-assets/v0.2.2/checksums.sha256`. Then inspect the archive before extraction:

- every member uses a forward-slash path;
- every member lives under one top-level `agent-swarm-orchestration/` directory;
- `SKILL.md` sits directly inside that directory;
- the expected `agents`, `assets`, `examples`, `references`, `scripts`, and `tests` members are present.

A matching digest verifies exact archive identity. It does not establish installation, discovery, invocation, or healthy behavior.

## Recover or roll back

1. Stop new use of the uncertain installation.
2. Record the installed path, host version, package version, and any local modifications.
3. Reconcile active worker, file, commit, and external-action state separately; package rollback does not undo them.
4. Remove only the exact failed installation folder or plugin registration.
5. Restore a previously verified archive or the immutable `v0.2.1` release when rolling back this presentation repair.
6. Restart or refresh the host, confirm discovery, and run the first-invocation check in `INSTALLATION.md`.

Keep extracted backups outside the active destination. Do not overwrite a locally modified installation until those changes are preserved or intentionally discarded.
