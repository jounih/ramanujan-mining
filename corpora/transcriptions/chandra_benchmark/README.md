# Chandra OCR benchmark — OPERATIONAL via Datalab API

**Status (2026-05-24)**: Pivoted from local `--method hf` (crashed Mac) to
the Datalab hosted Chandra 2 API. End-to-end smoke test on the canonical
1729 page (`in/page-340.jpg` = LN reprint p. 341) succeeded in 8.76 s.

## Operational path

1. API key in `.env` (gitignored): `DATALAB_API_KEY=…`
2. SDK: `datalab-python-sdk` (installed in `.venv/`, v0.5.0).
3. Wrapper: [`corpora/scripts/chandra_api_runner.py`](../../scripts/chandra_api_runner.py).
4. Settings tuned for handwritten math:
   - `mode="accurate"` (slowest tier — needed for handwriting)
   - `output_format="markdown,html,json"` (markdown carries `$..$` LaTeX;
     html carries `<math display="block">` MathML/LaTeX; json carries
     block-level structure with bbox/polygon/section hierarchy)
   - `disable_image_captions=True` (no AI captions on hand diagrams)
   - figures extracted as base64-decoded PNGs alongside text
5. Idempotency: wrapper skips files whose `.md` output already exists
   (override with `--force`); per-run JSONL log in `_run_log.jsonl`.

## Smoke-test result (page-340.jpg = LN reprint p. 341, canonical 1729 page)

```
[chandra-api] inputs=1  output=out  mode=accurate  formats=markdown,html,json
  OK  page-340.jpg  (8.76s)
[chandra-api] done: ok=1  skip=0  fail=0
```

Block recognition: 16 blocks (Page + 15 child blocks, mostly Equation
blocks with display-math LaTeX). The numerator `(1 - 85x - 85x² + x³)`
appears in three generating-function lines on the page — this matches
the canonical cube-near generators Ramanujan tabulated on p. 341 (per
training-memory; cross-check against Ono arxiv 2014.xxxxx and
Berndt-Andrews LN Part IV before treating individual OCR'd digits as
ground truth). Diary 27 has the full 4-class error audit on this page.

**See also diary 28** for the expanded 6-class error taxonomy after
OCR'ing 3 more LN pages (pp. 342-344). Key downgrade: Chandra 2
**hallucinates fabricated content** on TABLE pages (page-341 returned
German text and invented modular polynomials in place of the actual
Weber class-invariant table). The chandra_api_runner is fine; the
underlying model is not safe to point at table-shaped pages without a
layout-classifier pre-pass.

## Limits + costs (per Datalab docs)

| limit | value |
|---|---|
| Max file size | 200 MB |
| Max pages per request | 7,000 |
| Requests / minute | 400 |
| Concurrent requests | 400 |
| Concurrent pages in flight | 5,000 |

At ~9s/page sequential, the full 1,149-page Notebook corpus is
~3 hours single-threaded; with the `AsyncDatalabClient` and even modest
concurrency (~10 parallel calls) it drops to ~20 minutes.

## Usage examples

```bash
# Single-image smoke test (this one):
python corpora/scripts/chandra_api_runner.py \
    --input  corpora/transcriptions/chandra_benchmark/in/page-340.jpg \
    --output corpora/transcriptions/chandra_benchmark/out/

# Directory batch (idempotent — skips pages whose .md exists):
python corpora/scripts/chandra_api_runner.py \
    --input  chatgpt-pro-mining/.../primary_originals/page_images/lost_notebook \
    --output corpora/transcriptions/lost_notebook_chandra/

# Dry-run (no API calls, lists what would be processed):
python corpora/scripts/chandra_api_runner.py --input <dir> --output <dir> --dry-run
```

## Output layout per input

```
out/
├── page-340.md            # LaTeX-rich markdown
├── page-340.html          # html with <math display="block"> blocks
├── page-340.json          # blocks: bbox, polygon, block_type, section_hierarchy
├── page-340.metadata.json # page_stats, num_blocks
├── page-340_*.png         # extracted figures (if any)
└── _run_log.jsonl         # append-only run log (one line per file)
```

## Don't re-attempt local --method hf

Per user note (2026-05-24): "i think chandra keeps crashing my mac".
The ~10 GB safetensors blob + working memory exceeded what's stable on
the user's setup. Stick with the API path; cost per page is small and
the corpus is bounded (≤1,149 pages).

## Next steps (ladder)

1. **Spot-check page-340 OCR vs Ono 2014 + Berndt-Andrews LN Part IV** —
   confirm the cube-near generating-function coefficients character-for-
   character, identify which subscript / digit errors Chandra makes on
   Ramanujan's hand.
2. **Pick a 30-50 page Hunt-relevant subset** — e.g. Hunt 4 class-
   invariants pages, Hunt 1 reverification pages — and batch-OCR via
   the wrapper.
3. **Add `--async` flag** to the wrapper to use `AsyncDatalabClient` for
   concurrent calls when batching the full 1,149-page corpus.
4. **Feed accepted OCR'd identities into `rkc/search/seeds.py`** as new
   search inputs for Project C.
