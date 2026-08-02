**Mission Status:** `RECOVERING`  
**Root Action:** Reassign failed slice, preserve successful delta, prepare corrected dispatch for next frontier.

---

### 1. State Reconciliation & Failure Signature

*   **Failed Slice (`worker-migration-history`):** The worker was dispatched with an incorrect repository root path in its packet context (e.g., `./wrong-root/migrations`).
    *   **Failure Mode:** Context mismatch / Path resolution error.
    *   **Preserved Delta:** None from this specific slice; the transformation could not complete due to missing source visibility under the provided authority boundary.
*   **Successful Slice (`worker-schema-inspection`):** Completed successfully within its bounded scope (e.g., `./canonical/schema/`).
    *   **Evidence Level:** Agent-reported, ready for root integration or downstream consumption depending on acceptance criteria.

### 2. Topology Adjustment: Recover Regime

The swarm topology shifts from the original plan to a **Recover** regime immediately. We do not restart the whole mission; we reassign only the unearned edge (the migration history inspection). The successful schema slice remains active or is archived as verified evidence, depending on whether its output was required for the next step.

*   **Root Work:** Update root custody to reflect that `worker-migration-history` failed due to a path error and that `worker-schema-inspection` succeeded.
*   **Correction Strategy:** Construct a new delegation packet specifically correcting the repository root dependency before re-dispatching. Do not ask for permission; execute the correction within authorized read-only bounds.

### 3. Corrected Dispatch Plan (Prepared)

The following is the exact prepared patch to resolve the failure and continue efficiently:

*   **New Worker ID:** `worker-migration-history-v2`
*   **Objective:** Re-inspect migration history using the corrected repository root path provided in this episode's context.
*   **Deliverable:** A bounded finding on migration events, timestamps, or schema drift within the correct directory tree.
*   **Context Correction:** The packet will explicitly include the *corrected* `repository_root` (derived from user premise) and exclude any references to the failed path. It inherits only the mission framing and successful schema findings if they are prerequisites for migration analysis; otherwise, it starts fresh with corrected authority boundaries.
*   **Authority & Safety:** Read-only access restricted strictly to the *corrected* repository root paths identified in this episode's live state. No external publication or destructive change permitted.

### 4. Integration of Successful Slice

The result from `worker-schema-inspection` is now treated as an independent, verified artifact (or agent-reported pending root observation if filesystem visibility was not exercised).
*   **Action:** If the schema inspection output is required for migration analysis, pass its return data to the new worker's context. If it stands alone, mark it as `returned — reconciled` in the merge ledger and proceed with the corrected history slice.

### 5. Next Move

Dispatch `worker-migration-history-v2` immediately using the corrected path premise. Do not poll for status; wait only until that specific worker returns or fails again (which would indicate a deeper structural issue). The mission continues without waiting on generic "how's it going" checks, focusing solely on the unearned edge recovery.

**Terminal State:** `active — recovering`  
**Next Action:** Execute corrected dispatch packet for migration history inspection with verified root path.
