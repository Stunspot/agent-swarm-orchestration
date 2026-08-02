**Mission:** Inventory 200 filenames + classify five ambiguous documents; produce a single qualified release recommendation based on that classification.  
**Topology:** `Enlist` (one bounded semantic worker).  

### Root Work (Direct)
- Perform deterministic inventory of the stated 200 filenames and obvious-extension classification without invoking tools or reconstructing bytes.  
- Maintain mission custody, acceptance condition (“release recommended only after qualified document review”), authority envelope (read-only on inputs; no external publication), evidence level (`agent-reported` for worker claims until root observes them).  

### Worker Packet
**Worker ID:** `doc-classifier-a`  
**Objective:** Semantically read the five ambiguous documents and produce a bounded classification delta.  
**Deliverable:** A concise return containing: (1) per-document label with confidence, (2) evidence citations (source locations or excerpts), (3) unresolved facts/assumptions, (4) conflicts if any, (5) touched state summary, and (6) the exact stop condition met.  
**Context & Sources:** The five ambiguous documents as stated premises; no reconstruction of their bytes is required—treat them available per case premise. Include only mission framing, vocabulary for classification, prior decisions on release policy, and authority boundaries in this packet.  
**Scope:** Included: semantic interpretation of the five documents against the inventory context. Excluded: any external network actions, writes to shared surfaces, or speculation beyond the stated premises. Read-only access; no sensitive material disclosed.  
**Authority & Safety:** Allowed tools: none (context-only episode). Reads: logical references to the five documents only. Writes: `none`. External actions: prohibited. Stop gates: halt if a document is truly unavailable despite case premise, or if authority revokes release recommendation.  
**Evidence Burden:** Return must cite exact source identifiers for each claim; mark any missing evidence as unknown without inventing paths.  
**Return Contract:** Result first (classification delta), then evidence and state summary; concise rationale sufficient to review the decision.  
**Stop Condition:** Completion upon return of all five classifications or escalation if a document is genuinely unobservable despite premise.  

### Merge & Verification Plan
- Root observes `doc-classifier-a`’s return before any release recommendation.  
- Reconcile claims against mission acceptance: only proceed to “release recommended” when the worker’s evidence supports it and no unresolved facts block integration.  
- If conflicts arise (e.g., contradictory labels), preserve them as agent-reported until a discriminating observation or user decision resolves them.  

### Next Move
Dispatch `doc-classifier-a` with the packet above; continue root work on inventory framing while awaiting return. Upon receipt, reconcile and issue one coherent release recommendation bounded by observed evidence.
