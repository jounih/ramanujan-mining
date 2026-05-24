# Diary 37 — Generalized obstruction principle: 3rd confirming instance (Riemann-Liouville + quartic confinement)

**Date:** 2026-05-24 (late evening, after diary 35 + 36)
**Source:** ChatGPT Pro response to Prompt 3 from the v0.8a follow-up
("Generalized obstruction principle on a 3rd bridge"). Same Erdős-style
prompt design.
**Status:** Generalized obstruction principle now at HIGH CONFIDENCE with
3 independent confirming instances. Promoted from §E candidate to §A
substantiated claim.

## What was tested

The B1.5 closure (diary 35) used Caputo time-fractional FPE with
harmonic confinement. We asked: does the obstruction generalize to a
THIRD setting — Riemann-Liouville time-fractional FPE with quartic
confinement?

If yes → 3 confirming instances strengthens the generalized principle.
If no (counterexample) → the principle is narrower than we thought;
identifies what fails.

## Verdict (ChatGPT Pro)

**(A) Constructive confirmation.** For probability-conserving RL
time-fractional FPE with scalar time kernel and quartic confinement,
the equilibrium partition function is STILL σ-independent:

```
Z_σ(β) = Z(β) = Γ(1/4)/√2 · β^(-1/4)
R_σ(β) = ∂_σ log Z_σ(β) ≡ 0
```

Same one-line spectral argument as B1.5:
- The standard RL fractional FPE is `∂_t ρ_σ = ₀D_t^{1-σ,RL} L_β ρ_σ`
  (Baeumer-Meerschaert form with the initial-condition source term
  `ρ_0 · t^{-σ}/Γ(1-σ)` that protects the zero mode).
- For the equilibrium density `ρ_eq,β(x) = e^{-β·x⁴/4}/Z(β)` (Boltzmann
  form, σ-independent), the RL source EXACTLY cancels `₀D_t^{σ,RL} ρ_eq`.
- The functional calculus commutes with spectral projections of L; the
  n=0 mode is fixed pointwise since `E_σ(0) = 1`.
- Quartic potential only changes the nonzero spectrum and the
  non-Gaussian form of `φ_0`; it does NOT turn `λ_0 = 0` into a
  σ-dependent object.

The "pure RL without initialization" variant (which doesn't conserve
mass) gives `Z_σ^{pure RL}(β,t) ∝ t^{σ-1} · Z(β)` — a time-dependent
scaling, not a β-spectral deformation. Cannot match Berndt-Dixit's
reciprocal-symmetric BD_int(α). So no rescue.

## Sharp principle statement (refined from diary 35)

After 3 instances:

> **Scalar time-only functional calculus of a Fokker-Planck-type
> generator L preserves ker L (the equilibrium sector).**
>
> Therefore, any Mellin-pair-style reciprocal-symmetric spectral object
> (Watson M(α), Berndt-Dixit BD_int(a), etc.) cannot be matched by a
> functional of L's equilibrium partition function under such a
> calculus, because the equilibrium sector is fixed pointwise while the
> reciprocal object lives in a non-trivial class.

The 3 confirming instances:
1. **B1**: modular S-transform on lattice-gas g* vs Watson M(α) —
   closed via 20 candidates × 5 families failing (diary 19)
2. **B1.5**: Caputo time-fractional FPE (harmonic) vs Berndt-Dixit
   BD_int(α) — closed via 1-line argument (diary 35)
3. **NEW**: RL time-fractional FPE (quartic) vs Berndt-Dixit
   BD_int(α) — closed via 1-line argument extended with RL
   initialization handling (this diary)

## What actually WOULD break the principle (ChatGPT-identified)

This is the most interesting part of the answer — it sharpens the
principle by identifying the precise boundary:

**The principle requires SCALAR TIME-ONLY functional calculus.** If the
anomalous exponent or memory kernel depends on SPACE, the calculus no
longer commutes cleanly with the FPE generator, and the
Gibbs-Boltzmann stationary measure can fail. ChatGPT cites:

- **Fedotov-Falconer**: space-dependent anomalous exponent →
  Gibbs-Boltzmann is NOT the stationary solution for such variable-
  order subdiffusive equations.

This is a **genuine route to a B-type counterexample**. If the bridge
holds for space-dependent variable-order subdiffusion, then the
Berndt-Dixit reciprocal structure could be matched by some functional
of `Z_σ(β)` because `Z_σ` would no longer be σ-trivial.

