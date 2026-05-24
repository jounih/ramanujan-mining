# Diary 27 — Chandra 2 API smoke test on LN p. 341 (`page-340.jpg`); OCR audit vs known content

**Date:** 2026-05-24 (evening)
**Source:** Datalab hosted Chandra 2 OCR API output on
`corpora/transcriptions/chandra_benchmark/in/page-340.jpg` (= LN reprint
p. 341, the canonical 1729 page; pagination off-by-one per diary 21),
audited against the ground-truth content recorded in diary 21 (Hunt 1
closure) and Ono & Trebat-Leder *The 1729 K3 Surface* (arXiv:1510.00735).
**Status:** Smoke test SUCCEEDED end-to-end; the OCR audit yields a
clear character-class error profile that bounds Chandra 2's reliability
on Ramanujan's handwriting.

## Setup

Pivoted off local `chandra --method hf` (crashed user's Mac repeatedly;
see `corpora/transcriptions/chandra_benchmark/README.md` history). Now
using the Datalab API via `corpora/scripts/chandra_api_runner.py` with
settings tuned for handwritten math:

- `mode="accurate"` (slowest tier — needed for handwriting)
- `output_format="markdown,html,json"`
- `disable_image_captions=True`

Smoke-test target: `page-340.jpg` (the famous 1729 page; ground truth is
diary 21 — three rational functions over `1 − 82x − 82x² + x³`; master
identity `a_n³ + b_n³ = c_n³ + (−1)ⁿ`; six numerical examples including
`9³ + 10³ = 12³ + 1`, `135³ + 138³ = 172³ − 1`, etc.).

## What the API returned (selected lines from `page-340.md`)

| Ground truth (diary 21 / Ono) | Chandra 2 API output | Verdict |
|---|---|---|
| Three rational functions `(i),(ii),(iii)` numerator `1−82x−82x²+x³` | Three rational functions `(i),(ii),(iii)` numerator `1 - 85x - 85x² + x³` | **STRUCTURE OK, DIGIT WRONG** (82→85) |
| Display equations as fractions (LaTeX) | `$$\frac{1 - 85x - 85x^2 + x^3}{5 + 8x - 10x^2} = c^0 + c^1x + c^2x^2 + \dots$$` | **LATEX SYNTHESIS OK** (exponents-as-superscript on `c^0 c^1 …` correct) |
| Master `a_n³ + b_n³ = c_n³ + (−1)ⁿ` | `$$a^w_2 + b^w_3 = x^w_2 + (-1)_3$$` (with `w` = unparsed pre-superscript) | **STRUCTURE PARTIAL** — `³` exponent collapsed to subscript `_3`; the leading `a_n` index was rendered as `a^w_2` (spurious `w` and `_2`) |
| `9³ + 10³ = 12³ + 1` | `$$d_3 + 10_3 = 15_3 + 1$$` | **NUMBERS WRONG** (9→d?; 12→15); structure preserved |
| `135³ + 138³ = 172³ − 1` | `$$132_3 + 138_3 = 125_3 - 1$$` | **NUMBERS WRONG** (135→132, 172→125); sign correct |
| (other 4 numerical examples) | Variously garbled in numbers | **CONSISTENT PATTERN** — see §"Error classification" below |
| 16 blocks of structure total | 16 blocks detected (`page_stats.num_blocks=16`) | **BLOCK-LEVEL DETECTION 100% OK** |
| Walltime ground-truth | `runtime=5.87s` server, `elapsed=8.76s` wall | **FAST ENOUGH** for the 1,149-page corpus (~20 min async) |

Side-by-side artifacts: `corpora/transcriptions/chandra_benchmark/out/{page-340.md,page-340.html,page-340.json}`.

## Error classification (Chandra 2 on Ramanujan's hand)

Four distinct error classes appear consistently:

| Class | Description | Frequency on this page | Severity |
|---|---|---|---|
| **A: Digit substitution** | Cursive `2 ↔ 5`; `7 ↔ 1`; `8 ↔ 0` | ~6 instances in 8 number tokens | HIGH (corrupts numerical content) |
| **B: Exponent ↔ subscript** | `n³` → `n_3` (cube exponent read as subscript-3) | All exponents on the page | HIGH (changes meaning — `n³` is arithmetic, `n_3` is sequence indexing) |
| **C: Spurious adornments** | Pre-superscript `w` / `w_2` annotations inserted on bare letters | ~3 places in displayed equations | MEDIUM (introduces phantom variables) |
| **D: Letter/digit confusion** | `9` → `d`; `i` → `l`; `8` → `S` | ~2 instances | MEDIUM-HIGH |

