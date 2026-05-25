# Diary 58 — Level-pq Lambert/E_2 annihilator FAMILY: adversarial verification + literature diff revises novelty downward

**Date:** 2026-05-25
**Source:** `analysis/32_level_pq_family_adversarial_verification.py` + `analysis/results/32_level_pq_family_verification.csv` (25 annihilator tests across 5 cells each at mpmath dps=200) + literature diff across 6 PDFs (downloaded-pdfs/) + ~12 arxiv/SpringerLink/AMS/IAS/LMFDB web searches
**Status:** Independent NUMERICAL verification of the 7 new levels CONFIRMED + STRUCTURAL EXTENSIONS mapped (3-prime squarefree pqr, p²q, and p² prime-power cases) + **LITERATURE DIFF: NOVELTY CLAIM DOWNGRADED.** The closed-form coefficient formula is plausibly novel as a *specific explicit parameterization*, but the underlying STRUCTURE (a 1-dim linear-relation kernel among 4 Lambert blocks at squarefree pq) is a TRIVIAL CONSEQUENCE OF THE CLASSICAL DIMENSION FORMULA dim E_2(Γ_0(pq)) = 3 for the Eisenstein subspace of weight-2 modular forms at squarefree composite level. The formula content reduces to (i) the H-R-B base identity (1916, well-known) + (ii) Gaussian elimination on 3 equations in 4 unknowns.

## Bottom line

| Item | Verdict |
|---|---|
| H-R-B base identity (anchors the whole construction) | VERIFIED to rel-err ≤ 10⁻²⁰⁰ at 6 cells |
| 7 NEW levels (35, 51, 65, 77, 87, 95, 115) in OUR env at dps=200 | ALL PASS rel-err ≤ 10⁻¹⁰⁰ (5 cells each, worst across all 7 = 1.99×10⁻¹⁹⁹) |
| Twin primes N=143=11·13, N=323=17·19 | PASS (worst 6.99×10⁻¹³⁴ at N=323; bar-margined but in-spec) |
| Far-apart primes N=187=11·17, N=391=17·23 | PASS (worst 3.46×10⁻¹¹⁰ at N=391; bar-margined but in-spec) |
| Small-prime levels N=6, 10, 14, 22 (p=2 cases) | PASS (5/5 cells each; formula symmetric under p ↔ q) |
| 3-prime squarefree pqr (N=30, 105, 165) | 5-D annihilator space; both full-support and basis[0] combos PASS at dps=200 |
| p²-prime-power (N=49, 121) | NO ANNIHILATOR EXISTS; family does NOT extend; rank-3 constraint matrix saturates |
| p²·q (N=18, 45) | 3-D annihilator space; both full-support and basis[0] PASS |
| Literature diff (PDFs + arxiv + LMFDB + OEIS) | Specific coefficient formula appears novel BUT structural existence is classical |
| **Overall NOVEL vs PRIOR-OCCURRENCE verdict** | **PARTIAL-PRIOR**: structure is classical; explicit closed-form parameterization is novel but trivially derivable |

## (1) Independent numerical verification (7 new levels)

`analysis/32_*.py` independently computes coefficients via the closed-form formula, evaluates Σ c_d · T_d(α, β) at 5 cells on the αβ=π² hyperbola at mpmath dps=200, and reports per-cell rel-err = |Σ|/max_d|c_d·T_d|. All 5/5 cells pass for each of the 7 new levels:

| N | Coefficients (c_1, c_p, c_q, c_pq) | g, δ, m | Worst rel-err / 5 cells |
|---|---|---|---|
| 35 = 5·7 | (-1, 17, -17, 1) | g=2, δ=1, m=17 | 2.76×10⁻²⁰⁰ |
| 51 = 3·17 | (-7, 25, -25, 7) | g=2, δ=7, m=25 | 2.85×10⁻²⁰⁰ |
| 65 = 5·13 | (-1, 8, -8, 1) | g=8, δ=1, m=8 | 4.42×10⁻²⁰⁰ |
| 77 = 7·11 | (-1, 19, -19, 1) | g=4, δ=1, m=19 | 1.27×10⁻²⁰⁰ |
| 87 = 3·29 | (-13, 43, -43, 13) | g=2, δ=13, m=43 | 1.99×10⁻¹⁹⁹ |
| 95 = 5·19 | (-7, 47, -47, 7) | g=2, δ=7, m=47 | 4.88×10⁻²⁰⁰ |
| 115 = 5·23 | (-3, 19, -19, 3) | g=6, δ=3, m=19 | 1.07×10⁻¹⁹⁹ |

