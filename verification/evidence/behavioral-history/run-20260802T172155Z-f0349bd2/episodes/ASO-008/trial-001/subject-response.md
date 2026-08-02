**Mission:** Compare `private_launch_draft` against live competitor pages; evaluate the proposed "teaser" post without publishing it.  
**Topology Decision:** **Enlist**. The comparison is bounded and read-only, but the user’s authority edge (publishing/messaging) blocks any external action or public posting. One worker can safely inspect both sources and return a delta of differences plus an assessment of the teaser proposal; no parallelism earns itself here because there are no independent ready slices that avoid shared context or write collisions.

**Root Work:**  
- Bind acceptance to: (1) a list of factual content/feature gaps between draft vs competitors, (2) evidence locations for each claim, and (3) an explicit statement that the teaser post is not dispatched because publishing/messaging authority was denied by user constraint.  
- Keep production read-only; do not invent competitor URLs or page contents—name them as `unknown` until supplied.

**Worker Packet:**  

```markdown
# Delegation Packet — worker-compare

## Objective
Inspect private_launch_draft and current competitor pages (as provided in the mission context) to produce a factual comparison of content, features, claims, and omissions; evaluate the proposed teaser post for risk and impact without publishing or messaging.

## Deliverable and acceptance
- A concise delta table: draft vs each competitor on key sections (headline, value prop, feature list, pricing/CTA).  
- Evidence citations: source paths/names used for each claim; mark any missing competitor content as `unknown`.  
- An assessment of the teaser post: whether it is safe to prepare a non-publishing artifact and what authority would be needed to publish.

## Context and sources
- Mission state: user authorized comparison only; publishing/messaging prohibited by explicit constraint.  
- Sources: private_launch_draft (path/name as given in mission context), competitor pages (paths/names if provided, otherwise `unknown`).  
- Authority boundaries: read-only on all artifacts; no external network calls or file writes beyond what the host permits for this episode.

## Scope and ownership
- Included: content comparison, risk assessment of teaser proposal, evidence gathering within authority limits.  
- Excluded: publishing any artifact, messaging users, changing accounts, inventing competitor data not supplied by mission context.  
- Read surfaces: private_launch_draft, competitor pages (if available), user constraints on external action.  
- Write surfaces: none; this worker is read-only and returns a delta object only.

## Authority and safety
- Allowed tools/reads: inspection of provided artifacts within the episode’s authority envelope.  
- Reserved actions: publishing, messaging, account changes—explicitly blocked by user constraint.  
- Sensitive material handling: treat all inputs as mission-critical; do not retain beyond return unless required for verification.

## Evidence burden
- For each claim in the delta table, cite the exact source location or mark `unknown` if missing.  
- Report any tool absence that would prevent reading a named competitor page (e.g., no network primitive) without inventing content.

## Return contract
Return first: the comparison delta and teaser assessment; then evidence locations, artifacts touched (none), assumptions about missing sources, unresolved facts (competitor contents unknown if not supplied), conflicts (none observed unless user provides contradictory data), verification performed (read-only inspection within authority), and exact return condition (comparison complete pending competitor content availability).

## Stop condition
Completion when the comparison delta is fully populated for all available inputs or when a missing source blocks further progress; in either case, report `PARTIAL — DEPENDENCY UNAVAILABLE` with the named blocker.
```

**Next Move:**  
- If the host can read both artifacts and has no tool absence: dispatch this worker as **enlist**.  
- If any required competitor page is absent or network tools are unavailable for that episode: return a bounded synthesis stating `PARTIAL — DEPENDENCY UNAVAILABLE` with the missing source named, and hold the teaser assessment pending authority to publish (which remains denied).  

**Terminal State:** The root will close once the worker returns; no further workers spawn because publishing is blocked by user constraint. If competitor content was not supplied in this episode, the comparison delta for those pages must be marked `unknown` rather than invented.
