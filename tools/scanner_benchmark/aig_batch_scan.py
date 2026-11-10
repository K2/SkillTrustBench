#!/usr/bin/env python3
"""Batch-submit SkillTrustBench cases to Tencent A.I.G task APIs.

This helper uploads each case directory as a zip archive, creates an A.I.G
`mcp_scan` task, polls until completion, and stores raw result JSON files.
It does not execute sample code.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
import time
import zipfile
from pathlib import Path
from typing import Any

import requests


def zip_case(case_dir: Path, out_path: Path) -> None:
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(case_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(case_dir.parent))


def upload_archive(base_url: str, archive: Path) -> str:
    url = f"{base_url.rstrip('/')}/api/v1/app/taskapi/upload"
    with archive.open("rb") as f:
        resp = requests.post(url, files={"file": f}, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != 0:
        raise RuntimeError(f"A.I.G upload failed: {data}")
    return data["data"]["fileUrl"]


def create_task(
    base_url: str,
    file_url: str,
    model: str,
    token: str,
    model_base_url: str | None,
    language: str,
    thread: int,
    prompt: str,
) -> str:
    url = f"{base_url.rstrip('/')}/api/v1/app/taskapi/tasks"
    model_cfg: dict[str, Any] = {"model": model, "token": token}
    if model_base_url:
        model_cfg["base_url"] = model_base_url
    payload = {
        "type": "mcp_scan",
        "content": {
            "prompt": prompt,
            "model": model_cfg,
            "thread": thread,
            "language": language,
            "attachments": file_url,
        },
    }
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != 0:
        raise RuntimeError(f"A.I.G task creation failed: {data}")
    return data["data"]["session_id"]


def get_json(base_url: str, path: str) -> dict[str, Any]:
    resp = requests.get(f"{base_url.rstrip('/')}{path}", timeout=120)
    resp.raise_for_status()
    return resp.json()


def poll_task(base_url: str, session_id: str, interval: float, timeout: float) -> dict[str, Any]:
    deadline = time.time() + timeout
    while time.time() < deadline:
        status = get_json(base_url, f"/api/v1/app/taskapi/status/{session_id}")
        task_status = (status.get("data") or {}).get("status")
        if task_status in {"completed", "failed"}:
            return status
        time.sleep(interval)
    raise TimeoutError(f"Timed out waiting for A.I.G task {session_id}")


def iter_targets(targets_file: Path) -> list[Path]:
    targets = []
    for line in targets_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            targets.append(Path(line).expanduser().resolve())
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", required=True, type=Path, help="File containing one case directory per line.")
    parser.add_argument("--out", required=True, type=Path, help="Output directory for raw A.I.G JSON results.")
    parser.add_argument("--base-url", default=os.environ.get("AIG_BASE_URL", "http://127.0.0.1:8088"))
    parser.add_argument("--model", required=True, help="Evaluation model name configured for A.I.G mcp_scan.")
    parser.add_argument("--token", default=os.environ.get("AIG_MODEL_TOKEN"), help="Model API token.")
    parser.add_argument("--model-base-url", default=os.environ.get("AIG_MODEL_BASE_URL"))
    parser.add_argument("--language", default="en")
    parser.add_argument("--thread", type=int, default=4)
    parser.add_argument("--prompt", default="Scan this Agent Skill directory for security risks. Do not execute it.")
    parser.add_argument("--poll-interval", type=float, default=5.0)
    parser.add_argument("--timeout", type=float, default=1800.0)
    args = parser.parse_args()

    if not args.token:
        raise SystemExit("Missing model token. Pass --token or set AIG_MODEL_TOKEN.")

    args.out.mkdir(parents=True, exist_ok=True)
    summary_path = args.out / "aig_batch_summary.jsonl"

    with tempfile.TemporaryDirectory(prefix="skilltrustbench-aig-") as tmp:
        tmp_dir = Path(tmp)
        with summary_path.open("w") as summary:
            for case_dir in iter_targets(args.targets):
                case_id = case_dir.name
                raw_path = args.out / f"{case_id}.json"
                archive_path = tmp_dir / f"{case_id}.zip"
                record: dict[str, Any] = {"id": case_id, "case_dir": str(case_dir), "raw_path": str(raw_path)}
                try:
                    if not (case_dir / "SKILL.md").exists():
                        raise FileNotFoundError(f"{case_dir} does not contain SKILL.md")
                    zip_case(case_dir, archive_path)
                    file_url = upload_archive(args.base_url, archive_path)
                    session_id = create_task(
                        args.base_url,
                        file_url,
                        args.model,
                        args.token,
                        args.model_base_url,
                        args.language,
                        args.thread,
                        args.prompt,
                    )
                    record["session_id"] = session_id
                    record["status"] = poll_task(args.base_url, session_id, args.poll_interval, args.timeout)
                    result = get_json(args.base_url, f"/api/v1/app/taskapi/result/{session_id}")
                    raw_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
                    record["ok"] = True
                except Exception as exc:  # Keep batch runs moving.
                    record["ok"] = False
                    record["error"] = repr(exc)
                    raw_path.write_text(json.dumps(record, ensure_ascii=False, indent=2))
                summary.write(json.dumps(record, ensure_ascii=False) + "\n")
                summary.flush()

    # Remove accidental temp archives if an older Python left any behind.
    shutil.rmtree(args.out / "__tmp__", ignore_errors=True)
    print(f"Wrote A.I.G raw results to {args.out}")
    print(f"Wrote summary to {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
