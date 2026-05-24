# Ramanujan Mining Run — Live TODO

The live list of open action items. The bottom of the file preserves the
historical record of completed work. New work goes near the top; finished work
gets moved into the historical record.

**Last major update:** 2026-05-24, after Hunt 5 closure (diary 20) and
ingestion of the ChatGPT-Pro source pack at `chatgpt-pro-mining/`.

---

## Now actionable (Hunts unblocked by the source pack)

### H1. Hunt 1 — Lost Notebook pp. 341-343 (1729 / two-cubes / K3) — UNBLOCKED

**Source.** `chatgpt-pro-mining/.../priority_sources/lost_notebook_pages_341_343/`
(page images) + `chatgpt-pro-mining/.../priority_sources/open_access_context_pdfs/ono_trebat_leder_1729_k3_surface_arxiv_1510.00735.pdf` (8 pages).

**Predict (HUNT_MAP §1).** 60-80% of the identities on these three pages
parameterise a 2-parameter family of K3 surfaces. Ono *speculated* it; nobody
has done the full inventory.

**Concrete deliverable.** A `formula_record_schema.json`-shaped catalogue of
every identity / observation Ramanujan writes on pp. 341-343, each tagged with:
classical-known / rediscovered / corpus-novelty / K3-parameterisation /
none-of-the-above. Then count the K3 fraction. Output: a new diary entry
+ `analysis/results/hunt1_k3_inventory.csv`.

**Tractable in one focused session** with image-reading (handwritten facsimile,
3 pages). If image quality is poor, fall back to Chandra OCR per H4 below.

### H2. Hunt 5b — Notebooks operator tagging — UNBLOCKED

**Source.** `chatgpt-pro-mining/.../primary_originals/pdfs/notebooks/` (4
facsimiles: NB1 380p, NB2 355p, NB3 35p, Lost Notebook 379p) +
`chatgpt-pro-mining/.../primary_originals/page_images/` (1,149 extracted page
images).

**Predict.** The 4 operators that did NOT fire in the QRs (`modular_S_transform`,
`eisenstein_normal_ordering`, `q_shift`, `class_field_galois_average`) *will*
fire heavily in specific Notebooks chapters per Berndt's TOC: NB II ch. 16
(q-series), ch. 17 (modular equations), ch. 21 (Eisenstein + class invariants).
Confirming this establishes the **QR-vs-Notebooks toolkit contrast** as the
real cog-sci finding (diary 20, BIG_IDEAS_REVIEW §2 + §4).

**Scope.** Don't try to tag all 1,149 pages. Pick 3-5 specific chapters
chosen to test the 4 unfired operators:
- NB II ch. 16 → q_shift
- NB II ch. 17 → modular_S_transform
- NB II ch. 21 → eisenstein_normal_ordering + class_field_galois_average
- LN ch. on partial-theta (pp. 28-39) → mock-theta context (cross-check rkc)

**Blocker.** Page images are handwritten facsimiles, not typeset text like
the QRs were. Will need OCR (Chandra) or careful image-reading. See H4.

### H3. f5/f7 Watson-Hickerson instrumentation for `rkc/completions.py`

**Source.** `chatgpt-pro-mining/.../primary_originals/pdfs/published/` may
contain Hickerson 1988 / Berndt-Chan; check first. If not, fetch directly
(open-access from arXiv / hrj.episciences.org).

**Concrete deliverable.** `rkc/completions.py` returns numerical values for
f5 and f7 mock-theta inputs at ≥30 digits with a certificate, just like f3
does today. Adds unit tests. Removes `CompletionNotImplemented` for f5/f7.
Diary entry. Per BIG_IDEAS_REVIEW §1, this closes the recognizer end-to-end
on all 3 registered mock-theta families.

### H4. Install Chandra OCR + benchmark against a Lost Notebook page

