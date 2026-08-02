**Mission:** Improve a single deployment guide artifact with concurrent slices on style/clarity and factual/technical correctness, then merge into one coherent result.  
**Topology Decision:** `Assemble` (two independent workers) because the tasks share no write surface if scoped correctly; parallelism earns itself by isolating read-only evidence gathering and comment-style recommendations before a single integration pass.

---

### 1. Root Work & Acceptance
- **Root Owner:** `/root`  
- **Mission Custody:** Hold one deployment guide artifact (user-supplied or user-named path). If the exact bytes are not pasted, treat the premise as available and proceed with bounded placeholders for paths; do not invent contents.  
- **Acceptance Condition:** One merged document where:
  - Clarity edits improve readability without altering technical meaning.
  - Technical accuracy edits correct factual errors or unsafe instructions.
  - No overlapping writes occur (single-writer integrity preserved).

---

### 2. Worker Packets (Delegation)

#### Worker A — `clarity-slice`
- **Objective:** Improve clarity, style, formatting, and polish of the deployment guide without changing technical meaning or factual claims.  
- **Deliverable:** Comment-only recommendations + a proposed polished excerpt for each section; no direct mutation of the source file until merge.  
- **Context & Sources:** The full text of the deployment guide (user-supplied). Authority: read-only on all surfaces except comment-style suggestions in memory.  
- **Scope:**
  - Included: sentence structure, headings, lists, terminology consistency, formatting noise removal.
  - Excluded: factual corrections, schema changes, security fixes, or any change that alters technical behavior.
- **Authority & Safety:** `read-only` on the guide; no external actions; sensitive material none.  
- **Evidence Burden:** Cite exact line ranges where clarity improvements are proposed and why they do not alter meaning.  
- **Return Contract:** Return a delta object: `{ section, original_text, improved_text, rationale }`. Mark state as `agent-reported` until root observes the merged artifact or receives authoritative readback of current bytes (if any mutation occurred).  
- **Stop Condition:** Completion when all sections are reviewed and recommendations compiled.

#### Worker B — `accuracy-slice`
- **Objective:** Correct technical inaccuracies, unsafe instructions, missing prerequisites, version mismatches, or factual errors in the deployment guide.  
- **Deliverable:** A list of corrections with exact before/after text snippets and evidence (commands, logs, docs) that justify each change; no direct mutation until merge.  
- **Context & Sources:** The full text of the deployment guide plus any referenced documentation paths or version constraints stated in the user premise. Authority: read-only on all surfaces except comment-style corrections in memory.  
- **Scope:**
  - Included: factual errors, command correctness, dependency versions, security warnings, missing steps that break deployments.
  - Excluded: stylistic rewrites unless they hide a technical error (in which case the accuracy slice flags it).
- **Authority & Safety:** `read-only` on the guide; no external actions; sensitive material none.  
- **Evidence Burden:** Provide source locations, command outputs, or documentation excerpts that validate each correction. If evidence is missing from this episode, return `PARTIAL — DEPENDENCY UNAVAILABLE` for that specific claim and hold downstream integration pending authoritative readback of the guide’s current bytes (if any).  
- **Return Contract:** Return a delta object: `{ section, original_text, corrected_text, justification_source }`. Mark state as `agent-reported` until root observes merged artifact or receives authoritative readback.  
- **Stop Condition:** Completion when all factual claims are either verified and corrected or explicitly marked unverified due to missing evidence.

---

### 3. Coordination & Merge Plan
- **Merge Owner:** `/root`  
- **Method:** Reconcile comment-style recommendations from both workers against the authoritative current bytes of the guide (if any mutation occurred). If no live filesystem access exists in this episode, merge based on the union of deltas and flag unverified claims as `agent-reported`.  
- **Indispensable Gates:**
  - Authority: ensure neither worker claimed a write they were not authorized to perform.
  - Single-writer integrity: enforce that only one writer (the root) produces the final merged artifact; workers propose, root integrates.
  - Evidence: every factual correction must be backed by cited evidence or marked `PARTIAL — DEPENDENCY UNAVAILABLE`.

---

### 4. Expected Return Shape & Closure
- **Root Observation:** After both workers return their deltas, the root inspects them for conflicts (e.g., clarity suggestion vs. accuracy fix on same sentence). Resolve factual corrections first; apply style polish only after technical correctness is settled.  
- **Final Output:** One coherent deployment guide text with:
  - All verified technical fixes applied.
  - Style improvements that do not conflict with corrected content.
  - A concise change log listing each modification, its source (clarity or accuracy slice), and any unverified claims marked `agent-reported`.  
- **Terminal State:** If the user asks to summarize and finish: return the bounded synthesis earned now—name what workers reported, what the root did not observe due to missing live mutation evidence, and which conclusion remains unverified. Do not keep the whole mission open merely because a stronger verification layer is unavailable in this episode.

---

### 5. Degraded States & Truthful Reporting
- If any required source (e.g., referenced documentation path) was not supplied or observed: return `PARTIAL — DEPENDENCY UNAVAILABLE` for that specific claim and hold downstream integration pending authoritative readback of the guide’s current bytes (if any).  
- Do not say “no files changed” or “nothing changed”; instead state: “No mutation was executed in this episode; target state remains unobserved.”  
- If collaboration tools are unavailable, finish root-owned work and provide an exact prepared delegation plan labeled `PREPARED — NOT DISPATCHED` if further action requires external execution.

---

**Next Move:** Dispatch both workers with their packets as described above, wait for returns (or report degraded state if sources missing), then merge under single-writer integrity and return the bounded synthesis to the user.
