**Mission:** Compare user's internal "launch draft" against current competitor pages for strategic alignment and gap analysis.  
**Constraint:** No publication, no external messaging, no account changes, no public copy drafting.  
**Topology Decision:** `Direct` (single bounded worker). The task is a read-only comparison of two distinct sources; parallelism adds coordination cost without benefit here.  

---

### **Delegation Packet — `worker-compare-launch-vs-competitors`**

## Objective
Privately compare the user's internal launch draft against current competitor pages to identify strategic alignment, feature gaps, messaging differences, and potential competitive advantages or risks. Do not publish results, message anyone, change accounts, or draft external copy during this phase.

## Deliverable and acceptance
A concise comparison report containing:
- Feature/offerings matrix (user vs competitors)  
- Messaging tone and value proposition contrast  
- Identified gaps where user lags behind leaders  
- Opportunities to differentiate based on unique strengths  

Acceptance is met when the root can observe a structured delta between internal draft and competitor evidence, with explicit unknowns about any missing competitor data.

## Context and sources
- **Internal Draft:** Available as `launch-draft.md` (or equivalent artifact referenced by user).  
- **Competitor Pages:** Current public web pages of relevant competitors in the same domain or segment.  

Mark authority: read-only access to both internal draft and external competitor content; no write, network publication, or account modification permitted during this slice.

## Scope and ownership
- Included: Comparative analysis of features, pricing models (if visible), user-facing messaging, technical capabilities shown publicly, and perceived brand positioning.  
- Excluded: Internal strategy documents beyond the launch draft, confidential roadmaps not in the draft, private customer data, or any action that alters external state.  

## Authority and safety
- Allowed tools: Read-only file access to internal draft; read-only web browsing for competitor pages (if host permits).  
- Reserved actions: Publishing results, sending messages, modifying accounts, drafting public copy. These remain outside this worker's authority envelope until explicitly reauthorized by the user or root.  

## Evidence burden
Cite exact sections of the launch draft and specific claims observed on each competitor page used for comparison. Note any missing competitor data that prevents a full matrix (e.g., “Competitor X pricing not visible”).

## Return contract
Return:
1. The structured comparison delta;  
2. List of sources consulted with URLs or paths;  
3. Explicit unknowns about unavailable evidence;  
4. Any conflicts between internal claims and competitor reality;  
5. A recommendation on whether the draft needs adjustment before any future public action (e.g., teaser posting).  

## Stop condition
Completion occurs when all available competitor pages for the relevant segment have been inspected, or when further inspection yields diminishing returns relative to cost/latency. If a required competitor page is inaccessible due to tool limits, report `PARTIAL — DEPENDENCY UNAVAILABLE` with the exact method needed to access it (e.g., “browser fetch of https://competitor.com/page”).

---

### **Root Action Plan**
- Dispatch `worker-compare-launch-vs-competitors`.  
- While worker runs: root prepares acceptance criteria for future steps (e.g., teaser posting) and monitors tool availability.  
- Upon return, reconcile evidence levels; if any competitor data is missing, either request access or proceed with bounded conclusions labeled as such.  

**Status:** `planned` → awaiting dispatch via live host contract.
