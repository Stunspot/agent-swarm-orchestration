**Mission:** Diagnose export latency (database vs. PDF rendering).  
**Topology Decision:** `Direct` with a single bounded worker to avoid coordination overhead for this specific, low-latency diagnostic task where shared context is heavy and write surfaces are read-only during inspection. Spawning two agents would waste tokens on duplicated reads of the same evidence without improving the causal diagnosis before merge costs exceed benefit.

**Root Action:**
1.  **Inspect Evidence Boundary:** Acknowledge that no live filesystem, logs, or metrics were observed in this episode (per `source-and-currentness-register.md` and runtime conditions). Claims about "database queries" vs. "PDF rendering" are currently unverified hypotheses without cited artifacts (e.g., query plans, render times, thread dumps).
2.  **Prepare Delegation Packet:** Construct a single worker packet to investigate the *entire* export pipeline end-to-end under read-only authority. This avoids splitting work on shared state before reconciliation.
3.  **Execute/Report Degraded State:** Since no live tools or logs are available in this episode, return the prepared analysis and stop artifact-specific claims at that evidence boundary (`PARTIAL — DEPENDENCY UNAVAILABLE` for specific metrics).

---

# Agent Return: Root Coordinator Analysis

**Disposition:** `returned | capability-limited (live execution)`  
**Result:** The user's request to "give me the answer" cannot be resolved with a definitive causal diagnosis because no live evidence (logs, traces, or artifacts) was observed in this episode. Both hypotheses ("database queries" and "PDF rendering") remain unverified claims without cited sources like query plans (`EXPLAIN ANALYZE`), render timings, or thread stack traces.

**Evidence:**
-   **Missing Source:** Live export logs, database metrics (e.g., `pg_stat_activity`, slow query log), PDF generation service telemetry, and application performance profiles were not observed in the episode context.
-   **Agent-reported vs Observed:** The user's premise ("One blames X; one blames Y") represents agent reports or external claims without root observation of the underlying bytes or metrics. Per `evidence-merge-and-review.md`, these remain `agent-reported` until verified by a discriminating check (e.g., comparing query duration to render duration).
-   **Unavailable Dependency:** The specific evidence required to distinguish cause from amplification is absent in this non-interactive episode.

**Assumptions and unresolved facts:**
-   Assumption: Export slowness exists and requires attribution.  
-   Unresolved fact: Which layer (DB or Render) contributes the majority of latency? Is there contention, locking, network I/O, or serialization overhead? Without metrics, we cannot distinguish cause from correlation.

**Conflicts and downstream effect:**
-   **Conflict:** Competing hypotheses without consensus theater (`competing-hypotheses-example.md`). One agent claims DB; another claims PDF. Neither has presented evidence that overrides the other in this episode.  
-   **Effect:** The root must hold both possibilities as unverified until a discriminating observation is made (e.g., "If we disable rendering, does latency drop?").

**Verification and return condition:**
-   **Check performed:** None; no live tools or logs were accessible to execute `validate_swarm_plan.py` against actual data.  
-   **Unverified:** The causal chain linking the slow export to a specific component is unobserved.  
-   **Next move (Root-owned):** Prepare a diagnostic packet that instructs an external agent (or user) on how to gather the missing evidence:
    1.  Capture query execution plans and durations for the export transaction.
    2.  Measure PDF rendering time in isolation vs. combined with DB fetches.
    3.  Check thread contention or I/O wait states during the export window.

**Bounded Conclusion:**  
Without live evidence, neither hypothesis is accepted as truth. The root cannot claim "database queries" are slow without seeing a query plan exceeding thresholds, nor can it accept "PDF rendering" blame without timing data.  

**Terminal State:** `PARTIAL — DEPENDENCY UNAVAILABLE` (specifically: missing log/metric sources).  
**Prepared Action:** Return the exact diagnostic packet below that defines what evidence is needed to resolve this conflict and how to integrate it once observed externally.

---

# Prepared Diagnostic Packet (for external execution)

```markdown
# Delegation Packet — diag-export-latency-01

## Objective
Isolate whether export latency stems from database query overhead or PDF rendering bottlenecks by measuring each stage independently under read-only authority.

## Deliverable and acceptance
A causal diagnosis supported by:
- Query duration vs. render duration breakdown (e.g., 80% DB, 20% Render).
- Evidence of contention (locks) or I/O saturation during the export window.
- A prepared patch if one stage is confirmed as the bottleneck.

## Context and sources
- **Sources:** Export logs, database slow query log (`pg_slow_query.log`), PDF service metrics, thread dumps from the application server.
- **Authority:** Read-only access to these artifacts; no write permission for production systems (per `authority`).  
- **Scope:** The specific export job that exhibited slowness in the user's report.

## Scope and ownership
- Included: Timing breakdown of DB fetch, serialization, PDF generation, and network egress.
- Excluded: General system load unrelated to this export; unrelated jobs running concurrently unless they share resources (e.g., same disk queue).
- Read surfaces: `/var/log/app/export.log`, database slow query log, application metrics endpoint (`/metrics`).
- Write surfaces: `none` (read-only inspection only).

## Authority and safety
- Allowed tools: Log parsing, metric scraping.  
- Reserved actions: No production writes; no schema changes to test hypotheses in live systems without user approval.  
- Sensitive material: None declared beyond standard logs/metrics.  

## Evidence burden
- Required source locations: Paths to the export job's log files and database metrics for that specific run ID.
- Commands/tests: `grep <job-id> /var/log/app/export.log | awk '{print $NF}'` (to extract durations), or equivalent metric queries.

## Return contract
Return the result first, then evidence, artifacts touched, assumptions, unresolved facts, conflicts, verification performed, and exact return condition. Provide concise rationale for why one hypothesis is favored over another based on observed timings.

## Stop condition
Stop if:
- Evidence confirms a single dominant bottleneck (e.g., query > 90% of total time).
- User revokes authority or cancels the mission.
```
