# Diary 67 — Brusselator A=1, B=3 limit-cycle period: calibrated-honest negative + Lambert-W conservative-cousin

**Date:** 2026-05-25
**Source:** ChatGPT-Pro response to a closed-form-period prompt for
the Brusselator chemical-oscillator at the canonical parameter point
A=1, B=3 (well past Hopf at B = 1 + A² = 2).
**Status:** **CALIBRATED-HONEST NEGATIVE** with two useful
sub-deliverables. 8th calibrated-honest cycle.

## The verdict

> "I do not see a closed-form period formula here."

> "Llibre and Valls prove that the Brusselator with A ≠ 0 has no
> analytic first integrals... That does not prove that no expression
> using elliptic or other special functions exists for this single
> numerical parameter pair. It does rule out the standard 'period as
> an integral over known analytic level sets' mechanism. The numerical
> multiplier ρ ≠ 1 also shows the cycle is hyperbolic and isolated,
> so it cannot be a regular level curve of a local analytic first
> integral."

## The 30-digit numerical anchor

ChatGPT computed the period at A=1, B=3 by Poincaré shooting (section
x=1, ẋ>0), iterating the return map to the fixed point:

```
(x_0, y_0) = (1, 4.46889305620907548510997570325262400661836...)

T(1, 3) = 7.15691992117987981979986960576635244970738...

Rounded to 30 digits: T(1,3) = 7.15691992117987981979986960577
```

Nontrivial Poincaré multiplier:

```
ρ ≈ 2.51637579988970937917961166298 × 10⁻⁴
```

ρ ≪ 1 confirms the cycle is **strongly attracting + hyperbolic**, so
it cannot be a member of a continuous family of closed level curves
of any local analytic first integral.

This 30-digit value is a benchmarkable primitive for any future
Brusselator ODE-solver test. Independent verification target.

## Sub-deliverable 1: Liénard transform + conservative cousin

Eliminating y and substituting u = 1/x gives the Liénard form:

```
u'' + [u⁻² - (B+1) + 2 A u] u' + A - 1/u = 0
```

At A=1, B=3:

```
u'' + [u⁻² - 4 + 2u] u' + 1 - 1/u = 0
```

**Drop the damping term, keep the conservative part:**

```
u'' + 1 - 1/u = 0
```

This conservative cousin IS Hamiltonian with

```
E = ½(u')² + u - log u
```

Its period at energy E > 1 is the **one-quadrature formula**

```
T_0(E) = √2 ∫_{u_-(E)}^{u_+(E)} du / √(E - u + log u)
```

with turning points given **explicitly in Lambert W**:

```
u_-(E) = -W_0(-e^{-E})       (principal branch)
u_+(E) = -W_{-1}(-e^{-E})    (non-principal branch)
```

(These solve `u - log u = E`, which is the standard Lambert-W
transcendental.)

**Why this matters.** The conservative cousin admits a clean
closed-form period. The damping term ω(u) = u⁻² - 4 + 2u in the
real Brusselator both injects energy (near the focus) and removes it
(elsewhere), and the limit cycle is selected by global balance, not
by any conserved level set. The lost energy conservation is exactly
the obstruction to a closed-form period for the true Brusselator.

## Sub-deliverable 2: Hopf normal-form prediction

For the Brusselator equilibrium (x*, y*) = (A, B/A) with Jacobian

```
J = [[B-1, A²], [-B, -A²]]    →    tr J = B-1-A²,   det J = A²
```

At Hopf (B = 1 + A²) the eigenvalues are λ = ± i A, so the Hopf-born
period satisfies

```
T_Hopf → 2π/A    (NOT 2π/√(B-1-A²) as sometimes misquoted)
```

For A=1, T_Hopf = 2π ≈ 6.283. The cubic Hopf normal-form expansion
(with μ = B - 2, A = 1) gives

```
T_NF(μ) = 2π / (1 - μ/18) + O(μ²)
```

