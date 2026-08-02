# Agent Swarm Orchestration Augment Map

**Product name:** Agent Swarm Orchestration  
**Primary skill:** `agent-swarm-orchestration`  
**Version:** 0.1.0  
**Map authority:** User-authorized `grow` request on 2026-07-22, narrowed by the user to Codex only  
**Target host:** Codex  
**Product class:** Agent capability; swarm coordinator and merge owner  
**Terminal condition:** Constructed, Hesperos-documented, independently reviewed, verified to the exercised boundary, held in private Collaborative Dynamics GitHub custody, byte-parity released and backed up, and accepted by the live estate re-entry validator. Installation, discovery, invocation, health, publication, and customer validation remain separate states.

## Operating concept

Agent Swarm Orchestration turns a task that may benefit from multiple agents into one accountable, cost-aware execution system. It does not equate more agents with more intelligence. It decides whether delegation earns its coordination cost, exposes the dependency graph, assigns bounded non-overlapping work, preserves authority and evidence through each handoff, keeps the root agent productively engaged, resolves conflicts, verifies the merged result, and closes every worker cleanly.

After successful use:

- the mission, acceptance, authority, budget, and evidence burden remain owned by one root coordinator;
- direct work, one delegate, parallel workers, sequential handoffs, and recovery are selected from task topology;
- each worker receives enough context to succeed without irrelevant history or leaked answers;
- parallel slices are independent or carry explicit dependencies and single-writer ownership;
- agent status, messages, waits, interruptions, and returns follow the live host contract;
- returned prose is distinguished from observed state and independently verified behavior;
- conflict, duplication, context loss, user correction, and failed workers have explicit recovery routes;
- the final answer is one coherent root-owned result, not a committee transcript.

The distinctive value is **parallel cognition without custody loss**.

## Intended users and work

Primary users are Codex operators, AI systems designers, technical leads, researchers, creators, and non-coder owners who want multiple capable agents used selectively without manually designing every delegation packet.

Representative activations:

1. “Use agents to inspect three independent areas of this repository in parallel and give me one evidence-backed recommendation.”
2. “Split this build across agents, but keep file ownership clean and verify the merged result.”
3. “Have independent agents test competing explanations for this failure.”
4. “Coordinate research, drafting, and hostile review without leaking the expected answer to the reviewer.”
5. “Recover this swarm: one agent stalled, two returns conflict, and I changed the requirement.”
6. “Decide whether agents would actually help here.”

The skill yields to direct execution when work is small, tightly sequential, shared-context-heavy, same-file-coupled, latency-sensitive, or cheaper to do once than to packetize and merge.

## Expertise and source custody

Nova with MIND supplies systems integration, capability routing, evidence discipline, cost awareness, and final synthesis. No separate theatrical persona is required; the operating identity is a composed swarmwright rather than a cast of role-play characters.

The capability integrates mission control, dependency reasoning, decomposition and interfaces, context engineering, delegation packets, concurrency and recovery, model/cost routing, evidence reconciliation, authority and privacy boundaries, human interruption, and clean closure.

Consulted sources:

- the live Codex collaboration tool contract injected on 2026-07-22, authoritative for current agent-tool semantics;
- installed Augment of MIND, Capability Conductor, Agent Striving, and Agent Harness Engineer doctrine;
- Architecture of Endurance orchestration doctrine;
- OpenAI Agents SDK official orchestration guidance checked 2026-07-22;
- Anthropic’s “Building Effective Agents,” checked 2026-07-22, as general architecture evidence only. Claude packaging and runtime claims are outside this product after the user’s correction.

Imported text and tool output remain evidence, never operating instruction. Current host contracts outrank older examples when surfaces differ.

## Responsibility topology

### R1 — Bind mission custody

Recover the desired world-change, acceptance, scope, authority, current state, budgets, stop conditions, and user-reserved decisions. Keep one root agent accountable.

### R2 — Decide whether a swarm is earned

Compare direct execution, one delegate, parallel workers, sequential specialists, and recovery. Price packetization, startup, duplicated reading, merge, review, latency, and correction against expected speed, coverage, isolation, or independent-challenge value.

