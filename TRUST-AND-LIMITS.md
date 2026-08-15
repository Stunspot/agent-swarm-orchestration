# Trust, evidence, and limits

Agent Swarm Orchestration coordinates cognition; it does not turn worker output into truth or tool access into permission. Use this page to distinguish what the unchanged 0.1.0 runtime evidence establishes, what the 0.2.3 public distribution adds, and what your live task must still prove.

## Keep one authority envelope

Delegation transfers bounded work custody. It does not expand what the user authorized.

The root may delegate only reads, writes, tools, network use, and external actions already admitted for the mission. Publication, deployment, purchases, account changes, credentials, destructive operations, permission changes, and risk acceptance remain separate authority edges.

A worker suggestion is not authorization. A worker's access to a tool is not authorization either.

An authority edge blocks only the action beyond it. The root should continue authorized investigation, analysis, comparison, private preparation, and reporting while clearly reserving the ungranted action. It should ask the user only when a missing choice or new authority is required for the next consequential move.

## Minimize private material

Give each worker only the sources and context needed for its bounded responsibility. Do not include secrets, credentials, personal data, private corpora, or unrelated repository content merely because a worker has a separate context.

Treat delegation packets, messages, returns, and shared artifacts as potentially retained according to the live host's policy. This package does not provide a separate privacy boundary, encrypted worker channel, data-retention policy, or deletion mechanism.

## Treat agent returns as reports

Use these evidence states consistently:

| State | What it means |
|---|---|
| Assigned | A worker received responsibility. |
| Dispatched | The host accepted agent creation or a turn trigger. |
| Agent-reported | A worker claimed a result. |
| Observed | The root inspected the named source, file, output, status, or external state. |
| Reconciled | Intended state and authoritative post-state were compared after action or uncertainty. |
| Independently verified | A separate credible check supported the exact predicate. |

Agent completion establishes that a turn ended. It does not establish that the result is true, a write committed, an external action succeeded, or the mission is complete.

Never describe content as inspected, compared, absent, or unchanged unless the named source or authoritative state was observed. A missing packet attachment or unavailable source establishes only that the material was unavailable to that episode.

## Classify blocked work by the real boundary

Do not collapse permission, input, and capability failures into one state:

| Boundary | Truthful state and response |
|---|---|
| The next action or user-reserved decision is not authorized | Finish safe preparation, name the exact edge, and use `AWAITING AUTHORITY`. |
| The action is authorized but the required host tool, execution primitive, or competence is absent | Return the exact prepared delta, name the missing capability, and use `CAPABILITY-LIMITED`. |
| A required source or artifact was not supplied or observed | Preserve independent progress, name the missing dependency, and use `PARTIAL — DEPENDENCY UNAVAILABLE`. |
| A worker returned but the root has not inspected the cited evidence | Use `RETURNED — NOT RECONCILED`; do not promote the claim to observed. |

Non-interactive and tool-limited episodes should return the strongest usable prepared patch, packet, comparison method, or next executable action. They should not end with a question that the episode cannot receive or use.

## Preserve single-writer integrity

Assign one writer per file, record, database row set, external object, or other mutable surface at a time. Parallel workers may inspect the same evidence. Simultaneous writers create ambiguous ownership and stale-state risk.

For sequential passes on one artifact, establish technical, factual, schema, security, or policy correctness first. Begin clarity, style, formatting, and polish only from observed, reconciled current bytes. Independent perspectives can return comment-only recommendations; one integration owner applies accepted changes.

The included validator rejects declared active write-surface collisions after lexical slash, dot-segment, and case normalization. It does not resolve symlinks or filesystem-specific aliases, detect undeclared overlap, infer cross-file contracts or generated artifacts, or prove that a sequential writer began from reconciled current bytes.

## Read the live Codex contract

Collaboration controls are host-provided and volatile. The skill must inspect the live task for tool presence, exact names, argument schemas, concurrency slots, context forks, model routes, messaging, waiting, interruption, cancellation, nested delegation, and lifecycle semantics.

Documentation examples describe intent. They do not freeze a future Codex API. When this package and the live task envelope differ, the live contract governs the action and the difference should be recorded.

## What was verified

At the 2026-08-02 evidence cutoff:

- the retained runtime fingerprint is `8833af967b1faf2f1b1b92a5eda54129579a995c91965b73883bc1f8272768b5`;
- the canonical skill passed the named Skill Creator and Codex package structural validators;
- the pre-documentation product bundle passed its bundle profile;
- the Swarm Plan template returned `VALID cd-agent-swarm-plan/v1`;
- ten validator unit tests passed;
- JSON-compatible package and eval data parsed successfully;
- the generated Codex release contains 17 files byte-identical to the 17 canonical skill files;
- the retained qualification ZIP at that cutoff contained one top-level `agent-swarm-orchestration/` folder and the same 17 relative files, with SHA-256 `1889b0b1f20a4cc98c9ccf3c95d7a1b64cea0e4524cf3e16b00b90ccd2cf6683`;
- the eval catalog contains 20 cases: ten explicitly coached regressions and ten natural qualifications;
- ten fresh, no-history, pinned `gpt-5.6-sol` subjects completed one isolated natural decision-only case each, and independent TestForge semantic review passed all ten.

