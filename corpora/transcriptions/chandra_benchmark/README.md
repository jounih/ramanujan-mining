# Chandra OCR benchmark — DEFERRED (local inference crashes macOS)

**Status (2026-05-24)**: Local Chandra-OCR-2 inference attempts on
Apple Silicon repeatedly crashed the user's Mac. Pivoting to Chandra 2
via API (datalab-to hosted endpoint) when OCR work resumes.

## What was tried

1. `pip install chandra-ocr[hf]` — successful (0.2.0 in `.venv`).
2. Model weights pulled to `~/.cache/huggingface/hub/models--datalab-to-
   -chandra-ocr-2/`. Full safetensors blob: 10,591,220,088 bytes
   (~9.86 GiB) downloaded successfully.
3. Test runs of `chandra page-340.jpg <out> --method hf`:
   - First attempt: agent context-window timed out mid-download
     (safetensors blob truncated at 8.13 GB / 77%)
   - Subsequent attempts: model load OK after redownload, but inference
     crashed the system (no output captured; tmpfs logs lost on reboot)

## Why pivot to API

- Local HF inference of the chandra-ocr-2 model is too memory-heavy for
  the user's Mac (~10 GB model + working memory + RAM).
- `datalab-to` operates a hosted Chandra 2 API; structured-text/handwriting
  OCR via the API is the right path for any production OCR work.
- Per-page cost is small; the 1,149-page facsimile corpus is bounded.

## Next steps when OCR work resumes

1. Get a datalab-to API key.
2. Build a `corpora/scripts/chandra_api_runner.py` wrapper that:
   - Accepts a directory of images
   - Calls the API per page with retry / rate-limit handling
   - Writes structured Markdown + HTML output per page
   - Skips already-processed pages (idempotent)
3. Initial scope: 30-50 high-value Lost Notebook pages (Hunt 1 + Hunt 4
   class-invariants pages + a few mock-theta pages).
4. Feed OCR'd expressions into Project C's seed library
   (`rkc/search/seeds.py`) as new search inputs.

## What this dir holds today

- `in/page-340.jpg` — the canonical 1729 page, kept as a benchmark target
  for when the API path is set up.
- `LN_p341_canonical_1729/` (empty) — placeholder for the eventual output.
- `page-341/` (empty) — placeholder.

## Don't re-attempt local inference

Per user note (2026-05-24): "i think chandra keeps crashing my mac".
Pinning this here so future sessions don't try `chandra ... --method hf`
again. Use API path only.
