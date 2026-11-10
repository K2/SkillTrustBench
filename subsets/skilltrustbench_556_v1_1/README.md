# SkillTrustBench — Fixed 556-Case Subset, v1.1

This package contains the same 556 stable case IDs used by the v1.0 public
leaderboard, updated for three-class evaluation.

## v1.1 distribution

- malicious: 316
- suspicious: 74
- normal: 166

The v1.0 distribution was 285 malicious / 105
suspicious / 166 normal.

## What changed

1. **31 judgments** changed from `suspicious` to `malicious` after semantic
   adjudication of deceptive concealment, instruction override, and related
   attack-intent cases.
2. **44 risk-label sets** were corrected.
3. **228 case directories** use quality-rewritten content. Rewrites naturalize
   carrier names and paths and integrate payloads more realistically while
   preserving the intended security behavior. The remaining 328 directories
   retain their v1.0 content.
4. The full 5,520-case v1.1 release is in preparation. Until it is published,
   the full-corpus `benchmark_full_v1.0.zip` remains the current full benchmark.

## Files

- `ground_truth.jsonl` / `ground_truth.json`: v1.1 labels and audit metadata.
- `case_manifest.jsonl`: original vs quality-rewritten source for every case.
- `metrics.json`: v1.0/v1.1 reference metrics.
- `cases/`: self-contained case directories.

## Reference scanner continuity

| labels | accuracy | macro F1 | suspicious F1 |
| --- | ---: | ---: | ---: |
| v1.0 | 0.853 | 0.820 | 0.675 |
| v1.1 | 0.815 | 0.758 | 0.522 |

Binary non-normal membership is unchanged: all 31 promotions stay inside the
non-normal class.

## Safety

Contains intentionally malicious and vulnerable skills. Inspect only in a
restricted, disposable sandbox. Do not install, import, or execute any case.
