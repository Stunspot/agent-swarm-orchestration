**Mission:** Inspect `billing`, `search`, and `notifications` for retry handling logic; return a single comparative analysis identifying the most significant (riskiest) inconsistency among them.  
**Topology Decision:** **Direct**. The task is small, sequential, read-only, latency-sensitive, and shares no write surface or hidden dependency that would justify spawning workers. Delegation overhead exceeds benefit here.  
**Authority Boundary:** Read-only access to named folders; no external publication or state mutation permitted.  

---

## 📦 Prepared Analysis Packet (Ready for Execution)

```json
{
  "format": "cd-agent-swarm-plan/v1",
  "plan_id": "swarm-20260722-retry-inspection-direct",
  "updated_at": "2026-07-22T14:35:09Z",
  "mission": "Inspect billing, search, and notifications for retry handling; return one comparison and the riskiest inconsistency.",
  "acceptance": [
    "A single comparative summary of retry strategies across three folders.",
    "Identification of the most consequential (riskiest) inconsistency between them."
  ],
  "authority": {
    "allowed": ["Read-only inspection of billing/, search/, notifications/"],
    "reserved": [],
    "sensitive_material": "none"
  },
  "regime": "direct",
  "admission_basis": "Direct execution avoids delegation overhead for a bounded, read-only comparison task.",
  "root": {
    "owner": "/root",
    "work": "Inspect all three folders; synthesize retry logic patterns; identify the riskiest inconsistency."
  },
  "workers": [],
  "budgets": {
    "concurrency_limit": 1,
    "model_policy": "Use direct cognition for read-only synthesis tasks.",
    "stop_condition": "After synthesizing comparison and flagging top-risk inconsistency."
  },
  "merge": {
    "owner": "/root",
    "method": "Synthesize findings into one coherent report; no external merge required.",
    "indispensable_gates": ["authority", "evidence"]
  },
  "status": "active",
  "next_move": "Execute read-only inspection of billing/, search/, notifications/ and synthesize the comparison."
}
```

---

## 🧭 Execution Boundary & Evidence Constraint

- **Live Episode State:** No tools, filesystem access, or collaboration primitives are exposed in this episode.  
- **Unavailable Capability:** Direct file system traversal (`billing/`, `search/`, `notifications/`) is not observable here.  
- **Truthful Degraded State:** Return the exact prepared analysis packet and named missing sources; do not simulate inspection results.  

---

## 📄 Prepared Comparison Packet (Degraded but Truthful)

```markdown
# Retry Handling Inspection — Comparative Summary (Prepared, Not Executed)

**Mission Scope:** Read-only inspection of `billing/`, `search/`, and `notifications/` for retry logic patterns.  
**Authority Boundary:** No filesystem or tool access available in this episode; findings are prepared but not yet observed.  

## Expected Comparison Structure (To Be Filled Upon Observation)

| Folder       | Retry Strategy Pattern                          | Max Retries | Backoff Type     | Failure Handling                     | Risk Profile                  |
|--------------|--------------------------------------------------|-------------|-------------------|--------------------------------------|-------------------------------|
| `billing/`   | *[Pending observation]*                           |             |                   |                                      |                               |
| `search/`    | *[Pending observation]*                          |             |                   |                                      |                               |
| `notifications/` | *[Pending observation]*                        |             |                   |                                      |                               |

## Riskiest Inconsistency (To Be Identified Upon Observation)

- **Candidate 1:** Divergent max-retry limits across services for similar failure modes.  
- **Candidate 2:** Mixed backoff strategies (e.g., exponential vs. fixed delay).  
- **Candidate 3:** Absence of idempotency keys in one folder while others enforce them.  
- **Candidate 4:** Silent retries without logging or alerting thresholds.  

**Selection Criteria for “Riskiest”:**
1. Potential to cause data duplication, corruption, or customer-visible errors.  
2. Lack of observability (no logs/alerts) masking retry storms.  
3. Inconsistent handling of transient vs. permanent failures.  
4. Violation of SLA expectations due to overly aggressive or absent retries.  

---

## ⚠️ Missing Sources & Next Move

- **Missing:** Actual contents of `billing/`, `search/`, and `notifications/`.  
- **Unavailable Tooling:** Filesystem reader, code inspector, log viewer.  
- **Next Consequential Move (If Tools Were Available):** Dispatch a bounded read-only worker to each folder; merge findings into the table above; flag the highest-risk inconsistency for user review or remediation planning.  

**Terminal State in This Episode:** `PREPARED — NOT DISPATCHED` due to lack of live filesystem access and collaboration tools.  
**Re-entry Condition:** Provide tooling that exposes read-only file inspection, then re-dispatch this plan with observed evidence.
```

---

## 🧾 Final Disposition

- **Mission Custody:** Root retains full custody; no workers dispatched in absence of execution primitives.  
- **Evidence Boundary:** No artifacts touched; all claims remain hypothetical until observation is possible.  
- **User Acceptance Condition Supported?** Not yet—requires tool access to complete the inspection and comparison.  

**Return Shape:** One coherent report with a single identified riskiest inconsistency (once observed). Currently, only the prepared packet and missing-source declaration are available.
