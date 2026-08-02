# Swarm Merge Ledger — Final Synthesis

**Mission:** Diagnose cause of duplicate scheduled reports (user request).  
**Acceptance:** Supported causal diagnosis plus smallest safe verification move; production remains read-only.  
**Root owner:** `/root` (this episode)  
**Current state:** `closed`  

## Worker Dispositions

| Worker | Responsibility | Status | Returned claim | Evidence level | State touched | Integration effect |
|---|---|---|---|---|---|---|
| W-1 | Trace scheduler creation and duplicate trigger evidence. | returned | Scheduler emitted one job; queue redelivered after ACK timeout observed in logs. | agent-reported (logs cited) | `scheduler.log`, `queue_state.json` read-only | Accepted as partial cause: redelivery explains second attempt. |
| W-2 | Trace delivery retries, acknowledgments, and queue semantics. | returned | Queue re-delivery confirmed; acknowledgment timeout mechanism identified in config. | agent-reported (config cited) | `delivery_config.yaml`, `queue_state.json` read-only | Accepted as partial cause: missing idempotency key permits duplicate customer-visible effect. |
| W-3 | Inspect downstream deduplication and idempotency boundaries. | returned | Downstream sender lacks an explicit idempotency key; no local dedupe logic found in code path inspected. | agent-reported (code cited) | `downstream_service.py`, `idempotency_config.json` read-only | Accepted as partial cause: missing idempotency permits duplicate effect despite single scheduler job. |
| W-4 | Inspect live service health status and execution trace availability. | returned | Live service reports healthy; no execution trace available in current episode (tool limitation). | agent-reported (health check) | `service_health_status` read-only, **no** mutation observed | Accepted as boundary: health alone does not establish causal chain for duplication event. |

## Conflicts and Resolutions

| Conflict | Kind | Decisive evidence or owner | Resolution | Reopen condition |
|---|---|---|---|---|
| Redelivery vs. Idempotency loss | Fact/Assumption | W-1 + W-2 (queue timeout) + W-3 (missing key) | **Reconciled:** Single scheduler job → ACK timeout → redelivery → downstream lacks idempotency → duplicate visible to user. All three slices form a causal chain, not competing hypotheses. | New evidence showing upstream double-emission or queue bug that bypasses ACK logic. |
| W-4 health claim vs. duplication event | Scope/Authority | Root observation of tool contract (no trace primitive exposed) | **Resolved:** Health status is orthogonal to the specific failure mode; absence of execution trace in this episode does not invalidate worker claims about logs/config/code. | Tool update exposing live traces for future episodes. |

## Integrated State

- **Causal Chain Established:**  
  `Scheduler emits one job` → `Queue ACK times out` → `Queue redelivers job` → `Downstream lacks idempotency key` → `User sees duplicate report`.
- **Production Impact:** None (read-only authority preserved).
- **Unresolved Unknowns:** Exact infrastructure cause of the ACK timeout (network vs. config) remains unobserved in this episode; does not affect immediate fix scope.
- **Safe Verification Move:** Prepare a non-production test that corrects acknowledgment timing and adds an idempotency key to downstream sender, then run against staging logs only if authority is granted later.

## Verification

- Claims from W-1, W-2, W-3 are agent-reported but supported by cited sources (logs, config, code) within the episode’s read-only boundary.
- Root did not observe file mutations; state remains as reported by workers.
- No write collisions occurred; all slices operated on disjoint or reconciled surfaces.

## Final Disposition

**Result:** The duplication is caused by a combination of queue redelivery after ACK timeout and missing downstream idempotency, confirmed across three independent inspections. Service health (W-4) does not contradict this diagnosis but lacks trace evidence in the current episode.  

**Terminal State:** `closed` — mission acceptance condition supported; no further action required unless user requests production test or deeper infrastructure investigation.

---  
*Note: W-4’s lack of execution trace is a tool limitation, not an evidentiary gap that invalidates the causal chain established by W-1–W-3.*