What WORKS well:
- **Block layout**: every display equation isolated correctly; paragraph breaks correct; numbered list `(i),(ii),(iii)` recognized
- **LaTeX/MathML syntax**: fraction structure `\frac{...}{...}` rendered correctly; power series `c^0 + c^1x + c^2x^2 + \dots` correctly typed
- **Bounding boxes**: `page-340.json` carries per-block bbox + polygon coordinates — useful for layout-aware downstream tools

## Implications for the OCR plan

1. **Chandra 2 is good for STRUCTURAL transcription** — block layout,
   equation isolation, generic LaTeX scaffolding — but **NOT reliable
   for character-level numerical content** on Ramanujan's hand without
   human review.
2. **The exponent-as-subscript class-B error is systemic** — every cube
   `³` became `_3`. This means any direct programmatic use of the
   markdown for numerical evaluation is unsafe; the output needs a
   post-processing pass that flags `_<digit>` as a candidate `^<digit>`
   when the variable convention says so (e.g. on a cube-near-identity
   page where everything is `³`, replace all `_3` with `^3`).
3. **For Project C seed extraction** (the downstream goal — feed OCR'd
   identities into `rkc/search/seeds.py`), the workflow becomes:
   a) Chandra API → markdown
   b) Human spot-check + corrections OR a structured rules-based
      post-processor (exp→sub class-B fix; common digit-confusion
      class-A repairs against known constants)
   c) Sympify the cleaned LaTeX into seed expressions
   The middle step is necessary; we cannot trust raw OCR for the
   numerical detail.
4. **A useful API-side experiment** (deferred to a later session):
   try `extras="chart_understanding"` or one of Datalab's other extras
   to see if any flag improves the exponent-handling for math.

## Verdict

| Question | Answer |
|---|---|
| Is the API path operational? | **YES** — end-to-end works in 8.76 s, all output formats present |
| Is structural OCR usable for downstream programmatic work? | **YES** for block-level layout; markdown+html+json all serviceable |
| Is character-level OCR usable WITHOUT human review? | **NO** — at least 4 error classes appear consistently; numerical content corrupted on every example tested |
| Is it good enough to scale to the 1,149-page corpus? | **YES** for a pre-pass that produces draft transcriptions for human/agent review; cost and walltime are fine |
| Should we add `--async` for bulk runs? | **YES, recommended** before doing the bulk pass (next-step task) |

## Confidence

**High** on the operational pipeline (test reproducible; settings
documented; idempotency proven). **Medium-high** on the error
classification (one page; would refine after 3-5 more spot-checks across
different handwriting densities). **High** on the recommendation:
Chandra 2 is the right pre-pass, not a hands-off transcription engine.

## Follow-up leads (in priority order)

1. **Add `--async` flag** to `chandra_api_runner.py` using
   `AsyncDatalabClient` so the 1,149-page bulk pass takes ~20 min
   instead of ~3 h.
2. **OCR a Hunt-4-relevant subset** (the 15 class invariants on LN
   p. 342 — see diary 21 §"Hidden Hunt 4 / Hunt 1 overlap"): these
   are textually simpler (table-like) and likely OCR more cleanly than
   the cube-identity page. Good second data point for the error
   classification.
3. **Write the class-B post-processor** (`_3` → `^3` when context-
   appropriate): trivial regex on the markdown; would dramatically
   improve downstream sympify-ability of cube/square/n-th power
   identities.
4. **Spot-check 3-5 more pages** to firm up the error-class profile
   (this diary is based on n=1).
5. **Test the `extras` flag** for OCR-mode improvements (one parameter
   sweep; if any extra helps numerical-content recognition, that's a
   big win).

## Bottom line

**The Datalab Chandra 2 API path is OPERATIONAL.** First-page smoke
test on the canonical 1729 page succeeds end-to-end in 8.76 s with
clean structural OCR (block layout, LaTeX equations, paragraph breaks
all correct), but with a consistent ~4-class character-error profile
on Ramanujan's hand (digit substitution; exponent-as-subscript;
phantom adornments; letter/digit confusion). The output is a usable
DRAFT requiring human/agent review for numerical content, not a
hands-off transcription. Confidence: **high** on the pipeline and the
verdict; ready to scale (with `--async`) to the full 1,149-page
corpus when needed.