Compare with ChatGPT-Pro's reported worst at dps=120: 2.18×10⁻¹¹³ for level 115; our dps=200 worst 1.07×10⁻¹⁹⁹ for the same level. Confirmed independently with ≥85 digits of additional headroom.

## (2) Edge-case adversarial tests

### (2a) Twin primes (q − p = 2)

- N=35=5·7 already verified above (worst 2.76e-200)
- N=143=11·13: c=(-1, 71, -71, 1); worst 1.93e-200 ✓
- N=323=17·19: c=(-1, 161, -161, 1); worst 6.99e-134 ✓ (margined because coefficients are larger ⇒ cancellation eats ~66 digits at the most extreme α-large cell)

### (2b) Far-apart primes

- N=187=11·17: c=(-1, 31, -31, 1); worst 9.60e-200 ✓
- N=391=17·23: c=(-1, 65, -65, 1); worst 3.46e-110 ✓ (margined at cell 5 by ~90-digit cancellation; comfortably in-spec for the 10⁻¹⁰⁰ bar)

### (2c) p = 2 cases (small even prime; ChatGPT focused on p > 2)

- N=6=2·3: c=(-1, 5, -5, 1); worst 4.02e-200 ✓
- N=10=2·5: c=(-1, 3, -3, 1); worst 1.91e-200 ✓
- N=14=2·7: c=(-5, 13, -13, 5); worst 2.70e-200 ✓
- N=22=2·11: c=(-3, 7, -7, 3); worst 1.22e-199 ✓

Formula is symmetric under p ↔ q and the derivation does not require p > 2. The "p > 2" restriction in ChatGPT's exposition was a convention, not a structural requirement.

## (3) Structural extensions

### (3a) 3-prime squarefree N = p·q·r

Divisors: {1, p, q, r, pq, pr, qr, pqr} — 8 divisors. The 3 linear constraints (Σc_d = Σd·c_d = Σc_d/d = 0) give a rank-3 system; kernel dim = 8 − 3 = **5**.

So at level N = pqr there is a 5-DIMENSIONAL FAMILY of annihilators — non-unique. Computed rational nullspace via sympy at each of N ∈ {30, 105, 165}:

| N | First basis vector (sub-divisor annihilator, supports only {1,p,q,r}) | Full-support combo verified |
|---|---|---|
| 30 = 2·3·5 | basis[0] = (-3, 16, -18, 5, 0, 0, 0, 0) on divs (1,2,3,5,6,10,15,30) | combo (-107, 457, -371, 5, 1, 5, 5, 5) PASS |
| 105 = 3·5·7 | basis[0] = (-1, 9, -15, 7, 0, 0, 0, 0) | combo (-123, 769, -675, 7, 1, 7, 7, 7) PASS |
| 165 = 3·5·11 | basis[0] = (-6, 45, -50, 11, 0, 0, 0, 0) | combo (-323, 1993, -1715, 11, 1, 11, 11, 11) PASS |

All combinations verified to rel-err ≤ 10⁻¹⁹⁹ at dps=200. Note: basis[0] is itself a "linear sub-annihilator" using only the four divisors {1, p, q, r} — it's a 4-divisor annihilator on a *non-multiplicative* divisor set, not a pq-type annihilator.

There is also a sub-annihilator inherited from each pq sub-level: for N=105, basis[1] = (-1, 7, -7, 0, 1, 0, 0, 0) which is exactly the N=15=3·5 family annihilator (-1, 7, -7, 1) embedded with the 1 on the pq=15 position and zeros elsewhere — sub-annihilators lift.

### (3b) Prime power N = p²

Divisors: {1, p, p²} — 3 divisors. The 3 constraint equations form a 3×3 matrix:

```
[1  1  1   ]
[1  p  p²  ]
[1  1/p 1/p²]
```

