# Diary 41 — Mock theta completion: ChatGPT Pro caught a bug in P2 prompt; Zwegers R_{a,b} erfc form is the actionable speedup

**Date:** 2026-05-25
**Source:** ChatGPT Pro response to Prompt P2 ("novel closed form for
Watson-Hickerson Eichler integral").
**Status:** No finite closed form in the requested holomorphic class
(rigorous obstruction); Zwegers R_{a,b} erfc form is the practical
speedup + the cleanest path for f5/f7/f10 implementations.

## What ChatGPT Pro caught (and what was wrong with my prompt)

The integral I wrote in the P2 prompt:

```
g*(τ) = -2 (η(τ))³ ∫_{-τ̄}^{i∞} (η(2σ))^{-3} / (-i(σ+τ))^{3/2} dσ
```

ChatGPT correctly diagnosed this **diverges**: parametrize the
vertical tail as `σ = -τ̄ + it` for `t → +∞`. Then `(η(2σ))^{-3}
~ e^{-πiσ/2}` (from the leading `e^{πiσ/6}` of η at large imaginary
part), so `|(η(2σ))^{-3}| ~ e^{π·Im(σ)/2}`. The denominator
`|-i(σ+τ)|^{3/2} = (2y+t)^{3/2}` is polynomial. Net: integrand
`~ e^{πt/2} / (2y+t)^{3/2}` → ∞ as t → ∞.

**This is a bug in MY prompt, not in our code.** Our actual
implementation (`analysis/17_mock_theta_residual_ebm_v1.py::
watson_mordell_integral`) uses the **convergent Mordell form**:

```python
return 4 * sqrt(3 * alpha / (2 * pi)) * quad(integrand, [0, mp.inf])
```

over `t ∈ [0, ∞)` with super-exponential decay at large t. This works
and gives ≥30 digits.

My prompt summary picked a generic Eichler-integral form from
training-memory; should have copied the actual Mordell integrand.
**Lesson: when asking ChatGPT for a faster form, paste the actual
implementation, not a memory-paraphrase.**

## The actionable speedup ChatGPT Pro provided

**Zwegers' R_{a,b} contour integral** (the modern standard form for
mock theta completions) has a closed-form **erfc series** that is:
- **Exact** (no quadrature truncation error)
- **Gaussian-convergent** (~O(log(1/ε)) terms for ε precision)
- **Tool-free** beyond standard `mpmath.erfc`

The formula:

```
R_{a,b}(z) = Σ_{ν ∈ a+ℤ} sgn(ν) · e^{-2πiνb − πiν²z} · erfc(|ν|·√(2π·Im(z)))
```

Derived by substituting `u = -i(σ+z)` in Zwegers' contour integral
and integrating termwise.

For Ramanujan's f₀ (5th-order mock theta, OEIS A053256), the
published completion is:

```
~tilde f₀(z) = q^{-1/60}·f₀(q) − ζ_10·(ζ_12^{-1}·R_{1/30, 1/2}
                                       + ζ_12·R_{11/30, 1/2})(30z)
```

ChatGPT Pro verified at z = 30·τ where τ = i·log(2)/(2π) (i.e.,
q = 1/2):
- R_{1/30, 1/2}(z) ≈ 0.83484382693219515599718622290975173097955529... − 0.087745621995979123430700447571244921745491... i
- erfc series and direct contour integral agree to **>45 digits**

For f₃ (3rd-order, what we currently have), the analogous formula
uses different (a, b) parameters; same machinery.

## Why no finite closed form exists in the requested grammar

This is the rigorous Level-3 obstruction (mirrors diary 38's
algebraicity argument for the latent operator algebra):

Any finite expression built from `{exp, log, algebraic, Γ, ψ^{(m)},
η(q), θ(q), ζ, L}` at `q = e^{2πiτ}` is **holomorphic in τ on the
upper half-plane**. Its ∂̄-derivative is zero.

But g* (the non-holomorphic completion) has nonzero ∂̄:
```
∂g* / ∂τ̄ = -2 · η(τ)³ · η(-2τ̄)^{-3} · (2y)^{-3/2}
```

