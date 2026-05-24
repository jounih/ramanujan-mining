# Candidate Insights from the Ramanujan Mining Run

A concise scannable summary of the operationally interesting findings from
this run. Each item carries a *confidence* tag and a *novelty* tag based on
the SOTA notes in `sota_comparisons/`. Where the finding is numerically
substantiated, the experiment file is linked.

Provenance flags:
- **(scan)** = primary source, NOT directly read in this env (network
  allow-list excluded archive.org / Trinity). Awaiting ChatGPT-Pro corpus
  fetched in a parallel run.
- **(transcription)** = identity copied verbatim from Berndt/Andrews
  printed commentary or Hardy *Collected Papers* (cited).
- **(training-memory)** = recalled from training data, numerically verified
  in this run before use.

---

## A. Substantiated — numerical evidence in this run

### A1. Representation switching gives 10^1 – 10^5 × term-count reductions on physically-meaningful kernels

**Confidence:** high. **Novelty:** the *quantification across kernels and
tolerances* is novel; the underlying identities are classical.

- Gaussian theta `Z(β) = Σ exp(-βn²)`: 68 cells, β∈{1e-8..1e8}, tol∈{1e-6..1e-100}.
  At β=1e-8, tol=1e-100: direct 151,745 terms vs dual 3. Crossover at β=π,
  tolerance-independent. (`analysis/02_theta_dual_switching_curve.py`)
- Bose-Einstein partition `Z(β) = Π(1-e^(-βn))⁻¹`: at β=1e-3, tol=1e-60:
  direct 145,064 product factors vs modular 1. Crossover at β≈π². Two
  independent kernels show the same qualitative gain pattern.
  (`analysis/04_partition_modular_switch.py`)

The "central hypothesis" from the ChatGPT-Pro first pass (reciprocal-kernel
compiler beats naive evaluation by orders of magnitude) is substantiated
on a second, distinct kernel family.

### A2. A naïve "next-term-below-tol" tail bound silently violates the target by 4-5 orders of magnitude in the slow-decay regime

**Confidence:** high. **Novelty:** technical, not in any RKC writeup I'm
aware of.

In experiment 02, using "next term < tol" as the truncation criterion gave
an *observed* relative error of 6e-4 against a tol=1e-6 target at β=1e8.
The fix is a rigorous erfc tail integral; implemented in
`analysis/03_rkc_v0.py`. **Any production RKC must co-design the tail-bound
machinery with the kernel registry.** Each registered kernel needs its own
certificate function, not a generic per-term check.

### A3. A working kernel-fingerprint recognizer is a standalone Python package

**Confidence:** high. **Novelty:** the live prototype itself is the
contribution. v0 in `analysis/09_kernel_recognizer_v0.py` (200 lines, 3
kernels); v1 in `analysis/13_recognizer_v1.py` (11 kernels with per-kernel
degeneracy detectors); **v2 shipped as standalone `ramanujan/rkc/` package**
(11 kernels + scalar-coefficient stripping + fuzzy second-pass matcher +
per-component composite cost rollup + per-term complexity tracking).

Benchmark progression: v0 7/7 trivially → v1 54/55 = 98.2% on a 55-case
battery (canonical / perturbed / composed / adversarial) → **v2 55/55 =
100%, macro precision 1.00, macro recall 0.95**, with the one v1 miss
(`3·exp(-βn²)`) fixed by the scalar-stripping wrapper and zero v1
regressions. 35 unit tests pass.

The silent-zero hazard (§A4) is built in as a hard degeneracy check —
fires on every adversarial Gauss-sum case at q ≡ 2 mod 4. Per-term cost
tracking (per §A7) is now wired through `rkc/costs.py`; mock-theta is
correctly priced at ~12× gaussian per-term.

Next-pass priority: wire `MODULAR_COMPLETION_REQUIRED` route through to
Exp 17's Watson-Hickerson Eichler integral so the recognizer produces a
numerical answer on mock-theta inputs rather than just emitting a flag.

### A4. Rational-temperature snapping has a 50%-silent-zero hazard from q ≡ 2 (mod 4) Gauss sums

