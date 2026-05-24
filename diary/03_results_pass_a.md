# Diary 03 — Pass A results: representation-switching gains on two kernels

**Date:** 2026-05-24
**Status:** Experiments 02, 03, 04 complete. RKC v0 prototype shipped.

## Experiment 02 — Theta-dual switching curve (Gaussian kernel)

Quantity: `Z(beta) = sum_{n in Z} exp(-beta n^2)`.
Two routes: direct vs Jacobi-theta dual `sqrt(pi/beta) * Z(pi^2/beta)`.
Sweep: beta in {1e-8 ... 1e8}, tol in {1e-6, 1e-12, 1e-30, 1e-100}, 68 cells.

**Result (file: `analysis/results/theta_dual_curve.csv`):**
- Small beta (T-winning regime): dual is dramatically cheaper.
  - At beta=1e-8, tol=1e-100: direct needs **151,745** terms vs dual **3**. Gain ≈ 50,000×.
- Large beta (D-winning regime): direct is dramatically cheaper. Symmetric.
- Crossover at beta = pi (where direct and dual become equally costly, since dual carries alpha = pi^2/beta).
- Crossover is **independent of tolerance** because both representations have the same form of exponential decay; only their decay rates differ.

**Caveat / bug:** initial certificate used "next term below tol" as the truncation criterion. This is loose when the sum is in its slow-decay regime; observed actual error 6e-4 against tol=1e-6 at beta=1e8. Fixed in experiment 03 by switching to a rigorous `erfc` tail bound.

## Experiment 03 — RKC v0 with rigorous tail bounds

File: `analysis/03_rkc_v0.py`.

Adds: `cost_direct_gaussian(beta, tol)` and `cost_dual_gaussian(beta, tol)` returning a `TruncatedSumCost(terms, tail_bound, why)`. Tail bound is `(sqrt(pi)/(2 sqrt(beta))) * erfc(N sqrt(beta))`, inverted by binary search on `erfc`. The `compile_and_run` function picks the cheaper route, runs it, cross-checks against the other route, reports certified-tail and observed relative agreement.

68/68 cells in the same beta x tol grid as experiment 02 now give:
- Rigorous tail bounds match or beat the observed relative agreement.
- Predicted cost is a *strict* upper bound on what's needed (the bound is tight up to constants).
- The route choice is identical to experiment 02 except for the boundary at beta ≈ pi (corrected by 1 term).

**Implication for any production RKC:** the bound machinery must be *kernel-specific*. The Gaussian case uses erfc; other kernels (Lambert, q-series, Dirichlet) will each need their own. The kernel registry must carry not just the dual identity but also the certificate function.

## Experiment 04 — Partition-function Z(beta) modular switch

Kernel: `Z(beta) = sum_{n>=0} p(n) exp(-beta n) = prod_{n>=1} (1 - exp(-beta n))^-1`.

This is the partition function of a 1D free-bosonic gas — physically meaningful, *not* Gaussian.

Modular S-transform of Dedekind eta gives:
```
Z(beta) = exp(-beta/24) sqrt(beta/(2 pi)) exp(pi^2/(6 beta)) / prod_{n>=1} (1 - exp(-4 pi^2 n / beta))
```

Sweep: beta in {1e-3 ... 1e4}, tol in {1e-12, 1e-30, 1e-60}.

**Result (file: `analysis/results/partition_modular_switch.csv`):**

| beta | tol | direct K | modular K | gain |
|------|-----|---------:|----------:|-----:|
| 1e-3 | 1e-12 | 34,540 | 1 | 35,000x |
| 1e-3 | 1e-60 | 145,064 | 1 | 145,000x |
| 1e-1 | 1e-30 | 715 | 1 | 715x |
| 1   | 1e-12 | 29 | 1 | 29x |
| 10  | 1e-12 | 3 | 8 | DIRECT wins |
| 100 | 1e-12 | 1 | 73 | DIRECT wins |
| 1e3 | 1e-12 | 1 | 783 | DIRECT wins |
| 1e4 | 1e-30 | 1 | 18,900 | DIRECT wins |

All routes agree to within tolerance.

Crossover at beta ≈ pi^2 ≈ 10 — where beta and 4*pi^2/beta become comparable, the "geometric" balance point of the two product representations.

**Initial bug:** my modular Z had the wrong sign on the (beta/24) prefactor. The relative error at beta=100 was exactly `e^(beta/12) = e^8.33 ≈ 4150`, matching the observed 4160. Caught by cross-checking against the direct route. Lesson: a representation-switching compiler will hallucinate spectacular gains if the dual identity is incorrectly encoded. The cross-check is non-negotiable.

## Synthesis after Pass A

Two completely different kernel families (Gaussian theta vs Bose-Einstein product) both exhibit the predicted representation-switching gain, in the same qualitative shape (asymmetric in temperature, with sharp crossover at the modular-balanced point, gain rising as power of tolerance).

The central hypothesis from ChatGPT-Pro's pass is **substantiated** on two independent kernels with full numerical certification. Not just a one-point anecdote.

The *machinery* of the gain — rigorous tail bounds, sign-correct dual identities, cross-checks — is more subtle than the headline suggests. Building an automatic RKC requires:

1. **A kernel registry** with (canonical form, dual identity, tail-bound function, certificate sample).
2. **A recognizer** mapping an arbitrary input expression to a registry entry (or "none").
3. **A cost model** comparing the term-count predictions across recognized routes and picking the cheap one.
4. **A cross-check protocol** running the chosen route AND the next-best route in low-precision mode to detect encoding bugs *before* trusting high-precision output.

Next: experiment 09 (the recognition layer per Gemini's question), then onward to the FEP / mock-modular bridge (Pass D, where genuine novelty plausibly lives per the SOTA agent's findings).