**Source.** github.com/datalab-to/chandra (open-weights from HuggingFace,
tested specifically on Ramanujan's letters to Hardy per user). Pack ships a
wrapper at `chatgpt-pro-mining/.../phase2_context/run_chandra_ocr.py`.

**Concrete deliverable.**
1. Install Chandra (pip + HF model download).
2. Run on Lost Notebook pp. 341-343 + 2-3 representative NB II pages.
3. Hand-grade output: characters correct, mathematical notation correct,
   typesetting correct, structure preserved.
4. Compare against alternatives: tesseract baseline, math-aware OCR
   (e.g., LaTeX-OCR / pix2tex), Claude vision direct image read.
5. If Chandra wins, set it up as the standard pipeline for facsimile →
   transcription. Output: a comparison MD in `corpora/transcriptions/`.

Foundation for H1, H2, and any future facsimile work.

---

## Tractable without primary scans

### W1. Architecture paper draft: kernel-fingerprint compiler

**From BIG_IDEAS_REVIEW §1.** Recognizer is shipped + benchmarked. Draft from
existing artefacts (rkc/, A1-A7, DID_NOT_PAN_OUT). Target: Computing in
Science & Engineering, ACM TOMS, or workshops (ML4PS at NeurIPS, JuliaCon).
1-2 weeks of focused writing.

### W2. Closure paper draft: cohomological irreducibility of the mock-theta shadow

**From BIG_IDEAS_REVIEW §3.** Pass D is closed at high confidence; 20
candidates across 5 structurally-different families all fail; two decisive
structural arguments. Target: Comm. Math. Phys. or Physical Review Research.
The honest "we tested hard, none works, here's why structurally" is itself
the result.

### W3. Watson-identity calibration regime extension

The W-partner formula in `analysis/17_*.py` is calibrated only for α ≤ 0.7;
(0.7, π) flagged `regime="near-cusp-warning"` with uncomputed q₁⁴ correction.
Computing the next-order correction extends the calibrated regime. Small,
self-contained, useful.

### W4. `recognize_composite` `numerical_completion` propagation

Cheap fix flagged in diary 16; deferred. Wire the opt-in flag through to
per-component calls so composites return values not flags. <1 day of work.

### W5. Small operator-composition search prototype

**From BIG_IDEAS_REVIEW §7.** Build a small operator-composition search
using the 7 QR operators; generate ~100 candidate identities; run them
through the recognizer + mpmath/PSLQ numerical verification; classify
candidates as classical-known vs genuinely new. Even 1-2 new identities
would validate the approach. Bounded scope (~1 week); is the seed of the
larger "LLM + symbolic-verification" frontier-AI bet.

### W6. Add umbral-operator kernels to the rkc/ recognizer

**From BIG_IDEAS_REVIEW §2b (added after parallel-Claude review).** QR III §12
uses formal-power-series operator algebra (shift E, difference Δ, RL fractional
D^α) — structurally the natural lens for the recognizer. Add umbral-operator
primitives to `rkc/registry.py` as new kernels with degeneracy detectors.
After this, the recognizer can route QR III-style identities, not just the
QR I + QR II Mellin/Master cluster. Concrete + bounded (~1 week).

### W7-pre. Check QR II §3 cubic-roots-of-unity for Gauss-sum degeneracy awareness

**From parallel-Claude review.** QR II §3 (lines 2086-2280 of the HRJ text)
uses the cubic-roots-of-unity multisection
`1 - x³/3! + x⁶/6! - ... = (e^{-x} + e^{-xω} + e^{-xω²}) / 3`. This is the
same operator family as the **Gauss-sum silent-zero hazard** the recognizer
guards against ([CANDIDATE_INSIGHTS §A4](insights/CANDIDATE_INSIGHTS.md);
implemented at `rkc/registry.py` for q ≡ 2 mod 4). Quick test: does QR II §3
mention or implicitly guard against the q ≡ 2 mod 4 case (the cube-root case
analogue would be q ≡ 0 mod 3 or some sub-case where the sum degenerates)?

If yes → bibliographic evidence that the silent-zero hazard was in
Ramanujan's working knowledge, not a modern engineering catch. Strengthens
the §A4 finding. A small note to add to diary 20 or as a new short diary
entry.

If no → still informative: Ramanujan happened not to hit the degeneracy
because he restricted to specific cubic roots, but didn't generalise the
caveat. Still worth a one-line note.

**Effort:** ~30 minutes (just careful re-read of QR II §3, lines 2086-2280,
plus 1-2 paragraphs of write-up).

### W8. "Pre-Julia iteration theory in Ramanujan's third Quarterly Report" — standalone paper scope

**From parallel-Claude review.** QR III §4-§10 contains explicit fractional-
iteration computations (Chebyshev semigroup F(x) = x²-2 with `F^n(x)` via
cosh-formula; F(x) = x²+2x, x²-2x, x²+4x; iteration of `x → (1-x)/(1-x²)` at
fractional r) and the infinitesimal generator `ψ_1(x) = C/F(x)` of the
iteration flow. Schröder (1871) and Koenig (1884) predate Ramanujan; the
ψ_1 = C/F identification, however, is the Lie-theoretic content — the bridge
between iteration theory and one-parameter semigroups that becomes the
renormalisation-group setup decades later. **Notably this prefigures Julia
(1918) and Fatou (1917-19) by 3-4 years.**

**Concrete first step:** literature scan. Has modern work on Ecalle resurgence,
Belitskii normal forms, or holomorphic dynamics integrated Ramanujan's QR III
fractional-iteration work? If no → a short standalone paper "Pre-Julia
iteration theory in Ramanujan's third Quarterly Report" is the natural
deliverable, with the explicit linearizations + the ψ_1 = C/F identification
as the historical artefact. Target: Historia Mathematica or a focused
math-history note in a number-theory venue.

**Effort:** literature scan ~1 day; paper ~2-3 weeks if the lit scan
confirms novelty. Worth a focused agent.

### W7. B1.5 fractional-Fokker-Planck bridge experiment

**From BIG_IDEAS_REVIEW §3b (NEW).** Parallel to the closed B1 modular bridge:
pick a 1D fractional Fokker-Planck system with a known closed-form propagator
(plenty in the Klafter / Metzler anomalous-diffusion literature), compute its
partition function, and test whether the "Markovian-surrogate residual" is
recognisable from QR III's Schröder / RL / umbral machinery.

If yes: write up as the second Ramanujan-style FEP bridge, parallel to the
closed (and falsified-for-candidate-families) modular bridge.

If no: structural reason for closure becomes a sharper result — both modular
and fractional-calculus generative-model classes resist Ramanujan-style
completion, suggesting whatever "completion" means is even more specific than
B1 closure already implied.

Status: SCOPED but UNTESTED. Single-experiment scope ~2-3 weeks.

---

## Partially blocked (have facsimiles, missing Berndt commentary)

### B1. Hunt 2 — Modular equations at level ≥23

Have NB II facsimile pages; missing Berndt Notebooks Parts III-V commentary
(which is where Berndt identifies *which* facsimile pages contain the level
≥23 entries). Workaround: page-by-page facsimile reading is possible but
slow. Lower priority than H1, H2 above.

### B2. Hunt 3 — Eisenstein-style continued fractions

Have Bhatnagar arxiv:2208.12656 (q-CF context) + NB facsimiles; missing
Berndt Part V ch. 32 (which catalogues the relevant Notebook entries).
Workaround: read Bhatnagar to identify candidate entries, then look in the
facsimiles directly.

### B3. Hunt 4 — Unproven class invariants Gₙ

Have Lost Notebook facsimile; missing Andrews-Berndt LN Vol I supplement
pp. 200-220 (which identifies *which* 18 of Ramanujan's 116 tabulated Gₙ
are unproven). Workaround: would need to re-enumerate from the facsimile
directly, which is significant work.

Partial progress already: 8 invariants verified to ≥100 digits via PSLQ in
Experiment 08 (diary 09).

### B4. Hunt 6 — Ramanujan-Sato at moonshine levels

Have NB II facsimile + open-access context PDFs; missing Cooper *Theta
Functions* (which catalogues RS series by level). Workaround: re-derive the
level-by-level catalogue from Berndt's open-access papers (Berndt's papers
on theta functions are mostly open-access; the book is the
synthesis).

