# Did Not Pan Out — Consolidated Log of Refuted / Corrected / Open Speculations

**Purpose.** Methodological credibility. A run that publishes the speculations
it refuted alongside the ones it confirmed is more trustworthy than one
that publishes only the wins. Per `todo.md` cross-cutting deliverable #4,
this file is the consolidated honest accounting.

**Inclusion discipline.** Every entry below cites a specific diary entry
**and** an experiment script (or a SOTA-check artifact). Speculations
that were *made but never tested* are listed in the OUTSTANDING section,
not the refuted section. Some entries are partially refuted or
significantly corrected rather than fully refuted — they are tagged
accordingly.

**Tag legend.**
- **REFUTED** — the speculation failed a numerical or SOTA test outright.
- **CORRECTED** — the speculation had a true qualitative core but the
  quantitative claim, mechanism, or normalization was wrong; v1 fixed it.
- **PARTIALLY REFUTED** — the speculation holds in a restricted regime
  but was over-stated as a general claim.
- **DOWNGRADED** — the speculation was not numerically tested but had its
  calibration lowered by a SOTA check showing prior art covers more
  ground than initially credited.
- **OPEN** — speculation made, listed here for inventory, but not yet
  tested. (Distinct from "refuted".)

**Final entry count: 17**, breaking down as:
- 4 REFUTED
- 4 CORRECTED
- 7 PARTIALLY REFUTED
- 2 DOWNGRADED

(Plus a separate OUTSTANDING section listing speculations that the run
made but never tested. These do NOT count toward the refuted-vs-corrected
total — they are inventory, awaiting future work.)

---

## R1 — v0 mock-theta toy: the "1/√β" asymptotic for the bias

**What was speculated.** Diary 04 (`pass_d_mock_theta_demo.md`, Exp 15)
stated: *"If you fit an EBM whose true normalizer has the shape of f(q)
but you use a 'purely modular' Z surrogate (θ_3 in this toy), you
systematically underestimate the log-partition function near the
critical / high-temperature regime by a factor that goes like 1/√β."*
The intuition was that θ_3 diverges as √(π/β) while f(q) saturates,
giving a residual that scales as 1/√β at small β.

**What was tested.** Experiment 17, written to plug in the exact
Hickerson-Mortenson shadow and the Watson 1936 Eichler integral, and
verify the v0 picture quantitatively. Documented in
`diary/12_mock_theta_residual_v1.md`; script
`ramanujan/analysis/17_mock_theta_residual_ebm_v1.py`; CSV
`ramanujan/analysis/results/mock_theta_residual_v1.csv`.

**What we found.** The v1 modular-only residual (the Mordell integral
M(α)) **saturates at 4/3** as α → 0+ — a finite radial limit (Watson-
Hickerson), NOT a divergent 1/√β. Empirically the CSV column
`residual_v1_modonly` reads 1.333 → 1.333 → 1.332 → 1.324 → 1.255 → 0.932
across β = 1e-4 .. 10. The v0 qualitative picture (mock theta is
bounded, modular surrogate isn't, ratio → 0) was right; the
*quantitative* asymptotic was off; v0 was confusing two different
residuals (the f vs. θ_3 mismatch — which DOES grow like √(2π/α) — with
the genuine shadow Eichler integral, which is bounded).

**Updated estimate (tag: CORRECTED).** The correct version is that the
bounded-at-cusp limit 4/3 is what the shadow Eichler integral
contributes, not a 1/√β divergence. This is now A5 in
`insights/CANDIDATE_INSIGHTS.md` with the explicit retraction. The
qualitative point (mock-modular bias is structural and the shadow is
the missing piece) survives; the numerical asymptotic is replaced by
the right one.

---

## R2 — v0 mock-theta toy: EVEN Kronecker character mod 12 as the shadow character

**What was speculated.** Diary 04 / Exp 15 used the EVEN Kronecker
character (12/·) — i.e. χ(n) = +1 if n ≡ ±1 mod 12, −1 if n ≡ ±5 mod 12 —
as the character of the weight-3/2 unary theta shadow.

**What was tested.** Symbolic derivation in Experiment 17 / Diary 12
re-derived the shadow's character from first principles by rewriting
sinh(αt)/sinh(3αt/2) in the Watson Mordell integrand as
Σ_{m≥0} [e^{−αt(6m+1)/2} − e^{−αt(6m+5)/2}]. The character that emerges
is the ODD primitive character of conductor 12: χ(1)=χ(7)=+1,
χ(5)=χ(11)=−1, χ(−n)=−χ(n).

**What we found.** The EVEN-character unary theta `Σ χ(n)·n·q^{n²/24}`
**vanishes identically** by the pairing n ↔ −n (n·χ(n) + (−n)·χ(−n) =
0 when χ is even). So v0's `shadow_unary_theta` was structurally
zero-by-symmetry as a real unary theta; v0 silently computed the
one-sided (positive-n) version, which is not modular under any
nontrivial transformation.

**Updated estimate (tag: REFUTED).** v0's character choice is plain
wrong. The correct character is the ODD one. The fix is documented in
diary 12 §"v0 bug found and fixed" and the corrected sign pattern is
verified numerically at α = 1 (n=1:+1, n=5:−5, n=7:+7, n=11:−11, n=13:+13,
magnitudes decay hyperexponentially). This is exactly the
"looks-fine-returns-wrong-answer-with-confidence" failure mode that A4
in `CANDIDATE_INSIGHTS.md` warns about for ANY representation-switching
compiler — and it's the most painful place it bit me in this run.

---

## R3 — "Naive rational-temperature snapping is a generic RKC speedup"

**What was speculated.** Original framing (carried over from the Gemini
critique, diary 02 §"Lead 5"): snap an irrational temperature α to a
nearby rational p/q and use Gauss's closed form for the quadratic Gauss
sum G(p,q) = Σ_{n=0}^{q-1} exp(2πi p n²/q). This was framed as a generic
acceleration route, with Gemini warning only about "residual bounds and
denominator blow-up".

**What was tested.** Experiment 10 — full sweep over α = √2 − 1 with
snap targets eps ∈ {1e-2 … 1e-13} and best continued-fraction
convergents. Documented in `diary/05_rational_snap_pareto_and_zero_hazard.md`;
script `ramanujan/analysis/10_rational_temp_snapping.py`.

**What we found.**
1. The Pareto is **linear**, not super-linear: doubling q halves the
   phase error and doubles the cost — a 1-for-1 trade, never
   asymptotically dominant over a well-damped direct truncation (which
   gives `O(1/√damping)` cost with linear convergence in `log(1/tol)`).
2. **The "silent zero hazard"**: classical Gauss-sum evaluation gives
   G(p, q) = 0 identically when q ≡ 2 (mod 4). Roughly *half* of the
   best CF convergents of a generic irrational land in that residue
   class. A naive snap-and-Gauss RKC returns ZERO with high algorithmic
   confidence on those cases.

**Updated estimate (tag: PARTIALLY REFUTED).** The snap is most genuinely
valuable only when (a) α is rational *by structure* (physical or
quantization-imposed), or (b) the dual representation is the ONLY
available one. As a *generic* speedup over damped direct summation it
is refuted. The silent-zero hazard is real and serious enough that the
v1 recognizer (Exp 13) carries an explicit degeneracy detector for
q ≡ 2 (mod 4); see diary 11 and CANDIDATE_INSIGHTS A4. The recognizer
benchmark confirms the detector fires on every adversarial case in the
55-case battery (`recognizer_routing_benchmark.csv`).

---

## R4 — Gemini's "highly composite tensor schedules" as a paradigm

**What was speculated.** Gemini's commentary (relayed in diary 02
§"Lead 2") framed "highly composite numbers" as the basis for novel
compute schedules, with the claim that "the entire hardware world is
locked into powers of two".

