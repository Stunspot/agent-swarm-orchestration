**Mission:** Rename `notes.md` heading from "Draft" to "Working Notes".  
**Topology Decision:** **Direct**.  

### Reasoning for Topology Selection (Admit the lightest capable topology)
The user request involves a single, atomic file mutation on one artifact (`notes.md`). 
- The task is small and sequential.
- It requires shared-context-heavy work (reading current bytes to verify "Draft", then writing).
- There are no independent ready slices; there is only one bounded transformation: the rename operation itself.
- Spawning workers for a single-file edit incurs unnecessary startup, context reconstruction, and merge costs that exceed the benefit of parallelism here.

Per `references/topology-and-admission.md`: "Use **Direct**... when [work] is small, sequential, shared-context-heavy, same-surface, or latency-sensitive."
Per `SKILL.md` under *Admit the lightest capable topology*: "Do not spawn merely because agents are available... When the swarm is not earned, proceed directly and keep the explanation brief."

### Authority Check & Capability Boundary
The user authorized a write to `notes.md`. However, in this specific episode context (Context-only Codex orchestration), no file system or tool primitive for writing files has been injected into the build task. 
- **Allowed:** Read current state of `notes.md` if available; prepare the exact edit delta and authority conclusion.
- **Reserved/Unavailable:** Actual filesystem mutation, network calls to save, or external publication.

Per `references/cost-authority-and-recovery.md`: "If a required artifact... was not supplied or observed, report `PARTIAL — DEPENDENCY UNAVAILABLE`... In a non-interactive run, return the strongest usable prepared result instead of ending with a question."
Since I cannot observe the live file content to verify it currently says "Draft" (no tool execution), and I lack the write primitive:

**State:** `PREPARED — NOT DISPATCHED`.  
**Evidence Boundary:** The user's request is accepted as the mission, but the host contract lacks the specific mutation tools for this episode.

### Prepared Action
I return the exact prepared patch packet that would be dispatched if a file-write tool were available or in an interactive mode where I could execute it. This satisfies "return only the named missing sources... and any independent authority conclusion."

---

# Agent Return — `root` (Direct Regime)

**Disposition:** `returned | capability-limited`

## Result
The mission to rename the heading of `notes.md` from "Draft" to "Working Notes" is **prepared but not dispatched**. The topology selected was **Direct**, as no parallel decomposition exists for a single-file mutation. However, execution cannot proceed because the live host contract does not expose file-write primitives in this episode context.

## Evidence
- **Mission:** Rename `notes.md` heading ("Draft") -> "Working Notes".
- **Topology:** Direct (single bounded transformation).
- **Host Contract Check:** No injected tools for filesystem mutation observed at runtime boundary 2026-07-22 evidence cutoff.
- **File Observation:** Content of `notes.md` was not read via tool execution; assumed based on user prompt but unverified by live observation.

## Artifacts and state touched
- None (read-only access to package doctrine only).
- No file mutation occurred.

## Assumptions and unresolved facts
- **Assumption:** The file `notes.md` exists at the canonical root or a relative path accessible in this session context.
- **Unresolved Fact:** Whether "Draft" is currently present (user stated it, but I did not observe).
- **Capability Gap:** Missing write primitive for artifact mutation.

## Conflicts and downstream effect
- None observed. The only conflict is between the user's implied authority to mutate a file and the host's lack of tooling to perform that mutation.

## Verification and return condition
- **Checked:** Topology validity (Direct), Authority boundaries, Host contract limits.
- **Unverified:** Actual content of `notes.md` before edit; success of hypothetical write operation.
- **Next Move:** The root returns the prepared patch packet labeled below. If a file-write tool becomes available or this is an interactive session where I can execute code to modify files, dispatch that worker immediately. Otherwise, report terminal state: `PREPARED — NOT DISPATCHED`.

---

# Prepared Delegation Packet (Not Dispatched)
*This packet represents the exact work unit ready for execution if tools permit.*

```markdown
# Delegation Packet — `worker-rename-notes`

## Objective
Rename the heading in `notes.md` from "Draft" to "Working Notes".

## Deliverable and acceptance
- **Artifact:** `notes.md`.
- **Change:** The first-level header text changes exactly.
- **Acceptance:** File content diff shows old string removed, new string inserted; file hash updated.

## Context and sources
- **Source:** User request + implied presence of `notes.md` in workspace.
- **Current State:** Assumed "Draft" present (per user).

## Scope and ownership
- Included: Editing the specific header line in `notes.md`.
- Excluded: Any other files, formatting changes outside the heading text, or content deletion beyond the rename scope.
- Read surfaces: `notes.md` (current bytes required to verify "Draft").
- Write surfaces: `notes.md` (single-writer target).

## Authority and safety
- Allowed tools: File read/write primitives (if injected), string replacement logic.
- Network/External actions: None.
- Stop gates: If file does not exist or is locked, stop immediately with error code.

## Evidence burden
- Command result of the write operation.
- Hash comparison before and after to prove mutation.

## Return contract
Return success/failure status, exact bytes changed (diff), new hash, and any collision errors.

## Stop condition
Completion upon successful atomic update or failure due to missing tooling/authority.
```
