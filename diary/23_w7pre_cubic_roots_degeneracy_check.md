# Diary 23 — W7-pre: QR II §3 cubic-roots check for Gauss-sum degeneracy awareness

**Date:** 2026-05-24
**Source:** Berndt 2022 HRJ reproduction of QR II §3 (lines 2086-2280 in
`chatgpt-pro-mining/.../priority_sources/quarterly_reports/ramanujan_quarterly_reports_2022_HRJ_Berndt.txt`).
**Status:** Closed. Verdict: NEGATIVE — Ramanujan's text shows no
explicit awareness of the cube-roots-of-unity-analogue silent-zero
hazard.

## The test

Per [todo.md W7-pre](../todo.md) and the connection flagged in the parallel
review: QR II §3's cubic-roots-of-unity multisection is the same operator
family as the **Gauss-sum silent-zero hazard at q ≡ 2 (mod 4)** that the
recognizer guards against
([CANDIDATE_INSIGHTS §A4](../insights/CANDIDATE_INSIGHTS.md)). Question: does
Ramanujan, in QR II §3, mention or implicitly guard against the cubic-roots
analogue (when the target function has no `n ≡ 0 (mod 3)` terms, the
averaged sum vanishes silently)?

If yes → bibliographic evidence that the silent-zero hazard was in
Ramanujan's working knowledge, strengthening §A4 as "a modern engineering
catch that Ramanujan also knew".

If no → consistent with §A4 being a modern observation. Effort: ~30 min.

## What Ramanujan does (lines 2086-2280)

The setup: solve the transcendental equation

```
1 - x³/3! + x⁶/6! - x⁹/9! + x¹²/12! - ··· = 0.
```

His method:

1. **Recognise the LHS as a multisection** of the exponential series:
   `1 - x³/3! + x⁶/6! - ··· = (e^(-x) + e^(-xω) + e^(-xω²)) / 3`, where
   ω = e^(2πi/3), ω² are the primitive cube roots of unity. This is the
   standard roots-of-unity filter for extracting `n ≡ 0 (mod 3)` terms.
2. **Simplify the RHS** using ω + ω² = -1 and ω² = ω̄: get
   `(e^(-x) + 2 e^(x/2) cos(x√3/2)) / 3`.
3. **Set to zero**: `cos(x√3/2) = -(1/2) e^(-3x/2)`.
4. **Locate roots** geometrically (intersections of cos curve and exponential)
   near `x = πn/√3` for odd n.
5. **Perturb**: write `x = πn/√3 - z`; substitute; solve for `z` as a power
   series in `h = e^(-πn√3/2)` using his Lagrange-inversion (from QR II §1).
6. **Final series**: `x ≈ πn/√3 - z(h)` where `z(h)` is given as an explicit
   alternating series in `h` with rational coefficients.

This is correct and elegant. The multisection trick is used cleanly.

## What he does NOT say

He does not mention the degeneracy case. The cube-roots-of-unity multisection

```
F_k(x) = (1/3) [f(x) + ω^{-k} f(ωx) + ω^{-2k} f(ω²x)]
```

is the projection of `f` onto its `n ≡ k (mod 3)` Taylor coefficient
sub-series. When `f` has NO `n ≡ k (mod 3)` Taylor coefficients (e.g.
`f(x) = x` with `k = 0`), `F_k(x) ≡ 0` identically — the "silent-zero
case" for the cubic multisection.

In Ramanujan's worked example, `f(x) = e^(-x)`, which has ALL Taylor
coefficients present (n = 0, 1, 2, 3, ...), so the `k = 0` projection
`F_0(x) = 1 - x³/3! + x⁶/6! - ···` is non-trivial. Degeneracy doesn't
arise. **Ramanujan happens to apply the operation to a safe case and
makes no commentary about edge cases.**

There's no implicit guard either — no condition like "provided f has
non-zero n ≡ 0 (mod 3) coefficients" or "this method fails if f is
linear in x". He just applies the trick and moves on.

## Verdict

**NEGATIVE on the bibliographic-evidence question.** QR II §3 does NOT
show Ramanujan flagging the silent-zero hazard for the cube-roots-of-unity
multisection. He applies the operation correctly in a regime where it's
safe; no commentary on when it would not be safe.

This is consistent with §A4's silent-zero-at-q-≡-2-mod-4 hazard being a
**modern engineering catch** rather than a re-discovery of a Ramanujan
caution. The recognizer's degeneracy detector is value-adding
independently; it is not validating a Ramanujan-was-aware-too claim.

## Why this matters (despite the negative)

Two implications:

1. **§A4 stands on its own merits** — the silent-zero detector is a real
   engineering contribution, not a re-statement of a known Ramanujan
   caveat. The "did not pan out" log shouldn't downgrade §A4; if
   anything this strengthens its novelty.

2. **The cube-roots-of-unity multisection is itself a separate operator**
   (`MULTISECTION_ROOTS_OF_UNITY` in
   [qr_section_index.json](../corpora/transcriptions/quarterly_reports/qr_section_index.json)
   §qr2_sec_3_cubic_roots). It fires ONCE in the QR corpus. The fact that
   Ramanujan applied it without commenting on edge cases is consistent
   with the §6.2 toolkit-split hypothesis interpretation: this is a
   *casually-used* technique, not one Ramanujan systematically developed
   with its own degeneracy theory.

## Honest caveat

I checked only the QR II §3 passage. Ramanujan may have discussed the
multisection-degeneracy case in his Notebooks (NB II perhaps), in his
problems for the *Journal of the Indian Mathematical Society*, or in
his letters to Hardy. A broader search across the Notebooks corpus
would be a Hunt-5b-style extension. Not in scope for this 30-minute
check.

## Bottom line

W7-pre **closes negative** with high confidence (for the QR corpus
specifically). The silent-zero hazard at Gauss sums q ≡ 2 (mod 4) per
[CANDIDATE_INSIGHTS §A4](../insights/CANDIDATE_INSIGHTS.md) is a modern
engineering contribution; not in Ramanujan's working knowledge as
evidenced by the QRs.

**Effort**: ~30 minutes as scoped. **Status**: closed. Updates the W7-pre
entry in [todo.md](../todo.md) to DONE.
