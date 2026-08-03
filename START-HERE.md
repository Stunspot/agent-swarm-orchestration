# Start here: coordinate agents without losing control

Agent Swarm Orchestration helps an AI host decide whether multiple agents will improve a task, divide earned work safely, and return one evidence-bounded result. It is for people who want the benefit of parallel cognition without handing mission, authority, or final judgment to a committee.

Version 0.2.0 is a free public Augment. It packages the same verified runtime as a Codex marketplace plugin, standalone Codex and Claude skill folders, and one-skill release archives. The package does not supply collaboration tools; the current host must expose them.

## Decide whether this fits your task

Use it when the work has at least one of these shapes:

- two or more independent areas can be inspected at the same time;
- one bounded specialist task can run while the root continues useful work;
- one result must be accepted before a dependent specialist begins;
- competing explanations benefit from independent investigation;
- a writer needs a separate, independent reviewer;
- an existing swarm has stalled, conflicted, or been redirected.

Stay with one agent when the task is small, tightly sequential, dependent on shared conversational context, latency-sensitive, or focused on one shared file. The skill is designed to decline unnecessary swarms.

## Install the package that matches your host

- **Codex marketplace plugin:** use the two commands in [Installation](INSTALLATION.md).
- **Standalone Codex:** install `release/codex/agent-swarm-orchestration/`.
- **Claude or another one-skill host:** use `release/claude/agent-swarm-orchestration/` or the matching archive under `claude-ai/`.
- **Source and evidence review:** use the repository, not an installed runtime folder.

Installation files existing on disk do not establish host discovery or activation. Follow the check for your host and record what you actually observe.

## Reach first value

Start a fresh task if your host requires reload after installation. Then use a real task with independent read surfaces:

```text
Use $agent-swarm-orchestration to inspect billing, search, and notifications for retry behavior. Keep every worker read-only. Decide whether parallel agents earn their coordination cost, give each worker one bounded evidence question, and return one comparison with the riskiest inconsistency. Treat worker findings as reported until you inspect their cited evidence.
```

Look for these results:

1. The root selects Direct, Enlist, Assemble, Chain, or Recover for the actual work.
2. Each worker receives a distinct responsibility and explicit authority.
3. Mutable surfaces have one writer at a time.
4. The root reconciles returned claims against cited evidence.
5. You receive one integrated answer with limits, not a stack of worker summaries.

A correct Direct decision is success when parallelism would cost more than it contributes.

## If the first attempt fails

- If the host does not recognize the skill, check the installed folder or plugin registration in [Troubleshooting](TROUBLESHOOTING.md).
- If the skill is recognized but no agents can be created, confirm that the current task exposes collaboration controls.
- If workers returned claims but the root cannot inspect their evidence, keep those claims labeled `agent-reported`.
- If a write or external action may have committed, reconcile authoritative state before retrying.

## Continue the journey

- [README](README.md): product promise, install commands, release map, and evidence boundary.
- [Installation](INSTALLATION.md): Codex, Claude, direct ZIP, removal, and rollback.
- [Workflows](WORKFLOWS.md): practical orchestration patterns.
- [Troubleshooting](TROUBLESHOOTING.md): symptom-led recovery.
- [Trust and limits](TRUST-AND-LIMITS.md): authority, privacy, evidence, validation, and non-claims.
- [Host matrix](host-matrix.md): supplied and untested host surfaces.
- [Data and privacy](DATA-AND-PRIVACY.md): data-handling boundary.
- [Support](SUPPORT.md): useful issue reports and maintenance boundary.
