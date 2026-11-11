# Agent Swarm Orchestration 0.3.2

This patch improves how the skill checks an orchestration plan and recovers when work stops partway through. It ships the same skill as a Codex plugin and a standalone package for Codex, Claude, and other compatible Agent Skills hosts.

- A closed plan now distinguishes finished coordination from a verified result. Accepting a result requires evidence for each acceptance criterion.
- The validator catches overlapping write reservations, including a directory and a file inside it. An interrupted writer keeps its reservation until the lead agent checks what actually changed.
- The plan distinguishes work that never started from work that was interrupted. A closed worker’s accepted output can still be used by the next worker once the required write state is reconciled.
- The validator checks the declared active worker limit and detects permissions listed as both allowed and reserved.

Use the [current installation guide](https://github.com/Stunspot/agent-swarm-orchestration/blob/main/INSTALLATION.md) to choose a package and check discovery. The [kit with updated documentation](https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/main/release-assets/v0.3.2/documentation-20261111/Agent-Swarm-Orchestration-v0.3.2.zip) includes the same skill and plugin as the original release. Use its [matching checksum](https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/main/release-assets/v0.3.2/documentation-20261111/Agent-Swarm-Orchestration-v0.3.2.zip.sha256). The assets attached to the [GitHub release](https://github.com/Stunspot/agent-swarm-orchestration/releases/tag/v0.3.2) are the original release snapshots.

Release checks covered package contents and the plan validator. The release has no fresh model trial or clean-host activation result. See [Trust and limits](https://github.com/Stunspot/agent-swarm-orchestration/blob/main/TRUST-AND-LIMITS.md) for the scope of the evidence.
