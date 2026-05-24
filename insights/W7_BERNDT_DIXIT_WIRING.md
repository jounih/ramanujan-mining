# W7 Wiring Sketch — Berndt-Dixit 2009 as the Concrete Identity for the Fractional-Calculus Bridge

**Date:** 2026-05-24
**Author note:** Drafted as a research sketch in response to H10 / W7 / T4 in
[todo.md](../todo.md). NOT a verified experiment; the goal is to make B1.5
falsifiable. Confidence is explicitly low going in (see §7). Per the run's
discipline, any "looks promising but I can't prove it works" finding is
INDICATIVE, not CONFIRMED.
**Source:** [downloaded-pdfs/0904.1053v2.pdf](../downloaded-pdfs/0904.1053v2.pdf)
(Berndt & Dixit, arXiv:0904.1053v2, April 2009; 10 pages). Treats Lost
Notebook pp. 219–227, "Copied from the Loose Papers" (Watson's handwriting,
not Ramanujan's directly). Original Ramanujan claim on LN p. 195 used a
*divergent* version of the series; Berndt-Dixit corrected the φ definition.

**Honesty check.** I read the statement of Theorem 1.1 carefully and worked
through the first proof in §3 line-by-line (eqs 3.1–3.13). I followed the
second proof in §4 only at the level of which Poisson-summation form is used
(Guinand's Theorem 4.1) — I did not re-derive Lemma 4.2. I have not
independently re-verified eq (1.3) numerically. The mapping in §2 below is my
analysis, not Berndt-Dixit's.

---

## 1. Theorem 1.1, transcribed verbatim

Berndt-Dixit's Theorem 1.1 (Berndt-Dixit 2009, p. 1, eqs 1.1–1.3):

> Let
> ```
> ψ(x) := Γ'(x)/Γ(x) = −γ − Σ_{k=0}^∞ [ 1/(k+x) − 1/(k+1) ],          (1.1)
> ```
> where γ denotes Euler's constant. Let
> ```
> ξ(s) := (s−1) π^{−s/2} Γ(1 + s/2) ζ(s),
> Ξ(t/2) := ξ(1/2 + it/2).
> ```
> Define
> ```
> φ(x) := ψ(x) + 1/(2x) − log x.                                       (1.2)
> ```
> If α and β are positive numbers such that αβ = 1, then
> ```
> √α · { (γ − log(2πα))/(2α)  +  Σ_{n=1}^∞ φ(nα) }
>   = √β · { (γ − log(2πβ))/(2β)  +  Σ_{n=1}^∞ φ(nβ) }
>   = −(1/π^{3/2}) ∫_0^∞ |Ξ(t/2) Γ((−1+it)/4)|² · cos((t/2) log α)/(1+t²) dt.
>                                                                       (1.3)
> ```

Three observations on the structure of (1.3):

- **The αβ=1 coupling is the parameter analogue of the modular S-transform.**
  α ↔ 1/α is exactly how `τ → −1/τ` acts on the imaginary axis: if `τ = iα`
  then `−1/τ = i/α = iβ`. (1.3) says the two "sides" — series at α and
  series at β — are equal, with their common value computed by the Ξ-integral.
- **(a) The analogue of "the original Ramanujan summand":** the series
  `Σ_{n=1}^∞ φ(nα)` on the left of (1.3). It is a Mellin-style discrete sum
  of `φ` sampled at the lattice `αℕ`, mirroring how Ramanujan's lattice-gas
  partition function `f(q) = Σ q^{n²}/(−q;q)²` is a discrete sum sampled at
  the lattice `n ∈ ℕ` weighted by `q^{n²}`. Crucially, `φ` is `ψ` with its
  *leading asymptotic terms removed*: `ψ(x) ~ log x − 1/(2x)` at large `x`,
  so `φ(x) ~ O(1/x²)` and the sum converges. The `+1/(2x) − log x`
  subtraction is structurally an **Eichler-style polynomial subtraction** —
  removing the divergent / non-modular pieces so what remains can be paired
  with an `αβ=1`-symmetric integral. (Ramanujan's original LN p. 195
  statement used `φ = ψ + 1/(2x) − γ − log x`, which makes the series
  diverge — Berndt-Dixit's first contribution was to fix this.)
- **(b) The analogue of "the modular S-transform partner":** the
  right-hand series `Σ_{n=1}^∞ φ(nβ)` together with the polynomial
  prefactor `(γ − log(2πβ))/(2β)`. Setting them equal under αβ=1 is exactly
  the analogue of the Eichler equivariance `Z(τ) = (something)·Z(−1/τ) +
  cocycle`. The Ξ-integral plays the role of Watson's `M(α)` — the
  α-independent "spectral measure" whose Mellin-transform-with-respect-to-α
  reproduces both sides.

In Eichler-cocycle language: the LHS series at α minus the RHS series at β,
weighted by their √α, √β factors and polynomial subtractions, **forms a
1-cocycle of `α ↔ 1/α`** valued in a logarithmic-polynomial completion
class. The Ξ-integrand `|Ξ(t/2) Γ((−1+it)/4)|² / (1+t²)` is positive and
α-independent; the only α-dependent piece is `cos((t/2) log α)`, which is
manifestly even under `α → 1/α`. So the Ξ-integral is a fixed function on
the α/β orbit, exactly the way `g*(τ)` is a fixed cohomology class on the
upper half-plane modulo Γ.

---

## 2. Operator-class mapping to QR III §15

QR III §15 ([corpora/transcriptions/quarterly_reports/qr_section_index.json](../corpora/transcriptions/quarterly_reports/qr_section_index.json) section qr3_sec_15)
states a Mellin-pair self-reciprocity theorem: if `F` and `f` satisfy
```
∫_0^∞ F(ax) f(bx) dx = 1/(a+b)
```
(equivalently `∫ x^{p−1} F dx · ∫ x^{−p} f dx = π/sin(πp)`), then the
Fourier-like pair `ψ(n) = ∫ φ(x) [F(nxi)+F(−nxi)]/2 dx` implies
`φ(n) = (2/π) ∫ ψ(x) [f(nxi)+f(−nxi)]/2 dx`. Corollary 1 (e^{−x} pair) is
the Fourier cos pair, which is QR II Theorem III. Corollary 5 specialises
m=n=2, a=b=1.

**The Berndt-Dixit Theorem 1.1 IS a specific Mellin pair (F, f) in this
schema, with αβ=1 playing the role of a + b on the *parameters* rather than
on the integration variable.** Concretely:

- The Mellin partner of `ψ(1+x) − log x` is essentially the digamma-via-
  Hurwitz-zeta integral representation. The exact (F, f) pair that
  underwrites Theorem 1.1 is read off the proof at eq (2.2):
  `φ(z) = −2 ∫_0^∞ t dt / [(t² + z²)(e^{2πt} − 1)]`, valid for Re z > 0.
  In QR III §15 schema this is the **F-side**: `F(t; z) = t / [(t²+z²)(e^{2πt}−1)]`,
  parameterised by z but with t the Mellin-conjugate variable.
- The **f-side partner** is what the Ξ-integral implicitly inverts:
  `|Ξ(t/2) Γ((−1+it)/4)|² / (1+t²)` is the *spectral density* such that
  Mellin-pairing it against `cos((t/2) log α)` (which is an even function of
  log α with Mellin variable `it/2`) reproduces the LHS series. Concretely,
  `cos((t/2) log α) = (α^{it/2} + α^{−it/2})/2` is the symmetric power-of-α
  pair, exactly the αβ=1-symmetric Mellin kernel.
- The αβ=1 condition is then the *parameter-side* analogue of the QR III
  §15 reciprocity. Where QR III §15 has `1/(a+b)` symmetric in the
  integration-variable scales a, b, Berndt-Dixit has the integrand
  `cos((t/2) log α) = cos((t/2) log(1/β)) = cos(−(t/2) log β)` symmetric
  under `α ↔ β = 1/α`.

So the operator-class is: **Mellin-pair self-reciprocity with multiplicative
parameter-coupling αβ=1**, i.e. the *parameter-Mellin-pair* version of
QR III §15. The (F, f) pair is the Hurwitz-zeta-style kernel paired with the
Ξ × Γ spectral density.

This mapping is **clean at the operator-class level** (both are Mellin-pair
self-reciprocity statements with multiplicative parameter symmetry) and
**slightly strained at the specific-pair level** (QR III §15 has a, b
appearing inside F(ax), f(bx) as scale parameters; Berndt-Dixit has α
appearing only in the sampling lattice `nα` of a univariate series). The
mapping is morally correct: both are Plancherel-style identities at αβ=1.
A skeptic could complain that QR III §15 is about *integral* reciprocity
and Berndt-Dixit is about a *discrete/integral* hybrid. The Poisson
summation in Berndt-Dixit's second proof (§4, Theorem 4.1) bridges them.

---

## 3. Comparison to the modular B1 setup (closed verdict)

B1 (closed; see [diary 19](../diary/19_eichler_cocycle_transfer_matrix.md),
[CANDIDATE_INSIGHTS §B1](CANDIDATE_INSIGHTS.md), [BIG_IDEAS_REVIEW §3](BIG_IDEAS_REVIEW.md)):

| B1 (modular, closed) | B1.5 (fractional, proposed) |
|---|---|
| Generative model: 2-bosonic-species lattice gas at z = −1 | Generative model: non-Markovian fractional Fokker-Planck system with power-law memory kernel |
| Partition function: `f(q) = Σ q^{n²}/(−q;q)²` = Ramanujan f mock theta | Partition function: `Z_α(β)` for the fractional FPE with order α ∈ (0,1] (α=1 is Markovian limit) |
| Markovian/modular "surrogate": Watson partner `W(q_1²)` modular under S | "Markovian surrogate": Z_{α=1}(β) — the Markov limit of the fractional FPE |
| Modular S-transform: `τ → −1/τ`, equivalently `β → π²/β` | Parameter S-transform: `α → 1/α` per Berndt-Dixit αβ=1 (a different "α" — see naming note) |
| Equivariance defect: Watson-Hickerson Eichler integral `g*(τ) = ∫ overline{shadow}(z)/(−i(z+τ))^{3/2} dz` | Equivariance defect: (log Z_α − log Z_1)(β), candidate match: Berndt-Dixit Ξ-integral |
| Verdict: forward = identity; reverse FALSIFIED for 20 candidates | Verdict: SCOPED + UNTESTED |

**Naming hazard.** "α" is overloaded — in Berndt-Dixit it's a positive scaling
parameter under αβ=1; in fractional Fokker-Planck it's the *fractional
order* of the time derivative (typically α ∈ (0,1]). To avoid confusion below
I'll write **σ for the FPE fractional order** and reserve **α, β for the
Berndt-Dixit pair**.

**Structural analogue claim (the B1.5 thesis):**

> For a 1-D fractional Fokker-Planck system parameterised by σ ∈ (0,1] (where
> σ=1 recovers the Markovian limit), the residual `R_σ(β) := log Z_σ(β) −
> log Z_1(β)` admits a closed-form representation in which the Berndt-Dixit
> Ξ-integral structure (the αβ=1 spectral measure) appears as a building
> block, with α a function of (σ, β).

The motivation for *that* specific structural analogue is exactly the QR III
§11 connection: the Riemann-Liouville fractional derivative — which is the
operator of the fractional FPE — is itself a Mellin-transform construction
(`x^{n−1}` kernel in the defining integral), so when Z_σ has a closed-form
Mellin representation, the residual against the Markovian surrogate should
also be a Mellin-transform object. The Berndt-Dixit Ξ-integral is the
natural specific Mellin-Plancherel structure that has the right αβ=1 (i.e.
inversion) symmetry.

**The B1 analog argument that should structurally fail for B1.5 — i.e. why
this might be wrong.** B1's reverse direction was killed by *cohomological
irreducibility*: the modular S-transform's action on the lattice gas state
space couldn't be lifted to a unitary intertwiner (Exp 22 dim mismatch). For
B1.5 the analogous question is: does the fractional FPE generator have an
α ↔ 1/α symmetry-action on its state space that lifts to the Berndt-Dixit
αβ=1 symmetry? If yes, the bridge could land. If no, the same structural
obstruction kills B1.5 too. I do not know the answer; I conjecture it is
"the symmetry lifts trivially on the propagator's Mellin transform but not
on the trajectory measure" — analogous to Exp 21's path-direction obstruction.
**This is the central open question.**

---

## 4. Concrete W7 experiment proposal

### Setup

Take the 1-D fractional Fokker-Planck equation for the probability density
`p(x, t)`:
```
∂^σ_t p(x, t) = ∂_x [V'(x) p] + D · ∂_x² p,           σ ∈ (0, 1],
```
where `∂^σ_t` is the Caputo or Riemann-Liouville fractional derivative of
order σ (QR III §11's operator). At σ = 1 this is the Markovian Fokker-Planck
equation. For σ < 1 the dynamics is sub-diffusive with power-law memory; the
Mittag-Leffler function `E_σ(−Dk²t^σ)` replaces the exponential `exp(−Dk²t)`
in the free propagator.

**Pick the simplest non-trivial concrete case:** harmonic confinement
`V(x) = (1/2) k_h x²`. The Markovian (σ=1) partition function is the standard
Gaussian integral `Z_1(β) = √(2π/(β k_h))`. For σ < 1, the partition function
follows from the spectral decomposition of the fractional-FPE generator.
Closed forms exist via Mittag-Leffler eigenfunctions (Metzler & Klafter 2000
*Phys. Rep.*, Eq. 84ff and corollaries; check whether they give Z_σ explicitly
or just the propagator).

### Inputs
- σ ∈ {0.5, 0.6, 0.7, 0.8, 0.9, 1.0} (six values; σ=1.0 is the surrogate)
- β grid: logarithmically spaced over ≥ 2 decades, e.g. β ∈ {0.1, 0.3, 1, 3, 10, 30}
- k_h = 1 (units)
- mp.dps = 50

### Compute
1. `Z_σ(β)` for each (σ, β) cell. Two implementations cross-check:
   (a) Spectral sum over Mittag-Leffler eigenvalues; (b) numerical inversion
   of the fractional-FPE Laplace transform. Bar: agreement to ≥ 40 digits on
   the σ=1 cell (where the closed form `√(2π/β)` is the truth oracle) and on
   at least one σ < 1 cell against an independent Mittag-Leffler tabulation.
2. `R_σ(β) := log Z_σ(β) − log Z_1(β)` — the residual.
3. The Berndt-Dixit Ξ-integral RHS of (1.3) evaluated at some
   `α = α(σ, β)` map — the natural first guess is `α = c · β^{1/σ − 1}` or
   `α = β^{2σ−1}` (need to derive the right exponent from how the fractional
   derivative scales β; this is a key sub-question — see §6 below).
4. Define `BD_int(α) := −(1/π^{3/2}) ∫_0^∞ |Ξ(t/2) Γ((−1+it)/4)|² · cos((t/2)
   log α)/(1+t²) dt`.

### Residual test

Strict bar (per the run's discipline, [CLAUDE.md gotcha 6](../CLAUDE.md)):

> `|R_σ(β) / [c · BD_int(α(σ, β))] − 1| ≤ 1%` across **≥ 2 decades of β**,
> for some constant c independent of (σ, β).

If this is met, BD's structure recognises R_σ; **CONFIRMED**.

If `R_σ(β)` is dimensionally wrong, or wrong sign, or only matches at a
single β (no orders-of-magnitude span), or matches only after fitting α(σ,β)
with a free function: **FALSIFIED** or **INCONCLUSIVE**.

**Most important to predefine.** What does NOT count as success:
- A 1-parameter fit `R = A · BD_int(λβ)` that succeeds at one σ value (this
  is overfitting; need the same c across σ ∈ {0.5, 0.6, 0.7}).
- Agreement at the σ → 1 limit only (this is trivial: both sides → 0).
- A match on the leading log-log slope without matching the cos-oscillation
  structure of the Ξ-integral.

Verdict bucket per discipline:
- **CONFIRMED**: strict bar met across ≥ 3 σ values, single shared constant c.
- **INDICATIVE**: bar met for one σ over ≥ 2 dex but not stable across σ.
- **INCONCLUSIVE**: bar met only over 1 dex (matches B1 Exp 22 tight-window
  caveat: this is a *near-match at insufficient width*, not a pass).
- **FALSIFIED**: deviation > 10% across the grid, OR the natural α(σ, β) map
  produces α-values outside the Theorem 1.1 convergence domain.

---

## 5. Risk assessment

### Borrowed B1 failure modes that probably apply

1. **Bounded-at-cusp behaviour (Exp 18 lesson).** Many natural divergences
   between two partition functions are bounded as β → 0 or β → ∞; the
   Ξ-integral has specific cusp behaviour (`log α` blowup) that any
   candidate match must reproduce. If `R_σ(β)` is bounded at one cusp where
   BD_int diverges, the bar instantly fails.
2. **Cohomological irreducibility (Exp 22 lesson).** The Ξ-integral lives in
   a parameter-Eichler-cohomology class — analogous to `g* ∈ H¹(Γ, V_k)` for
   the modular case. If `R_σ(β)` is constructable from a "natural functional
   of the fractional propagator", it shouldn't reproduce a cohomology-class
   object. The dimension-mismatch argument from Exp 22 may have a fractional
   analogue: the σ-parameterised state space ≠ the 1/σ-parameterised state
   space at any finite truncation. **This is the most likely structural killer.**
3. **Path-direction (Exp 21 lesson).** The fractional FPE is non-Markovian
   precisely because the memory kernel breaks time-reversal symmetry: cooling
   from σ < 1 to σ = 1 is NOT the same as warming from σ = 1 to σ < 1 along
   the parameter trajectory. Berndt-Dixit's αβ=1 is *symmetric* under
   inversion. If R_σ inherits the time-direction asymmetry, it can't match
   an αβ=1-symmetric object.

### Two-three specific decisive failure scenarios

1. **Wrong scaling exponent.** If `R_σ(β)` scales as `β^p` and BD_int(λ·β^q)
   scales as `(log β)·(some oscillation)`, there is no exponent map `α =
   α(σ, β)` that makes them agree at leading order. Plot `log|R_σ|` vs `log
   β` for σ ∈ {0.5, 0.7, 0.9}; if the three curves don't collapse onto a
   single curve under any 2-parameter rescaling, the bridge fails.
2. **Cusp-behaviour mismatch.** BD_int(α) has a specific logarithmic
   divergence at α → 0 and α → ∞ (the `cos((t/2) log α)` becomes a delta-like
   ringing). If `R_σ(β)` is bounded as β → 0 (which is generic for partition
   functions with confined ground state), no choice of α(σ, β) will reproduce
   the BD_int cusp.
3. **σ → 1 limit pathology.** At σ → 1 the residual `R_σ → 0` by definition;
   BD_int → BD_int(α=1) = −(1/π^{3/2}) ∫ ... · 1/(1+t²) dt, a *non-zero
   constant*. Unless the map `α(σ → 1, β) → 1` is delicately tuned, the
   limits are inconsistent. So we already know `α(σ, β) → 1` as σ → 1, which
   constrains the form sharply — if BD_int(α(σ,β)) doesn't vanish at the
   right rate as σ → 1, the bridge fails.

Failure scenario 3 is **the cleanest pre-numeric kill**: it is essentially a
boundary-condition check that should be done before running the full grid.

---

## 6. Next experimental step: `analysis/25_w7_fractional_bridge_v0.py` outline

**Do not write the script in this pass.** Outline only:

```
# 25_w7_fractional_bridge_v0.py

INPUTS
- σ_grid = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
- β_grid = logspace(-1, 1.5, 30)  # 2.5 decades
- mp.dps = 50
- harmonic confinement k_h = 1

COMPUTE
1. Z_1(β) = sqrt(2π/β)  # closed form, truth oracle
2. For each σ < 1: Z_σ(β) via Mittag-Leffler spectral sum, cross-checked
   against Laplace-inversion of the Caputo-FPE Green's function. Bar:
   ≥40-digit agreement at one (σ, β) cell against published M-L table value
   (Metzler-Klafter 2000 or Mainardi-Pagnini).
3. R_σ(β) = log Z_σ(β) - log Z_1(β)
4. Berndt-Dixit Ξ-integral: implement via mpmath quad over t ∈ [0, T_max]
   with T_max chosen so the integrand drops below mp.eps. Cross-check
   against eq (1.3)'s series side at one (α, β) test cell — should agree to
   ≥30 digits (this validates the BD_int implementation independently of
   the bridge claim).
5. Try TWO natural α(σ, β) maps and report both:
   (i) α = β^(1/σ - 1)         # naive scaling-symmetry map
   (ii) α = (β/β_0)^(2σ-1)      # alternative consistent with σ→1 limit
6. Compute ratio_i(σ, β) = R_σ(β) / [c_i · BD_int(α_i(σ, β))]
   with c_i fit on (σ=0.5, β=1) cell, then check whether ratio_i is
   constant ≈ 1 across the rest of the grid.

OUTPUTS (write to ramanujan/analysis/results/25_*.csv)
- One row per (σ, β, map_i) cell: σ, β, log_Z_sigma, log_Z_1, R, alpha,
  BD_int, ratio, rel_dev
- Summary table: per-σ max |1 - ratio| over the β grid

REPORT TO DIARY
- Single-point cross-check of BD_int implementation (validates the
  numerical RHS of (1.3) to ≥30 digits before any bridge claim).
- Plot R_σ(β) vs β on log-log for σ ∈ {0.5, 0.7, 0.9}; comment on whether
  curves collapse under any 2-parameter rescaling.
- Verdict per discipline: CONFIRMED / INDICATIVE / INCONCLUSIVE / FALSIFIED.
- Cohomological / dimension-mismatch analogue check (qualitative):
  is the natural σ-truncated state space of the fractional FPE isomorphic
  to its 1/σ-image under any reasonable parameter map? If no, the B1.5
  bridge is structurally closed by the same argument that closed B1.

TARGET PRECISION
- mp.dps = 50 for all numerics; ≥40-digit cross-checks at validation cells.
- The strict bar (≤1% rel dev across ≥2 dex) is far above mp precision; the
  precision matters because subtraction R = log Z_σ - log Z_1 cancels
  leading digits at σ ≈ 1.

ABORT CONDITIONS
- If neither candidate α(σ, β) map satisfies the σ → 1 boundary condition
  (failure scenario 3 in §5), abort the bridge claim BEFORE running the
  full β sweep; report as "FALSIFIED by boundary-condition argument" with
  no further experiments needed.
```

This is a ~3-day implementation if Z_σ(β) admits a clean Mittag-Leffler
spectral form (which it should for harmonic confinement; see Mainardi 1996
*Chaos, Solitons & Fractals*). The validation cells (step 2 cross-check and
step 4 BD_int cross-check against (1.3) series side) take half the budget
because both involve mpmath at 50-digit precision.

---

## 7. Risk-aware confidence

**Going-in confidence that B1.5 lands positive (residual is recognisable):
~10–15%.**

Parallel-Claude's estimate was 15–25% (per [BIG_IDEAS_REVIEW §3b](BIG_IDEAS_REVIEW.md)).
I revise *downward* to 10–15% for three reasons:

1. **B1's reverse direction failed for 20 candidates across 5 structurally
   different families.** The B1 closure was very thorough; the cohomological-
   irreducibility argument that anchors it is general enough that I'd expect
   it to apply to *any* "generative-model side" / "modular-form side" bridge
   attempt, including B1.5. Concretely: Berndt-Dixit's Ξ-integral is
   structurally analogous to Watson's `M(α)` (both are spectral measures
   for the parameter-Plancherel pair); both are likely to be cohomologically
   irreducible in their respective settings. If true, no functional of the
   fractional FPE will reproduce BD_int, just as no functional of the lattice
   gas reproduced Watson's M(α).
2. **The σ → 1 boundary condition (failure scenario 3 in §5) is the most
   likely fast kill.** It requires the α(σ, β) map to be delicately tuned
   for the integral to vanish at the right rate. The two natural candidate
   maps I sketched probably don't satisfy it; we'd need a third map that
   carries the σ-derivative information in a non-obvious way.
3. **The mapping QR III §15 ↔ Theorem 1.1 is clean at the operator-class
   level but slightly strained at the specific-pair level (§2).** Operator-
   class analogues often guide the right framing without guaranteeing a
   numerical match. The B1 forward direction was a numerical *identity*
   precisely because the lattice gas → f(q) construction was specific, not
   operator-class-analogous; the analogue in B1.5 would require a *specific*
   non-Markovian lattice gas (or fractional process) whose partition function
   IS the Berndt-Dixit series, not just a structural sibling.

**What would push my confidence UP to 25–30%:** if the σ → 1 boundary
condition has a *natural* α(σ, β) map that satisfies it (e.g. one falling
out of the M-L expansion of Z_σ at leading order in (1 − σ)), and that map
also reproduces the cusp behaviour qualitatively.

**What would push my confidence DOWN below 5%:** if the literature scan
turns up a paper showing that Z_σ for the fractional FPE in harmonic
confinement is itself a Mellin-Barnes integral, but with a *different*
spectral measure from Berndt-Dixit's `|Ξ(t/2) Γ((−1+it)/4)|² / (1+t²)`.
That would mean the right "completion" is a different cohomology class, not
BD's specific one. Plausible reading; would close B1.5 to "wrong specific
identity, framework still open".

---

## Cross-references

- [BIG_IDEAS_REVIEW §3b](BIG_IDEAS_REVIEW.md) — B1.5 origin and framing
- [BIG_IDEAS_REVIEW §3](BIG_IDEAS_REVIEW.md) — B1 closed verdict
- [diary 19](../diary/19_eichler_cocycle_transfer_matrix.md) — B1 structural-negative
  argument (Exp 22 dim mismatch + Watson 1936 reduction)
- [todo.md H10 / W7 / T4](../todo.md) — the action items this sketch addresses
- [corpora/transcriptions/quarterly_reports/qr_section_index.json](../corpora/transcriptions/quarterly_reports/qr_section_index.json) §qr3_sec_15 — QR III §15 Mellin-pair operator
- [CANDIDATE_INSIGHTS §B1](CANDIDATE_INSIGHTS.md) — full B1 entry
- Berndt-Dixit 2009 source: [downloaded-pdfs/0904.1053v2.pdf](../downloaded-pdfs/0904.1053v2.pdf)
- Suggested literature for §4 implementation: Metzler & Klafter 2000
  (Phys. Rep. 339:1–77), Mainardi 1996 (Chaos, Solitons & Fractals 7:1461)

---

## Bottom-line claim with confidence tag

**Confidence:** low (~10–15%) on whether B1.5 lands as numerically positive.
**Confidence:** medium-high on whether the *wiring* in this sketch is
correctly stated (the αβ=1 ↔ τ → −1/τ mapping, the Eichler-style
polynomial-subtraction structure of `φ`, the operator-class identification
with QR III §15).

**Bottom line:** Berndt-Dixit Theorem 1.1 provides a *concrete*
Ramanujan-class identity with the right operator structure (αβ=1 Mellin-pair
self-reciprocity + Eichler-style polynomial subtraction + spectral Ξ-integral
on the "completion" side) to make W7 falsifiable. The experiment proposed in
§4 is a ~3-day numerical test with a predefined verdict bucket. *Going in,
the most likely outcome is FALSIFIED by the σ → 1 boundary-condition
argument (§5 scenario 3) or by a cohomological-irreducibility argument
analogous to Exp 22.* If the experiment fails as predicted, the B1.5
question remains open at the "need a fractional-Eichler-cohomology
formalism" level — the right completion is structurally different, not just
a different specific identity. If it succeeds, write up immediately.
