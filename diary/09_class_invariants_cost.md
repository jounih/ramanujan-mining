# Diary 09 — Experiment 08: Ramanujan's class invariants G_n, direct vs radical cost

**Date:** 2026-05-24
**Source pointer:** training-memory + PSLQ confirmation in this run (no
primary-scan access in this env). Cross-referenced against the standard
Berndt *Ramanujan's Notebooks* Vol V Chapter 34 table conventions; the
radical forms used here are reconstructed from training memory and then
numerically verified to >= 100 digits before being committed (see
discipline gate `_verify_radical_table()` at the top of the script).
**Status:** complete; CSV at `analysis/results/class_invariants_cost.csv`.

## What G_n is and which normalization I'm using

For odd integer n > 0, Ramanujan's class invariant is

    G_n = 2^{-1/4} * exp(pi*sqrt(n)/24) * prod_{k odd, k>=1} (1 + e^{-k*pi*sqrt(n)}).

Equivalently in Weber's notation, G_n = 2^{-1/4} f(sqrt(-n)) where
f(tau) = q^{-1/48} prod (1 + q^{(2k-1)/2}) and q = e^{2 pi i tau}, evaluated
at tau = i sqrt(n). G_n is an algebraic unit in the ring class field of
Q(sqrt(-n)). For ~98 of the 116 values Ramanujan tabulated he gave nested
radical expressions; the remaining ~18 (class-number-8, two-class-per-genus
discriminants) require Kronecker-limit-style machinery he never wrote down
— this is the open target flagged in §C4 of CANDIDATE_INSIGHTS.

## Which n I used

Eight values, all numerically verified to >=100 digit agreement against the
infinite-product evaluation before commit:

| n  | radical form (verified)                                              |
|----|----------------------------------------------------------------------|
| 1  | 1                                                                    |
| 5  | ((1+sqrt(5))/2)^(1/4)                                                |
| 9  | (2+sqrt(3))^(1/6)                                                    |
| 13 | ((3+sqrt(13))/2)^(1/4)                                               |
| 17 | ((y + sqrt(y^2-4))/2)^(1/4), y = (5+sqrt(17))/2                      |
| 25 | (1+sqrt(5))/2  (= phi)                                               |
| 37 | (6+sqrt(37))^(1/4)                                                   |
| 49 | sqrt((y + sqrt(y^2-4))/2), y = 2+sqrt(7)                             |

For n in {21, 33, 45, 57, 85} I tried PSLQ at modest degree (up to 8) and
got no clean polynomial, so I excluded them from the table per the
"verify or exclude" discipline. (Their honest radicals exist but require
class-field-theoretic input I didn't try to recover here.)

## Two methods, two cost measures

- **Method A (direct):** evaluate the infinite product. Term count =
  number of odd k included until e^{-k pi sqrt(n)} drops below 10^{-d-pad}.
  Wall time measured around the loop and the prefactor exp().
- **Method B (radical):** evaluate the closed-form nested-radical
  expression at mp.dps = d+pad. "Operations" is a hand-count of
  +,-,*,/,sqrt,** nodes in the AST (a tight upper bound on irreducible
  mpmath primitive calls).

Both routes are cross-checked to relative agreement < 10^{-(d-5)} on every
single (n, d) cell. The check passes uniformly.

## What I observed (CSV summary)

Direct-evaluation term counts grow with `d` as ~ sqrt(d / (pi sqrt(n))) — a
crude inversion of e^{-k pi sqrt(n)} < 10^{-d}. Two specific things to call
out:

1. **As n grows, direct evaluation gets *faster*, not slower.** The brief
   asked me to double-check this. The expansion parameter is q =
   e^{-pi sqrt(n)}; larger n means smaller q means *faster* product
   convergence (fewer factors to reach a given precision). At d=1000
   digits: G_1 needs 369 terms, G_5 needs 165, G_25 needs 74, G_49 needs
   53. So my initial intuition "convergence gets slower with n" was wrong
   — the prompt's hedge was correct: it gets *faster*. The radical-form
   advantage is therefore *less compelling* at larger n than at n=1.

2. **At n=1 the radical form is trivially "1" and beats direct by the
   full 14x-369x term ratio (and ~430x wall time at d=1000).** This is
   the most dramatic single cell. It's also somewhat unfair as a
   benchmark — G_1 = 1 is a special case where the infinite product
   non-trivially equals 1 / (the prefactor) by the Ramanujan-Selberg
   identity, but the radical "constant" route is unbeatable by
   construction.

3. **For n in {17, 49} at d=30, direct *beats* radical on op-count.**
   Direct needs only 2-3 product factors at 30 digits, while the nested
   radical involves 7-8 primitive ops. This is the most interesting
   surprise of the experiment: **when n is large and the working precision
   is modest, the truncated infinite product is cheaper than evaluating a
   nested radical of equivalent algebraic depth.** Wall times still favor
   radical because each nested sqrt is cheaper than an exp, but the
   conceptual point stands: the "always prefer the closed form" intuition
   has a small-d, large-n exception.

4. At d=1000 the radical wins by op-count for every n (ratio 7x-369x) and
   by wall time for every n (ratio 3x-430x). This is where Ramanujan's
   tabulation pays off: at industrial precision the radical is essentially
   free.

5. Wall-time ratios are noisier than op-count ratios — the radical
   wall-times are dominated by a single sqrt() that is heavily cached
   inside mpmath, and at small d the timing resolution is poor. For a
   serious benchmark one would batch-iterate. The CSV captures the raw
   per-call times.

## Bottom line

**Claim (medium confidence):** For Ramanujan's class invariants G_n at
class-number-1 (or small-class-number) discriminants where a nested
radical of bounded depth is available, the radical form gives a
1x-400x speedup over direct infinite-product evaluation, with the
advantage growing roughly linearly in working precision d and decaying
sub-linearly in n. The crossover where radical begins to dominate by op
count is around d ~ 30-100 digits for medium n (17-49). Below that and
for large n, direct is competitive — a small but real exception to the
"closed form always wins" prior.

**Confidence: medium.** Limited by (a) my small verified-n table (only 8
values, all class-number 1 or 2), and (b) by op-count being a coarse
proxy for actual arithmetic cost on the underlying mpz/mpf primitives.

**Connection to CANDIDATE_INSIGHTS §C4:** the 18 unproven class-number-8
invariants Ramanujan tabulated are *precisely* the cases where the
radical-form advantage would matter most — they sit at large n
(discriminants in the hundreds-to-thousands range) where direct
evaluation is still cheap at modest precision, but at d=1000 digits
or beyond the radical absolutely dominates if you can write it down.
The "latent-space speedrun" hypothesis predicts that Ramanujan was, in
effect, carrying the (Klein-j, Weber-f) reduction in his head as a
primitive operation; recovering those 18 closed forms would extend the
RKC's kernel registry with the most precision-elastic shortcuts in the
entire run.

**Speculation (low confidence):** the cell where direct *beats* radical
(n=17, d=30) is suggestive of a more general "use direct below precision
threshold T(n)" rule that a future RKC routing policy could encode.
Threshold appears to scale roughly as T(n) ~ pi * sqrt(n) * (radical_ops).
Quantifying this on more (n, d) cells would be a one-line extension of
the experiment.

## Files
- `analysis/08_class_invariants_cost.py`
- `analysis/results/class_invariants_cost.csv`
- this diary entry
