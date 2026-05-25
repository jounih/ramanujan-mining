# Diary 60 — Web-based prior-art audit of the four verified cross-domain accelerators

**Date:** 2026-05-25
**Source:** Literature-audit subagent task. WebFetch + WebSearch over the
prior art for the 4 accelerators verified locally in diary 59
(commit `1a413d4`). The verification was about correctness + speedup;
this is about novelty: is the construction (not the speedup, not the
methodology) published before?
**Status:** Two CONFIRMED-KNOWN, one CONFIRMED-KNOWN-WITH-REPACKAGING-NOVELTY,
one PARTIAL with the closed Tricomi-U Ai(-x) two-sector form being the
least-documented of the four.

## Headline

| # | Accelerator | Verdict | Closest published prior art |
|---|---|---|---|
| a | Finite-pole semiseparable attention | **KNOWN-AS-RETNET / SSD-MULTI-HEAD** | RetNet (multi-scale γ per head) + SSD/Mamba-2 (1-SS matrix = single geometric decay); the multi-pole "R poles per row" form is mathematically equivalent to R heads of single-pole RetNet |
| b | Annular Poisson Green modular kernel | **KNOWN MATH; PACKAGING-NOVELTY** | Crowdy–Marshall–Nasser Schottky-Klein/θ₁-quotient annular Green construction (classical); diary 51 itself flags "I did not find this exact 30-digit wall-clock benchmark packaged as a replacement kernel" — confirmed |
| c | PH spring-mass Bessel-image propagator | **KNOWN (Schrödinger 1914 + standard periodic-image)** | Schrödinger 1914 *Zur Dynamik elastisch gekoppelter Punktsysteme* gives J_{2n}(2ωt) for infinite chain; the periodic Σ_ℓ J_{n+ℓN}(2ct) is the standard image-method extension and is in Mattis-style harmonic-chain literature |
| d | Airy Tricomi-U two-sector closed form | **PARTIAL — special-case-of-classical; specific packaging less-documented** | DLMF 9.6.21 gives Ai(+z) = U(5/6, 5/3, 2ζ) (different parameters); the *negative-argument* two-sector U(1/6, 1/3, ±2iη) form is a re-derivation of the same Borel-Hankel sum but the specific equation isn't on the DLMF page, Wikipedia, or in Fredrik Johansson's mpmath survey blog. Mera–Boito Meijer-G resummation literature is the closest broader pattern. |

