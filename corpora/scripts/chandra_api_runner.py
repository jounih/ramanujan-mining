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

OCR-error profile (per diary 27, n=1 spot-check on LN p. 341)
-------------------------------------------------------------
Chandra 2 on Ramanujan's hand shows 4 consistent error classes:
- A: digit substitution (cursive `2↔5`, `7↔1`, `8↔0`)
- B: exponent-as-subscript (cube `³` collapses to `_3` systemically)
- C: phantom adornments (spurious `w` superscripts)
- D: letter/digit confusion (`9→d`, `i→l`)
Block layout + LaTeX scaffolding are reliable; numerical content needs
human review. Treat output as DRAFT-quality pre-pass.

Auth
----
Reads `DATALAB_API_KEY` from `.env` (gitignored). The Datalab SDK reads it
from the environment automatically when present.

Usage
-----
# Single-file smoke test (sync):
python corpora/scripts/chandra_api_runner.py \\
    --input  corpora/transcriptions/chandra_benchmark/in/page-340.jpg \\
    --output corpora/transcriptions/chandra_benchmark/out/

# Directory of images (idempotent — skips any page whose .md output exists):
python corpora/scripts/chandra_api_runner.py \\
    --input  chatgpt-pro-mining/.../primary_originals/page_images/lost_notebook \\
    --output corpora/transcriptions/lost_notebook_chandra/

# Bulk async run (10-way concurrency; ~10× speedup):
python corpora/scripts/chandra_api_runner.py \\
    --input  <directory> --output <dir> --async --concurrency 10

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

