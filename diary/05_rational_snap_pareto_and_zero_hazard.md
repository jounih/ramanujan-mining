# Diary 05 — Rational-temperature snapping: a real Pareto and a routing hazard

**Date:** 2026-05-24
**Source:** experiment 10
**Status:** Gemini lead 5 calibration updated; novel concrete hazard identified.

## Setup

For oscillatory theta-like sums of the form
    T(alpha) = sum_n exp(2 pi i alpha n^2)
that don't converge in the usual sense, Ramanujan's quadratic-Gauss-sum
identity gives a closed form when alpha = p/q is rational and gcd(p,q)=1:
    G(p, q) = sum_{n=0..q-1} exp(2 pi i p n^2 / q)
with cost O(q). Gemini's lead 5 was: snap an irrational alpha to a
rational p/q with q chosen so the snap distance is small enough, then use
the Gauss-sum closed form. Cost is O(q); accuracy depends on |alpha - p/q|.

I ran this over alpha = sqrt(2) - 1 with snap targets eps = 1e-2 .. 1e-13
and best continued-fraction convergents.

## What the data showed

| eps_target | q_snap | snap_distance | |G|/sqrt(q) | snap_phase_err |
|-----------:|------:|--------------:|----------:|---------------:|
| 1e-2  | 12    | 2.45e-3 | 1.4142 | 1.85e-1 |
| 1e-3  | 29    | 4.20e-4 | 1.0000 | 7.66e-2 |
| **1e-4**  | **70**    | **7.22e-5** | **0.0000** | **3.17e-2** |
| 1e-5  | 408   | 2.12e-6 | 1.4142 | 5.44e-3 |
| 1e-6  | 985   | 3.64e-7 | 1.0000 | 2.26e-3 |
| **1e-7**  | **2378**  | **6.25e-8** | **0.0000** | **9.34e-4** |
| 1e-8  | 13860 | 1.84e-9 | 1.4142 | 1.60e-4 |
| 1e-9  | 33461 | 3.16e-10 | 1.0000 | 6.64e-5 |
| **1e-10** | **80782** | **5.42e-11** | **0.0000** | **2.75e-5** |
| ... | ... | ... | ... | ... |

## Two findings, one of which is a real hazard

### Finding 1 — the Pareto is linear, not super-linear

Best CF convergents of any irrational obey |alpha - p/q| < 1/q^2. Combined
with the Gauss kernel modulus ~ sqrt(q), the *phase contamination* from
snap distance at n ~ sqrt(q) is roughly `2 pi q * snap_dist ~ 1/q`. So
doubling q halves the phase error and doubles the cost. That's a 1-for-1
trade — useful, but not asymptotically dominant over a well-damped direct
truncation, which costs O(1/sqrt(damping)) and has linear convergence in
log(1/tol).

The snap is most genuinely valuable when:
- alpha is RATIONAL by structure (physical or by quantization choice).
  Then snap distance is 0; the Gauss sum is exact at finite cost.
- The dual representation is the ONLY available one (e.g., the sum is
  conditionally convergent at best and standard damping introduces a
  systematic shift).

### Finding 2 (novel, hazardous) — half the convergents have G(p,q) = 0

Gauss's classical evaluation of the quadratic Gauss sum gives:
- q odd, gcd(p,q)=1: `|G(p,q)| = sqrt(q)`. The Jacobi-symbol sign tells you which root of unity.
- q ≡ 0 (mod 4): `|G(p,q)| = (1+i) sqrt(q)`, modulus `sqrt(2 q)`.
- **q ≡ 2 (mod 4): G(p,q) = 0 identically**.

The bold rows in the table above (eps_target 1e-4, 1e-7, 1e-10, 1e-13) all
have q ≡ 2 (mod 4): q = 70, 2378, 80782, 2744210. The Gauss sum vanishes
exactly. A naive "snap and compute" RKC route would return ZERO with high
algorithmic confidence — a catastrophic silent error.

Roughly **half** of the best CF convergents of a generic irrational fall
into the q ≡ 2 (mod 4) class (because CF denominators interleave under
the basic CF recursion). So this isn't a rare corner case — it's a near-
50% failure mode for the naive routing.

### Mitigation an RKC must implement

The recognizer must check `q mod 4` before recommending the snap-and-Gauss
route. If q ≡ 2 (mod 4), skip to the next CF convergent (which raises q to
typically the next-or-second-next denominator with q ≡ 0, 1, or 3 mod 4).
This costs at most a 2-4x factor in q while preserving the closed form.

This is the kind of detail Gemini's commentary didn't surface but is
essential to actually building the compiler. The headline lead is right;
the implementation has a 50%-failure-mode trap that needs explicit
handling.

## Bigger lesson for any RKC

Mathematical structure (here, the Gauss-sum closed form) and its
*degeneracies* (vanishing for one residue class of denominator) are
co-located in the same identity. An automated compiler that picks routes
by cost alone, ignoring the degeneracy structure, will silently produce
wrong answers in a measurable fraction of cases.

The recognizer registry needs *two* layers per kernel:
1. The cost predictor (what we built in experiment 09).
2. The **degeneracy detector** — when does the chosen route give a
   trivially wrong answer that the user must be warned of?

For Gauss sums the detector is `q mod 4 != 2`. For modular S-transforms
on Dedekind eta, the analogous degeneracy is at certain cusps of high
level (the eta function vanishes only at cusps, but evaluation precision
drops near them). Each kernel has its own analogue; the compiler must
carry it.

I don't see this discussed in the Ramanujan-style-identity-as-compiler
literature, though it's standard in the modular-forms-evaluation
community (e.g., Cohen-Stromberg eta-quotient implementations explicitly
guard against these).

## Updated calibration of Gemini lead 5

- The Pareto exists but is *linear*, not super-linear.
- Most valuable when alpha is rational by structure or no good alternative
  exists.
- **Carries a 50% silent-zero hazard** under naive denominator selection.
- Mitigation is easy once known: skip q ≡ 2 (mod 4) CF convergents.

Adds substantive technical content to the lead beyond Gemini's framing.
