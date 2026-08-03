# Support Agent Swarm Orchestration

Use the [GitHub issue tracker](https://github.com/Stunspot/agent-swarm-orchestration/issues) for reproducible product defects, documentation problems, portability issues, and bounded host-compatibility reports.

## Before opening an issue

Read [Troubleshooting](TROUBLESHOOTING.md) and preserve the current package, task transcript, worker returns, and affected artifact state before replacing or retrying anything.

## Include

1. Package version and installation surface: marketplace plugin, Codex folder, Claude folder, or archive.
2. Host name and version.
3. Operating system when relevant.
4. Whether the host discovered the skill in a fresh task.
5. Whether collaboration tools were present, with their observed names or schemas when safe.
6. The smallest synthetic request that reproduces the behavior.
7. Selected topology and expected result.
8. Worker disposition and the evidence level of returned claims.
9. Exact error text or command output.
10. What you attempted after the failure and whether authoritative state was read back.

Remove credentials, access tokens, private customer data, proprietary code outside the authorized scope, and unrelated repository content. Preserve the shape of the failure with synthetic values.

## Security reports

Do not place sensitive vulnerability details in a public issue. Follow [SECURITY.md](SECURITY.md) and request a private reporting route through [Collaborative Dynamics](https://collaborative-dynamics.com).

## Maintenance boundary

Support can diagnose the packaged skill, validator, documentation, and distribution shape. It cannot guarantee third-party host availability, restore external actions, prove that interrupted writes did not commit, or certify every future collaboration-tool contract.

A useful issue ends with one discriminating observation or exact re-entry condition—not a séance around a vanished worker.
