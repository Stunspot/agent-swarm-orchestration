# Agent Swarm Orchestration workflows

These workflows are starting patterns, not fixed recipes. The active host should inspect the current task, authority, evidence, dependencies, write surfaces, live collaboration-tool contract, and total coordination cost before selecting a topology.

Before any dispatch, distinguish skill discovery from tool availability: a host may recognize `$agent-swarm-orchestration` while exposing no agent controls in that task. In that case, complete root-owned work and return the strongest honest prepared result rather than simulating a swarm.

## Decide whether a swarm is worth using

Use this when you want the skill to challenge the premise that more agents are better.

```text
Use $agent-swarm-orchestration to choose the lightest capable topology for this task. Compare direct work, one bounded delegate, independent parallel work, a dependency chain, and recovery against startup, context reconstruction, merge, verification, latency, and token cost. Proceed with the smallest topology that improves the accepted result, and keep final synthesis with the root.

Task: <describe the desired outcome, acceptance, authority, and available evidence>
```

**Done when:** Codex either proceeds directly or names a justified topology, with one accountable root and a clear evidence boundary.

## Inspect independent areas in parallel

Use this for separate repositories, folders, datasets, documents, or hypotheses that can be read without changing one another.

```text
Use $agent-swarm-orchestration to inspect <area A>, <area B>, and <area C> in parallel where the live Codex slots allow it. Keep every worker read-only. Give each worker one bounded question, exact source scope, and required evidence locations. Keep the cross-area comparison with the root. Reconcile the returns against cited sources and deliver one conclusion with conflicts and untested points.
```

**Check before dispatch:** each area has its required input, no worker depends on another worker's unfinished result, and the root has a merge question that can consume all returns.

**Done when:** every worker has a disposition, cited evidence has been inspected to the claimed boundary, and the root returns one comparison.

## Sequence dependent specialists

Use a chain when the next question depends on an accepted earlier result.

```text
Use $agent-swarm-orchestration as a chain. First identify which component owns <behavior> and return source evidence. Inspect and accept that result before giving a second agent the exact component and asking for <dependent deliverable>. Preserve the dependency; do not guess the component to simulate parallelism.
```

**Expected branch:** if the first result is ambiguous, the root resolves the target or returns the ambiguity before dispatching the dependent worker.

## Improve one shared file safely

Two agents may inspect the same file, but they should not edit it concurrently. When the file needs more than one pass, establish technical, factual, schema, security, or policy correctness before clarity, style, formatting, or polish. Each later pass starts from observed, reconciled current bytes.

```text
Use $agent-swarm-orchestration to improve <file> through ordered passes. Keep one writer at a time. First have an independent reviewer inspect technical and factual correctness read-only, then let one writer integrate accepted corrections. Inspect and reconcile the resulting current bytes. Only then review clarity, style, formatting, or polish against that corrected substrate and let one writer integrate accepted improvements. Verify the final result.
```

Alternative: collect separate comment-only recommendations in parallel, then let one integration owner apply accepted changes in correctness-before-presentation order.

**Done when:** one writer owned each mutation, correctness-bearing changes established the substrate, every later writer began from reconciled bytes, the final bytes were inspected, and relevant verification passed. Reviewer prose alone is not proof that the file changed correctly.

## Investigate competing explanations

Use independent contexts when shared anchoring could create false agreement.

```text
Use $agent-swarm-orchestration to investigate why <observable symptom> occurs. Give independent workers the same observation set without revealing a preferred diagnosis. Ask each to produce a testable explanation, contrary evidence, and the cheapest discriminating check. The root will compare sources and compose layered causes where the evidence supports them.
```

**Done when:** the result distinguishes agent reports, root observations, unresolved conflict, and the next discriminating check. Confidence or consensus does not choose the winner.

## Redirect active work after a correction

Tell the root the changed mission, not every worker separately.

