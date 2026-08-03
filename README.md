![Agent Swarm Orchestration — parallel cognition without custody loss](docs/assets/aso-readme-banner.png)

# Agent Swarm Orchestration

Agent Swarm Orchestration is a free Collaborative Dynamics Augment for coordinating multiple AI agents without misplacing the mission, authority, evidence, or final judgment somewhere in the group chat.

Its promise is simple: **parallel cognition without custody loss**. One accountable root decides whether a swarm is worth its overhead, gives each worker one coherent responsibility, prevents write collisions, reconciles returned claims against evidence, and delivers one integrated result.

**[Explore the visual project guide →](https://stunspot.github.io/agent-swarm-orchestration/)**

## Get the Codex plugin

```text
codex plugin marketplace add Stunspot/agent-swarm-orchestration
codex plugin add agent-swarm-orchestration@cd-agent-swarm-orchestration
```

Start a fresh Codex task, then invoke `$agent-swarm-orchestration`. The repository also preserves a standalone Codex folder, a byte-matched Claude folder, and one-skill ZIPs for hosts that accept direct skill installation.

The package does not create agent tools. It reads the collaboration controls exposed by the current host and adapts to their live schemas, concurrency, messaging, waiting, interruption, and lifecycle semantics.

## What it helps an agent do

- choose Direct, Enlist, Assemble, Chain, or Recover instead of spawning by reflex;
- map prerequisites, ready work, ownership, budgets, and stop conditions;
- keep deterministic inventory at the root and delegate only work that earns context reconstruction;
- give each worker a bounded packet with exact scope, authority, evidence burden, and return shape;
- reserve one writer for every mutable surface;
- sequence correctness-bearing changes before clarity or polish on shared artifacts;
- keep worker findings `agent-reported` until the root inspects their evidence;
- continue authorized work while reserving only the actual authority edge;
- recover from stale context, failed workers, collisions, corrections, and capability loss without discarding accepted work;
- account for every worker before closure.

It does not expand authority, prove worker claims, guarantee savings, run after the host task ends, or turn five agents into five times the competence. That last trick remains regrettably unavailable from physics.

## The five operating shapes

| Shape | Use it when |
|---|---|
| **Direct** | The root can complete small, sequential, same-surface, or shared-context-heavy work more safely and cheaply. |
| **Enlist** | One bounded worker can return a useful result while the root continues the mission. |
| **Assemble** | Two or more independent, ready slices can run concurrently under separate ownership. |
| **Chain** | One accepted result determines the exact input to the next specialist. |
| **Recover** | Existing work is failed, stale, conflicting, interrupted, or based on a bad premise. |

## Get to first value

Use a task with genuinely independent read surfaces:

```text
Use $agent-swarm-orchestration to inspect billing, search, and notifications for retry behavior. Keep every worker read-only. Decide whether parallel agents earn their coordination cost, give each worker one bounded evidence question, and return one comparison with the riskiest inconsistency. Treat worker findings as reported until you inspect their cited evidence.
```

A correct decision to work directly is not a failure. It is the skill saving you from a tiny bureaucracy with tokens.

## Product and release map

- `canonical/skills/agent-swarm-orchestration/` — maintained runtime source.
- `plugins/agent-swarm-orchestration/` — installable Codex marketplace plugin.
- `release/codex/agent-swarm-orchestration/` — standalone Codex folder.
- `release/claude/agent-swarm-orchestration/` — byte-matched Claude folder.
- `release-assets/v0.2.0/` — governed plugin and standalone release archives.
- `claude-ai/` — one-skill Claude upload archive.
- `canonical/evals/` and `verification/` — retained behavioral cases and evidence.
- `docs/` — tailored GitHub Pages source and visual assets.

## Documentation journey

| Your question | Read |
|---|---|
| Will this help, and what should I try first? | [Start here](START-HERE.md) |
| How do I install, check, remove, or roll back? | [Installation](INSTALLATION.md) |
| How do I use the common orchestration patterns? | [Workflows](WORKFLOWS.md) |
| Why is it not behaving as expected? | [Troubleshooting](TROUBLESHOOTING.md) |
| What may I trust, and what remains untested? | [Trust and limits](TRUST-AND-LIMITS.md) |
| Which host surfaces are packaged? | [Host matrix](host-matrix.md) |
| How is data handled? | [Data and privacy](DATA-AND-PRIVACY.md) |
| What are the use and responsibility boundaries? | [Terms of use](TERMS-OF-USE.md) |
| What should I send for support? | [Support](SUPPORT.md) |
| What changed in the public release? | [0.2.0 release notes](RELEASE-NOTES-v0.2.0.md) |

## Evidence boundary

Version 0.2.0 preserves the verified runtime fingerprint `8833af967b1faf2f1b1b92a5eda54129579a995c91965b73883bc1f8272768b5`. The included validator suite, runtime parity checks, portable ZIP topology, and ten-case Codex decision qualification support the boundaries recorded in [Trust and limits](TRUST-AND-LIMITS.md).

That evidence does not establish universal reliability, universal savings, live behavior on every future host contract, clean installation on every customer machine, Claude activation, accessibility conformance, directory approval, or customer outcomes. Packaging and publication receipts are tracked separately from runtime behavior.

## License

Agent Swarm Orchestration is free to use and redistribute under a split license: MIT for Python software and machine-readable schemas; CC BY-ND 4.0 for original authored Augment material. See [LICENSE.md](LICENSE.md), [ATTRIBUTION.md](ATTRIBUTION.md), and [TRADEMARKS.md](TRADEMARKS.md).

## Publisher

Agent Swarm Orchestration is a Collaborative Dynamics Augment. Issues and contributions are welcome within the boundaries in [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).