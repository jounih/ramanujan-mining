#!/usr/bin/env python3
"""
Optional Chandra OCR runner for the downloaded Ramanujan Wren page corpus.

This wrapper assumes the `chandra` command is installed. It does not vendor or
install Chandra; install it separately following the upstream README, e.g.

  pip install chandra-ocr[hf]

or, for the vLLM path,

  pip install chandra-ocr
  chandra_vllm

Then run, for example:

  python scripts/run_chandra_ocr.py \
      --images-root ./ramanujan_wren_download/wren_pages \
      --out ./ramanujan_wren_download/ocr_chandra \
      --method hf

The wrapper runs one Chandra job per manuscript/component directory so a failed
component can be retried independently.
"""
from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}


def list_component_dirs(root: Path) -> List[Path]:
    dirs = []
    for p in sorted(root.iterdir() if root.exists() else []):
        if p.is_dir() and any(f.suffix.lower() in IMAGE_EXTS for f in p.iterdir() if f.is_file()):
            dirs.append(p)
    return dirs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--images-root", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--method", choices=["hf", "vllm"], default="hf")
    ap.add_argument("--max-workers", type=int, default=1)
    ap.add_argument("--batch-size", type=int, default=0, help="0 lets Chandra choose default")
    ap.add_argument("--include-headers-footers", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    exe = shutil.which("chandra")
    if not exe:
        print("ERROR: `chandra` command was not found on PATH.", file=sys.stderr)
        print("Install from upstream, e.g. `pip install chandra-ocr[hf]`, then retry.", file=sys.stderr)
        return 2

    args.out.mkdir(parents=True, exist_ok=True)
    log_rows = []
    dirs = list_component_dirs(args.images_root)
    if not dirs:
        print(f"No component directories with images found under {args.images_root}", file=sys.stderr)
        return 1

    for comp in dirs:
        comp_out = args.out / comp.name
        cmd = [exe, str(comp), str(comp_out), "--method", args.method]
        if args.max_workers:
            cmd += ["--max-workers", str(args.max_workers)]
        if args.batch_size:
            cmd += ["--batch-size", str(args.batch_size)]
        if args.include_headers_footers:
            cmd += ["--include-headers-footers"]
        else:
            cmd += ["--no-headers-footers"]
        cmd += ["--include-images"]

        print(" ".join(cmd), file=sys.stderr)
        if args.dry_run:
            rc = 0
        else:
            proc = subprocess.run(cmd, text=True)
            rc = proc.returncode
        log_rows.append({"component": comp.name, "image_dir": str(comp), "output_dir": str(comp_out), "returncode": rc, "command": " ".join(cmd)})
        if rc != 0:
            print(f"WARNING: Chandra returned {rc} for {comp.name}; continuing", file=sys.stderr)

    with (args.out / "chandra_run_log.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["component", "image_dir", "output_dir", "returncode", "command"])
        w.writeheader(); w.writerows(log_rows)
    print(f"Wrote OCR output/logs under {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
