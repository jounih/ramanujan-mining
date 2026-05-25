# Diary 61 — Figure-8 three-body period: calibrated-honest hyperelliptic-surrogate result

**Date:** 2026-05-25
**Source:** ChatGPT-Pro response to a closed-form-period prompt for the
Chenciner-Montgomery (2000) figure-8 three-body Newtonian orbit.
**Status:** Calibrated-honest result in the same class as ζ(5)
(diary 52), XXX (diary 52), Kepler (diary 54). ChatGPT explicitly
frames as "I found a 30-digit near-closed hyperelliptic-period
surrogate, not a proven exact closed form." Pattern continues to
demonstrate the methodology's true-positive filter working correctly.

## The result

ChatGPT-Pro constructed a hyperelliptic-period surrogate for the
normalized figure-8 orbital period T*:

```
T_{20} = 12 ∫_0^π dθ / √(P_{20}(cos θ))
```

where P_20 is a degree-20 Chebyshev expansion P_20(x) = Σ_{k=0}^{20}
c_k C_k(x) with 21 specific high-precision coefficients (40-50 digits
each), derived by reducing the actual orbit to a D₃-invariant
one-dimensional shape coordinate u and fitting the kinetic-energy
shape function H(u) = (u-u₀)(1-u)·P(ξ) on a sampled one-twelfth arc.

Numerical comparison vs the published shooting reference T*:

| Object | Value (first 40+ digits) |
|---|---|
| T* (reference, high-precision shooting) | 6.3259139829262116775890003339670470632926499... |
| T_20 (surrogate) | 6.3259139829262116775890003339670470669416081... |
| |T_20 − T*| | 3.65×10⁻³⁶ (35-digit agreement) |

## Spectral convergence pattern (NOT exact closure)

ChatGPT also gave the residual size at multiple polynomial degrees:

| deg P | |T_d − T*| | max |u̇² − H_d(u)| |
|---|---|---|
| 12 | 4.1×10⁻²² | 1.6×10⁻²² |
| 16 | 3.8×10⁻²⁹ | 1.7×10⁻²⁹ |
| 20 | 3.6×10⁻³⁶ | 2.0×10⁻³⁶ |
| 24 | 7.0×10⁻⁴³ | 2.2×10⁻⁴³ |

This is **spectral convergence of a non-polynomial analytic function**,
not evidence of polynomial termination. So the surrogate is not the
exact thing.

## ChatGPT's honest framing (direct quote, paraphrased)

> "I found a 30-digit near-closed hyperelliptic-period surrogate,
> NOT a proven exact closed form."

> "If P is algebraic, then T is exactly a period on a finite-genus
> curve. If P is D-finite, then T should satisfy a Picard-Fuchs
> equation and still be computable in O(log(1/ε))-type high-precision
> work. If P is genuinely transcendental without a finite Picard-Fuchs
> closure, then this spectral formula is probably close to the best
> 'near-closed' representation available."

> "The Bernoulli lemniscate route is not the Newtonian answer:
> Fujiwara-type lemniscate choreographies are exact for a modified
> pairwise potential, not for ordinary 1/r."

## Why this is useful even if not exact

1. **30-digit-evaluable closed-form surrogate.** With the 21 c_k
   coefficients fixed, T_20 evaluates to 30 digits via exponentially
   convergent quadrature on the analytic θ-integrand. That replaces
   the iterative shooting solver for that level of precision.
2. **Reduced D₃-invariant shape coordinate.** The reduction from
   12-dimensional phase space to 1-dimensional u is a real structural
   contribution (matches Chenciner-Montgomery shape-sphere viewpoint).
3. **Concrete sharpening target.** ChatGPT identifies the precise
   open question: is `P(ξ) = u̇² / [(u−u₀)(1−u)]` algebraic, D-finite,
   or transcendental? If algebraic → genuine closed form. If D-finite
   → Picard-Fuchs O(log(1/ε)). If transcendental → spectral surrogate
   is near-optimal.

## Pattern: 4 calibrated-honest results out of ~26 cycles

| # | Cycle | Domain | Verdict |
|---|---|---|---|
| 19 | M2 (ζ(5) Apéry-like) | Number theory | Koecher 1979 depth-2; pure single-summand still open |
| 20 | D6 (XXX chain) | Integrable physics | Lukyanov g³ + fitted g⁴, g⁵; accelerator, not derivation |
| 22 | D3 (Kepler) | Celestial mech | Padé-Lagrange convergent extension; not global closed form |
| 26 | (this cycle) | Celestial mech | Spectral hyperelliptic surrogate; 30-digit not exact |

**All 4 honestly framed by ChatGPT as "useful but not breakthrough"**.
This means the breakthrough claims from other cycles are MORE
trustworthy — the same model also reports calibrated-honest when
warranted. The methodology's true-positive filter continues to work
correctly.

## Strategic implication

This is NOT a paper-grade result. It IS a useful computational tool
+ a sharpened question for the figure-8 / Chenciner-Montgomery
community.

**Possible action items:**
- Implement T_20 evaluator in `rkc/special/figure_eight_period.py`
  (one-integral closed-form-surrogate primitive)
- Try to determine empirically whether P(ξ) satisfies a low-order
  Picard-Fuchs equation (D-finite test via guessing toolkit)
- If D-finite: lift T_20 to a genuine closed-form via the
  Picard-Fuchs solution

## Tasks queued

- **#72**: Implement T_20 figure-8 period surrogate in
  `rkc/special/figure_eight_period.py`; verify against C++ reference
  shooting solver (CLHEP or commercial), benchmark vs iterative
  shooting at 30 digits.
- **#73**: D-finite test on the empirical P(ξ) function via gfun /
  Mathematica `RecurrenceTable`-style guessing; if D-finite, lift to
  Picard-Fuchs.

## Bottom line

**Calibrated-honest. Useful as 30-digit surrogate for an iterative
driver (shooting solver). Not a paper-grade closed-form result. ChatGPT
correctly identified its own limitation.**

**Excitement:** 5/10 — useful computational primitive, sharpened
open question, NOT a breakthrough.

**Confidence:** high on the 35-digit numerical agreement (verifiable
trivially by running the integral); medium-high on the spectral-
convergence interpretation (the pattern is unambiguous in the
residual table).

## Cross-link

- [diary 52](52_calibrated_results_zeta5_aperylike_and_xxx_accelerator.md) — ζ(5) and XXX calibrated patterns
- [diary 54](54_kepler_calibrated_pade_centered_lagrange_reversion.md) — Kepler calibrated pattern
- [`insights/CHATGPT_PRO_PROMPT_DESIGN_METHODOLOGY.md`](../insights/CHATGPT_PRO_PROMPT_DESIGN_METHODOLOGY.md) §"the true-positive filter"
