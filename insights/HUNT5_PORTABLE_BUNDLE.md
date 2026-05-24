# Hunt 5 portable bundle — shareable with other Claude sessions

Purpose: This file is a self-contained dump of the Hunt 5 closure deliverables
(diary 20 + verdict CSV + per-section tagging CSV + responses to the three
specific questions asked in parallel review) for sharing with other Claude /
agent sessions that can't access the `jounih/ramanujan-mining` repo directly.

Copy from `---BEGIN PASTE---` to `---END PASTE---` into the other session.

---BEGIN PASTE---

# Hunt 5 closure — Quarterly Reports operator tagging (Ramanujan mining run)

This is the full package: methodology, numbers, per-section tagging, and
answers to three follow-up questions. Self-contained for review.

## TL;DR

**Claim:** HUNT_MAP §5 predicted that 6 specific operators would cover ≥80%
of the math sections in Ramanujan's three Quarterly Reports. Tested against
Berndt's 2022 HRJ reproduction (faithful copy of Satagopan's 1925 handwritten
copy of the lost originals; 5519 lines / 33 math sections after excluding 5
meta sections). **Found 57.6% coverage** — predicted basis falsified.
**Revised 7-operator basis covers ~91%.** Underlying latent-space-speedrun
hypothesis supported with corrected basis.

The shape of the failure is the real finding: QR III is not a modular-forms
document at all. It is fractional-iteration / Hardy-orders / operator-calculus
(Schröder/Koenig, Riemann-Liouville, umbral), which 60+ years of Hardy/Watson/
Berndt-curated reception has under-read. QR III uses *zero* modular-form
notation across 11 math sections.

## Method

- Hand-tagging, not regex. The schema's regex tests are calibrated against
  textbook notation; Ramanujan rarely names operators and uses archaic
  notation (`Z ∞` for `∫₀^∞`; `n .` for `n!`; `Π(x)` for `Γ(x+1)`; …).
- Section-level granularity: one tag per Ramanujan-numbered section
  (§1, §2, ...; (i), (ii), ...; (a), (b), ...). Boundaries are Ramanujan's
  own, not imposed.
- Binary scoring: a section uses an operator (primary OR secondary) or not.
- Excluded 5 meta sections (validity discussions, foundational interpolation
  arguments) from the 80% denominator. These are sections *about* the
  operators, not using them.

## Numbers

### Per-report coverage by the 6-operator predicted basis

| Report | n_math | n_in_basis | % | meets ≥80%? |
|---|---|---|---|---|
| QR1 (5 Aug 1913) | 13 | 13 | 100.0% | YES |
| QR2 (7 Nov 1913) | 9  | 6  | 66.7%  | NO |
| QR3 (9 Mar 1914) | 11 | 0  | 0.0%   | NO |
| **ALL** | 33 | 19 | **57.6%** | **NO** |

### Predicted-operator usage (all math sections)

| Operator | n_sections |
|---|---|
| `master_theorem` | 19 |
| `mellin_inversion` | 17 |
| `q_shift` | 0 |
| `modular_S_transform` | 0 |
| `eisenstein_normal_ordering` | 0 |
| `class_field_galois_average` | 0 |

Vocabulary check on the raw text (5519 lines): zero occurrences of `\tau`,
`\theta`, `\eta`, "Bernoulli", "Heegner", "Eisenstein", "modular",
"class invariant", "elliptic", "Lambert", "continued fraction". One
occurrence of "Eulerian" (naming the gamma integral).

### Out-of-schema operators that fired (the empirical correction)

| Operator | n_sections | Where |
|---|---|---|
| `FOURIER_SELF_RECIPROCITY` | 5 | QR II §7 (Theorem III); QR III §13, §14, §15 |
| `FRACTIONAL_FUNCTIONAL_ITERATION` | 5 | QR III §4-§6, §8, §9, §10 |
| `HARDY_ORDERS_OF_INFINITY` | 3 | QR III §7, §8, §9 |
| `FRULLANI_LIMIT` | 2 | QR II §4 (Theorem II), §5 |
| `MULTISECTION_ROOTS_OF_UNITY` | 1 | QR II — cubic-roots-of-unity factoring of `1 - x³/3! + x⁶/6! - ...` |
| `RIEMANN_LIOUVILLE_FRACTIONAL_DIFF` | 1 | QR III §11 |
| `UMBRAL_OPERATOR_SUBSTITUTION` | 1 | QR III §12 |
| `PARTIAL_FRACTION_OF_INFINITE_PRODUCT` | 1 | QR III §13 |
| `BANDLIMITED_FOURIER_DISCONTINUITY` | 1 | QR III §14 |
| `MELLIN_PAIR_RECIPROCITY` | 1 | QR III §15 |