```text
Correction: preserve completed evidence, but change the mission to <new outcome>. Authority is now <allowed actions>; <removed actions> are no longer authorized. Update root custody first, continue unaffected work, redirect or interrupt only affected workers, and reconcile any uncertain writes or external actions before claiming the state is safe.
```

Interruption stops current sampling when the live host supports it. It does not prove rollback, non-commit, or unchanged state.

## Continue at a narrow authority edge

One ungranted action does not block the authorized remainder of the mission.

```text
Use $agent-swarm-orchestration to complete every safe, authorized part of this task. Continue the in-bounds investigation, analysis, comparison, and private preparation without asking again for authority already granted. Clearly reserve any publication, deployment, purchase, account change, destructive action, or other ungranted external step. Ask me only when a missing choice or new authority is required for the next consequential move.
```

**Done when:** the root reports the useful authorized result, identifies the exact reserved action, and avoids both unauthorized execution and an unnecessary full-task stop.

## Handle missing inputs or capabilities honestly

Classify the boundary before asking the user for anything:

| Observed boundary | Useful return |
|---|---|
| A new permission or user-reserved decision is genuinely required next | Complete all safe preparation, name the exact requested authority, and use `AWAITING AUTHORITY`. |
| The action is authorized, but the host lacks the required tool, execution primitive, or competence | Return the exact prepared patch, packet, method, or next executable action; name the missing capability; and use `CAPABILITY-LIMITED`. |
| A required source or artifact was not supplied or observed | Complete independent work, name the missing input, avoid claiming the blocked read or comparison occurred, and use `PARTIAL — DEPENDENCY UNAVAILABLE`. |
| Collaboration tools are unavailable but a delegation packet can still be prepared | Return the exact packet as `PREPARED — NOT DISPATCHED`. |

In a non-interactive or tool-limited episode, return the strongest usable prepared result. A question that cannot be answered in that episode is not a recovery path.

```text
Use $agent-swarm-orchestration to classify any blocked step by its actual boundary: authority, source, tool, execution primitive, or capability. Preserve observed work. Represent unavailable inspection as unobserved. When execution is unavailable, return the exact prepared delta and truthful degraded state. Reserve AWAITING AUTHORITY for a genuinely ungranted next action or user decision.
```

## Reconcile conflicting returns

```text
Use $agent-swarm-orchestration to reconcile these worker returns. Classify each conclusion as agent-reported, compare source scope, time, version, assumptions, and artifacts touched, then run or propose the smallest authorized observation that can distinguish the live branches. Preserve unresolved factual conflict and return value or priority conflicts to me.
```

The root may use `assets/merge-ledger.template.md` when several claims, artifacts, or evidence levels need explicit custody.

## Recover a failed worker without restarting accepted work

```text
Recover this swarm from the first unearned edge. Preserve accepted work and the failure signature. Classify whether the failure came from context, target path, missing source, capability, tool, dependency timing, ownership, authority, evidence, cost, or user correction. Change that premise before reassigning only the unfinished slice. Return an exact prepared delta when execution is unavailable, use the truthful degraded state, account for all workers, and return one bounded result.
```

Useful degraded states include `PREPARED — NOT DISPATCHED`, `RETURNED — NOT RECONCILED`, `PARTIAL — DEPENDENCY UNAVAILABLE`, `AWAITING AUTHORITY`, `CAPABILITY-LIMITED`, and `CANCELLED`. The label identifies the boundary; it does not replace the prepared work or missing-dependency detail.

## Use the included planning artifacts

For consequential, multi-turn, or recovery-prone work:

1. Start from `assets/swarm-plan.template.json` and keep one working copy outside the installed package.
2. Use `assets/delegation-packet.template.md` for each worker's objective, scope, authority, evidence, and return contract.
3. Ask workers to return the fields in `assets/agent-return.template.md` or an equivalent compact shape.
4. Use `assets/merge-ledger.template.md` when claims or shared state can conflict.
5. Validate the plan structure with the packaged script, then manually judge semantic quality and reconciled state.
