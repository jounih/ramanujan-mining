# Diary 35 — B1.5 fractional-Fokker-Planck × Berndt-Dixit bridge FALSIFIED via single-line structural argument

**Date:** 2026-05-24 (late evening)
**Source:** ChatGPT Pro response to the Erdős-style open-T/F prompt
designed in this session (see prior conversation; prompt was the user's
"d" item from the (a,b,c,d) parallel execution request). The prompt was
modeled directly on the OpenAI Erdős unit-distance prompt structure
(open-ended T/F, anti-handwave guards, prior-surfacing, explicit
construction invitation).
**Status:** B1.5 falsified DECISIVELY. Pass D fully closed.

## Setup

Per [insights/BIG_IDEAS_REVIEW.md §3b](../insights/BIG_IDEAS_REVIEW.md)
and [insights/W7_BERNDT_DIXIT_WIRING.md §4-§6](../insights/W7_BERNDT_DIXIT_WIRING.md),
B1.5 was the conjecture that Ramanujan-Berndt-Dixit's αβ=1 Mellin-pair
reciprocity (Berndt-Dixit arXiv:0904.1053v2, Theorem 1.1) extends to
systems with non-Markovian Caputo time-fractional dynamics. The
concrete question: is there a map α(σ, β) and a single constant c such
that

  R_σ(β) := log Z_σ(β) − log Z_1(β) = c · BD_int(α(σ, β))

holds to ≤1% rel-dev across σ ∈ {0.5, 0.7, 0.9} and ≥2 dex of β?

Going-in confidence per BIG_IDEAS_REVIEW: 10-15% positive (i.e., most
experts expect this to fail by cohomological-irreducibility analog of
the closed B1 result).

The W7 wiring document scoped a 3-day numerical analysis
(`analysis/25_w7_fractional_bridge_v0.py`) to test the conjecture
empirically. That experiment is now **no longer needed**.

## What ChatGPT Pro delivered

A clean structural argument that settles B1.5 in a single line, plus
explicit numerical demonstration. Reproduced + reformatted:

### The killer argument

**For Caputo time-fractional FPE with harmonic confinement,
R_σ(β) ≡ 0 identically for all σ ∈ (0,1] and all β > 0.**

Proof sketch:
1. The harmonic FP operator `L_β = ∂_x(k_h x p) + β^{-1} ∂_xx p` has
   stationary density `p_eq(x) = exp(-β k_h x²/2) / Z_1(β)` with
   `Z_1(β) = √(2π/(β k_h))`.
2. The Caputo time-fractional FPE is `∂_t^σ p = L_β p`. A
   time-independent function has `∂_t^σ p_eq = 0` for any σ ∈ (0,1].
   So `p_eq` solves the σ-fractionalized equation for EVERY σ.
3. Therefore `Z_σ(β) = ∫ p_eq dx = Z_1(β)` for all σ.
4. Therefore `R_σ(β) ≡ 0`.

Equivalent operator-theoretic restatement:
- Caputo fractionalization is a scalar functional calculus of L
  (specifically: `p(t) = E_σ(t^σ L) p(0)` where E_σ is Mittag-Leffler).
- This calculus commutes with the spectral projections of L.
- For nonzero modes n ≥ 1: replaces exponential relaxation
  `e^{-n k_h t}` with `E_σ(-n k_h t^σ)`.
- For the zero mode (ker L): fixed pointwise since `E_σ(0) = 1`.
- The equilibrium partition function only sees ker L.
- Therefore Z_σ is σ-independent.

### Why BD_int can't be zero non-trivially

Berndt-Dixit's `B(a) := BD_int(a)` admits the series form

  B(a) = √a · [(γ − log(2πa))/(2a) + Σ_{n≥1} φ(na)]

where `φ(x) = ψ(x) + 1/(2x) − log(x)` and ψ is the digamma. By
Binet's formula,

  φ(x) = −2 ∫_0^∞ t / ((t² + x²)(e^{2πt} − 1)) dt < 0  for x > 0.

