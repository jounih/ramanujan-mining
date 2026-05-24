# Ramanujan Mining Run — Live TODO

The live list of open action items. The bottom of the file preserves the
historical record of completed work. New work goes near the top; finished work
gets moved into the historical record.

**Last major update:** 2026-05-24, after Hunt 5 closure (diary 20) and
ingestion of the ChatGPT-Pro source pack at `chatgpt-pro-mining/`.

---

## Now actionable (Hunts unblocked by the source pack)

### H1. Hunt 1 — Lost Notebook pp. 341-343 (1729 / two-cubes / K3) — CLOSED

Result in [diary/21](diary/21_hunt1_lost_notebook_341_343.md);
falsification in [DID_NOT_PAN_OUT §R16](insights/DID_NOT_PAN_OUT.md). K3
fraction 33% (10/30), well below the 60-80% prediction. K3 material is fully
concentrated on p. 341 itself; pp. 342-343 are different topics. Three
sub-leads spawned:

#### H1a. Resolve pagination ambiguity (need Andrews-Berndt Part IV)

Ono's 2016 colloquium speculation about "pp. 342-343 near-counterexamples"
may refer to a different edition than the Narosa/Sirinudi facsimile inventoried.
Andrews-Berndt *Lost Notebook Part IV* chapter on "Approximations and
asymptotic methods, including 1729" would resolve. Copyrighted Springer book;
not in the local pack. Lower priority than H1b.

#### H1b. Cross-check p. 342 Weber class invariants against Berndt-Chan-Kang-Zhang

**Hunt 4 partial unblock.** p. 342 has a 15-row Weber `f₁(√-n)` table for
n ∈ {20,27,26,29,35,36,38,39,41,44,50,51,52,63,87}. Some of these
discriminants (-63 class number ≥ 4, -87 class number ≥ 6) likely overlap
the ~18 of Ramanujan's 116 tabulated invariants that were unresolved as of
2000. Cross-check: which (if any) appear here? Each unresolved one is
simultaneously a Hunt 1 deliverable AND a Hunt 4 deliverable.

Concrete deliverable: a CSV adding a `proof_status_2000` column to the
p. 342 rows of `analysis/results/hunt1_k3_inventory.csv` based on the
modern reproof table. ~half-day of work given the table.

#### H1c. Verify Ramanujan's `O(...)` bound on p. 343 against modern Thue-Siegel-Roth

p. 343 has explicit conjugate-product bounds for `|a^m b^n ⁵√2 - p_{m,n}|`.
Numerically verify (mpmath, ~100 digits) for specific (m,n) whether the
bound is tight, approximately tight, or loose. Compare against the modern
effective Thue-Siegel-Roth or Schmidt-subspace bound for ⁵√2. **If tight,
this is Ramanujan anticipating effective Diophantine bounds 25+ years
before Schneider-Mahler** — a dedicated diary entry on its own.

~1 day of work.

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

### H4. Install Chandra OCR + benchmark against a Lost Notebook page — PARTIAL

**Status.** Chandra installed (chandra-ocr 0.2.0 in `.venv`); model weights
downloaded (datalab-to/chandra-ocr-2 in `~/.cache/huggingface/`, 2.7 GB).
**The benchmark agent did not finish:** the `corpora/transcriptions/chandra_benchmark/page-341/`
directory is empty and the README.md was never written. The agent appears to
have run out of context / time after the install but before the actual run.

**Finish inline next session:**
1. Run Chandra on `chatgpt-pro-mining/.../priority_sources/lost_notebook_pages_341_343/page-341.jpg`
   (which per Hunt 1 finding is actually LN reprint p. 342 — the Weber class
   invariants page; a good test case since the structure is tabular).
2. Hand-grade output (characters / math notation / table structure).
3. Compare against the Claude-vision direct read used in Hunt 1.
4. Write the README.md with verdict.

Hunt 1's finding ("the facsimile is legible enough at the level of 'which
topic is this page about' to be decisive without OCR") suggests Chandra
is not on the critical path for Hunt 1 results but is critical for Hunt 5b
(1,149 pages to inventory). Worth finishing the benchmark before launching
Hunt 5b.

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

## Newly unblocked by downloaded-pdfs/

The user obtained Berndt-family commentary volumes directly from the
authors for personal use; they're now committed to this private repo at
[downloaded-pdfs/](downloaded-pdfs/) (see
[downloaded-pdfs/README.md](downloaded-pdfs/README.md) for the manifest).

### H5. Hunt 1a — Resolve Ono pagination ambiguity (Andrews-Berndt Part IV)