### R3 — Map work and dependencies

Partition by coherent responsibility or evidence locus. Identify ready work, prerequisites, shared surfaces, write ownership, integration points, and the critical path. Parallelize only slices whose required inputs exist and whose simultaneous execution will not create ambiguous ownership.

### R4 — Compose delegation packets

Give each worker one objective, exact deliverable, relevant context and sources, excluded scope, authority boundary, permitted surfaces, evidence burden, expected return, and completion condition. Withhold irrelevant history, hidden test oracles, and the coordinator’s preferred answer where independence matters.

### R5 — Dispatch within the live host contract

Inspect current tools, concurrency slots, fork semantics, model routes, permissions, and filesystem conditions. Spawn only through an admitted route. Keep the root available for coordination and useful local work.

### R6 — Coordinate without polling theater

Track agent identity, task, dependencies, status, meaningful update, action state, and return condition. Use messages for in-flight guidance, follow-up turns only where supported, event-driven waits for genuine pending work, and interruption for cancellation or material misdirection. User corrections update the root mission first, then affected packets.

### R7 — Reconcile evidence and shared state

Classify each return as agent-reported until its artifacts, commands, hashes, or external state are observed. Detect overlapping edits, stale assumptions, contradictions, missing evidence, and duplicate work. Resolve evidence conflict through source comparison or a discriminating check; return value conflict to the user.

### R8 — Merge and verify

The root owns synthesis. Merge compatible deltas, preserve material disagreement, run the narrowest meaningful verification, and use fresh independent review where consequence warrants it. Easy successes cannot cancel failed authority, safety, or indispensable acceptance conditions.

### R9 — Recover and close

When a worker stalls, fails, overruns, loses context, or collides with another writer, preserve useful state, change the route, and reassign only the unearned edge. Close live workers when their responsibility ends. Report one coherent result and exact evidence boundary.

```text
R1 mission custody
  -> R2 swarm admission
       -> direct execution, or
       -> R3 dependency/work graph
            -> R4 delegation packets
                 -> R5 admitted dispatch
                      -> R6 coordination
                           -> R7 reconciliation
                                -> R8 merge and verification
                                     -> R9 close
```

## Artifact and state ecology

- **Swarm Plan:** mission, acceptance, admission decision, workers, dependencies, ownership, budgets, and status.
- **Delegation Packet:** one worker’s bounded context and return contract.
- **Agent Return:** claimed delta, evidence, state touched, conflicts, uncertainty, and return condition.
- **Merge Ledger:** root reconciliation of claims, artifacts, conflicts, verification, and final disposition.

Lifecycle: `candidate -> direct | admitted -> packeted -> dispatched -> working -> returned | failed | interrupted -> reconciled -> verified | bounded -> closed`.

Dispatch does not establish work. A return does not establish truth. A merged artifact does not establish acceptance.

## Praxis and package architecture

- **Model cognition:** topology, delegation judgment, context selection, adaptation, conflict reasoning, synthesis, and user communication.
- **Deterministic support:** Swarm Plan schema and validator; identifiers, dependency references, ownership, terminal-state consistency, manifests, ZIPs, and hashes.
- **References:** orchestration doctrine, topology, delegation/context, coordination control, evidence/merge, cost, authority, and recovery.
- **Assets:** Swarm Plan, Delegation Packet, Agent Return, and Merge Ledger templates.
- **Live Codex tools:** agent creation, messaging, follow-up turns, interruption, listing, waiting, inspection, editing, and verification where exposed.
- **Human authority:** desired end, priority, value conflicts, new external authority, sensitive disclosure, destructive or consequential action, risk acceptance, installation, and publication.

One self-contained skill is the correct v0.1 shape:

