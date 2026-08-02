**Mission:** Inventory 200 filenames + classify five ambiguous documents; produce a single release decision based on that classification.  
**Topology:** `Enlist` (one bounded semantic worker).  

### Root Work (Direct)
- Perform deterministic inventory of the stated 200 filenames using only case premises: list them as known, note obvious extensions where provided in the premise, and mark any extension-less or ambiguous entries for the single qualified worker.  
- Do not claim actual filesystem reads; treat all listed names/ambiguities as available case premises per runtime boundary.  

### Worker Dispatch (Enlist)
**Worker ID:** `doc-classifier`  
**Objective:** Semantically read exactly five ambiguous documents, determine their content class and release eligibility under the mission’s acceptance condition.  
**Deliverable:** A bounded return containing: document identifier, inferred semantic category, evidence citations (source locations/claims), unresolved facts, conflicts if any, and a clear recommendation on whether to include or exclude each from release.  
**Context & Sources:** The five ambiguous documents as case premises; the root’s inventory list of filenames for cross-reference only where needed. No hidden rubric or expected verdict is provided—only the raw premise that these files exist and are ambiguous until classified.  
**Authority:** Read-only access to document content (as supplied in the episode); no external publication, write actions, or production changes permitted without explicit user authority.  
**Evidence Burden:** Cite exact source locations for claims; distinguish agent-reported findings from root-observed state. If a required byte is missing despite premise availability, report `PARTIAL — DEPENDENCY UNAVAILABLE` and stop that slice’s downstream steps.  
**Return Contract:** Result first (classification + recommendation), then evidence, artifacts touched, assumptions, unresolved facts, conflicts, verification performed, and exact return condition.  
**Stop Condition:** Completion of all five classifications or early halt if a dependency is missing; do not draft the final release list before this worker returns.  

### Root Review & Closure
- Receive `doc-classifier`’s return as **agent-reported**.  
- Inspect cited evidence only where available in the episode; retain any claim that remains unobserved as agent-reported until root verification occurs (which it does not here).  
- Synthesize a bounded conclusion: name what workers reported, note which claims remain unverified due to lack of live observation, and state whether the mission can close now or requires re-entry.  
- Do not invent findings, file contents, paths, owners, patches, commands, worker returns, or completion states beyond what is stated in the user request and episode premises.  

### Next Move
Dispatch `doc-classifier` with the packet above; while it runs, root continues mission framing (inventory cross-check) without waiting for status metronomes. Upon return, reconcile claims against authoritative evidence boundaries and close with one accountable outcome or a truthful degraded state if dependencies remain unobserved.
