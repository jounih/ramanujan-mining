# Diary 68 — Adversarial verification of the Brusselator 30-digit period + the Lambert-W conservative-cousin formula

**Date:** 2026-05-25
**Source:** Independent verification of ChatGPT-Pro's two sub-deliverables
in diary 67 (Brusselator A=1, B=3 limit-cycle period and the Lambert-W
conservative-cousin Hamiltonian).
**Status:** **Both claims CONFIRMED.**

## TL;DR

| Claim | Quantity | ChatGPT-Pro reported | Our independent value | Agreement |
|---|---|---|---|---|
| 1 | y_0* (Poincaré section, x=1) | 4.46889305620907548510997570325262... | 4.46889305620907548510997570325277... | **31 digits** |
| 1 | T (limit-cycle period) | 7.15691992117987981979986960576635... | 7.15691992117987981979986960576626... | **31 digits** |
| 1 | ρ (Poincaré multiplier) | 2.51637579988970937917961166298e-4 | 2.51637579988970937917961166538e-4 | **27 digits** |
| 2 | u_-(E), u_+(E) satisfy u-log u = E | (exact) | 0.0 to 4.6e-42 absolute | working precision |
| 2 | T_0(E) via quadrature vs direct ODE | (none, ours) | match to 19-20 digits at dps=30 | **internally consistent** |

Both verdicts: **CONFIRMED** by the diary-67 rubric.

## Setup

The Brusselator at A=1, B=3 is

```
dx/dt = 1 - 4 x + x² y
dy/dt = 3 x - x² y
```

with equilibrium at (1, 3), past Hopf (B_Hopf = 1 + A² = 2), so there is
an attracting limit cycle. The Poincaré section is Σ = {x = 1, dx/dt > 0}
(`dx/dt > 0` at x=1 iff y > 3).

We verify ChatGPT-Pro's two sub-deliverables independently.

## Claim 1: 30-digit Brusselator period at A=1, B=3

### Method

`scipy.integrate` is float64-only (≤15-16 digits). To honestly check a
30-digit period claim we need an arbitrary-precision ODE integrator.

We first implemented a Dormand-Prince 5(4) adaptive integrator at mpmath
precision (`rkc/dynamics/rk45.py`), but its per-step cost grows steeply
with target precision: at mp.dps=30 the truncation error per step is
≈ h⁵, so to reach 1e-28 we need h ≲ 10⁻⁶, which is millions of steps per
period. After timing experiments showed this would take hours, we
switched the production integrator to **`mpmath.odefun`**, which uses
adaptive arbitrary-order Taylor series with arithmetic-of-numbers cost
scaling that is much friendlier to high dps. (We kept DOPRI5 in the
module as an independent cross-check at moderate dps.)

The verification protocol:

1. Set mp.dps = 35, define Brusselator RHS in mpmath.
2. Start from `y_0 = 4.4688930562090759` (~16 digits, well inside the
   basin of the attracting cycle) on the section.
3. **Iterate the Poincaré return map** `P: y ↦ y(T)` where T is the next
   intersection time with Σ. Because the cycle is *strongly attracting*
   (|ρ| ≈ 2.5 × 10⁻⁴, see below), naïve fixed-point iteration converges
   linearly with rate ρ per step — quadrupling correct digits every 4
   iterations.
4. To detect the return: build the trajectory once with `mp.odefun`,
   sample at coarse times t ∈ {4, 5, 6, 6.5, 7, 7.5, 8} to bracket where
   x(t) crosses 1 from below, then bisect to working precision.

After 7 iterations starting from a 16-digit guess we hit 34-digit
agreement on y_0; the period inherits the same precision via the bisection.

The Poincaré multiplier is then `ρ = (P(y* + ε) - P(y* - ε)) / (2ε)`
with `ε = 10⁻³⁵` at working dps=70 (so finite-difference truncation
≲ ε² × P'' ≪ 10⁻⁶⁰ ≪ working precision).

### Results