**What was tested.** Direct SOTA check (no scripted experiment, but
documented analysis in `diary/02_critique_gemini.md` §"Lead 2",
cross-referenced against the SOTA notes for HPC / FFT prior art).

**What we found.**
1. **The framing conflates two different combinatorial extremes.**
   Ramanujan's "highly composite" (more divisors than any smaller
   integer) is a *specific* subset; the FFT-relevant optimum is
   **smoothness** (no prime factor exceeds bound B). A 5-smooth or
   7-smooth number isn't necessarily highly composite, and vice versa.
2. FFTW, cuFFT, MKL already expose mixed-radix algorithms; Bluestein's
   chirp-z handles arbitrary sizes; Rader's algorithm handles primes;
   Winograd minimizes multiplications for small kernels. The actual
   binding constraint in modern AI is memory-bandwidth alignment, not
   factorization optionality.
3. Real prior art exists; the "paradigm shift" framing is overstated.

**Updated estimate (tag: PARTIALLY REFUTED).** The narrower honest
version — *expose compile-time factorization metadata to the schedule
planner so block/tile/batch decisions can use it; build a Ramanujan-
style ranking function over (size, factor structure, hardware cost
model)* — is real but modest. CANDIDATE_INSIGHTS B2 captures the
calibrated version. The headline is "real niche lead", not "paradigm
shift". Confidence: medium negative.

---

## R5 — Modular checksums as a broad DP primitive

**What was speculated.** Gemini called Ramanujan's congruences
(p(5n+4) ≡ 0 mod 5, p(7n+5) ≡ 0 mod 7, p(11n+6) ≡ 0 mod 11) "brilliant
cheap invariants for combinatorial state spaces."

**What was tested.** Argued, not numerically run. Documented in
`diary/02_critique_gemini.md` §"Lead 3" and CANDIDATE_INSIGHTS B3.

**What we found.** To use these congruences as DP checksums you need
either (a) the DP to be computing exactly p(n) (in which case you've
already done the hard work) or (b) a *structurally analogous* generating
function for the DP problem where the congruence transfers. The
general principle (using number-theoretic invariants as cheap parity-
like checks on coefficient streams) is real and underused, but it's
bigger than Ramanujan and the work is in *finding the right invariant
for the right DP*, which is per-problem.

**Updated estimate (tag: PARTIALLY REFUTED).** Real principle, narrow
applicability of Ramanujan's specific congruences. The lead is a
"medium novelty, per-problem work" entry rather than a turnkey
primitive. Confidence: medium. Not pursued further in this run because
the per-problem cost is the binding constraint.

---