This is a Vandermonde-type matrix in (1, p, p²) and (1, 1/p, 1/p²); for p ≥ 2 it has rank 3 (full rank). Kernel dim = **0**. Verified at N ∈ {49, 121}: no non-trivial integer annihilator exists.

**VERDICT: The family does NOT extend to prime powers.** The construction requires at least 4 divisors (i.e. at least 2 distinct prime factors).

### (3c) Composite with repeated prime N = p²·q

Divisors: {1, p, q, p², pq, p²q} — 6 divisors. Kernel dim = 6 − 3 = **3**.

Tested at N ∈ {18, 45}:

| N | basis[0] (sub-annihilator) | Full-support combo |
|---|---|---|
| 18 = 3²·2 | (-1, 5, -5, 1, 0, 0) on divs (1,2,3,6,9,18) | (-28, 122, -101, 1, 3, 3) PASS |
| 45 = 3²·5 | (-1, 8, -10, 3, 0, 0) on divs (1,3,5,9,15,45) | (-16, 103, -94, 3, 1, 3) PASS |

basis[0] of N=18 is exactly the N=6=2·3 family annihilator (-1, 5, -5, 1) lifted. basis[0] of N=45 is a SUB-divisor annihilator (-1, 8, -10, 3, 0, 0) on the {1,3,5,9} set, not on {1, 3, 5, 45}.

All combinations verified to rel-err ≤ 10⁻¹⁹⁹ at dps=200. The family extends as a *parametric construction* (kernels are non-empty) but the closed-form parameterization breaks because the rank-deficiency dimension grows beyond 1.

## (4) Literature diff

This is the most important section. **Searched (a) downloaded PDFs via pdftotext grep + (b) ~12 arxiv/SpringerLink/AMS/IAS/LMFDB/OEIS web searches:**

### (4a) Local PDF grep (downloaded-pdfs/)

Searched the following PDFs for terms: `lambert.*annih | eisenstein.*linear | p_1.*p_n | nP_n | level 33 | level 35 | ... | level 115 | composite.*lambert | annihil.*lambert | gcd(pq-1, q-p)`.

| PDF | Hits |
|---|---|
| Ramanujan_39_s_Lost_Notebook_Part_I_2005.pdf | 0 |
| Ramanujan_39_s_Lost_Notebook_Part_II_2008.pdf | 0 |
| Ramanujan_39_s_Lost_Notebook_Part_III_2012.pdf | 0 |
| Ramanujan_39_s_Lost_Notebook_Part_IV_2013.pdf | 0 |
| Berndt NB Part 1 (ramanujankitap1.pdf) | 0 (only generic "Lambert" historical refs) |
| Berndt NB Part V (ramanujan-notebooks-v.pdf) | 0 |
| Berndt-Yee RIMS 2002 (1274-16.pdf) | 0 on annihilator-style identities; many Eisenstein-series identities of OTHER structural form (differential equations, eta-quotients) |
| Berndt-Dixit 2009 (0904.1053v2.pdf) | 0 |
| Berndt-Chan-Zhang 1997 (TAMS_349) | 0 |
| KSRchap3.pdf | 0 |
| hal-03912911.pdf | 0 |
| openai_2026_unit_distance_erdos_remarks.pdf | 0 (unrelated topic) |

**Local PDF verdict: NO PRIOR OCCURRENCE of the specific Lambert-annihilator formula.**

### (4b) Web search (arxiv, SpringerLink, AMS, LMFDB, OEIS)

**Catalog 1: Dixit-Maji-Vatwani family (arXiv:2304.05923, arXiv:2012.12064 "Explicit transformations of certain Lambert series")**. Definition `σ_a^(N)(n) := Σ_{d^N | n} d^a` (note: d^N divides n, NOT d divides N). Different topic; focuses on TRANSFORMATIONS of Sum_n σ_a(n) e^{-ny} via Voronoï-summation, not VANISHING LINEAR COMBINATIONS. **NO MATCH.**

**Catalog 2: Berndt "Lambert series and Ramanujan" (IAS 1993)**. Cited but URL access blocked; based on title, likely covers H-R-B base identity (= our Phase 0 anchor). **PROBABLE PARTIAL MATCH for base identity (which is the standard ζ(2m+1) Ramanujan formula at m=1), but does NOT cover the annihilator family.**

