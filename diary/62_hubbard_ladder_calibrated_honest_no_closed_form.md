# Diary 62 — Half-filled 2-leg Hubbard ladder (t=U/4=t_⊥=1): calibrated-honest negative

**Date:** 2026-05-25
**Source:** ChatGPT-Pro response to a closed-form-ground-state-energy
prompt for the isotropic half-filled two-leg Hubbard ladder.
**Status:** **CALIBRATED-HONEST NEGATIVE** in the same class as ζ(5)
(diary 52), XXX (diary 52), Kepler (diary 54), figure-8 (diary 61).
ChatGPT explicitly refuses to fake a 6-digit number and explains
why none is available.

## The ask

Closed-form value for ground-state energy per site of the half-filled
2-leg Hubbard ladder at t = U/4 = t_⊥ = 1.

## ChatGPT's response (verbatim core)

> "No certified closed-form e_0(1, 4, 1) to 10⁻⁶ was obtained."

> "A six-digit number here would be false precision unless it came from
> high-accuracy DMRG/iDMRG/AFQMC or a new integrability result. My own
> finite-ladder exact-diagonalization sanity checks put the
> thermodynamic energy roughly near -0.70 per site, but not to six
> digits."

ChatGPT provided 8 exact finite-size diagonalization values (OBC and
PBC, L = 1 to 6 rungs) showing finite-size drift too large for even
10⁻³ accuracy in the thermodynamic limit.

## Why no closed form (ChatGPT's structural analysis)

1. **The 1D Hubbard chain IS exactly soluble** (Lieb-Wu 1968 via Bethe
   ansatz). t_⊥ = 0 limit is closed-form.
2. **The 2-leg Hubbard ladder is NOT known to inherit integrability.**
3. Weihong-Hamer-Oitmaa-Bursill rung-expansion series in
   x = t/t_⊥ converges only up to x ~ 0.6; the isotropic point has
   x = 1, outside the convergence region.
4. Noack-White-Scalapino DMRG treats the half-filled 2-leg ladder as
   a spin-gapped insulating ladder, not an exactly soluble model.

## Adjacent closed-form cells (ChatGPT's escape-hatch suggestions)

### Cell A: Weak-coupling symmetric ladder (SO(8) Gross-Neveu)

For U/t << 1, 0 < t_⊥ < 2t, the half-filled ladder flows under
weak-coupling RG to an integrable SO(8) Gross-Neveu field theory
(Lin-Balents-Fisher; Balents-Fisher). Gives universal IR structure
but NOT the absolute lattice ground-state energy.

### Cell B: Asymmetric Hubbard ladder U_1 = U, U_2 = 0

One Hubbard chain coupled weakly to one free chain. At t_⊥ = 0, both
are exact (Lieb-Wu + free). Second-order hybridization correction is
formal:

```
Δe_cell^(2) = -t_⊥² Σ_σ ∫ dk dω/(2π)² · G_Hub^1D(k, iω; U) · G_0(k, iω) + O(t_⊥⁴)
```

The 1D Hubbard one-particle Green's function is much more complicated
than the Lieb-Wu ground-state energy alone — not a clean six-digit
closed form without form-factor / TBA machinery.

## Why this matters methodologically

This is the **6th calibrated-honest result** in our 27-cycle run:
- ζ(5) Apéry-like (diary 52)
- XXX integrable chain (diary 52)
- Kepler equation (diary 54)
- M3 P_pq Lambert-series ζ(2k+1) variants
- Figure-8 three-body period (diary 61)
- **Hubbard ladder (this diary)**

ChatGPT correctly refuses to fabricate a number when it doesn't have
one. The methodology's true-positive filter continues to work — this
is what an honest negative looks like.

## What we learned

For physics-accelerator targets that ask for "closed form ground-state
energy of a strongly-correlated lattice model at the interacting
point", the answer will almost always be NO unless:
1. The model is exactly integrable (rare: 1D Hubbard yes; ladders/2D no)
2. The cell is in a weak-coupling regime mapping to a known integrable
   QFT (then it's universal IR only, not lattice e_0)
3. The cell is in a strong-coupling regime mapping to a known spin
   model (e.g., t/U → 0 Heisenberg)

The most productive future asks would be: (a) the integrable points
(1D Hubbard, t-J at U/J = 1, etc.); (b) controlled small-parameter
expansions around integrable points; (c) calibrated weak-coupling
field-theory IR (NOT lattice e_0).

## Strategic implication

**No new accelerator delivered. Calibrated-honest negative.** No
diary 55-style overclaim risk.

**Excitement:** 3/10 — useful refutation that bounds the methodology's
reach. NOT paper-grade.

**Confidence:** HIGH on the structural argument (the integrability
landscape of Hubbard ladders is well-mapped); HIGH on the finite-size
data showing the thermodynamic value sits broadly near -0.70.

## Tasks queued (none)

The honest verdict here is: don't keep prompting on this exact target.
If pursuing Hubbard physics, ask about Lieb-Wu integrable cells or
SO(8) Gross-Neveu IR matching, not the isotropic 2-leg ladder.