---

## Standing items (per BIG_IDEAS_REVIEW)

- **Cohomological generative model** (BIG_IDEAS §3). Research-grade math
  question, not a well-scoped experiment. Entry points in diary 19 §"what next".
- **LLM + symbolic-verification operator search** (BIG_IDEAS §7). Long-running
  research project; W5 above is the smallest first step.
- **Library-design / silent-zero technical note** (BIG_IDEAS §5). The
  silent-zero hazard at Gauss sums q ≡ 2 mod 4 → 1-2 page note for
  Mathematics of Computation. Cheap, citable.

---

## Sourcing — gaps remaining

What the ChatGPT-Pro pack does NOT cover (copyrighted books):

| Source | Unlocks | Notes |
|---|---|---|
| Andrews-Berndt *Lost Notebook Part IV* (Springer 2013) | Hunt 1 deeper, Hunt 4 | Have the LN facsimile + Ono context; missing the editorial commentary |
| Berndt *Notebooks Part V* (1998), ch. 32 + ch. 34-37 | Hunt 3, Hunt 4 | Have the NB facsimiles; missing the chapter-organisation map |
| Berndt *Notebooks Parts III-V* (1991-1998), modular equations | Hunt 2 | Have NB II facsimile; missing the level-by-level map |
| Cooper *Ramanujan's Theta Functions* (Springer 2017) | Hunt 6 | Have NB + papers; missing the synthesis |
| Berndt-Rankin *Ramanujan: Letters and Commentary* (AMS 1995) | Letters/QR context | QRs themselves unlocked via the open-access HRJ 2022 reprint |

