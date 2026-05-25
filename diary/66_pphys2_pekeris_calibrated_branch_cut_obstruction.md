# Diary 66 — P-Phys2 Pekeris waveguide: calibrated-honest negative (branch-cut continuum is the obstruction)

**Date:** 2026-05-25
**Source:** ChatGPT-Pro response to P-Phys2 prompt (closed-form
acoustic propagation in 2-layer Pekeris waveguide vs PE-marching
solver). One of the 4 physics-accelerator prompts I drafted.
**Status:** **CALIBRATED-HONEST NEGATIVE** with a concrete escape
hatch. The exact O(K) replacement for PE-marching does NOT exist
for the radiating Pekeris (c₂ > c₁); the obstruction is precisely
identified as the branch-cut continuum from the radiating halfspace.
The trapped-mode part IS O(K) and useful as a fast approximate
primitive. 8th calibrated-honest cycle of the run.

## The verdict

> "For the radiating two-layer Pekeris waveguide, the requested
> exact O(K) evaluator does not exist in the usual finite-trapped-
> mode sense. The trapped-mode part is O(K), but the radiating
> lower halfspace leaves a continuous spectrum / branch-line
> integral. That branch term can be reduced to a clean
> one-dimensional real integral, and at large range to a
> lateral-wave asymptotic series, but not to a finite closed
> expression involving only the K trapped poles."

> "Exact O(K) evaluation is possible for trapped modes only; the
> radiating branch term prevents an exact finite O(K) formula."

## The structure ChatGPT provided

For the standard fluid Pekeris model with pressure-release surface
and radiating fast halfspace (c₂ > c₁), the exact field decomposes as

```
P(r, z; Ω) = P_modes(r, z) + P_br(r, z)
```

where:

**Trapped-mode part (O(K)):**
- K trapped modes at horizontal wavenumbers κ_m ∈ (k_2, k_1) satisfying
  q_m cos(q_m h) + η_m sin(q_m h) = 0
- For the benchmark cell (c_1=1500 m/s, c_2=1800 m/s, h=100 m, f=50 Hz):
  K=4 trapped modes computed
- P_modes = (i/4) · Σ_m φ_m(z_s) φ_m(z) H_0^(1)(κ_m r)
- Real O(K), cheap (~5.5 µs evaluation)

**Branch-cut part (continuous spectrum, NOT closed-O(K)):**
- P_br = (i/(2π)) · ∫_0^∞ [s² sin(q_s z_s) sin(q_s z) / (q_s² cos²(q_s h) + s² sin²(q_s h))] · H_0^(1)(α(s) r) ds
- Reduces to a clean 1D real integral but does NOT factor through
  finite K-trapped-pole evaluation
- At large range, leading lateral-wave asymptotic ~ exp(ik_2 r)/r²

## Numerical magnitudes at the benchmark

| Range | P_modes magnitude | P_br magnitude | Rel. err if branch omitted |
|---|---|---|---|
| 5 km | 3.9e-5 | 2.0e-8 | 5.25e-4 |
| 10 km | 2.8e-5 | 2.0e-9 | 1.84e-4 |
| 20 km | 6.1e-5 | 1.3e-9 | 2.15e-5 |
| 50 km | 4.7e-5 | 2.1e-10 | 4.51e-6 |

Branch term is small but NOT negligible for a 10-digit claim. For
~6-digit accuracy at long range (≥50 km), the trapped-mode-only
evaluator IS competitive (5 µs vs PE-marching's ~2 ms kernel = 360×
faster).

## Why this is calibrated-honest

ChatGPT explicitly refused to report a fake PE comparison:

> "I am not reporting a PE relative error because I did not run a
> converged PE solver with a matched source starter, bottom
> radiation/PML, Padé order, and convergence study. More
> importantly, the proposed object to compare against — an exact
> closed O(K) modal-plus-branch evaluator — does not exist in this
> radiating Pekeris case as a finite trapped-mode expression."