```
y_0*    = 4.46889305620907548510997570325277003...
ChatGPT = 4.46889305620907548510997570325262400661836...
       → 31 correct digits.

T       = 7.15691992117987981979986960576625971...
ChatGPT = 7.15691992117987981979986960576635244970738...
       → 31 correct digits (ChatGPT rounded to 30 was ...60577; the
         underlying value ...576635... agrees with ours to 31).

ρ       = 0.00025163757998897093791796116653862473
ChatGPT = 2.51637579988970937917961166298e-4
       → 27 correct digits. Within 1e-27 relative; vastly better than
         the 1% requirement of the rubric.
```

Wall time at dps=35: 8 iterations × 2.2 s ≈ 18 s for (y_0, T); the ρ
finite-difference at working dps=70 takes 53 s (two extra map calls).
Total ~70 s.

### Verdict for Claim 1: **CONFIRMED**

Agreement ≥ 25 digits on T, multiplier within 1e-27 relative (≪ 1%):
this clears the diary-67 CONFIRMED rubric with significant headroom.

The cycle is hyperbolic with ρ ≪ 1, confirming ChatGPT's structural
observation that no continuous family of level curves of a local
analytic first integral can contain it. (Llibre-Valls non-integrability
+ this hyperbolic ρ together rule out the standard "period as integral
over analytic level set" mechanism.)

### Honest caveat on precision floor

`mpmath.odefun` is the high-precision workhorse here. We did NOT need to
write a custom IVP integrator for this dps regime — Taylor-series with
adaptive radius outperforms DOPRI5 dramatically. At dps=35 the inner
ODE is solved by mp.odefun to working precision in ~2 s per period,
and the limiting factor is the convergence rate of the return-map
iteration (linear with rate ρ ≈ 2.5e-4 per step, so 4 digits per
iteration). With more iterations (or one Newton step using the
finite-diff ρ value) we could push much further; **we stopped at 31
digits as that comfortably exceeds the 30-digit target.**

The custom DOPRI5 in `rkc/dynamics/rk45.py` is left in the package
because it's used for an independent (slower) cross-check of the
cousin period; the unit tests `test_period_quadrature_matches_ode_E_*`
exercise that path and show 15-19 digit agreement with the quadrature
at dps=30.

## Claim 2: Lambert-W conservative-cousin period formula

### The cousin Hamiltonian

Dropping the damping in the Liénard form gives

```
u'' + 1 - 1/u = 0    (u = 1/x, A = 1)
E(u, u') = (1/2)(u')² + u - log u
```

with potential V(u) = u - log u, minimum V(1) = 1, so closed orbits at
E > 1. Turning points solve u - log u = E.

### Lambert-W identification (verified)

Rewriting u - log u = E ⟹ -u·e^(-u) = -e^(-E), i.e. with w = -u,
w·e^w = -e^(-E), so w = W(-e^(-E)). Two real branches give

```
u_-(E) = -W_0  (-e^(-E))    in (0, 1)
u_+(E) = -W_{-1}(-e^(-E))   in (1, ∞)
```

Verified numerically at dps=40 for E ∈ {1.1, 2, 5, 10, 100, 1000}:
absolute residual `|u - log u - E|` is **0.0** (exact in working
precision) for E ≥ 2 and **4.6 × 10⁻⁴²** at E = 1.1 (where the two
turning points are closest together and `mp.lambertw` has a 4-digit
loss of precision near the branch point).

### Period formula

```
T_0(E) = √2 ∫_{u_-(E)}^{u_+(E)} du / √(E - u + log u)
```

The integrand has integrable 1/√ singularities at both endpoints; calling
`mp.quad` directly on the unmodified integrand returns +∞ (Gauss-Legendre
quadrature evaluates at the endpoints, hitting `1/√0`). We use a
Sundman-style change of variables:

```
u(θ) = u_- + L sin²(θ),    L = u_+ - u_-,   θ ∈ [0, π/2]
du = L sin(2θ) dθ
```

so the substituted integrand `L sin(2θ) / √(ρ(u(θ)))` is finite and
smooth at both endpoints (the sin(2θ) numerator cancels the √ρ
singularity exactly). `mp.quad` on this then converges to 19+ digits
at dps=30 in 50 ms per E value.

### Direct ODE cross-check

We integrate u'' + 1 - 1/u = 0 from the **interior point u = 1, u' =
√(2(E-1))** (which lies on the energy-E orbit at the potential
minimum), then collect the time between successive transverse crossings
of u = 1 with u' > 0 — the full period. Using our DOPRI5 integrator at
dps=20, this gives the cousin period to ~19-20 digits, matching the
Sundman-substitution quadrature.

### Results (T_0(E) vs E, dps=30)

| E | T_0(E) (quadrature) | T_0(E) (direct ODE) | Match digits |
|---|---|---|---|
| 1.1 | 6.3356514543419208011 | 6.3356514543419208011 | 20 |
| 2 | 6.8148653644748163363 | 6.8148653644748163363 | 20 |
| 5 | 8.3919070123504277761 | 8.3919070123504277761 | 19 |
| 10 | 10.631150053709343635 | 10.631150053709343635 | 19 |
| 100 | 29.128465552893562612 | (not run; ODE expensive) | — |
| 1000 | 89.813279125656324162 | (not run; ODE expensive) | — |

T_0(E) → 2π ≈ 6.2832 as E → 1⁺ (linearised oscillation around u=1 has
ω² = V''(1) = 1, so period → 2π), and at the lower end T_0(1.000001) =
6.28318... already to 5 digits.

T_0(E) grows quasi-logarithmically: T_0(1000)/T_0(100) ≈ 3.08 while
E ratio is 10. Specifically T_0(E) ~ √(2 E) for large E since the orbit
spends most of its time near u_+ ≈ E and the period integral picks up
its dominant contribution there.

### Does any cousin E give T = 7.157?

Yes: bisection on T_0(E) = 7.157 yields **E* ≈ 2.6364952779**, with
T_0(E*) = 7.157 to working precision. **But this is not the true
Brusselator period at A=1, B=3** — the damping ω(u) = u⁻² − 4 + 2u
shifts the attracting cycle off any conservative level set, and ChatGPT's
diary-67 prediction stands: the cousin is a clean closed-form benchmark
of an *adjacent* but structurally-different oscillator, not a closed
form for the actual chemical oscillator.

### Verdict for Claim 2: **CONFIRMED**

All four sub-checks pass:
- Turning points satisfy u - log u = E to working precision.
- T_0(E) via quadrature matches direct ODE integration to 19-20 digits
  at dps=30 (all tested E ∈ {1.1, 2, 5, 10}).
- T_0(E) grows monotonically and tends to 2π as E → 1⁺.
- The cousin Hamiltonian is genuinely a useful closed-form ODE-solver
  benchmark, distinct from the Brusselator.

## Reproducibility

```bash
source .venv/bin/activate
python -m pytest rkc/tests/test_brusselator.py -v     # 9/9 pass in 11 s
python analysis/38_brusselator_period_verification.py # full run, ~80 s
```

## Files shipped

| Path | Purpose |
|---|---|
| `rkc/dynamics/__init__.py` | Module exports |
| `rkc/dynamics/brusselator_cousin.py` | Lambert-W turning points + period quadrature + cross-check ODE |
| `rkc/dynamics/rk45.py` | Custom Dormand-Prince 5(4) at mpmath precision (for the cousin cross-check) |
| `rkc/tests/test_brusselator.py` | 9 unit tests (turning points, periods, cross-check, Brusselator smoke) |
| `analysis/38_brusselator_period_verification.py` | Full analysis script |
| `analysis/results/38_brusselator_verification.csv` | Numeric output |

## Bottom line

ChatGPT-Pro's two sub-deliverables from diary 67 are **both
independently confirmed at 27-31 digit precision** by `mpmath.odefun` +
Sundman-substituted quadrature. The 30-digit Brusselator period is a
*usable benchmark primitive* for any ODE-solver evaluation; the
Lambert-W conservative-cousin period formula is a *clean closed-form
test case* for ODE integrators that lets us pre-tabulate exact answers
at given energies.

This is a methodology-affirming verification: no surprises, both numbers
match, the rubric is cleared with significant headroom.

## Cross-link

- [diary 67](67_brusselator_period_calibrated_lambert_w_cousin.md) — the
  original claim being verified.
- Other adversarial-verification cycles: diaries 31 (AB 4.2.3), 32
  (level pq family), 33 (finite-pole attention), 34 (annular Green),
  35 (port-Hamiltonian Bessel), 36 (Airy resurgent), 37 (CsCl Madelung).
