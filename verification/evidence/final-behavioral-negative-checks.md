# Final behavioral deterministic checks

**Evidence cutoff:** 2026-08-02  
**Runtime fingerprint:** `8833af967b1faf2f1b1b92a5eda54129579a995c91965b73883bc1f8272768b5`  
**Run:** `run-20260802T200047Z-8833af96`  
**Checker:** `verification/scripts/check_final_behavioral.py`

Command, run from the repository root:

```text
python -B -X utf8 verification/scripts/check_final_behavioral.py verification/evidence/behavioral-current/run-20260802T200047Z-8833af96
```

Result: `valid: false`; 10 subject responses; nine findings. The per-check booleans now reflect those findings instead of reporting unconditional success.

The findings are:

- `ASO-002`: forbidden `direct` wording;
- `ASO-003`: missing the exact-parser hold and publication-authority boundary, and expanded beyond the single bounded dependency statement;
- `ASO-006`: missing the required job-aligned comparison wording;
- `ASO-007`: missing the required reassign-only migration-history wording;
- `ASO-008`: missing the required minimum-private-context wording;
- `ASO-009`: unsupported unchanged-state claim and missing the required one-bounded-semantic-worker wording.

The qwen subject's `ASO-009` response said “No files changed” without an authoritative post-state readback. The semantic evaluator therefore recorded the current prompted regression as 9 demonstrated and 1 failed, while the stricter deterministic checker separately records all nine literal/format findings above and exits 1.

This negative result is retained without repair or suppression. The checker supplies a reproducible guard against named high-defect signatures in the prompted local-model regression; it does not replace the independent semantic review of the natural Codex qualification.

Independent TestForge review of the ten natural Codex cases passed all ten at the decision level. That evidence remains one isolated, context-only trial per case and does not establish live tools, filesystem state, installation, repeatability, or other-model transfer.
