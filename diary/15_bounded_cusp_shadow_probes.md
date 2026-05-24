# Diary 15 — Experiment 18: bounded-at-cusp shadow probes for the third-order mock theta f(q)

**Date:** 2026-05-24
**Status:** complete; clean negative result that *sharpens* the structural picture from Exp 16. Recommendation: pivot the bridge narrative toward cohomological / anomaly-theoretic completion.
**Source pointers:**
- `ramanujan/analysis/18_bounded_cusp_shadow_probes.py`
- `ramanujan/analysis/results/bounded_cusp_shadow_probes.csv`
- prior experiment: `diary/13_fep_mock_modular_toy.md`, `analysis/16_fep_mock_modular_toy.py`
- charter B1 in `ramanujan/insights/CANDIDATE_INSIGHTS.md`

This entry continues the falsification line of Exp 16. Exp 16 falsified the four "standard" info-theoretic candidates (MI, KL, Surprise, Fisher) as proxies for the Eichler integral g*(τ) of f's shadow, with a structural reason: g* is bounded at the cusp β → 0 (limit ≈ 3.46) while KL/Surprise diverge and MI/Fisher vanish. Diary 13 recommended the next class of probes: "bounded-at-cusp candidates (Rényi-α, Bhattacharyya, entropic uncertainty)". This is that experiment.

---

## (a) Convention chosen for the signed-weight subtlety

This is the first thing to nail down, because there is a real ambiguity.

**The bare weights `w(C) = (-1)^F · q^E(C)` are signed.** They sum, over all configurations C, to f(q) — a positive real for real q ∈ (0,1) but the per-configuration weights can have either sign because of the (-1)^F factor.

**The n-marginal is positive.** When we sum out (a_k, b_k) for fixed n, the bosonic factor `Σ_{a,b} (-q^k)^{a+b} = (1+q^k)^{-1}` is *positive* (1 + q^k > 0 for q ∈ (0,1)). So

  w_signed(n) = q^{n²} / Π_{k=1..n} (1+q^k)²    > 0,

and the n-marginal of the signed measure is therefore a bona-fide probability distribution after normalization by f(q). The signs cancel on the *interior* of each n-sector.

**Convention adopted (verbatim from the brief, option (a)):** operate on the n-marginal probability distributions p_signed(n) and p_unsigned(n) (both honest, both positive), and compare candidates against g*(τ). We do *not* extend into Wigner-style quasi-probability for the three primary candidates: that extension would be needed only if we wanted to probe candidates on the joint configuration measure, which has signed values at intermediate (a_k, b_k). All three candidate families in this experiment (Rényi-α, Bhattacharyya, entropic uncertainty) are well-defined on the n-marginals as written.

This is also the convention Exp 16 used implicitly. The choice is forced for honesty: a candidate built on signed weights through a logarithm or sqrt is mathematically undefined; reporting one would be a confusion of physics intuition with formal manipulation.

What we *do* lose by this choice: any information carried by the sign cancellations inside an n-sector is invisible to our candidates. If the shadow g*(τ) "knows" about those internal signs, no marginal-based information divergence can reproduce it. **This is a real structural hypothesis** — and the negative result below is consistent with it.

---

## (b) Candidates probed, with explicit data

The acceptance bar is identical to Exp 16: max |candidate/g* − median(candidate/g*)| / median ≤ 1% across the full β sweep (≥ 2 dex). The sweep here is β ∈ [10⁻⁵, 10] — **6 dex**, exceeding the Exp-16 bar.

### Candidate set

1. **Rényi-α divergence** D_α(P_unsigned ‖ P_signed) for α ∈ {0.5, 1.5, 2, 5, ∞}. Standard definition

   D_α(P‖Q) = (α−1)⁻¹ log Σᵢ pᵢ^α qᵢ^(1−α)        (α ≠ 1)
   D_∞(P‖Q) = log maxᵢ pᵢ/qᵢ

   Theoretical expectation pre-experiment: D_α for α < 1 should be bounded even when D₁ = KL diverges; α ≥ 1 expected to diverge similarly to KL.

2. **Bhattacharyya distance** d_B = −log Σᵢ √(pᵢ qᵢ). Bounded for any pair of probability distributions when their overlap is non-zero; vanishes when P = Q.