**Catalog 3: Cooper-Ye 2016 "Level 14 and 15 analogues of Ramanujan's elliptic functions to alternative bases" (TAMS)**. Covers Eisenstein series at composite levels 14 = 2·7 and 15 = 3·5. *Different structural form*: their identities are eta-quotient relations and continued-fraction identities, NOT Lambert-annihilator linear combinations. The level-15 identity in Ramanujan's NB II (pp. 255-256, proved by Berndt in NB Part III ch. 21) is *Eisenstein-series identity of level 15* but of the form  η-quotient = polynomial in (E_2, E_4, E_6), not a vanishing linear combination across divisors. **NO MATCH** — different identity structure.

**Catalog 4: Ramanujan-type Z_N construction**. The 2-divisor analogue `Z_N := (N E_2(N τ) − E_2(τ))/(N − 1)` is the **standard "old Eisenstein form" at level N** in the modular forms literature — well-known, appears in many references including Cohen "Factorizations of Eisenstein Series of Level up to 4" (arXiv:2103.07698), Eisenstein series in M_2(Γ_0^*(N)). This is the **2-divisor analogue** of our 4-divisor identity. The pattern extends naturally to 4 divisors at level pq. **CLASSICAL STRUCTURE PRESENT**: the linear-relation existence at level pq is *guaranteed* by the dimension formula (see Catalog 5).

**Catalog 5: dim E_2(Γ_0(N)) for squarefree N (DECISIVE).** It is a **classical fact** that for squarefree N with t prime divisors, the Eisenstein subspace of M_2(Γ_0(N)) has dimension **2^t − 1**:
- t=1 (N prime): dim 1
- t=2 (N=pq): **dim 3** ← *4 candidate Eisenstein series E_2(d·τ) for d ∈ {1, p, q, pq} in a 3-dim space ⟹ exactly 1 non-trivial linear relation*
- t=3 (N=pqr): dim 7 ← 8 candidates ⟹ 1 relation among 8 (but our Phase 3a finding gives kernel dim 5; the discrepancy means the Eisenstein-subspace approach is the *true* dimension and the H-R-B-only approach loses 4 degrees of relation — see "Discrepancy" below)

For N=33 specifically: LMFDB confirms M_2(Γ_0(33)) has total dim 9, cuspidal dim 6, **Eisenstein dim 3**. The 4 functions {E_2(τ), E_2(3τ), E_2(11τ), E_2(33τ)} therefore span a 3-dim space, leaving exactly one linear relation up to scale.

Source: search hit "for squarefree N = ∏ q_j with t prime divisors, E_2(Γ_0(N)) is spanned by 2^t − 1 Eisenstein series" — well-documented in the modular-forms literature (Cohen, Diamond-Shurman, Stein).

**DECISIVE STRUCTURAL FINDING (Catalog 5)**: The *existence* of the family annihilator is a known fact in the modular forms framework (specifically: a 2-codim subspace of a 4-dim space of E_2-class functions guaranteed to have at least one linear relation, which is in fact a 1-dim relation because dim E_2(Γ_0(pq)) = 3). The *specific coefficient formula* in terms of `gcd(pq-1, q-p)` may not appear written-out anywhere in this exact form, but the formula itself is a 5-line consequence of solving a 3×4 linear system by Gaussian elimination (see "Algorithmic derivation" below).

**Discrepancy between Eisenstein-subspace dim (= 2^t − 1) and 3-equation kernel dim (= n_divisors − 3) for t ≥ 3:**

For N = pqr (t=3, n_divisors=8): the 3-equation system gives kernel dim **5**, but the Eisenstein-subspace would give kernel dim 8 − (2^3 − 1) = **1**. The factor-of-5 discrepancy is because:
- The H-R-B base identity is a *weaker* constraint than full E_2-modularity. T_d(α, β) = d·α/24 + β/(24d) − 1/4 only uses the *first three terms* of the E_2 q-expansion's behavior under modular inversion. So at higher levels, the kernel of the H-R-B-projected constraints is *larger* than the kernel of the full modular-form Eisenstein-subspace constraints.
- This means at pqr the family annihilators are NOT all Eisenstein-subspace relations; they include "spurious" relations that follow from the H-R-B constant-only collapse and may not survive at the full q-series level.

