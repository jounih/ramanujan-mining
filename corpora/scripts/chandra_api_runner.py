"""chandra_api_runner.py — wrap the Datalab Chandra 2 OCR API for
batch-OCR'ing Ramanujan facsimile pages (handwritten math notation).

Why this exists
---------------
Local `chandra --method hf` inference crashed the user's Mac (see
`corpora/transcriptions/chandra_benchmark/README.md`). Datalab operates a
hosted Chandra 2 API; this script is the API-side replacement.

Best settings for our content (handwritten math)
------------------------------------------------
- mode="accurate"         — slowest, highest accuracy (essential for handwriting)
- output_format="markdown,html,json"  — markdown carries LaTeX math `$..$`;
                              json gives block-level structure for downstream
                              programmatic use (seed library / re-tagging);
                              html for visual diff review.
- disable_image_captions=True — we don't want AI-written captions of figures
- save_images=True        — keep extracted figures (Ramanujan's hand diagrams)
- paginate=False (single-image) / True (multi-page PDF)

Auth
----
Reads `DATALAB_API_KEY` from `.env` (gitignored). The Datalab SDK reads it
from the environment automatically when present.

Usage
-----
# Single-file smoke test:
python corpora/scripts/chandra_api_runner.py \\
    --input corpora/transcriptions/chandra_benchmark/in/page-340.jpg \\
    --output corpora/transcriptions/chandra_benchmark/out/

# Directory of images (idempotent — skips any page whose .md output exists):
python corpora/scripts/chandra_api_runner.py \\
    --input chatgpt-pro-mining/ramanujan_claude_source_pack_v2/primary_originals/page_images/lost_notebook \\
    --output corpora/transcriptions/lost_notebook_chandra/

Output layout per input file (foo.jpg):
    <output>/foo.md         markdown w/ LaTeX math
    <output>/foo.html       rendered html
    <output>/foo.json       block-level structure
    <output>/foo.metadata.json
    <output>/foo_*.png      extracted figures (if any)
    <output>/_run_log.jsonl one line per file (success / fail / skip)

Log shape per line:
    {"file": "...", "status": "ok|skip|fail", "elapsed_s": 3.2,
     "page_count": 1, "parse_quality_score": 0.92, "error": null}
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Iterable

# Load .env early so DATALAB_API_KEY is on env before the SDK initializes.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from datalab_sdk import DatalabClient
from datalab_sdk.models import ConvertOptions


SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".gif", ".pdf"}


def iter_inputs(root: Path) -> Iterable[Path]:
    """Yield input files. If `root` is a file, yield just it; if a dir, yield
    every supported file inside (non-recursive)."""
    if root.is_file():
        yield root
        return
    if not root.is_dir():
        raise FileNotFoundError(f"--input not found: {root}")
    for p in sorted(root.iterdir()):
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS:
            yield p


def already_done(out_dir: Path, input_path: Path) -> bool:
    """A file is 'done' if its .md output exists and is non-empty."""
    md = out_dir / (input_path.stem + ".md")
    return md.exists() and md.stat().st_size > 0


def run_one(client: DatalabClient,
            input_path: Path,
            out_dir: Path,
            options: ConvertOptions) -> dict:
    """Convert one file via the API. Returns a log record."""
    t0 = time.time()
    out_base = out_dir / input_path.stem
    try:
        result = client.convert(file_path=input_path, options=options)
        # Save markdown / html / json / images / metadata under out_base.*
        result.save_output(out_base, save_images=True)
        elapsed = time.time() - t0
        return {
            "file": str(input_path),
            "status": "ok" if result.success else "fail",
            "elapsed_s": round(elapsed, 2),
            "page_count": result.page_count,
            "parse_quality_score": result.parse_quality_score,
            "runtime": result.runtime,
            "error": result.error,
        }
    except Exception as e:
        elapsed = time.time() - t0
        return {
            "file": str(input_path),
            "status": "fail",
            "elapsed_s": round(elapsed, 2),
            "page_count": None,
            "parse_quality_score": None,
            "runtime": None,
            "error": f"{type(e).__name__}: {e}",
        }


def build_options(args) -> ConvertOptions:
    """Settings tuned for handwritten math facsimiles."""
    return ConvertOptions(
        mode=args.mode,
        output_format=args.output_format,
        disable_image_captions=True,     # we don't want AI captions on figures
        disable_image_extraction=False,  # keep figures (hand diagrams matter)
        paginate=args.paginate,
        max_pages=args.max_pages,
        page_range=args.page_range,
        skip_cache=args.skip_cache,
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--input", required=True, type=Path,
                   help="A single image/PDF file, or a directory of them.")
    p.add_argument("--output", required=True, type=Path,
                   help="Output directory (created if missing).")
    p.add_argument("--mode", default="accurate",
                   choices=["fast", "balanced", "accurate"],
                   help="API processing mode (default: accurate — best for "
                        "handwritten math).")
    p.add_argument("--output-format", default="markdown,html,json",
                   help="Comma-separated subset of "
                        "{markdown, html, json, chunks}. Default keeps all "
                        "three primary formats for downstream auditing.")
    p.add_argument("--paginate", action="store_true",
                   help="Paginate multi-page PDFs with horizontal rules.")
    p.add_argument("--max-pages", type=int, default=None,
                   help="Stop after N pages (for partial PDFs).")
    p.add_argument("--page-range", default=None,
                   help="Subset, e.g. '0-5,10,15-20'.")
    p.add_argument("--skip-cache", action="store_true",
                   help="Force re-run server-side (default: use cache).")
    p.add_argument("--force", action="store_true",
                   help="Re-process even if .md output already exists.")
    p.add_argument("--dry-run", action="store_true",
                   help="List what would be processed, then exit.")
    args = p.parse_args(argv)

    api_key = os.environ.get("DATALAB_API_KEY")
    if not api_key:
        print("ERROR: DATALAB_API_KEY not set. Put it in .env (gitignored).",
              file=sys.stderr)
        return 2

    args.output.mkdir(parents=True, exist_ok=True)
    log_path = args.output / "_run_log.jsonl"

    inputs = list(iter_inputs(args.input))
    if not inputs:
        print(f"ERROR: no supported files under {args.input}", file=sys.stderr)
        return 2

    print(f"[chandra-api] inputs={len(inputs)}  output={args.output}  "
          f"mode={args.mode}  formats={args.output_format}")

    if args.dry_run:
        for f in inputs:
            status = "skip" if (not args.force and already_done(args.output, f)) else "run"
            print(f"  {status}  {f.name}")
        return 0

    options = build_options(args)
    client = DatalabClient(api_key=api_key)

    n_ok = n_skip = n_fail = 0
    with log_path.open("a", encoding="utf-8") as log:
        for f in inputs:
            if not args.force and already_done(args.output, f):
                n_skip += 1
                print(f"  skip  {f.name}  (md exists)")
                log.write(json.dumps(
                    {"file": str(f), "status": "skip"}) + "\n")
                continue
            rec = run_one(client, f, args.output, options)
            log.write(json.dumps(rec) + "\n")
            log.flush()
            tag = rec["status"].upper()
            qs = rec.get("parse_quality_score")
            qs_str = f"  qs={qs:.2f}" if isinstance(qs, (int, float)) else ""
            print(f"  {tag}  {f.name}  ({rec['elapsed_s']}s){qs_str}"
                  + (f"  err={rec['error']}" if rec["status"] == "fail" else ""))
            if rec["status"] == "ok":
                n_ok += 1
            else:
                n_fail += 1

    print(f"\n[chandra-api] done: ok={n_ok}  skip={n_skip}  fail={n_fail}  "
          f"log={log_path}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
