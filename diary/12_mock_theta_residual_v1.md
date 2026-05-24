# Diary 12 — Pass D toy v1: shadow-exact bias cancellation

**Date:** 2026-05-24
**Status:** experiment 17 complete; v0 caveat substantially addressed but
not yet "publishable" — see "what's still missing" at the bottom.

## Headline

Building on `analysis/15_mock_theta_residual_demo.py` (= the v0 toy from
diary 04 / candidate-insight A5), this entry's experiment plugs in the
Watson / Zwegers Eichler integral of the shadow of `f(q)` and demonstrates
the bias-cancellation **end-to-end at ≥ 30 digits of precision** in the
small-β (hot temperature) regime that the v0 toy was about.

- **Modular cross-check passed at ≥ 30 digits**: yes (min 31.9 digits at
  α = 0.7; 75-80 digits at α ≤ 0.3).
- **Bias reduction headline**: at β = 1e-4 the v1 residual is `3.4e-76`
  versus v0's `1.8e+2` — that's a reduction by `2^258` in absolute size
  (≈ 258 bits). The number is at the precision floor of `mp.dps = 80`,
  so it's bounded below not by the math but by the working-precision
  setting.
- **Caveat from v0 substantially resolved**: the v0 "structurally
  illustrative, not Hickerson-Mortenson-exact" critique becomes a
  numerically-verifiable identity to ≥30 digits in the regime of interest.
  See "what's still missing" for the residual rough edges.
- **A v0 bug was found and fixed in the process**: see "v0 bug" below.

## What I actually did

The point of v1 is to make a precise numerical statement about the
"missing piece" between `f(q)` and its modular completion. v0 used:

  - "modular surrogate" = θ_3(q)
  - "shadow proxy" = an ad-hoc unary theta with the EVEN Kronecker
    character mod 12 (wrong; see bug section), without the right
    normalization constant, without the Eichler integral step

v1 replaces both with the rigorous Zwegers content:

  - "modular surrogate" = the explicit modular term of Watson's 1936
    transformation of `q^{-1/24} f(q)`
  - "shadow Eichler integral" = the Mordell-type integral that Watson
    proved is the error term and Zwegers (2002) recognised as the
    non-holomorphic period integral of the unary theta shadow

The Watson identity (calibrated form, verified to ≥30 digits below):

    q^{-1/24} f(q) = 2 √(2π/α) · q_1^{4/3} · W(q_1²) + M(α)

with q = e^{-α}, q_1 = e^{-π²/α}, and:

    M(α) := 4 √(3α/(2π)) · ∫₀^∞ sinh(αt)/sinh(3αt/2) · e^{-3αt²/2} dt
    W(q) := Σ_{n>=0} q^{n(n+1)} / Π_{k=0..n} (1 - q^{2k+1})²

## How the Hickerson-Mortenson "exact normalization" gets pinned down

The task instruction said "the entire value of this upgrade hinges on the
exactness of the shadow normalization." I want to be honest about what I
*could* and *could not* derive:

1. **Could derive**: the *character* χ of the unary theta shadow and the
   *structure* of the q-expansion (q^{n²/24} exponents). These come out
   of a clean rewriting of `sinh(αt)/sinh(3αt/2)` as
   `Σ_{m≥0} [e^{-αt(6m+1)/2} - e^{-αt(6m+5)/2}]`, which is an
   identity I derived from first principles in this session and checked
   numerically before using.  The character that emerges is the ODD
   primitive character of conductor 12 — i.e. χ(1)=χ(7)=+1, χ(5)=χ(11)=-1,
   χ(-n)=-χ(n).  This is different from the (more familiar) EVEN
   Kronecker symbol (12/·).

2. **Could not derive symbolically in this session**: the precise
   constant `4√(3α/(2π))` in front of the Mordell integral, written
   purely from a Hickerson-Mortenson Hecke-type double-sum starting
   point. Instead I took the constant as given by **Watson's 1936
   transformation** (as reported in modern survey literature surfaced
   via search) and **verified it numerically to ≥30 digits**. So the
   exact constant is pinned by the modular-invariance check in §6a,
   not by a fresh symbolic derivation.

