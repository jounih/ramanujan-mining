# Diary 18 — Experiment 21: path-measure shadow probes for the Eichler integral g*(τ)

**Date:** 2026-05-24
**Status:** complete; clean three-candidate negative result; the structurally-most-likely-positive candidate (the Eichler-shaped path average) FAILS by ≥ 10 orders of magnitude. The Eichler-cocycle conjecture for B1 is therefore *substantially strengthened* — the shadow is NOT a path average over the natural lattice-gas Markov chain.
**Source pointers:**
- `ramanujan/analysis/21_path_measure_shadow.py`
- `ramanujan/analysis/results/path_measure_shadow.csv`
- prior experiments: `diary/13_fep_mock_modular_toy.md`, `diary/15_bounded_cusp_shadow_probes.md`
- charter B1 in `ramanujan/insights/CANDIDATE_INSIGHTS.md`
- Watson-Hickerson Eichler-integral implementation: `analysis/17_mock_theta_residual_ebm_v1.py`

This entry continues the Exp 16 / Exp 18 falsification line. Twelve marginal-based candidates have already failed the strict 1% / 2-dex bar. The remaining structurally-most-promising candidate family was *path-measure functionals* — and the Eichler integral

  g*(τ) = (i/√2) ∫_{-τ̄}^{i∞} g(w) / √(-i(w+τ)) dw

is *literally* a path-measure (an integral over a path in the upper half-plane). If the shadow ↔ information bridge exists at all, candidate 3 (the Eichler-shaped path average over the lattice-gas cooling trajectory) is the structurally-most-likely match anywhere in the investigation.

---

## (a) The cooling-path parameterization

We construct a one-parameter family of paths through the lattice-gas state space, parameterized by inverse temperature β(t) on t ∈ [0, 1]:

  β(t) = β_start · (β_end / β_start)^t       (logarithmic interpolation)

with **β_start = 1e-5** (deep cusp; the limit β→0 corresponds to τ→0 in the upper half-plane, i.e. the cusp) and **β_end varying over the standard grid {1e-3, 1e-2, 0.1, 0.3, 1, 3, 10}**. The cooling path goes from cusp (small β, hot / disordered) to deep cold (large β, ordered). Along the path, P_{β(t)} is the (positive) n-marginal of the signed lattice-gas distribution from Exp 16; convention (a) of diary 15.

Discretization: 100 trapezoidal steps for candidates 1 and 2; 200 for candidate 3 (because the Eichler-shaped integrand has an integrable square-root singularity at t = 1, which we remove by a u = √(1-t) substitution to recover regular trapezoidal convergence).

Precision: mp.dps = 40. Trapezoidal rule on ~100 points limits accuracy to ~3-4 digits; mp.dps = 40 leaves ample headroom and keeps the per-step cost under O(n_max) per marginal evaluation (achieved by a cumulative-product reimplementation of `signed_marginal_n_fast` — the Exp 16 form was O(n_max²)).

---

## (b) Candidate verdicts

The strict bar (per Exp 16 / 18): max |candidate/g* − median(candidate/g*)| / median ≤ 1% across the ≥2-dex β_end sweep. Anything else FAILS.

### Candidate 1: PATH ENTROPY PRODUCTION

  S_prod(β_end) = ∫₀¹ dt · (∂_t β) · ⟨E⟩_β(t)

with ⟨E⟩ computed as the SIGNED conditional expectation under the (positive) n-marginal:

  ⟨E | n⟩_signed = n² − 2 · Σ_{k=1..n} k · q^k / (1 + q^k)
  ⟨E⟩_β        = Σ_n p_signed(n) · ⟨E | n⟩_signed.

(The k-occupation expectation per species in the signed measure is −q^k/(1+q^k), which is *negative* — a signature of the signed-measure / Wigner-style structure inside each n-sector. The two-species combination doubles it.)

Empirical sweep:

| β_end | S_prod | g* | ratio = S/g* |
|------:|------:|----:|------------:|
| 0.001 | 1.10e−4 | 3.463 | 3.18e−5 |
| 0.01  | 1.11e−3 | 3.457 | 3.21e−4 |
| 0.1   | 1.10e−2 | 3.397 | 3.24e−3 |
| 0.3   | 3.24e−2 | 3.281 | 9.86e−3 |
| 1     | 1.02e−1 | 2.754 | 3.70e−2 |
| 3     | 2.43e−1 | 1.913 | 1.27e−1 |
| 10    | 2.88e−1 | 1.034 | 2.78e−1 |

