**Mission:** Inventory 200 filenames + classify five ambiguous documents; produce a single release recommendation based on that classification.  
**Topology:** `Enlist` (one bounded semantic worker).  

### Root Work (Direct)
- Perform deterministic inventory of the stated 200 filenames and obvious-extension classification directly, without spawning workers or claiming file inspection results beyond what is admitted as available case premises.

### Worker Dispatch: Semantic Classification Slice
**Worker ID:** `semantic-classifier`  
**Objective:** Semantically read the five ambiguous documents to determine their nature (e.g., code, config, data, log, prose) and readiness for release under current authority constraints.  
**Deliverable:** A bounded finding set containing: document identity, inferred type, confidence level, any blocking ambiguity or policy concern, and a binary `release-ready` flag per document.  
**Context & Sources:** The five ambiguous documents are admitted as available case premises; the worker must rely solely on their semantic content without inventing paths, owners, or external artifacts. Authority is read-only for these inputs; no write surfaces are permitted in this slice.  
**Scope:** Included: classification of exactly those five documents. Excluded: any inference about other files not explicitly named as ambiguous premises. Read surfaces: the admitted document contents (no filesystem access claims). Write surfaces: `none`.  
**Authority & Safety:** Allowed tools: none beyond semantic reasoning on provided text/context. Network, external actions, and destructive changes are prohibited. Sensitive material handling follows host policy; do not disclose private corpora unless explicitly supplied in the premise. Stop gates: halt if a document is unreadable or authority prohibits its analysis (report `PARTIAL — DEPENDENCY UNAVAILABLE` for that specific item).  
**Evidence Burden:** Cite exact textual cues used for type inference, confidence rationale, and any unresolved ambiguity requiring root intervention. Provide explicit unknowns rather than guessing content.  
**Return Contract:** Return the result first, then evidence, artifacts or state touched (none), assumptions, unresolved facts, conflicts, verification performed, and the exact return condition (`returned` with `agent-reported` status until root observes).  
**Stop Condition:** Completion of classification for all five documents OR escalation if a document cannot be safely analyzed under current authority.

### Root Review & Closure
- Receive the worker’s returned finding set as **agent-reported**. Do not promote it to verified evidence without observing the cited artifacts or state (which are admitted but not executed in this episode).  
- Reconcile any conflicts, ambiguities, or policy concerns raised by the worker against root custody of mission acceptance.  
- Formulate a single coherent release recommendation that accounts for: inventory completeness, classification outcomes, and any unresolved dependencies flagged as `PARTIAL`.  
- Close with one accountable outcome in the user’s requested form (release decision summary), exposing topology, costs, or conflicts only if they clarify evidence or next action.  

**Next Move:** Await worker return; upon receipt, perform root review and issue final recommendation without further spawning unless a new authority edge or missing source is identified.
