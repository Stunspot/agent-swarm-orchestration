# Swarm Recovery Report: `PARTIAL — DEPENDENCY UNAVAILABLE`

**Mission:** Reconcile the failure of the `migration-history` slice and integrate its successful counterpart, while preserving mission custody under read-only authority constraints.  
**Root Owner:** `/root` (Agent ID not specified in fixture; assumed root coordinator).  
**Current State:** `recovering`.  

---

## 1. Failure Analysis: The Migration-History Slice
The worker designated for **migration-history analysis** failed due to a packet ambiguity regarding the repository root path (`depends_on` or context source mismatch). This is classified as a **packet ambiguity / missing context** failure per doctrine.  
*   **Failure Signature:** `PARTIAL — DEPENDENCY UNAVAILABLE`. The specific dependency (the correct repository root) was not supplied in the live episode's evidence stream, nor can it be inferred without violating read-only constraints or inventing paths.
*   **Useful Delta Preserved:** None for this slice specifically; however, the *mission objective* remains intact and recoverable via a corrected premise.

## 2. Integration: The Schema Inspection Slice
A second worker completed successfully with a schema inspection result.  
*   **Status:** `returned`.  
*   **Evidence Level:** `agent-reported` (awaiting root observation of specific artifact if provided, or accepted as the current authoritative state for that slice).  
*   **Integration Effect:** The schema data is now available to inform downstream decisions or serve as a baseline. It does not resolve the migration-history failure but provides necessary context for any recovery attempt involving database structures.

## 3. Recovery Strategy: Changing the Premise
Per `references/cost-authority-and-recovery.md`, we must change the representation, decomposition, sequence, or owner before retrying. We do **not** restart everything; we reassign only the unearned edge (the migration-history slice).  

*   **Action:** Re-declare the objective for the failed worker with a corrected premise regarding the repository root path.  
*   **Constraint Check:** The user has not explicitly authorized writing to production or changing external state beyond read-only inspection in this episode. If the "corrected" packet requires accessing an unlisted file system location, that action remains `CAPABILITY-LIMITED` until authority is explicit. Assuming the corrected root path exists within permitted read surfaces:  
    *   **New Objective:** Inspect migration history using `[CORRECT_REPOSITORY_ROOT]`.
    *   **Deliverable:** Migration delta or causal diagnosis of duplication/loss events (if applicable to mission).

## 4. Topology Decision for Next Move
*   **Regime Selection:** `Enlist` (one bounded worker) is appropriate here because the failure was isolated to a single dependency resolution, not a systemic collapse requiring parallel hypothesis testing (`Assemble`) or sequential chaining from another specialist yet unready (`Chain`).  
    *   *Note:* If the schema inspection result requires immediate consumption by the migration analysis before it can run (e.g., filtering logs by table name), we would switch to `Chain`. Without that explicit dependency, they remain independent.

## 5. Prepared Recovery Packet
The following packet is prepared for dispatch once authority permits or if read-only access allows:

```markdown
# Delegation Packet — worker-migration-history-recovery

## Objective
Inspect migration history using the corrected repository root path to identify causes of duplication or data loss events, without modifying production state.

## Deliverable and acceptance
A bounded finding set identifying whether duplicates arise from scheduling triggers, queue redelivery, or downstream idempotency gaps (as per `competing-hypotheses-example.md`), citing specific log locations if available in the corrected root.

## Context and sources
- **Sources:** The live repository at `[CORRECT_REPOSITORY_ROOT]`.  
- **Prior Decisions:** Schema inspection completed successfully; use its structure to guide migration analysis scope.  
- **Authority:** Read-only access permitted for this episode only. External publication or destructive change remains reserved.

## Scope and ownership
- **Included:** Migration logs, scheduler triggers, queue acknowledgments within the corrected root.  
- **Excluded:** Production write operations; unrelated repository branches not in evidence.  
- **Read surfaces:** `[CORRECT_REPOSITORY_ROOT]/logs`, configuration files defining migration jobs.  
- **Write surfaces:** `none` (strict read-only).

## Authority and safety
- Allowed tools: Read file, list directory contents within the corrected root.  
- Stop gates: If a required log or config is missing from this path, report immediately as `PARTIAL — DEPENDENCY UNAVAILABLE`.  

## Evidence burden
Cite exact paths to logs inspected; do not claim observation of content that was not read in this episode.

## Return contract
Return the result first (migration delta), then evidence locations and touched state. If the corrected path is still invalid, return `PARTIAL — DEPENDENCY UNAVAILABLE` with the specific missing source name.

## Stop condition
Completion upon finding a causal diagnosis or confirmation that the repository root remains inaccessible under current authority.
```

---

## 6. Final Disposition & Next Move
*   **Integrated State:** Schema inspection result is active; migration-history slice is held pending corrected context (`[CORRECT_REPOSITORY_ROOT]`).  
*   **Conflict Resolution:** No factual conflict exists between the two slices other than their independence. The schema data does not contradict the failure mode of the history worker, only provides a structural baseline for it to use upon recovery.  
*   **Terminal State:** `recovering`.  

**Next Move:** Dispatch the prepared packet above if `[CORRECT_REPOSITORY_ROOT]` is known and accessible under current authority. If that path remains unknown or inaccessible without user input:
1.  Report `PARTIAL — DEPENDENCY UNAVAILABLE`.
2.  Name the missing source explicitly (the correct repository root).
3.  Hold the downstream slice pending that specific evidence boundary.

**Root Observation:** No files changed in this episode; no mutation was executed. The workspace state remains unobserved regarding any external artifacts outside the provided fixture boundaries.