So: **diary 59's CORE CLAIM that all 4 are real accelerators** stands.
**Diary 50/51/53/56's PROVENANCE-NOVELTY CLAIMS** were already honest
("packaging contribution, not new theorem" — direct quote from diary 56;
"this is essentially modular_transform_with_correction applied to a
theta-quotient Green kernel" — diary 51; "classical Bessel-image kernel
repackaged as a PH simulation primitive" — diary 53). The audit
substantiates the diaries' own self-assessment. Paper framing should
be: **"verified implementation + benchmarking contribution"**, not
"new identity discovery", for (a), (b), (c). For (d), the closed
Tricomi-U two-sector representation of Ai(−x) appears to be a
re-derivation of classical-but-uncommonly-collected material — worth
checking against Olver *Asymptotics and Special Functions* or Wong
*Asymptotic Approximations of Integrals* if available locally.

## Methodology

For each accelerator I did 3–5 WebFetch + WebSearch queries targeting
both the specific construction and the closest broader literature
class. Searches covered:

- (a) Linformer / Performer / Linear Attention (Katharopoulos) /
  RetNet / Mamba / S4 / RWKV / Lightning Attention / SSD / multi-pole
  rational kernels
- (b) classical annulus Green function literature
  (Englis 1989 / Grossi-Vujadinovic 2015 / Crowdy multiply-connected
  / Schottky-Klein prime function)
- (c) Schrödinger 1914 Annalen / Wittman-Sullivan-Friesecke harmonic
  chain reviews / finite-periodic-chain literature
- (d) DLMF §9.6 / Wikipedia Airy article / Fredrik Johansson mpmath
  blog / Meijer-G + Borel-Padé resurgence / Olver

Total queries: **15 WebSearch + 11 WebFetch = 26 calls**. Time spent:
about 35 minutes wall-clock.

## Per-accelerator findings

### (a) Finite-pole semiseparable attention → KNOWN

The construction in `rkc/attention/finite_pole.py`:

```
A_{ij} = 1_{j<=i} · Σ_{r=1}^R q_{i,r} k_{j,r} α_r^(i-j)
S_{r,i} = α_r · S_{r,i-1} + k_{i,r} v_i
```

is structurally identical to two published recurrent attention designs:

1. **RetNet** (Sun et al., *Retentive Network*, [arxiv 2307.08621](https://arxiv.org/abs/2307.08621),
   2023). RetNet uses *multi-scale γ* with **one decay per head** but
   **H heads** in total, so the per-position output is Σ_h q_{i,h} S_{h,i}
   with S_{h,i} = γ_h · S_{h,i-1} + k_{i,h} v_{i,h}. Identifying h ↔ r
   gives the diary 50 form exactly.

2. **Mamba-2 SSD** (Dao & Gu, *Transformers are SSMs*,
   [arxiv 2405.21060](https://arxiv.org/abs/2405.21060), 2024).
   The 1-SS (1-semiseparable) mask is by definition the geometric-decay
   single-pole kernel; multi-head SSD with H heads = the same R-pole
   construction.

3. **Lightning Attention** (Qin et al.,
   [arxiv 2401.04658](https://arxiv.org/abs/2401.04658), 2024) uses
   per-head fixed scalar λ with the explicit recurrence
   S_t = λ S_{t-1} + k_t^T v_t. **Identical** to the diary 50 form for R=1.

4. **Elucidating the Design Space of Decay in Linear Attention**
   ([arxiv 2509.05282](https://arxiv.org/pdf/2509.05282), 2025) is a
   survey paper that explicitly enumerates scalar / multi-pole /
   data-dependent decay parametrisations — including the multi-pole
   variant.

Diary 50 itself acknowledged: "Per ChatGPT, recent SSD work explicitly
connects semiseparable matrix decompositions to SSMs and attention
variants; this falls in the semiseparable / state-space family." This
audit confirms that. The specific multi-pole-per-row formulation
A_{ij} = Σ_r q_{ir} k_{jr} α_r^(i-j) is equivalent to R parallel
single-pole heads, and is in the published 2024-25 SSD/RetNet/Lightning
literature.

**Verdict: CONFIRMED-KNOWN.** The construction is published; the diary
50 wrapper adds nothing structurally new. Diary 50's claim was
"closed-form for THIS structured attention semantics + paper material
in ML systems venues" — the closed-form part is correct, but the paper
framing must be re-cast as either (i) a clean reference implementation
of the multi-pole-RetNet/SSD family with novel benchmarking, or (ii)
a connection between Project C's modular operator basis and the SSD
family (the cross-domain methodology-transfer story). Diary 59 measured
50× at N=4096 for R=8; that's a perfectly publishable benchmark but it
should be framed against the published RetNet/Mamba-2 baseline, not as
a new architectural primitive.

Most relevant citation: **Sun et al., "Retentive Network: A Successor
to Transformer for Large Language Models", arxiv:2307.08621, July 2023.**
https://arxiv.org/abs/2307.08621

### (b) Annular Poisson Green modular kernel → KNOWN MATH + PACKAGING NOVELTY

The fast form in `rkc/pde/annular_green.py`:

```
G_L(θ, y; φ, η) ≈ (1/4π) · log [(cosh(πδ/L) − cos(π(y+η)/L))
                              / (cosh(πδ/L) − cos(π(y−η)/L))]
```

is the n=0 image of the classical θ₁-quotient Green function for the
annulus under the modular S-transform τ = iL/π → −1/τ. Status:

- **Englis (1989) "A Green's Function for the Annulus"** — classical
  reference, expresses G via "generalisations of the Weierstrass
  zeta function" (which are equivalent to θ-derived kernels).
- **Crowdy & coauthors** (Imperial, since 2007) — extensive series on
  Green's functions for multiply-connected domains via the
  Schottky-Klein prime function. The annulus is the simplest non-trivial
  case. See "Green's functions for Laplace's equation in multiply
  connected domains", D. Crowdy & J. Marshall.
  https://www.ma.imperial.ac.uk/~dgcrowdy/PubFiles/Paper-19.pdf
- **Grossi & Vujadinovic (2015) "On the Green function of the annulus"**,
  [arxiv 1508.06404](https://arxiv.org/abs/1508.06404) — uses
  Gegenbauer / zonal spherical harmonics rather than θ-functions; an
  alternative form.
- **Recent (2025) "The Neumann Green function of the annulus"**,
  [arxiv 2512.19397](https://arxiv.org/abs/2512.19397) — Gegenbauer
  approach for Neumann BC.

The diary 51 form (S-transform on θ₁-quotient → one-image collapse for
L<<1) is unambiguously KNOWN MATHEMATICS. What appears to be less
well-documented is the specific **30-digit-precision wall-clock
benchmark packaging as a replacement kernel for numerical PDE solvers**
on thin annuli — exactly as diary 51 itself flagged
("packaging/recipe contribution more than a novel theorem").

I did NOT find a published benchmark paper presenting this exact
construction as a drop-in primitive for annular Poisson solvers with
the thin-L → one-image error bound made explicit. So:

**Verdict: KNOWN-MATH; SPECIAL-CASE-OF-CROWDY-SCHOTTKY-KLEIN; but the
packaging as "drop-in 30-digit kernel with L<<1 truncation bound" looks
under-documented as a numerical-PDE recipe.** Paper framing: SIAM J.
Sci. Comput. short note as a numerical-PDE primitive, citing
Crowdy-Marshall as the mathematical source.

Most relevant citation: **Crowdy, D. & Marshall, J. (2007), "Green's
functions for Laplace's equation in multiply connected domains",
IMA J. Appl. Math.**
https://www.ma.imperial.ac.uk/~dgcrowdy/PubFiles/Paper-19.pdf

### (c) PH spring-mass Bessel-image propagator → KNOWN

The construction in `rkc/ph/bessel_image_propagator.py`:

```
q_n(t) = Σ_{ℓ∈ℤ} J_{2(n+ℓN)}(2ct),   c = √(k/m)
p_n(t) = √(mk) · Σ_{ℓ∈ℤ} [J_{2(n+ℓN)−1}(2ct) − J_{2(n+ℓN)+1}(2ct)]
```

is the **periodic image extension** of Schrödinger's 1914 infinite-chain
Bessel solution.

- **E. Schrödinger (1914), "Zur Dynamik elastisch gekoppelter
  Punktsysteme", Annalen der Physik 349, 916–934** — the original
  Bessel-function solution u_n(t) ∝ J_{2n}(2ωt) for the infinite chain.
  https://onlinelibrary.wiley.com/doi/10.1002/andp.19143491405
  (English translation: hal-02915049)
- **Trovato et al. (2016), "The classical harmonic chain: solution
  via Laplace transforms and continued fractions",
  [arxiv 1608.00616](https://arxiv.org/abs/1608.00616)** — explicitly
  gives the periodic-N form as u_n(t) = Σ_ℓ J_{n+ℓN}(2ct). The
  WebFetch confirmed: "the periodic solution involves
  u_n(t) = Σ_l J_{n+lN}(2ct)" — **letter-for-letter identical** to
  diary 53 except for the factor-of-2 in the index (a convention
  difference: 2n vs n depending on how one indexes nearest-neighbor
  vs next-neighbor).
- **Sadurnì et al. (2012), "Exact propagators on the lattice with
  applications to diffractive effects",
  [arxiv 1205.3972](https://arxiv.org/abs/1205.3972)** — same
  Bessel-image pattern for tight-binding chains.
- **Sullivan/Friesecke** harmonic-chain reviews (cited in diary 53
  itself) cover the infinite-chain side.

Diary 53's own framing was honest: "Known: PH formulation, infinite
harmonic-chain solution q ∝ J_{2m}(2ωt) (Sullivan/Friesecke),
Jacobi-Anger expansion. New construction here (not the kernel itself):
The finite-periodic PH-network 'Bessel image' propagator with a 30-digit
truncation rule + sparse-output complexity claim."

The audit confirms the kernel is published; the diary's positioning as
"packaging contribution + sparse-query complexity bound + PH-systems
framing" is appropriate.

**Verdict: KNOWN — Schrödinger 1914 + standard periodic-image
extension.** The 30-digit-truncation rule and per-query O(1) sparse
complexity bound are the diary's authentic addition; those are
publishable as a numerical-methods note but the propagator formula
itself is over a century old.

Most relevant citation: **E. Schrödinger (1914), Annalen der Physik
349:916–934.**
https://onlinelibrary.wiley.com/doi/10.1002/andp.19143491405

Plus the modern explicit periodic form:
**Trovato et al. (2016),** https://arxiv.org/pdf/1608.00616

### (d) Airy Tricomi-U two-sector closed form → PARTIAL

The construction in `rkc/special/airy_resurgent.py`:

```
Ai(-x) = [e^{i(η-π/4)}/(2√π·x^{1/4})] · (-2iη)^{1/6} · U(1/6, 1/3, -2iη)
       + complex conjugate
```

where η = (2/3)x^{3/2} and U is Tricomi's confluent hypergeometric.

Status:

- **DLMF §9.6.21** gives `Ai(z) = 3^{-1/6} π^{-1/2} ζ^{2/3} e^{-ζ} · U(5/6, 5/3, 2ζ)`
  for POSITIVE z. **Different parameters** (5/6, 5/3) than the diary 56
  formula (1/6, 1/3). https://dlmf.nist.gov/9.6
- **DLMF §9.6** for Ai(-z) gives only the Bessel-function form
  `Ai(-x) = √(x/9)·[J_{1/3}(2x^{3/2}/3) + J_{-1/3}(2x^{3/2}/3)]`
  — does NOT give a Tricomi-U two-sector form on the page.
- **Wikipedia Airy function article** — does NOT contain a Tricomi-U
  closed form for negative argument.
- **Fredrik Johansson, "Airy in the library" (2015 mpmath blog)** —
  the most authoritative survey of Airy implementations from a
  computational standpoint. Lists ₀F₁ representations and Olver's
  asymptotic expansions; **does NOT mention the U(1/6, 1/3, ±2iη)
  two-sector form**.
- **Mera-Boito-Sumino / Meijer-G resummation literature** (e.g.
  [arxiv 1802.06034](https://arxiv.org/abs/1802.06034)) — the broader
  pattern "Borel transform IS a hypergeometric function, hence the
  Borel-Laplace integral has a Meijer-G closed form, hence no Padé
  needed" is exactly the meta-pattern of the diary 56 construction.
  This is the closest published broader CLASS.
- The U(1/6, 1/3, z) parameters (rather than (5/6, 5/3)) come from
  the alternative Whittaker representation; both are valid and
  related by the Kummer transformation. The two-sector Borel-Hankel
  decomposition for the oscillatory (negative-argument) sector
  produces the (1/6, 1/3) form naturally.

So: **the underlying special-function identity is classical** (Kummer
transformation + Borel-Hankel decomposition for the oscillatory
sector). What is less-well-documented is the **specific equation as a
drop-in computational primitive for Ai(−x)** — i.e. the precise
"Ai(-x) = sum of two U(1/6, 1/3, ±2iη)-evaluations" packaged as a
numerical recipe.

I did NOT find this exact equation in the standard computational
references checked (DLMF, Wikipedia, mpmath blog, basic Olver
references). It MAY be in Wong *Asymptotic Approximations of Integrals*
or Berry-Howls hyperasymptotics — those are textbook references not
fully on the web. Worth checking against a copy if one is available.

**Verdict: PARTIAL — the closed-form pattern is classical (Kummer +
Borel-Hankel + Meijer-G/Borel-resurgence), but the specific
ready-to-evaluate two-sector U(1/6, 1/3, ±2iη) form for Ai(−x) was
not found on standard online references.** The 50–328× speedup is real
(verified in diary 59) but the speedup baseline is a non-tuned
Borel-Padé; the speedup vs `scipy.special.airy` would be unfavorable
for double precision (mp.airyai at 70 dps is comparable per diary 59,
1.48×). Honest paper framing: "ready-to-use multiprecision Tricomi-U
representation of Ai(−x); not classically packaged this way; useful
for asymptotic-analysis enthusiasts using Borel-Padé as default tool".

Most relevant citation: **DLMF §9.6 (Olver, Lozier, Boisvert,
Clark)** for the positive-argument Tricomi-U Airy form
(https://dlmf.nist.gov/9.6). Closest broader-pattern citation:
**Mera et al. (2018), "Fast Summation of Divergent Series and
Resurgent Transseries in Quantum Field Theories from Meijer-G
Approximants", arxiv 1802.06034** for the "Borel transform is
classical → closed form replaces Padé" meta-pattern.
https://arxiv.org/abs/1802.06034

## Bottom line for publication

| Accelerator | Publishable framing |
|---|---|
| (a) | "Reference implementation + benchmark of multi-pole SSD/RetNet attention" — NOT a new architecture |
| (b) | "Drop-in numerical-PDE kernel with thin-L bound" — cite Crowdy-Marshall as math source |
| (c) | "30-digit + sparse-query primitive for periodic spring-mass chains" — cite Schrödinger 1914 + Trovato et al. 2016 |
| (d) | "Ready-to-use multiprecision Tricomi-U representation of Ai(−x)" — needs Olver/Wong textbook check before claiming "novel computational primitive"; the Meijer-G/Borel-collapse meta-pattern is in Mera 2018 |

**The cross-domain methodology-transfer story** (Project C's modular-S
operator + finite-pole intuition + resurgence-via-closed-special-function
generalizing outside number theory) is **structurally interesting**
even though each accelerator individually is KNOWN math, because:

1. The diary-by-diary closed-form discovery happened by Project C's
   operator-search workflow — a *methodology claim* (the workflow finds
   real things, not just q-series), not an *identity claim* (these
   specific identities are new).
2. The cross-domain landings are validation that the methodology
   generalizes; the individual identities being old is *fine* for the
   methodology paper.
3. For the four individual implementation papers, each must clearly
   cite the prior art.

## Tasks queued (this diary)

- **#81**: Re-frame any paper draft for (a) as "reference implementation
  + benchmark of multi-pole SSD/RetNet attention with R poles per head"
  — cite Sun/Dao/Qin et al.
- **#82**: Re-frame any paper draft for (b) as "drop-in 30-digit
  numerical-PDE kernel" with Crowdy-Marshall as math source citation.
- **#83**: Re-frame any paper draft for (c) as "30-digit periodic
  spring-mass chain primitive" citing Schrödinger 1914 + Trovato 2016.
- **#84**: Check Olver *Asymptotics and Special Functions* and/or Wong
  *Asymptotic Approximations of Integrals* (offline textbook check)
  for the specific Ai(−x) Tricomi-U two-sector formula. If absent,
  the (d) paper can claim "ready-to-use multiprecision packaging of
  classical material"; if present, must cite that source instead.
- **#85**: Update `insights/CANDIDATE_INSIGHTS.md` C-section and the
  4 source diaries (50, 51, 53, 56) with a "PROVENANCE-AUDITED" tag
  pointing at this entry.

## Bottom line

**Four independent cross-domain accelerators, all real, but all closer
to PUBLISHED PRIOR ART than the source diaries claimed.** Diary 59's
verification + this audit together mean:

- The accelerators *work* (diary 59).
- The accelerators are *not novel as mathematical identities*
  (this diary, for a/b/c; PARTIAL for d).
- The Project C methodology-transfer story is *intact* (the workflow
  found real, working, cross-domain identities — that the identities
  are classical doesn't invalidate the workflow).
- Paper framing for each must shift from "new construction" to
  "verified implementation + benchmark" or "drop-in numerical primitive
  citing source", as flagged above.

This matches the source diaries' own honesty markers (every one of
diaries 50, 51, 53, 56 includes a "Known / New construction here"
provenance section that essentially predicts the audit verdict). The
audit just makes it explicit and citation-ready.

**Confidence:** high on (a) and (c); high on (b)'s "known math"
verdict and medium-high on the "packaging novelty" qualifier; medium
on (d) PARTIAL pending an offline check of Olver / Wong.

## Time spent + total calls

- Total wall-clock: ~35 min
- WebSearch calls: 15
- WebFetch calls: 11
- Total web-tool calls: 26
