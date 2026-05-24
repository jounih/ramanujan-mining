# Diary 08 — Divisor sum σ_k: direct vs Möbius vs Lambert/Eisenstein

**Date:** 2026-05-24
**Source:** experiment 07 (`analysis/07_divisor_sum_methods.py`, CSV
`analysis/results/divisor_sum_methods.csv`)
**Status:** Pass A item 07 complete. Third independent kernel substantiates
the central RKC representation-switching hypothesis, this time on a
*number-theoretic* (Lambert / Eisenstein) rather than an analytic (Gaussian
theta, Dedekind eta) kernel.

## Setup

The arithmetic divisor sum

    σ_k(n) = Σ_{d | n} d^k

admits three natural evaluation routes:

| code | route | per-call cost | comments |
|------|-------|---------------|----------|
| A | DIRECT — trial-divide enumerate divisors of n, sum d^k | O(√n) probes | each probe is one big-int `%` |
| B | MÖBIUS — factor n = ∏ p_i^{a_i}, apply σ_k(n) = ∏ (p_i^{k(a_i+1)} − 1)/(p_i^k − 1) | dominated by factoring | small const factor better than A because once a prime is extracted we apply the closed form |
| C | LAMBERT/EISENSTEIN — for a batch σ_k(1..N) at once, sieve the divisor-sum generating function Σ_{n≥1} n^k q^n/(1−q^n) = Σ σ_k(m) q^m | O(N · H_N) for the whole batch ≈ O(N log N) | amortized O(log N) per output value |

The third row is the "switch": σ_k is the q-coefficient of the Lambert
series, which for k ≥ 1 is (up to constants) the Eisenstein series
E_{k+1}(q). The "switch" is at the generating-function level — evaluate
Σ at the kernel q rather than per-n at the kernel d. Same conceptual move
as theta-dual (exp 02) and Dedekind-eta-S (exp 04), only here the
representation is a power series in q rather than an analytic functional
identity.

## Ops accounting (defensible)

I count inner-loop iterations, NOT big-int multiplies (those depend on k
and on the magnitude of intermediate divisors). Specifically:

- Method A op = one trial-divide probe `n % d` for d ∈ 1..⌊√n⌋.
- Method B op = one trial-divide probe in the factoring loop (~ O(√n) in
  the worst case, but in practice O(distinct small primes) for n up to 10^9).
- Method C op = one `sigma[m] += n**k` update in the sieve, i.e., one
  Lambert cell write. Total = Σ_{n=1..N} ⌊N/n⌋.

This count is *k-independent* by construction: the big-int width of `n**k`
or `d**k` affects wall-time but not the op count. That's deliberate. The
op count is what generalizes to other counting modules; wall-time is the
practical headline.

## Numbers

### Single-call A vs B

For one σ_k(n):

| n | A ops (≈√n) | B ops (probes during factoring) | B/A |
|---|---:|---:|---:|
| 10 | 3 | 1 | 0.33 |
| 100 | 10 | 6 | 0.60 |
| 10⁴ | 100 | 10 | 0.10 |
| 10⁶ | 1,000 | 14 | 0.014 |
| 10⁹ | 31,622 | 20 | **6.3 × 10⁻⁴** |

B/A drops monotonically because Method A always pays √n while Method B's
work scales with the *largest prime factor* of n. For n = 10⁹ (= 2⁹ · 5⁹),
B finishes in 20 probes vs A's ~31k. Wall-time follows: 5 μs vs 1.5 ms,
a ~300× speedup at n = 10⁹. The exponent k is irrelevant to the op count
(it enters only as a single big-int power per accepted divisor / prime).

### Batch A summed vs C amortized

For σ_k(1..N) all at once:

| N | A summed ops | C sieve ops | C/A |
|---|---:|---:|---:|
| 100 | 625 | 482 | 0.77 |
| 1,000 | 20,615 | 7,069 | 0.34 |
| 10,000 | 661,750 | 93,668 | 0.14 |
| 100,000 | 21,032,170 | 1,166,750 | **0.056** |

Wall-times in seconds at N = 100,000: A ≈ 0.82 s, C ≈ 0.10 s (≈ 9× faster).
The asymptotic ratio is C/A ∼ (N log N) / (N · √N) = (log N) / √N, which
matches: at N = 10⁵, log(10⁵)/√(10⁵) ≈ 11.5 / 316 ≈ 0.036, the predicted
ratio is sub-6%, observed 5.55%, within the constant-factor tolerance.

### The crossover N*

Counting probes one N at a time:

- N* = **41** is the first N at which Σ_{n=1..N} ⌊N/n⌋ < Σ_{n=1..N} ⌊√n⌋,
  i.e., the first N at which C beats A in op count.
- N** = **43** is the first N from which C *stays ahead* for 50+ consecutive
  N (there's a sporadic re-tie at N = 42 because both functions step by
  small integer amounts).

Practical takeaway: **for any batch with N ≥ 50 or so, prefer the Lambert
sieve.** Below that, the per-call O(√n) trial-division is already cheap
enough that the sieve's overhead (allocating an N-length list, writing
to it) is not justified.

## Why C wins for batches — the kernel-switch lens

The same pattern shows up across exps 02, 04, 07:

| exp | kernel | naive route | switched route | gain mechanism |
|-----|--------|-------------|----------------|----------------|
| 02 | Gaussian Σ e^{-βn²} | direct n-sum | theta-dual (Poisson) | small β → fast decay in dual |
| 04 | partition Π(1−e^{-βn})⁻¹ | direct product | Dedekind-η S-transform | small β → fast decay in dual product |
| 07 | divisor σ_k(m) | per-m trial divide | Lambert q-series sieve | batch reuses each n across all multiples |

In every case the switched route *amortizes shared structure* (Fourier mode
overlap; modular S-symmetry; divisor lattice membership). The naive route
recomputes that structure independently per output. For σ_k this is most
explicit: in Method A we discover that 6 = 2·3 by probing 6 separately
from 12, 18, …; in Method C we visit each (n, m) pair exactly once across
the whole batch. The Lambert / Eisenstein identity is the formal name for
"don't rediscover divisibility per query."

## Honest caveats

1. **k-dependence in wall-time.** At k = 5 and N = 10⁵ the per-coefficient
   integer width is meaningful (`σ_5(N)` is ~30 decimal digits at N = 10⁵);
   the big-int adds inside C still dominate the timing. C is the right
   route but a future RKC must account for `k · log N` bit-width in the
   cost model, not just op count. (Confidence: high. The wall-time / op
   ratio in C grows ~linearly with k as expected.)
2. **B's "factoring is cheap" assumption.** Trial-division factoring is
   O(√n) worst case, the same class as A. B beats A by a *constant
   factor* (~10×–500× on the n grid tested) but is not asymptotically
   faster on adversarial inputs (e.g. n = pq with p, q ~ √n). For
   cryptographic n where factoring is the bottleneck of B, the table
   flips — A wins. (Confidence: high.)
3. **Memory for C.** Method C allocates an N+1-length list. At N = 10⁵
   this is trivial; at N = 10⁹ the list itself is ~8 GB of pointers and
   the method becomes infeasible without a streaming variant. Not measured
   here. (Confidence: speculative for N > 10⁶; not tested.)
4. **No GC surprises observed.** Wall-time scaled with op count within
   ~10% across all batch cells, suggesting interpreter / allocator
   overhead is not dominant. The op count is a faithful proxy. (Confidence:
   medium — single run, no per-run variance estimate.)

## Bottom-line claim

**For evaluating σ_k as a batch of size N ≥ 41, the Lambert/Eisenstein
generating-function sieve dominates per-element trial division by a factor
that grows like √N / log N. The crossover is at N* = 41 (op count),
empirically stable from N** = 43.** Confidence: high (numbers reproduce
exactly; op counts derived from a closed expression Σ ⌊N/n⌋ vs Σ ⌊√n⌋
match the experimental count).

A registry-driven RKC should recognize "request batch of σ_k values" as a
distinct call signature from "request single σ_k(n)" and route them
differently. Currently the recognizer (exp 09) treats only single
expressions; extending it to *call-signature-aware* routing is a natural
next step.

## Speculation (tagged)

*Speculative:* the Lambert-sieve pattern is the discrete analog of the
theta-dual / eta-S pattern: in all three cases the "switch" is a
generating-function evaluation that bundles together what the naive
route would visit element-by-element. If true, the right abstraction
for an RKC kernel registry entry is not "(direct form, dual form)" but
"(per-query form, batch-generating form, amortization rule)." The
"amortization rule" tells the planner the break-even N. For σ_k that
rule is N* ≈ 41; for sums Σ e^{-βn²} over a batch of β values the
analogous rule has not been measured here and is a candidate for a
follow-up experiment.

## Next

This closes Pass A item 07. Item 05 (Hardy–Ramanujan–Rademacher exact
p(n) bits-per-term) and item 08 (class invariants G_n) remain.