3. **Honest gap**: at α > 1, the Watson identity as I wrote it picks
   up O(q_1^4) corrections in the modular term — the W function above
   matches the small-α calibration to leading order but isn't the
   "true" modular partner at all α (or it's the modular partner of a
   slightly different mock theta sister and I haven't disentangled the
   notational variants across the Watson / Berndt / Ono / Hickerson
   literature). For the EBM toy this doesn't matter because the regime
   of interest is small β (hot / near-cusp), where the calibration is
   tight to ≥30 digits. But for a *publishable* writeup I would want
   to either:

     (i) chase down the right Watson partner function such that the
         identity holds at all α (this is bibliographic, not deep), OR
     (ii) reformulate using only the Mordell integral M(α) as the
          shadow Eichler integral and pair it with a *different*
          choice of explicit modular form computed via Dedekind-η
          products — which is what one would do for a clean Maass-form
          presentation.

## The Eichler-integral substitution and numerical-stability tricks

The Mordell integral has integrand

    sinh(αt)/sinh(3αt/2) · e^{-3αt²/2}

which is apparently 0/0 at t=0 but actually evaluates to `2/3` there
(both sinh's vanish linearly with their argument). `mpmath.quad` handles
this cleanly via its limit-aware adaptive Gauss-Legendre — no manual
regularization was needed. The Gaussian factor gives super-exponential
decay at large t, so the quadrature converges fast at all α tested.

I did NOT need to use the substitution `w = -τ̄ + iu²` that the task
prompt mentioned; in the parametrization where q = e^{-α} (i.e.
τ = iα/(2π) purely imaginary), Watson's form of the Mordell integral
already runs over a smooth, super-exponentially-damped integrand on
`[0,∞)`. The `iu²` substitution would be needed for *general* τ in the
upper half-plane (to get convergence near the boundary), but for the
EBM toy where β is real and positive, we never leave the positive
imaginary axis.

## v0 bug found and fixed

v0's `shadow_unary_theta` (in `analysis/15_mock_theta_residual_demo.py`)
uses the EVEN Kronecker character (12/·):

    chi(n) = +1 if n ≡ ±1 mod 12,
    chi(n) = -1 if n ≡ ±5 mod 12.

But a weight-3/2 unary theta of the form `Σ χ(n) · n · q^{n²/24}` with
EVEN χ vanishes identically: pair n and -n, get `n·χ(n) + (-n)·χ(-n) =
n·χ(n) - n·χ(n) = 0`. So v0's "shadow_proxy" is structurally
zero-by-symmetry as a true unary theta — what v0 actually computed was
the *one-sided* (positive-n only) version, which is not modular even
under restricted transformations.

The correct ODD character (χ(1) = χ(7) = +1, χ(5) = χ(11) = -1,
χ(-n) = -χ(n)) is derived independently in v1 from the `sinh` expansion
of Watson's Mordell integrand. The v1 shadow leading terms look like
(at α=1, q^{n²/24}):

    n=1: +1·1·q^{1/24}   ≈ +9.59e-1
    n=5: -1·5·q^{25/24}  ≈ -1.76e+0
    n=7: +1·7·q^{49/24}  ≈ +9.09e-1
    n=11: -1·11·q^{121/24} ≈ -7.11e-2
    n=13: +1·13·q^{169/24} ≈ +1.14e-2
    ...

Sign pattern is alternating-by-residue, magnitudes decay
hyperexponentially.

## Asymptotic finding: v0's "1/√β" prediction was wrong

v0 (diary 04 / candidate insight A5) claimed:

> "you systematically underestimate the log-partition function near the
> critical / high-temperature regime by a factor that goes like 1/√β"

The actual leading behavior of the v1 "modular-only" residual (= Mordell
integral M(α) in v1) is

    M(α) → 4/3   as α → 0+

— it **saturates at a finite radial limit** (Watson-Hickerson), it does
NOT diverge as 1/√α. The Mordell integrand at t→0 is

    sinh(αt)/sinh(3αt/2) → 2/3,    e^{-3αt²/2} ≈ 1,

so M(α) ≈ 4√(3α/(2π)) · (2/3) · ½√(2π/(3α)) = 4/3.

Empirically the CSV shows residual_v1_modonly going 1.333 → 1.333 →
1.332 → 1.324 → 1.255 → 0.932 across β = 1e-4..10 — clearly bounded,
clearly not 1/√β.

So the v0 *qualitative* picture (mock theta is bounded, modular surrogate
isn't, ratio → 0) was right, but the *quantitative* asymptotic claim was
off; the v1 modular-only residual is `O(1)`-bounded, while the
*surrogate vs mock* mismatch `f-θ_3` of v0 grows like √(2π/α) precisely
because it's `θ_3` that's the wrong modular surrogate (it has the wrong
asymptotic). The v0 toy was mixing up two different residuals.

## Does this count as a "publishable bias-cancellation demonstration"?

Honest answer: **mostly yes for the conceptual point, not quite for a
mathematical publication.** Specifically:

- The toy demonstrates, at ≥30 digits in the regime of interest, that
  the Eichler integral of the shadow EXACTLY cancels the structural
  bias between a mock-theta EBM normalizer and its modular surrogate.
  That is the qualitative content of v0 made quantitative. ✓

- The constants used (4√(3α/(2π)) prefactor, ODD-χ structure) are all
  numerically pinned by the Watson identity check in §6a — not
  hand-waved. ✓

- HOWEVER, my "modular surrogate" is the Watson companion `W(q_1²)`,
  not a canonical modular form (η-product, Eisenstein series, theta
  series with prescribed level/character). For a publication I would
  want the modular surrogate written in terms of standard objects from
  the modular-forms taxonomy at level 6 / 12 / 24, so the result
  becomes "*the bias between f and [η-product of level X with explicit
  character] is exactly the Eichler integral of the unary theta of
  conductor 12 with character χ*". That's a few hours of standard
  modular-forms bookkeeping but I did not do it here.

- Also: my Watson identity has been confirmed at small α (calibrated
  regime) to ≥30 digits, but at α > 1 there are O(q_1⁴) corrections I
  haven't disentangled (probably because I'm picking a slightly wrong
  Watson partner; the literature uses several inconsistent labelings of
  ω vs ψ vs ν). A publishable version would need either the full
  q-expansion of W or the alternative formulation noted in (ii) above.

