![Agent Swarm Orchestration](docs/assets/aso-readme-banner.png)

# Agent Swarm Orchestration

Agent Swarm Orchestration is a free Collaborative Dynamics skill that helps an AI assistant decide when to delegate, give each worker a useful job, and turn their findings into one checked result. The lead agent (the **root**) stays responsible for your request, permissions, shared work, and final answer.

The same skill ships as a **Codex plugin** through this repository's marketplace and as a **standalone skill** for Codex, Claude, and other hosts that support Agent Skills. The plugin packages the skill for installation. Your host supplies any tools the assistant uses to start or coordinate workers.

[Choose an installation method](INSTALLATION.md) · [Try your first task](START-HERE.md) · [Explore the visual guide](https://stunspot.github.io/agent-swarm-orchestration/)

## Install version 0.3.2

- **Codex plugin:** [Install from this repository's marketplace](INSTALLATION.md#install-the-codex-plugin). You can also register the marketplace included in the downloaded kit.
- **Standalone Codex skill:** [Copy the skill into a Codex skills directory](INSTALLATION.md#install-the-standalone-skill-in-codex).
- **Claude or another Agent Skills host:** [Install the one-skill ZIP using your host's skill installer](INSTALLATION.md#install-the-skill-in-claude-or-another-host).

The [complete 0.3.2 kit](https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/main/release-assets/v0.3.2/documentation-20261111/Agent-Swarm-Orchestration-v0.3.2.zip) includes the Codex marketplace, the standalone skill, the Claude ZIP, and the updated guides. Its [SHA-256 checksum](https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/main/release-assets/v0.3.2/documentation-20261111/Agent-Swarm-Orchestration-v0.3.2.zip.sha256) lets you check the download before extracting it.

## What it helps you do

- Compare findings from independent sources before the workers see each other's conclusions.
- Pass a checked result to the next specialist when the work has to happen in order.
- Decide who may edit which files and who resolves conflicting findings.
- Keep verified progress when a worker fails, then resume from the first unfinished step.

Working directly is a valid result. The skill weighs whether delegation will improve the answer enough to justify the extra time and coordination.

## Try a read-only comparison

In a new Codex CLI or IDE task with three relevant folders, enter:

```text
Use $agent-swarm-orchestration to compare how billing, search, and notifications handle retries. Keep the work read-only. Decide which parts, if any, to delegate. Check conflicting findings against the source and return one comparison with the biggest risk.
```

Expect one comparison with source references, a brief reason for how the work was divided, and any unresolved differences. [Start here](START-HERE.md) walks through this example and what to do if your host cannot start workers.

## Guides and release evidence

| I want to… | Read |
|---|---|
| Plan parallel work, handoffs, or independent review | [Workflows](WORKFLOWS.md) |
| Fix a missing skill, stalled worker, or uncertain write | [Troubleshooting](TROUBLESHOOTING.md) |
| Validate a plan or resume stopped work | [Plan validation and recovery](PLAN-VALIDATION.md) |
| Check host options or verify a download | [Host matrix](host-matrix.md) and [Archive custody](ARCHIVE-CUSTODY.md) |
| Understand privacy and what the tests establish | [Data and privacy](DATA-AND-PRIVACY.md) and [Trust and limits](TRUST-AND-LIMITS.md) |
| See what changed in 0.3.2 | [0.3.2 release notes](RELEASE-NOTES-v0.3.2.md) |

The 0.3.2 checks cover package contents, matching skill files across distributions, and the plan validator. The release has no fresh model trial or clean-host activation result. [Trust and limits](TRUST-AND-LIMITS.md) describes the evidence and its scope.

The [maintained skill source](https://github.com/Stunspot/agent-swarm-orchestration/tree/main/canonical/skills/agent-swarm-orchestration) and [versioned release files](https://github.com/Stunspot/agent-swarm-orchestration/releases) are available on GitHub.

## License and support

Python software and machine-readable schemas use MIT. Original authored Augment material uses CC BY-ND 4.0. See the [license](LICENSE.md), [attribution](ATTRIBUTION.md), and [trademarks](TRADEMARKS.md).

See [Support](SUPPORT.md) for reporting a problem and [Security](SECURITY.md) for sensitive reports.
