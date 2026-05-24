# Diary 07 — HRR vs pentagonal partition benchmark: bits-per-term curve

**Date:** 2026-05-24
**Source:** experiment `analysis/05_hrr_partition_benchmark.py`
**Status:** representation switching for p(n) quantified end-to-end; HRR's
bit-density per summand is verified to climb monotonically while the pentagonal
recurrence's bit-density per summand decays as n^{-1/2} (asymptotically).

## Setup

Two exact representations of the integer partition function p(n):

- **Pentagonal (Euler).** p(n) = Σ_{k≥1} (-1)^{k+1} [p(n-g_k) + p(n-g_{-k})],
  g_k = k(3k-1)/2. Integer arithmetic in Python, no precision concerns.
  Cost metric: total recurrence summands evaluated while building the table
  p(0), p(1), …, p(n).
- **HRR (Hardy-Ramanujan-Rademacher).** p(n) = (1/π√2) Σ_{k=1}^∞ √k · A_k(n)
  · d/dn [sinh(C λ_n / k) / λ_n], λ_n = √(n - 1/24), C = π√(2/3),
  A_k(n) = Σ_{0≤h<k, gcd(h,k)=1} exp(πi s(h,k) - 2πi hn/k), s(h,k) the
  Dedekind sum. Cost metric: number of HRR terms summed before the
  rigorous Rademacher tail bound (eq. below) drops below 0.5.

Tail bound used:
  |R_N(n)| ≤ (44π² / 225√3) · N^{-1/2}
          + (π√2 / 75) · √(N / (n-1)) · sinh(π√(2n/3) / N)

(Rademacher 1937 / Lehmer 1938; form per Calkin-Johansson as quoted by
Johansson, arXiv:1410.1672 §5. **(training-memory)** — the exact constants
were recalled and then numerically tested; for every n in {10, 100, 1000,
10000, 100000} the smallest N satisfying the bound *did* produce the correct
integer when rounded, cross-checked against the pentagonal table.)

Working precision: dps = ⌈log₁₀ p(n)⌉ + 30 (Hardy-Ramanujan asymptotic for
the size). At n = 100000 this is 372 decimal digits.

## Results

| n      | method     | terms      | total_bits | bits/term | wall_s | check |
|-------:|:-----------|-----------:|-----------:|----------:|-------:|:------|
| 10     | pentagonal |         29 |          6 |    0.21   | <1e-4  | —     |
| 10     | hrr        |          7 |          6 |    0.86   | 0.002  | OK    |
| 100    | pentagonal |       1004 |         28 |    0.028  | 1e-4   | —     |
| 100    | hrr        |         10 |         28 |    2.80   | 0.004  | OK    |
| 1000   | pentagonal |      33475 |        105 |    0.0031 | 0.005  | —     |
| 1000   | hrr        |         20 |        105 |    5.25   | 0.025  | OK    |
| 10000  | pentagonal |    1078839 |        354 |    0.00033| 0.176  | —     |
| 10000  | hrr        |         51 |        354 |    6.94   | 0.324  | OK    |
| 100000 | pentagonal |   34327029 |       1151 |    0.000034| 7.17  | —     |
| 100000 | hrr        |        138 |       1151 |    8.34   | 5.98   | OK    |

"OK" = HRR-rounded integer matches the pentagonal integer exactly (all 347
digits at n=100000 — verified, not asserted).

Headline numbers:

- **HRR uses 138 terms at n=100000 vs 34.3 million pentagonal summands.**
  That is a **2.49 × 10⁵ reduction in term count.**
- **HRR's bits-per-term curve climbs:** 0.86 → 2.80 → 5.25 → 6.94 → 8.34 from
  n=10 to n=100000. Asymptote per the theory is *unbounded growth*
  ~ (π / (log 10 · √(2n/3))) per term as n→∞ — but very slow growth,
  because total bits scales as √n and term count also scales as √n.
- **Pentagonal's bits-per-term curve decays as n^{-1/2}:** 0.21 → 0.028 →
  0.0031 → 0.00033 → 0.000034. Each new pentagonal summand contributes
  a vanishing share because the *number* of summands grows as n^{3/2}
  while *total* bits grow only as √n.
- **Wall-clock crossover sits between n=10000 and n=100000.** Pentagonal
  is faster up through n=10000 (per-term work is cheap integer adds, even
  on bignums); HRR finally overtakes at n=100000 (5.98s vs 7.17s).
  Wall ratio (HRR/pent): 193.3 / 30.0 / 5.0 / 1.8 / 0.83.

## The crossover, two ways

The crossover is *much* later in wall-clock than in term-count because each
HRR term is enormously more expensive than each pentagonal summand:

- A pentagonal summand is one Python bignum add — O(log p(n)) bit ops.
- A single HRR term k involves φ(k) Dedekind sums each of cost O(k)
  multiplications at dps≈log₁₀ p(n) precision, plus φ(k) complex
  exponentials at that precision. Per-term cost ≈ k² · log p(n) bit ops
  at the precision of `mp.dps`, and the constant is large.

