# Install Agent Swarm Orchestration

Version 0.3.2 ships one runtime skill through several governed transport surfaces. Choose the surface your host actually supports; do not install the entire repository as though build evidence were runtime cargo.

## Before you begin

You need an AI host that supports Agent Skills or Codex plugins. To create or coordinate agents, the current task must also expose collaboration tools. Python 3 is optional for package and Swarm Plan validation; the runtime instructions themselves require no Python.

Back up an existing `agent-swarm-orchestration` installation before replacing it. Keep the backup outside the destination folder.

## Codex marketplace plugin

```text
codex plugin marketplace add Stunspot/agent-swarm-orchestration --ref main --sparse .agents --sparse plugins/agent-swarm-orchestration
codex plugin add agent-swarm-orchestration@cd-agent-swarm-orchestration
```

Start a fresh task if Codex requires a reload, then invoke `$agent-swarm-orchestration`.

**Observe before claiming success:** plugin registration, skill discovery in a fresh task, and actual application of the topology logic are separate states.

## Standalone Codex folder

Copy the complete folder:

```text
release/codex/agent-swarm-orchestration/
```

to the skill directory used by your Codex installation. In user-level installations that use `%USERPROFILE%\.codex\skills`, the resulting path is:

```text
%USERPROFILE%\.codex\skills\agent-swarm-orchestration\SKILL.md
```

Keep the `agents`, `assets`, `examples`, `references`, `scripts`, and `tests` directories beside `SKILL.md`.

## Claude or another one-skill host

Use the byte-matched folder:

```text
release/claude/agent-swarm-orchestration/
```

or the one-skill archive supplied by the current restored complete kit. Earlier repository and GitHub release archives retain their historical runtime. Preserve the single top-level `agent-swarm-orchestration/` folder and keep `SKILL.md` directly inside it.

Host upload controls, discovery rules, reload behavior, and supported tool contracts can change. The package shape is validated; only an observed upload and fresh invocation establish activation in a particular host.

## Check discovery and first invocation

Start a new task and enter:

```text
Use $agent-swarm-orchestration to decide what temporary organization this task earns: compare three independent folders read-only, identify the distinct contributions and resolver, compile the next phase into a safe execution regime, and return one evidence-backed recommendation with the root responsible for verification.
```

A successful check requires:

1. the host recognizes the named skill;
2. the skill designs causal contributions, relations, authority, state, and resolution, then applies its Direct, Enlist, Assemble, Chain, or Recover execution logic;
3. if agents are needed, the task exposes usable collaboration controls;
4. returned claims remain bounded by evidence.

A Direct result is valid when the task does not justify a swarm.

## Optionally validate a Swarm Plan

From the installed skill root:

```text
python scripts/validate_swarm_plan.py path/to/swarm-plan.json
```

Successful output is:

```text
VALID cd-agent-swarm-plan/v1 — declared structure only
Control: planned; mission outcome: unverified (declared, not independently authenticated)
```

The validator checks declared fields, dependency readiness and cycles, capacity, authority consistency, directory-inclusive write collisions and outcome coverage. [Plan validation](PLAN-VALIDATION.md) explains the exact limits. It does not judge whether the task deserves agents or whether returned claims are true.

## Remove the package

- For the marketplace plugin, use the removal command exposed by your current Codex plugin manager.
- For a folder installation, remove only the exact installed `agent-swarm-orchestration` folder.
- Reload or start a fresh task if the host caches discovery.
- Confirm absence through the host's skill or plugin surface when available.

Removal does not cancel running agents, undo committed changes, or roll back external actions. Reconcile those surfaces separately.

## Roll back

Restore the backed-up folder or reinstall the prior marketplace version, reload the host if required, and confirm the restored `SKILL.md` bytes before resuming work. If copy, removal, or reload state is uncertain, mark installation state `unknown` and inspect the exact destination before another mutation.

## Check the extracted customer kit

From the extracted customer-kit root (where START-HERE.md lives), run:

    python tools/verify_package.py

The verifier compares the recorded file hashes, checks portable paths and compares the nested Claude skill with the Codex runtime. It changes no installation. Its success is exact package evidence, not host activation or model behavior. Keep package-custody.json with the kit and compare the outer ZIP checksum supplied by your trusted distributor before extraction.
