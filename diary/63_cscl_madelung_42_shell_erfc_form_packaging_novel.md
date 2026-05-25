# Diary 63 — CsCl Madelung constant: 42-shell erfc/exp packaging vs 1201-term 2D csch/sech

**Date:** 2026-05-25
**Source:** ChatGPT-Pro response to a Madelung-sum-acceleration prompt
on the CsCl (B2) lattice structure.
**Status:** **REAL ACCELERATOR with packaging novelty.** Cost ratio
28× in scalar terms, ~5.6× in wall-clock (mpmath 80 dps). Math is
classical Ewald/Poisson machinery; the specific 42-shell formula is
new packaging. Needs in-env verification (queue task #74).

## The result

For CsCl (B2 lattice), nearest-neighbor-normalized signed Madelung
constant:

```
M_CsCl = -1.7626747730709883979356733206386442911705...
```

ChatGPT proposes:

```
M_CsCl = (√3/2) [ -2
                  + 2 Σ_{n≥1} r_3^odd(n) · e^{-πn}/(πn)
                  + Σ_{n≥1} r_3(n) · erfc(√(πn))/√n
                  - 2 Σ_{N≥3, N≡3 mod 8} h(N) · erfc(√(πN)/2)/√N ]
```

where:
- r_3(n) = #{u ∈ ℤ³ : u_1² + u_2² + u_3² = n}
- r_3^odd(n) = #{u ∈ ℤ³ : same, u_1+u_2+u_3 ≡ 1 (mod 2)}
- h(N) = #{u ∈ ℤ³ : (2u_1+1)² + (2u_2+1)² + (2u_3+1)² = N}

For 30 digits, truncate at n ≤ 24 (both r_3 sums) and N ≤ 96 (h sum).
Total nonzero shell entries: 21 + 9 + 12 = **42**.

## Verification table (ChatGPT-claimed, mpmath dps=80)

| Method | Cutoff | Scalar terms | Value | Abs. error |
|---|---|---|---|---|
| Current 2D csch/sech (Zucker-Glasser-style) | m,n,j,k ≤ 24 | 1201 | -1.762...4589... | 2.98×10⁻³⁴ |
| Proposed 42-shell erfc/exp | R²≤24 (or N≤96) | **42** | -1.762...4234... | 5.64×10⁻³⁵ |
| Reference (high-precision) | — | — | -1.762...4291... | — |

**Term-count ratio:** 1201 / 42 = **28.6×**.

**Wall-clock ratio (ChatGPT's measurement, mpmath dps=80):** median
33.2 ms (current) vs 5.89 ms (proposed) = **5.6×**.

## Provenance (ChatGPT's framing)

> "The theta/Mellin and Ewald background is not new: Borwein-Borwein-
> Taylor established rigorous convergence issues for Madelung sums,
> and Crandall-Buhler describe Ewald, cosech, and generalized
> functional-equation expansions for arbitrary point-charge crystals."

> "The new part here is the particular CsCl packaging above: the
> folded t≥1 theta integral followed by a nearest-neighbor-normalized
> three-shell erfc/exponential formula with r_3, r_3^odd, and odd-
> shift counts. I did not find this exact 42-shell formula in the
> sources checked. It should be viewed as a concrete, reproducible
> specialization of standard Ewald/Poisson machinery, not as a
> fundamentally new analytic identity."

So: **packaging novelty over Crowdy-Marshall/Borwein-Borwein-Taylor/
Crandall-Buhler classical Ewald machinery.** Same category as the
annular Poisson Green accelerator (diary 51): known math, useful
packaging.

## What this is NOT

- NOT replacing an iterative driver. Madelung sums are computed once
  per crystal structure; the speedup matters but the iteration-driver
  reframing doesn't apply.
- NOT a new analytic identity.
- NOT a 30-digit closed form (in the strict "named special function"
  sense); it's a fast Ewald-style sum.

## What this IS

- A small real packaging contribution.
- 28× term reduction, 5.6× wall-clock — these are real numbers (if
  verified in our env).
- A useful primitive for lattice physicists / chemists doing CsCl-
  family structures.

## Tasks queued

- **#74**: Verify the 42-shell formula independently at mpmath dps=80
  in our local env. Compare measured wall-clock against the
  1201-term Zucker-Glasser baseline. Replicate the 5.64×10⁻³⁵
  absolute-error claim. Half-day.
- **#75**: Audit the local literature corpus (especially Crandall-
  Buhler-style references in `corpora/text/` if present) for the
  specific r_3^odd / h(N) shell weighting; confirm or refine the
  novelty claim.

## Strategic implication

**Real accelerator, partially-novel packaging, easy to verify.**
Smaller-ticket than the AB 4.2.3 corrigendum but a clean adjunct.
Could be part of a "computational lattice-sums primitives" appendix
in the tool paper, alongside (a)-(d) cross-domain accelerators.

**Excitement:** 5/10 — real but small; packaging novelty + a useful
primitive.

**Confidence:** medium-high pending in-env verification of the 28×
term-count + 5.6× wall-clock claims.