This DOES NOT invalidate the numerical verification — Σ c_d T_d = 0 holds for any kernel vector of the 3-equation system, by construction. But it DOES mean the family is *richer at the H-R-B level* than at the modular-form level, and the cog-sci framing should be careful: this is *linear algebra on the H-R-B closed form*, not *modular forms theory*.

### (4c) OEIS

Direct grep on `seq:-1,4,-4,1` returns 942 hits, but the top matches are Bezier-curve coefficients (A065109), product expansions (A284313, A284314, A284499) — none related to Eisenstein/Lambert/composite-level annihilators. The coefficient sequence does not appear to be a recognized OEIS index for our family. **NO MATCH.**

## Algorithmic derivation of the formula (5-line Gaussian elimination)

The "closed-form formula" `c_p = -c_q, c_1 = -c_pq, m·(q-p) = δ·(pq-1)` derives in 5 lines from elementary linear algebra:

```
System (3 equations, 4 unknowns c_1, c_p, c_q, c_pq):
  E1:  c_1 + c_p + c_q + c_pq = 0          (Σ c_d = 0)
  E2:  c_1 + p c_p + q c_q + pq c_pq = 0   (Σ d c_d = 0)
  E3:  c_1 + c_p/p + c_q/q + c_pq/pq = 0   (Σ c_d/d = 0)

Step 1 (E2 - E1):   (p-1) c_p + (q-1) c_q + (pq-1) c_pq = 0   ... (A)
Step 2 (-pq * (E3 - E1)):
                    q(p-1) c_p + p(q-1) c_q + (pq-1) c_pq = 0  ... (B)
Step 3 ((A) - (B)): (p-1)(1-q) c_p + (q-1)(1-p) c_q = 0
                  = -(p-1)(q-1)(c_p + c_q) = 0
              ==> c_p = -c_q       (assuming p, q > 1)
Step 4: Substituting c_p = -c_q in (A): (pq-1) c_pq = -(p-q) c_p
                                       => c_pq = (q-p) c_p / (pq-1)
                  let m = c_p, delta = c_pq:  m (q-p) = delta (pq-1)
                  integer-lowest-height: delta = (q-p)/g, m = (pq-1)/g,
                  where g = gcd(pq-1, q-p).
Step 5: From E1 with c_p = -c_q: c_1 = -c_pq.  So c_1 = -delta.
```

So the closed-form `(c_1, c_p, c_q, c_pq) = (-δ, m, -m, δ)` is **the unique integer-lowest-height parameterization of a 1-dim kernel of a 3×4 system**, derivable in 5 steps. The formula is not surprising, novel, or deep; it's the obvious answer.

## Discussion: what counts as "novel" here?

There are 3 distinct claims, with very different novelty status:

| Claim | Novelty |
|---|---|
| (i) The H-R-B base identity `x L(x) + y L(y) = (x+y)/24 − 1/4 for xy=π²` | CLASSICAL (Hardy-Ramanujan, Berndt expositions; equivalent to the E_2 transformation law `E_2(-1/τ) = τ² E_2(τ) + 6τ/(πi)`). **NOT NOVEL.** |
| (ii) The existence of a 1-dim linear-relation among {T_d(α, β) : d ∣ pq} at squarefree pq | TRIVIAL once H-R-B base identity collapses T_d to a 3-parameter affine function of (α, β). The 3-equation kernel is non-empty whenever there are ≥4 divisors. **NOT NOVEL.** |
| (iii) The explicit closed-form `(c_1, c_p, c_q, c_pq) = (-δ, m, -m, δ)` with `g = gcd(pq-1, q-p)` parameterization | NOT FOUND in literature audit, but trivially derivable via 5-line Gaussian elimination. **NOVEL IF AT ALL ONLY AS A CONVENIENT EXPLICIT FORM**, but unlikely to be publishable on its own merits — the underlying linear-algebra reduction is too elementary. |
| (iv) The claim that this is an *infinite family* of identities at composite squarefree levels | TRUE but the family is parameterized by 2 prime variables (p, q) via the trivial linear-algebra reduction, not by deep modular structure. **NOT NOVEL.** |
| (v) The CONNECTION to the Eisenstein-subspace dimension formula `dim E_2(Γ_0(pq)) = 3` | CLASSICAL but POTENTIALLY USEFUL framing for an exposition paper. **NOT NOVEL** as standalone result. |