## Surprises

1. QR I confirmed the 80% prediction cleanly (13/13 = 100%); the failure is
   entirely in QR II and especially QR III.
2. Modular forms simply don't appear in the QRs. Three of the six predicted
   operators (`modular_S_transform`, `eisenstein_normal_ordering`,
   `class_field_galois_average`) were predicted on the basis of "QR III
   demonstrates Ramanujan's modular toolkit." That prediction is falsified.
3. `q_shift` also doesn't fire despite the surface presence of an infinite
   product `(1+x)(1+ax)(1+a²x)···` in QR I §5(v). Ramanujan treats it as an
   ordinary Taylor series and reduces to the Master Theorem — never invokes
   `(a;q)_n`, the q-binomial theorem, `D_q`, or Heine.
4. QR III is a different mathematical universe from QR I and QR II:
   - QR I: Master Theorem manifesto. One operator, ~10 worked applications.
   - QR II: Master-Theorem-with-extensions. Adds Frullani limit (Theorem II)
     and Fourier cos/sin self-reciprocity (Theorem III), plus a brief
     multisection.
   - QR III: Foundations and operator calculus. Discusses uniqueness of
     interpolation (§1-§3); fractional iteration of functions via
     Schröder/Koenig (§4-§6, §10); Hardy orders of infinity (§7-§9);
     Riemann-Liouville fractional differentiation (§11); shift and difference
     operators umbrally (§12); partial-fraction decomposition of infinite
     products (§13); Mellin-pair self-reciprocity theorems (§14, §15).
     **The Master Theorem appears in QR III only as a consistency check** on
     the operator calculus (§12), not as a primary move.
5. The latent-space-speedrun hypothesis is supported by a small toolkit per
   report — just not the predicted one. Within each report the active toolkit
   is small: QR I uses essentially 2, QR II uses ~4, QR III uses ~6-7.
6. The revised 7-operator basis:
   - Kept: `mellin_inversion`, `master_theorem`
   - Dropped: `q_shift`, `modular_S_transform`, `eisenstein_normal_ordering`,
     `class_field_galois_average`
   - Added: `FOURIER_SELF_RECIPROCITY`, `FRACTIONAL_FUNCTIONAL_ITERATION`,
     `HARDY_ORDERS_OF_INFINITY`, `FRULLANI_LIMIT`, `MELLIN_PAIR_RECIPROCITY`
   - Coverage: 30/33 = 90.9%. The 3 left out are QR II's multisection,
     QR III §11 RL, §12 umbral, §13 partial-fractions — adding 1-2 more
     QR-III-specific operators would cover those.

## Answers to the three follow-up questions

### Q1: Which exact additional operators became the 7th (i.e. the additions)?

Five additions, listed above. The corrected basis is:

1. `mellin_inversion` (kept)
2. `master_theorem` (kept)
3. `FOURIER_SELF_RECIPROCITY` — added (5 sections; QR II Theorem III + QR III
   §13, §14, §15)
4. `FRACTIONAL_FUNCTIONAL_ITERATION` — added (5 sections; QR III §4-§6,
   §8, §9, §10; Schröder/Koenig)
5. `HARDY_ORDERS_OF_INFINITY` — added (3 sections; QR III §7-§9)
6. `FRULLANI_LIMIT` — added (2 sections; QR II §4-§5; the n→0 limit move on
   a parametric Master-Theorem identity)
7. `MELLIN_PAIR_RECIPROCITY` — added (1 section; QR III §15; generalises
   Fourier-pair self-inversion to arbitrary Mellin-pairs F, f defined by
   ∫₀^∞ F(ax) f(bx) dx = 1/(a+b))

Three additional QR III-specific operators show up once each and didn't make
the 7-operator basis (would need an 8-9-operator basis to cover them):
- `RIEMANN_LIOUVILLE_FRACTIONAL_DIFF` (QR III §11)
- `UMBRAL_OPERATOR_SUBSTITUTION` (QR III §12)
- `PARTIAL_FRACTION_OF_INFINITE_PRODUCT` (QR III §13)

### Q2: Does QR III have latent connections back to modular forms?

Yes, but they are *deeply hidden* and Ramanujan never makes them explicit.
Four shadow-connections I'd flag:

1. **QR III §6(b) Chebyshev iteration ↔ degenerate j-function dynamics.**
   Ramanujan computes F^n for F(x) = x² - 2 explicitly via cosh-form
   linearisation. The Chebyshev semigroup is the genus-0 limit of the
   j-function modular dynamics (collapsing the elliptic structure at the
   degenerate cusps). The Schröder linearisation σ(x) = arccos(x/2)
   conjugates F to the angle-doubling map on the circle — this IS what's
   left of the modular dynamics after the elliptic collapse.
2. **QR III §15 Mellin-pair reciprocity ⊃ Poisson summation.** The
   reciprocal-pair theorem (∫F(ax)f(bx) dx = 1/(a+b)) generalises Fourier
   self-inversion. Its degenerate Gaussian case IS Poisson summation, which
   is the standard proof route to theta modularity. So §15 is structurally a
   *higher-generality* shadow of theta modularity.
3. **QR III §11 Mellin kernel x^{n-1} ↔ Riemann ζ asymptotics.** The
   Riemann-Liouville integral has the Mellin-transform kernel; the Mellin
   transform of ζ(s) is the most-used analytic-number-theory bridge. Less
   direct than (1) and (2) but real.
4. **QR III §7-§9 Hardy orders of infinity ↔ asymptotic moduli of modular
   coefficients.** Hardy's ≺ hierarchy is the formal backbone of asymptotic
   estimates of modular-form Fourier coefficients (e.g. Hardy-Ramanujan's
   p(n) asymptotic). Ramanujan's QR III §8 construction of a function
   defying all logarithmic scales doesn't invoke ζ, but the scale-hierarchy
   machinery is what later feeds the Selberg-trace-formula style estimates.

Re-framing this gives the QR-vs-Notebooks contrast a sharper shape: QR III
is *not* a disjoint toolkit from the Notebooks; it's a *more abstract layer*
that contains the modular case as a degenerate specialisation. The Notebooks
then do the actual identity-discovery work in the degenerate specialisation.

### Q3: Did the agent hold discipline on near-matches?

Yes, explicitly. Examples from the per-section index (the "note" fields):

- **QR I §5(v)** (the infinite product example):
  > "Surface notation involves a q-Pochhammer-like product. But Ramanujan
  > does NOT use (a;q)_n notation, D_q, Heine, or the q-binomial theorem.
  > He treats the product as an ordinary Taylor series in x and reduces to
  > Master Theorem. So this does NOT trigger the schema's q_shift detector
  > (correctly: the operator move is Master Theorem, not q-shift)."

- **QR II §7 (Theorem III, Fourier cos/sin self-reciprocity):**
  > "The 6-operator MELLIN_INVERSION is conceptually similar (continuous
  > transform self-inverse) but the schema's regex looks for Mellin-specific
  > signatures (x^{s-1}, Bromwich, Γ(s)) — Fourier cos has none of these."
  > → tagged as the separate `FOURIER_SELF_RECIPROCITY`, not as
  > `mellin_inversion`.

- **QR III §11 (Riemann-Liouville fractional diff):**
  > "Has a Mellin-style kernel x^{n-1} but is not what schema mellin_inversion
  > detects; the schema looks for x^{s-1} F(x) where F is a function, not
  > f^{(r)}. ... distinct operator move."

- **QR III §12 (Umbral operator calculus):**
  > "The MASTER_THEOREM appears here AS A CHECK / consistency test:
  > substituting E for a scalar a in the Mellin integral gives back the
  > Master Theorem statement. Methodologically interesting — Ramanujan is
  > using the Master Theorem as a check on his operator calculus." → tagged
  > as `UMBRAL_OPERATOR_SUBSTITUTION` only, not `master_theorem`.

The same discipline that caught noisy positives during the FEP × mock-modular
investigation (per `insights/DID_NOT_PAN_OUT.md`) was held here too.

## Caveats

- The Berndt HRJ 2022 reproduction is a typeset, lightly-edited version of
  Satagopan's 1925 handwritten copy of originals that no longer exist.
  Editorial substitutions are documented (`n .` → `!`; `Π(x)` → `Γ(x+1)`;
  commas/periods inserted; display math reformatted).
- Section boundaries are Ramanujan's own. No imposed granularity.
- Hand-judgment tagging can be audited by reading the cited HRJ line ranges.

## Raw verdict CSV (5 lines)

