# Verification report

## Decision

**Status:** `READY_WITH_RESIDUAL_RISK`  
**Target:** Agent Swarm Orchestration 0.1.0  
**Runtime fingerprint:** `8833af967b1faf2f1b1b92a5eda54129579a995c91965b73883bc1f8272768b5`  
**Documentation fingerprint:** `b82a71589301372d941b182c93d5434b28cb1ced6e5a163b0583215f7028223c`  
**Release ZIP SHA-256:** `1889b0b1f20a4cc98c9ccf3c95d7a1b64cea0e4524cf3e16b00b90ccd2cf6683`  
**Evidence cutoff:** 2026-08-02  
**Independent TestForge review:** `REVIEW_PASS`; all five recorded conditions closed  
**Independent documentation review:** `REVIEW_PASS`

The evidence supports private Codex source custody with explicit residual risk. It does not support installation health, clean-host discovery or invocation, repeatability, live collaboration-tool behavior, public publication, customer readiness, universal model transfer, or customer outcomes.

## Scope and exclusions

Included: canonical and released Codex runtime, portable release ZIP, validator and tests, 20 eval definitions, natural Codex decision qualification, honest qwen regression evidence, eight customer documents, Hesperos provenance, independent documentation review, package parity, and private-custody release readiness.

Excluded: other harnesses; the parked automated cross-harness testing and repair direction; installation; clean-host discovery and invocation; live external actions; public publication; accessibility conformance in a specific renderer; and customer outcomes.

## Current evidence

| Evidence | Result | Authority |
|---|---|---|
| Validator unit suite | 10 passed | deterministic validator behavior |
| Packaged Swarm Plan template | `VALID cd-agent-swarm-plan/v1` | declared plan structure |
| Skill Creator | PASS | skill structure |
| Augment Builder canonical Codex | PASS | canonical runtime package |
| Augment Builder released Codex | PASS | released runtime package |
| Augment Builder bundle | PASS | product bundle structure |
| Eval definitions | 20 valid cases across 11 dimensions | case structure only |
| Canonical/release comparison | 17 files each; zero path or byte mismatches | exact local runtime parity |
| Release ZIP | 17 entries; one portable top-level directory; direct `SKILL.md`; zero backslash names; zero content mismatches | exact local asset topology and bytes |
| Natural Codex qualification | 10 of 10 cases passed independent TestForge semantic review | one isolated decision-only trial per case |
| Exact-fingerprint prompted qwen regression | 10 valid; 9 demonstrated; 1 failed; mean 90 | negative smaller-model regression evidence |
| Natural qwen qualification | 9 valid; 5 demonstrated; 2 partial; 2 failed; 1 invalid | negative smaller-model transfer evidence |
| Hesperos authorship | PASS; zero findings | exact eight-document provenance |
| Hesperos lint | 8 of 8 PASS | Markdown accessibility heuristics |
| Independent documentation review | `REVIEW_PASS`; no actionable findings | fresh documentation challenge |
| TestForge manifest and traceability | valid; zero errors and zero warnings | risk-to-scenario-to-test-to-execution structure |

The current prompted regression is retained under `verification/evidence/behavioral-current/run-20260802T200047Z-8833af96/`; its 104 copied files were observed byte-identical to the originating run. The natural Codex prompts, raw returns, model and task identities, and independent case dispositions are retained in `verification/evidence/codex-natural-qualification.md` and `verification/testforge-review.md`.

## Behavioral disposition

Independent TestForge review passed `ASO-N001` through `ASO-N010` at the decision level. The three prior semantic blockers were repaired: redirect compliant active workers before interrupting noncompliance, avoid excessive small-batch sharding, and minimize disclosure of private draft material.

The natural qualification did not execute collaboration tools, inspect the referenced artifacts, mutate files, transmit private context, or repeat trials. The exact-fingerprint qwen regression remains `NOT_DEMONSTRATED` because `ASO-009` asserted that no files changed without authoritative post-state readback. The deterministic checker correctly exits 1 on that retained response.

Earlier prompted qwen 10-of-10 evidence is historical coached regression only. Its prompts disclosed target behavior and it is not transfer evidence.

## Residual risks

- One isolated decision-only natural Codex trial per case does not establish repeatability or live tool behavior.
- Worker qualification and privacy minimization were specified rather than operationally exercised.
- Qwen transfer remains negative and inconsistent.
- Filesystem mutation, browsing, clean-host installation, discovery, invocation, health, and accessibility conformance in a specific renderer were not exercised.
- Current Codex collaboration-tool contracts can drift and must be inspected live before dispatch.
- Public publication and customer outcomes remain outside authority and evidence.

## Release boundary

This record freezes a verified private release candidate. Repository commit, immutable `v0.1.0` tag, private GitHub release asset readback, recovery backup, and live Skill Estate re-entry are subsequent custody receipts. Installation and public publication are not authorized.