**Combined verdict:** The infinite-family claim, while mathematically correct and numerically verified to ≥ 100 digits across 18+ instances, is **NOT a novel discovery**. It is:
- (a) An algebraic CONSEQUENCE of the well-known H-R-B base identity by elementary linear algebra
- (b) An INSTANCE of the well-known dimension formula `dim E_2(Γ_0(pq)) = 3` in the Eisenstein subspace of weight-2 modular forms at squarefree composite level pq

What MAY still be publishable: a clean exposition giving the explicit `gcd(pq-1, q-p)` closed-form coefficients for the integer-lowest-height representative of the 1-dim kernel, perhaps as a short note in a low-tier journal, or as a teaching example in a number-theory text. But it does **not** support the "INFINITE FAMILY of E_2 Lambert annihilator identities" headline framing in diary 55 as a novel scientific result.

## Recalibration of diary 55's "9.5/10 excitement" claim

Diary 55 framed this as "the biggest single result of the session" with "excitement 9.5/10" and proposed venues "Trans. AMS or Math. Comp." with a 6-12 page paper. The literature diff revises this substantially:

- **Trans. AMS / Math. Comp.**: NOT appropriate. Top-tier journals require novel mathematical content; a re-derivation of the well-known `dim E_2(Γ_0(pq)) = 3` consequence via elementary linear algebra would not meet their standards.
- **Math. Mag. / Amer. Math. Monthly / College Math. J.**: POSSIBLE. The closed-form `gcd(pq-1, q-p)` parameterization is a charming explicit formula that could anchor a 2-4 page expository note showing the connection between the H-R-B identity and the dim-3 Eisenstein subspace.
- **arXiv preprint / short note / blog post**: APPROPRIATE. Useful for the record, demonstrates the explicit family, but not a research milestone.

**Revised excitement: 4.5/10** (down from 9.5/10). The numerical verification at 7 new levels + 11 edge cases is solid technical work, but the claim downgrades to "elegant explicit form of a classical result" rather than "novel infinite family".

## What does this mean for the Project C short paper (diary 45)?

The short paper currently positions the Level-33 finding as "first novel from-scratch identity" (Result 5 from diary 48 / commit 4150472). Given this diary's literature diff:

- Keep the Level-33 (and now level-pq family) as a worked example of the engine's `modular_transform_with_correction` operator EXTRACTING the explicit closed form, but
- REFRAME from "novel identity" to "engine-rederived classical Eisenstein-subspace relation"
- Be explicit that the *underlying mathematical content* is classical, but the *engine's autonomous re-derivation* + the *closed-form gcd parameterization* may be the actual novel content
- The strongest claim is **"the engine autonomously rediscovered, in explicit closed form, the linear relation guaranteed by the classical dim E_2(Γ_0(pq)) = 3 dimension formula"** — which is meta-novel (a finding about the engine's capabilities) rather than mathematically novel
- Recommend MOVING this from §5 ("novel identity") to §6 ("toolkit-split / engine capability case study")

## Confidence

- HIGH confidence on numerical verification (25 tests, 5 cells each at dps=200, worst rel-err 3.46e-110 well within 10⁻¹⁰⁰ bar)
- HIGH confidence on structural extensions (rank-3 constraint matrix; family extends to ≥2 distinct prime factors only)
- HIGH confidence on connection to dim E_2(Γ_0(pq)) = 3 (well-established classical result, LMFDB-confirmed at N=33)
- MEDIUM-HIGH confidence on novelty assessment: the EXPLICIT FORMULA may not be in the literature exactly as stated, but the underlying STRUCTURE is classical; the formula is derivable in 5 lines from elementary linear algebra applied to the H-R-B base identity, so even if not explicitly written down before, it is at most a "very minor explicit specialization of a well-known dim-counting fact"
- MEDIUM confidence on the diary-55 9.5/10 → 4.5/10 recalibration: depends partially on what the user wants to claim in the paper. If the paper is honest about the classical structure and only claims novelty for the engine's autonomous rederivation + explicit form, then 4.5/10 is appropriate; if it's framed as "discovery of an infinite family of identities", that overclaim is not supportable.

## Tasks queued

- **#79**: Update diary 55's framing (and the short paper draft) to reflect the classical-structure / engine-rederivation reframing. Specifically: remove "infinite family of novel identities" and replace with "engine-rederived classical Eisenstein-subspace relation, explicit gcd(pq-1, q-p) closed form".
- **#80**: Investigate whether the *engine's autonomous discovery* of this closed form (via `modular_transform_with_correction` + algebraic preprocessing) is itself novel as an engine-capability demonstration. If so, this becomes the cleaner publication angle: "an autonomous proof engine rediscovers and explicitly parameterizes a classical Eisenstein-subspace relation" — which is a positive cog-sci / AI-for-math finding even if the math itself is classical.
- **#81**: If pursuing publication, check whether the explicit `gcd(pq-1, q-p)` parameterization for the integer-lowest-height kernel basis appears in: (a) Cohen's "Number Theory Vol I: Tools and Diophantine Equations" or "Vol II: Analytic and Modern Tools" (modular forms chapters); (b) Diamond-Shurman "A First Course in Modular Forms"; (c) Stein's "Modular Forms, A Computational Approach" (Chapter on Eisenstein subspaces). These are standard references that may contain or explicitly omit the gcd-parameterization.
- **#82**: At the deeper structural level: investigate the *Atkin-Lehner eigensystem* connection. The sign pattern `(c_1, c_p, c_q, c_pq) = (-, +, -, +) = (-1)^{number of prime factors}` suggests an Atkin-Lehner eigenform structure. From search Catalog 2: `E^(ε)_{k,N}(z) := Σ_{d|N} ε(d) d^{k/2} E_k(dz)` for Atkin-Lehner eigensystem ε is a known construction. Verify whether our annihilator IS (or is closely related to) the Atkin-Lehner-twisted Eisenstein construction with the specific eigensystem signed by Möbius-like character. If so, this is *another* known structural fact that the engine "rediscovered". This would clarify the formula's content further.
- **#83**: Update `insights/CANDIDATE_INSIGHTS.md` (Result 5 entry) and `insights/DID_NOT_PAN_OUT.md` to reflect the novelty downgrade. The "12 instances + closed-form" stays as a TECHNICAL achievement; the "INFINITE FAMILY of novel identities" framing moves to DID_NOT_PAN_OUT as a partial-falsification of the novelty claim.

## Bottom line

**Numerical verification: 25/25 tests PASS at dps=200, rel-err ≤ 10⁻¹¹⁰ across all cases (worst 3.46e-110 at level 391 edge case; most ≤ 10⁻¹⁹⁹).** The formula is mathematically correct, the family extends as claimed for squarefree pq (and beyond, with multi-dim kernels for pqr/p²q), and the structural-extension test pinpoints exactly where it fails (prime powers p²: kernel dim 0, no annihilator exists).

**Literature diff: the underlying structural fact is CLASSICAL.** The H-R-B base identity is well-known; the existence of a 1-dim relation at level pq follows from the well-known `dim E_2(Γ_0(pq)) = 3` dimension formula. The specific `gcd(pq-1, q-p)` explicit closed-form parameterization for the integer-lowest-height kernel basis may not appear in this exact form in our literature audit, but it is derivable in 5 lines of elementary linear algebra and is unlikely to constitute a "novel identity" by research-mathematics standards.

**Verdict: PARTIAL-PRIOR-OCCURRENCE.** Specific formula novel-as-explicit-form but structure classical. Diary 55's "INFINITE FAMILY of novel identities" framing must be downgraded. The cleanest remaining claim is *the engine autonomously rediscovered, in explicit closed form, the linear relation guaranteed by the classical dim E_2(Γ_0(pq)) = 3 result* — which is meta-novel (engine capability) but not mathematically novel.

**Time spent:** ~70 minutes (15 min script design, 25 min run + iteration, 25 min literature search, 5 min diary).
