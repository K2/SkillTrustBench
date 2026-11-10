---
license: cc-by-4.0
pretty_name: MaliciousSkillBench
configs:
  - config_name: primary
    default: true
    data_files:
      - split: train
        path: primary.parquet
  - config_name: metadata
    data_files:
      - split: train
        path: metadata.parquet
  - config_name: attack_taxonomy
    data_files:
      - split: train
        path: attack_taxonomy.parquet
  - config_name: impact_taxonomy
    data_files:
      - split: train
        path: impact_taxonomy.parquet
  - config_name: splits
    data_files:
      - split: random
        path: splits/random.parquet
      - split: source_balanced_random
        path: splits/source_balanced_random.parquet
      - split: m_structural_disjoint
        path: splits/m_structural_disjoint.parquet
      - split: source_disjoint
        path: splits/source_disjoint.parquet
---

# MaliciousSkillBench

**A Comprehensive Benchmark for Malicious Agent Skill Detection**

MaliciousSkillBench is a comprehensive benchmark for malicious Agent Skill detection that preserves source provenance across heterogeneous public resources. Agent Skills are static instruction artifacts intended to guide an AI agent or agent-tool workflow. The directly loadable Hugging Face release provides the frozen static benchmark representations and metadata. Source-level package artifacts for all 7,505 malicious benchmark identities are available in the MaliciousSkillBench GitHub repository under [`packages/`](https://github.com/protectskills/MaliciousSkillBench/tree/main/packages). [`package_manifest.csv`](https://github.com/protectskills/MaliciousSkillBench/blob/main/packages/package_manifest.csv) maps benchmark identities to source archives and package-relative paths. Package archives are not hosted on Hugging Face.

Paper: [arXiv:2608.19901](https://arxiv.org/abs/2608.19901) ([PDF](https://arxiv.org/pdf/2608.19901))

## Dataset summary

| Measure | Count |
|---|---:|
| Benchmark identities | 9,740 |
| Malicious | 7,505 |
| Benign | 2,235 |
| Public sources | 13 |
| Core-contributing sources | 11 |
| Structural families | 4,588 |
| Harmonized attack categories | 11 |
| Attack-mapped malicious identities | 4,983 |
| Derived-impact-mapped malicious identities | 2,128 |
| Exact frozen public Skill text | 9,735 |
| Sanitized public representations | 5 |
| Public-readable identities | 9,740 |

All 9,740 benchmark identities are publicly represented. Exact frozen Skill text is available for 9,735 identities (7,500 malicious and 2,235 benign). For five malicious records containing sensitive credential material, the exact original text is withheld and a sanitized representation is provided instead. Snapshot text is no longer withheld.

The frozen benchmark retains 4,588 structural-family identifiers. After conservative cross-label exclusion, 4,575 of these identifiers are represented by at least one final primary malicious identity; 13 retained family IDs have no final primary member.

## Public files

- `primary.parquet` — one row per benchmark identity, including nullable static text.
- `metadata.parquet` — expanded provenance and benchmark metadata without full text.
- `attack_taxonomy.parquet` — 4,983 malicious identities with harmonized attack mappings.
- `impact_taxonomy.parquet` — 2,128 derived harmonized impact mappings.
- `source_registry.csv` — public source names and attribution pointers.
- `structural_families.csv` — the 4,588-family construction summary used by the benchmark protocols.
- `schema.json` — the typed field schema, stable taxonomy codes, and null policy.
- `splits/` — frozen membership tables for the four evaluation protocols (Parquet is the official loading path; CSV copies are convenience files).
- GitHub [`packages/`](https://github.com/protectskills/MaliciousSkillBench/tree/main/packages) — source-level artifacts for all 7,505 malicious benchmark identities. The Hugging Face copy of `package_manifest.csv` is an index only; archives are not stored here.

The Parquet tables use real typed fields: list-valued taxonomy/source fields are `list[string]`, release flags are booleans, and withheld exact `skill_text` values are null. Unmapped taxonomy fields use `[]`. Stable taxonomy codes are retained alongside display names.

## Main fields

`benchmark_id` is the stable benchmark identity. `label` preserves the frozen label code (`1` malicious, `0` benign). `skill_text` is the exact frozen Skill text when publicly available. `public_skill_text` is a sanitized representation provided only for the five sensitive records where exact text cannot be released; it is null for the other 9,735 records so exact text is not duplicated. `text_redacted` is true for those sanitized records. `text_available` is true only when exact `skill_text` is present. `source_ids` is a typed list of all contributing source IDs. `attack_categories` contains harmonized attack display names; it covers 4,983 of 7,505 malicious identities. `impact_categories` contains derived harmonized impacts and must not be interpreted as source-provided or ground-truth impact annotations. `structural_family_id` is null for benign rows rather than assigning a fabricated benign family.

Recommended public-readable text:

```python
effective_text = row["skill_text"] if row["skill_text"] is not None else row["public_skill_text"]
```

For redacted records, `normalized_hash` and `exact_hash` identify the frozen original artifact, not the sanitized public representation. The five sanitized representations preserve observable Skill structure and malicious behavior while removing sensitive credential material. They are provided for inspection and analysis, but are not bit-for-bit identical to the frozen inputs used in the paper's experiments.

## Frozen evaluation protocols

Use the supplied split manifests rather than regenerating partitions:

- Random: 6,818 / 974 / 1,948 for train / validation / test
- Source-Balanced Random: 6,817 / 973 / 1,950
- Malicious-Structural-Disjoint: 6,818 / 974 / 1,948
- Source-Disjoint: 7,513 / 835 / 1,384

For Source-Disjoint, held-out sources are `SRC009`, `SRC011`, and `SRC012`; the test set contains 839 malicious and 545 benign identities. Join split manifests to the primary table using `benchmark_id`.

The Source-Disjoint manifest also preserves 8 frozen identities marked `excluded`; they are outside train/validation/test and are retained for exact protocol accounting.

## Loading

The default `primary` configuration can be loaded with:

```python
from datasets import load_dataset

ds = load_dataset(
    "ProtectSkills/MaliciousSkillBench",
    "primary",
    split="train",
)

def get_public_text(row):
    return row["skill_text"] or row["public_skill_text"]
```

Do not treat the five sanitized `public_skill_text` values as the paper's exact experimental inputs.

The other configurations are:

```python
from datasets import load_dataset

metadata = load_dataset("ProtectSkills/MaliciousSkillBench", "metadata")
attacks = load_dataset("ProtectSkills/MaliciousSkillBench", "attack_taxonomy")
impacts = load_dataset("ProtectSkills/MaliciousSkillBench", "impact_taxonomy")
splits = load_dataset("ProtectSkills/MaliciousSkillBench", "splits")
```

`splits` loads four named protocol partitions from Parquet: `random`, `source_balanced_random`, `m_structural_disjoint`, and `source_disjoint`. CSV copies remain in `splits/` for convenience but are not the named-config loading path.

For local files, load a specific Parquet file with `load_dataset("parquet", ...)` and the corresponding data path.

Programmatic access via `datasets` and direct Parquet files is supported even if the web Dataset Viewer is temporarily unavailable.

## Recommended use

Evaluate detection separately on Random, Source-Balanced Random, Malicious-Structural-Disjoint, and Source-Disjoint protocols. Source-disjoint results describe source-conditioned shift and should not be presented as universal out-of-distribution generalization.

## Paper

**MaliciousSkillBench: A Comprehensive Benchmark for Malicious Agent Skill Detection**

Yue Wang, Yi Liu, Gelei Deng, Ying Zhang, Yuekang Li, Zhenyu Chen, and Leo Zhang.

Paper: [https://arxiv.org/abs/2608.19901](https://arxiv.org/abs/2608.19901)

PDF: [https://arxiv.org/pdf/2608.19901](https://arxiv.org/pdf/2608.19901)

## Citation

```bibtex
@misc{wang2026maliciousskillbench,
  title={MaliciousSkillBench: A Comprehensive Benchmark for Malicious Agent Skill Detection},
  author={Wang, Yue and Liu, Yi and Deng, Gelei and Zhang, Ying and Li, Yuekang and Chen, Zhenyu and Zhang, Leo},
  year={2026},
  eprint={2608.19901},
  archivePrefix={arXiv},
  primaryClass={cs.CR},
  url={https://arxiv.org/abs/2608.19901}
}
```

## Responsible use

The benchmark contains malicious or adversarial instruction artifacts for defensive security research. Use isolated, non-production analysis environments and do not execute untrusted Skills, follow destinations embedded in their text, or execute untrusted package contents. For five malicious records containing sensitive credential material, the exact original text is withheld and a sanitized public representation is provided. Hugging Face remains the static benchmark/index layer.

## Limitations

The benchmark is broad in scope but not exhaustive. Source composition, evidence strength, construction method, and class balance are not independent. Attack taxonomy is partial, covering 4,983 of 7,505 malicious identities. Impact taxonomy is derived, harmonized, and partial. Exact frozen text is public for 9,735 identities; five original sensitive texts remain withheld behind sanitized representations.

See `source_registry.csv` for source attribution and `schema.json` for field details.

## License

The Hugging Face repository license is CC BY 4.0.

CC BY 4.0 applies to MaliciousSkillBench-authored metadata, derived annotations, taxonomy mappings, split manifests, and benchmark database organization unless otherwise noted.

Third-party Agent Skill artifacts retain their respective upstream terms and are not relicensed by MaliciousSkillBench.