Median ratio = 0.00986; **max rel dev = 27.2** (≈ 2722% — way above the 1% bar).

**Verdict: FAIL.** The ratio S_prod / g* varies smoothly by **~4 orders of magnitude** across the sweep. Structurally, S_prod ~ β_end (linear in the small-β regime where ⟨E⟩ saturates and dβ/dt ~ β_end log(β_end/β_start)) while g* approaches the finite cusp value ~3.46. They have entirely different shapes.

**Falsifier (verified):** ratio S/g* changes by more than 1% across the grid. Verified at 2722%.

### Candidate 2: CUMULATIVE PATH KL DIVERGENCE

  D_path(β_end) = Σᵢ D_KL(P_{β(tᵢ)} ‖ P_{β(tᵢ₊₁)})  (per-step KLs summed; "info-theoretic length" of the cooling path)

Convention: the n-marginal of the signed lattice gas (positive; convention (a) of diary 15).

| β_end | D_path | g* | ratio |
|------:|------:|----:|------:|
| 0.001 | 4.54e−9 | 3.463 | 1.31e−9 |
| 0.01  | 6.70e−7 | 3.457 | 1.94e−7 |
| 0.1   | 7.76e−5 | 3.397 | 2.29e−5 |
| 0.3   | 6.04e−4 | 3.281 | 1.84e−4 |
| 1     | 3.98e−3 | 2.754 | 1.45e−3 |
| 3     | 1.76e−2 | 1.913 | 9.18e−3 |
| 10    | 3.21e−2 | 1.034 | 3.11e−2 |

Median ratio = 1.84e−4; **max rel dev = 167.6** (≈ 16766%).

**Verdict: FAIL.** D_path varies by **~7 orders of magnitude**; the ratio D_path / g* varies by **~7 orders**. Structurally D_path → 0 as β_end → β_start (the path has zero length); g* has finite cusp value ~3.46. They are *infinitely* mismatched at the cusp.

**Falsifier (verified):** ratio D/g* changes by more than 1% across the grid. Verified at 16766%.

### Candidate 3: EICHLER-SHAPED PATH AVERAGE (the structurally-most-likely candidate)

Construction. Map the cooling-path β(t) to a point on the imaginary axis in the upper half-plane:  τ(t) = i · β(t) / (2π). The Eichler kernel becomes

  K(t) = 1 / √(τ_end − τ(t))
       = 1 / √(i (β_end − β(t)) / (2π))
       = e^{−iπ/4} · √(2π / (β_end − β(t)))

(integrable square-root singularity at t = 1). The "shadow density" is g(iy(t)) where y(t) = β(t)/(2π) — the integrand of the unary-theta-form Eichler integral as a function of β. We compute

  I_eich(β_end) = ∫₀¹ dt · g(iβ(t)/(2π)) · K(t)

using a u = √(1-t) substitution that removes the singularity (Jacobian 2u exactly cancels 1/√(1-t)), with 200 trapezoidal steps in u. The integrand is complex; the natural real counterpart to g* is Re(I_eich), since g* is real on the imaginary axis. We also report |I_eich|.

Empirical sweep:

| β_end | Re(I_eich) | \|I_eich\| | g* | ratio_real | ratio_abs |
|------:|------:|------:|----:|------:|------:|
| 0.001 | −1.03e−34 | 1.46e−34 | 3.463 | −2.98e−35 | 4.22e−35 |
| 0.01  | −3.60e−34 | 5.10e−34 | 3.457 | −1.04e−34 | 1.47e−34 |
| 0.1   | 5.66e−6 | 8.00e−6 | 3.397 | 1.67e−6 | 2.36e−6 |
| 0.3   | 5.96e−2 | 8.43e−2 | 3.281 | 1.82e−2 | 2.57e−2 |
| 1     | 4.87e−1 | 6.89e−1 | 2.754 | 1.77e−1 | 2.50e−1 |
| 3     | 3.81e−1 | 5.39e−1 | 1.913 | 1.99e−1 | 2.82e−1 |
| 10    | 2.07e−1 | 2.92e−1 | 1.034 | 2.00e−1 | 2.83e−1 |

