# Ramanujan Mining Run — Handoff Brief

You are taking over an ongoing research run that has been running across
multiple Claude Code sessions. The run is mining Ramanujan's mathematical
work for novel insights in three areas:
**(1) computation acceleration**, **(2) energy-based modeling / Friston FEP**,
**(3) "latent-space speedrun" — what compressed representations Ramanujan
carried in his head**.

This file is your orientation. Read it once, then start from
[todo.md](todo.md).

---

## First six files to read (in order)

1. [diary/00_charter.md](diary/00_charter.md) — mission, operating discipline, corpus inventory
2. [diary/INDEX.md](diary/INDEX.md) — every diary entry with topic + source pointer
3. [todo.md](todo.md) — current state of every Pass A/B/C/D/E + hunts + cross-cutting deliverable
4. [insights/CANDIDATE_INSIGHTS.md](insights/CANDIDATE_INSIGHTS.md) — every substantiated finding, with confidence + novelty tags
5. [insights/DID_NOT_PAN_OUT.md](insights/DID_NOT_PAN_OUT.md) — the equally-important refuted / corrected speculations
6. [insights/BIG_IDEAS_REVIEW.md](insights/BIG_IDEAS_REVIEW.md) — running judgment on which big-picture ideas still have legs

After those six files you'll know what's been done, what's pending, what was
tried and didn't work, and where the open questions sit. Then read
[insights/HUNT_MAP.md](insights/HUNT_MAP.md) for the prioritized targets and
their current scan-blocked / unblocked status.

---

## File layout

```
ramanujan-mining/
├── CLAUDE.md                  ← you are here
├── todo.md                    ← live state of all passes + open action items
├── analysis/                  ← experiment scripts; numbered ##_*.py
│   ├── 02..23_*.py            ← experiments (some skipped — see todo)
│   └── results/               ← every script writes a *.csv here
├── chatgpt-pro-mining/        ← ★ LOCAL ONLY (gitignored, ~352 MB) ★
│                                 ChatGPT-Pro-curated source pack
├── diary/                     ← numbered ##_*.md entries (latest is the head)
│   ├── 00_charter.md
│   ├── INDEX.md               ← keep updated when adding entries
│   └── 01..20_*.md
├── insights/                  ← synthesis documents
│   ├── CANDIDATE_INSIGHTS.md  ← positive findings, organized A/B/C/D/E + D1
│   ├── DID_NOT_PAN_OUT.md     ← refuted / corrected / outstanding
│   ├── HUNT_MAP.md            ← priority targets and current unblock status
│   └── BIG_IDEAS_REVIEW.md    ← which big-picture ideas have legs after each pass
├── manifest/                  ← cataloging of primary sources
├── sota_comparisons/          ← what published work covers vs doesn't
├── corpora/                   ← primary sources
│   ├── scans/                 ← raw facsimile PDFs (gitignored above 1MB)
│   ├── transcriptions/        ← LaTeX/unicode transcriptions
│   │   ├── README.md          ← format spec
│   │   ├── operator_tagging_schema.py  ← 6-operator schema (now QR-verified)
│   │   └── quarterly_reports/ ← qr_section_index.json + tagging deliverables
│   ├── RamanujanMachine/      ← vendored 3rd-party (Trinity College Dublin)
│   └── RamanujanMachine_v0/   ← older vendored fork
└── rkc/                       ← STANDALONE PACKAGE — kernel-fingerprint recognizer
    ├── __init__.py, recognizer.py, registry.py, routing.py, costs.py
    ├── completions.py         ← MCR route wired to exp 17 Eichler integral
    ├── README.md              ← 1-page worked example
    └── tests/                 ← pytest unit tests; MUST stay green (50/50)
```