3. **Hellinger²** = 1 − Σᵢ √(pᵢ qᵢ). Bounded in [0, 1] by construction. Proper metric cousin of d_B.

4. **Entropic uncertainty** U(β) = H(n|P) − H(n) = −I(n; P) in the unsigned measure. Bounded in [−log|Ω|, 0]; flagged as a probable failure-class (it inherits MI's vanishing at the cusp) but probed anyway to test whether the *entire* entropic-uncertainty-of-marginals family fails together with MI.

### Numerical results (full table in CSV)

Excerpt at key β values:

| β       | g*    | D_{0.5} | D_{1.5} | D_2   | D_5   | D_∞   | d_B   | H²    | U       |
|--------:|------:|--------:|--------:|------:|------:|------:|------:|------:|--------:|
| 1e−5    | 3.461 | 1112    | 1112    | 1112  | 1112  | 1112  | 556   | 1.000 | −1.3e−4 |
| 1e−4    | 3.460 | 1141    | 1142    | 1142  | 1142  | 1142  | 571   | 1.000 | −1.3e−4 |
| 1e−3    | 3.463 | 818     | 1395    | 1420  | 1439  | 1445  | 409   | 1.000 | −1.4e−4 |
| 1e−2    | 3.457 | 79.3    | 144     | 161   | 212   | 325   | 39.7  | 1.000 | −3.0e−4 |
| 0.1     | 3.397 | 6.44    | 12.7    | 14.3  | 19.2  | 30.4  | 3.22  | 0.960 | −2.3e−2 |
| 1       | 2.754 | 0.131   | 0.439   | 0.577 | 0.971 | 1.91  | 0.065 | 0.063 | −0.280  |
| 10      | 1.034 | 3.7e−13 | 1.1e−12 | 1.5e−12 | 3.7e−12 | 1.8e−4 | 1.9e−13 | 1.9e−13 | −4.1e−8 |

### Proportionality tests (strict bar)

| candidate              | median ratio | max rel dev | verdict |
|------------------------|-------------:|------------:|--------:|
| renyi_α=0.5            |   4.17       |  82.5       | FAIL    |
| renyi_α=1.5            |   7.89       |  50.1       | FAIL    |
| renyi_α=2              |   8.87       |  45.2       | FAIL    |
| renyi_α=5              |  11.8        |  34.3       | FAIL    |
| renyi_α=∞              |  18.4        |  21.7       | FAIL    |
| bhattacharyya_dist     |   2.09       |  82.5       | FAIL    |
| hellinger_sq           |   0.289      |   1.0       | FAIL    |
| entropic_uncertainty   |  −6.1e−4     | 166.6       | FAIL    |

All eight candidates fail the strict 1%-rel-dev bar.

### Cusp behavior (the diagnostic that matters)

The point of this experiment was to test whether *bounded-at-cusp* candidates exist. The data forces a sharper categorization than I expected:

- **Rényi-α for α = 0.5 DIVERGES at the cusp** (D_{0.5}(1e−5) ≈ 1112). This is a surprise relative to the textbook expectation that D_α is bounded for α < 1. The reason is specific to *this pair of distributions*: the unsigned (bosonic) marginal puts essentially all its mass at large n (n ~ 1/β), where the signed marginal puts almost none. The integrand pᵤ^α p_s^(1−α) is dominated by large n where pᵤ ≫ p_s, and the sum log-diverges with the support cap. So even α = 0.5 diverges here — the boundedness of Rényi-α at α < 1 requires the two distributions to have *comparable support*, which fails dramatically at the cusp.

- **Bhattacharyya distance also diverges at the cusp** (d_B(1e−5) ≈ 556), and tracks exactly d_B = (1/2) · |log(overlap)| with overlap → 0 as supports decouple. Same mechanism as above.

- **Hellinger² SATURATES to 1** at the cusp — *this* is bounded as advertised, because H² is built from BC and BC → 0 (orthogonal supports) gives H² → 1. So Hellinger² is the only candidate that is actually bounded at the cusp in this setup. But its cusp value is 1, while g*(0) ≈ 3.461. **They differ by an absolute constant of ≈ 3.46 — and the ratio H²/g* takes values that range from 0.289 (cusp) to 1.8e−13 (large β).** Hellinger² goes to 0 too fast at large β; it lacks the polynomial tail g* has.

- **Entropic uncertainty (= −MI)** vanishes at both ends (U(1e−5) ≈ −1.3e−4, U(10) ≈ −4e−8) and peaks near β ≈ 1 — the same shape as MI from Exp 16, just flipped in sign. Inherits MI's failure mode and shape; no improvement.

### What would FALSIFY each candidate

Identical structure to Exp 16:

- **Rényi-α (each α)**: ratio (D_α / g*) must hold constant to 1% across the sweep. Verified false: ratios vary by 22×–82× across α.
- **Bhattacharyya d_B**: same test. Verified false: ratio varies by 82×.
- **Hellinger² (H²)**: same. Verified false: ratio varies by ~10¹². [This is the most informative single failure — see (d) below.]
- **Entropic uncertainty (−MI)**: same. Verified false: ratio varies by 166×.

---

## (c) Does any candidate pass the bar?

**No.** Eight candidates probed (five Rényi orders + Bhattacharyya + Hellinger² + entropic uncertainty), zero pass. The *closest by max-rel-deviation* is Hellinger² at 100% — meaning H²/g* varies by a factor of 2 (within the small-β regime), but spans 12 orders of magnitude across the full sweep. By the strict-bar standard, no candidate is even close.

A noteworthy observation: in the **small-β regime β ∈ [1e−5, 1e−4]** alone, the Rényi-α values are *internally consistent across α* — they all hit ~1112 at β = 1e−5, ~1141 at β = 1e−4, etc. — because the unsigned and signed marginals are nearly orthogonal there and the Rényi-α formula degenerates into log|support_overlap|^{−1}. This is structural and uninformative for the bridge question.

A second observation: Hellinger² alone is the only candidate that is *bounded* over the full sweep (range [1.9e−13, 1.000]). Bhattacharyya and Rényi-α all DIVERGE at the cusp despite the prior theoretical expectation, because the two marginals develop near-orthogonal supports there. So "bounded-at-cusp candidate" turned out to be a more stringent property than the textbook taxonomy suggested.

---

## (d) Conjecture statement for the closest near-match

The strict-bar verdict says no match. But let's see what proportionality constant a hypothetical exact analog WOULD need.

For Hellinger², the cusp limit is

  H²(P_u, P_s; β → 0) = 1   (because supports decouple, BC → 0)

and the empirical g* cusp limit is

  g*(i β / 2π; β → 0) ≈ 3.46140...

If H² were exactly proportional to g* at the cusp, the constant would be

  **c_cusp = g*(0) / H²(0) ≈ 3.4614**.

At β = 1 (mid-range), H²/g* ≈ 0.023, so c_mid ≈ 43. At β = 10, H²/g* ≈ 1.8e−13, so c_large ≈ 5e12. These do not agree even at the order-of-magnitude level — the conjecture "H² ∝ g*" is false by 12 orders of magnitude.

For Rényi-α in the high-α limit (α = ∞), at the cusp the ratio is 1112/3.461 ≈ 321; at β = 1 it is 0.69. These vary by a factor of ~500 over the sweep — also vastly outside the bar.

**Conclusion of the conjecture exercise**: there is no constant c such that any candidate ≈ c · g* across the sweep. The geometry of g* — *bounded at the cusp, polynomial-shaped, vanishing slowly at large β* — does not match any of the candidates tested.

---

## (e) Bottom-line claim with confidence tag

**Confidence:** medium-high.

**Bottom line:**

> **The shadow of Ramanujan's third-order mock theta f, as captured by the Eichler integral g*(τ), is not a member of any of the standard "bounded-at-cusp" information-divergence families on the natural n-marginals of the toy lattice gas.** Twelve candidates have now been tested across two experiments (four standard divergences in Exp 16, eight bounded-at-cusp variants here, including five Rényi orders, Bhattacharyya distance, Hellinger², and the −MI entropic uncertainty). All twelve fail the ≤1% / ≥2 dex strict proportionality bar.

The structural reason has crystallized further:

1. **Marginal-based information divergences cannot distinguish sign-cancellation patterns** that live on the *interior* of each n-sector. The (-1)^F factor that makes f a mock theta is integrated out before any divergence is computed. If g* "remembers" the signed-cancellation structure, no marginal-based divergence will track it.

2. **The supports of the signed and unsigned n-marginals decouple at the cusp.** This destroys the cusp-boundedness that Rényi-α (α < 1) and Bhattacharyya theoretically promise. The bosonic surrogate puts mass at n ~ 1/β; the signed (mock-theta) measure puts mass at n ~ O(1). In this asymptotically-disjoint-support regime, Rényi-α diverges for *every* α, and only Hellinger² stays bounded — at its trivial saturation value of 1, with no further structure.

3. **g* itself is a non-trivial bounded analytic function with O(1) curvature at the cusp.** Its shape is governed by the modular S-transformation of the unary theta g(τ) = Σ (−1)ⁿ (6n+1) e^{2πi(6n+1)²τ/24}, not by any probabilistic property of marginals.

These three facts together support the **anomaly-theoretic / cohomological interpretation** that diary 13 flagged as the alternative: g* measures the failure of the holomorphic part of f to be modular, and modularity is an algebraic / cohomological property, not a probabilistic-distribution property of marginals.

**The bridge story has TIGHTENED**, in the negative direction. The space of viable completions for "shadow = something" has narrowed substantially:

- Marginal divergences (any α, any pair): RULED OUT.
- Bounded-at-cusp marginal divergences: RULED OUT *empirically*, even those (Hellinger²) that satisfy the cusp-boundedness criterion — because being bounded at the cusp turns out to be necessary but not sufficient.
- The remaining candidates worth a future experiment are *signed-weight quasi-probability* extensions (Wigner-style negativity-aware functionals like the "Wigner negativity volume" or Renou-Spee–style quasi-probability divergences), which can in principle see the (-1)^F structure that marginal-based functionals cannot.

**Sharpened conjecture** (replaces the prior "shadow = some bounded info divergence" wishlist):

> **g*(τ) is not a probabilistic functional of any natural marginal of the toy lattice gas. The most likely formal status of g* is as the boundary value of a cohomological / anomaly-theoretic invariant — concretely, an Eichler cocycle in the cohomology H¹(Γ, V_k) for the modular group Γ acting on the period space V_k of weight-k forms.** This is a falsifiable claim: any future construction of g* as such a cocycle, plus a derivation showing the cocycle reduces to none of the divergences tested, would *confirm* this conjecture; conversely, an exhibition of a Wigner-negativity-aware divergence on the signed configuration measure that does pass the ≤1% / ≥2 dex bar would *refute* it.

---

## What would change the conclusion

- A **Wigner-negativity-aware divergence** on the joint signed measure (e.g. the "negativity volume" Σ_C |w(C)| − |Σ_C w(C)| or a Renou-Spee quasi-probability KL) that passes the strict bar would re-open the divergence-theoretic interpretation. Not implemented here; out of scope.
- A **non-marginal** information functional — e.g. one defined on the *path measure* of a Monte-Carlo dynamics whose stationary state is the signed weight — could in principle see interior sign cancellations. This is computationally much heavier and would require its own experiment.
- An **independent derivation** that g* is an Eichler cocycle in a specific cohomology, plus a no-go theorem that no Wigner-style divergence on the joint can equal it, would crystallize the conjecture above into a theorem.

---

## Caveats

- Hellinger² and Bhattacharyya use sqrt; if the marginals had quasi-probability negative entries we would need to choose a branch convention. Here the n-marginals are positive, so no ambiguity arises. This is the substantive content of the (a)-convention.
- All cusp-region values use n_max = 800 (the cap from Exp 16); for β < 0.001 the unsigned marginal is undertruncated and the Rényi/Bhattacharyya values are lower bounds. This *strengthens* the divergence-at-cusp observation. Hellinger² is not affected since both terms saturate.
- The entropic uncertainty uses the Exp-16 joint (n_max=18, P_max=80) for tractability; values agree with the −MI from Exp 16 to plotting precision.
- The "5 Rényi orders" choice covers the full taxonomic range; we did not bother with α = 0.1, 0.9, etc. since the α-dependence within the probed range is monotone and weak relative to the β-dependence.
- The Eichler integral prefactor is convention-dependent (same as Exp 16); rescaling it changes the absolute "median ratio" but not the "max rel dev", so the verdicts are convention-invariant.