```
scope,n_math_sections,n_in_predicted_basis,pct_in_predicted_basis,meets_80pct_prediction,predicted_operator_uses,extra_operator_uses
QR1,13,13,100.0,True,"{""master_theorem"": 13, ""mellin_inversion"": 13}",{}
QR2,9,6,66.7,False,"{""master_theorem"": 6, ""mellin_inversion"": 4}","{""MULTISECTION_ROOTS_OF_UNITY"": 1, ""FRULLANI_LIMIT"": 2, ""FOURIER_SELF_RECIPROCITY"": 2}"
QR3,11,0,0.0,False,{},"{""FRACTIONAL_FUNCTIONAL_ITERATION"": 5, ""HARDY_ORDERS_OF_INFINITY"": 3, ""RIEMANN_LIOUVILLE_FRACTIONAL_DIFF"": 1, ""UMBRAL_OPERATOR_SUBSTITUTION"": 1, ""PARTIAL_FRACTION_OF_INFINITE_PRODUCT"": 1, ""FOURIER_SELF_RECIPROCITY"": 3, ""BANDLIMITED_FOURIER_DISCONTINUITY"": 1, ""MELLIN_PAIR_RECIPROCITY"": 1}"
ALL,33,19,57.6,False,"{""master_theorem"": 19, ""mellin_inversion"": 17}","{""MULTISECTION_ROOTS_OF_UNITY"": 1, ""FRULLANI_LIMIT"": 2, ""FOURIER_SELF_RECIPROCITY"": 5, ""FRACTIONAL_FUNCTIONAL_ITERATION"": 5, ""HARDY_ORDERS_OF_INFINITY"": 3, ""RIEMANN_LIOUVILLE_FRACTIONAL_DIFF"": 1, ""UMBRAL_OPERATOR_SUBSTITUTION"": 1, ""PARTIAL_FRACTION_OF_INFINITE_PRODUCT"": 1, ""BANDLIMITED_FOURIER_DISCONTINUITY"": 1, ""MELLIN_PAIR_RECIPROCITY"": 1}"
```

## Raw per-section tagging CSV (38 sections)