Datalab limits (per docs/common/limits.md):
- 200 MB max file size; 7000 max pages per request
- 400 req/min and 400 concurrent requests (server-side cap)
- 5000 concurrent pages in flight (system-wide cap)
Default --concurrency 6 stays well under these; bump to ~20 for bulk
runs on the 1,149-page Notebook corpus.
"""
from __future__ import annotations

import argparse
import asyncio
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

from datalab_sdk import DatalabClient, AsyncDatalabClient
from datalab_sdk.models import ConvertOptions


SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".gif", ".pdf"}


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

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


def _ok_record(result, input_path: Path, elapsed: float) -> dict:
    return {
        "file": str(input_path),
        "status": "ok" if result.success else "fail",
        "elapsed_s": round(elapsed, 2),
        "page_count": result.page_count,
        "parse_quality_score": result.parse_quality_score,
        "runtime": result.runtime,
        "error": result.error,
    }


def _fail_record(e: Exception, input_path: Path, elapsed: float) -> dict:
    return {
        "file": str(input_path),
        "status": "fail",
        "elapsed_s": round(elapsed, 2),
        "page_count": None,
        "parse_quality_score": None,
        "runtime": None,
        "error": f"{type(e).__name__}: {e}",
    }


def _print_record(rec: dict) -> None:
    tag = rec["status"].upper()
    qs = rec.get("parse_quality_score")
    qs_str = f"  qs={qs:.2f}" if isinstance(qs, (int, float)) else ""
    err_str = f"  err={rec['error']}" if rec["status"] == "fail" else ""
    print(f"  {tag}  {Path(rec['file']).name}  ({rec['elapsed_s']}s){qs_str}{err_str}")


# ---------------------------------------------------------------------------
# Sync path (one file at a time)
# ---------------------------------------------------------------------------

def run_one_sync(client: DatalabClient,
                 input_path: Path,
                 out_dir: Path,
                 options: ConvertOptions) -> dict:
    """Convert one file via the sync API. Returns a log record."""
    t0 = time.time()
    out_base = out_dir / input_path.stem
    try:
        result = client.convert(file_path=input_path, options=options)
        result.save_output(out_base, save_images=True)
        return _ok_record(result, input_path, time.time() - t0)
    except Exception as e:
        return _fail_record(e, input_path, time.time() - t0)


def run_sync(inputs: list[Path],
             out_dir: Path,
             options: ConvertOptions,
             api_key: str,
             log_path: Path,
             force: bool) -> tuple[int, int, int]:
    """Sequential sync runner. Returns (n_ok, n_skip, n_fail)."""
    client = DatalabClient(api_key=api_key)
    n_ok = n_skip = n_fail = 0
    with log_path.open("a", encoding="utf-8") as log:
        for f in inputs:
            if not force and already_done(out_dir, f):
                n_skip += 1
                print(f"  skip  {f.name}  (md exists)")
                log.write(json.dumps({"file": str(f), "status": "skip"}) + "\n")
                continue
            rec = run_one_sync(client, f, out_dir, options)
            log.write(json.dumps(rec) + "\n")
            log.flush()
            _print_record(rec)
            if rec["status"] == "ok":
                n_ok += 1
            else:
                n_fail += 1
    return n_ok, n_skip, n_fail


# ---------------------------------------------------------------------------
# Async path (concurrent file processing)
# ---------------------------------------------------------------------------

async def _run_one_async(client: AsyncDatalabClient,
                         input_path: Path,
                         out_dir: Path,
                         options: ConvertOptions,
                         sem: asyncio.Semaphore) -> dict:
    """Convert one file via the async API, under a concurrency semaphore.
    Returns a log record.
    """
    async with sem:
        t0 = time.time()
        out_base = out_dir / input_path.stem
        try:
            result = await client.convert(file_path=input_path, options=options)
            # save_output is sync-only (writes files); call directly. This is
            # cheap (just disk I/O), so we don't bother to_thread it.
            result.save_output(out_base, save_images=True)
            return _ok_record(result, input_path, time.time() - t0)
        except Exception as e:
            return _fail_record(e, input_path, time.time() - t0)


async def _run_async_main(inputs: list[Path],
                          out_dir: Path,
                          options: ConvertOptions,
                          api_key: str,
                          log_path: Path,
                          force: bool,
                          concurrency: int) -> tuple[int, int, int]:
    """Async runner with a bounded semaphore. Returns (n_ok, n_skip, n_fail)."""
    # Partition into to-run and to-skip up front
    to_run, to_skip = [], []
    for f in inputs:
        (to_skip if (not force and already_done(out_dir, f)) else to_run).append(f)

    n_skip = len(to_skip)
    with log_path.open("a", encoding="utf-8") as log:
        for f in to_skip:
            print(f"  skip  {f.name}  (md exists)")
            log.write(json.dumps({"file": str(f), "status": "skip"}) + "\n")

    n_ok = n_fail = 0
    if not to_run:
        return n_ok, n_skip, n_fail

    sem = asyncio.Semaphore(concurrency)
    async with AsyncDatalabClient(api_key=api_key) as client:
        tasks = [
            asyncio.create_task(_run_one_async(client, f, out_dir, options, sem))
            for f in to_run
        ]
        # as_completed lets us log + print as each finishes (not in submission order)
        with log_path.open("a", encoding="utf-8") as log:
            for coro in asyncio.as_completed(tasks):
                rec = await coro
                log.write(json.dumps(rec) + "\n")
                log.flush()
                _print_record(rec)
                if rec["status"] == "ok":
                    n_ok += 1
                else:
                    n_fail += 1
    return n_ok, n_skip, n_fail


def run_async(inputs: list[Path],
              out_dir: Path,
              options: ConvertOptions,
              api_key: str,
              log_path: Path,
              force: bool,
              concurrency: int) -> tuple[int, int, int]:
    """Sync wrapper around the async runner; spins up the asyncio loop."""
    return asyncio.run(_run_async_main(
        inputs, out_dir, options, api_key, log_path, force, concurrency,
    ))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

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
    p.add_argument("--async", dest="use_async", action="store_true",
                   help="Use AsyncDatalabClient + asyncio for concurrent "
                        "processing (recommended for batches of 5+ files).")
    p.add_argument("--concurrency", type=int, default=6,
                   help="Max concurrent in-flight requests for --async mode "
                        "(default: 6; server cap is 400, but stay polite).")
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

    mode_tag = f"async×{args.concurrency}" if args.use_async else "sync"
    print(f"[chandra-api] inputs={len(inputs)}  output={args.output}  "
          f"mode={args.mode}  formats={args.output_format}  exec={mode_tag}")

    if args.dry_run:
        for f in inputs:
            status = "skip" if (not args.force and already_done(args.output, f)) else "run"
            print(f"  {status}  {f.name}")
        return 0

    options = build_options(args)

    t_start = time.time()
    if args.use_async:
        n_ok, n_skip, n_fail = run_async(
            inputs, args.output, options, api_key, log_path,
            args.force, args.concurrency,
        )
    else:
        n_ok, n_skip, n_fail = run_sync(
            inputs, args.output, options, api_key, log_path, args.force,
        )
    elapsed = time.time() - t_start

    print(f"\n[chandra-api] done: ok={n_ok}  skip={n_skip}  fail={n_fail}  "
          f"wall={elapsed:.1f}s  log={log_path}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