**Confidence:** high. **Novelty:** appears genuinely missing from any
"compiler" framing of Gauss sums; well-known in the modular-forms-eval
community but not transferred to the EBM/RKC discussion.

For oscillatory T(α) = Σ exp(2πi α n²) at irrational α, "snap to
rational p/q and use Gauss-sum closed form" sounds clean. But Gauss's
classical evaluation gives G(p,q) = 0 *identically* when q ≡ 2 mod 4.
Roughly half of the best CF convergents of a generic irrational land in
that residue class. A naive snap-and-compute RKC returns ZERO with high
algorithmic confidence on those cases. (`analysis/10_rational_temp_snapping.py`)

Mitigation: registry must carry a per-kernel **degeneracy detector** that
guards against trivially-wrong outputs, separate from the cost predictor.
For Gauss sums the detector is `q mod 4 ≠ 2`. For Dedekind-eta S-transforms
near high-level cusps, an analogous precision-floor guard.

Also: the Pareto from snapping is *linear* (q doubles → error halves,
cost doubles), not super-linear. The snap is most valuable when α is
rational by structure or no good alternative exists, NOT as a generic
speedup over damped direct summation.

### A5. Mock-theta vs modular bias is visibly structural in a toy fit — UPGRADED to v1 with exact shadow; v0 had a real bug

**Confidence:** high (after v1). **Novelty:** the *application* to EBM-bias
diagnostics is, per SOTA notes 00 §6 and 01 §2, essentially unwritten.

**v0 finding (analysis/15):** Ramanujan's third-order mock theta f(q) stays
bounded (~1.33) as q → 1-, while a plain modular surrogate θ_3(q) diverges
as √(π/β). Ratio f/θ_3 → 0 as β → 0+. Fitting an EBM whose true Z has
shape f with a modular-only surrogate gives a systematic bias.

**v1 upgrade (analysis/17, diary 12):** plugged in the exact
Hickerson-Mortenson shadow + Eichler integral via Watson's 1936
transformation. Bias reduction ~258 bits at small β; modular cross-check
passes at ≥30 digits (75-80 digits for α ≤ 0.3). Caveat substantially
resolved for the conceptual point.

**v0 BUG retraction:** v0 used the EVEN Kronecker character (12/·); the
correct shadow uses the ODD primitive character mod 12 — otherwise the
weight-3/2 unary theta with `n` in front vanishes identically. v0's
claimed "1/√β" asymptotic for the bias was also wrong; the actual
modular-only residual saturates at the Watson-Hickerson radial limit 4/3.
Both errors are documented in diary 12.

**Still missing for publishable claim:** the "modular surrogate" in v1 is
Watson's partner function W rather than a canonical η-product / Eisenstein
form at level 6/12/24 — standard bibliographic work that was out of scope
for this run.

### A6. Representation-switching crossovers follow a universal "modular conjugate radius / β" pattern across three independent kernels

**Confidence:** high (three independent confirmations now). **Novelty:**
the cross-kernel constant is new framing; the per-kernel S-transforms are
classical.

Each representation-switching curve in this run has a crossover β* set by
the kernel's modular S-transform:

| Kernel | Crossover β* | S-transform balance |
|--------|-------------:|---------------------|
| Gaussian theta `Σ e^{-βn²}` (Exp 02) | π | direct rate β vs dual rate π²/β balanced at β = π |
| Bose-Einstein partition `Π(1-e^{-βn})⁻¹` (Exp 04) | π² | dual variable 4π²/β reaches 1 at β = π² (less sharp; smeared by Dedekind eta prefactors) |
| Lambert/Eisenstein `Σ n^k q^n/(1-q^n)` (Exp 12) | 2π | direct rate β vs modular rate 4π²/β balanced at β = 2π |

All three follow the form β* = c·π where c is set by the prefactor of the
S-transformed argument. This is the operational principle a routing
recognizer should encode (cf. Recognizer v1, kernel registry).

### A7. The HRR / per-term-cost asymmetry: bits-per-term lies about wall-clock when each term is expensive