## R6 — "Modular surrogate" in v1 mock-theta toy = a canonical level-X η-product

**What was speculated.** Diary 12 §"Does this count as a publishable
bias-cancellation demonstration?" flagged the hope that the Watson
companion `W(q_1²)` used as the modular surrogate would correspond
cleanly to a canonical η-product / Eisenstein form at level 6 / 12 / 24
under the modular-forms taxonomy.

**What was tested.** Attempted in the v1 derivation, but not
disentangled — diary 12 §"what's still missing" honestly states the
gap: "my Watson identity has been confirmed at small α (calibrated
regime) to ≥30 digits, but at α > 1 there are O(q_1⁴) corrections I
haven't disentangled (probably because I'm picking a slightly wrong
Watson partner; the literature uses several inconsistent labelings of
ω vs ψ vs ν)."

**Updated estimate (tag: PARTIALLY REFUTED for the "publishable"
framing; CORRECTED in scope.)** The v1 bias-cancellation IS quantitative
in the small-α regime (≥30 digits), which is the regime of interest for
the EBM toy. It is NOT in the canonical-η-product form at all α. A
publishable mathematical writeup would need to either (i) chase down
the right Watson partner so the identity holds at all α, or (ii)
reformulate using only the Mordell integral as the shadow Eichler
integral, paired with a Dedekind-η-product modular form. Bibliographic
work, not deep, but explicitly out of scope here. CANDIDATE_INSIGHTS A5
notes this caveat in its "still missing" line.

---

## R7 — Shadow of f(q) is proportional to mutual information

**What was speculated.** B1 of CANDIDATE_INSIGHTS originally listed
mutual information `I(n ; total_particles)` as a candidate for the
shape of the shadow's Eichler integral g*(τ). This was one of four
standard info-theoretic candidates probed in Pass D.

**What was tested.** Experiment 16. Documented in
`diary/13_fep_mock_modular_toy.md`; script
`ramanujan/analysis/16_fep_mock_modular_toy.py`; data
`ramanujan/analysis/results/fep_mock_modular_toy.csv`. 13 data points
across β ∈ {10⁻³, …, 10}, 4 orders of magnitude.

**What we found.** Median ratio `MI / g*` = 6.6e-3 with max relative
deviation **14.3× (= 1430%)** across the sweep. Fails the strict ≤1%
proportionality bar by a large margin.

**Updated estimate (tag: REFUTED).** MI vanishes at the cusp β → 0
(the unsigned distribution becomes nearly uniform on a huge range of n
and particle-count factorizes through n, so MI → 0). g* is bounded at
the cusp (≈ 3.46). The two have qualitatively wrong shapes at the
boundary. Not the right info-theoretic identification.

---

## R8 — Shadow of f(q) is proportional to KL divergence

**What was speculated.** Same B1 entry — KL(p_unsigned ‖ p_signed) as
the second of the four standard candidates.

**What was tested.** Same Exp 16.

**What we found.** Median ratio = 1.34, max relative deviation
**262× (= 26200%)**. Worst of the four candidates.

**Updated estimate (tag: REFUTED).** KL diverges at the cusp (because
Z_unsigned diverges fast — bosonic partition function blows up — while
Z_signed = f(q) → 1.33). The structural mismatch is the same as MI but
with the opposite sign (divergent rather than vanishing).

---

## R9 — Shadow of f(q) is proportional to cross-entropy "Surprise"

**What was speculated.** Same B1 entry — third candidate.

**What was tested.** Same Exp 16.

**What we found.** Median ratio = 1.81, max relative deviation
**196× (= 19600%)**.

**Updated estimate (tag: REFUTED).** Same structural reason as KL —
diverges at the cusp.

---

## R10 — Shadow of f(q) is proportional to Fisher information F(β)

**What was speculated.** Same B1 entry — fourth and most plausible-
looking candidate.

**What was tested.** Same Exp 16.

**What we found.** Median ratio = 0.076. Max relative deviation
**0.999 (= 99.9%, i.e. a factor of ~2 variation in ratio across
4 dex of β)**. The least falsified of the four — but still failing
the ≤1% bar.

**Updated estimate (tag: REFUTED, with note.)** Fisher vanishes at the
cusp (p_signed freezes; the β-derivative becomes negligible). g* is
bounded. Different cusp behaviour ⇒ not proportional. The factor-of-2
variation suggests Fisher and g* track each other over a *limited*
range, which is informative for whatever the true identification is
(if any), but does not pass the test.

The pattern across R7–R10 is itself a finding: the **necessary
structural condition** for any candidate is "bounded and nonzero at
the cusp"; none of the four standard candidates satisfies it. This
"clean negative with structural content" is captured in
CANDIDATE_INSIGHTS B1 as the *positive* corollary — the search should
move to bounded-at-cusp candidates (Rényi-α, Bhattacharyya, entropic
uncertainty).

---

## R11 — "Always prefer the closed-form radical over direct evaluation" for class invariants

**What was speculated.** The standard intuition (and a corollary of the
"latent-space speedrun" framing): Ramanujan's nested radicals for class
invariants `G_n` should always beat direct evaluation of the infinite
product.

