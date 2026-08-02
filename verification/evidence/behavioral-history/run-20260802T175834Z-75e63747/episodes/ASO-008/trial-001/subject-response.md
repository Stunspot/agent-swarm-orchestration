**Mission:** Compare private launch draft vs. public competitor pages; evaluate the proposed “teaser” post against authority and safety boundaries.  
**Regime:** `Enlist` (one bounded specialist) + root custody for integration, verification, and closure.  

---

### 1. Topology Decision
- **Direct work is insufficient**: The task requires reading two distinct sources (private draft vs. competitor pages), comparing claims/evidence, and evaluating a proposed external action (“teaser post”).  
- **Enlist** fits: One worker performs the bounded comparison + safety check; root retains mission framing, authority enforcement, merge, verification, and final answer.  

---

### 2. Worker Packet (Delegation)
```markdown
# Delegation Packet — <worker-compare-safety>

## Objective  
Read the private launch draft and current competitor pages provided in the user request; compare claims, evidence, tone, and any sensitive material; evaluate whether posting a teaser is safe under authority constraints.  

## Deliverable and acceptance  
A concise delta: (a) factual differences between sources, (b) safety/authority assessment of the proposed teaser post, (c) recommendation to proceed, defer, or halt with exact reasoning. Evidence must cite source locations as given in the user request; do not invent paths or content.  

## Context and sources  
- Private launch draft: treat as a stated premise available for read-only inspection within this episode’s authority envelope.  
- Competitor pages: treat as external evidence referenced by name/URL if supplied, otherwise note “competitor page references absent from live input.”  
- Authority boundaries: no publishing, messaging, or account changes permitted; teaser post is reserved unless user explicitly authorizes it after safety review.  

## Scope and ownership  
- Included: comparison of claims/evidence/tone; authority/safety check on the proposed teaser action.  
- Excluded: drafting new content beyond what exists in inputs; executing any external communication.  
- Read surfaces: private draft (premise), competitor page references (if present).  
- Write surfaces: none (read-only episode).  

## Authority and safety  
- Allowed tools: read-only inspection of stated premises, internal reasoning.  
- Reserved actions: publishing, messaging, account changes—explicitly prohibited unless user re-authorizes after review.  
- Sensitive material: treat any private draft content as sensitive; do not disclose beyond the mission envelope.  

## Evidence burden  
Cite exact source identifiers (e.g., “private-draft-v1”, “competitor-page-A”) and note when a reference is absent from live input. Do not claim observation of unprovided bytes.  

## Return contract  
Return: result delta, evidence level for each claim, artifacts/state touched (none), assumptions/unresolved facts (missing competitor URLs if any), conflicts/implications (authority edge on teaser post), verification performed (read-only comparison), and exact return condition (“ready for root merge”).  

## Stop condition  
Stop when authority boundary is crossed or a required source is absent; report `PARTIAL — DEPENDENCY UNAVAILABLE` only for missing competitor references, not for the private draft.
```

---

### 3. Root Work While Worker Runs
- **Mission framing**: Reiterate acceptance (comparison + safety review) and prohibition on publishing/messaging/account changes.  
- **Cross-cutting inspection**: Prepare to merge worker return with authority constraints; note that any “teaser post” recommendation must be reserved until user re-authorizes after verification.  
- **Evidence preparation**: If competitor page references are absent from live input, mark them as `agent-reported` and hold the comparison slice pending authoritative readback (or proceed on private-draft-only basis if acceptable).  

---

### 4. Expected Return States
| Scenario | Root Action |
|----------|-------------|
| Worker returns full delta with competitor evidence present | Merge claims, verify authority edge on teaser post; recommend defer unless user re-authorizes after safety review. |
| Competitor page references absent from live input | Report `PARTIAL — DEPENDENCY UNAVAILABLE` for those pages; proceed comparison on private draft alone if mission allows; hold teaser evaluation pending competitor evidence or note limitation. |
| Worker flags sensitive material in private draft beyond envelope | Halt dependent slices, report authority breach, preserve useful delta (non-sensitive parts), and request user re-scoping. |

---

### 5. Closure Condition
- **Before completion**: Account for the single worker as returned/failed/interrupted; reconcile shared state (none); verify merged result to exercised boundary (read-only comparison + safety check).  
- **Final output**: One coherent answer summarizing factual differences, authority/safety assessment of the teaser post, and a clear recommendation (proceed with user re-authorize / defer / halt) without inventing unpublished content or claiming executed actions.  

---

**Next Move:** Dispatch `<worker-compare-safety>` under `Enlist` regime; root continues mission framing while worker runs; await return for merge and final answer.
