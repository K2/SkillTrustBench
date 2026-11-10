#!/usr/bin/env python3
"""Normalize scanner JSON outputs into SkillTrustBench prediction JSONL.

The output format is one record per case:
{"id": "case_00433", "scanner": "cisco", "prediction": "malicious", ...}

The default verdict mapping is intentionally simple for quick benchmarking:
critical/high/malicious -> malicious; medium/moderate/suspicious -> suspicious;
low findings -> suspicious; no findings -> normal. For formal evaluation,
replace this heuristic with scanner-specific label mapping.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable


CASE_RE = re.compile(r"case_\d+")
SEVERITY_KEYS = {"severity", "level", "risk", "risk_level", "max_severity", "verdict", "status"}
SCORE_KEYS = {"score", "risk_score", "riskScore"}
FINDING_KEYS = {"findings", "issues", "vulnerabilities", "threats", "alerts", "results"}


def walk(obj: Any) -> Iterable[Any]:
    yield obj
    if isinstance(obj, dict):
        for value in obj.values():
            yield from walk(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk(value)


def find_case_id(path: Path, obj: Any) -> str | None:
    for candidate in [path.stem, path.name, str(path)]:
        match = CASE_RE.search(candidate)
        if match:
            return match.group(0)
    for node in walk(obj):
        if isinstance(node, str):
            match = CASE_RE.search(node)
            if match:
                return match.group(0)
        elif isinstance(node, dict):
            for key in ("id", "case_id", "caseId", "name"):
                value = node.get(key)
                if isinstance(value, str):
                    match = CASE_RE.search(value)
                    if match:
                        return match.group(0)
    return None


def collect_signals(obj: Any) -> tuple[list[str], list[float], int]:
    severities: list[str] = []
    scores: list[float] = []
    finding_count = 0

    for node in walk(obj):
        if not isinstance(node, dict):
            continue
        for key, value in node.items():
            key_text = str(key)
            key_norm = key_text.lower()
            if key_norm in SEVERITY_KEYS or "severity" in key_norm or "risk" in key_norm:
                if isinstance(value, str):
                    severities.append(value.lower())
            if key_text in SCORE_KEYS or key_norm in SCORE_KEYS:
                if isinstance(value, (int, float)):
                    scores.append(float(value))
                elif isinstance(value, str):
                    try:
                        scores.append(float(value))
                    except ValueError:
                        pass
            if key_norm in FINDING_KEYS and isinstance(value, list):
                finding_count += len(value)

    return severities, scores, finding_count


def predict(severities: list[str], scores: list[float], finding_count: int) -> str:
    joined = " ".join(severities)
    if any(word in joined for word in ["critical", "high", "malicious", "unsafe"]):
        return "malicious"
    if any(word in joined for word in ["medium", "moderate", "suspicious", "warning"]):
        return "suspicious"
    if scores:
        max_score = max(scores)
        if max_score >= 70:
            return "malicious"
        if max_score >= 30:
            return "suspicious"
    if finding_count > 0:
        return "suspicious"
    return "normal"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(errors="replace"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", required=True, type=Path, help="Directory containing per-case raw JSON outputs.")
    parser.add_argument("--scanner", required=True, help="Scanner name, such as aig, cisco, or skillspector.")
    parser.add_argument("--output", required=True, type=Path, help="Prediction JSONL output path.")
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for path in sorted(args.raw_dir.rglob("*.json")):
        try:
            obj = load_json(path)
            case_id = find_case_id(path, obj)
            if not case_id:
                continue
            severities, scores, finding_count = collect_signals(obj)
            records.append(
                {
                    "id": case_id,
                    "scanner": args.scanner,
                    "prediction": predict(severities, scores, finding_count),
                    "finding_count": finding_count,
                    "max_score": max(scores) if scores else None,
                    "severity_signals": sorted(set(severities))[:20],
                    "raw_path": str(path),
                }
            )
        except Exception as exc:
            match = CASE_RE.search(str(path))
            if match:
                records.append(
                    {
                        "id": match.group(0),
                        "scanner": args.scanner,
                        "prediction": "scan_error",
                        "scan_error": repr(exc),
                        "raw_path": str(path),
                    }
                )

    with args.output.open("w") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Wrote {len(records)} predictions to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