**Confidence:** high. **Novelty:** medium — known qualitatively in the
arblib community; the explicit quantification is new in this framing.

For partition `p(n)`, HRR climbs from 0.86 to 8.34 bits/term as n goes
10 → 10⁵, while pentagonal-recurrence decays from 0.21 to 3.4×10⁻⁵ bits/term.
HRR therefore *should* dominate by ~10⁵× in cost. It dominates by only
~1.2× in wall-clock at n=10⁵ — because each HRR term requires φ(k)
Dedekind sums at dps=372, while each pentagonal term is a single big-int
add. Johansson's arblib closes the gap via binary-splitting + FLINT
bignums; without those, bits-per-term is a misleading routing metric.

**Lesson for the recognizer:** a kernel's bits-per-term gain must be
divided by per-term computational cost — the registry's cost estimator
needs to track per-term complexity, not just term count. (Exp 05,
diary 07.)

---

## B. Operationally plausible — needs more work

### B1. The Friston FEP × mock-modular bridge — partial verdict: forward direction is an IDENTITY; shadow ≠ standard info-theoretic quantities

**Confidence:** medium-high (after Exp 16). **Novelty:** still no published
work overlapping these areas — the verdict below is itself novel.

Both concrete entry points from B1 are now tested (Exp 16, diary 13):

