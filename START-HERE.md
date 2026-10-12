# Start here: design the organization the work needs

Agent Swarm Orchestration helps an AI coordinator decide not only whether multiple agents will help, but what temporary organization can improve the accepted result. It separates memorable role names from actual contributions, designs information and authority relations deliberately, compiles the next phase into a safe execution regime, and changes the form when evidence changes the problem.

Version 0.3.2 is packaged as a Codex marketplace plugin, standalone Codex and Claude skill folders, and one-skill archives. The package does not supply collaboration tools; the current host must expose them.

## Decide whether this fits your task

Use it when work benefits from one or more of these mechanisms:

- independent evidence gathering without shared anchoring;
- distinct transformations that can proceed concurrently;
- dependent specialists whose inputs must be accepted in sequence;
- structured disagreement, cross-review, or bounded deliberation;
- purposeful redundancy with an explicit resolver;
- changing membership or information exposure as uncertainty moves;
- recovery that preserves accepted evidence and resumes from the first unearned edge.

Stay with one agent when the next horizon is small, tightly sequential, shared-context-heavy, latency-sensitive, or concentrated on one mutable surface. The skill is designed to decline unnecessary organizations as cheerfully as it designs useful ones.

## Think in contributions, not costumes

For the next reasoning horizon, identify the product of the phase, the contributions that can cause it, their consumers, dependencies, evidence burdens, error opportunities, information exposure, authority, state custody, resolver, and transition signal.

A role label such as “critic,” “stakeholder,” or “review bot” may help a model hold a stance. It does not prove competence, independence, legitimacy, or useful difference. An agent simulating residents is not authorized to speak for residents. Stakeholder evidence and stakeholder standing remain separate.

## Install the package that matches your host

- **Codex marketplace plugin:** use the commands in [Installation](INSTALLATION.md).
- **Standalone Codex:** install `release/codex/agent-swarm-orchestration/` or the versioned skill ZIP.
- **Claude or another one-skill host:** use the current matched `release/claude/agent-swarm-orchestration/` folder or the current complete kit’s supplied one-skill archive. Earlier repository and GitHub release archives retain their historical runtime.
- **Source and evidence review:** use the repository, not an installed runtime folder.

Files existing on disk do not establish discovery or activation. Confirm what the named host actually loads.

## Reach first value

Start a fresh task if your host requires reload after installation, then try:

```text
Use $agent-swarm-orchestration to compare retry handling in billing, search, and notifications. Keep mutations out of scope. Identify the distinct causal contributions, decide whether independence or cross-review is useful, name the resolver, and compile only the next phase into the lightest safe execution regime. Reconcile cited evidence into one answer.
```

A good run should make four things legible: why each contribution exists, what each member may see and do, how disagreement or overlap will be resolved, and what observation will change or end the organization. It should then return one integrated result—not a hamper of worker summaries tied with ribbon.

## If the first attempt fails

If the host does not recognize the skill, check the installed folder or plugin registration in [Troubleshooting](TROUBLESHOOTING.md). If the skill is recognized but agent controls are unavailable, work directly or return an exact delegation packet marked `PREPARED — NOT DISPATCHED`. If a worker returns claims the root cannot inspect, keep them `agent-reported`. If a write may have landed, read authoritative state before retrying.

Continue with [Workflows](WORKFLOWS.md), [Trust and limits](TRUST-AND-LIMITS.md), and the [host matrix](host-matrix.md).

## Validate a plan or resume stopped work

Use [Plan validation and recovery](PLAN-VALIDATION.md) for exact state meanings, commands, accepted-output handoffs and partial completion. A closed worker is disposed; a closed plan can still be partial or unverified.
