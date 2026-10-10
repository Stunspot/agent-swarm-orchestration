![Agent Swarm Orchestration — parallel cognition without custody loss](docs/assets/aso-readme-banner.png)

# Agent Swarm Orchestration

Agent Swarm Orchestration is a free Collaborative Dynamics Augment for designing and coordinating the temporary agent organization a task actually needs. It keeps one accountable root responsible for the mission, authority, shared state, integration, and final claim.

Version 0.3.1 retains the organization design introduced in 0.3.0 and adds concise discovery and complete customer installation guidance. The design adds the missing layer above “split the work”: it asks which distinct contributions are causally useful, who should see or challenge whose work, where authority and state live, how conflicts will be resolved, and what evidence should recruit, release, rewire, change phase, or stop the organization. A bucketline, anthill, platoon, boardroom, general staff, complex adaptive system, or unfamiliar hybrid is a source of mechanisms—not a sacred taxonomy handed down by the Department of Tiny Committees.

**[Explore the visual project guide →](https://stunspot.github.io/agent-swarm-orchestration/)**

## Get the Codex plugin

```text
codex plugin marketplace add Stunspot/agent-swarm-orchestration --ref main --sparse .agents --sparse plugins/agent-swarm-orchestration
codex plugin add agent-swarm-orchestration@cd-agent-swarm-orchestration
```

Start a fresh Codex task, then invoke `$agent-swarm-orchestration`. The repository also carries standalone Codex and Claude folders plus one-skill ZIPs for hosts that accept direct skill installation.

The package does not create agent tools. It reads the collaboration controls exposed by the current host and adapts to their live schemas, concurrency, messaging, waiting, interruption, and lifecycle semantics.

## What it helps an agent think about

Before dispatch, the coordinator identifies the next reasoning horizon and asks what has to be produced, which contributions have distinct causal jobs, what information exposure will improve or contaminate them, who may decide or mutate what, where task truth and artifact state live, and what resolver can settle disagreement without inventing an oracle.

Named personas can make a stance memorable or perturb search usefully. They do not establish competence, independence, evidence, or authority. Every admitted contribution still needs a distinct transformation, evidence channel, capability, error opportunity, containment boundary, check, or justified redundancy—and a named consumer.

The organization can change as evidence arrives. It may recruit a new capability, release a completed member, isolate competing hypotheses, expose selected work for critique, switch resolver, move to another execution regime, or dissolve entirely. The form is a working hypothesis, not a pet org chart seeking tenure.

## Execution kernel

Each live phase compiles into one legible control regime:

| Regime | Use it when |
|---|---|
| **Direct** | The root can complete the current horizon more safely and cheaply. |
| **Enlist** | One bounded worker can add a useful contribution while the root continues. |
| **Assemble** | Two or more independent, ready slices can run concurrently under separate ownership. |
| **Chain** | An accepted result must become the next specialist’s exact input. |
| **Recover** | Useful state should survive while a failed premise, route, owner, tool, sequence, or verifier changes. |

These are execution regimes, not the whole design vocabulary. One task may move through several of them; each phase still needs explicit authority, state, evidence, and closure.

## Get to first value

Try a problem where simple parallel inspection is useful:

```text
Use $agent-swarm-orchestration to inspect billing, search, and notifications for retry behavior. Keep every worker read-only. Decide which contributions are actually distinct, whether they should remain independent or cross-review, and what evidence will resolve disagreement. Compile the next phase into the smallest safe execution regime and return one reconciled comparison with the riskiest inconsistency.
```

Or use a problem where deliberation matters:

```text
Use $agent-swarm-orchestration to design a temporary deliberative organization for this messy policy problem. Give each contribution a causal job and evidence burden. Do not treat stakeholder simulation as stakeholder authority. Choose information exposure and a resolver deliberately, adapt the organization when evidence changes the live uncertainty, and return one accountable synthesis with unresolved value conflicts intact.
```

A correct Direct decision is success. So is purposeful redundancy when it has a causal reason, a cap, and a resolver. Headcount is not the unit of intelligence. Sometimes it is merely the unit of catering.

## Product and release map

For current installation, use the maintained runtime folders listed in this product map or the [current restored complete kit](https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/main/release-assets/v0.3.1/restoration-20261010/Agent-Swarm-Orchestration-v0.3.1-restoration-20261010.zip). Check the [ZIP checksum](https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/main/release-assets/v0.3.1/restoration-20261010/Agent-Swarm-Orchestration-v0.3.1-restoration-20261010.zip.sha256). Follow [Installation](INSTALLATION.md) and verify the supplied kit custody. Earlier versioned archives remain available as historical snapshots.

- `canonical/skills/agent-swarm-orchestration/` — maintained 28-file runtime source.
- `plugins/agent-swarm-orchestration/` — Codex marketplace plugin wrapper.
- `release/codex/agent-swarm-orchestration/` — byte-matched standalone Codex folder.
- `release/claude/agent-swarm-orchestration/` — byte-matched Claude folder.
- `release-assets/v0.3.1/restoration-20261010/` — current restored complete kit and its checksum in the public source repository.
- `release-assets/v0.3.1/` — historical 0.3.1 plugin and skill ZIPs, custody, checksums, and verification companions; these retain their original runtime.
- `claude-ai/agent-swarm-orchestration-v0.3.1.zip` — historical one-skill archive matching that original release.
- `canonical/evals/` and `verification/` — bounded qualification contracts and historical evidence.
- `docs/` — GitHub Pages source and visual assets.

## Documentation journey

| Your question | Read |
|---|---|
| Will this help, and what should I try first? | [Start here](START-HERE.md) |
| How do I install, check, remove, or roll back? | [Installation](INSTALLATION.md) |
| How do I design and run common organizations? | [Workflows](WORKFLOWS.md) |
| Why is it not behaving as expected? | [Troubleshooting](TROUBLESHOOTING.md) |
| What may I trust, and what remains untested? | [Trust and limits](TRUST-AND-LIMITS.md) |
| Which host surfaces are packaged? | [Host matrix](host-matrix.md) |
| How is data handled? | [Data and privacy](DATA-AND-PRIVACY.md) |
| What changed? | [0.3.1 release notes](RELEASE-NOTES-v0.3.1.md) |

## Evidence boundary

The current 0.3.1 restoration binds exact runtime bytes in package-manifest.json and package-custody.json. Canonical/plugin/Codex/Claude parity, adversarial plan tests, portable ZIP topology, checksums and documentation links are checked locally. The six earlier organization scenarios remain historical expert review; they are not fresh model execution. New model trials in this repair: zero.

The vNext live-control cases and role-synergy ablations are specified but not run. Prior 0.1.0 and 0.2.3 behavioral evidence does not silently transfer to the new runtime. Local packaging does not establish public publication, clean-host installation, discovery, invocation, Claude activation, universal savings, stakeholder legitimacy, customer outcomes, or superiority over a strong single-agent route. See [Trust and limits](TRUST-AND-LIMITS.md).

## License

Agent Swarm Orchestration is free to use and redistribute under a split license: MIT for Python software and machine-readable schemas; CC BY-ND 4.0 for original authored Augment material. See [LICENSE.md](LICENSE.md), [ATTRIBUTION.md](ATTRIBUTION.md), and [TRADEMARKS.md](TRADEMARKS.md).

Agent Swarm Orchestration is a Collaborative Dynamics Augment. Issues and contributions are welcome within the boundaries in [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).
## Repair and package verification

[Plan validation and recovery](PLAN-VALIDATION.md) distinguishes worker disposal, accepted output and mission acceptance. [Archive custody](ARCHIVE-CUSTODY.md) identifies exact-byte verification and the reproducible source build route.