```
report_id,date,section_id,title,type,is_meta,line_start,line_end,operators_predicted_basis,operators_extra,in_predicted_basis,note
QR1,1913-08-05,qr1_sec_1,Subject of the paper — statement of the Master Theorem,theorem_statement,False,158,175,master_theorem;mellin_inversion,,True,
QR1,1913-08-05,qr1_sec_2,A:- Proof of the Master Theorem,proof,False,176,308,master_theorem;mellin_inversion,,True,
QR1,1913-08-05,qr1_sec_3,When valid? — convergence conditions,validity_discussion,True,309,338,,,True,
QR1,1913-08-05,qr1_sec_4,Generalization — substitution rules,extension,True,345,363,,,True,
QR1,1913-08-05,qr1_sec_5i,Example (i): ∫₀^∞ x^{m-1}/(1+x^n) dx = π/(n sin(πm/n)),worked_example,False,367,461,master_theorem;mellin_inversion,,True,
QR1,1913-08-05,qr1_sec_5ii,Example (ii): Beta function ∫₀^1 x^{m-1}(1-x)^{n-1} dx = Γ(m)Γ(n)/Γ(m+n),worked_example,False,466,519,master_theorem;mellin_inversion,,True,
QR1,1913-08-05,qr1_sec_5iii,Example (iii): ∫₀^∞ x^{n-1} cos(px) dx = Γ(n) cos(πn/2) / p^n,worked_example,False,520,611,master_theorem;mellin_inversion,,True,
QR1,1913-08-05,qr1_sec_5iv,Example (iv): Bessel-function integral via Master Theorem,worked_example,False,612,646,master_theorem;mellin_inversion,,True,
QR1,1913-08-05,qr1_sec_5v,Example (v): ∫₀^∞ x^{n-1} dx / ∏_{k≥0}(1+a^k x) and triangular-number identity,worked_example,False,647,826,master_theorem;mellin_inversion,,True,"Surface notation involves a q-Pochhammer-like product. But Ramanujan does NOT use (a;q)_n notation, D_q, Heine, or the q-binomial theorem. He treats the product as an ordinary Taylor series in x and reduces to Master Theorem. So this does NOT trigger the schema's q_shift detector (correctly: the operator move is Master Theorem, not q-shift)."
QR1,1913-08-05,qr1_sec_5vi,Example (vi): ∫₀^∞ Γ(x+a)/(x^m Γ(x+a+n+1)) dx,worked_example,False,828,989,master_theorem;mellin_inversion,,True,
QR1,1913-08-05,qr1_sec_6_intro,B. Converse of A — Expansions of functions using the theorem,extension,False,991,997,master_theorem;mellin_inversion,,True,
QR1,1913-08-05,qr1_sec_6i,B.(i): Expansion of (2/(1+√(1+4x)))^n,worked_example,False,998,1131,master_theorem;mellin_inversion,,True,This is functionally Lagrange inversion done via Master Theorem.
QR1,1913-08-05,qr1_sec_6ii,B.(ii): Expansion of (x+√(1+x²))^{-n},worked_example,False,1137,1295,master_theorem;mellin_inversion,,True,
QR1,1913-08-05,qr1_sec_6_3,"B.(3): Given log x / x = -a, find expansion of x^n in powers of a",worked_example,False,1297,1370,master_theorem;mellin_inversion,,True,The φ(p)=n(n+p)^{p-1} formula is the Cayley tree formula / Lambert-W coefficients.
QR1,1913-08-05,qr1_sec_6_4,"B.(4): Given aq·x^p + x^q = 1, find expansion of x^n in powers of a",worked_example,False,1372,1525,master_theorem;mellin_inversion,,True,"This is the explicit power-series formula for a root of an algebraic equation in terms of the equation's coefficients — Lagrange inversion in its most general form, done via Master Theorem."
QR2,1913-11-07,qr2_sec_a,Further example (a): ∫₀^∞ x^{r-1}(1-2mx/1!+3m²x²/2!-...) dx = Γ(r)(1-r)^m,worked_example,False,1543,1620,master_theorem;mellin_inversion,,True,
QR2,1913-11-07,qr2_sec_b,Further example (b): Expand e^{ax} in powers of e^{-bx} sin(cx)/c (Lagrange-like inversion),worked_example,False,1622,1884,master_theorem;mellin_inversion,,True,
QR2,1913-11-07,qr2_sec_2_3,§2-§3: Convergence and validity discussion of (b),validity_discussion,True,1886,1928,,,True,
QR2,1913-11-07,qr2_sec_3_particulars,Particular cases (a)-(d) of (b),worked_examples,False,1929,2086,master_theorem,,True,
QR2,1913-11-07,qr2_sec_3_cubic_roots,Roots of 1 - x³/3! + x⁶/6! - ... = 0 via cube roots of unity,worked_example,False,2086,2280,,MULTISECTION_ROOTS_OF_UNITY,False,"The multisection (∑_{n≡0 mod 3} x^{3n}/(3n)! extracted by averaging exp at 1, ω, ω²) is a distinct operator move. The 6-operator schema does not predict it. ChatGPT's broader taxonomy has FINITE_GAUSS_COLLAPSE which is the closest match."
QR2,1913-11-07,qr2_sec_4,§4: Theorem II — Frullani-extended Master Theorem,theorem,False,2287,2615,master_theorem;mellin_inversion,FRULLANI_LIMIT,True,"The Frullani-limit move (n→0 in a Master-Theorem identity) is a distinct operator. The 6-operator schema does not capture this specific limit, though MASTER_THEOREM itself is the underlying primitive."
QR2,1913-11-07,qr2_sec_5,§5: Examples of Theorem II — Frullani as special case,worked_examples,False,2616,2869,master_theorem,FRULLANI_LIMIT,True,
QR2,1913-11-07,qr2_sec_6,§6: Corollaries (1)-(8) to Theorem I — cos/sin variants,corollaries,False,2884,3149,master_theorem;mellin_inversion,,True,
QR2,1913-11-07,qr2_sec_7,§7: Theorem III — Fourier cosine/sine self-reciprocity,theorem,False,3158,3239,,FOURIER_SELF_RECIPROCITY,False,"This is the Fourier cosine inversion theorem (modern: F_c·F_c = π/2·Id). It is NOT one of the 6 predicted operators. The 6-operator MELLIN_INVERSION is conceptually similar (continuous transform self-inverse) but the schema's regex looks for Mellin-specific signatures (x^{s-1}, Bromwich, Γ(s)) — Fourier cos has none of these."
QR2,1913-11-07,qr2_sec_7_examples,Examples of Theorem III + closing integrals,worked_examples,False,3239,3457,,FOURIER_SELF_RECIPROCITY,False,
QR3,1914-03-09,qr3_sec_1,§1: Validity of Theorem I revisited — nature of u_n,validity_discussion,True,3481,3510,,,True,
QR3,1914-03-09,qr3_sec_2_3,§2-§3: Uniqueness of the function passing through u_n,foundational_argument,True,3511,3556,,,True,"This is a meta-discussion about interpolation, important as a foundation for all subsequent fractional-iteration / fractional-differentiation work but not itself an operator move."
QR3,1914-03-09,qr3_sec_4_5,§4-§5: Fractional Order of Functions — definition of F^n,definition_and_examples,False,3557,3641,,FRACTIONAL_FUNCTIONAL_ITERATION,False,This is the entry point to Ramanujan's fractional iteration theory. Closely related to the Schröder / Koenig functional equation tradition. Not in the 6-operator schema.
QR3,1914-03-09,qr3_sec_6,§6: Conjugation theorem for fractional iteration + examples,theorem_and_examples,False,3643,3950,,FRACTIONAL_FUNCTIONAL_ITERATION,False,"Schröder conjugation: F^n acts on a fixed-point-free function by conjugating to a 'normal form' φ where the iterate is easy (a power map). Example (b) — F(x) = x²-2 has the Chebyshev semigroup as its iteration; F^{log 3/log 2}(x) = x³-3x and so on, which Ramanujan computes explicitly."
QR3,1914-03-09,qr3_sec_7,§7: Orders of Infinity — Hardy ≺ notation,definitions,False,3958,3983,,HARDY_ORDERS_OF_INFINITY,False,
QR3,1914-03-09,qr3_sec_8,§8: Construction of a function defying all logarithmic scales,construction,False,4034,4181,,HARDY_ORDERS_OF_INFINITY;FRACTIONAL_FUNCTIONAL_ITERATION,False,
QR3,1914-03-09,qr3_sec_9,§9: Scales of Orders of Infinity — theorem that the number of scales is infinite,theorem,False,4182,4287,,HARDY_ORDERS_OF_INFINITY;FRACTIONAL_FUNCTIONAL_ITERATION,False,
QR3,1914-03-09,qr3_sec_10,§10: Expand f^r(x) in ascending powers of r — derives ψ_1(x) = C/F(x),theorem_and_derivation,False,4288,4456,,FRACTIONAL_FUNCTIONAL_ITERATION,False,This is the Lie-theoretic / generator-of-flow content of fractional iteration. Modern: ψ_1 is the vector field of the iteration flow.
QR3,1914-03-09,qr3_sec_11,§11: Fractional Order of Differentiation,theorem_and_examples,False,4458,4561,,RIEMANN_LIOUVILLE_FRACTIONAL_DIFF,False,"This is the Riemann-Liouville fractional derivative via the Cauchy formula, but with the role of f and its derivatives flipped (operates on f^{(r)}, returns f^{(r-n)}). Has a Mellin-style kernel x^{n-1} but is not what schema mellin_inversion detects; the schema looks for x^{s-1} F(x) where F is a function, not f^{(r)}."
QR3,1914-03-09,qr3_sec_12,"§12: The Use of Operators — shift E, difference Δ",theorem_and_examples,False,4562,4805,,UMBRAL_OPERATOR_SUBSTITUTION,False,Heaviside / umbral operator calculus. The MASTER_THEOREM appears here AS A CHECK / consistency test: substituting E for a scalar a in the Mellin integral gives back the Master Theorem statement. Methodologically interesting — Ramanujan is using the Master Theorem as a check on his operator calculus.
QR3,1914-03-09,qr3_sec_13,§13: Partial fractions of an infinite product → cos integrals,theorem_and_examples,False,4806,4956,,PARTIAL_FRACTION_OF_INFINITE_PRODUCT;FOURIER_SELF_RECIPROCITY,False,
QR3,1914-03-09,qr3_sec_14,§14: Finite-vs-infinite Fourier — discontinuous-bandwidth theorem,theorem,False,5044,5108,,BANDLIMITED_FOURIER_DISCONTINUITY;FOURIER_SELF_RECIPROCITY,False,The bandlimited variant of Theorem III. This is essentially the Paley-Wiener phenomenon: compactly-supported φ has Fourier transform that 'looks band-pass' against trial functions.
QR3,1914-03-09,qr3_sec_15,§15: Reciprocal-pair theorem — Mellin pair self-reciprocity + Bessel/Fourier corollaries,theorem_and_corollaries,False,5111,5519,,MELLIN_PAIR_RECIPROCITY;FOURIER_SELF_RECIPROCITY,False,"Most general reciprocity theorem in the QRs. Uses MASTER_THEOREM in the proof (line 5234, line 5275) but the *operator* is Mellin-pair reciprocity — a generalization of Mellin self-inversion to pairs of functions."
```

---END PASTE---
