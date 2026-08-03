# Troubleshoot Agent Swarm Orchestration

Version 0.2.0 can arrive through a Codex marketplace plugin, a standalone Codex folder, or a Claude/one-skill archive. Begin with the observable boundary: package bytes, host registration, discovery, invocation, collaboration-tool availability, worker behavior, merge, or external state.

## Marketplace command succeeds but the skill is not recognized

1. Confirm the marketplace source is registered as `Stunspot/agent-swarm-orchestration`.
2. Confirm the installed plugin name is `agent-swarm-orchestration@cd-agent-swarm-orchestration`.
3. Start a fresh task if the host caches plugin discovery.
4. Ask the host to resolve `$agent-swarm-orchestration`.

A successful command return establishes the command result. It does not by itself establish fresh-task discovery.

## Claude upload or folder copy is present but inactive

Confirm that the archive contains one top-level `agent-swarm-orchestration/` folder with `SKILL.md` directly inside it. Follow the current host's reload or upload procedure, then test in a fresh task. Static archive validity does not establish live activation.

Start from the observable symptom. Preserve the package, task transcript, agent returns, and current file state before replacing, deleting, or retrying anything.

## Codex does not recognize the skill name

**Check:** inspect the installed folder shape.

```text
<Codex skill directory>/agent-swarm-orchestration/SKILL.md
```

`SKILL.md` must be directly inside the `agent-swarm-orchestration` folder. A common ZIP mistake is an extra nested folder.

**Then:**

1. Confirm all 17 released files are present.
2. Confirm you copied the release folder or extracted top-level ZIP folder, not the whole product root.
3. Reload Codex or start a fresh task if the host requires discovery at session start.
4. Invoke the exact name `$agent-swarm-orchestration`.

**Safe stopping state:** leave the existing folder intact and record the Codex version, installed path, observed folder shape, and exact response. Clean-host discovery is not established for version 0.1.0, so an unrecognized skill needs host-specific diagnosis rather than repeated copying.

## The skill loads but does not create agents

This can be correct. The skill deliberately chooses direct work when delegation costs more than it adds.

**Check:** ask Codex to state the admission basis briefly. If the task has independent ready slices, also confirm the current task exposes collaboration tools and available slots.

The skill does not create those tools. Exact tool names, schemas, model routes, concurrency, waits, messaging, interruption, and lifecycle behavior come from the live Codex task envelope.

**Recovery:** restate the independent slices, their inputs, read or write surfaces, evidence burden, and merge question. Do not demand agent count as a success measure.

## Agents were dispatched, but work is duplicated or inconsistent

**Check:** compare each worker's objective, source scope, ownership, and downstream consumer.

**Recovery:**

1. Stop adding workers.
2. Preserve useful returns as agent-reported evidence.
3. Give each remaining worker one distinct responsibility.
4. Keep cross-cutting synthesis with the root.
5. Inspect cited evidence before accepting conclusions.

If multiple workers already changed shared state, reconcile current bytes and ownership before any new mutation.

## Two workers touched the same file or mutable surface

**Important:** do not let another writer continue until the authoritative current state is known.

1. Capture the current file bytes, diff, or external-object state.
2. Identify which writes were attempted and which commits can be observed.
3. Preserve both returns and any failure signatures.
4. Select one writer for the next mutation.
5. Integrate accepted changes from reconciled current state.
6. Run the narrowest meaningful verification.

Do not call an interrupted worker rolled back or the surface unchanged without a post-action readback.

## Worker returns conflict

Classify the conflict before choosing a next step:

- factual conflict: compare primary evidence or run a discriminating check;
- scope conflict: compare target, version, environment, and time;
- assumption conflict: find an observation that separates the branches;
- artifact conflict: reconcile bytes, ownership, and integration order;
- recommendation conflict: compare consequences after facts stabilize;
- value or priority conflict: return the decision to the user;
- authority conflict: reserve the affected action until permission is explicit, while continuing independent work that remains authorized.

Do not average incompatible answers or select the most confident worker.

## A worker stalls, fails, or reads the wrong location

Preserve completed independent work. Classify the failed premise, then change the path, context, capability, model, tool, sequence, owner, or verifier before retrying.

Reassign only the unfinished edge. Repeating the same packet with another worker is not recovery.

## A user correction arrives during active work

Update the root mission and authority first. Continue unaffected work, redirect affected workers, and interrupt only work whose objective or authority disappeared.

If any worker may already have written a file or acted externally, inspect authoritative post-state before claiming the correction prevented the action.

## The Swarm Plan validator reports `INVALID`

Run it with exactly one plan path:

```text
python <skill-root>/scripts/validate_swarm_plan.py <swarm-plan.json>
```

The validator prints `INVALID` followed by one or more structural errors and exits with code 1. Repair the named field, dependency, state, or active write collision, then rerun it.

If the command prints usage and exits with code 2, supply exactly one plan path. If Python or the file is unavailable, preserve the plan and report the missing prerequisite instead of calling it valid.

The validator can pass a semantically weak plan. A `VALID cd-agent-swarm-plan/v1` result does not prove good decomposition, sufficient context, truthful returns, or reconciled sequential writes.

## Authority exists, but a source or tool is missing

Do not ask for permission the user already granted. Identify the actual boundary:

- If the host lacks a required tool, execution primitive, or competence, return the exact prepared patch, packet, method, or next executable action as `CAPABILITY-LIMITED`.
- If a required source or artifact was not supplied or observed, complete independent work, name the missing input, and return `PARTIAL — DEPENDENCY UNAVAILABLE`.
- Use `AWAITING AUTHORITY` only when the next consequential action or decision is genuinely ungranted.
- Use `PREPARED — NOT DISPATCHED` when the delegation packet exists but collaboration dispatch is unavailable.

Never describe a source as inspected, a comparison as completed, or content as absent unless the named material was actually observed. In a non-interactive episode, return the strongest usable prepared delta and exact re-entry condition instead of ending with an unanswerable question.

## You cannot safely continue

Use this stop only when no responsible in-bounds move remains. A narrow authority edge blocks the action beyond it, not authorized investigation, analysis, comparison, private preparation, or reporting.

Stop with an exact state such as `RETURNED — NOT RECONCILED`, `PARTIAL — DEPENDENCY UNAVAILABLE`, `AWAITING AUTHORITY`, or `CAPABILITY-LIMITED`. Preserve:

- the user-authorized mission and latest correction;
- worker IDs and dispositions;
- packets and returns;
- paths or external objects touched;
- current observed state;
- commands and outputs;
- unresolved evidence, ownership, and authority;
- the exact condition required to resume.

Send that evidence with the issue details in [Support](SUPPORT.md).