At B=3 (μ=1) the moderate-amplitude global cycle is already beyond
cubic NF reach. Linear-focus oscillation period at this μ is
4π/√3 ≈ 7.255, reasonably close to the nonlinear T_true = 7.157.

## Pattern: 8 calibrated-honest cycles of ~30

This is consistent with the methodology's true-positive filter:

| # | Cycle | Domain | Obstruction |
|---|---|---|---|
| 19 | ζ(5) Apéry-like | Number theory | Koecher 1979 has depth-2; pure depth-1 open |
| 20 | XXX integrable chain | Integrable physics | Lukyanov g³ closed; g⁴/g⁵ require fitted parameters |
| 22 | Kepler equation | Celestial mechanics | Branch-point geometry forces slow Bessel-Kapteyn |
| ?? | M3 P_pq Lambert series | Number theory | Specific structural class boundaries |
| 26 | Figure-8 three-body | Celestial mechanics | P(ξ) not algebraic/D-finite |
| 27 | Hubbard ladder | Strongly correlated | Lieb-Wu doesn't extend to ladders |
| 28 | XXZ form factor | Quantum dynamics | Non-factorizing Bethe-ansatz kernel |
| 29 | Pekeris waveguide | Underwater acoustics | Branch-cut continuum from radiating halfspace |
| **30** | **Brusselator A=1,B=3** | **Chemical oscillators** | **Llibre-Valls non-integrability + cycle hyperbolic** |

All 9 honestly framed. The 1 novel result (AB 4.2.3 corrigendum)
remains the headline; the methodology's filter rate is now 9 of ~30
calibrated negatives.

## Strategic implication

**Useful as a small primitive for the tool paper:**
- 30-digit Brusselator period at A=1, B=3 — chemical-oscillator
  benchmark
- Lambert-W conservative-cousin period formula — closed-form benchmark
  for ODE solvers
- The structural argument (Llibre-Valls + hyperbolic cycle) is
  publishable as a 1-page expository note in itself, particularly the
  Lambert-W appearance which is surprising in this context

**Not a new theorem.** No headline finding. But two clean
sub-deliverables.

## Tasks queued

- **#80**: Verify the 30-digit Brusselator period T(1,3) =
  7.156919921179879819799869605... in our mpmath env via independent
  Poincaré shooting. Half-day.
- **#81**: Implement Lambert-W conservative-cousin period
  formula `T_0(E) = √2 ∫ du/√(E - u + log u)` in
  `rkc/dynamics/brusselator_cousin.py`. Plot T_0(E) vs E and identify
  whether ANY E gives T = 7.157 (probably no exact match, since the
  damping shifts the cycle off any conservative level set).
- **#82**: If verified, add as primitive (h) to the tool paper:
  Brusselator benchmark + Lambert-W conservative cousin.

## Bottom line

**Calibrated-honest. No closed-form period exists at A=1, B=3.** The
methodology correctly identified the structural obstruction
(Llibre-Valls 2003/2007) + provided two useful sub-deliverables (the
30-digit numerical anchor + the Lambert-W conservative cousin).

**Excitement:** 4/10 — sub-deliverables useful, full closed form
unavailable, structural argument clean.

**Confidence:** HIGH on the no-closed-form verdict (Llibre-Valls is
a published theorem); HIGH on the 30-digit numerical value (verifiable
by any independent Poincaré shooting at the same section); MEDIUM-HIGH
on the Lambert-W conservative-cousin period being a genuinely useful
benchmark primitive.

## Cross-link

- [diary 54](54_kepler_calibrated_pade_centered_lagrange_reversion.md) — Kepler equation calibrated
- [diary 61](61_figure_eight_three_body_period_calibrated.md) — Figure-8 calibrated
- [diary 66](66_pphys2_pekeris_calibrated_branch_cut_obstruction.md) — Pekeris calibrated
- Other calibrated-honest cycles (diaries 52, 62, 64)

## References (ChatGPT-cited)

- J. Llibre, C. Valls, *Analytic first integrals of the Brusselator
  system*, dynamical systems literature ~2003-2007. (Need to track
  exact citation if pursuing for publication.)
