# Support and maintenance

Collaborative Dynamics owns Agent Swarm Orchestration 0.1.0. Use the channel that supplied your package to contact the owner; this release does not include a separate support address or service-level commitment.

## Before requesting support

Check these pages first:

- [Installation](INSTALLATION.md) for folder shape, discovery checks, removal, and rollback;
- [Troubleshooting](TROUBLESHOOTING.md) for failed recognition, missing tools, collisions, conflicts, and recovery;
- [Trust and limits](TRUST-AND-LIMITS.md) for the difference between package evidence and live-host evidence;
- [Host matrix](host-matrix.md) for the supported target and untested states.

## Send a useful issue report

Include the smallest evidence packet that can reproduce or classify the problem:

1. Product name and version: Agent Swarm Orchestration 0.1.0.
2. Codex version or build identifier, operating system, and task date.
3. Installation source: released folder or ZIP.
4. Exact installed folder path and whether `SKILL.md` is directly inside it.
5. Whether the symptom concerns installation, discovery, invocation, agent tools, orchestration behavior, the plan validator, shared-state mutation, or documentation.
6. The exact request with secrets and personal data removed.
7. The observed response, error, or validator output.
8. Worker IDs, dispositions, and affected paths or external objects.
9. What you expected and what evidence would establish recovery.
10. Any local modifications to the package.

Do not send credentials, access tokens, private customer data, or unrelated repository content. Replace sensitive values while preserving the shape of the failure.

## Preserve evidence before recovery

Keep copies of the relevant plan, packets, returns, merge ledger, task transcript, commands, outputs, current file hashes or diffs, and the exact package bytes. If a write or external action may have committed, record the authoritative post-state before retrying.

Mark uncertain states as unknown. Do not describe a task as rolled back, unchanged, healthy, or recovered without the corresponding observation.

## Maintenance triggers

Customer documentation and runtime guidance should be reviewed when any of these change:

- Codex skill discovery or installation behavior;
- collaboration tool names, schemas, concurrency, waiting, messaging, interruption, or cancellation;
- package files, paths, templates, schema, validator, or tests;
- the supported host or product promise;
- authority, privacy, or data-handling policy;
- recurring support symptoms or failed customer tasks;
- verification evidence or a known limit.

Because host contracts are volatile, re-check the current Codex task envelope before relying on exact collaboration primitives.

## Updates and retirement

Preserve a known-good package before replacing version 0.1.0. Treat a new folder, successful copy, host discovery, invocation, healthy behavior, publication, and customer validation as separate states.

If the product is retired, remove only the installed skill folder, preserve customer-created work elsewhere, and retain evidence needed to explain prior decisions. Removal does not stop existing workers or undo their effects; reconcile those separately.