Trinity / Wren IIIF (Add. MS a/94) — high-resolution scans of original papers
— are also not in the pack. The pack ships a downloader
(`chatgpt-pro-mining/.../phase2_context/wren_ramanujan_downloader.py`) that
can run on this machine.

---

## Constraints in this environment

- Full network access (arXiv, HuggingFace, GitHub, ...).
- macOS / zsh; Python 3.12.7 in `.venv/`.
- PARI/GP can be installed locally if needed.
- The primary-source corpus lives at `chatgpt-pro-mining/` (gitignored,
  ~352 MB). See CLAUDE.md for the inventory.

---

# Historical record (completed)

## Pass A — substantiate the central hypothesis on diverse kernels

- [x] **02 Theta-dual switching curve.**
- [x] **03 RKC v0 with rigorous erfc tail bounds.**
- [x] **04 Lambert ↔ Eisenstein switching** (shipped as Exp 12). Crossover
  β* = 2π; gain up to 1.21×10⁶× at extreme β. Two normalization gotchas
  caught (sign factor, Bernoulli prefactor cancellation). Diary 10.
- [x] **05 HRR exact p(n) vs Euler-product recurrence.** Term-count crossover
  small n; wall-clock crossover n=10⁵ (HRR per-term cost is enormous without
  binary-splitting + FLINT). Diary 07. Caught a silent-zero failure mode
  (`round(float(mpf))` mangles p(1000)); fixed with `int(mpmath.nint(...))`.
- [x] **06 Ramanujan 1/π vs AGM vs Chudnovsky vs Machin-like.** Diary 06.
- [x] **07 Divisor sum σ_k(n).** Batch crossover N* = 41. At N=10⁵
  method C uses 5.5% of A's ops. Diary 08.
- [x] **08 Class invariants Gₙ direct vs radical.** 8 invariants PSLQ-verified
  to ≥100 digits. Radical/direct cost ratio grows 1× → 369× as precision
  climbs 30 → 1000 digits. Diary 09.

## Pass B — automated recognition layer

- [x] **09 Kernel-fingerprint matcher v0.** Diary 04.
- [x] **10 RKC routing benchmark v1.** 11 kernels; benchmark 54/55 = 98.2%,
  macro precision 1.00 (zero false positives). Silent-zero Gauss-sum hazard
  fires on every q ≡ 2 mod 4 case. Diary 11.
- [x] **14b RKC routing benchmark v2.** **55/55 = 100%**. Macro precision 1.00,
  macro recall 0.95. No v1 regressions. Diary 14.

