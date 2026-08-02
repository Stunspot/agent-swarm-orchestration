**Mission:** Resolve conflicting agent reports on export latency causes without external evidence.  
**Topology:** `Direct` (root-only synthesis; no workers dispatched).  

### Current State Summary
- **Agent A Claim:** Latency correlates with database query time (`agent-reported`).  
- **Agent B Claim:** Latency correlates with PDF render time (`agent-reported`).  
- **Evidence Level:** Unverified conflict. Traces are absent from the live episode; no authoritative readback exists to reconcile claims.  

### Next Move
The root holds both claims as unresolved and prepares a discriminating observation: measure `database-query_duration` and `pdf-render_duration` aligned by job for slow exports only. This isolates causality without editing production or inventing paths/tools unavailable in this episode.

**Disposition:**  
- **Status:** `active — awaiting-evidence` (discriminating measurement pending).  
- **Authority Boundary:** Read-only analysis of existing traces; no write access to logs, databases, or renderers assumed absent unless stated otherwise.  

### Closure Condition
Complete when either:  
1. Measurement data confirms one cause dominates and the other is noise/secondary effect; OR  
2. Data shows both contribute significantly (multi-factor latency), requiring decomposition into sub-slices if further resolution is authorized.

**Note:** No workers were spawned because the task requires a single discriminating observation rather than parallel hypothesis testing, and no external tools or trace sources are available to execute in this episode. The root retains custody of mission framing, evidence integration, and final acceptance.