## Implications

### Closures + promotions

- **Generalized obstruction principle PROMOTED** from §E candidate
  (medium-high, 2 instances) to §A substantiated (high, 3 instances
  with sharp scope statement). See `insights/CANDIDATE_INSIGHTS.md §A8`
  (new).
- **DID_NOT_PAN_OUT §R18** records the closed B1.5-style "fractional
  FPE bridge attempts" speculation (refuted across Caputo-harmonic and
  RL-quartic both).
- **`analysis/25_w7_fractional_bridge_v0.py`** remains obviated.
- **W7 paper draft** scope sharpens: the short note's headline becomes
  "scalar time-only fractional calculus of FPE generators preserves
  equilibrium; reciprocal-class objects cannot bridge". The
  Fedotov-Falconer counterexample territory becomes the natural §6
  open-direction.

### New open direction (HIGH novelty)

**Hunt 7 candidate (NEW)**: test the obstruction principle on
**space-dependent variable-order subdiffusion** (per Fedotov-Falconer).
If R_σ(β) is NOT identically zero in that setting, the Berndt-Dixit
αβ=1 reciprocity might bridge to it. Specifically:

- Setup: 1D variable-order fractional FPE with `σ = σ(x)` — e.g.
  `σ(x) = σ_0 + ε·x²` for small ε; harmonic OR quartic confinement.
- Compute: `Z_σ(β)` (likely no longer Boltzmann) at multiple
  (σ_0, β) cells via spectral or Monte Carlo.
- Test: does `R_σ(β) = c · BD_int(α(σ,β))` hold for some scaling map?

Going-in confidence: maybe 30-40% positive. Higher than B1.5's 10-15%
because the space-dependent case is genuinely different — the
zero-mode-protection argument breaks down. The Fedotov-Falconer
literature provides the analytical machinery.

**This is a publishable Hunt** if it lands either direction.

## Methodology — Erdős-style prompt cycle works (3rd validation)

We now have 3 cases where a single ChatGPT-Pro Erdős-style prompt
produced a high-quality, project-advancing result:

1. **v0.8a proposer-test** (Bose-Einstein log-partition formula) →
   confirmed v0.8b's identities + identified the Stieltjes/Lambert
   occupation-number identity as a v0.8c gap.
2. **B1.5 fractional bridge** → falsified with 1-line structural
   argument.
3. **3rd-bridge generalization** (THIS diary) → confirmed the
   principle's scope sharply + identified Fedotov-Falconer as the
   genuine-counterexample territory.

Cycle time: ~10 min prompt design + ~3 min model response + ~30 min
verification/integration. The pattern is now a validated research
workflow alongside our own subagent-based work. ChatGPT-Pro plays the
"frontier-LLM external collaborator" role well for sharp T/F questions
with clear verification paths.

## Bottom line

**Generalized obstruction principle established at high confidence across
3 structurally-different instances** (modular cohomology, Caputo
fractional, RL fractional). Sharp scope: scalar time-only functional
calculus of FP-type generators preserves ker L. Counterexample
territory identified: space-dependent variable-order subdiffusion
(Fedotov-Falconer). New Hunt 7 candidate scoped for future work.

**Confidence**: high on the principle (3 confirming instances, 2 with
clean structural arguments, scope characterized sharply). Medium on the
Fedotov-Falconer counterexample direction (literature exists; need to
do the calculation to know if BD bridge applies there).

## Follow-up leads

1. **CANDIDATE_INSIGHTS update** — add §A8 entry for the obstruction
   principle as substantiated.
2. **DID_NOT_PAN_OUT update** — R18 entry for the closed "fractional FPE
   bridge" speculation (covering both B1.5 Caputo-harmonic and the
   RL-quartic confirmation).
3. **W7 paper draft restructure** — short note on subordination
   obstructions with Fedotov-Falconer as the open frontier.
4. **Hunt 7 scoping** — design the variable-order subdiffusion
   experiment (1-2 day script + paper-length writeup if positive).
5. **HUNT_MAP update** — add Hunt 7 to the active hunts section,
   credit ChatGPT-Pro for the lead.

## Cross-link

- diary/19 — B1 closure (cohomological irreducibility)
- diary/35 — B1.5 closure (Caputo + harmonic)
- this diary (37) — 3rd-bridge confirmation (RL + quartic)
- diary/31 — v0.8b additive-correction API (related but separate work)