## Pass D — FEP / mock-modular bridge

- [x] **15 Generative model whose evidence is a mock theta.** Lattice gas
  with two bosonic species at z = -1; Z(q) = f(q) verified to 25-50 digits
  across β ∈ [0.05, 10]. Diary 13.
- [x] **16 "Shadow = mutual information?" probe.** 4 candidates (MI, KL,
  Surprise, Fisher) all fail; structural reason (g* bounded at cusp). Diary 13.
- [x] **17 Mock-theta residual EBM v1.** Exact Hickerson-Mortenson shadow +
  Eichler integral via Watson 1936; bias reduction ~258 bits at small β;
  modular cross-check at ≥30 digits. **Caught a real v0 bug**: even Kronecker
  character used when odd primitive mod 12 was required. Diary 12.
- [x] **18 Bounded-at-cusp shadow probes.** 8 new candidates fail (Rényi-α,
  Bhattacharyya, Hellinger², entropic uncertainty). Sharpened conjecture:
  g* is an **Eichler cocycle in H¹(Γ, V_k)**. Diary 15.
- [x] **20 Wigner-negativity-aware divergences.** 4 candidates fail. One
  zero-parameter cusp-asymptote coincidence (log(2)/g*(0) = 0.20025 vs
  empirical 0.20033); bulk shape fails 100% → coincidence not proportionality.
  Diary 17.
- [x] **21 Path-measure functionals.** 3 candidates fail. **Decisive
  structural finding**: cooling path traverses imaginary-axis half-line in
  the wrong direction (cusp 0 → interior vs Eichler interior → ∞). Rules
  out the partition-function-path-integral interpretation. Diary 18.
- [x] **22 Direct Eichler-cocycle reconstruction from transfer matrix.**
  STRUCTURAL NEGATIVE: trivial spectrum + (K+1)² S-transform dim mismatch
  + K→∞ defect reduces to Watson 1936 (tautological). Diary 19.

**Pass D closed.** 20 candidates across 5 structurally-different families
all fail. Cohomological-irreducibility conjecture established at
medium-high → high confidence.

## Pass B follow-up — recognizer ↔ Eichler integration

- [x] **19 `MODULAR_COMPLETION_REQUIRED` → Watson-Hickerson.**
  `rkc/completions.py` shipped. f3 mock-theta inputs return numerical values
  to ≥30 digits with a certificate. 50/50 unit tests. Diary 16.

## Hunt 5 — Quarterly Reports operator tagging

- [x] **23 QR operator tagging.** Hand-tagged all 33 math-content sections of
  Berndt's 2022 HRJ reproduction. 80% prediction FALSIFIED at 57.6% coverage;
  4 of 6 predicted operators NEVER fire. Revised 7-operator basis covers
  ~91%. QR III is fractional iteration / Hardy orders / operator calculus,
  not modular forms. **Hunt 5 closed.** Diary 20.

## Cross-cutting deliverables (shipped)

- [x] `insights/CANDIDATE_INSIGHTS.md` — substantiated findings (A1-A7, B1,
  C, D, D1, E synthesis).
- [x] `insights/DID_NOT_PAN_OUT.md` — 15 entries (4 REFUTED, 4 CORRECTED,
  5 PARTIALLY REFUTED, 2 DOWNGRADED) + OUTSTANDING.
- [x] `insights/HUNT_MAP.md` — Hunt-by-Hunt with current unblock status.
- [x] `insights/BIG_IDEAS_REVIEW.md` — running judgment on the 7 big-picture
  ideas from the brainstorm.
- [x] `corpora/transcriptions/operator_tagging_schema.py` — 6-operator
  schema; now flagged 2 verified / 4 falsified-for-QR-corpus.
- [x] `rkc/` standalone package (recognizer, registry, costs, routing,
  completions, tests).
- [x] `diary/` (20 entries) + `diary/INDEX.md`.
- [x] `manifest/` (cataloguing of primary sources).
- [x] `sota_comparisons/` (physics & computation, open problems / under-mined
  corners).
