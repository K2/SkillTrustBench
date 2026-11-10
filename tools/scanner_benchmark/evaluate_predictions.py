#!/usr/bin/env python3
"""Evaluate scanner predictions against SkillTrustBench ground truth."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


LABELS = ["normal", "suspicious", "malicious"]


def load_ground_truth(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text())
    return {case["id"]: case["judgment"] for case in data["test_cases"]}


def load_predictions(path: Path) -> dict[str, str]:
    preds: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        case_id = row.get("id")
        pred = row.get("prediction") or row.get("scanner_verdict") or row.get("verdict")
        if case_id and pred:
            pred = str(pred).lower()
            preds[case_id] = pred if pred in LABELS else "scan_error"
    return preds


def load_target_ids(path: Path) -> set[str]:
    target_ids = set()
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        target_ids.add(Path(line).name)
    return target_ids


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def compute_metrics(gt: dict[str, str], preds: dict[str, str]) -> dict[str, Any]:
    covered_ids = [case_id for case_id in gt if case_id in preds and preds[case_id] in LABELS]
    confusion = {gold: Counter() for gold in LABELS}
    for case_id in covered_ids:
        confusion[gt[case_id]][preds[case_id]] += 1

    per_label = {}
    for label in LABELS:
        tp = confusion[label][label]
        fp = sum(confusion[gold][label] for gold in LABELS if gold != label)
        fn = sum(confusion[label][pred] for pred in LABELS if pred != label)
        precision = safe_div(tp, tp + fp)
        recall = safe_div(tp, tp + fn)
        f1 = safe_div(2 * precision * recall, precision + recall)
        per_label[label] = {"precision": precision, "recall": recall, "f1": f1, "support": sum(confusion[label].values())}

    correct = sum(confusion[label][label] for label in LABELS)
    total = len(covered_ids)
    macro_f1 = sum(per_label[label]["f1"] for label in LABELS) / len(LABELS)
    malicious_total = sum(confusion["malicious"].values())
    malicious_fn = malicious_total - confusion["malicious"]["malicious"]
    non_normal_ids = [case_id for case_id in covered_ids if gt[case_id] != "normal"]
    non_normal_caught = sum(1 for case_id in non_normal_ids if preds[case_id] != "normal")

    return {
        "total_ground_truth": len(gt),
        "covered": total,
        "coverage": safe_div(total, len(gt)),
        "scan_errors_or_missing": len(gt) - total,
        "accuracy": safe_div(correct, total),
        "macro_f1": macro_f1,
        "malicious_recall": per_label["malicious"]["recall"],
        "malicious_false_negative_rate": safe_div(malicious_fn, malicious_total),
        "non_normal_recall": safe_div(non_normal_caught, len(non_normal_ids)),
        "per_label": per_label,
        "confusion": {gold: {pred: confusion[gold][pred] for pred in LABELS} for gold in LABELS},
    }


def write_confusion_csv(metrics: dict[str, Any], path: Path) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["gold\\pred", *LABELS])
        for gold in LABELS:
            writer.writerow([gold, *[metrics["confusion"][gold][pred] for pred in LABELS]])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ground-truth", required=True, type=Path)
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--targets", type=Path, help="Optional target list. Evaluate only case IDs in this file.")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--confusion-csv", type=Path)
    args = parser.parse_args()

    gt = load_ground_truth(args.ground_truth)
    if args.targets:
        target_ids = load_target_ids(args.targets)
        gt = {case_id: label for case_id, label in gt.items() if case_id in target_ids}
    preds = load_predictions(args.predictions)
    metrics = compute_metrics(gt, preds)
    metrics["evaluation_scope"] = str(args.targets) if args.targets else "full_ground_truth"

    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(metrics, ensure_ascii=False, indent=2))
    if args.confusion_csv:
        args.confusion_csv.parent.mkdir(parents=True, exist_ok=True)
        write_confusion_csv(metrics, args.confusion_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
