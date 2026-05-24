# Big Ideas Review — What Survived the First Pass + Hunt 5

**Purpose.** The original ChatGPT-Pro / Claude brainstorm seeded ~7 substantive
ideas. This file rates each one against the empirical state of the run as of
diary 20 (Hunt 5 closed). The point is to keep the durable judgment of "which
of these still has legs" in a stable location, not buried in conversation.

**Confidence tags:** high / medium-high / medium / low / dead.
**Status tags:** SHIPPED (operational artefact exists) / SUPPORTED (numerical
evidence in CSVs) / FALSIFIED (decisive negative) / PARTIAL (qualitative right
direction, quantitative wrong) / OPEN (untested) / DEAD (refuted).

Cross-references: [CANDIDATE_INSIGHTS.md](CANDIDATE_INSIGHTS.md),
[DID_NOT_PAN_OUT.md](DID_NOT_PAN_OUT.md), [HUNT_MAP.md](HUNT_MAP.md),
[diary/INDEX.md](../diary/INDEX.md).

---

## 1. The "reciprocal-kernel compiler" framing

**Original claim.** Ramanujan's mathematical style was, mechanically, a
reciprocal-kernel compiler: he took dense sums/products/recurrences and routed
them through theta/modular/Gauss-sum/CF/asymptotic identities that cost orders
of magnitude less to certify.

**Status: SHIPPED + SUPPORTED. Confidence: high.**

- The recognizer is operational: [rkc/](../rkc/) package with 11 registered
  kernels, **50/50 unit tests passing**, **55/55 = 100% on the routing benchmark**.
- Five kernels substantiated end-to-end with rigorous tail certificates and
  degeneracy detectors: Gaussian theta, Bose-Einstein partition, Lambert-Eisenstein,
  π methods, divisor sum. See [CANDIDATE_INSIGHTS A1-A7](CANDIDATE_INSIGHTS.md).
- Quantified gains (numerical, certified, not estimated): Gaussian theta
  Z(β=10⁻⁸) to 100 digits, 151,745 terms → 3 terms (**50,000×**). Bose
  partition Z(β=10⁻³) to 60 digits, 145,064 → 1 (**145,000×**).
- Universal **β* = c·π** crossover pattern across five independent kernels
  ([CANDIDATE_INSIGHTS A6](CANDIDATE_INSIGHTS.md)).
- Per-term-cost vs term-count framing replaces naive "bits-per-term"
  ([CANDIDATE_INSIGHTS A7](CANDIDATE_INSIGHTS.md); falsifies the
  bits-per-term proxy: see [DID_NOT_PAN_OUT R12](DID_NOT_PAN_OUT.md)).
- Honest qualifier holds: gains apply only when kernel structure is
  *recognized*. The recognizer is the binding constraint, not the
  representation switch itself.

**What still has legs:**
- The architecture paper is publishable as-is. "Kernel-fingerprint compiler
  for partition-function-like quantities, with rigorous tail certificates and
  degeneracy detection." Confidence in clean acceptance: medium-high.
- f5/f7 instrumentation for [`rkc/completions.py`](../rkc/completions.py) is
  a clean continuation now that the source pack is local. Requires Hickerson
  1988 / Berndt-Chan transcriptions.
- Watson-identity calibration regime extension (currently calibrated only for
  α ≤ 0.7; (0.7, π) flagged `near-cusp-warning`) is a clean follow-up.

---

## 2. The "Quarterly Reports = operator-basis demo" framing (Hunt 5)

**Original claim.** The QRs reveal the *operators Ramanujan carried in his
head* (Mellin inversion, master-theorem operator, q-shift, modular S, Eisenstein
normal-ordering, class-field Galois average) as first-class primitives.
Specific testable prediction: 5-10 operators recur 80%+ of the time.

**Status: PARTIAL (80% prediction FALSIFIED, underlying hypothesis SUPPORTED
with corrected basis). Confidence: high.**

- Hand-tagged all 33 math-content sections of Berndt's 2022 HRJ reproduction.
  Full verdict in [diary 20](../diary/20_hunt5_qr_operator_tagging.md).
- 80% prediction falsified at **57.6% coverage**. QR I confirms (13/13 = 100%);
  QR II partial (6/9 = 67%); QR III complete failure (0/11 = 0%).
- **4 of 6 predicted operators never fire** (q_shift, modular_S_transform,
  eisenstein_normal_ordering, class_field_galois_average). Zero occurrences
  of `\tau`, `\theta`, `\eta`, "Eisenstein", "Heegner", "class invariant"
  in 5519 lines.
