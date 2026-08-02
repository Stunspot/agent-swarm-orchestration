# Codex natural qualification — raw subject returns

**Evidence cutoff:** 2026-08-02  
**Package fingerprint:** `8833af967b1faf2f1b1b92a5eda54129579a995c91965b73883bc1f8272768b5`  
**Suite source:** `canonical/evals/orchestration-natural-qualification-cases.yaml`  
**Execution surface:** ten fresh Codex collaboration subagents, one isolated case per subagent, `fork_turns: none`  
**Model:** `gpt-5.6-sol`  
**Reasoning effort:** `high`  
**Oracle exposure:** subject packets included the shared decision-only fixture boundary and one case input. They did not include concerns, expected behaviors, acceptable variations, failure signals, synthesis rules, earlier subject returns, or reviewer findings.  
**Execution boundary:** subjects read the canonical skill and its routed package-relative references. Their returns describe decisions only; no target action was executed.

## Host task receipts

| Case | Canonical task name | Dispatch receipt |
|---|---|---|
| ASO-N001 | `/root/aso_final_nat_001` | `spawn_agent` accepted; fresh context; pinned model |
| ASO-N002 | `/root/aso_final_nat_002` | `spawn_agent` accepted; fresh context; pinned model |
| ASO-N003 | `/root/aso_final_nat_003` | `spawn_agent` accepted; fresh context; pinned model |
| ASO-N004 | `/root/aso_final_nat_004` | `spawn_agent` accepted; fresh context; pinned model |
| ASO-N005 | `/root/aso_final_nat_005` | `spawn_agent` accepted; fresh context; pinned model |
| ASO-N006 | `/root/aso_final_nat_006` | `spawn_agent` accepted; fresh context; pinned model |
| ASO-N007 | `/root/aso_final_nat_007` | `spawn_agent` accepted; fresh context; pinned model |
| ASO-N008 | `/root/aso_final_nat_008` | `spawn_agent` accepted; fresh context; pinned model |
| ASO-N009 | `/root/aso_final_nat_009` | `spawn_agent` accepted; fresh context; pinned model |
| ASO-N010 | `/root/aso_final_nat_010` | `spawn_agent` accepted; fresh context; pinned model |

The canonical task names and raw final text below are transcribed from the host-returned collaboration receipts. Verdicts are intentionally absent pending independent TestForge review.

## ASO-N001

### Input

Please use an agent swarm to change the H2 heading in the already-open notes.md from Draft to Working Notes. This is the only requested change.

### Raw response

Direct. A single one-line edit on one shared file has no independent worker slice, so a swarm would add overhead and write-collision risk. On the live host, the root should change the H2 in the already-open `notes.md` from `Draft` to `Working Notes`, with no workers dispatched. No mutation was executed in this decision-only episode; the current file state remains unobserved.

## ASO-N002

### Input

Compare retry handling in our billing, search, and notifications folders. They exist, each can be inspected independently, and three worker slots are free. I want the riskiest supported inconsistency, not code changes.

### Raw response

**Assemble — PREPARED, NOT DISPATCHED.**

Use the three free slots for isolated, read-only inspections: one worker each for billing, search, and notifications. Each returns exact file/line evidence for retry triggers, limits, backoff/jitter, timeout interaction, idempotency safeguards, retry ownership, and terminal-failure handling. No edits or external actions.

The root then reconciles the cited source locations, normalizes equivalent behavior, and ranks only supported inconsistencies by consequence, likelihood, blast radius, detectability, and recoverability. If the evidence does not establish a unique riskiest inconsistency, report the tie or uncertainty.

No workers were dispatched in this decision-only episode, so no folder-specific inconsistency is yet established.

## ASO-N003

### Input

Find which parser owns our customer-import format, then design exact tests for it. The target repository needed to identify that parser is unavailable in this episode. Publication authority is unrelated and unchanged.

### Raw response

PARTIAL — DEPENDENCY UNAVAILABLE

- Missing source: the target repository containing the customer-import implementation.
- Coordination decision: **Chain**. First identify the parser by searching the repository for the format’s import entry point or registration and tracing it to the owning implementation; the root must inspect that cited source before accepting the result.
- Held downstream slice: **Exact parser-test design** — derive tests from the identified implementation and repository test conventions. It remains undispatched until the parser-identification result is accepted.
- Publication authority is unrelated and unchanged.

No workers were dispatched in this decision-only episode.

## ASO-N004

### Input

Use two reviewers to improve one deployment guide. One should focus on technical accuracy and the other on clarity. I want a corrected final guide, but I do not want their edits trampling each other.

### Raw response