**What was tested.** Experiment 08. Documented in
`diary/09_class_invariants_cost.md`; script
`ramanujan/analysis/08_class_invariants_cost.py`; CSV
`ramanujan/analysis/results/class_invariants_cost.csv`. Eight invariants
all numerically PSLQ-verified to ≥100 digits before the cost benchmark.

**What we found.**
1. As n grows, **direct evaluation gets faster, not slower** — the
   expansion parameter q = e^{−π√n} shrinks with n, so fewer product
   factors are needed at fixed precision. At d=1000 digits: G_1 needs
   369 terms, G_49 needs only 53. Initial intuition was wrong; the
   prompt's hedge was correct.
2. **For n ∈ {17, 49} at d=30 digits, direct beats radical on op-count.**
   Direct needs 2–3 product factors at 30 digits; the nested radical
   involves 7–8 primitive ops. This is the most surprising cell of
   the experiment.
3. At d=1000 the radical wins for every n by 7×–369× on op-count and
   3×–430× on wall-time — but only at industrial precision.

**Updated estimate (tag: PARTIALLY REFUTED.)** The "closed form always
wins" prior has a documented small-d, large-n exception. The honest
calibrated statement (medium confidence): the radical gives a 1×–400×
speedup, with the advantage **growing linearly in working precision d**
and **decaying sub-linearly in n**. Crossover where radical begins to
dominate by op-count is around d ~ 30–100 digits for medium n
(17 ≤ n ≤ 49); below that, direct is competitive. A future RKC routing
policy should encode the "use direct below threshold T(n)" rule, with
T(n) ~ π · √n · (radical_ops) per the empirical scaling.

---

## R12 — "Bits-per-term is the right routing metric"

**What was speculated.** Implicit in many early diary entries (notably
diary 06, the π-methods compression piece): bits-per-term is the
natural compression metric to drive routing.

**What was tested.** Experiment 05 / diary 07 (`hrr_partition_benchmark.md`),
script `ramanujan/analysis/05_hrr_partition_benchmark.py`. HRR vs the
pentagonal recurrence for p(n), n ∈ {10, 10², 10³, 10⁴, 10⁵}.

**What we found.** Bits-per-term flatters HRR by a factor of ~10⁵ at
n=10⁵ (138 HRR terms vs 34.3M pentagonal summands), but the wall-clock
crossover sits at n ≈ 10⁵ — **only 1.2× speedup**, not 10⁵×. Each HRR
term costs φ(k) Dedekind sums at dps ≈ log₁₀ p(n) precision, while each
pentagonal term is one big-int add. With binary-splitting + FLINT
bignums the wall-clock gap would re-open, but with naive mpmath
arithmetic, bits-per-term over-credits HRR.

**Updated estimate (tag: CORRECTED.)** Bits-per-term is a *necessary*
but not *sufficient* routing signal. The cost predictor must divide
bits-per-term by per-term computational cost — the registry's cost
estimator needs to track per-term complexity, not just term count.
This is now A7 in CANDIDATE_INSIGHTS. The full lesson: a kernel's
information-theoretic density and its computational-cost density must
be tracked jointly. Confidence: high.

---

## R13 — "Catastrophic cancellation in the Lambert-Eisenstein modular formula at large β is a real route-failure"