For a ≥ 1: `γ − log(2πa) < 0` and every `φ(na) < 0`, so `B(a) < 0`.
For 0 < a < 1: B(a) = B(1/a) < 0 by the Berndt-Dixit self-reciprocity
(arXiv:0904.1053v2 Theorem 1.1).

Therefore **BD_int(a) < 0 strictly for every a > 0**.

Numerical samples (per ChatGPT Pro's computation):
- BD_int(0.1) ≈ −0.5677306817
- BD_int(1.0) ≈ −0.7606614015
- BD_int(10.0) ≈ −0.5677306817   ← reciprocal-symmetric with 0.1

Large-a asymptotic:
  BD_int(a) = (γ − log(2πa))/(2√a) − π²/(72 a^{3/2}) + O(a^{-5/2})

The only `R_σ(β) = c · BD_int(α(σ,β))` solution consistent with
R_σ ≡ 0 and BD_int < 0 is `c = 0`, which is degenerate (vacuous —
the "≤1% relative deviation" criterion is meaningless when the
target is identically zero).

### Why the "spectral partition" reinterpretation doesn't rescue it

One could try replacing `Z_σ(β)` with `Z_σ^{dyn}(t) := Tr E_σ(t^σ L) =
Σ_n E_σ(-n k_h t^σ)`, but:
- At σ=1: `Z_1^{dyn}(t) = 1/(1 − e^{-k_h t})`, **not** the equilibrium
  partition function `√(2π/(β k_h))`. So this is a different object.
- For σ < 1: the asymptotic `E_σ(-n k_h t^σ) ~ 1/(n k_h t^σ Γ(1−σ))`
  as n → ∞ gives logarithmically divergent trace. **Not even
  well-defined** as a partition function.

So the only `Z_σ` for which the question is well-posed gives R_σ ≡ 0.
Done.

## The structural-analog table

| Bridge | Trivial-sector obstruction | Nontrivial reciprocal sector | Closure mechanism |
|---|---|---|---|
| **B1** (modular forms, closed diary 19) | g* ∈ H¹(Γ, V_k) is irreducible as a cohomology class | Watson's M(α) is irreducibly modular | 20 candidates across 5 families all fail; cohomological irreducibility |
| **B1.5** (fractional FPE, closed here) | `ker L` is fixed pointwise by Caputo subordination | BD_int(a) < 0 strictly with α↔1/α reciprocity | **One-line spectral argument: subordination fixes ker L** |

The shared structural pattern: a *trivial invariant sector* (modular
cohomology / equilibrium kernel) cannot be identified with a *nontrivial
reciprocal sector* (Watson M(α) / Berndt-Dixit BD_int(a)). The mechanism
is different but the conclusion is parallel.

**Generalized claim** (now medium-high confidence after B1 + B1.5):
*any* attempt to bridge a subordination-style time-deformation of a
generator L to a Mellin-pair-style nontrivial reciprocal spectral object
will fail by the same structural principle — the trivial-sector
projector is invariant under functional calculus of L, but the reciprocal
object lives in a non-trivial fixed class.

## What this changes in the project

### Closures

1. **Pass D is now FULLY CLOSED.** B1 was "essentially established" at
   diary 19; B1.5 was the last 10-15% positive-confidence gap; that gap
   is now decisively closed at structural-zero.
2. **`analysis/25_w7_fractional_bridge_v0.py` is NOT NEEDED** — the
   3-day numerical experiment scoped in W7_BERNDT_DIXIT_WIRING.md §6 is
   superseded by the structural argument. Mark as "obviated by diary 35"
   in the W7 doc.

### Updates needed

- [ ] `insights/DID_NOT_PAN_OUT.md` — add R18 entry: "B1.5 fractional-FPE
      bridge FALSIFIED structurally; Caputo subordination fixes ker L"
- [ ] `insights/BIG_IDEAS_REVIEW.md §3b` — update from "10-15% positive"
      to "CLOSED NEGATIVE"; promote the "generalized obstruction
      principle" (trivial-sector vs nontrivial-reciprocal-sector) to a
      named pattern
- [ ] `insights/W7_BERNDT_DIXIT_WIRING.md` — append closure note pointing
      to diary 35
- [ ] `insights/CANDIDATE_INSIGHTS.md` — promote the
      generalized-obstruction-principle as a §E candidate (medium-high
      confidence after 2 confirming instances)
- [ ] W7 paper draft — restructure: was a planned bridge experiment,
      now a SHORT NOTE on "subordination obstructions in fractional
      dynamics × Mellin-pair reciprocity"

### Implications for Project C

The recognizer + cost-model architecture currently doesn't reason about
which *sector* of a generator's spectrum a candidate expression lives in.
Adding sector-awareness would be a future v1.x capability — would help
the search engine identify "this transformation can't possibly help
because it's in a trivial sector" without doing the numerics.

## Methodology note — Erdős-style prompt design works

This is the SECOND case (after v0.8a's ChatGPT-Pro proposer test) where
a single Erdős-style open T/F prompt to ChatGPT Pro produced a
high-quality result that advances the project. The prompt structure that
worked:

1. Open-ended T/F framing ("either direction would be interesting")
2. Construction invitation explicit (Option A) but counterexample/
   obstruction invitation also explicit (Option B)
3. Prior-surfacing ("most experts would expect failure for reason X")
4. Anti-handwave guard ("'it's likely hard' is not an answer")
5. Numerical bar ("≤1% rel-dev across 3 σ values × 2 dex β")
6. Literature anchors (Berndt-Dixit + Mittag-Leffler + cohomological
   irreducibility)

The model picked Option B (obstruction), gave the structural argument
in 3 paragraphs, provided numerical demonstration, AND identified the
exact analog with B1's modular obstruction. This is the same pattern
as the OpenAI Erdős CoT ("number fields deserve a closer look" →
honed methodically).

**For future B-question work**: this is now a validated workflow.
Design Erdős-style prompts for genuinely open questions, present to
frontier LLM, treat the answer as a serious candidate that needs human
verification, write up the result. Cycle time: ~10 min prompt design +
~3 min model response + ~30 min verification + diary write-up.

## Bottom line

**B1.5 falsified at structural zero — Pass D fully closed.** The
fractional analog of the cohomological irreducibility obstruction is
SHARPER than the modular case: Caputo subordination commutes with
spectral projections of L, so it fixes ker L (the equilibrium sector)
pointwise. The Berndt-Dixit reciprocal integral cannot match an
identically-zero residual non-trivially. The generalized
trivial-sector-vs-nontrivial-reciprocal-sector obstruction principle is
now supported by 2 instances (B1 modular + B1.5 fractional) — promoted
to a §E candidate insight at medium-high confidence.

**Confidence**: very high on B1.5 closure (structural one-line argument
verified by ChatGPT Pro + numerical demonstrations consistent;
independently reproducible from the operator-theoretic definition of
Caputo subordination + Berndt-Dixit's Binet form). Medium-high on the
generalized obstruction principle (2 confirming instances, both with
clean closure mechanisms).

## Confidence tag

high (single-line structural argument verifiable from first principles)

## Follow-up leads

1. **Sharpen the generalized obstruction principle** — characterize the
   class of bridges that fall by trivial-sector-vs-nontrivial-reciprocal
   mismatches. Likely a one-page note in CANDIDATE_INSIGHTS §E.
2. **W7 short-note draft** — replace the W7 planned-experiment paper
   with a 4-6 page note on "subordination obstructions in
   fractional-dynamics × Mellin-pair reciprocity, with comparison to
   the modular B1 obstruction".
3. **Test the obstruction principle on a third bridge** — find a
   structurally analogous candidate (e.g. Riemann-Liouville rather than
   Caputo; non-harmonic confinement; non-equilibrium quantities). If
   the obstruction still applies, that's stronger evidence for the
   generalized principle.
4. **Update HUNT_MAP §B** to reflect Pass D closure.
