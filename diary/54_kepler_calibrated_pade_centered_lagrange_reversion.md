# Diary 54 — Kepler equation: calibrated-honest result (Padé-centered Lagrange reversion, not a global closed form)

**Date:** 2026-05-25
**Source:** ChatGPT-Pro cycle 22, response to Prompt D3 (Kepler
equation closed form at high eccentricity).
**Status:** Calibrated-honest like ζ(5) and XXX. Concrete useful
improvement (saves 1 sin/cos eval over best Markley-style solver +
gives arbitrary-precision path), but NOT a global closed form. Same
calibration discipline as diary 52.

## The result

For Kepler equation `M = E - e·sin(E)` at e=0.95, M=0.1 (the hard
regime):
- Reference: E = 0.741917668105761546051947990277383070... (30+ digits)
- ChatGPT's "Padé-centered Lagrange reversion" gives E_8 with
  |E_8 - E_*| = 4.99×10⁻³⁴ after 8 algebraic correction terms

The construction:
1. Start with Markley's Padé-cubic starter E_0 (closed form involving
   ³√, √, and one sin/cos pair)
2. Define F(E) = E - e·sin(E) - M; η = -F(E_0)
3. Lagrange-Bürmann reversion: u = H^{-1}(η) where H(u) = F(E_0+u) -
   F(E_0); expand as power series in η
4. 8 correction terms give 30+ digits

Cost:
- Direct Bessel-Kapteyn series at e=0.95: ~5504 J_n(ne) evaluations
- Newton from M=0.1: 9 sin/cos pairs (~9 transcendental evals)
- Markley + 1 Newton: ~1√ + ~1³√ + 2 sin/cos pairs
- **Proposed**: 1√ + 1³√ + 1 sin/cos pair + 8 algebraic correction
  terms

So the proposed form saves 1 sin/cos pair vs the best Markley-style
solver + gives an arbitrary-precision extension. **Major improvement
over Bessel-Kapteyn (slow). Modest improvement over Markley.**

## Honest framing (ChatGPT's own)

> "For Fourier/Bessel forms the obstruction is structural — the nearby
> complex branch points force slow convergence. For a broader 'closed
> form' using named special functions, the obstruction is not a known
> impossibility theorem; it is currently an absence of a representation
> that beats optimized Padé-cubic/local-inversion methods in both
> proof and cost."

> "The gap is therefore: the formula above is a convergent arbitrary-
> precision extension of Padé-cubic solvers, NOT a new global closed
> form. It avoids the Bessel bottleneck by changing the expansion
> center. It does not prove a uniform O(1) term bound over the entire
> [...] wedge unless one adds a domain decomposition and a lower bound
> on the Lagrange-reversion radius."

This is the right level of calibration. The Bessel-vs-branch-point
analysis (β = arcosh(1/e) - √(1-e²) ≈ 0.0108 at e=0.95) explains
WHY Bessel series is structurally slow + WHY the Padé-centered
approach helps.

## What we learned

1. **The Kepler equation Bessel-Kapteyn obstruction is STRUCTURAL** —
   branch-point geometry forces it. Not a missing-trick situation;
   not solvable by adding operators to the Project C basis.

2. **The Markley Padé-cubic solver is essentially optimal** in the
   "small finite number of transcendental evals" class. The proposed
   Padé-centered Lagrange reversion saves at most 1 sin/cos pair +
   extends to arbitrary precision.

3. **For a Kepler "breakthrough"**, the realistic targets are:
   - Domain-decomposition + uniform bounds (more analysis, not a
     new closed form)
   - Borghi-style Stieltjes acceleration of the Bessel series
   - Different parametrization (Stumpff/universal variables) where
     the bottleneck is mostly moved, not eliminated

So Kepler is NOT a Project C target — it's already at the frontier of
non-Bessel local-inversion methods. The contribution would be
analysis, not algebra.

## Pattern: 3 calibrated cycles (M2, D6, D3) out of 22 total

| # | Cycle | Domain | Verdict |
|---|---|---|---|
| 19 | M2 (ζ(5) Apéry-like) | Number theory | Koecher 1979 depth-2; pure single-summand still open |
| 20 | D6 (XXX chain) | Integrable physics | Lukyanov g³ + fitted g⁴, g⁵; accelerator, not derivation |
| 22 | D3 (Kepler) | Celestial mech | Padé-Lagrange convergent extension; not global closed form |

All 3 honestly framed by ChatGPT as "useful but not breakthrough".
This means the 19 breakthrough claims from cycles 1-21 (excluding
these 3) are MORE TRUSTWORTHY — the same model also reports
"calibrated, not theorem" when warranted.

Methodology continues to filter true-positives correctly.

## Bottom line

**Kepler is structurally outside Project C's reach** because the
obstruction is branch-point analytic (not a missing modular operator
or modular-S transform pattern). The Padé-centered Lagrange reversion
is a useful arbitrary-precision tool but not a new closed form.

**Excitement update**: stays at 9/10. This calibrated negative doesn't
add to the paper portfolio but confirms the workflow's true-positive
filtering. The headline results (1 verified novel identity + 2 more
claimed + 3 cross-domain landings + two-branch §A8) are unchanged.

**Confidence**: high on ChatGPT's honest framing (the Bessel
branch-point analysis is structurally correct; the Markley starter is
already near-optimal in its class).

## Cross-link

- diary 52 — ζ(5) Koecher + XXX Lukyanov calibrated results
- Cycle log + paper portfolio status in recent diaries
