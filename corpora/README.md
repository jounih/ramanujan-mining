# `corpora/` — primary-source scans and transcriptions

This directory is the **landing zone** for primary Ramanujan material as it
arrives from the user / parallel ChatGPT-Pro run. It is the bridge between
the network-blocked Claude environment (which cannot fetch from
archive.org / Trinity / TIFR) and the analyses under `ramanujan/analysis/`.

## Layout

```
corpora/
  scans/            # raw PDFs and image facsimiles of primary sources.
                    # Files >1MB are gitignored (see ../.gitignore at repo
                    # root). A `.gitkeep` keeps the directory tracked.
  transcriptions/   # LaTeX / unicode-text transcriptions of primary
                    # sources, ready for programmatic consumption.
    README.md            — format spec + worked example
    operator_tagging_schema.py
                         — Hunt 5 operator-tagging schema (6 operators
                           per HUNT_MAP §5); see Hunt 5 section below.
    quarterly_reports/   — empty until the Berndt 1984 transcription
                           arrives; pre-wired filenames are documented
                           in its README.md.
  RamanujanMachine/      — upstream RamanujanMachine clone (existing)
  RamanujanMachine_v0/   — earlier RamanujanMachine snapshot (existing)
```

## How to add a new primary source

Two cases:

### 1. Raw PDF / image facsimile

Drop the file under `scans/`. If it is >1MB, it will be silently ignored
by git (the gitignore rule at the repo root). The recommended filename
shape is:

```
scans/<corpus_code>_<short_id>_<page_or_label>.pdf
```

Where `<corpus_code>` is from `diary/00_charter.md`:

| Code | Corpus |
|------|--------|
| LN   | "Lost" Notebook (Trinity Add.Ms.a.94.15-style) |
| N1, N2, N3 | Notebooks 1–3 (TIFR facsimile) |
| L1–L3 | Letters to Hardy (Trinity Add.Ms.a.94.2 etc.) |
| QR   | Quarterly Reports (Berndt 1984 typeset / Satagopan handwritten) |
| CP   | Collected Papers (Hardy–Aiyar–Wilson 1927) |
| OL   | Other letters / fragments |

Examples:

```
scans/QR_berndt_1984_blms_qr1_full.pdf      # Quarterly Report 1, full
scans/LN_341.pdf                            # Lost Notebook page 341
scans/CP_paper06.pdf                        # Collected Papers paper #6
```

Add a one-line provenance entry in `manifest/` pointing to the upstream
URL and license. Do not check in copyrighted material in violation of its
license; if in doubt, transcribe instead.

### 2. Transcription (LaTeX / unicode-text)

Transcriptions belong under `transcriptions/`. They are the durable,
diffable form that downstream analyses actually consume. See
`transcriptions/README.md` for the format spec.

Hunt 5 (the Quarterly Reports operator-tagging task) has its own
sub-directory `transcriptions/quarterly_reports/` whose README describes
the exact file naming and section structure agents will expect.

## Provenance discipline

Per `diary/00_charter.md`, every identity cited in downstream analyses
must carry one of three provenance tags:

- **(scan)** — verbatim from a file under `scans/` (cite filename + page).
- **(transcription)** — copied from a file under `transcriptions/` (cite
  filename + section). The transcription itself must point at the upstream
  primary source.
- **(training-memory)** — recalled from training data, MUST be numerically
  verified before use.

A scan/transcription entering `corpora/` is the precondition for upgrading
a previously training-memory-only identity to (scan) or (transcription)
status in `insights/CANDIDATE_INSIGHTS.md`.

## Hunt 5 highest-leverage target

The single highest-leverage scan arrival per `insights/HUNT_MAP.md §5` is
the Berndt 1984 typeset edition of the **Quarterly Reports** (HAL OA PDF:
`https://hal.science/hal-03912911/document`, see
`manifest/sources_letters_papers_qr.md §C.3`). When that PDF arrives:

1. Drop the raw PDF as `scans/QR_berndt_1984_blms.pdf` (large; gitignored).
2. Transcribe section-by-section into
   `transcriptions/quarterly_reports/qr<N>_section_<M>.tex` per the
   README in that sub-directory.
3. For each transcribed snippet, run
   `transcriptions/operator_tagging_schema.py` over the LaTeX text. The
   schema returns per-operator confidences ∈ [0,1] — entries scoring
   ≥0.5 on any operator are flagged for inspection; the goal per HUNT_MAP
   §5 prediction is to verify the conjecture that 5–10 operators recur
   80%+ of the time.

The full Hunt 5 dataset of (snippet → operator-tag) pairs is the
"latent-vocabulary" evidence for the latent-space-speedrun hypothesis.