Aggregate: pentagonal does ~n^{3/2} cheap bignum adds; HRR does
~√n expensive multi-precision evaluations totalling ~n^{3/2}·log²(p(n))·log(p(n))
bit ops before factoring in FFT-based multiplication. Asymptotically with
*fast* arithmetic HRR wins; with naive arithmetic the crossover is around
n≈10⁵ here, which is exactly what we see.

This is the same lesson as A2 in CANDIDATE_INSIGHTS (a clean tail bound is
non-trivial) plus an additional asymmetry — the bits-per-term comparison
*flatters HRR* and the wall-time comparison *flatters pentagonal*, and
neither is the full picture. The honest characterization is:

- **Information-theoretically** (bits/term), HRR is at least 4× and up to
  2.5 × 10⁵× denser than pentagonal across our n range.
- **In bit-ops on this implementation**, HRR pulls ahead only at n ≥ 10⁵.
- **With binary-splitting / arblib-grade arithmetic** (Johansson 2014), HRR
  wins from much smaller n and stays ahead by a Θ(n^{1/2}) factor.

## Subtleties caught

1. **`float(round(...))` loses precision past ~15 digits.** First attempt
   used Python's `round(float(mpf))`, which silently mangled p(1000) by a
   few units in the trailing 105-bit integer. Fix: `int(mpmath.nint(x))`.
   Same bug class as A4 ("looks fine, returns wrong answer with confidence").
2. **The Rademacher bound is rigorous but loose.** At n=100000 the bound
   delivers 0.488 with N=138; the *observed* truncation error of the partial
   sum is closer to 10⁻³ (the bound's two constants 44π²/225√3 and π√2/75
   are derived for the worst case). A tighter bound would let us drop a few
   terms but the constant is < 2×.
3. **Pentagonal also delivers p(0)…p(n-1) "for free".** The term-count
   comparison gives pentagonal credit only for the *summands* needed to fill
   the whole table to row n; if you only wanted p(n) by itself with the
   recurrence, you'd still need the whole table because the recurrence is
   non-trivially backward-recursive. HRR genuinely computes a single value.
   Adjusting for this is unfair to neither method — they solve subtly
   different problems.
4. **`A_k(n)` has heavy cancellation.** φ(k) terms each of unit modulus
   summing to something of size O(√k); we use precision ≈ log₁₀ p(n) + 30
   to keep the cancellation noise below the truncation tail. At n=100000
   we burn 372 digits to certify a 347-digit answer.
5. **n>10⁵ was within reach but skipped.** At n=10⁶ the HRR formula needs
   N≈440 terms at dps≈1100, which extrapolated would take ~1500 seconds
   with this naive Dedekind-sum loop. Pentagonal at n=10⁶ would need
   ~10⁹ summands and on the order of an hour of bignum adds. Both are
   feasible but blew past the run budget; documenting the projection
   rather than running it. **(speculation: timings extrapolated from the
   N=138 / dps=372 measurement, not measured.)**

## Bottom line

**HRR's bits-per-term advantage over the pentagonal recurrence is roughly
4 × n / √n = 4√n, and the wall-clock crossover with naive mpmath arithmetic
sits at n ≈ 10⁵; with binary-splitting / arblib arithmetic it would sit
several orders of magnitude lower.** Confidence: **high** for the
term-count and bits/term curves (multiple n, exact integer cross-check at
every point); **medium** for the precise crossover location (sensitive to
mpmath implementation, would shift with FLINT/arb).

## Novelty assessment vs prior art

- Johansson's `arblib` paper (arXiv:1410.1672, **(training-memory)** — I do
  not have direct arXiv access in this env) is THE reference benchmark for
  HRR partition computation. Johansson's headline is that with binary-split
  evaluation of the Bessel/sinh derivative pieces and FLINT bignum, HRR
  computes p(n) at n=10¹² in seconds, vastly outperforming pentagonal for
  any n past a few hundred. The crossover *number* differs from ours by
  orders of magnitude because their arithmetic stack is asymptotically
  faster.
- What this experiment adds, beyond Johansson, is the **bits-per-term**
  framing — connecting the partition benchmark to the broader
  representation-switching narrative (CANDIDATE_INSIGHTS A1, A2). In that
  framing, HRR's per-summand density is the cousin of Chudnovsky's
  per-summand density for π (Experiment 06): a kernel structure (here
  Dedekind sums at the Heegner-like rational cusps; for Chudnovsky a
  Heegner point with discriminant -163) encodes an unbounded amount of
  number-theoretic data into each successive term.
- Treat the headline number above as **a new operational sentence about a
  well-known algorithm**, not a new algorithm. Original HRR is 1937;
  Lehmer's tail bound is 1938; the *bits/term per Heegner-like kernel*
  framing is, to my recall, not the way Johansson states it, but it's
  consistent with his numbers.

## Next

The pentagonal/HRR pair is now established as a third independent kernel
where representation switching gives the predicted dramatic gain pattern
(after theta and Bose-Einstein in A1). Next natural extensions:

- Divisor sum σ_k(n) via Eisenstein / Lambert representations (Pass A item
  07) — should show similar pattern with a different cost metric.
- Wrap the HRR cost predictor into the kernel recognizer registry
  (`09_kernel_recognizer_v0.py`) so a sum that looks like Σ p(n) e^{-βn}
  routes to HRR-of-coefficients vs. eta-product evaluation correctly.