The repo is on `main` branch at [github.com/jounih/ramanujan-mining](https://github.com/jounih/ramanujan-mining)
(private). Default expectation: **commit & push frequently** — the user's
preference, and diary entries are the durable artifacts.

---

## ★ chatgpt-pro-mining/ — the local-only high-leverage corpus ★

The `chatgpt-pro-mining/` directory (gitignored, ~352 MB) is the curated
source pack ChatGPT-Pro assembled to unblock the Hunts. **This is the most
operationally important resource in the repo** for any hunt or notebook-tagging
work; without it you are blind to the primary sources.

What's inside (per Hunt status as of diary 20):

| Hunt | What | Where | Status |
|---|---|---|---|
| 1 | Lost Notebook pp. 341-343 (1729/K3) | `priority_sources/lost_notebook_pages_341_343/` + Ono arxiv | **CLOSED** (diary 21; K3 prediction falsified at 33%) |
| 1a | Pagination ambiguity follow-up | [downloaded-pdfs/](downloaded-pdfs/) AB *Lost Notebook Part IV* | **UNBLOCKED** |
| 2 | Modular equations at level ≥23 | [downloaded-pdfs/](downloaded-pdfs/) Berndt *Notebooks Part V* Ch. X + NB II facsimile | **UNBLOCKED** |
| 3 | Eisenstein-style CFs | [downloaded-pdfs/](downloaded-pdfs/) Berndt *Notebooks Part V* Ch. 32 + Berndt-Yee RIMS 2002 | **UNBLOCKED** |
| 4 | Unproven class invariants | [downloaded-pdfs/](downloaded-pdfs/) AB *LN Part I* supplement + Berndt *NB Part V* Ch. 33-34 | **UNBLOCKED** |
| 5 | Quarterly Reports operator tagging | `priority_sources/quarterly_reports/` Berndt 2022 HRJ | **CLOSED** (diary 20; 57.6% < 80% predicted) |
| 5b | Notebooks operator tagging | `primary_originals/pdfs/notebooks/` (1,149 facsimile pages) + downloaded-pdfs commentary | **UNBLOCKED** |
| 6 | Ramanujan-Sato at moonshine levels | facsimile NB II + OA PDFs | PARTIAL (missing Cooper *Theta Functions*) |

**downloaded-pdfs/** is the second high-leverage local-only corpus (alongside
chatgpt-pro-mining/). It is **committed to this private repo** because the
user obtained the volumes legitimately from the authors (Berndt et al.) for
personal use; private repo so on-disk inclusion is fine, but **do not
redistribute outside this repo**. See
[downloaded-pdfs/README.md](downloaded-pdfs/README.md) for the per-file
manifest.
The pack contains: Berndt *Notebooks Part 1* + Part V (front and back of the
5-volume series; II/III/IV still missing); AB *Lost Notebook* Parts I-IV (complete);
Berndt-Yee RIMS 2002 (Eisenstein-series survey); Berndt-Dixit arXiv 2009
(αβ=1 Mellin-pair transformation, LN pp. 219-227); Berndt 2022 HRJ QR
reproduction (duplicate of chatgpt-pro-mining); RMS *Ramanujan Rediscovered*
front-matter preview only; KSR notebooks-chapter; 1927 Hardy-Aiyar-Wilson
*Collected Papers* (public domain).

The pack also has:
- `priority_sources/quarterly_reports/` — Berndt 2022 HRJ reproduction (used for Hunt 5)
- `primary_originals/page_images/` — 1,149 extracted page-images from the four facsimile PDFs
- `phase2_context/formula_record_schema.json` + `operator_tag_taxonomy.json` — alternative 20-operator broader taxonomy
- `phase2_context/run_chandra_ocr.py` + `wren_ramanujan_downloader.py` — auxiliary scripts
- `PACK_MANIFEST.csv` + `PDF_MANIFEST.csv` with SHA-256 hashes

What's **not** in the pack (copyrighted AMS/Springer): Andrews-Berndt *Lost
Notebook Part IV*, Berndt *Notebooks Part V*, Cooper's *Ramanujan's Theta
Functions*, Ramanujan: Letters and Commentary. These are the gap. Trinity/Wren
IIIF page images are also not included but a downloader is.

When you need a PDF or page image, look in this pack first. **If you OCR or
transcribe any facsimile page, drop the output under
`corpora/transcriptions/<source-tag>/` so it lands in the committed history
even though the source images stay local.**

---

## Conventions (non-negotiable)

### Provenance flags

Every cited identity carries one of:
- **(scan)** — primary source, page-cited; transcription expected in `corpora/transcriptions/`
- **(transcription)** — Berndt/Andrews printed text or verified GitHub mirror, cited
- **(training-memory)** — recalled from training data; **must be numerically verified before use** (≥50 digits via mpmath/PSLQ)

If a citation lacks a provenance flag, treat it as suspect.

### Diary discipline

- Every experiment session writes a numbered, dated entry in `diary/`.
- Each entry: `# Diary <N> — <topic>` + Date + Source/Status + body.
- Body: setup, what you did, numbers, surprises, one-line bottom-line claim
  with confidence tag (high / medium / low / indicative).
- Update [diary/INDEX.md](diary/INDEX.md) when you add an entry.

### Documentation discipline

- **Always commit findings to a markdown file so they survive context-window
  rotation.** Working state in the conversation is volatile; .md files in the
  repo are not.
- **Always add your own suggestions to `todo.md`** before / after raising them
  in chat. If you propose a next step in conversation, write it into todo
  the same turn. The chat scrolls; todo persists. User's standing
  instruction: "generally always add your suggestions to todo so they
  survive this context window".
- New synthesis that crosses multiple experiments goes in `insights/`.
- Per-experiment findings go in `diary/`.
- Action items go in `todo.md` (and TaskCreate during the working session).

### Claim discipline (strict)

- Every numerical claim must be reproducible by running the script
  (no orphan numbers).
- Tag speculation explicitly. The boundary between observation and
  interpretation must be clear in every diary entry.
- **If a "near match" exists in an experiment, report it as a near-match with
  the specific deviation pattern — never as a match.** Noisy positives are
  the worst possible outcome.
- The strict bar for proportionality claims: ≤1% relative deviation across
  ≥2 orders of magnitude in the swept parameter.
- Honest "did not pan out" entries go in `insights/DID_NOT_PAN_OUT.md`. The
  credibility of the run depends on this file growing alongside
  `CANDIDATE_INSIGHTS.md`.

### Bug-find protocol (per T7's mock-theta v0 bug)

The strongest single methodological lesson from the run: **rerun prior work
with explicit "verify rigorously" instructions every few experiments**. T7
caught a real character-parity bug in v0 of the mock-theta toy that the
original session's introspection missed. If you find a similar bug while
extending earlier work, retract the prior claim in `DID_NOT_PAN_OUT.md` and
ship the fix — never paper over.

---

## Environment

### Local context (this repo lives on the user's machine)

- macOS / zsh, full network access (arXiv/Wikipedia/HuggingFace OK).
- Python 3.12.7 in `.venv/` (3.11 not available on system; 3.12 is fine for
  sympy 1.14 + mpmath 1.3).
- PARI/GP can be installed locally if needed for class-number /
  modular-polynomial work.
- The user's primary-source corpus is at `chatgpt-pro-mining/` (gitignored,
  see section above).

### Dependencies

```
python 3.12 (3.11 originally specified; 3.12 substitute works)
sympy 1.14
mpmath 1.3
numpy
pytest (for rkc/tests)
```

All in `.venv/`. Activate: `source .venv/bin/activate`.

For OCR of handwritten facsimiles (Hunt 1, Hunt 5b on the Notebooks):
**Chandra OCR** (datalab-to/chandra on GitHub, weights on HuggingFace) is the
recommended tool — was tested specifically on Ramanujan's letters to Hardy.
Install + benchmark before bulk OCR work. The pack ships a wrapper at
`chatgpt-pro-mining/.../phase2_context/run_chandra_ocr.py`.

### Git workflow

```bash
# Standard cycle when finishing an experiment:
git add analysis/NN_*.py analysis/results/NN_*.csv diary/NN_*.md
git commit -m "Exp NN: <one-line summary>"
git push origin main

# Do NOT use --no-verify or --no-gpg-sign.
# Do NOT amend published commits.
# Do NOT force-push to main.
```

The repo is standalone on `main` (no feature branches required; create one
if doing a long-running spike).

---

## Current state (as of diary 20)

### Completed

- **Pass A (representation switching)**: 5 kernels substantiated (Gaussian
  theta, Bose-Einstein partition, Lambert-Eisenstein, π methods, divisor
  sum). Universal β\* = c·π crossover pattern (§A6); per-term-cost vs
  term-count framing (§A7).
- **Pass B (recognizer)**: shipped as standalone `rkc/` package. v2 hits
  **55/55 = 100%** on the routing benchmark with macro precision 1.00.
  **50 passing unit tests** (35 base + 15 completions).
  `MODULAR_COMPLETION_REQUIRED` route wired through to Watson-Hickerson
  Eichler integral — **f3 mock-theta inputs return numerical values to
  ≥30 digits with a certificate**; f5/f7 surface `CompletionNotImplemented`
  honestly.
- **Pass D (FEP × mock-modular bridge) — CLOSED for the candidate-family
  approach**: forward direction confirmed as an *identity* (lattice gas →
  f(q) to 25-50 digits); reverse direction *falsified for 20 candidates
  across 5 structurally-different families* (Exp 16, 18, 20, 21, 22). Two
  decisive structural arguments anchor the closure (Exp 21 path-direction;
  Exp 22 (K+1)² dim mismatch + Watson-reduction). **The cohomological-
  irreducibility conjecture is essentially established at medium-high →
  high confidence**: g\* is irreducibly an Eichler cocycle in H¹(Γ, V_k).
- **Hunt 5 (CLOSED, diary 20)**: 80% prediction falsified at 57.6% coverage;
  4 of 6 predicted operators never fire; revised 7-operator basis covers
  ~91%. QR III is fractional-iteration / Hardy-orders / operator-calculus,
  not modular forms.
- **Cross-cutting deliverables**: CANDIDATE_INSIGHTS.md, DID_NOT_PAN_OUT.md
  (15 entries + outstanding), HUNT_MAP.md (with current Hunt-by-Hunt
  unblock status), BIG_IDEAS_REVIEW.md (running judgment on the 7 big-
  picture ideas from the brainstorm).

### Open / actionable (see [todo.md](todo.md) for the live list)

**Hunts with primary-source material now in the pack:**
- **Hunt 1**: UNBLOCKED (LN pp. 341-343 page images + Ono K3 paper). Test
  the 60-80% K3-parameterisation prediction.
- **Hunt 5b**: UNBLOCKED (1,149 notebook facsimile pages). Operator-tagging
  on the Notebooks, scoped to chapters that test the 4 operators that
  didn't fire in the QRs (modular S-transform, Eisenstein normal-ordering,
  q-shift, class-field Galois average).
- **Hunts 2, 3, 4, 6**: PARTIAL unblock (have facsimiles; missing the
  copyrighted Berndt commentary books). Manual reading of facsimiles is
  possible but slower.

**Tractable without scans:**
- f5/f7 Watson-Hickerson instrumentation for `rkc/completions.py` (needs
  Hickerson 1988 / Berndt-Chan transcriptions; check pack first).
- Watson-identity calibration regime extension (α > 0.7).
- Architecture paper draft for the recognizer.
- Closure paper draft for the cohomological-irreducibility conjecture.

### Numbered slots that are FREE

- **Experiments**: 24+ are clear. (00, 01 reserved; 02-23 used.)
- **Diary entries**: 21+ are clear.

---

## Known gotchas (these will bite you if you don't watch for them)

1. **Silent-zero hazard at Gauss sums q ≡ 2 mod 4** (§A4). Built into
   `rkc/registry.py` as a degeneracy detector. If you add a new
   Gauss-sum-related kernel, *test the degeneracy branch explicitly* —
   sympy auto-reduces `2n²/6 → n²/3` before the matcher sees it; use
   `recognize_with_raw_string` for AST-pre-reduction work.

2. **Character parity in mock-theta shadows** (T7's bug). The unary theta
   shadow of Ramanujan's f3 uses the **ODD primitive character mod 12**,
   not the even Kronecker character. Using the even one makes the
   weight-3/2 theta with `n` in front vanish identically. Documented in
   `diary/12_*.md` and `DID_NOT_PAN_OUT.md` R2.

3. **Mock-theta v0 asymptotic claim was wrong** (T7). The "1/√β" asymptotic
   for the bias is incorrect; the actual modular-only residual saturates at
   the Watson-Hickerson radial limit 4/3. See `DID_NOT_PAN_OUT.md` R1.

4. **Bits-per-term is a misleading routing metric** (§A7). The recognizer's
   cost estimator must use per-term complexity, not just term count. HRR
   uses 4× fewer terms than pentagonal recurrence at n=10⁵ but is comparable
   in wall-clock without binary-splitting + FLINT.

5. **Cross-validate before benchmarking** any new representation-switching
   pair. At least one (kernel, β) cell must match to ≥40 digits across both
   representations before you trust the comparison. See `analysis/12_*.py`
   for the template: it caught a sign-factor bug and a Bernoulli-prefactor
   cancellation that would have shipped silently otherwise.

6. **Strict claim discipline at candidate 3 of any "shadow probe"**. Any
   path-measure / Eichler-shaped candidate is the structurally-most-likely-
   to-match candidate in the FEP × mock-modular investigation. A noisy
   positive at one of those is the worst-possible outcome — hold the
   ≤1% / ≥2-dex bar ruthlessly. Falsify cleanly or confirm cleanly; nothing
   in between.

7. **Hunt 5 lesson: predicted operator bases can be wrong without the
   underlying hypothesis being wrong.** The 6-operator HUNT_MAP §5 basis
   was falsified at 57.6%, but a revised 7-operator basis covers 91%. When
   running Hunt 5b on the Notebooks, do not assume the QR basis carries
   over — test the *predicted* basis (modular S, q-shift, Eisenstein,
   class-field) afresh against actual Notebook content. The QR-vs-Notebooks
   toolkit-contrast hypothesis is the real test.

---

## Bottom line

The intellectual win of this run so far is **the lens + the catalogue + a
closed conjecture + a partial-falsification-with-correction**, not new
theorems:

- An operational kernel-fingerprint recognizer with documented failure modes,
  end-to-end on mock-theta f3 (Pass B).
- A universal β\* = c·π crossover pattern across five independent kernels
  (Pass A).
- A **closed-verdict** FEP × mock-modular bridge story: cohomological-
  irreducibility conjecture established (Pass D, ~20 candidates across 5
  structurally-different families all fail).
- **The QR-as-Mellin/operator-calculus finding** (Hunt 5, diary 20): the
  Quarterly Reports are not a modular-forms document at all; QR III is
  fractional iteration / Hardy orders / operator calculus. The
  latent-space-speedrun hypothesis is supported with a corrected
  7-operator basis (91% coverage).
- The honest "did not pan out" log.

The deepest research question — *what compressed representations did
Ramanujan carry in his head?* — is now testable on a different corpus:
**Hunt 5b on the Notebooks** is the natural next test. Confirming a
*different but still small* toolkit in the Notebooks (vs. the QR toolkit)
would make the QR-vs-Notebooks contrast the headline cog-sci finding.

Carry on with the same discipline. Commit & push frequently. Diary entries
are the durable artifacts.

---

## Quick-start for a fresh Claude Code session

```bash
# 1. Latest main
git pull --ff-only

# 2. Activate venv (already set up)
source .venv/bin/activate

# 3. Verify everything works (<30 s)
python -m pytest rkc/tests/                      # expect 50/50 passing
python analysis/14b_recognizer_v2_benchmark.py   # expect 55/55 = 100%
python corpora/transcriptions/operator_tagging_schema.py  # expect 6/6 OK
python analysis/23_hunt5_qr_operator_tagging.py  # expect 57.6% overall coverage

# 4. Read CLAUDE.md (this file), then todo.md, then insights/BIG_IDEAS_REVIEW.md
# 5. Start work — incoming primary sources land under
#    chatgpt-pro-mining/ (local-only) or corpora/scans/ (gitignored >1MB)
```

If a new primary-source artefact arrives:
1. Drop the PDF or page images under `chatgpt-pro-mining/` (if part of
   the bundled pack) or `corpora/scans/<source-tag>/` (if separate).
2. If you OCR or transcribe, put the text under
   `corpora/transcriptions/<source-tag>/` so the transcription itself lands
   in git history even though the binary stays local.
3. For Quarterly Reports specifically: use the schema at
   `corpora/transcriptions/operator_tagging_schema.py`, output under
   `corpora/transcriptions/quarterly_reports/`.
4. For Notebooks (Hunt 5b): same schema, but expect to need to **add new
   operators** to it as new kinds of moves appear; the QR-derived schema
   may be incomplete for the Notebooks corpus.
5. Then dispatch a Hunt-N agent (see `insights/HUNT_MAP.md` for the
   specific prediction each scan is meant to test) or work through it
   directly.
