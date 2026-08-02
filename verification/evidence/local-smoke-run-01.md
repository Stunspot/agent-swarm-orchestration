# Local behavioral smoke run 01

**Run ID:** `run-20260722T201827Z-35b5ad94`  
**Package fingerprint:** `35b5ad944b73d5b1a7775a8bd0364ed5914f496e6adf161e1f702c87fbbad4d2`  
**Runtime:** `ollama-context / qwen35:latest`  
**Cases:** `ASO-001`, `ASO-004`, `ASO-006`, `ASO-008`, `ASO-010`  
**Trials:** one per case

## Result

- Run status: `COMPLETE`
- Valid episodes: 5 of 5
- Mean score: 93.33
- Demonstrated: 3
- Partial: 2
- Failed: 0
- Invalid: 0
- Claim status: `PARTIAL`

The partials exposed two repairable transfer defects:

1. `ASO-004` preserved single-writer ownership but proposed clarity before technical correction instead of establishing correctness first.
2. `ASO-008` correctly reserved publication authority but stopped to request permission instead of completing the authorized private comparison.

The canonical skill was revised after this run. This receipt is regression input, not evidence for the revised fingerprint.

## Preserved evidence

The raw run was retained outside the distributable because generated prompts and execution metadata contain machine-specific absolute paths. Integrity anchors for that preserved run are:

- `summary.json`: `ca62a5eaeae617b57219c74b68f9ea2e9b46a7ad7acaa3a9bfb8123a895f0e1b`
- `run.json`: `1ab077e64ca8e2e94348f2b1e5d8b0660cb3b706da5a211bfd933a73af3824ff`
- `suite.json`: `846053e525fd7779e51034a4b30a5b64a8c3d599968ca8b000c3364facad082f`

## Claim boundary

This context-only local-model smoke run checks response transfer against five declared cases. It does not exercise Codex collaboration tools, install or discover the skill, establish customer outcomes, or prove behavior across untested models and tasks.
