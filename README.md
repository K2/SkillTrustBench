---
pretty_name: SkillTrustBench
license: cc-by-nc-sa-4.0
language:
- en
- zh
language_creators:
- found
- machine-generated
multilinguality:
- multilingual
annotations_creators:
- expert-generated
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
size_categories:
- 1K<n<10K
configs:
- config_name: default
  data_files:
  - split: benchmark
    path: data/test_cases.jsonl
- config_name: subset_556_v1_1
  data_files:
  - split: evaluation
    path: data/evaluation_subset_556_v1_1.jsonl
tags:
- cybersecurity
- ai-safety
- agent-safety
- benchmark
- code
- static-analysis
- malware-detection
- prompt-injection
- supply-chain-security
- red-teaming
- tool-use
- skills
---

# SkillTrustBench

SkillTrustBench is a benchmark dataset for evaluating security analysis of agent skills: reusable capability packages that extend an AI agent through natural-language instructions, tool-use guidance, and optional executable or reference assets. Each case follows an agent-skill-style layout, with a `SKILL.md` entrypoint that defines when and how the skill should be used, plus optional scripts, references, assets, configuration files, or agent definitions.

The benchmark tests whether AI agents, coding assistants, and security scanners can distinguish benign skills from vulnerable or intentionally malicious skills before installation or use.

The dataset is intended for security research, agent-safety evaluation, static analysis, red-team benchmarking, and classifier development.

<!-- V1_1_556_NOTICE_START -->
## v1.1 update notice

The first v1.1 artifact is now available as the fixed 556-case evaluation subset:

- [`skilltrustbench_556_v1_1.zip`](skilltrustbench_556_v1_1.zip)
- [`data/evaluation_subset_556_v1_1.jsonl`](data/evaluation_subset_556_v1_1.jsonl)
- [`subsets/skilltrustbench_556_v1_1/`](subsets/skilltrustbench_556_v1_1/)
- [v1.1 three-class leaderboard](https://huggingface.co/spaces/cuhk-zhuque/SkillTrustBench-Leaderboard)

It keeps the same 556 IDs, updates 31 judgments and 44 risk-label sets, and uses
quality-rewritten content for 228 cases. The full 5,520-case v1.1 release is in
preparation; `benchmark_full_v1.0.zip` remains the current full-corpus release.
<!-- V1_1_556_NOTICE_END -->

## Safety Notice

**WARNING: Some malicious skills in this dataset are real-world samples or derived from real-world malicious skill patterns. They are provided strictly for security research and benchmark evaluation. Do not attempt to install, import, execute, or run any skill package from this dataset outside a restricted disposable sandbox.**

This dataset contains intentionally malicious and vulnerable examples. Do not install, import, execute, or run scripts from individual cases on a host machine. Treat every case as untrusted code and inspect it only in a restricted, disposable sandbox.

The labels describe benchmark ground truth. They are not a guarantee that a case is safe, exhaustive, or representative of all real-world agent-skill attacks.

## Dataset Summary

- Version: `v1.0`
- Cases: 5,520
- Case ID range: `case_00000` to `case_05767`
- Case IDs are stable identifiers but are not contiguous. Some candidate IDs were filtered, merged, or withheld during construction, so gaps in the numeric range are expected.
- Raw directory size: about 240 MB
- Archive size: about 77 MB
- Files: 37,721
- Primary index: `benchmark_full_v1.0/ground_truth.json`
- Full archive: `benchmark_full_v1.0.zip`

## Label Distribution

| Judgment | Count | Meaning |
| --- | ---: | --- |
| `malicious` | 2,863 | Clear attack intent, such as exfiltration, persistence, command execution, prompt injection, tool hijacking, or obfuscation. |
| `normal` | 1,643 | Benign skill with no attack pattern and no vulnerability signal. |
| `suspicious` | 1,014 | Vulnerable or high-risk skill pattern without clear attack intent. |

## Source Distribution

| Source | Count | Malicious | Suspicious | Normal | Description |
| --- | ---: | ---: | ---: | ---: | --- |
| `injected` | 3,359 | 2323 (69.2%) | 1001 (29.8%) | 35 (1.0%) | Synthetic skills with injected attack or vulnerability patterns, covering malicious and suspicious cases across the main functional domains. |
| `safe_pool` | 1,500 | 0 (0.0%) | 10 (0.7%) | 1490 (99.3%) | Benign seed skills used as normal examples, with no current attack pattern or vulnerability signal in the ground truth. |
| `injected_d11` | 290 | 290 (100.0%) | 0 (0.0%) | 0 (0.0%) | Additional injected cases focused on deceptive or evaluation-resistant variants, such as obfuscation and evaluation-bypass patterns. |
| `wild_diffused` | 159 | 159 (100.0%) | 0 (0.0%) | 0 (0.0%) | Mutated or diffused variants derived from wild-style skill attacks, broadening delivery methods and lure categories. |
| `injected_d8` | 119 | 0 (0.0%) | 1 (0.8%) | 118 (99.2%) | False-positive and hard-negative style injected cases, including security tools or test fixtures that should not be labeled malicious by default. |
| `wild_expanded` | 46 | 46 (100.0%) | 0 (0.0%) | 0 (0.0%) | Expanded variants of wild-style cases, mainly around installer and dropper families. |
| `wild` | 37 | 35 (94.6%) | 2 (5.4%) | 0 (0.0%) | Wild or externally sourced real-world-inspired malicious skill cases and closely related subskill variants. |
| `injected_p0_normal_base` | 6 | 6 (100.0%) | 0 (0.0%) | 0 (0.0%) | Fixed-volume replacements generated by injecting high-priority P0 scanner signals into otherwise normal `safe_pool` skills. |
| `external_overtly_malicious_skills` | 4 | 4 (100.0%) | 0 (0.0%) | 0 (0.0%) | Fixed-volume replacements sourced from Trail of Bits `overtly-malicious-skills`; these are real malicious benchmark samples and must not be installed or executed. |

The `source` field describes how a case entered the benchmark, not the target domain of the skill. For functional domains, use `base_category`.
Judgment ratios are computed within each source group in this 5,520-case release; they are not intended to represent prevalence in the original ecosystem.

## Base Categories

| Category | Count | Malicious | Suspicious | Normal | Coverage |
| --- | ---: | ---: | ---: | ---: | --- |
| `api_integration` | 1,056 | 516 (48.9%) | 208 (19.7%) | 332 (31.4%) | Skills that connect agents to external APIs, SaaS services, webhooks, credentials, or backend integration workflows. |
| `crypto_wallet` | 591 | 280 (47.4%) | 107 (18.1%) | 204 (34.5%) | Wallet, token, transaction, private-key, exchange, and Web3 automation scenarios. |
| `content_gen` | 506 | 254 (50.2%) | 106 (20.9%) | 146 (28.9%) | Writing, summarization, publishing, translation, marketing, and other content-production workflows. |
| `agent_ops` | 497 | 249 (50.1%) | 103 (20.7%) | 145 (29.2%) | Agent operations, orchestration, memory/state handling, tool routing, workspace management, and automation control. |
| `data_tool` | 488 | 239 (49.0%) | 100 (20.5%) | 149 (30.5%) | Data extraction, transformation, analytics, reporting, file conversion, and dataset-oriented utilities. |
| `system_admin` | 356 | 184 (51.7%) | 70 (19.7%) | 102 (28.7%) | Shell, filesystem, service management, deployment, backup, monitoring, and local system maintenance tasks. |
| `scraper` | 340 | 172 (50.6%) | 67 (19.7%) | 101 (29.7%) | Crawling, browser automation, data collection, website parsing, and anti-bot-adjacent workflows. |
| `productivity` | 336 | 179 (53.3%) | 65 (19.3%) | 92 (27.4%) | Notes, calendars, personal workflows, office automation, email-like tasks, and general task assistants. |
| `devtool` | 334 | 197 (59.0%) | 58 (17.4%) | 79 (23.7%) | Developer tooling, code analysis, build/test automation, repository maintenance, and local developer workflows. |
| `lifestyle` | 329 | 159 (48.3%) | 61 (18.5%) | 109 (33.1%) | Consumer, personal, health, shopping, home, entertainment, and daily-life assistant scenarios. |
| `finance` | 246 | 125 (50.8%) | 46 (18.7%) | 75 (30.5%) | Market data, trading support, portfolio analysis, accounting, billing, and financial-reporting workflows. |
| `wild_real_world` | 242 | 240 (99.2%) | 2 (0.8%) | 0 (0.0%) | Wild-style malicious skill families and real-world-inspired lure scenarios, including installer/dropper variants. |
| `travel` | 132 | 52 (39.4%) | 14 (10.6%) | 66 (50.0%) | Itinerary, visa, booking, weather, packing, and trip-planning workflows. |
| `media` | 67 | 17 (25.4%) | 7 (10.4%) | 43 (64.2%) | Image, audio, video, design, asset generation, and media-processing tasks. |

The categories are functional domains. They are intentionally independent of the security labels: each domain can contain normal, suspicious, and malicious examples.
Judgment ratios are computed within each functional category in this release.

## Risk Labels

| Label | Count | Attack Category | Agent Dependency | Core Attack Method |
| --- | ---: | --- | --- | --- |
| `T01` | 1,425 | Skill Instruction Hijacking | Instructions / Skill text | Alters the agent's current session goals or safety constraints when the skill is loaded. |
| `T02` | 164 | Agent Memory Poisoning | Long-term memory / state storage | Writes attacker-controlled rules into persistent memory so they continue to affect future sessions. |
| `T03` | 812 | Remote Payload Retrieval and Execution | Code execution channel | Fetches code from an external URL, allowing the effective payload to change after skill review. |
| `T04` | 2,860 | Embedded Malicious Code | Skill `scripts/` directory | Ships malicious scripts inside the skill package and executes them locally when invoked. |
| `T05` | 1,077 | Unauthorized Access and Privilege Escalation | System permissions / access control | Breaks least-privilege boundaries by obtaining permissions beyond the task's legitimate needs. |
| `T06` | 96 | System Persistence | Startup services / scheduled tasks | Installs cross-session backdoors, hooks, services, or scheduled tasks that survive the skill run. |
| `T07` | 124 | Tool Hijacking and Spoofing | Local tools / APIs | Modifies, wraps, spoofs, or replaces tools so legitimate-looking calls execute attacker logic. |
| `T08` | 240 | Insecure Dependencies | Third-party dependencies / supply chain | Introduces malicious packages or components through dependency confusion, typosquatting, or unsafe sources. |
| `T09` | 1,120 | Insecure Skill Coding Practices | Skill code / configuration | Exposes exploitable flaws such as hardcoded secrets, command injection, plaintext sensitive data, or unsafe temp files. |

Risk labels are multi-label. A single case can carry more than one taxonomy label.

## Data Structure

The Hugging Face repository is organized as a viewer-friendly annotation table plus a compressed benchmark tree:

```text
data/
  test_cases.jsonl          # compact table used by the Hugging Face Dataset Viewer
metadata/
  case_metadata.jsonl       # full per-case metadata, including sparse construction fields
benchmark_full_v1.0/
  ground_truth.json
benchmark_full_v1.0.zip  # archive containing:
  benchmark_full_v1.0/case_00000/SKILL.md
  benchmark_full_v1.0/case_00001/scripts/...
  ...
README.md
```

`data/test_cases.jsonl` is the compact row-wise annotation table used by the Hugging Face Dataset Viewer. It keeps only stable, broadly applicable columns so the default datatable remains easy to scan.

`metadata/case_metadata.jsonl` contains the fuller row-wise metadata exported from `benchmark_full_v1.0/ground_truth.json`, including sparse construction and provenance fields such as trigger style, encoding, honeypot targets, wild-sample lineage, confidence, delivery method, lure category, and source notes.

The full per-case skill directories are stored in `benchmark_full_v1.0.zip`. If you unpack the archive locally, `benchmark_full_v1.0/` becomes the complete benchmark tree with one `case_*` directory per test case.

`ground_truth.json` contains:

- `metadata`: aggregate statistics, source distributions, risk distributions, and build notes.
- `judgment_criteria`: definitions of `normal`, `suspicious`, and `malicious`.
- `risk_taxonomy`: taxonomy labels used by `risk_labels`.
- `test_cases`: one annotation record per `case_*` directory.

Viewer fields in `data/test_cases.jsonl`:

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Case directory name, such as `case_04866`. |
| `judgment` | string | One of `normal`, `suspicious`, or `malicious`. |
| `risk_labels` | list[string] | Multi-label risk taxonomy identifiers. |
| `source` | string | Dataset source or generation pool. |
| `base_category` | string | Functional domain of the skill. |
| `primary_pattern` | string or null | Main attack or vulnerability pattern. |
| `attack_pattern` | list[string] | All associated attack or vulnerability patterns. |
| `skill_path` | string | Path to the corresponding skill directory after expanding the archive. |

Additional metadata fields in `metadata/case_metadata.jsonl` and `ground_truth.json` may include `vuln_signals`, `trigger_type`, `encoding`, `fragment_count`, `honeypot_target`, `confidence`, `wild_source`, `delivery_method`, `lure_category`, `family_id`, `subfamily_id`, `c2_ip`, `skill_md_sha256_short`, and other construction notes. These fields are intentionally separated from the default viewer table because they apply only to specific subsets of the benchmark.

## Loading Example

Load the row-wise annotation table with Hugging Face Datasets:

```python
from datasets import load_dataset

ds = load_dataset("cuhk-zhuque/SkillTrustBench", split="benchmark")
row = ds[0]
print(row["id"], row["judgment"], row["risk_labels"])
```

To inspect full skill files, read the expanded benchmark tree or fall back to the zip archive:

```python
import json
import zipfile
from pathlib import Path

root = Path("benchmark_full_v1.0")
with (root / "ground_truth.json").open() as f:
    data = json.load(f)

cases = data["test_cases"]
first = cases[0]

skill_path = root / first["id"] / "SKILL.md"
if skill_path.exists():
    skill_text = skill_path.read_text(errors="replace")
else:
    # The Hugging Face repo ships full case directories inside this archive.
    with zipfile.ZipFile("benchmark_full_v1.0.zip") as zf:
        with zf.open(f"benchmark_full_v1.0/{first['id']}/SKILL.md") as f:
            skill_text = f.read().decode("utf-8", errors="replace")

print(first["id"], first["judgment"], first["risk_labels"])
```

For evaluation pipelines, treat `ground_truth.json` as the authoritative index and join each annotation with the corresponding `case_*` directory by `id`.

## External Scanner Quickstart

SkillTrustBench can be used as an offline benchmark corpus for external skill scanners. Each test case is a standalone skill directory named `case_*`; scanners should inspect these directories without installing dependencies, running setup scripts, importing Python modules, or executing shell commands from the samples.

The fast validation loop is:

1. Expand the benchmark and create target lists.
2. Run one scanner over `representative_scan_targets.txt`.
3. Normalize scanner JSON into `id + prediction`.
4. Compare predictions with `ground_truth.json`.
5. Switch to `scan_targets.txt` for the full 5,520-case benchmark.

This mirrors the workflow used by many public agent and tool-use benchmarks: use a small subset for smoke testing, keep raw model or scanner outputs, normalize predictions into a documented schema, and evaluate against ground truth with an explicit run scope. Do not compare representative-set scores with full-benchmark scores.

Prepare the expanded benchmark tree:

```bash
# Run from the dataset repository root, i.e. the directory containing
# README.md, benchmark_full_v1.0.zip, data/, and tools/.
mkdir -p scan_workspace
unzip -q benchmark_full_v1.0.zip -d scan_workspace
export SKILLSEC_ROOT="$PWD/scan_workspace/benchmark_full_v1.0"
find "$SKILLSEC_ROOT" -mindepth 1 -maxdepth 1 -type d -name "case_*" | sort > scan_targets.txt
```

Start with the representative cases before scanning all 5,520 samples:

```bash
printf "%s\n" \
  "$SKILLSEC_ROOT/case_00433" \
  "$SKILLSEC_ROOT/case_00541" \
  "$SKILLSEC_ROOT/case_00677" \
  "$SKILLSEC_ROOT/case_00070" \
  "$SKILLSEC_ROOT/case_02160" \
  > representative_scan_targets.txt
```

### Verify Scanner Output

SkillTrustBench includes small helper scripts under `tools/scanner_benchmark/`:

- `normalize_scanner_results.py`: convert per-case scanner JSON into `predictions.jsonl`.
- `evaluate_predictions.py`: compare predictions against `ground_truth.json`.
- `aig_batch_scan.py`: optionally submit case directories to Tencent A.I.G through its task APIs.

The normalized prediction file should contain one JSON object per line:

```json
{"id": "case_00433", "scanner": "scanner-name", "prediction": "malicious"}
```

Valid predictions are `normal`, `suspicious`, and `malicious`. The normalizer provides a quick severity-based mapping for raw scanner JSON. For formal evaluation, replace that heuristic with scanner-specific label mapping.

Run evaluation:

```bash
python3 tools/scanner_benchmark/evaluate_predictions.py \
  --ground-truth benchmark_full_v1.0/ground_truth.json \
  --predictions results/cisco_predictions.jsonl \
  --json-out results/cisco_metrics.json \
  --confusion-csv results/cisco_confusion.csv
```

Key metrics to inspect first:

- `coverage`: how many cases produced valid scanner predictions.
- `macro_f1`: balanced three-way classification quality.
- `malicious_recall`: ability to catch malicious skills.
- `malicious_false_negative_rate`: malicious cases incorrectly missed by the scanner.
- `non_normal_recall`: ability to catch both suspicious and malicious cases.

For reproducible reporting, include the scanner name, scanner version or commit, run date, target list, scan mode, whether LLM/cloud analysis was enabled, model name if applicable, and whether sample content was uploaded to any external service.

For representative-set smoke tests, add `--targets representative_scan_targets.txt`:

```bash
python3 tools/scanner_benchmark/evaluate_predictions.py \
  --ground-truth benchmark_full_v1.0/ground_truth.json \
  --predictions results/cisco_predictions.jsonl \
  --targets representative_scan_targets.txt \
  --json-out results/cisco_representative_metrics.json \
  --confusion-csv results/cisco_representative_confusion.csv
```

### Cisco Skill Scanner

[Cisco Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner) provides the `skill-scanner` CLI. Its README describes core static analyzers, optional behavioral analysis, optional LLM analysis, optional Cisco AI Defense analysis, recursive `scan-all`, JSON/SARIF/HTML outputs, and `--lenient` mode for non-standard skill formats.

Install:

```bash
# Requires Python 3.10+.
python3 -m venv .venv-skill-scanner
source .venv-skill-scanner/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install cisco-ai-skill-scanner
# Or, if you use uv:
# uv pip install cisco-ai-skill-scanner
```

Optional model-backed scan:

```bash
# Cisco's LLM analyzer uses provider/model environment variables.
# Install provider extras if needed, for example:
# python3 -m pip install "cisco-ai-skill-scanner[all]"

export SKILL_SCANNER_LLM_API_KEY="<provider-api-key>"
export SKILL_SCANNER_LLM_MODEL="gpt-4o"

skill-scanner scan "$SKILLSEC_ROOT/case_00433" \
  --use-llm \
  --llm-provider openai \
  --lenient \
  --format json \
  --output results/cisco_model_case_00433.json
```

For Anthropic, OpenAI, Azure, Bedrock, Gemini, Vertex, or other LiteLLM-backed routes, set the provider-specific model string and environment variables according to Cisco's LLM Analyzer documentation. When reporting benchmark results, record the provider, exact model string, scanner version, and whether `--use-llm`, `--enable-meta`, or cloud analyzers were enabled.

Batch scan the representative set:

```bash
mkdir -p results/cisco
while read -r case_dir; do
  case_id="$(basename "$case_dir")"
  skill-scanner scan "$case_dir" \
    --use-behavioral \
    --lenient \
    --format json \
    --output "results/cisco/${case_id}.json" || true
done < representative_scan_targets.txt
```

Normalize and evaluate:

```bash
python3 tools/scanner_benchmark/normalize_scanner_results.py \
  --raw-dir results/cisco \
  --scanner cisco \
  --output results/cisco_predictions.jsonl

python3 tools/scanner_benchmark/evaluate_predictions.py \
  --ground-truth benchmark_full_v1.0/ground_truth.json \
  --predictions results/cisco_predictions.jsonl \
  --targets representative_scan_targets.txt \
  --json-out results/cisco_representative_metrics.json \
  --confusion-csv results/cisco_representative_confusion.csv
```

For full benchmark scanning, use `scan_targets.txt` in the loop and omit `--targets` in the evaluation command. You can also use Cisco's recursive mode for a single aggregate report:

```bash
skill-scanner scan-all "$SKILLSEC_ROOT" \
  --recursive \
  --use-behavioral \
  --lenient \
  --format json \
  --output results/cisco_full.json
```

For metric calculation, the per-case loop above is the safer path because it produces one JSON file per `case_*` directory. If you use Cisco's aggregate `scan-all` report, split or map the aggregate output into one prediction per case before running `normalize_scanner_results.py`.

Only enable cloud or LLM-backed analyzers, such as `--use-llm`, `--use-aidefense`, or `--use-virustotal --vt-upload-files`, if your evaluation policy allows uploading sample content, file hashes, or binaries to external services.

### NVIDIA SkillSpector

[NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector) provides the `skillspector` CLI. Its README describes scanning local skill directories, single `SKILL.md` files, Git repositories, and zip files, with terminal, JSON, Markdown, and SARIF outputs. It also supports static-only scanning through `--no-llm`.

Install:

```bash
# Requires Python 3.12 or 3.13.
git clone https://github.com/NVIDIA/skillspector.git
cd skillspector
uv venv .venv --python 3.13 && source .venv/bin/activate
# Or, without uv:
# python3.13 -m venv .venv && source .venv/bin/activate
make install
cd -
```

Optional model-backed scan:

```bash
# NVIDIA Build provider.
export SKILLSPECTOR_PROVIDER=nv_build
export NVIDIA_INFERENCE_KEY="<nvidia-inference-key>"
export SKILLSPECTOR_MODEL="deepseek-ai/deepseek-v4-flash"

skillspector scan "$SKILLSEC_ROOT/case_00433" \
  --format json \
  --output results/skillspector_model_case_00433.json
```

To use a different provider, set `SKILLSPECTOR_PROVIDER` and the matching credential environment variable. For example, use `SKILLSPECTOR_PROVIDER=openai` with `OPENAI_API_KEY`, or `SKILLSPECTOR_PROVIDER=anthropic` with `ANTHROPIC_API_KEY`. Use `SKILLSPECTOR_MODEL` to override the provider's default model. For local OpenAI-compatible endpoints such as Ollama, vLLM, or llama.cpp, set `SKILLSPECTOR_PROVIDER=openai`, `OPENAI_BASE_URL`, and the local model name.

Batch scan the representative set:

```bash
mkdir -p results/skillspector
while read -r case_dir; do
  case_id="$(basename "$case_dir")"
  skillspector scan "$case_dir" \
    --no-llm \
    --format json \
    --output "results/skillspector/${case_id}.json" || true
done < representative_scan_targets.txt
```

Normalize and evaluate:

```bash
python3 tools/scanner_benchmark/normalize_scanner_results.py \
  --raw-dir results/skillspector \
  --scanner skillspector \
  --output results/skillspector_predictions.jsonl

python3 tools/scanner_benchmark/evaluate_predictions.py \
  --ground-truth benchmark_full_v1.0/ground_truth.json \
  --predictions results/skillspector_predictions.jsonl \
  --targets representative_scan_targets.txt \
  --json-out results/skillspector_representative_metrics.json \
  --confusion-csv results/skillspector_representative_confusion.csv
```

For full benchmark scanning, use `scan_targets.txt` in the loop and omit `--targets` in the evaluation command. If using SkillSpector semantic LLM analysis, configure the provider and API key according to the upstream documentation and remove `--no-llm`. SkillSpector may also query OSV.dev for live dependency vulnerability lookups; if your benchmark policy forbids outbound network requests, run it in an offline or egress-restricted environment and document that setting.

### Tencent A.I.G

[Tencent A.I.G / AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard) supports MCP Server and Agent Skills scanning through the A.I.G service. The official README describes Docker deployment, and the official API documentation exposes file upload, task creation, status, and result endpoints. The helper below follows the documented MCP source-code scanning workflow: upload each case as a zip archive, create an `mcp_scan` task with the returned attachment URL, poll task status, and fetch the result JSON.

Deploy A.I.G locally:

```bash
git clone https://github.com/Tencent/AI-Infra-Guard.git
cd AI-Infra-Guard
docker-compose -f docker-compose.images.yml up -d
# If you use Docker Compose V2, use:
# docker compose -f docker-compose.images.yml up -d
cd -
```

Do not expose the A.I.G web service to public networks unless you have added your own authentication and network controls.

Batch scan the representative set:

```bash
python3 -m pip install requests

export AIG_BASE_URL="http://127.0.0.1:8088"
export AIG_MODEL_TOKEN="<model-api-token>"
export AIG_MODEL_BASE_URL="https://api.openai.com/v1"
export AIG_MODEL_NAME="gpt-4o-mini"

python3 tools/scanner_benchmark/aig_batch_scan.py \
  --targets representative_scan_targets.txt \
  --out results/aig \
  --base-url "$AIG_BASE_URL" \
  --model "$AIG_MODEL_NAME" \
  --model-base-url "$AIG_MODEL_BASE_URL" \
  --language en
```

Normalize and evaluate:

```bash
python3 tools/scanner_benchmark/normalize_scanner_results.py \
  --raw-dir results/aig \
  --scanner aig \
  --output results/aig_predictions.jsonl

python3 tools/scanner_benchmark/evaluate_predictions.py \
  --ground-truth benchmark_full_v1.0/ground_truth.json \
  --predictions results/aig_predictions.jsonl \
  --targets representative_scan_targets.txt \
  --json-out results/aig_representative_metrics.json \
  --confusion-csv results/aig_representative_confusion.csv
```

For the full benchmark, replace `representative_scan_targets.txt` with `scan_targets.txt` in the scan command and omit `--targets` in the evaluation command. Because A.I.G uses a model-backed analysis flow, estimate API cost and rate limits before running all 5,520 cases.

## Intended Uses

- Benchmarking security classifiers for agent skills and tool-use packages.
- Evaluating LLM and agent robustness against malicious instructions, prompt injection, tool hijacking, remote payload execution, persistence, and insecure coding patterns.
- Building static-analysis or retrieval pipelines that inspect `SKILL.md`, scripts, configs, and references.
- Red-team research in controlled, non-production environments.

## Out-of-Scope Uses

- Executing cases on personal, corporate, or production machines.
- Deploying any case as a real assistant skill or plugin.
- Treating the labels as legal, compliance, or malware-family determinations.
- Using the dataset to create or improve harmful malware, persistence, credential theft, or exfiltration tooling.

## Evaluation Notes

Recommended classification tasks:

- Three-way classification: `normal` vs. `suspicious` vs. `malicious`.
- Binary safety screening: `normal` vs. `non-normal`.
- Multi-label risk classification using `risk_labels`.
- Pattern detection using `primary_pattern` and `attack_pattern`.

Suggested metrics include macro F1, per-class precision and recall, false-negative rate on `malicious`, and confusion between `suspicious` and `malicious`.

## Limitations

- Some cases are synthetic or template-mutated and may not match the full diversity of real-world threats.
- The dataset intentionally contains deceptive or obfuscated patterns, but it is not exhaustive.
- Distribution counts reflect this release and should not be interpreted as real-world prevalence.
- Some case directories include runnable scripts or package manifests; they are benchmark artifacts, not usage instructions.

## License

© Tencent Zhuque Lab SkillTrustBench | [CC BY-NC-SA 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Citation

If you use this dataset, please cite the dataset repository and version:

```bibtex
@dataset{skilltrustbench_v1_0,
  title = {SkillTrustBench},
  version = {v1.0},
  year = {2026},
  note = {Benchmark dataset for agent skill security evaluation}
}
```

## Checksums

Current release artifacts:

| File | SHA-256 |
| --- | --- |
| `data/test_cases.jsonl` | `138504943647184f4f6455b91f04288d0ae4d9e1e5e1ba99c9728e5eb887f3c4` |
| `metadata/case_metadata.jsonl` | `e448af71299377c3a2ccf1010c7308b02a76ee83121ba11460bb84fcbcf6616a` |
| `benchmark_full_v1.0.zip` | `d65fe234bb2142b3b96d7aa6ad94993e1dad7cc4cbcc34a79e318e8b43ff0ead` |
| `benchmark_full_v1.0/ground_truth.json` | `3ba99b732042e7bae2d4d605c34146c5486bf3876a6433a085412eb4aa51ebe1` |