Sub-lead from H1 closure. Read AB *Lost Notebook Part IV* (2013) chapter on
"Approximations and asymptotic methods, including 1729". Locate Berndt's
own commentary on Ramanujan's pp. 341-343 cube material; identify where
Ono's "near-counterexamples on pp. 342-343" speculation maps to. Source:
[downloaded-pdfs/Ramanujan_39_s_Lost_Notebook_Part_IV_2013.pdf](downloaded-pdfs/Ramanujan_39_s_Lost_Notebook_Part_IV_2013.pdf).
Effort: ~half-day if the chapter is well-organised. Should close the
H1a ambiguity in DID_NOT_PAN_OUT §R16.

### H6. Hunt 2 — Modular equations at level ≥23 — NEWLY UNBLOCKED

Berndt *Notebooks Part V* (Ch. X) now available at
[downloaded-pdfs/ramanujan-notebooks-v.pdf](downloaded-pdfs/ramanujan-notebooks-v.pdf).
Ready to run the prediction in [HUNT_MAP §2](insights/HUNT_MAP.md): level-23
entries decompose into two Atkin-Lehner families; level-29 same pattern;
level-47 entries hide higher-genus modular curve. Algorithmic win on
SEA point-counting if confirmed.

### H7. Hunt 3 — Eisenstein-style continued fractions — NEWLY UNBLOCKED

Berndt *Notebooks Part V* Ch. 32 at
[downloaded-pdfs/ramanujan-notebooks-v.pdf](downloaded-pdfs/ramanujan-notebooks-v.pdf);
focused secondary source at
[downloaded-pdfs/1274-16.pdf](downloaded-pdfs/1274-16.pdf) (Berndt-Yee 2002
RIMS survey). Bhatnagar in chatgpt-pro-mining. Ready to run the
~20-Eisenstein-CFs clustering analysis in HUNT_MAP §3.

### H8. Hunt 4 — Unproven class invariants Gₙ — NEWLY UNBLOCKED

AB *Lost Notebook Part I* supplement (pp. 200-220) at
[downloaded-pdfs/Ramanujan_39_s_Lost_Notebook_Part_I_2005.pdf](downloaded-pdfs/Ramanujan_39_s_Lost_Notebook_Part_I_2005.pdf).
Plus Berndt *Notebooks Part V* Ch. 33-34 commentary. **Overlaps with H1b**:
the Weber class invariants on LN p. 342 are likely a subset of the same
list; cross-checking H1b with H8 in one pass is the efficient play.

## Still partially blocked

### B4. Hunt 6 — Ramanujan-Sato at moonshine levels

Have NB II facsimile + open-access context PDFs; missing Cooper *Theta
Functions* (Springer 2017). Worth emailing Shaun Cooper for a personal-use
PDF — see [VALIDATION_CONTACTS.md](insights/VALIDATION_CONTACTS.md).
Workaround: re-derive level-by-level catalogue from Berndt's open-access
papers on theta functions.

---

## Standing items (per BIG_IDEAS_REVIEW)

- **Cohomological generative model** (BIG_IDEAS §3). Research-grade math
  question, not a well-scoped experiment. Entry points in diary 19 §"what next".
- **LLM + symbolic-verification operator search** (BIG_IDEAS §7). Long-running
  research project; W5 above is the smallest first step.
- **Library-design / silent-zero technical note** (BIG_IDEAS §5). The
  silent-zero hazard at Gauss sums q ≡ 2 mod 4 → 1-2 page note for
  Mathematics of Computation. Cheap, citable.

## Sourcing follow-ups (only when needed)

[VALIDATION_CONTACTS.md](insights/VALIDATION_CONTACTS.md) has the directory
of expert contacts (Zagier, Ono, Bringmann, Berndt, Andrews, Cooper) with
"why them for this run" notes. Open asks once we have a result firm enough
to take to a real expert:

- **Berndt 1984 BLMS paper** ("Ramanujan's Quarterly Reports", Bull. London
  Math. Soc. 16, 449-489). Contains Berndt's per-section assessment of
  "really new" vs "rederivation of known results" for the QRs — would let
  us calibrate the Hunt 5 findings against Berndt's editorial judgment.
  Ask Berndt next time we're in touch (he's already provided
  [downloaded-pdfs/](downloaded-pdfs/)).
- **Cooper *Ramanujan's Theta Functions*** (Springer 2017) for Hunt 6 —
  ask Cooper.
- **Berndt *Notebooks Parts III & IV*** (1991, 1994) — lower priority than
  Part V which is now in.

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
