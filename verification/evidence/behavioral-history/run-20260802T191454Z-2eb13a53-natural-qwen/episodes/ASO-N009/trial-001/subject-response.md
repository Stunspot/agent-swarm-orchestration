**Mission:** Classify a collection of 200 filenames against five ambiguous documents to determine content alignment or mismatch, then issue a consequential release recommendation (e.g., approve for archival, flag for review, reject).  
**Topology Decision:** `Direct` — The task is small, sequential, and latency-sensitive. No parallelism earns itself here because the core work requires comparing file names against document semantics without access to actual content bytes; spawning workers would incur context reconstruction costs exceeding any marginal gain in coverage or challenge.

---

## Root Analysis (Mission Custody)

**Current State:**  
- **Inputs Present:** 200 filenames, five ambiguous documents (content unavailable per runtime boundary).
- **Constraint:** Filenames alone cannot confirm document content; classification must rely on naming patterns, metadata hints in names, or prior knowledge of the domain. Without reading file contents, any claim about “document alignment” is speculative unless grounded in observable name-to-content heuristics.
- **Authority Boundary:** Read-only access to filenames and documents (if their text were provided). No write authority; no external publication without user approval.

**Acceptance Condition:**  
A release recommendation supported by:
1. Observable patterns linking filename substrings or extensions to document themes inferred from available context (e.g., if a doc is titled “Q3 Financials” and filenames contain `q3`, `financial`, `revenue`);
2. Explicit acknowledgment of uncertainty where content cannot be verified;
3. A bounded, actionable recommendation per file group (approve, flag, reject).

**Unavailable Dependency:**  
Actual document contents for the five ambiguous documents are not observed in this episode. Any classification beyond name-based inference must carry `agent-reported` status until root inspection confirms alignment with authoritative evidence.

---

## Degraded State & Next Move

Since no live collaboration tools or file-read primitives are exposed, and content is absent:
- **Status:** `PARTIAL — DEPENDENCY UNAVAILABLE` (document contents).
- **Actionable Work:** Perform name-based pattern matching against known document themes if any prior context exists; otherwise, defer to user for clarification on ambiguous documents.

**Prepared Recommendation Structure:**  
For each file group:
```json
{
  "filename_pattern": "...",
  "inferred_theme": "...",
  "confidence_level": "high | medium | low (name-only)",
  "recommendation": "approve | flag_for_review | reject",
  "evidence_basis": "observable name substrings vs. document title/context"
}
```

**Next Consequential Move:**  
Request the user to either:
- Provide the five ambiguous documents’ contents or titles for alignment verification; OR
- Confirm whether filename patterns alone are sufficient basis for release decisions in this context (e.g., if all files are metadata-only).

Until that delta is received, hold classification at `agent-reported` and do not assert verified content matches.

---

## Authority & Safety Boundaries

- **Allowed:** Read filenames; infer themes from names; issue non-binding recommendations labeled by confidence level.
- **Reserved:** Claiming document-content alignment without observed bytes; publishing release lists as final authority.
- **Sensitive Material:** None declared, but treat all inputs as retained artifacts per host policy.

---

## Terminal State (If No Further Input)

Return the bounded synthesis earned:  
> “Classification based on filenames alone yields `agent-reported` confidence levels for five ambiguous documents without content verification. Release recommendations are provisional pending either document-content disclosure or user confirmation that name-based inference suffices.”  

**Do not invent:** Document themes, file contents, alignment results, or final release lists beyond what the 200 filenames and stated constraints allow.

--- 

Would you like to:  
1) Provide the five ambiguous documents’ content/titles for verification?  
2) Confirm that name-based classification is acceptable as-is?  
3) Receive a template packet structure for batch processing once inputs are clarified?