For the standard R_{a,b} completion, the ∂̄-derivative is the unary
theta shadow (the central object in Zwegers' framework).

So no finite holomorphic-in-τ expression can equal the completion.
The grammar MUST be enlarged to include erfc, incomplete-gamma, or
explicit `τ̄`-dependence for any closed form.

**This sharpens an obstruction we'd been implicitly assuming.** No
amount of operator-composition over our 8-op basis (all holomorphic-
in-τ) can produce a Watson-Hickerson completion. Mock theta computation
is structurally outside the basis's reach for the closed-form question.

## L-values don't help

In classical Eichler theory, L-values enter via PERIOD COCYCLES:
```
f*(z) − γ·z^{k-2}·g*(-1/z) = Σ_j C_j · L(k-1-j, f) · z^j
```
This expresses the modular *discrepancy* in critical L-values, but
the Eichler integral f*(z) itself remains a period-type function with
nontrivial transformation law (the Eichler cohomology class). It's
not finite-replaceable by L-values.

## Rational-cusp caveat

At rational radial limits `q → e^{2πih/k}`, special finite expressions
CAN occur because some q-hypergeometric series terminate. Folsom et
al. exploit this on rational quantum sets. Doesn't apply to q=1/2
(interior point of H, not a cusp), but COULD apply if we wanted to
evaluate f₃ at rational radial limits — a niche capability that's
worth flagging.

## What to actually implement (v0.8d / v0.9)

1. **Replace `analysis/17_mock_theta_residual_ebm_v1.py::
   watson_mordell_integral` with the erfc series form.**
   Same numerical output to ≥30 digits; faster + simpler.

2. **Implement R_{a,b} via erfc as a primitive in `rkc/completions.py`**:
   ```python
   def zwegers_R_ab(a: mpf, b: mpf, z: mpc, n_digits: int = 30) -> mpc:
       """R_{a,b}(z) via Gaussian-convergent erfc series.
       N terms needed: ~log(10^n_digits) / (π·a²)."""
   ```

3. **f5/f7/f10 completions become tractable** via the Andersen
   formulation:
   - f5: tilde f_0 = q^{-1/60}·f_0(q) − ζ_10·(ζ_12^{-1}·R_{1/30, 1/2}
                                              + ζ_12·R_{11/30, 1/2})(30z)
   - f7: analogous with different (a, b) parameters from Hickerson 1988
   - f10: analogous from Choi 1999

4. **Validation**: cross-check against OEIS b-files (A053256-A053287)
   to ≥30 digits, AND against our existing f3 Mordell-form output.

5. **Speedup measurement**: at the canonical test point q=1/2,
   measure wall-clock for erfc form vs current Mordell-quad form.
   Hypothesis: erfc ≥3× faster.

This addresses task #45 (self-serve f5/f7/f10 completion) cleanly —
the path is now Zwegers R_{a,b} erfc, not Hickerson 1988 contour
machinery.

## Bottom line

ChatGPT Pro's P2 answer is mixed:
- NO finite closed form in the requested holomorphic grammar
  (rigorous obstruction theorem)
- YES the Zwegers R_{a,b} erfc form is faster + cleaner than our
  current Mordell-quad implementation AND unblocks f5/f7/f10

The "bug" in my P2 prompt (divergent integral form) was caught and
diagnosed by ChatGPT. Our code is fine but the documentation /
prompt-summary was sloppy. **Lesson for future prompts: paste actual
implementation, not memory-summary.**

The erfc form is implementable in 1-2 days; would close task #45 and
the rkc v0.1 mock-theta-coverage gap.

**Confidence**: high on the structural obstruction theorem (standard
harmonic-Maass-form theory); high on the erfc form's mathematical
correctness (Zwegers 2002 + Andersen 2017 publish it); medium on the
3× speedup claim (needs benchmark; could be 10× or 0.5× depending on
mpmath erfc cost vs quad cost).

## Follow-up leads

1. **v0.8d task**: implement Zwegers R_{a,b} erfc form for f3 (replaces
   Mordell-quad); validate against OEIS A053256 b-file to ≥30 digits.
2. **v0.9 task**: extend R_{a,b} to f5/f7/f10 per Andersen 2017
   formulations.
3. **Update diary 16** with a correction note about the P2-prompt bug
   (or just cross-link to this diary).
4. **Add "ChatGPT-as-bug-catcher"** as a methodology pattern. 6th
   cycle and counting; this is the first time the model caught an
   error in OUR framing rather than confirming/refuting an open claim.
   That's a different mode of value than the previous 5 cycles.

## Cross-link

- diary/16 — original Watson-Hickerson f3 instrumentation
- diary/35, 37, 38, 39, 40 — earlier ChatGPT-Pro Erdős-style cycles
- HUNT_MAP §"f5/f7 instrumentation" → now actionable via Zwegers erfc
- analysis/17_mock_theta_residual_ebm_v1.py — current Mordell impl
- rkc/completions.py — where the new R_{a,b} primitive should land