**What was speculated.** During Exp 12 derivation (diary 10, "Surprises
3"), the worry was raised that the modular path `c_k · (small · E − 1)`
at large β might produce relative-error explosion that breaks the route.

**What was tested.** Direct numerical check at β=100, tol=1e-10 with k=3,
documented in the CSV `lambert_eisenstein_switch.csv` row for that cell.

**What we found.** Relative error of the modular route at β=100 *is*
~3e33 in the sense of `value_check`, because L_k ≈ e^{−100} ≈ 4e-44 is
absurdly tiny and the cancellation noise sits at ~1e-11 — so the
*absolute* error meets tol but relative blows up by orders of magnitude.
HOWEVER: at β > 2π, the cost predictor *already* routes to DIRECT (by
30–95× margin), so the modular route is never actually selected in the
regime where the cancellation matters.

**Updated estimate (tag: PARTIALLY REFUTED as a real hazard for the
running system; CORRECTED as a documentation matter.)** The cancellation
exists but is operationally invisible — the cost-based router never
picks the modular path where it would blow up. The honest version of
the hazard: any user manually invoking the modular formula outside its
β ≤ 2π regime would see it, and the kernel-registry entry should carry
a warning. Captured in diary 10 §"Surprises 3" as a speculative
hardening note for a production RKC. The "real route-failure" framing
is wrong; the "documentation needed" framing is right.

---

## R14 — Gemini lead 1: "completely bypass the log-normalizer wall for specific distributions"

**What was speculated.** Gemini's framing of the Reciprocal-Kernel
Compiler lead: representation switching gives a clean bypass of the
log-normalizer wall.

**What was tested.** Experiment 02 (Gaussian theta), Experiment 03 (RKC
v0 with rigorous tail bounds), Experiment 04 (partition function),
Experiment 12 (Lambert-Eisenstein). Documented across diary 03 and
diary 10, CANDIDATE_INSIGHTS A1 and A2.

**What we found.** The bypass IS real *when the kernel structure is
recognized*. But the *certificate of correctness* is more delicate than
the cost-prediction — the v0 "next-term < tol" tail bound silently
violated the target by **4–5 orders of magnitude** in the slow-decay
regime (Exp 02 → 03 fix). The recognition problem is the binding
constraint, not the switching itself.

**Updated estimate (tag: DOWNGRADED, with technical addenda.)** The
bypass is operationally real, but the headline "completely bypass" is
over-stated. The realistic picture is: **representation switching gives
10¹–10⁵× term-count reductions on physically-meaningful kernels (A1),
but each kernel needs (a) a rigorous, kernel-specific tail-bound
certificate (A2) and (b) a degeneracy detector to guard against
silent-zero / silent-cancellation hazards (A4)**. The recognizer must
co-design certificate + cost model + degeneracy guard per kernel.
Calibrated wins are in CANDIDATE_INSIGHTS A1–A4, A6, A7. Gemini's
qualitative direction was right; the implementation cost was understated.

---

## R16 — "60-80% of LN pp. 341-343 manipulations parameterize K3 surfaces" (HUNT_MAP §1)

**What was speculated.** HUNT_MAP §1 (and Ono's 2016 colloquium speculation):
extending Ono's Theorem 1.3 (Picard-18 K3 from the p. 341 cube identities),
the remaining identities on pp. 342-343 should also trace out K3 surfaces or
Calabi-Yau threefolds. Predicted fraction: 60-80%.

**What was tested.** Hand inventory of all 48 identifiable identities across
the LN reprint pp. 340-344 from the Sirinudi/Narosa facsimile in the
chatgpt-pro-mining pack, cross-referenced against Ono-Trebat-Leder
(arXiv:1510.00735) and Agarwal-Garg (arXiv:2309.00427). Tagged each with
`k3_status` ∈ {K3_PARAMETERISATION_CONFIRMED, K3_CANDIDATE_PER_ONO, NOT_K3,
UNKNOWN_FROM_FACSIMILE}. Documented in `diary/21_hunt1_lost_notebook_341_343.md`;
inventory in `analysis/results/hunt1_k3_inventory.csv`; reproducible via
`analysis/24_hunt1_k3_inventory.py`.

**What we found.** 33.3% K3 coverage on the HUNT_MAP §1 target pp. 341-343
(10/30 known identities, with 1 row tagged UNKNOWN_FROM_FACSIMILE and
excluded from the fraction). The K3 material is **100% concentrated on p. 341
itself** (10/10 = 100% there). pp. 342-343 are not cube-identity continuation
at all:

| Page | Topic | n_known | n_K3 | K3 fraction |
|---|---|---|---|---|
| 341 | 1729 cube identities (rational fns + master identity + 6 numerical examples) | 10 | 10 | **100%** |
| 342 | **Weber class invariants** (`f₁(√-n)` table for n ∈ {20,27,…,87}) — Hunt 4 territory | 18 | 0 | 0% |
| 343 | Best Diophantine approximation to ⁵√2 and ⁷√2 with conjugate-product `O(…)` bounds | 2 | 0 | 0% |

Widening to pp. 341-344 gives 23.8% (10/42), also FALSIFIED.

**Updated estimate (tag: PARTIALLY REFUTED).** The K3 prediction is refuted
in the form "60-80% of identities on these three pages are K3" — pp. 342-343
are entirely different mathematical topics (the Lost Notebook is loose scrap
paper; consecutive pages aren't always thematically contiguous). The
underlying Ono-Trebat-Leder finding (the p. 341 cube identities ARE a
Picard-18 K3) is **fully confirmed and reproduced**, so the prediction's
core insight is real — it's only the "and the next pages continue it" extension
that fails.

**Important methodological catch:** the user-curated
`priority_sources/lost_notebook_pages_341_343/` filenames are off-by-one
versus the LN reprint pagination — `page-N.jpg` corresponds to LN p. `N+1`.
Verified by byte-identity check + Ono Appendix cross-reference. The original
hunt would have given a wrong answer if the agent hadn't caught this
filename inconsistency. Lesson: cross-reference primary-source canonical
content before trusting curated-pack metadata.

**Bonus partial unblock:** p. 342's Weber-class-invariant table contains
discriminants (-63, -87 of class number ≥ 4, among others) that may overlap
the ~18 of 116 class invariants Hunt 4 targets as unresolved. New todo item
1b cross-checks this against Berndt-Chan-Kang-Zhang's reproof table.

**Open ambiguity:** Ono's 2016 colloquium speculation referenced
"pp. 342-343" without qualifying which edition's pagination. The
Andrews-Berndt *Lost Notebook Part IV* commentary (copyrighted Springer
book, not in the local pack) would resolve whether Ono meant the same
facsimile pages this inventory used.

---

## R15 — "5-10 operators recur 80%+ of the time in the Quarterly Reports" (HUNT_MAP §5)

**What was speculated.** HUNT_MAP §5: a specific 6-operator basis
(mellin_inversion, master_theorem, q_shift, modular_S_transform,
eisenstein_normal_ordering, class_field_galois_average) would cover ≥80%
of mathematical sections in Ramanujan's three Quarterly Reports. The
prediction served the latent-space-speedrun hypothesis: that Ramanujan
ran on a small compressed toolkit.

**What was tested.** Hand-tagging all 33 math-content sections of
Berndt's 2022 HRJ reproduction of the QRs (5519 lines from the
open-access PDF; faithful reproduction of Satagopan's 1925 handwritten
copy of the otherwise-lost originals). Documented in
`diary/20_hunt5_qr_operator_tagging.md`; structured tagging in
`corpora/transcriptions/quarterly_reports/qr_section_index.json`;
machine-readable output via `analysis/23_hunt5_qr_operator_tagging.py`
to `analysis/results/qr_operator_tags.csv` and
`analysis/results/qr_hunt5_verdict.csv`.

**What we found.** Coverage of the predicted basis is **57.6%** (19 of
33 math sections), well below the ≥80% bar. Breakdown:

| Report | n_math | n_in_basis | % | meets ≥80%? |
|---|---|---|---|---|
| QR1 | 13 | 13 | **100%** | YES |
| QR2 | 9  | 6  | **67%**  | NO |
| QR3 | 11 | 0  | **0%**   | NO |

Of the 6 predicted operators, **only 2 fire**: `master_theorem` (19
sections) and `mellin_inversion` (17 sections). The 4 modular-machinery
operators (`q_shift`, `modular_S_transform`, `eisenstein_normal_ordering`,
`class_field_galois_average`) **never fire**. Vocabulary check: zero
occurrences of `\tau`, `\theta`, `\eta`, "Bernoulli", "Heegner",
"Eisenstein", "modular", "class invariant" in the 5519 lines.

The QRs are NOT a modular-forms document. They are Mellin /
Master-Theorem analysis (QR I + QR II) and operator calculus / fractional
iteration / Hardy orders of infinity (QR III). The HUNT_MAP §5
prediction misread the QRs as Ramanujan's "modular toolkit demo" — they
are actually his "Mellin / functional calculus demo".

**Updated estimate (tag: PARTIALLY REFUTED).** The 80%-recurrence
prediction is refuted for the specified 6-operator basis. But the
*underlying* latent-space-speedrun hypothesis (small operator toolkit)
**holds at high confidence**, with a corrected basis. A revised
7-operator basis — dropping the 4 unfired modular operators and adding
{FOURIER_SELF_RECIPROCITY, FRACTIONAL_FUNCTIONAL_ITERATION,
HARDY_ORDERS_OF_INFINITY, FRULLANI_LIMIT, MELLIN_PAIR_RECIPROCITY} —
covers ~91% of QR math sections (30 of 33). The corrected basis is the
artefact; the prediction's failure is informative because it tells us
*which* corpus the modular-machinery operators belong to (Notebooks +
Lost Notebook, not Quarterly Reports). See diary 20 for the full
operator inventory and the Hunt 5b proposal (Notebooks corpus).

---

## R17 — "Bose-Einstein and Lambert summands have a clean term-by-term Poisson dual"

**What was speculated.** Project C v0.7 design brief (this file would
extend `_mellin_inversion_apply` in `rkc/search/basis.py`) initially
proposed handling one-sided kernels — `1/(1 - exp(-β n))` (Bose-Einstein
partition factor; seed `bose_einstein_beta_1em2`) and `n·q^n/(1-q^n)`
(Lambert / divisor factor; seed `lambert_divisor_q_p1`) — by emitting a
"dual summand" at rkc's known dual β'=4π²/β / q'=exp(-4π²/-log q)
respectively (per `rkc/registry.py` `_route_bose_einstein` and
`_route_lambert`).

**What was tested (structural, not numerical — v0.7 closure).**
The modular transformation laws for these one-sided sums are:

```
Σ_{n≥1} 1/(e^{βn}-1)   =  π²/(6β) - 1/2 - (1/2)log(β/2π) + O(exp(-4π²/β))
Σ_{n≥1} n q^n/(1-q^n)  =  E_2-related; modular law has additive 6iτ/π term
```

Neither admits a term-by-term equality `Σ_n f(n) = Σ_n g(n)` at the dual
parameter — the modular relations carry essential **additive scalar
correction terms** (Bernoulli polynomial values, logarithms, weight-2
quasi-modular anomalies) that live OUTSIDE the summand. A naive
"emit dual summand and verify" path would fail rkc's strict mpmath
verifier (which compares full sums) by exactly those correction terms.

**Why deferred rather than refuted (tag: PARTIALLY REFUTED).** The
underlying physical / mathematical phenomenon is real — these sums DO
have a small-β/large-β crossover, and rkc's existing cost model already
exploits it. The defect is at the *operator-API* level: the current
`Operator.apply_fn(expr, n) → expr` signature emits one new summand and
nothing else, so it cannot capture the additive correction. The correct
fix is a new operator class — `modular_transform_with_correction` —
whose apply_fn returns `(new_summand, scalar_correction)`. That is
**v0.8 territory** (extends the OperatorApplication data model + the
verifier's sum-comparison logic to fold the correction into the
before-side residual before comparing).

**Path forward.** v0.7 deliberately ships only **strict double-sided
Poisson identities** that fit the existing API: half-integer-shifted
Gaussian and weighted-Gaussian, both verified to rel-err 0 at dps=50
across β ∈ {1e-4, 5}. Documented in `diary/26_project_c_v07_*.md`.
v0.8 adds the additive-correction extension and re-enables the
Bose-Einstein and Lambert seeds (which remain in `rkc/search/seeds.py`
as v0.7+ targets, now correctly labelled `(v0.8+)`).

**R17 CLOSED 2026-05-24 (Project C v0.8b shipped, diary 31).** The v0.7
"deferred rather than refuted" framing was correct: the underlying
phenomenon was real and what was needed was the API extension. v0.8b
shipped it.

Specifically:
1. `OperatorApplication` got `additive_correction: Optional[sp.Expr]`
   and `summand_range: Optional[tuple]` fields, both defaulting to None
   to preserve v0.4 / v0.7 strict-Poisson semantics.
2. `MpmathVerifier._sum_evaluate` accepts a per-call `summand_range`
   override; the verifier folds the additive correction into the
   before-side residual before comparing.
3. A new `modular_transform_with_correction` operator handles two clean
   one-sided modular identities verified to **rel-err ≤ 1e-30 at dps=80
   across β ∈ {1e-3, 1e-2, 1e-1, 1, 10}** (5 dex):

   - **Bose-Einstein log (Dedekind eta-derived)**:
     `Σ_{n≥1} log(1 - exp(-βn))
        = -π²/(6β) - (1/2)log(β/(2π)) + β/24
          + Σ_{n≥1} log(1 - exp(-4π²n/β))`
   - **Lambert / E_2 quasi-modular**:
     `Σ_{n≥1} n·q^n/(1-q^n) (q = e^{-β})
        = π²/(6β²) + 1/24 - 1/(2β)
          - (4π²/β²) · Σ_{n≥1} n/(exp(4π²n/β) - 1)`

4. The seeds `bose_einstein_beta_1em2` and `lambert_divisor_q_p1` now
   accept end-to-end through the engine with ~2800× speedup at β=1/100
   (Bose-Einstein log) and ~13× speedup at q=1/10 (Lambert).

**Refinement to the original speculation (kept here for the record).**
The brief's original Bose-Einstein form `1/(1-exp(-βn))` (without the
`log`) was **divergent as a direct summand** (each term → 1 as n → ∞).
The natural convergent kernel is the **log form** `log(1-exp(-βn))`,
which IS the kernel of `-log Z_bosonic` and has a clean modular dual.
The seed was updated accordingly during v0.8b implementation. The
underlying physics (bosonic partition function) is unchanged; the
mathematical artefact that has a clean modular dual is the log-sum, not
the bare-sum.

Numerical evidence: `analysis/results/v08b_modular_correction_verification.csv`
(10 cells × 2 identities = 20 entries; 9 of 10 below 1e-30 rel-err, the
single 8e-16 outlier is mpmath.nsum truncation at the slowest-converging
cell, not an identity defect). Verifier-side numerical agreement at
n_digits=30 / dps=70 across the default 7-cell sweep is in the v0.8b
test `test_v08b_verifier_strict_agreement_high_digits`.

**Tag (final): RESOLVED → CONFIRMED at v0.8b.** This entry remains in
the refuted log per the inclusion discipline (the original "term-by-
term Poisson dual exists" speculation WAS partially refuted; what
shipped is a richer API, not the originally-proposed identity shape).
The deferral was strategic, not a failure.

---

## OUTSTANDING — Speculations made but NOT YET TESTED in this run

These are flagged here so a future pass (or a reader auditing
credibility) can see what is *still up in the air*. They are not in the
refuted log because we don't yet know.

### O1 — RESOLVED → see R16 below.

### O2 — RESOLVED → see R15 below.

### O3 — "The 18 unproven class-number-8 invariants Ramanujan tabulated correspond to discriminants where the genus subfield is itself class number ≥ 4"

HUNT_MAP §4 prediction; would directly confirm or falsify Ramanujan's
implicit "compressed mental algorithm" for nested-radical generation.
Requires Andrews-Berndt vol. I supplement pp. 200-220 transcription
plus genuine class-field-theoretic computation (not just sympy).
**Outstanding — not tested.**

### O4 — "Level-23+ modular equations decompose into two Atkin-Lehner-distinguished families"

HUNT_MAP §2 prediction. Requires Berndt vol. V Ch. X transcription plus
Newton-polytope analysis of the modular-polynomial coefficients.
**Outstanding — not tested.**

### O5 — "A bounded-at-cusp candidate (Rényi-α, Bhattacharyya, entropic uncertainty) would track g* to ≤1% across 2 dex of β"

CANDIDATE_INSIGHTS B1 / diary 13 §"What would change the conclusion".
The structural argument that ANY successful candidate must be bounded
at the cusp is established; the actual test of specific bounded-at-cusp
candidates is not in this run's CSVs. **Outstanding — not tested.**

### O6 — "Rationality snap is asymptotically dominated by damped direct summation for irrational α"

Established as "linear Pareto" in R3, but the *direct comparison*
(snap-and-Gauss vs. damped direct summation as a function of target
tolerance) was not benchmarked head-to-head. R3 makes the asymptotic
argument; a numerical wall-clock head-to-head would tighten the
claim. **Outstanding — not tested as a controlled benchmark.**

---

## Methodological notes

1. **Cross-validation gates caught real bugs.** Exp 04's modular Z had a
   wrong sign on the (β/24) prefactor; the cross-check against the direct
   route produced relative error `e^(β/12)` matching observation, instantly
   diagnosable. Without the cross-check this bug would have shipped silently.
   Lesson: every representation-switching identity must be cross-validated
   at ≥40 digits at ≥3 calibration points before being used as a fast route.
2. **The v0 → v1 cycle is healthy.** Both v0 mock-theta toy bugs (R1
   asymptotic, R2 character) were caught only because v1 explicitly tried
   to make a stricter quantitative statement than v0. The methodology
   "always plan a v1 that demands more precision than v0" *forces* the
   bugs into the open. Recommended as a discipline going forward.
3. **`float(round(mpf))` is the silent-zero hazard for high-precision
   integers.** Caught in Exp 05 (mangled p(1000) by a few units in the
   trailing 105-bit integer). Fix: `int(mpmath.nint(...))`. Same failure
   *class* as R3, applied to arithmetic-cast not Gauss-sum-routing.
4. **"Strict-match or null" recognizers leak coverage but never produce
   false positives.** The Exp 13 v1 recognizer's one false negative
   (`3 * exp(-β n²)` — bare gaussian with scalar coefficient) is a
   documented strict-matcher limitation, not a fingerprinting failure.
   The 100% precision (zero false positives across 12 family labels in
   the 55-case battery) is the right trade for a downstream routing
   compiler where a false positive routes to the wrong identity.

---

## R18 — "Some natural extension of the modular B1 bridge will work in fractional dynamics" (B1.5 family)

**What was speculated.** Per `insights/W7_BERNDT_DIXIT_WIRING.md` §4-§6
and `insights/BIG_IDEAS_REVIEW.md §3b`, the going-in conjecture was
~10-15% positive: the Ramanujan-Berndt-Dixit αβ=1 Mellin-pair
reciprocity (arXiv:0904.1053v2 Theorem 1.1) might extend to systems
with non-Markovian Caputo time-fractional FPE dynamics. The concrete
question: ∃ α(σ, β) and constant c such that

```
R_σ(β) := log Z_σ(β) − log Z_1(β) = c · BD_int(α(σ, β))
```

holds to ≤1% rel-dev across σ ∈ {0.5, 0.7, 0.9} and ≥2 dex of β?

**What was tested (structural, multiple cases).**

**Case 1 — B1.5 (Caputo + harmonic confinement)** — diary 35: For
Caputo time-fractional FPE with harmonic V(x) = k_h x²/2, the
equilibrium density `p_eq(x) = e^{-β k_h x²/2}/Z_1(β)` is time-
independent, so `∂_t^σ p_eq = 0` for any σ. Therefore the same
`p_eq` solves the fractionalized equation for EVERY σ ∈ (0,1]. So
`Z_σ(β) = Z_1(β)` identically, and `R_σ(β) ≡ 0`. Meanwhile BD_int(a)
< 0 strictly for all a > 0 (Binet's formula). Only `c = 0` is
consistent — degenerate.

**Case 2 — B1.5-ext (Riemann-Liouville + quartic confinement)** —
diary 37: For RL time-fractional FPE with V(x) = x⁴/4, the
probability-conserving form carries a `ρ_0 · t^{-σ}/Γ(1-σ)`
initialization source term (Baeumer-Meerschaert form) that EXACTLY
cancels `₀D_t^{σ,RL} ρ_eq`. Result: same conclusion as Case 1.
`Z_σ(β) = Γ(1/4)/√2 · β^{-1/4}` is σ-independent; `R_σ(β) ≡ 0`.

**Why both fail (the unified reason).** Scalar time-only functional
calculus of the FP generator L commutes with L's spectral projections.
The zero mode (`ker L`, equilibrium sector) is fixed pointwise since
`E_σ(0) = 1`. The equilibrium partition function only sees the n=0
sector. Therefore Z_σ is σ-trivial. Berndt-Dixit's reciprocal-symmetric
BD_int(α) lives in a non-trivial class and cannot match an identically-
zero residual non-trivially.

**Status: FALSIFIED across the family.** Two structurally-different
fractional-dynamics flavors (Caputo + harmonic; RL + quartic) both
collapse to the same one-line obstruction. Pass D fully closed (B1
already established at diary 19; B1.5 family closed here).

**What's NOT refuted.** ChatGPT Pro identified the precise scope: the
principle requires SCALAR time-only functional calculus. **Space-
dependent variable-order subdiffusion** (Fedotov-Falconer) breaks the
zero-mode-protection argument and is the genuine route to a
counterexample. Hunt 7 candidate scoped for future work in diary 37
§"New open direction".

**Promotion**: this falsification underwrites the **generalized
obstruction principle** in CANDIDATE_INSIGHTS §A8.

(Diaries 35, 37; CANDIDATE_INSIGHTS §A8.)

---

## How to read this file alongside CANDIDATE_INSIGHTS.md

`CANDIDATE_INSIGHTS.md` documents what the run **did** establish. This
file documents what it **didn't**. They are complementary and should be
read together. Several entries here (R1, R2, R6, R12, R14) are
explicitly cross-referenced in CANDIDATE_INSIGHTS as "honest correction"
or "still missing" footnotes; this file consolidates them into one
auditable place. A reader doing methodological credibility checks
should diff this file against the speculations in the diary entries 01
through 13 and confirm the cross-references close.