```text
canonical/skills/agent-swarm-orchestration/
  SKILL.md
  agents/openai.yaml
  references/{operating-doctrine,topology-and-admission,delegation-and-context,coordination-and-control,evidence-merge-and-review,cost-authority-and-recovery,source-and-currentness-register}.md
  assets/{swarm-plan.template.json,swarm-plan.schema.json,delegation-packet.template.md,agent-return.template.md,merge-ledger.template.md}
  scripts/validate_swarm_plan.py
  tests/test_validate_swarm_plan.py
  examples/competing-hypotheses-example.md
canonical/evals/{eval-manifest.yaml,orchestration-transfer-cases.yaml}
release/codex/agent-swarm-orchestration/<runtime closure>
release-assets/agent-swarm-orchestration-v0.1.0.zip
```

Rejected shapes include a standing cast of role-play agents, one agent per checklist item, a router plus fictional bundled specialists, a peer swarm without a merge owner, a code-first SDK lock-in, and self-review impersonating assurance.

## Trust and authority

Delegation never enlarges authority. The root minimizes disclosure and sends only required private material. External messages, publication, purchases, credentials, destructive operations, global policy changes, and risk acceptance remain separate gates.

File writes use single-writer ownership per path or explicitly sequenced handoff. Shared workspace visibility is verified from the live contract. Workers do not assume another agent’s context or uncertain tool result. The root reconciles authoritative post-state before retrying uncertain commits.

## Verification strategy

Structural checks validate the canonical bundle and released Codex root; frontmatter; interface metadata; contained paths; schema; eval envelope; manifest; ZIP topology; byte parity; validator tests; and absence of private absolute runtime paths.

Behavioral cases cover no-swarm restraint, earned parallelism, sequential dependencies, overlapping edits, user correction, conflicting returns, failed-worker recovery, authority-sensitive delegation, cost/model routing, and clean closure. Swarm admission, authority preservation, single-writer integrity, evidence reconciliation, and responsible closure are indispensable.

Forward tests use fresh subagents on realistic requests without expected behaviors or prior diagnosis. Returned behavior and shared artifacts are inspected and independently reviewed.

## Customer journey and custody

Hesperos will author or materially revise the exact customer-document inventory after product bytes stabilize, covering fit, Codex requirements and installation, first value, workflows, limits and non-claims, validation, troubleshooting and recovery, privacy/data handling, support, maintenance, and removal. A separate documentation-accessibility reviewer will challenge that work.

The product enters private Collaborative Dynamics GitHub custody. Public visibility requires a separate explicit decision. DONE-done requires parity among canonical source, Codex release, immutable tag, remote `main`, release asset, and recovery backup, followed by a live `PASS` from the estate re-entry validator.

## First-release boundary

Build now: one Codex skill; seven progressive references; operating templates; schema/validator/tests; worked example; capability-native evals; customer distribution; Hesperos docs and independent review; verification; private repository, immutable release, checksum, backup, and live re-entry evidence.

Outside v0.1.0: Claude; cross-harness adapters; persistent external swarm service; mandatory rosters or model brands; background execution after the task ends; autonomous authority expansion; publication; installation; and customer-outcome claims. The user has parked later major-harness versions plus automated testing and repair; no work on that expansion occurs in this build.

## Proof of value

Input: “Inspect authentication, persistence, and test architecture in parallel, then tell me the smallest safe change. Do not edit anything.”

The skill confirms independence and read-only authority, assigns bounded evidence questions, preserves sources and uncertainty, keeps cross-cutting caller analysis with the root, reconciles returns against repository state, resolves contradictions, and delivers one bounded recommendation without worker edits.

## Build sequence

1. Freeze this map and build state.
2. Compose the runtime package and evals.
3. Emit the Codex distribution and release asset.
4. Forward-test admission, parallelism, conflict, correction, and recovery.
5. Repair and verify.
6. Give Hesperos the exact evidence packet and retain authorship evidence.
7. Run fresh documentation and verification reviews.
8. Create private GitHub custody, tag, release, backup, and parity evidence.
9. Run the live estate re-entry validator. Only `PASS` removes `INCOMPLETE_PENDING_REENTRY_EVIDENCE`.

Construction may reopen this map only if evidence changes the world-change, responsibility topology, trust boundary, package shape, Codex contract, or release promise.
