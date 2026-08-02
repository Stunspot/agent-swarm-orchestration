**Mission:** Inventory 200 filenames and classify obvious extensions; resolve five ambiguous documents via a single qualified semantic read; root reviews that return to own release recommendations.  
**Topology:** `Enlist` (one bounded worker for the semantic slice).  

### Root Work (Direct)
- **Inventory & Classification:** The root performs deterministic listing, counting, hashing, and obvious metadata classification on all 200 filenames without spawning workers. This includes identifying files by extension patterns that are unambiguous (e.g., `.md`, `.py`) versus those requiring semantic inspection.  
- **State Custody:** Maintains the full source list and the boundary between classified vs. ambiguous items.  

### Worker Dispatch
**Worker ID:** `semantic-reader`  
**Objective:** Semantically read exactly five documents flagged as ambiguous by extension or content heuristics during root inventory.  
**Deliverable:** A bounded finding set containing: document identity, semantic summary of intent/structure, confidence score in classification, and any internal contradictions detected within the text itself.  
**Context & Sources:** The full list of 200 filenames (with obvious extensions already filtered out) plus the raw bytes or paths for only those five ambiguous documents. No other files are included to prevent answer leakage.  
**Authority:** Read-only access to the specific file contents; no write permissions, network calls, or external actions allowed.  
**Evidence Burden:** Return exact citations (paths), observed content summaries, and explicit unknowns if a document is unreadable or truncated.  
**Return Contract:** Result first, then evidence locations, touched state, assumptions made during reading, unresolved facts about the file's nature, conflicts with root inventory data, verification performed on readability, and return condition status (`returned` | `failed`).  

### Root Review & Closure
- **Integration:** The root observes the worker’s returned claims. Until that observation occurs, all findings from this slice remain `agent-reported`.  
- **Decision Logic:** Compare semantic intent against obvious extension labels; reconcile any discrepancies (e.g., a `.txt` file containing code). If the document is unreadable or evidence is insufficient to classify it meaningfully, mark it as unresolved and preserve that uncertainty.  
- **Output:** The root synthesizes one coherent recommendation on whether these five documents warrant release based solely on their semantic content and internal consistency. No generic tests, schemas, paths, sample data, or hypothetical downstream artifacts are drafted if the worker return is missing or ambiguous.  

### Terminal State
If the user requests a summary now:  
- **Completed:** Deterministic inventory of 200 files; one qualified worker dispatched for semantic analysis of five specific documents.  
- **Pending Verification:** The root has not yet observed the `semantic-reader`'s return in this episode (context-only constraint). All claims regarding those five documents remain `agent-reported`.  
- **Next Move:** Await authoritative readback of the worker’s result to finalize release recommendations, or proceed with degraded state if tools are unavailable.  

**Note:** No files changed; no external actions taken; no actual inspection results invented beyond what is stated as available case premises in this episode.