Median ratio (real) = 0.0182; **max rel dev = 10.0** (≈ 1000%). For |I_eich| the median is 0.0257 with the same 1000% max rel dev. The ratio span is from 4.2e−35 to 0.28 — **≥ 33 orders of magnitude**.

**Verdict: FAIL — decisively.**

The verdict is even cleaner than candidates 1 and 2 in one respect: the candidate-3 ratios at the cusp end of the β_end grid (β_end = 0.001 and 0.01) are *numerically zero* (1e−34 vs. g* ~ 3.46). The ratio is not just wrong — it's effectively zero at the cusp, while g* is at its *maximum* of ~3.46 there.

**Falsifier (verified):** ratio Re(I_eich)/g* changes by more than 1% across the grid. Verified at 1000% (the saturating value in the high-β_end regime); the true span is ≥33 orders of magnitude when including the cusp.

#### What closed-form constant would the conjecture require?

If candidate 3 held *as a uniform proportionality* across the β_end grid, we would expect a constant c such that I_eich ≈ c · g*. The empirical "ratios" at the deep-cold end of the grid (β_end ∈ {1, 3, 10}) cluster at ratio_real ≈ 0.18-0.20 — suggesting **c ≈ 0.2** *only in that regime*. But at the cusp the ratio is ~0 (sign cancellations in g(iy) at small y completely kill the integrand). **No constant c works across the grid** — the conjecture is FALSE, not merely off by a prefactor.

To make this even more concrete: c=0.2 would require the closed-form value √(π/(4π+...)) or similar — but no such constant matches a function-shape that disagrees on the cusp end. The structural ratio-shape (constant at deep cold, zero at cusp) is incompatible with any *uniform* proportionality.

#### Why does it fail? The structural reason

The unary theta g(iy) for the third-order mock theta f has the form

  g(iy) = Σ_{n ∈ ℤ} (−1)ⁿ (6n+1) exp(−π y (6n+1)² / 12).