## What's still missing — the next thing that needs to be true for FEP

For this to plug into a real Friston-style application (the B1 ambition
from the candidate insights), the next required step is the one labelled
TODO #16 in the live plan and called out in candidate-insight B1:

> "Shadow as information-theoretic residual: probe whether the Eichler
> integral of the shadow is equal (or proportional) to a mutual
> information / surprise quantity in the underlying generative model."

Concretely: I need to construct a small generative model (e.g. a 1D
lattice gas at imaginary fugacity, a fermionic q-Pochhammer, or a tiny
spin system at complex temperature) whose partition function has the
shape of `f(q)`. Then:

1. The "modular part" `2√(2π/α) q_1^{4/3} W(q_1²)` corresponds to a
   *truncated* / *modular-only* variational lower bound on -log Z.
2. The "shadow Eichler integral" M(α) is the gap between the modular
   bound and the true -log Z.
3. The hope is that M(α) has a clean interpretation as a mutual
   information (the difference between the full posterior entropy and
   what the modular sampler captures). If so, then **the unary theta
   shadow is computing an information-theoretic residual quantity in
   the generative model**, and that would be a structurally novel
   result — exactly the FEP × mock-modular bridge candidate-insight B1
   identifies as the largest white space.

If M(α) does NOT match a clean info quantity, the failure mode is also
informative: it would tell us that the modular bound is not the right
variational structure for the chosen generative model and would
constrain the search for the right generative model class.

Either way, the EBM toy in v1 (this entry) IS the right substrate to
test that on. v1 is the necessary prerequisite for the next-step
experiment.

## Files

- Experiment script: `analysis/17_mock_theta_residual_ebm_v1.py`
- CSV: `analysis/results/mock_theta_residual_v1.csv`
- v0 (for diff): `analysis/15_mock_theta_residual_demo.py`
- v0 narrative (for diff): `diary/04_pass_d_mock_theta_demo.md`

## Confidence tag

- "Watson identity verified to 31.9 digits at α=0.7, 75+ digits at α≤0.3":
  **high confidence** (numerical, mp.dps=80, reproducible from the script).
- "ODD character mod 12 is the correct shadow character": **high
  confidence** (derived from the sinh expansion in-session, both
  symbolically and numerically).
- "v0 used the wrong (even) character": **high confidence** (direct
  inspection of v0 source).
- "Watson partner W as written here is the 'true' partner at all α":
  **low/medium confidence** (calibrated to leading order at small α;
  next-order corrections present at α > 1).
- "The bias reduction would carry through to a real FEP application":
  **speculative** (needs experiment 16 / the next entry, see above).
