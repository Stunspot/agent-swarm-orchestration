# Archive custody and recovery

The current same-version 0.3.1 restoration corrects the accepted ownership, capacity, authority, lifecycle, completion and package promises. Previously accepted 0.3.1 and earlier artifacts remain frozen in the source repository; a version number alone cannot distinguish their bytes from this repair.

## Verify what you received

Compare the outer ZIP SHA-256 with the accompanying trusted distributor checksum. The complete kit extracts to agent-swarm-orchestration-v0.3.1 with START-HERE.md at its root. From that root, run:

    python tools/verify_package.py

The verifier checks the complete recorded file set and hashes, portable paths, and the nested Claude/Codex skill equality. The package-custody.json file binds the exact extracted content; the enclosing ZIP hash binds that manifest too. A self-consistent manifest by itself is not publisher authentication.

Standalone skill and Claude archives each use one agent-swarm-orchestration directory with SKILL.md directly inside. The plugin archive adds its plugin wrapper and assets. Never install the whole customer kit as a skill.

## Reproduce from canonical source

Repository maintainers use the canonical skill under canonical/skills/agent-swarm-orchestration. Inspect the source sync plan, then apply only reviewed source changes into the three governed mirrors with tools/sync_runtime_trees.py. This tool preserves its dirty-work guards; it is not permission to overwrite independent destination changes.

After updating the source fingerprint and passing source tests, build into a new repository-local directory:

    python tools/build_candidate.py --output-dir dist/my-reviewed-candidate
    python tools/validate_public_release.py --candidate dist/my-reviewed-candidate

The complete candidate is staged on the destination volume and published only after all channels and the extracted-kit verifier pass. An existing candidate is refused. Sources and archive members with links, junctions, portable-name collisions or unsafe paths are rejected. No historical directory is replaced. Rebuilding identical selected source into another new directory produces identical ZIP bytes.

This is a repository build route; the customer kit intentionally contains runtime and reader support, not the full source/evaluation repository.

## Recover or roll back

Record the installed path, host version, exact package checksum, local modifications and any active worker or external-action state. Package rollback does not undo agent work, commits, deployments or external actions.

Restore a previously verified complete installation from its retained backup, reload the host if required, then follow [Installation](INSTALLATION.md) to check discovery and invocation. Preserve modified local files outside the replacement destination. If state is uncertain, inspect it before retrying.

## Historical evidence

The original v0.2.3 tag and later reconciled v0.2.3 archive bytes remain distinct historical facts. Neither is rewritten by this repair. The original 0.3.0 and 0.3.1 builds, source reviews and receipts retain their original scope. Exact source and artifact hashes for the restoration are recorded with its candidate; none of these static checks implies public publication, installation or healthy behavior.