At small y, the exponential damping factor exp(−π y N²/12) becomes ≈ 1 for N up to ~ √(12 dps log 10 / (π y)), so the series is *enormously* alternating-sign and *almost vanishes* by cancellation. Empirically g(i · 1e-5/(2π)) ≈ −4 × 10⁻³⁴ at mp.dps = 40 (i.e. it's at our numerical noise floor — essentially zero). At moderate y (say y = 0.05), g(iy) is order unity (~1.3 at y=0.1). At large y, g(iy) decays as exp(−π y / 12).

So **the integrand of candidate 3 is enormously suppressed at the cusp end of the cooling path** (where the lattice gas "lives" most of the path, since β(t) ~ β_start for most of t ∈ [0, 1] until t→1). The path-measure construction *integrates through a regime where g ≈ 0 by anomalous cancellation*. The integral therefore picks up almost no contribution from the cusp portion of the path; what little it does pick up comes from the immediate vicinity of t = 1 (β ≈ β_end), where the cancellation has not yet kicked in.

This means: **the Watson-Hickerson Eichler integral and the cooling-path Eichler integral are NOT the same integral, even though they share an integrand-and-kernel structure.** The Watson form

  M(α) = 4√(3α/(2π)) · ∫₀^∞ sinh(αt)/sinh(3αt/2) · e^{−3αt²/2} dt    (Exp 17)

integrates a different variable (t = position in the upper half-plane, parameterized differently) over a different range (0 to ∞, not bounded by β_end). The lattice-gas cooling-path version restricts the integration to a finite range and traverses it in a direction (cusp → cold) that, in the upper half-plane, *misses the part of the y-axis where g(iy) is appreciable*.

Equivalent rephrasing: **the natural Markov-chain path on the lattice gas runs along the imaginary axis in the upper half-plane from y_start ≈ 0 to y_end = β_end/(2π) — but this is the WRONG half-line for the Eichler integral.** The Eichler integral runs from y_end OUTWARD to infinity, not from the cusp to y_end. The two paths are *in opposite directions* and on *disjoint half-lines*. So the cooling-path Eichler-shaped integral has structurally no business equaling g*.

---

## (c) Bottom-line claim with confidence tag

**Confidence:** medium-high (clean three-candidate negative; the structurally-most-likely candidate fails by ≥ 33 orders of magnitude at the cusp and the FAIL mechanism is mathematically transparent).

**Bottom line:**

> **The shadow of Ramanujan's third-order mock theta f, as captured by the Eichler integral g*(τ), is NOT a path-measure functional of the natural cooling trajectory of the lattice-gas Markov chain — neither in the entropy-production sense, the cumulative-KL sense, nor the Eichler-shaped path-average sense. The third candidate (the structurally-most-likely-to-match in the entire investigation, because it shares the integrand-and-kernel structure of the true Eichler integral) FAILS the strict bar by ≥ 10³%, with a transparent structural reason: the lattice-gas cooling path traverses the part of the imaginary axis where g(iy) is suppressed by enormous sign cancellations, while the true Eichler integral integrates the OTHER half-line where g(iy) is appreciable.**

**Interpretation: the Eichler-cocycle conjecture (diary 15, §e) is substantially strengthened.** The shadow's path-integral structure is **intrinsic to Γ acting on the upper half-plane** and does NOT reduce to a partition-function path integral over the natural lattice-gas Markov chain. The Markov-chain path and the Eichler-integral contour are *in opposite directions* on the imaginary axis and traverse disjoint half-lines, so even if the integrand-and-kernel structures match formally, the integrals are computing entirely different things.

This narrows the viable interpretations of the shadow further:

- **NOT** any marginal-based information divergence on the n-marginal (12 candidates falsified, Exp 16 + 18).
- **NOT** any path-measure functional of the natural cooling-path Markov chain (3 candidates falsified, this experiment).
- **Remaining viable candidates** are: (a) signed-weight Wigner-style quasi-probability functionals on the *joint* configuration measure (still open; would access inner-sector sign structure invisible to the n-marginal — flagged for Exp 20 elsewhere); (b) the Eichler cocycle itself, as a cohomological invariant in H¹(Γ, V_k) with no partition-function shadow.

Of these, (b) gains evidential weight from each successive negative result.

**Falsifier going forward:** a Wigner-style negativity-aware divergence on the joint signed measure that passes the strict 1% / 2-dex bar would re-open the divergence-theoretic interpretation. Per the spec (and CLAUDE.md item 6), any noisy near-positive at such a candidate would be the worst possible outcome — strict discipline applies.

---

## (d) Caveats

- The "entropy production" candidate uses the *signed conditional* energy expectation, which is the natural extension consistent with convention (a) of diary 15. An unsigned version (using only bosonic-surrogate weights) would give a different number but still fail the cusp / cold ratio test (the unsigned mean energy also diverges in the wrong direction relative to g*).
- The path-KL candidate is the *cumulative* KL (summed per-step), not the *rate* (KL / dt). The rate form is essentially the Fisher information and was tested in Exp 16. The cumulative form is the natural path-measure analog (the "info-theoretic length"), distinct from the Fisher rate.
- Candidate 3 was computed with a u = √(1-t) substitution to integrate through the integrable singularity at t = 1 (β = β_end); n_steps = 200 in the u variable. The accuracy is limited by the trapezoidal rule on a smooth integrand in u, not by the original sqrt singularity in t. We verified internally that the cusp values (~10⁻³⁴) are below our numerical noise floor (cf. mp.dps = 40, so ~10⁻³⁵ is the floor); the FAIL conclusion is therefore robust.
- The unary theta g(iy) at very small y was computed with adaptive truncation `nrange ~ sqrt((dps-5)·log 10 / (3π y))`, which guarantees tail < 10⁻³⁵ at mp.dps = 40. The "essentially zero" cusp values of g are therefore the *true* value at the precision floor, not under-truncated.
- The "ratio span" of ~33 orders of magnitude is dominated by the cusp end. Even if we restricted the sweep to β_end ∈ {0.1, 0.3, 1, 3, 10} (the well-converged regime, 2 dex), the max rel dev would still be > 1000% — the candidate would still fail the strict bar.
- An alternative reading of "g_density(β)" would use the integrand of the Watson-Mordell form (sinh-based) rather than the unary-theta form. We did not pursue this because (a) Watson-Mordell is in the variable t (over R+), not β, so the natural "density as a function of β" is the unary theta, and (b) the structural argument in §(b) candidate 3 would apply equally — the cooling-path β-axis is the wrong contour for the true Eichler integral regardless of which integrand form is chosen.
