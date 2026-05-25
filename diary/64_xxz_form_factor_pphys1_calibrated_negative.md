# Diary 64 — P-Phys1 XXZ form-factor closed form: CALIBRATED NEGATIVE at interacting Δ

**Date:** 2026-05-25
**Source:** ChatGPT-Pro response to P-Phys1 prompt (one of the 4
physics-accelerator prompts I drafted earlier). Asked whether the
2-form-factor expansion of ⟨σ^z_x(t) σ^z_0(0)⟩ in the gapless XXZ
chain (|Δ| < 1) reduces to a closed form in classical special
functions, replacing TEBD/iTEBD time evolution.
**Status:** **CALIBRATED NEGATIVE at interacting Δ.** False except at
the free-fermion point Δ = 0. For interacting gapless XXZ including
Δ = 1/2, the two-spinon term has structure (exactly known by
Caux-Konno-Sorrell-Weston) but does NOT collapse to a finite closed
form in Bessel / hypergeometric / theta. ChatGPT identifies the
specific structural obstruction.

## The verdict

> "Verdict: False, except at the free-fermion point Δ = 0."

> "For interacting gapless XXZ, including Δ = 1/2, the two-spinon /
> two-form-factor term is exactly known, but it does not collapse to
> a finite closed form in Bessel, hypergeometric, theta, or similar
> classical functions for a real-space cell (x, t). The obstruction
> is not TEBD, and not the soft-mode asymptotics; it is the
> non-factorizing Bethe-ansatz minimal form factor plus the inverse
> Fourier transform over the two-spinon continuum."

## The closest exact object (ChatGPT's careful exposition)

The two-spinon contribution has the form

```
C^zz_2(x, t) = ∫∫ dβ_1 dβ_2 / (2π)² · F_ξ(β_1, β_2) · e^{i x (K_1+K_2) - i t (W_1+W_2)}
```

with

- Δ = cos(π/(ξ+1))
- K(β) = 2 arctan(e^β)
- W(β) = v_F / cosh β
- F_ξ(β_1, β_2) = [2(1+ξ^{-1})² · e^{-I_ξ((β_1-β_2)/2π)}] / [cosh β_1 cosh β_2 · (cos(π/ξ) + cosh((β_1-β_2)/ξ))]
- I_ξ(z) = ∫_0^∞ du/u · sinh((ξ+1)u)/sinh(ξu) · (cosh(2u) cos(4uz) - 1)/(sinh(2u) cosh u)

This is exactly the structure in Caux-Konno-Sorrell-Weston for the
2-spinon longitudinal structure factor.

## Why the integral doesn't telescope

After changing to spinon momentum p = K(β), the one-spinon phase
becomes the Bessel-friendly form e^{i xp - i t v_F sin p}. **But the
form factor becomes a coupling kernel**

```
A_ξ(p_1, p_2) = [2(1+ξ^{-1})² · exp(-I_ξ((log tan(p_1/2) - log tan(p_2/2))/(2π)))] /
                 [cos(π/ξ) + cosh((log tan(p_1/2) - log tan(p_2/2))/ξ)]
```

**This kernel is not constant, not finite-rank, and not a finite
Fourier/Mellin polynomial in p_1, p_2.** So the double integral does
NOT factor into a finite product or finite sum of Bessel-type
one-particle integrals.

At Δ = 0 (free fermions): kernel becomes trivial (no interaction);
the integral factorizes and gives the known closed-form free-fermion
correlator.

At Δ = 1/2 (ξ = 2): kernel = (9/2) · exp(-I_2(...)) / cosh(...);
non-factorizing.

## Tail-completeness caveat (also cited)

Even if we ACCEPTED the truncated 2-spinon expression as "the
closed form", it would NOT match a converged iTensor benchmark to
10⁻⁶ at Δ = 0.5:

- Integrated intensity saturation: 0.9869
- First-moment saturation: 0.9849

That's percent-level tail before real-time cancellations. **A 10⁻⁶
agreement cannot be certified from the 2-spinon term alone** —
needs 4-, 6-spinon contributions, each requiring their own
form-factor machinery.

## The clean obstruction

> "Bethe-ansatz rapidity-contour / minimal-form-factor coupling, NOT
> soft modes."

Soft modes give Luttinger-liquid threshold asymptotics. Form-factor
machinery can compute those asymptotics exactly (Kitanine-Kozlowski-
Maillet-Slavnov-Terras). But for finite (x, t), the non-factorizing
2-spinon continuum integral remains.

## What this tells us methodologically

P-Phys1 was the highest-ceiling of the 4 physics-accelerator prompts.
It came back NEGATIVE with a clean structural explanation. **This is
the methodology working correctly**:
- ChatGPT didn't fake a number
- Identified the specific structural obstruction (non-factorizing
  kernel)
- Cited the right machinery (Caux et al.)
- Distinguished free-fermion (works) vs interacting (doesn't)

**7 calibrated-honest cycles** now (ζ(5), XXX, Kepler, M3 P_pq,
figure-8, Hubbard ladder, XXZ form-factor) out of ~30 cycles. The
true-positive filter continues to work.

## Implications for the other 3 P-Phys prompts

- **P-Phys2 (Pekeris waveguide)**: still high-value. The closed form
  IS published (Pekeris 1948); the question is computational
  packaging. Should NOT come back negative.
- **P-Phys3 (Demkov-Kunike Magnus)**: classical 2F1 known for
  -∞→+∞; finite-T extension is the real ask. Possibly negative if
  no clean closed form for finite-T exists, but the math is much
  smaller than XXZ.
- **P-Phys4 (boundary-dissipated XX chain)**: Prosen's MPO exists;
  the magnetization-profile-only closed form is the ask. Possibly
  positive (XX is the easiest case).

## Tasks queued

None for P-Phys1. Move on to P-Phys2-4 if pursuing physics-
accelerator path.

**Cross-link:** [diary/61](61_figure_eight_three_body_period_calibrated.md)
(figure-8 calibrated), [diary/62](62_hubbard_ladder_calibrated_honest_no_closed_form.md)
(Hubbard ladder calibrated).

## Bottom line

**P-Phys1 came back as a clean structural negative.** No accelerator
delivered. But the methodology correctly identified WHY no closed
form exists at interacting Δ — the non-factorizing Bethe-ansatz
form-factor kernel.

This is informative-by-falsification: future XXZ-dynamics work
should focus on the soft-mode asymptotic (where form factors DO
give closed forms) or on specific Δ-values where additional
structure simplifies the kernel.

**Excitement:** 2/10 — useful negative.
**Confidence:** HIGH on the structural obstruction (the form-factor
machinery is well-established; the non-factorization claim is
provably correct given Caux et al.'s explicit kernel).