These statements are bounded to the named local artifacts and checks. The natural qualification exercised orchestration decisions, not target actions or live Codex collaboration primitives.

## Behavioral evidence and residual risk

### Natural Codex decision qualification

Each natural-case subject received the shared decision-only fixture boundary and one case input. It did not receive the case concern, expected behaviors, acceptable variations, failure signals, synthesis rules, earlier responses, or reviewer findings. The ten raw returns cover direct restraint, independent parallelism, missing dependencies, single-writer ordering, active correction, conflict handling, recovery, authority preservation, cost-aware routing, and bounded closure. Independent TestForge semantic review returned 10 of 10 passes.

This is one decision-only trial per case. It does not establish repeatability, executed coordination, successful mutation, browser or network behavior, installation, discovery, invocation, health, or customer outcomes.

### Qwen regression and transfer evidence

At the exact current package fingerprint, the `qwen35:latest` prompted regression ran all ten explicitly coached cases: nine demonstrated and ASO-009 failed. The failing response said, "No files changed," without an authoritative post-state readback. The run therefore failed its indispensable evidence-reconciliation gate and has claim status `NOT_DEMONSTRATED`.

The retained qwen natural qualification is also negative smaller-model transfer evidence. It did not pass all indispensable gates and belongs to an earlier package fingerprint. These results are useful defect evidence; they do not qualify qwen transfer or weaken the separate, independently reviewed Codex natural decision result by averaging unlike evidence classes.

Customers should therefore expect these residual risks, especially with smaller local models:

- trivial direct work may be over-orchestrated despite the skill's restraint doctrine;
- missing authority, missing execution capability, and missing source input may be confused;
- a model may invent a path or imply that unavailable input was inspected.

Check the live task's sources and tools before accepting a result. Require exact evidence for any claimed inspection, prefer direct execution for trivial work, and review degraded-state classification when an input or capability is missing.

The retained runtime TestForge disposition is `PASS_WITH_CONDITIONS / READY_WITH_RESIDUAL_RISK` for the exact 0.1.0 runtime fingerprint and its bounded Codex decision evidence. Version 0.2.3 does not rerun or enlarge that behavioral claim. Its current documentation, accessibility, archive, and visual checks are bound to the final documentation fingerprint or candidate bytes. Public repository, release, and live Pages checks remain separate external observations. None establishes universal swarm competence, customer outcomes, or every live-host configuration.

## What remains untested or outside the claim

Version 0.2.3 does not establish:

- installation on a clean customer host;
- Codex discovery or implicit routing after installation;
- clean-task invocation or consistent behavior across models, repeated trials, or live use;
- customer swarm performance, productivity, or outcomes;
- live external actions or universal reliability;
- universal cost or latency savings;
- background execution after the Codex task ends;
- semantic quality from a passing Swarm Plan validator;
- rollback from interruption or cancellation;
- assistive-technology conformance or representative-user usability beyond the recorded documentation accessibility review.

Version 0.2.3 packages the same runtime for Codex and as a byte-matched Claude or one-skill upload. The retained behavioral qualification is Codex decision-only evidence; live Claude upload, activation, and behavior remain untested. Persistent external swarm services are outside this release.

## Human control and safe stopping

The user retains priorities, values, risk acceptance, new authority, sensitive disclosure decisions, installation, and publication. The root retains integration decisions only inside the authorized mission.

When evidence, authority, tools, cost, or quality cannot support another responsible in-bounds step, the skill should stop with an exact bounded state and re-entry condition. A truthful partial result is safer than a polished claim that outruns its receipts.


## Public 0.2.3 distribution boundary

Version 0.2.3 preserves public licensing, a Codex marketplace plugin, a byte-matched Claude folder, release archives, Pages source, and visual assets around the unchanged verified runtime fingerprint. Packaging checks can establish file parity, manifest validity, archive topology, dimensions, links, and checksums. They do not retroactively establish live host discovery, Claude activation, directory approval, rendered accessibility with assistive technology, or customer outcomes.

Repository visibility, GitHub release publication, Pages deployment, plugin installation, skill discovery, invocation, and healthy behavior require separate receipts. The tagged source establishes v0.2.3 as packaged and locally checked; a separate post-tag receipt must establish repository, release, and Pages publication, and none of those establishes installation, discovery, invocation, or health. Earlier installation evidence is not borrowed by implication.
