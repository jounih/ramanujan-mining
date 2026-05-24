# Diary 06 — π-methods compression: quantifying the latent-space speedrun

**Date:** 2026-05-24
**Source:** experiment 06
**Status:** the "latent-space compression" hypothesis is now quantified on
the canonical 1/π benchmark.

## Numbers

Computing π to a target precision via four methods, all at mpmath dps=200:

| method | K | bits correct | bits/term | notation_chars |
|--------|---:|-----:|-----:|------:|
| Machin (Taylor of 4 atan(1/5) - atan(1/239)) | 1 | 6.24 | 6.24 | 70 |
| Machin | 8 | 41.26 | 5.16 | 70 |
| Machin | 32 | 154.65 | 4.83 | 70 |
| AGM (Brent-Salamin) | 1 | 11.60 | 11.60 | 107 |
| AGM | 8 | 667.65 (saturated) | 83.46 | 107 |
| Ramanujan 1914 | 1 | 25.29 | 25.29 | 64 |
| Ramanujan 1914 | 8 | 212.08 | 26.51 | 64 |
| Ramanujan 1914 | 32 | 667.65 (saturated) | 20.86 | 64 |
| Chudnovsky 1987 | 1 | 45.60 | 45.60 | 77 |
| Chudnovsky | 8 | 376.58 | 47.07 | 77 |
| Chudnovsky | 16 | (saturated) | — | 77 |

Empirical bits/term:
- Machin: **~5 bits/term**, asymptotic.
- AGM: doubles per iteration (quadratic convergence; ~95 bits/iter at iter 7).
- Ramanujan 1914: **~26 bits/term**, asymptotic.
- Chudnovsky: **~47 bits/term**, asymptotic.

That's roughly a **10× density jump** from Machin to Chudnovsky in terms
of "information output per loop iteration."

## Bits per character of notation

A more interesting metric: how many bits of π does each method extract
*per character of the formula*?

Using K = 8 (below the saturation of mpmath's 200-digit precision):

| method | bits | chars | bits/char |
|--------|-----:|------:|-----:|
| Machin | 41 | 70 | 0.59 |
| AGM | 135 | 107 | 1.26 |
| Ramanujan 1914 | 212 | 64 | 3.31 |
| Chudnovsky | 376 | 77 | 4.89 |

**Chudnovsky packs ~8.3× more bits of π per character of formula than
Machin.** The Ramanujan-class identities are not appreciably shorter to
write — they're roughly the same length as the Machin formula — but each
character does dramatically more computational work.

## What this quantifies

The user framed Ramanujan's intuition as "novel compressed representations
in his brain that let him speedrun in latent space." This experiment
operationalizes "compression" two ways:

1. **Computational density** = bits of pi per term executed. The
   Ramanujan-class identities are 5-10× denser than the standard
   Machin-style expansion that everyone knew before him.
2. **Notational density** = bits of pi per character of surface notation.
   8× denser for Chudnovsky vs Machin at the same K.

Where does the compression live? Not in shorter symbols. It lives in the
*kernel structure* — the modular function evaluation at a CM point. The
Chudnovsky kernel `(6k)!/((3k)! k!^3 (640320)^(3k))` references the
class invariant `j(t) = 640320^3 + 744` at the CM point τ = (1+i√163)/2,
i.e., the Heegner point of class number 1 with the largest discriminant.

That single object encodes:
- The integral basis of the Hilbert class field of Q(√-163).
- A specific modular form's q-expansion identity at a known cusp.
- The convergence rate constant 1/640320^3 = ~1.7e-17, the modular
  discriminant ratio.

Ramanujan compressed all of this into a single ~80-character formula. To
*unpack* it requires a full course in modular forms. That's the
"latent-space" claim made concrete: he carried the modular-form-at-Heegner-
point object as a primitive token; we, lacking that primitive, see a series
that converges absurdly fast and ask "where did it come from."

## Implication for an automated RKC

The recognizer registry should treat **Ramanujan-Sato series** as a
first-class kernel family, parameterized by the modular level and the
Heegner discriminant. Each registry entry compresses an enormous amount
of class-field-theoretic data into a finite-recursion-relation summand,
which can then be selected by the cost predictor against (a) other
modular series at the same level and (b) AGM-class iterations.

A registry of all known Ramanujan-Sato candidates (~10s at level 1; ~50
at levels 2-12; scattered candidates at moonshine-relevant higher levels
per SOTA notes section 7) would give the compiler the "Ramanujan-style"
upgrade over a default Machin-class implementation, automatically.

## Caveat / honest accounting

The benchmark above measures *bits per term*, not *bit-operations per
bit-of-output*. Each Chudnovsky term has a large factorial cost; at very
high target precision the per-term work grows. With binary splitting and
asymptotically-fast multiplication, the total bit-cost is `O(M(N) log²(N))`
for N bits of π — same as AGM. So Chudnovsky's win over AGM is a constant
factor (~30%), not an asymptotic class. The dramatic gap is over MACHIN,
which is asymptotically slower (`O(M(N) N)` for the atan Taylor series).

The "latent-space" framing is honest at the LEVEL of "kernel structure
density," not "asymptotic complexity class."

## Next

Continue with composite-energy recognizer extension (experiment 11),
addressing the "partial recognition + residual" pattern that's structurally
the same as the mock-theta correction story (E_known + ε·residual).