- The QRs are **not a modular-forms document**. They are Mellin/Master-Theorem
  analysis (QR I + II) and **functional-iteration / Hardy-orders / operator
  calculus (QR III)** — a totally different mathematical universe from what
  HUNT_MAP §5 predicted.
- A revised 7-operator basis (drop the 4 unfired ops, add Fourier-self-
  reciprocity / Frullani-limit / fractional-iteration / Hardy-orders /
  Mellin-pair) covers **~91%** (30/33).

**What still has legs:**
- **Hunt 5b on the Notebooks** is the natural next test. The Notebooks (Berndt's
  five-volume edition) are where modular machinery should actually appear per
  Berndt's TOC. If Notebooks confirm a *different but still small* toolkit,
  the **QR-vs-Notebooks toolkit contrast** becomes the real cog-sci finding:
  Ramanujan deployed at least two toolkits in different contexts.
- The "QR III is about fractional iteration" finding is genuinely novel —
  it is not in any standard "Ramanujan in modular forms" or "Ramanujan and
  analysis" treatment I recall. The Schröder/Koenig functional-equation
  connection (QR III §10's `ψ_1(x) = C/F(x)` = infinitesimal generator of
  iteration flow) deserves a literature scan in its own right.
- The operator basis is now empirically grounded; the
  [operator_tagging_schema.py](../corpora/transcriptions/operator_tagging_schema.py)
  should be expanded with the 5 added operators and re-checked against the
  Notebooks transcriptions when they arrive.

---

## 3. The "mock-theta corrections as fitted-EBM bias diagnostics" big swing

**Original claim.** Bridge between Friston FEP and post-Zwegers mock modular
forms: if a generative model's Z is genuinely mock, fitting a "purely modular"
surrogate introduces a systematic bias whose shape is the **shadow** of the
mock theta. Speculative paper at ~15-25% confidence per the original brainstorm.

**Status: CLOSED (forward = identity; reverse FALSIFIED for 20 candidates;
cohomological irreducibility conjecture ESTABLISHED). Confidence: high.**

This was the run's biggest investment after the recognizer. Six experiments
(Exp 13, 16, 18, 20, 21, 22) across five structurally-different candidate
families. See diary 13, 15, 17, 18, 19 and [CANDIDATE_INSIGHTS §B/C](CANDIDATE_INSIGHTS.md).

- **Forward direction** is an *identity* (lattice gas → f(q) to 25-50 digits).
  This is operationally cleaner than expected — the generative model with the
  right partition function literally IS Ramanujan's mock theta.
- **Reverse direction falsified**: ~20 candidate shadow-functionals across
  marginal divergences (Exp 16), bounded-at-cusp divergences (Exp 18),
  Wigner-negativity-aware divergences (Exp 20), path-measure functionals
  (Exp 21), transfer-matrix eigenstructure (Exp 22). **No structurally-
  different candidate family remains untried.**
- **Two decisive structural arguments** anchor the closure:
  1. Exp 21: cooling-path direction-of-traversal on the imaginary axis is the
     *opposite* of the Eichler integral's natural direction (disjoint half-lines).
  2. Exp 22: the (K+1)² dimension mismatch under the modular S-transform means
     no finite-K intertwiner can exist; the K → ∞ defect reduces to Watson's
     1936 partner-function identity (tautological).
- **The cohomological-irreducibility conjecture** — g* is intrinsically an
  Eichler cocycle in H¹(Γ, V_k), not a functional of lattice-gas configuration
  statistics — is **established at medium-high → high confidence** (diary 19).

**What still has legs:**
- The closure itself is publishable: "We tested ~20 functionals of an
  EBM-style generative model against the Watson-Hickerson Eichler integral,
  found none match, and the structural reason is cohomological." Target:
  Comm. Math. Phys. or Physical Review Research. **The honest "we tried hard
  and it doesn't reduce" is itself the result.**
- The cohomological generative model — building a model that *has*
  H¹(Γ, V_k) cocycle structure as a primitive — is a research-grade math
  question. Not a well-scoped experiment; see diary 19 §"what next" for
  entry points.
- The 15-25% bet from the brainstorm should be downgraded to ~5% for the
  "naive functional bias" framing and upgraded to ~30-40% for the
  "cohomological generative model" framing (which is harder but the
  failure modes are now mapped).

---

## 4. The "latent-space speedrun" philosophical core

**Original claim.** Ramanujan's intuition was fast because he carried novel
compressed representations in his head — operating on entire generating
functions / modular objects as primitive tokens. The most generative framing.