**Forward direction (generative model → mock partition function): CONFIRMED
as an IDENTITY, not analogy.** A two-bosonic-species lattice gas at
imaginary fugacity z = -1, with Hamiltonian E = n² + Σk·(a_k+b_k), gives
Z(q) ≡ f(q) (Ramanujan's third-order mock theta) — verified to 25-50
digits across β ∈ [0.05, 10]. The construction has natural pieces (the
z=-1 bose-to-fermi duality is textbook) and hand-tuned pieces (the
Durfee-square q^(n²) core sector). The bridge is *structurally buildable*
in the forward direction.

**Reverse direction (shadow → info-theoretic quantity): FALSIFIED for the
four standard candidates.**

| candidate | median ratio to g* | max rel. dev | verdict |
|-----------|-------------------:|-------------:|---------|
| MI(n; total particles) | 0.0066 | 14× | FAIL |
| KL(unsigned ‖ signed) | 1.34 | 262× | FAIL |
| Surprise (cross-entropy) | 1.81 | 196× | FAIL |
| Fisher F(β) | 0.076 | factor of 2 | FAIL (closest) |

Structural reason: g*(τ) is BOUNDED at the cusp β → 0 (limit ≈ 3.46),
while KL and Surprise diverge there and MI and Fisher vanish. No standard
information divergence satisfies boundedness-at-cusp.

**Final interpretation (after Exp 16 + 18 + 20 + 21 + 22):** the shadow
is an **Eichler cocycle in H¹(Γ, V_k)** — a cohomological object on the
modular group, NOT derivable from any natural functional of the lattice
gas. **Twenty candidates total** across FIVE experiments, ALL fail the
strict ≤1% / ≥2-dex bar OR reduce to known classical identities (not
novel):

| Source | Candidates probed |
|--------|-------------------|
| Exp 16 (marginal divergences) | MI(n; total), KL(unsigned‖signed), Surprise, Fisher F(β) |
| Exp 18 (bounded-at-cusp) | Rényi α∈{0.5, 1.5, 2, 5, ∞}, Bhattacharyya d_B, Hellinger², entropic uncertainty |
| Exp 20 (Wigner-negativity-aware) | negativity volume, mana, Rényi-α=0.5 on |W|, Rényi-α=2 on |W| |
| Exp 21 (path-measure functionals) | path entropy production, path KL (cumulative), Eichler-shaped path average |
| Exp 22 (transfer-matrix eigenstructure) | diagonal T_K(β) with S-transform intertwiner test |

Mechanisms uncovered along the way:
- **Exp 18 surprise**: Rényi-α and Bhattacharyya *also* diverge at the
  cusp (contra textbook bounded-at-cusp expectation) because the unsigned
  bosonic mass migrates to n ~ 1/β while signed mass stays at n ~ O(1),
  so supports become asymptotically disjoint. Hellinger² stays bounded
  (saturates at 1) but has the wrong β-shape.
- **Exp 20 partial match**: D_{0.5}(|W|/L1 ‖ W_+/Z_+) has a closed form
  log(2L1/(L1+f)) → log(2) as β → 0, giving the cusp ratio
  log(2)/g*(0) = 0.20025… matching the empirical cusp-window median
  0.20033 to 0.04%. **Honest assessment: a zero-parameter coincidence of
  two bounded cusp values, not a deeper proportionality** — the bulk shape
  at β ≥ 0.3 fails by 100%. This is the only "near-match" anywhere in
  the 19-candidate sweep.
- **Exp 21 decisive structural failure**: the Eichler-shaped path average
  fails by ≥33 orders of magnitude because the cooling path traverses
  the imaginary-axis half-line **in the wrong direction**: the
  Watson-Hickerson Eichler integral runs from y_end outward to ∞
  (the cusp at ∞), but the cooling path goes from y_start → 0 (cusp at 0)
  toward y_end. **They are disjoint half-lines, traversed in opposite
  directions.** Worse: at small y the unary theta g(iy) ≈ 0 due to the
  alternating-sign cancellation that makes f a mock form, so the
  cooling-path integrand is essentially zero over most of the path.

**This rules out the partition-function-path-integral interpretation
structurally, not just numerically.** The shadow's path lives in a
direction the lattice-gas Markov chain never traverses.

- **Exp 22 final closure (transfer-matrix eigenstructure)**: three
  independent reasons the transfer matrix cannot carry the cocycle.
  (i) The diagonal transfer matrix has trivial eigenstructure —
  Γ-equivariance lives entirely in the trace, not in any spectral
  invariant. (ii) The S-transform Ω_K ↔ Ω'_K has a fundamental
  **(K+1)² dimension mismatch** at every finite K, so no unitary
  intertwiner can exist. (iii) The K → ∞ defect reduces analytically to
  Watson's 1936 partner-function identity: Δ_∞(β) = M(β) ≡ g*(β/2π).
  The closed-form constant c = 1 is **tautological** — Watson's
  90-year-old identity restated in lattice-gas language, not a new
  identification. (Verified to ~6 digits at K=24, β=0.5: confirms
  geometric K → ∞ convergence to Watson.)
  In the well-converged interior β ∈ [0.3, 3] (1 dex) the empirical
  ratio is 1.0000000140 with 0.28% rel.dev — but this is **disciplined
  rejection**: 1 dex below the 2-dex bar, and the constant is
  tautological. A noisier disciplined-rejection finding is more
  valuable here than a fabricated "near-match."

**No further structurally-different candidate families remain.** The
investigation has covered: marginal divergences, bounded-at-cusp
divergences, quasi-probability divergences, path-measure functionals,
and transfer-matrix eigenstructure. The clean negative across 20
candidates **essentially establishes the cohomological-irreducibility
conjecture**: g* is an intrinsic element of H¹(Γ, V_k), not derivable
from any natural functional of the lattice gas. Any future FEP × mock-
modular bridge must encode this cohomological structure DIRECTLY —
e.g., by treating the modular group's action as a primitive of the
generative model rather than emergent from configuration statistics.

The clean negative across 20 candidates is itself a publishable
contribution. It tells anyone trying to build the FEP × mock-modular
bridge that the completion is NOT a probabilistic functional of natural
marginals, NOT a bounded-at-cusp information divergence, NOT a quasi-
probability divergence on the joint signed measure, NOT a partition-
function path integral, AND NOT recoverable from the transfer matrix's
spectral data. The bridge, if it exists, requires direct cohomological
machinery built into the generative model from the start.

### B2. "Highly composite" tensor schedules is over-stated as a paradigm but contains a real niche lead

**Confidence:** medium negative. **Novelty:** low — FFTW / cuFFT / MKL
already handle non-power-of-2 sizes via Bluestein/Rader/Winograd.

Gemini's framing conflates "highly composite" (more divisors than any
smaller integer — Ramanujan's actual definition) with "smooth"
(no prime factor exceeds bound B). The relevant FFT optimum is
smoothness, not high compositeness. The narrower honest version is:
expose factorization metadata to the schedule planner so block / tile /
batch choices can leverage it. Some of this exists. What's missing is a
Ramanujan-style ranking function over (size, factor structure, hardware
cost model). Worth doing but no paradigm shift.

### B3. Modular-checksum DP is real but per-problem

**Confidence:** medium. **Novelty:** the general principle (number-theoretic
invariants as cheap parity-like checks on coefficient streams) is broader
than Ramanujan, and the per-problem work is in *finding the right
invariant for the DP at hand*. Ramanujan's specific congruences p(5n+4) ≡
0 mod 5 etc. apply when your DP coefficients literally are p(n).

---

## C. Genuine open targets identified for future passes

### C1. Lost Notebook pp. 341-343 / 1729-K3 manipulations

Per Ono-Trebat-Leder arXiv:1510.00735, Ramanujan's "1729 letter"
manipulations implicitly describe a K3 surface with Picard rank 18.
Ono speculates that LN pages 341-343 hide more K3 or Calabi-Yau
threefolds. **No proof exists.** A focused pass with the Ono-style
modularity tooling could turn this into a result.

Why it matters for an RKC: K3 elliptic genera are *mock* Jacobi forms
(Eguchi-Ooguri-Tachikawa) — exactly the territory of B1. A new K3
hidden in LN would feed directly into the kernel registry.

### C2. Modular equations at levels 23, 29, 31, 47 (NB II Ch. 19-21)

Per Berndt vol. V Ch. X, no general theory exists for the level-23+
"mixed" modular equations Ramanujan wrote down, only ad-hoc proofs
case by case. These are computationally relevant: modular polynomials
of level p are the input to Schoof-Elkies-Atkin point-counting on
elliptic curves over F_p, and Ramanujan's lower-degree alternatives
could give a constant-factor speedup at moderate p. Direct mining
target.

### C3. Eisenstein-style continued fractions in NB II Ch. 32

Per Bhatnagar arXiv:2208.12656, these entries lack a unifying framework.
Each is a candidate Lambert-series-of-quasi-modular companion ready to
plug into the recognizer registry — and they'd give the registry its
first quasi-modular (weight-2 anomaly) entry, which would expose new
classes of bias-correctable EBM normalizers.

### C4. Class invariants G_n of class-number-8, two-class-per-genus discriminants

The last ~18 of Ramanujan's 116 class invariants require Kronecker-limit
techniques he apparently used without writing them down. The "latent-space
speedrun" hypothesis predicts that these computations have a compressed
representation in his working memory that we should be able to reverse-
engineer; success would directly extend the kernel registry with
Ramanujan-Sato variants and explicit 1/π series at new levels.

---

## D. The "latent-space speedrun" hypothesis — partial evidence

The user's framing: Ramanujan's mathematical intuition was so fast
because he carried novel compressed representations in his head, letting
him "speedrun in latent space" — operating on entire generating functions
or modular objects as primitive tokens.

Operational predictions of this hypothesis (testable against scans I
don't have direct access to in this env but can reason about from
known transcriptions):
- **Notational compression density.** Identities should invoke many
  q-Pochhammer symbols, theta functions, modular discriminants as
  *named primitive objects* rather than spelling out infinite products.
- **Parallel-derivation evidence.** Consecutive folios should contain
  the same identity derived by two genuinely different routes — hallmark
  of search in compressed representation space.
- **Generating-function arithmetic.** Manipulations should happen at
  the level of whole GFs (multiply, divide, apply operator) rather than
  coefficient-by-coefficient.

All three are documented qualitatively in the Berndt commentaries; I
did not attempt quantitative survey in this pass (lacks primary scan
access here). This is a natural target for a parallel pass with the
ChatGPT-Pro fetched corpus.

A complementary computational angle: try to **discover** identities by
search in q-series notation primitives, parameterized by a small number
of structural choices (operator applications, character twists, modular
S-transforms). The RamanujanMachine project does this for constants via
continued fractions; an analogous search over the q-series identity
manifold has not been done at scale.

---

## E. Bottom-line synthesis (revised after the third parallel follow-up)

The strongest **operational** deliverable is the kernel-fingerprint
recognizer in `ramanujan/rkc/`, now end-to-end on mock-theta inputs.
Status:
- 11 registered kernels with per-kernel degeneracy detectors, scalar-
  coefficient stripping, fuzzy second-pass matcher, per-component
  composite cost rollup, per-term complexity tracking.
- **55/55 = 100% on the routing benchmark, macro precision 1.00.**
- **50/50 unit tests pass** (35 original + 15 completion tests).
- `MODULAR_COMPLETION_REQUIRED` route now wired through to the Watson-
  Hickerson Eichler integral. f3 is end-to-end callable to ≥30 digits;
  f5/f7 surface `CompletionNotImplemented` honestly (require Hickerson
  1988 / Berndt-Chan transcription).
- Silent-zero hazard caught on every adversarial Gauss-sum case.

The strongest **math-novelty** result is the FEP × mock-modular bridge
**closed verdict** (B1):
- Forward direction is an *identity* (lattice gas → Ramanujan's f to
  25-50 digits).
- Reverse direction is *falsified for 20 independent candidates* across
  Exp 16, 18, 20, 21, 22 — covering marginal divergences, bounded-at-cusp
  divergences, Wigner-negativity-aware divergences, path-measure
  functionals, and transfer-matrix eigenstructure. **No structurally-
  different candidate family remains.**
- Two decisive structural failures: Exp 21 (cooling path traverses the
  imaginary axis in the wrong direction from the Eichler integral —
  disjoint half-lines, opposite directions); Exp 22 (the (K+1)² dimension
  mismatch under S-transform means no finite-K intertwiner can exist;
  the K → ∞ defect reduces to Watson's 1936 partner-function identity,
  tautologically).
- Two non-trivial near-misses, both disciplined-rejected: Exp 20's
  log(2)/g*(0) cusp-asymptote coincidence (matches 0.04% at cusp, bulk
  shape fails 100%); Exp 22's interior β ∈ [0.3, 3] ratio 1.0000000140
  (matches to 7 decimals but only 1 dex, and the matching constant is
  Watson's known identity restated in lattice-gas language).

**The established conjecture (medium-high → high confidence after
Exp 22):** g* is irreducibly cohomological. The shadow is an intrinsic
element of H¹(Γ, V_k) — an Eichler cocycle for Γ acting on the upper
half-plane that does NOT reduce to any natural functional of the
underlying lattice gas. **The investigation is closed for the
candidate-family approach.** Any future FEP × mock-modular bridge must
encode the cohomological structure DIRECTLY as a primitive of the
generative model, not derive it from configuration statistics.

Publishable as a negative-with-conjecture paper as-is: "Twenty candidate
completions for a specific mock-modular EBM bridge are falsified across
five structurally-different families. The shadow is shown to be
intrinsically cohomological by a dimension-mismatch argument and a
path-direction argument. We conjecture that any future FEP × mock-
modular bridge requires a cohomological generative model."

The strongest **methodological** finding is the universal β* = c·π
crossover pattern (A6) across three independent kernels, which crystallizes
what the recognizer should encode and what a real routing cost-estimator
should track (per-term cost, not just term count — see A7).

The largest **practical hazard** remains the silent-zero failure of naive
rational-temperature snapping (A4) — built into the v1 recognizer's
Gauss-sum entry as a hard degeneracy check.

The largest **honest correction**: v0 of the mock-theta residual toy
(A5) had a real bug — even vs odd Kronecker character mod 12 — caught
and fixed in v1 with a 258-bit bias reduction. Documented in diary 12.

Everything in this document is reproducible from scripts in `analysis/`.
The diary entries (`diary/00..13`) capture how each finding came out,
including bugs caught and assumptions audited.