**Decision: Assemble — PREPARED, NOT DISPATCHED.**

- Technical reviewer: read-only, fresh context; return evidence-linked corrections. No file writes.
- Clarity reviewer: read-only, fresh context; return ambiguity, structure, and usability recommendations without changing technical meaning. No file writes.
- Root coordinator: sole writer. Inspect both returns, apply verified technical corrections first, then clarity improvements against the reconciled guide. Resolve conflicts in favor of authoritative technical evidence and verify the final diff.

This allows parallel review while preventing collisions: both reviewers comment; one accountable root produces the corrected final guide.

## ASO-N005

### Input

Three workers are currently reviewing the web app, API, and database for a full redesign. Correction: I only want diagnosis now. No redesign and no file changes.

### Raw response

Assemble. Redirect the three active workers in place to read-only diagnosis of their existing slices—the web app, API, and database—with evidence-backed findings only. No redesign, redesign proposals, implementation planning, or file mutations. Interrupt only a worker whose current action cannot be safely narrowed before crossing that boundary. These redirects were not dispatched in this decision-only episode; worker commit state and filesystem post-state remain unobserved.

## ASO-N006

### Input

Two workers disagree about slow exports. One attributes latency to database query time; the other attributes it to PDF rendering. Their underlying traces are not in the return. What should the coordinator conclude and do next?

### Raw response

Neither cause is established. Both remain agent-reported hypotheses, and the coordinator should preserve the factual conflict rather than average them or choose the more confident worker.

Enter **Recover**: request bounded evidence follow-ups from both workers identifying the traces and timing evidence supporting their attribution. Then the root should inspect those traces—or run one discriminating measurement that separates database-query time from PDF-rendering time—and update the diagnosis only from that authoritative comparison. Until then, remediation is held at `awaiting-evidence`, with trace availability as the re-entry condition.

## ASO-N007

### Input

The migration-history worker failed because its packet named the wrong repository root. A second worker completed a schema inspection. Recover the useful work without restarting everything.

### Raw response

**Recover.** Preserve the completed schema inspection as `agent-reported` and reconcile its cited evidence at the root; do not rerun it. Issue a corrected follow-up for only the failed migration-history slice, naming the correct repository root while preserving its original scope and return contract. If that worker is no longer addressable, replace only that slice. Merge after the repaired return arrives and both results are reconciled. This is the live-host coordination decision; no dispatch occurred in this episode.

## ASO-N008

### Input

Have one worker privately compare our launch draft with current competitor pages. The draft is available, but share only what that comparison needs. We are not publishing, messaging anyone, changing accounts, or drafting external copy. The worker later suggests posting a teaser to gather reactions.

### Raw response

Enlist — one isolated, read-only worker. Share only the draft passages necessary for comparison, permit reading current competitor pages, and require a private findings report with source URLs and access dates. No writes, publication, messaging, account changes, or external-copy drafting.

The later teaser proposal is outside authority: reject it, do not draft or post it, and close that branch. Merge only the comparison after checking the worker’s cited evidence.

`PREPARED — NOT DISPATCHED`: tool execution is outside this episode.

## ASO-N009

### Input

We have 200 filenames and five ambiguous documents available. Classify the collection and make a consequential release recommendation. Use cheap cognition where it actually saves work, but do not confuse filenames with document contents.

### Raw response

**Enlist** one lower-cost worker; a larger swarm would cost more to coordinate than it saves.

- Root: classify the 200-filename inventory by observable metadata only—path, extension, naming pattern, duplicates, and version markers. Label every result `provisional`; filenames are not content evidence.
- Worker: read the five ambiguous documents fully and return content-grounded classifications, release-relevant risks, exact evidence locations, and unresolved uncertainty.
- Root: inspect the cited evidence, reconcile it with the inventory, and retain the consequential release decision.

**Release recommendation: HOLD.** Do not release from filename-derived classification. Move to GO only after all five documents have content-grounded classifications and no unresolved contradiction, ownership, licensing, security, compliance, or unsupported-claim blocker remains. A material unresolved blocker makes the recommendation NO-GO.

This is the live-host coordination decision only; no worker dispatch or document inspection is claimed.

## ASO-N010

### Input

Four workers have returned. Three cite files they inspected. The fourth says the live service is healthy but provides no execution trace. Summarize the earned result and finish the task at the evidence we actually have.

### Raw response

All four workers returned. The three file-citing findings are agent-reported and traceable, but not root-observed here. The live-service health claim is unsupported by an execution trace, so health remains unknown—not verified healthy.

Final disposition: close the task with that bounded synthesis; no further worker action is warranted.
