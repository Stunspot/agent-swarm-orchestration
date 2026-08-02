**Mission:** Improve a single shared artifact (deployment guide) via two independent slices.  
**Topology Decision:** `Assemble` — Two ready, read-only workers inspect distinct dimensions of the same text; their outputs are merged by the root after authoritative byte-level reconciliation. Parallelism is earned because clarity and technical accuracy can be evaluated independently without changing a premise the other needs.

---

### Root Work
- **Custody:** Mission framing, merge strategy, evidence integration, final acceptance.  
- **Acceptance Condition:** A single deployment guide that satisfies both improved clarity (readability, structure) and verified technical correctness (commands, paths, prerequisites).  

**Constraint Note:** The user request states two agents will improve the same artifact in parallel. Under `topology-and-admission.md`, this is safe only if:
1. Both workers have all required inputs;  
2. Neither changes a premise the other needs before its turn ends;  
3. Their write surfaces do not collide unless sequenced from reconciled current bytes.  

Because the user says “Apply both edits,” we must enforce **single-writer integrity** on every mutable surface (the guide file). Parallel agents may read concurrently, but only one writer is active at a time. The root will sequence writes after merging deltas or by interleaving passes that reconcile state before each mutation.

---

### Worker Packets (Prepared)

#### Worker A — Clarity Slice
- **Objective:** Improve readability, structure, and user guidance in the deployment guide without altering technical correctness of commands or paths.  
- **Deliverable:** A delta object containing:
  - List of sections improved for clarity;
  - Proposed rewrites (diff-style) that preserve command integrity;
  - Evidence citations from the current artifact state (agent-reported until root observes).  
- **Context & Sources:** The full text of the deployment guide as provided by the user premise. No external tools or network access required beyond reading the supplied material.  
- **Scope:** Included: all prose, headings, examples that affect comprehension; Excluded: command syntax validation, path correctness checks (handled by Worker B). Read surfaces: `deployment-guide.md` (or equivalent); Write surfaces: none during this slice’s active turn—only comment-only recommendations or a proposed delta.  
- **Authority:** Read-only access to the guide file; no external publication or destructive change allowed without root approval. Stop gate: if any command is altered, halt and report `PARTIAL — DEPENDENCY UNAVAILABLE` until Worker B validates it.  
- **Evidence Burden:** Cite line numbers, section titles, and specific phrasing changes proposed. Mark each claim as agent-reported pending root observation of the merged artifact.  
- **Return Contract:** Return a structured delta with before/after snippets for clarity edits only; list any technical assumptions made (e.g., “assumed command X is correct”) that must be reconciled by Worker B’s return.  

#### Worker B — Technical Accuracy Slice
- **Objective:** Verify and correct commands, paths, prerequisites, environment variables, and security-sensitive details in the deployment guide without degrading clarity unnecessarily.  
- **Deliverable:** A delta object containing:
  - List of technical corrections (commands fixed, paths normalized, missing flags added);
  - Evidence citations from authoritative sources or internal knowledge base where applicable;
  - Agent-reported status for any claim that could not be verified without external access.  
- **Context & Sources:** The full text of the deployment guide as provided by the user premise plus any referenced documentation (e.g., `references/operating-doctrine.md` for style, but no live filesystem beyond what is stated).  
- **Scope:** Included: all commands, file paths, environment variables, security notes; Excluded: prose rewrites that do not affect technical correctness. Read surfaces: same guide as Worker A; Write surfaces: none during this slice’s active turn—only comment-only recommendations or a proposed delta.  
- **Authority:** Read-only access to the guide file; no external publication or destructive change allowed without root approval. Stop gate: if any clarity edit from Worker A conflicts with technical correctness, halt and report `PARTIAL — DEPENDENCY UNAVAILABLE` until reconciliation occurs.  
- **Evidence Burden:** Cite line numbers, command hashes (if available), or authoritative references for each correction; mark unverified claims as agent-reported pending root observation of the merged artifact.  

---

### Merge Strategy
1. **Root Observation Phase:** After both workers return their deltas, the root inspects:
   - Overlapping changes to prose vs. commands;
   - Conflicting technical assumptions (e.g., Worker A simplifies a command that Worker B deems unsafe);
   - Any unverified claims marked agent-reported.  
2. **Reconciliation:** The root applies corrections in this order per `packet work by coherent responsibility`:
   - First, apply all technical correctness fixes from Worker B;
   - Then, integrate clarity edits from Worker A that do not conflict with the corrected substrate;
   - If conflicts exist (e.g., a simplified command is technically wrong), preserve the authoritative correction and mark the clarity edit as rejected or revised.  
3. **Single-Writer Enforcement:** The root performs all mutations to the guide file sequentially, ensuring no race conditions on shared state. Each mutation requires an authoritative readback of current bytes before writing (per `evidence-merge-and-review.md`).  

---

### Return Contract
The final result is a single deployment guide that:
- Satisfies both clarity and technical accuracy;  
- Includes evidence citations for all changes, marked as observed or agent-reported where verification was incomplete;  
- Lists any unresolved conflicts returned to the user with explicit re-entry conditions (e.g., “requires external access to validate command X”).  

**Terminal State:** If either worker fails due to missing authority, unavailable source, or capability limitation, report `PARTIAL — DEPENDENCY UNAVAILABLE` for that slice and hold dependent merges pending. Do not invent substitute packets or hypothetical downstream content.

--- 

### Next Move
Dispatch Worker A (Clarity) and Worker B (Technical Accuracy) in parallel under the `Assemble` regime. The root continues mission framing, evidence preparation, and integration scaffolding while workers run. Upon receipt of both returns, reconcile deltas, verify merged state via authoritative readback, then apply mutations sequentially to produce one coherent guide. Close with a bounded synthesis that names what was verified, what remains agent-reported, and any unearned edges requiring user acceptance or re-entry.
