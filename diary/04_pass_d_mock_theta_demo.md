# Diary 04 — Recognizer v0 + Pass D toy on the mock-modular bridge

**Date:** 2026-05-24
**Status:** experiments 09 and 15 complete.

## Experiment 09 — Kernel-Fingerprint Recognizer v0

File: `analysis/09_kernel_recognizer_v0.py`.

A 200-line working prototype answering Gemini's "next step" question. Walks a
sympy expression tree, fingerprints the summand, matches against a registry of
canonical kernels, and recommends a route with a quantitative gain estimate.

Registry v0 entries:
- `gaussian_quadratic` (theta-dual)
- `bose_einstein_geometric` (Dedekind-eta modular S)
- `lambert_divisor` (Eisenstein-style modular S)

Test battery results:

| Input | Recognized | cost_D | cost_T | route | gain |
|-------|-----------|------:|------:|------|-----:|
| exp(-1e-4 n²) | gaussian_quadratic | 554 | 2 | DUAL | 280× |
| exp(-1·n²) | gaussian_quadratic | 7 | 3 | DUAL | 2.3× |
| exp(-1e4 n²) | gaussian_quadratic | 2 | 164 | DIRECT | (0.012) |
| 1/(1-exp(-0.01 n)) | bose_einstein_geometric | 3225 | 1 | DUAL | 3200× |
| 1/(1-exp(-10 n)) | bose_einstein_geometric | 3 | 8 | DIRECT | (0.38) |
| 0.99^n/(1-0.99^n) | lambert_divisor | 3208 | 1 | DUAL | 3200× |
| 0.5^n/(1-0.5^n) | lambert_divisor | 41 | 1 | DUAL | 41× |
| sin(0.1 n) | (none) | — | — | — | — |

All 7 known kernels are routed correctly; the unknown kernel returns "none"
(no false positive). The recognizer scales to the registry — adding a new
kernel is a 3-function addition (match + 2 cost predictors).

**Gaps to close in v1:**
- The recognizer is brittle to expression rewrites (e.g. won't recognize
  `1/(1-exp(-βn))` written as `exp(βn)/(exp(βn)-1)`). Need a normalization
  pass before matching.
- The Lambert cost bound is informal (per-term bound, not tail integral).
- Mock-theta and partial-theta entries (high-novelty kernels per SOTA notes)
  are not yet in the registry.
- No support for *composite* energies (e.g. Gaussian + small Lambert).
  The "partial recognition + residual" path from diary 02 needs an API.

## Experiment 15 — Mock-theta residual demo (Pass D toy)

File: `analysis/15_mock_theta_residual_demo.py`.

Question: if a generative model's normalizing constant has a *mock* modular
q-expansion rather than a truly modular one, what happens when you fit it
with a modular surrogate?

Test object: Ramanujan's third-order mock theta
    f(q) = 1 + sum_{n>=1} q^(n^2) / prod_{k=1..n} (1 + q^k)^2
versus its plain-modular cousin
    theta_3(q) = 1 + 2 sum_{n>=1} q^(n^2)
evaluated at q = exp(-beta) for a beta sweep covering cold (q ≈ 0) to hot
(q ≈ 1) regimes.

Result (file: `analysis/results/mock_theta_residual.csv`):

| beta | q | f(q) | theta_3(q) | rho = f/theta_3 |
|------:|-----:|-----:|---------:|----:|
| 4.8 | 0.00823 | 1.0081 | 1.0165 | 0.992 |
| 1.2 | 0.3012 | 1.1820 | 1.6189 | 0.730 |
| 0.3 | 0.7408 | 1.2909 | 3.2360 | 0.399 |
| 0.075 | 0.9277 | 1.3224 | 6.4721 | 0.204 |
| 0.0188 | 0.9814 | 1.3306 | 12.944 | 0.103 |

- f(q) **saturates** near 1.33 as q → 1- (Watson-Hickerson radial-limit
  bounds — finite even though the q-series formally diverges).
- theta_3(q) **diverges** as sqrt(pi/beta) (Jacobi modular asymptotic).
- The ratio rho = f / theta_3 → 0 as beta → 0+, decaying as ~sqrt(beta).

**Interpretation as a structural EBM bias:**

If you fit an energy-based model whose true normalizer has the shape of
f(q) but you use a "purely modular" Z surrogate (theta_3 in this toy), you
*systematically* underestimate the log-partition function near the
critical / high-temperature regime by a factor that goes like 1/sqrt(beta).
This is not stochastic — it has a precise functional form.

The mock-theta literature (post-Zwegers) gives an explicit *real-analytic*
correction (the Eichler integral of a unary theta shadow) that, when added
to f, restores modular invariance. In EBM language, that correction is
the "missing piece" any modular-only sampler/estimator would never recover.

**What's novel about this demo** (per SOTA notes 00 and 01 on Pass D
white space): the "mock theta as bias-correction-against-a-modular-fit"
framing is not, to my knowledge, articulated in the EBM / FEP literature.
The math is well-known (Zwegers, Hickerson, Mortenson, Bringmann-Ono);
the *application* to fitted-normalizer bias diagnostics in EBMs is not.

**Honest caveats:**
- My `shadow_unary_theta` is a structurally-correct sketch, not the exact
  Hickerson-Mortenson shadow with the right normalization constant. A
  publishable bias-cancellation demo would need to plug in the precise
  unary theta and Eichler integral, and verify cancellation to many
  decimals. Doable; left as future work.
- f(q) is one of 17+ classical mock theta functions of various orders;
  the cosmological/physical interpretation varies. The "EBM normalizer
  with a mock theta shape" is a hypothetical — I have not produced an
  *independently-motivated* generative model whose Z is f(q). That is
  the natural next target (TODO #15 in the live plan).

## What's next

- Experiment 13: Lost Notebook 1729 / K3 manipulations (Ono-Trebat-Leder) —
  computational test of whether modern arithmetic-geometry structure
  recognized in Ramanujan's terse manipulations can be picked out by an
  extended recognizer.
- Experiment 17: "modular leading + mock residual" EBM v0 — actually fit
  a parametric family of leading-order modular forms to sampled data,
  measure residual, identify mock contribution.
- Experiment 19-20: latent-space speedrun evidence — quantify the
  "notational compression" and "parallel derivation" patterns in NB II
  using available transcriptions.
- Continuing rational-temperature snapping (Gemini lead 5) Pareto
  experiment.