This is the methodology's true-positive filter working. ChatGPT
identified the precise structural obstruction (branch-cut continuum
from c₂ > c₁ radiation condition), cited the right literature
(Ocean Acoustics Library; Zhu and Lu on leaky modes), and refused
to overclaim.

## Escape hatch (the useful follow-up)

> "For a rigid bottom instead of a radiating halfspace, the branch
> cut disappears and a pure modal representation is possible."

This is the concrete next prompt: **rigid-bottom Pekeris admits the
O(K) closed form we asked for.** Worth re-prompting with that
constraint, which would likely yield a real accelerator (closed
modes-only formula for the rigid-bottom waveguide).

## Pattern: 8 calibrated-honest cycles of ~30

| # | Cycle | Domain | Obstruction |
|---|---|---|---|
| 19 | ζ(5) Apéry-like | Number theory | Koecher 1979 already has depth-2; pure depth-1 open |
| 20 | XXX integrable chain | Integrable physics | Lukyanov g³ closed; g⁴/g⁵ require fitted parameters |
| 22 | Kepler equation | Celestial mechanics | Branch-point geometry forces slow Bessel-Kapteyn |
| ?? | M3 P_pq Lambert series | Number theory | Specific structural class boundaries |
| 26 | Figure-8 three-body | Celestial mechanics | P(ξ) not algebraic / D-finite, only spectral surrogate |
| 27 | Hubbard ladder (isotropic) | Strongly correlated | Lieb-Wu doesn't extend to ladders |
| 28 | XXZ form factor | Quantum dynamics | Non-factorizing Bethe-ansatz kernel at interacting Δ |
| **29** | **Pekeris (this)** | **Underwater acoustics** | **Branch-cut continuum from radiating halfspace** |

All 8 honestly framed by ChatGPT. The model continues to refuse
fabrication when warranted. The 1 novel positive result (AB 4.2.3
corrigendum) is more trustworthy because the same model produces
calibrated negatives at the appropriate cadence.

## Strategic implication for the tool paper

The trapped-mode-only Pekeris evaluator (~5.5 µs, ~6 digit accurate
at long range, ~360× speedup vs PE-marching) IS a useful sub-primitive
for the tool paper IF framed honestly:

**"Fast approximate Pekeris evaluator: trapped-mode-only, valid
when branch contribution is negligible (long range, deep waveguide,
source/receiver well away from interface). Replaces PE-marching at
3-6 digit accuracy with ~360× wall-clock speedup."**

This is a candidate primitive (f) for the tool paper if we want to
add a 6th. Probably worth a small implementation + benchmark
follow-up.

## Tasks queued

- **#79**: Re-prompt ChatGPT-Pro for the rigid-bottom Pekeris case
  (the escape hatch). Likely yields O(K) closed form. ~1 cycle.
- **#80**: Implement trapped-mode-only Pekeris evaluator + benchmark
  in `rkc/acoustics/pekeris_trapped.py`. Verify the K=4 trapped
  modes at the benchmark cell match ChatGPT's table; verify the
  ~5.5 µs / ~360× speedup vs the simple PE-marching kernel. Add to
  tool paper as primitive (f) if confirmed.

## Bottom line

**Calibrated-honest. The full Pekeris O(K) replacement doesn't
exist. The trapped-mode sub-part does, and is potentially useful.**
The rigid-bottom escape hatch is the real next prompt if pursuing
this further.

**Excitement:** 4/10 — sub-primitive useful, full replacement
unavailable, escape hatch concrete.

**Confidence:** HIGH on the structural obstruction (Ocean Acoustics
Library + Zhu-Lu citations are sound; the radiating-halfspace branch
cut is a well-known mathematical feature of Pekeris).

## Cross-link

- [diary 61](61_figure_eight_three_body_period_calibrated.md), [62](62_hubbard_ladder_calibrated_honest_no_closed_form.md), [64](64_xxz_form_factor_pphys1_calibrated_negative.md) — other calibrated-honest cycles
- Companion to P-Phys1/3/4 prompts; P-Phys2 result documented here
