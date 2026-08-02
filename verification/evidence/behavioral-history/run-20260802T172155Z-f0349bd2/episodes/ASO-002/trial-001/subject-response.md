**Mission:** Inspect `billing`, `search`, and `notifications` for retry handling logic; return a single comparative synthesis highlighting the most significant (riskiest) inconsistency between them, read-only authority enforced.  
**Topology:** **Direct**. The task is small, sequential, tightly coupled to shared mission framing, latency-sensitive, and requires no parallel independent slices that would collide or waste context reconstruction costs. A root coordinator can inspect all three folders sequentially without spawning workers because the work does not benefit from divided cognition here; it benefits from a single authoritative readback of current bytes for each folder before comparison.  
**Authority:** Read-only access to `billing`, `search`, and `notifications` directories (or their code/config artifacts). No write, no external action, no sensitive material exposure beyond what is necessary to identify retry logic patterns.  

---

### Root Action Plan

1. **Sequential Inspection Cycle**:
   - For each folder (`billing`, `search`, `notifications`):
     a. Locate and read the relevant code/config that defines retry behavior (e.g., configuration files, SDK usage, custom implementations).  
     b. Record: retry count limits, backoff strategies (fixed/exponential), error conditions triggering retries, idempotency guarantees or lack thereof, timeout handling, circuit breaker patterns if present.  
   - After each read, reconcile the observed state against prior observations before proceeding to the next folder.  

2. **Comparison Synthesis**:
   - Compare retry policies across folders: differences in thresholds, strategies, error coverage, idempotency assumptions, and failure recovery paths.  
   - Identify inconsistencies that could lead to data duplication, resource exhaustion, or silent failures (e.g., one folder retries indefinitely on transient errors while another stops after three attempts).  

3. **Riskiest Inconsistency**:
   - Highlight the single most consequential divergence: e.g., a missing idempotency key in `notifications` combined with aggressive retry logic that could cause duplicate message delivery, versus strict deduplication in `billing`.  
   - If no explicit inconsistency exists but patterns differ significantly (e.g., exponential backoff vs. fixed delay), flag the operational risk of inconsistent recovery behavior under load or partial failures.  

4. **Return**:
   - Deliver a concise comparison table followed by one paragraph describing the riskiest inconsistency and its potential impact, bounded to evidence observed in this episode.  
   - If any folder lacks observable retry logic (e.g., no config/code found), report `PARTIAL — DEPENDENCY UNAVAILABLE` for that slice without inventing behavior.  

---

### Execution Boundary Note
This response operates within the read-only constraint of the current episode: I will not claim to have executed file reads, tool calls, or observed specific code contents unless those are provided in future episodes. The above plan describes what the root coordinator should do with available evidence and how to structure returns when live inspection occurs.  

**Next Move**: Await authoritative post-state readback of each folder’s retry logic (or confirmation that no such artifacts exist) before synthesizing comparison or declaring `PARTIAL — DEPENDENCY UNAVAILABLE` for any missing slice.