**Status: SUPPORTED with caveat on QRs; OPEN on Notebooks. Confidence:
medium-high.**

- Hunt 5 supported the underlying small-toolkit hypothesis: ~7 operators
  cover 91% of QR math sections. Just not the predicted set.
- The contrast across the three QRs is informative: QR I uses essentially 2
  operators, QR II uses ~4, QR III uses ~6-7. Even within a single document
  Ramanujan's *active toolkit* is small but not trivial.
- The cog-sci angle holds: this is "expert chunking" in Ericsson's sense,
  where the chunks are abstract operators rather than chess positions or
  programming patterns. Ramanujan is the extreme case but the framing
  generalises.

**What still has legs:**
- Hunt 5b (Notebooks): if it confirms a *different but still small* toolkit
  per topic-domain, the result generalises into a paper on
  "operator-vocabulary specialisation in mathematical expertise". This is
  publishable in philosophy-of-math or cognitive-science-of-expertise venues
  in addition to math journals.
- The frontier-AI angle from the brainstorm ("build a search engine over
  Ramanujan's operator basis using LLM + symbolic verification") is still
  open and now has a *seed basis* to search over. RamanujanMachine is the
  CF special case; an operator-extended version is genuinely interesting.

---

## 5. The degeneracy-detector pattern

**Original claim.** Every kernel that's exploitable in one regime fails
silently in another (Gauss sums at q≡2 mod 4; modular forms at high-level
cusps; AGM at certain initial conditions). Making failure-mode catalogues
a first-class part of computational-math tooling is broadly missing.

**Status: SHIPPED. Confidence: high.**

- Implemented in [rkc/registry.py](../rkc/registry.py) as a first-class part
  of every kernel registration.
- The silent-zero hazard at Gauss sums q ≡ 2 mod 4 is the headline catch
  ([CANDIDATE_INSIGHTS A4](CANDIDATE_INSIGHTS.md)).
- Multiple silent-failure cases caught: v0 mock-theta character parity (T7
  introspection check), bits-per-term over-credit (Lambert vs partition cells),
  cross-validation gap that would have shipped silently
  ([DID_NOT_PAN_OUT.md R1, R2, R12](DID_NOT_PAN_OUT.md)).

**What still has legs:**
- This is the **strongest broad-application claim** in the run. It generalises
  well beyond Ramanujan — any computational-math library has silent-failure
  classes that are not documented as such.
- The "silent-zero" short technical note (the brainstorm's confidence: high)
  is publishable as-is. Target: Mathematics of Computation notes section or
  Designs, Codes and Cryptography. Very narrow, very citable.
- A meta-paper on "failure-mode catalogues as first-class library features"
  with rkc/registry.py as the case study is a possibility for CSE / TOMS.

---

## 6. Gemini's "highly-composite tensor schedules"

**Original claim.** Tensor-decomposition schedules using highly-composite
integers would be Ramanujan-flavored speedups for ML.

**Status: DEAD. Confidence in deadness: high.**

- [DID_NOT_PAN_OUT.md §R4](DID_NOT_PAN_OUT.md). Smoothness ≠ high
  compositeness; FFTW/cuFFT/MKL already do this for decades; the framing
  conflated two different combinatorial extrema.
- Drop from any future planning.

---

## 7. "Build a search engine over Ramanujan's operator basis using LLM + symbolic verification"

**Original claim.** Frontier-AI bet: the gap between Ramanujan-1914 working
memory and Lean-2026 / AlphaProof reasoning is interesting and arguably
converging. Build a search over Ramanujan's basis.

**Status: OPEN. Conceptually validated by Hunt 5; technically untouched.
Confidence: medium.**

- RamanujanMachine (vendored at [corpora/RamanujanMachine/](../corpora/RamanujanMachine/)
  and v0 at [corpora/RamanujanMachine_v0/](../corpora/RamanujanMachine_v0/))
  is the CF-special-case proof-of-concept; it works and continues to find
  new identities.
- After Hunt 5 we now have a **seed basis** (the revised 7 QR operators +
  whatever Notebooks adds in Hunt 5b) and a **recognizer** that can score
  candidate identities against the basis. The pieces exist.
- The build would be: (i) generate candidate identities by composing
  operators on simple inputs; (ii) numerically verify via mpmath/PSLQ;
  (iii) classify via the recognizer; (iv) PSLQ-search for closed forms of
  newly-discovered constants. Pyo Stage.
- Risk: the operator basis from QRs is on the analysis / Master-Theorem
  side; truly modular-form-style identity discovery (which is what
  RamanujanMachine has not yet covered systematically) waits on Hunt 5b
  on the Notebooks.

**What still has legs:**
- This is a multi-quarter research project, not a 6-week sprint. Worth
  scoping as a follow-on if Hunt 5b confirms the Notebooks have a
  modular-form-flavoured operator basis distinct from the QRs'.
- Lower-risk first cut: build a small operator-composition search using
  the *7 QR operators*, generate ~100 candidate identities, run them
  through the recognizer + numerical verification, see how many are
  classical-known vs. genuinely new. Even 1-2 new identities would
  validate the approach.

---

## Summary table

| # | Idea | Status | Confidence | Has legs? |
|---|---|---|---|---|
| 1 | Reciprocal-kernel compiler | SHIPPED + SUPPORTED | high | yes — architecture paper, f5/f7 instrumentation |
| 2 | QR = operator-basis demo (Hunt 5) | PARTIAL (revised basis covers 91%) | high | yes — Hunt 5b on Notebooks |
| 3 | Mock-theta as fitted-EBM bias | CLOSED (cohomological irreducibility) | high | yes — closure paper at PRR or CMP |
| 4 | Latent-space speedrun (philosophical) | SUPPORTED | medium-high | yes — cog-sci paper after Hunt 5b |
| 5 | Degeneracy-detector pattern | SHIPPED | high | yes — silent-zero note + library-design paper |
| 6 | Gemini's highly-composite tensors | DEAD | high (in deadness) | no |
| 7 | LLM + symbolic-verification operator search | OPEN | medium | yes — small first cut feasible now |

---

## Source-pack status (verified by inventory agent, 2026-05-24)

| Hunt | Status | Notes |
|---|---|---|
| 1 | **UNBLOCKED** | LN pp. 341-343 JPGs + Ono-Trebat-Leder K3 paper both in pack |
| 2 | PARTIAL | Have NB facsimiles; missing Berndt Part III-V commentary |
| 3 | PARTIAL | Have Bhatnagar q-CF arxiv + facsimiles; missing Berndt Part V ch. 32 |
| 4 | PARTIAL | Have LN facsimile; missing Andrews-Berndt vol I supplement |
| 5 | CLOSED | diary 20; Berndt 2022 HRJ reproduction used |
| **5b** | **UNBLOCKED** | All 4 notebook facsimiles + 1,149 page images in pack |
| 6 | PARTIAL | Have NB II facsimile + papers; missing Cooper *Theta Functions* |

The copyrighted Berndt commentary volumes (Notebooks Parts III-V, Lost
Notebook Part IV, Cooper *Theta Functions*) are the gap. The facsimiles
themselves are all present.

## What I'd actually do next, ranked

This is my own ranking, not a directive — redirect freely.

1. **Hunt 1 on Lost Notebook pp. 341-343 (UNBLOCKED).**
   3 facsimile pages + an 8-page Ono-Trebat-Leder paper. Tractable in one
   focused session. Tests the 60-80% K3-parameterisation prediction. Smallest
   well-scoped hunt; highest leverage-per-effort.
2. **Hunt 5b on the Notebooks (UNBLOCKED, but big).**
   1,149 facsimile pages — should be scoped to ~3-5 chapters targeted at
   the 4 operators that didn't fire in the QRs (NB II ch. 16 → q_shift,
   ch. 17 → modular_S, ch. 21 → Eisenstein + class-field). Bottlenecked by
   OCR of handwritten facsimiles; benchmark Chandra first.
3. **Write the recognizer architecture paper** ("Kernel-fingerprint compiler
   …"). Draft from existing artefacts (rkc/, A1-A7, DID_NOT_PAN_OUT entries).
   1-2 weeks of focused writing.
4. **f5/f7 Watson-Hickerson instrumentation** for the recognizer (uses
   Hickerson 1988 / Berndt-Chan; if these are in the pack the work is
   bounded). Cleanly closes the recognizer end-to-end on all three
   registered mock-theta families.
5. **Small operator-composition search prototype** using the 7 QR operators.
   Generate 100 candidate identities, score against the recognizer,
   PSLQ-verify constants. Cheap and gives data for whether scaling to a
   larger search is worth the engineering.
6. **Set up Chandra OCR on a Lost Notebook page** and benchmark it against
   handwriting-OCR baselines. Per user note, Chandra was tested specifically
   on Ramanujan's letters to Hardy. If it works well on the LN pp. 341-343
   facsimiles, the rest of the LN becomes accessible cheaply.
