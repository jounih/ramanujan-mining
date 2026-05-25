# Diary 65 - In-env verification of CsCl Madelung 42-shell erfc/exp form

**Date:** 2026-05-25
**Source:** Analysis 37 (`analysis/37_cscl_madelung_42_shell_verification.py`).
**Status:** **CONFIRMED.** ChatGPT-Pro's 42-shell formula from diary 63 is
numerically correct and the wall-clock speedup measured here is
4.17x vs the 1201-term 2D csch/sech baseline (ChatGPT-Pro
claimed 5.6x; our env may differ).

## Setup

- mpmath 1.3.0, dps = 80 throughout.
- Wall-clock: median of 5 trials with `time.perf_counter()`.
- Literature reference (39 digits, diary 63):
  `M_ref = -1.7626747730709883979356733206386442911705...`
- Independent Ewald reference computed by running the same proposed shell
  form at higher cutoff (n_max=96, N_max=384, dps=100) and re-rounding to
  dps=80. This gives a same-recipe consistency check but does NOT
  cross-validate the recipe itself; the cross-validation is the 1201-term
  Zucker-Glasser-style 2D csch/sech form below.

## Shell counts (n <= 24 / N <= 96)

- non-zero r3      shells: 21
- non-zero r3_odd  shells: 9
- non-zero h       shells: 12
- **total non-zero scalar shells: 42**

Diary 63 claimed 21 + 9 + 12 = 42. Matches.

## Results

| Method | Scalar terms | Value (rounded to 35 digits) | Abs error vs literature | Wall-clock median (ms) |
|---|---|---|---|---|
| Proposed 42-shell erfc/exp | 42 | `-1.7626747730709883979356733206386442` | 5.642e-35 | 5.629 |
| Current 1201-term 2D csch/sech | 1201 | `-1.7626747730709883979356733206386446` | 2.982e-34 | 23.471 |
| Independent Ewald reference (n<=96, N<=384, dps=100) | -- | `-1.7626747730709883979356733206386443` | 2.862e-41 | -- |

**Wall-clock ratio (1201-term / 42-shell):** 4.17x

**ChatGPT-Pro claim:** 5.6x.

## Verdict

**CONFIRMED.**

- Math: 42-shell form converges to literature reference within
  5.64e-35 (well below the 1e-30 threshold).
- Accelerator: 4.17x wall-clock vs the 1201-term 2D csch/sech
  baseline.
- The 42-shell formula is numerically correct, machinery is classical
  Ewald/Poisson, packaging is the small novel contribution claimed.

### Caveat on wall-clock platform sensitivity

The wall-clock speedup is sensitive to:
- mpmath dps (here 80; ChatGPT also at 80, so comparable).
- whether mpmath compiles its inner loops to gmpy2 / sympy bigints.
- per-call overhead of `mp.csch`, `mp.sech`, `mp.erfc`, and `mp.exp`.

The 28x scalar-term-count ratio (1201 / 42) is a property of the math and
is reproducible everywhere. The 5.6x wall-clock figure (or our
4.17x) is the realised constant on this platform; another machine
or another arbitrary-precision backend may see a different multiplier.

## Tasks queued

- **#76**: Update HUNT_MAP / CANDIDATE_INSIGHTS with this verification.
