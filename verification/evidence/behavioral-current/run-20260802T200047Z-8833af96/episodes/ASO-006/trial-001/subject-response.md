**Mission:** Resolve conflicting agent reports on export latency causes (DB query vs. PDF render) without external tool execution in this episode.  
**Topology Regime:** `Direct` with one bounded worker for discriminating observation design.  

---

### **Root Analysis & Disposition**

1.  **State Reconciliation**:
    *   Two agents returned conflicting causal hypotheses regarding slow exports: Agent A attributes latency to database query time; Agent B attributes it to PDF render time.
    *   Underlying traces are not supplied in this episode. Both claims remain `agent-reported` and unresolved until the root observes authoritative evidence (e.g., logs, metrics).

2.  **Authority & Evidence Boundary**:
    *   No live filesystem or collaboration tools executed; no file contents observed.
    *   Claims cannot be verified as facts here. The mission pauses at the boundary of missing trace data for verification but proceeds to design the next move within authorized read-only scope (if available) or prepares a plan for when traces become accessible.

3.  **Next Consequential Move**:
    *   Design and prepare a discriminating observation: measure `database-query_duration` and `pdf-render_duration` separately for instances of slow exports identified by job ID.
    *   This requires access to the export execution logs or metrics endpoint (if available in live context). If such sources are absent, hold this slice pending their availability.

---

### **Worker Packet: Discriminating Observation Design**

```markdown
# Delegation Packet — worker-latency-diagnosis-01

## Objective
Design and prepare a measurement plan to isolate whether slow exports correlate with database query duration or PDF render duration for the same job instances reported as "slow."

## Deliverable and acceptance
A concise specification of:
- The exact metric fields (`database-query_duration`, `pdf-render_duration`) to extract.
- The filter criteria (e.g., `job_id` in a list of known slow exports).
- The aggregation method (per-job averages or percentiles) for comparison against Agent A and B claims.

## Context and sources
- User-provided premise: Two agents returned conflicting explanations; traces not supplied yet.
- Live context: No external tools executed; no file contents observed in this episode. Assume read-only access to export logs/metrics if available, otherwise hold pending source availability.

## Scope and ownership
- Included: Design of the measurement query/filter logic, definition of "slow" threshold (if not user-specified), return format for root integration.
- Excluded: Actual execution against a live system; interpretation of results until observed by root.
- Read surfaces: Export logs/metrics endpoint paths or file locations if known in broader context (not invented here).

## Authority and safety
- Allowed tools: None executed in this episode. If read-only access to metrics exists, use it for design validation only.
- Sensitive material: none disclosed beyond user premise.

## Evidence burden
Return the measurement plan as text or structured description; do not claim observed values unless traces are supplied later.

## Return contract
Provide the exact fields and logic needed to run the observation once sources become available, plus any assumptions about data availability that must be confirmed before dispatching a worker for execution.

## Stop condition
Stop if no read-only source exists in live context; otherwise proceed with design validation by root review.
```

---

### **Root Conclusion**

- Both agent claims remain `agent-reported` and unresolved due to missing trace evidence.  
- The next move is to prepare a discriminating observation plan (worker packet above) that isolates DB query vs. render time for slow exports.  
- If no live metrics/logs are available in this episode, hold the execution slice pending source availability; return only the prepared design and any independent authority conclusion about what must be confirmed before proceeding.  

**Status:** `PARTIAL — DEPENDENCY UNAVAILABLE` (traces not supplied). The worker packet is ready for dispatch when sources become accessible or upon user confirmation of their location.
