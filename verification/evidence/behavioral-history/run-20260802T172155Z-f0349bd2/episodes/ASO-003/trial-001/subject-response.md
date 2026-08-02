### 1. Identify Parser Ownership (Direct Analysis)

The request asks to "identify" a specific artifact: **the parser owning the `customer-import` format**.

**Current Evidence Boundary:** The live episode contains no file system, repository state, or prior mission history regarding this task. No artifacts named `customer-import`, nor any associated parsers, are present in the provided context.

**Authority & Capability Check:**
-   **Mission Custody:** I hold custody of the user's request to identify and test a parser for an unknown format.
-   **State Custody:** The state is empty regarding this specific domain object (`customer-import`).
-   **Tool/Execution Boundary:** No tools are injected that allow me to inspect external repositories or read files not explicitly provided in the episode context. I cannot "discover" which parser owns a file unless its path and content were supplied as evidence.

**Conclusion on Ownership:** The specific identity of the parser owning `customer-import` is **unobserved**. Claiming an owner (e.g., "Parser X") without observing it would be inventing state, violating the doctrine: *"Do not claim tools... or execution beyond what that episode states"* and *"Never report AWAITING AUTHORITY when the user already authorized the action but the host cannot perform it."*

**Disposition:** `PARTIAL — DEPENDENCY UNAVAILABLE` (The source defining the parser ownership is absent).

---

### 2. Design Tests for That Exact Parser (Chain/Enlist Strategy)

Since I cannot identify a specific existing parser, I must proceed by **designing the test structure** that *would* validate such a parser once its identity or implementation becomes known. This aligns with the directive: *"Return only the named missing source... and any independent authority conclusion."*

I will adopt an **Enlist** topology for this slice because it is bounded, sequential (identify -> design), and does not require parallelism to improve outcome here; adding workers would increase cost without reducing uncertainty about a non-existent input.

#### Proposed Delegation Packet: `design-parser-tests`
This packet defines the *contract* required from any parser that claims ownership of `customer-import`. It establishes the acceptance criteria for future verification once the specific implementation is located or provided.

**Packet Content:**

```markdown
# Delegation Packet — design-parser-tests

## Objective
Define a test suite contract and structural requirements for validating an arbitrary parser handling the `customer-import` format, ensuring robustness against malformed inputs, encoding variations, and schema drift before integration into production ingestion pipelines.

## Deliverable and acceptance
A structured specification (or code skeleton) defining:
1.  **Unit Test Cases:** At least one positive case (valid import), two negative cases (malformed CSV/JSON/XML depending on format guess), and boundary conditions (empty file, max row limit).
2.  **Schema Validation Logic:** A mechanism to assert that parsed rows conform to the expected entity model (e.g., `Customer`, `Order`).
3.  **Idempotency Check:** Verification logic ensuring duplicate imports are handled gracefully or rejected based on policy.

## Context and sources
-   **Target Artifact:** The file path or content stream for `customer-import` is currently unknown/unavailable in this episode.
-   **Authority:** Read-only access to the parser implementation once located; write-access restricted to generating test artifacts (mock files) within a sandbox directory if tools permit, otherwise purely conceptual design.

## Scope and ownership
-   **Included:** Designing the *interface* for testing `customer-import` parsing logic. Defining input/output schemas required by tests.
-   **Excluded:** Implementing the parser itself; executing tests against live production data (prohibited); modifying existing customer records in a database.

## Authority and safety
-   **Allowed tools:** None currently active beyond text generation for this packet. If file-write primitives are available, generate mock test files to `sandbox/customer-import-tests/`.
-   **Read surfaces:** The unknown parser implementation path (to be supplied).
-   **Write surfaces:** Mock data generators only; no production writes allowed.

## Evidence burden
The resulting design must specify:
1.  Input file paths for unit tests.
2.  Expected JSON/YAML output structure of the parsed result.
3.  Error handling signatures (exception types or status codes) returned on parse failure.

## Return contract
Return a text-based description of the test cases, including sample input data and expected outputs/exceptions. If file-write tools are unavailable, return the design as code blocks ready for implementation in an IDE environment. Explicitly state that execution has not occurred due to tool absence (`CAPABILITY-LIMITED` on execution).

## Stop condition
Completion when the test contract is fully specified or authority/tools prevent further elaboration without user intervention.
```

---

### 3. Root Synthesis and Next Move

**Integrated State:**
-   **Mission Status:** `active` (but bounded by missing source evidence).
-   **Topology Decision:** Direct/Enlist hybrid. The root performs the analysis of constraints; a single worker slice is prepared for test design once inputs are known or simulated.
-   **Evidence Level:** Agent-reported intent only. No actual parser observed, no tests executed.

**Final Conclusion & Next Move:**
The specific owner of `customer-import` cannot be identified from current evidence because the artifact and its owning code path were not supplied in this episode's context. I have prepared a bounded delegation packet (`design-parser-tests`) that defines exactly what must be tested once the parser is located or simulated.

**Next Action:** Await user provision of:
1.  The file path to `customer-import` (or content).
2.  Or, authorization for me to simulate/mock this format using a hypothetical schema if no real source exists.

Until then, I hold the prepared test design pending and do not claim any parser ownership or execution results.
