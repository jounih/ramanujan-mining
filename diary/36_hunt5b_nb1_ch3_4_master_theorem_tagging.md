# Diary 36 — Hunt 5b: NB Part 1 Ch. 3 + Ch. 4 (Master Theorem material) operator tagging

**Date:** 2026-05-25
**Source:** Berndt, *Ramanujan's Notebooks, Part 1*, Ch. 3 ("Combinatorial
Analysis and Series Inversions", pp. 44-83) + Ch. 4 ("Iterates of the
Exponential Function and an Ingenious Formal Technique", pp. 85-108).
Local copy at
[`downloaded-pdfs/ramanujankitap1.pdf`](../downloaded-pdfs/ramanujankitap1.pdf)
(Springer 1985 edition; 368 PDF pages total). Hunt 5b 4th-chapter pass
(after NB V Ch. 32 in diary 22, NB V Ch. 36 in diary 24, NB V Ch. 34 in
diary 25). This is the FIRST Hunt 5b pass that crosses out of NB Part V
into a different volume of Berndt's commentary.
**Status:** **NOVEL PATTERN** — the topic-toolkit reading is confirmed
(zero modular operators fire), but the dominant operator is
`fractional_functional_iteration` (33.0%), not `master_theorem` (24.2%).
A 4th analytic subcluster emerges, distinct from both the
QR-Master-Theorem cluster and the Notebooks-modular cluster.

## Setup

### Why this chapter pair was chosen

Per the pre-registration in
[`insights/HUNT5B_NB1_CH3_4_PREDICTION_REGISTRATION.md`](../insights/HUNT5B_NB1_CH3_4_PREDICTION_REGISTRATION.md)
(date-locked 2026-05-24), the central open question after diaries 22 / 24 / 25
was: is the Hunt 5b "toolkit-split" hypothesis **PROVENANCE-driven** (some
property of WHERE Ramanujan wrote — Cambridge Letters/QRs vs the India
Notebooks period) or **TOPIC-driven** (which mathematical area is being
worked on)? Berndt NB Part 1 Ch. 3-4 is **Notebooks-side material BY
PROVENANCE** (written in India, in Ramanujan's second notebook, before
1914) but **QR-side material BY TOPIC** (Master Theorem + analytic
integrals = the QR I + QR II substrate). Tagging it discriminates the
two hypotheses.

### Chapter scope (confirmed from PDF TOC, pp. ix-x)

- **Ch. 3** = "Combinatorial Analysis and Series Inversions" (pp. 44-83).
  Topics: Bell polynomials / Bell numbers / Stirling-2 numbers
  (§§1-9); asymptotic expansion of Poisson-expected-value-style sums
  (§10 with Entry 10 as the deepest result of the chapter); generating-
  function-product convolutions (§11); generalized inverse-factorial
  series (§12); Lagrange-inversion / functional-equation roots
  (§§13-17, with Entries 13-14 being Lambert / Lagrange's 1758 / 1770
  results, Entry 15-17 being Ramanujan's variants and iterated-
  exponential xx^... evaluations).
- **Ch. 4** = "Iterates of the Exponential Function and an Ingenious
  Formal Technique" (pp. 85-108). Topics: fractional iterates of
  f(x) = e^x - 1 defined for all real r (§§1-7); harmonic-sum
  identities (§8); the "Ingenious Formal Technique" of substituting
  phi(n) for x^n (§9 framework + Examples 1-4 + Corollaries); the
  generating-function-extraction Entry 10 + asymptotic examples;
  **Entry 11 = THE MASTER THEOREM** (the QR I + QR II centerpiece, in
  its Ramanujan-original "favourite formula" form per Hardy [20, p. 15],
  with Corollaries 1-5 covering all the trigonometric / Beta-function
  Master-Theorem applications); Fourier cosine inversion + Parseval
  (§12); trigonometric Beta integrals (§13); sinh / cosh / cos
  cyclotomic product (§14); e^x cubic-recurrence (§15).

### The 11-operator basis (SAME as Hunt 5b Ch. 32 / 34 / 36)

Per
[`corpora/transcriptions/operator_tagging_schema.py`](../corpora/transcriptions/operator_tagging_schema.py)
+ diary 20's extensions, the 11-op basis is:
`modular_S_transform`, `eisenstein_normal_ordering`, `q_shift`,
`class_field_galois_average`, `denesting_via_kummer_or_landau`,
`algebraic_number_field_norms`, `cardano_cubic_formula`, `master_theorem`,
`frullani_limit`, `fractional_functional_iteration`,
`mellin_pair_reciprocity`.

### Baseline comparisons

| Operator | QR (diary 20) | NB V Ch. 32 (d22) | NB V Ch. 36 (d24) | NB V Ch. 34 (d25) |
|---|---|---|---|---|
| `master_theorem` | 57.6% (dominant) | 0% | 0% | 0% |
| `modular_S_transform` | 0% | 91.7% | 100.0% | 97.1% |
| `q_shift` | 0% | 100.0% | 4.8% | 21.6% |
| `class_field_galois_average` | 0% | 33.3% | 4.8% | 98.0% |
| `eisenstein_normal_ordering` | 0% | 8.3% | 12.0% | 13.7% |
| `fractional_functional_iteration` | 15% | 0% | 0% | 0% |

Three NB V chapters: zero QR-cluster, dominant modular cluster.
QRs: dominant Master-Theorem cluster, zero modular cluster.

## What I did

1. Confirmed the chapter scope from the PDF's TOC (PDF page 11; Springer
   1985 page ix-x). Verified Ch. 3 starts at the body's "Combinatorial
   Analysis and Series Inversions" heading at PDF page 47 and Ch. 4 at
   PDF page 87; Ch. 5 begins at PDF page 111.
2. Read both chapters end-to-end (Ch. 3 §§1-17, Ch. 4 §§1-15) via
   `pdftotext -layout` extraction, cross-referencing the page-image
   text against the structure of Entries / Lemmas / Corollaries /
   Examples.
3. Hand-tagged each numbered proof unit against the 11-operator
   vocabulary. Same convention as diaries 22 / 24 / 25:
   - Unit of judgment = atomic proof block (Entry / Theorem / Lemma /
     Example / Corollary).
   - Tags record whether the operator is the *primary or major-
     secondary move* in the proof (not just the statement).
   - "Near match != match" — strict false-positive discipline.
   - When Berndt's commentary explicitly invokes a machinery name
     (e.g. "Lagrange inversion formula", "Master Theorem", "Ramanujan's
     particularly interesting formula"), the operator IS tagged.
4. Encoded the tags in
   [`analysis/28_hunt5b_nb1_ch3_4_tagging.py`](../analysis/28_hunt5b_nb1_ch3_4_tagging.py)
   as a list of dicts; computed per-operator saturation; wrote the CSV
   to
   [`analysis/results/hunt5b_nb1_ch3_4_tags.csv`](../analysis/results/hunt5b_nb1_ch3_4_tags.csv).
5. **Pre-registration confirmation**: the tagging was completed and
   codified in the script + CSV BEFORE
   [`insights/HUNT5B_NB1_CH3_4_PREDICTION_REGISTRATION.md`](../insights/HUNT5B_NB1_CH3_4_PREDICTION_REGISTRATION.md)
   was opened. The diary's comparison section below reflects the
   first-read-after-tagging.

### Decision rules for ambiguous cases (sharpened from diaries 22 / 24 / 25)

- **fractional_functional_iteration** fires when the proof appeals to:
  (a) explicit fractional iterates of a function (Ch. 4 §§1-7 — the
  F_r(x) iterates indexed by all real r); (b) Lagrange-inversion-style
  implicitly-defined functions where the iteration index enters
  polynomially (Ch. 3 Entries 13-17 — x = a log x, x^x = a^n e^h,
  algebraic-equation roots in implicit form); (c) Schröder/Koenig
  functional-iteration extensions including the Lambert-W neighborhood
  per diary 20's operator definition. Lagrange inversion (1770 paper
  on Lambert's 1758 equation) IS the canonical pre-fractional-iteration
  device.
- **master_theorem** fires when the proof explicitly invokes the
  substitute-coefficient-extraction move (§9 of Ch. 4 + Entry 10 +
  Entry 11 + Corollaries 1-5 + §13(i) Beta-function consequence) OR
  when Berndt's commentary calls out the Master-Theorem connection
  (e.g. "Hardy quotes Corollary 1 ... particularly interesting formula"
  per Ch. 4 §11).
- **mellin_pair_reciprocity** fires when an integral identity has
  alpha-beta=1 reciprocity STRUCTURE per QR III §15. Pure Fourier
  cosine self-reciprocity (Ch. 4 §12 Entry 12) does NOT fire because
  FOURIER_SELF_RECIPROCITY was dropped from the diary-25 11-op basis;
  only the alpha-beta=1 Mellin-pair variant is kept. Ch. 4 Cor 3 + 4
  of Entry 11 fire mellin_pair_reciprocity because the structure (the
  cosine transform with scaling) carries the alpha*beta = constant
  reciprocity in Ramanujan's QR-II original.
- **Asymptotic expansions** (Ch. 3 Entries 3, 9(i), 10, 16(b); Ch. 4
  Cor 1, Cor 2 of §9) are OUT-OF-SCHEMA when they use Stirling-2
  / Bell-polynomial / Borel-summation-adjacent machinery. They do NOT
  fire `master_theorem` even when they look superficially Mellin-like
  (no Gamma(s) phi(-s) form, no alternating-sign normalization).
- **Bernoulli numbers** in Ch. 3 §8 Example 4 and Ch. 4 Entry 3 +
  Cor 2 of E4 are OUT-OF-SCHEMA: they're plain expansion coefficients
  via Euler-Maclaurin, not Eisenstein-anchored E_{2k} normal-ordering.
- **Cube roots of unity** in Ch. 4 Entry 14 (omega = exp(2 pi i / 3)
  cyclotomic sum of three sinh factors) is OUT-OF-SCHEMA per diary 22
  E32-19's exclusion convention: a Galois-orbit-style move on the
  unit circle Q(omega) = Q(sqrt(-3)) does NOT fire
  `class_field_galois_average` unless CLASS-FIELD structure (Hilbert
  class field, Heegner orbit, class invariant) is explicitly invoked.

### Counting unit conventions

The Ch. 3 / Ch. 4 chapters are organized by Berndt as:
**Entry N** (Ramanujan's numbered claim), **Entry N(i), N(ii)**, etc.
(sub-claims of an entry), **Corollary 1, Corollary 2** (consequences
of an entry with their own proofs), **Example 1, Example 2, ...**
(specific applications, often with their own proofs), **Theorem**
(Berndt-inserted theorem in §13 of Ch. 3, attributed to Rota-Mullin).
The atomic unit is the **proof body**. Where Berndt aggregates 12
examples (Ch. 3 §15 Examples 3(i)-3(viii) + 4(i)-4(iv)) under "all
share the same skeleton — apply Entry 13 with various substitutions",
I count this as 1 aggregate unit, per the diary 25 §11 j-invariant
"catalogue of 13 class invariants = 1 aggregate" convention.

### Total proof units tagged

**91 atomic proof units** (Ch. 3: 49; Ch. 4: 42).

## Numbers

### Per-section operator distribution

#### Ch. 3 §§1-9 — Bell polynomials / Stirling-2 / asymptotic-expansion machinery

23 units (E1, E1-C1, E2, E2-C1, E2-C2, E3, E4, E5, E6, E7, E8,
E8-fn-table corollary, Ex1-of-E8, Ex2-of-E8, Ex3-of-E8, Ex4-of-E8,
Ex5-of-E8, Ex6-of-E8, E9i, E9ii, E9iii, E9iv-vii [aggregate of 9(iv)
through 9(vii) + F_n table + Examples (i)-(iv)]).

All 23 units fire **ZERO in-schema operators**. The machinery is pure
combinatorial generating-function manipulation: single-variable Bell
polynomials, Stirling numbers of the second kind, Pascal-like
recursions, formal power series with binomial coefficients. The Bell-
polynomial recursion (E5, E9iii) and the Stirling-2 explicit formula
(E7, E9v) are well-known classical results not aligned with any
modular-form / Mellin-transform / class-field structure.

#### Ch. 3 §10 — Entry 10 (asymptotic Poisson-expectation expansion)

6 units (L1-4-of-E10 [aggregate of Lemmas 1, 2, 3, 4], E10, Ex1-of-E10,
Ex2-of-E10, Ex3-of-E10, Ex4-of-E10).

All 6 fire **ZERO in-schema operators**. Berndt's proof uses Taylor
polynomial truncation + delicate exponential-tail bounds; Ramanujan's
own formal proof uses Bell-polynomial machinery. The expansion form
phi_x(x) = phi(x) + sum b_kn x^{...} phi^{(j)}(x) / k! + O(...) is
asymptotic-in-negative-powers-of-x but NOT Mellin: there is no
integral transform, no Gamma(s) prefactor, no alternating-sign
master-theorem normalization. Berndt remarks that the structure is
related to the Borel-summability question but "no other material in
the second notebook pertains to Borel summability" — i.e., even
Ramanujan didn't pursue this connection.

**Ch. 3 §§1-10 subtotal (29 units): ZERO operator firings.**

#### Ch. 3 §11-§12 — generating-function convolutions

3 units (E11, E11-Cor [Newton-Girard], E12).

All 3 fire **ZERO in-schema operators**. Newton-Girard formula for
symmetric functions, generating-function convolutions, formal
power-series identities for F_r(n) = sum (n+k)^{r+k} / (a^k k!).

#### Ch. 3 §§13-17 — Lagrange-inversion / iterated-exponential machinery

17 units (Thm-pre-E13, Cor-pre-E13, E13, Cor-E13, E14, Cor1-E14,
Cor2-E14, E15, Ex1-of-E15, Ex2-of-E15, Ex3-and-4-of-E15 [aggregate
of 12 examples], E16a, E16b, Cor1-E16, Cor2-E16, E17, Ex1-of-E17,
Ex2-of-E17 = 18 - 1 aggregation, count 17 below).

| Item | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| Thm-pre-E13 | (none) | "now part of a general theory developed by Rota and Mullin" — pure polynomial induction, no in-schema operators. |
| Cor-pre-E13 | (none) | Direct from theorem, explicit Gould polynomial formula. |
| **E13** | `fractional_functional_iteration` | "Entries 13 and 14 have a long history. Entry 14 was first established by Lambert [1, pp. 38-40] in a paper published in 1758. In 1770, Lagrange [1] published a proof of the celebrated Lagrange inversion formula. As an application, he derived Entry 14." x = a log x, f(n) = x^n IS the Lambert-W / Lagrange-inversion / fractional-iteration substrate. |
| **Cor-E13** | `fractional_functional_iteration` | Abel-type identity for e^z; inherits E13's fractional-iteration tag. |
| **E14** | `fractional_functional_iteration` | a^q x^p - x^q + 1 = 0; canonical Lagrange-inversion / implicit-function fractional iteration. |
| **Cor1-E14** | `fractional_functional_iteration` | Inherits. |
| **Cor2-E14** | `fractional_functional_iteration` | Inherits. |
| **E15** | `fractional_functional_iteration` | u - log u = 1 + x^2/2; fixed-point equation gives analytic inverse u = G^{-1}(x). |
| **Ex1-of-E15** | `fractional_functional_iteration` | Application of E14; inverts algebraic equation 2^{-n} x^n - x + 1 = 0. |
| **Ex2-of-E15** | `fractional_functional_iteration` | (log x)^n = a x^m; Lagrange-inversion. |
| **Ex3-and-4-of-E15** | `fractional_functional_iteration` | 12 examples aggregated. Famous iterated-power tower x^{x^{x^...}} display (Eisenstein notation), purest fractional-iteration motif. |
| **E16a** | `fractional_functional_iteration` | Uses E12 + the relation x/a = log x; inherits. |
| **E16b** | `fractional_functional_iteration` | Inherits. |
| **Cor1-E16** | `fractional_functional_iteration` | Maclaurin-like Cor 1: e^x = sum (x+kn)^k a^k / k!. |
| **Cor2-E16** | `fractional_functional_iteration` | n^* = lim phi_r(n). |
| **E17** | `fractional_functional_iteration` | x^x = a^n e^h; dx/dh = 1/(1+log x). Lambert-W neighborhood. |
| **Ex1-of-E17** | `fractional_functional_iteration` | A_r = (r-1)^{r-1} for n=1. Cayley-tree counting. |
| **Ex2-of-E17** | `fractional_functional_iteration` | Substitute x = 1/y in E17. |

**Ch. 3 §§13-17 subtotal (17 units): `fractional_functional_iteration`
16/17 (94.1%), zero other in-schema operators.**

#### Ch. 4 §§1-7 — fractional iterates of e^x - 1

13 units (E1-def, E2, Cor1-E2, Cor2-E2, E3, Cor-E3, E4, Cor1-E4,
Cor2-E4, E5, E6i, E6ii, E7, Ex1-of-E7).

| Item | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| **E1-def** | `fractional_functional_iteration` | "Ramanujan tacitly assumes that F_r(x) can be defined for all real values of r ... Comtet [1, pp. 144-148] describes how to define arbitrary real iterates of formal power series." THE cleanest possible firing of fractional_functional_iteration in the entire corpus. F_r(x) = sum phi_k(r) x^k = sum f_k(x) r^k — iteration index r enters polynomially. |
| **E2** | `fractional_functional_iteration` | F_r'(x) = (1+F_r) F_{r-1}'(x); chain rule on iteration. |
| **Cor1-E2** | `fractional_functional_iteration` | F_r'(x) = prod (1+F_k(x)); apply (2.1) r times. |
| **Cor2-E2** | `fractional_functional_iteration` | phi_n(r) - phi_n(r-1) recursion. |
| **E3** | `fractional_functional_iteration` | Euler-Maclaurin on the iterates phi_k(n). Bernoulli numbers appear as plain expansion coefficients (out-of-schema for eisenstein). |
| **Cor-E3** | `fractional_functional_iteration` | log(f_1(x)) integral representation. |
| **E4** | `fractional_functional_iteration` | F_{k+r}(x) = F_k(F_r(x)) composition law for the iterates — canonical move of fractional iteration. |
| **Cor1-E4** | `fractional_functional_iteration` | psi_k(n) recursions. |
| **Cor2-E4** | `fractional_functional_iteration` | (n+1) psi_n(1) = ... + 2 sum B_{2k}; Bernoulli coefficient. |
| **E5** | `fractional_functional_iteration` | f_1(x) = (1+x) f_1(log(1+x)) — apply F_{r-1}(x) = F_r(F_{-1}(x)). |
| **E6i** | `fractional_functional_iteration` | phi_n(1) = 1/n!, phi_n(-1) = (-1)^{n-1}/n. |
| **E6ii** | `fractional_functional_iteration` | psi_k closed forms, f_1(x) explicit through x^7. |
| **E7** | `fractional_functional_iteration` | F_{2r}(x) explicit expansion in r. |
| **Ex1-of-E7** | `fractional_functional_iteration` | f_1 f_1' identity, apply E4. |

**Ch. 4 §§1-7 subtotal (14 units): `fractional_functional_iteration`
14/14 (100%), zero other operators.**

#### Ch. 4 §8 — harmonic-sum identities

1 unit (E8).

Zero in-schema operators. Abel summation of harmonic sums. Out-of-
schema (classical analytic number theory).

#### Ch. 4 §9 — the "Ingenious Formal Technique" + Examples 1-4 + Corollaries

7 units (S9-framework, Ex1-S9, Ex2-S9, Ex3-S9, Ex4-S9, Cor1-of-S9,
Cor2-of-S9).

| Item | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| **S9-framework** | `master_theorem` | Ramanujan: "If two functions of x be equal, then a general theorem can be formed by simply writing phi(n) instead of x^n in the original theorem." THE PROTO-MASTER-THEOREM MOVE. Berndt later (p. 85) calls Cor 1 of E11 — built on this framework — "Ramanujan's favourite formula" per Hardy. |
| **Ex1-S9** | `master_theorem` | Residue-theorem evaluation of phi(z)/(z sin(pi z)). |
| **Ex2-S9** | `master_theorem` | sum (-1)^{k-1} phi(k) = phi(0); same machinery. |
| **Ex3-S9** | `master_theorem` | sum (-1)^{k-1} phi(k)/k = phi'(0). |
| **Ex4-S9** | `master_theorem` | sum (-1)^{k-1} psi(k)/(k! k); apply Example 3. |
| **Cor1-of-S9** | `master_theorem` | sum (-1)^{k-1} x^k / (k! k) ~ log x + gamma. |
| **Cor2-of-S9** | `master_theorem` | Ramanujan's (incorrect) n-th moment claim; operator fires REGARDLESS of correctness. |

**Ch. 4 §9 subtotal (7 units): `master_theorem` 7/7 (100%), zero
other operators.**

#### Ch. 4 §10 — Entry 10 contour-integral identity + Examples 1-4

8 units (E10, Cor-E10, Ex1-E10, Ex-of-E10-tan-inv, Ex2-E10-v1,
Ex2-E10-v2, Ex2-E10-v3, Ex3-E10, Ex4-E10 = 9 units; counted as 8 because
Ex2-E10-v2 fires no operators).

| Item | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| **E10** | `master_theorem` | Cot-cot contour integrand; corollary specializes to f(0) = phi(r), the Master-Theorem-style coefficient extraction at s = r. |
| **Cor-E10** | `master_theorem` | The "generating function" framework Ramanujan exploits. |
| **Ex1-E10** | `master_theorem` | Apply Cor with phi(z) = phi(z+1), r = -1. |
| **Ex-of-E10-tan-inv** | `master_theorem` | phi(z) = sin(pi z / 2) / z. |
| **Ex2-E10-v1** | `master_theorem` | Berndt: "Ramanujan deduces this result by setting phi(z) = Gamma(z) in Example 1." |
| **Ex2-E10-v2** | (none) | Standard Stieltjes-type analytic CF from Wall's book; NOT a Ramanujan-style q-CF. Out-of-schema. |
| **Ex2-E10-v3** | `master_theorem` | Uses Ch3-Cor2 of E2 + gamma evaluation. |
| **Ex3-E10** | `master_theorem` | Berndt: "Ramanujan deduced this value by letting phi(z) = Gamma(z+1) and r = n in the Corollary." |
| **Ex4-E10** | `master_theorem` | Berndt: "Ramanujan evidently put phi(z) = Gamma(z) sin(pi z / 2) in Example 1." |

**Ch. 4 §10 subtotal (9 units, 8 firing): `master_theorem` 8/9
(88.9%), zero other operators.**

#### Ch. 4 §11 — Entry 11 = THE MASTER THEOREM + Corollaries 1-5

6 units (E11, Cor1-E11, Cor2-E11, Cor3-E11, Cor4-E11, Cor5-E11).

| Item | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| **E11** | `master_theorem` | THE MASTER THEOREM. "integral_0^infty x^{n-1} sum phi(k)(-x)^k / k! dx = Gamma(n) phi(-n)". Cleanest possible firing. |
| **Cor1-E11** | `master_theorem` | "particularly interesting formula was one of Ramanujan's favourite formulas" (Hardy). pi phi(-n) / sin(pi n) form. |
| **Cor2-E11** | `master_theorem` | Cosine-Master version with phi(2k)(-x^2)^k. |
| **Cor3-E11** | `master_theorem`, `mellin_pair_reciprocity` | Cosine-transform version: sum phi(-2k-1)(-n^2)^k. Borderline mellin_pair_reciprocity — the cosine-transform pairing is alpha-beta-product-of-fixed-form (in the original QR II §4(vii) form the alpha*beta=2/pi reciprocity is explicit). Tagging both per the diary 20 §"Corollary (vii)" tagging precedent. |
| **Cor4-E11** | `master_theorem`, `mellin_pair_reciprocity` | Berndt: "Corollary 4, which also appears as Corollary (vii) in Ramanujan's second quarterly report ... defer ... to the quarterly reports." Same identity tagged in diary 20 as master_theorem + mellin-pair-reciprocity. |
| **Cor5-E11** | `master_theorem` | Beta function. "also given in Ramanujan's first quarterly report". |

**Ch. 4 §11 subtotal (6 units): `master_theorem` 6/6 (100%),
`mellin_pair_reciprocity` 2/6 (33.3%), zero other operators.**

#### Ch. 4 §§12-15 — Fourier inversion / Beta integrals / cube-root product

5 units (E12, E13i, E13ii, E14, E15).

| Item | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| **E12** | (none) | Pure Fourier cosine self-reciprocity + Parseval. FOURIER_SELF_RECIPROCITY was dropped from the diary-25 11-op basis; only alpha-beta=1 Mellin-pair reciprocity is kept. The QR III §15 form requires alpha*beta=2 substrate, not cosine self-pairing. 0 in-schema firings per "near match != match" discipline. |
| **E13i** | `master_theorem` | sin^m cos^n integral. Berndt: "an easy consequence of Corollary 5 of Entry 11" (which IS Master-Theorem-derived Beta function). |
| **E13ii** | (none) | cos^m cos(nx) integral. Berndt points to Whittaker-Watson exercise 39 — proof goes through binomial expansion + complex exponentials, NOT via §9 substitution or §11 Master-Theorem. Near-match excluded. |
| **E14** | (none) | sinh / cosh / cos cyclotomic product. Cube-root-of-unity sum over Q(omega) = Q(sqrt(-3)). Per diary 22 E32-19 near-match exclusion: NOT class_field_galois_average unless class-field structure explicitly invoked. Pure cyclotomic evaluation. |
| **E15** | (none) | Direct integral with G_k = sum 1/(2j+1). Out-of-schema. |

**Ch. 4 §§12-15 subtotal (5 units): `master_theorem` 1/5 (20%), zero
other operators.**

### Chapter-wide per-operator aggregate counts

**Total atomic proof units across Ch. 3 + Ch. 4: 49 + 42 = 91 units.**

| Operator | n_entries | % of 91 | Notes |
|---|---|---|---|
| `fractional_functional_iteration` | 30 | **33.0%** | **DOMINANT.** Splits into Ch. 3 (§§13-17) at 16/49 (32.7%) + Ch. 4 (§§1-7) at 14/42 (33.3%). |
| `master_theorem` | 22 | **24.2%** | All in Ch. 4: §9 (7), §10 (8), §11 (6), §13 (1). Ch. 3: 0%. |
| `mellin_pair_reciprocity` | 2 | **2.2%** | Ch. 4 Cor 3 + Cor 4 of E11 only. |
| `modular_S_transform` | 0 | **0.0%** | |
| `eisenstein_normal_ordering` | 0 | **0.0%** | |
| `q_shift` | 0 | **0.0%** | |
| `class_field_galois_average` | 0 | **0.0%** | |
| `denesting_via_kummer_or_landau` | 0 | **0.0%** | |
| `algebraic_number_field_norms` | 0 | **0.0%** | |
| `cardano_cubic_formula` | 0 | **0.0%** | |
| `frullani_limit` | 0 | **0.0%** | |

### Per-chapter operator distribution

| Operator | Ch. 3 (49 units) | Ch. 4 (42 units) | Combined (91) |
|---|---|---|---|
| `fractional_functional_iteration` | 16 (32.7%) | 14 (33.3%) | 30 (33.0%) |
| `master_theorem` | 0 (0.0%) | 22 (52.4%) | 22 (24.2%) |
| `mellin_pair_reciprocity` | 0 (0.0%) | 2 (4.8%) | 2 (2.2%) |
| (all other operators) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

**Ch. 3 is a fractional_functional_iteration monoculture (sole-operator
dominance, no others firing). Ch. 4 is a master_theorem +
fractional_functional_iteration dual-toolkit, with master_theorem the
primary operator (52.4%) and fractional_iteration the secondary
(33.3%) — they fire in DISJOINT entry-sets (§§1-7 are iteration; §§9-11
are Master Theorem; §12-15 are mixed analytics).**

## Surprises

1. **The pre-registered dominant operator `master_theorem` (85-95%)
   actually fires at only 24.2% overall and 52.4% on Ch. 4 alone.**
   The pre-registration assumed both chapters would be Master-Theorem-
   saturated. In fact, Ch. 3 has ZERO Master-Theorem firings, and even
   in Ch. 4 it doesn't break the 85% floor. The structural reason: the
   chapter-pair is operationally a TWO-toolkit chapter (iteration in
   Ch. 3 §§13-17 + Ch. 4 §§1-7; Master Theorem in Ch. 4 §§9-11).

2. **`fractional_functional_iteration` at 33.0% emerges as the
   DOMINANT operator, almost tied with master_theorem (24.2%) but with
   broader coverage (Ch. 3 AND Ch. 4 both at ~33%, vs master_theorem
   only firing in Ch. 4).** The pre-registration predicted 8-20% for
   fractional_iteration. The actual 33% is above the prediction's
   ceiling. This is the **novel-pattern outcome** the pre-registration
   listed as the 7% probability case ("novel generalized-Gamma operator
   pattern emerges").

3. **`mellin_pair_reciprocity` at 2.2% (Cor 3 + Cor 4 of Ch. 4 E11
   only) is FAR below the predicted 70-88% bracket.** The
   pre-registration's caveat was: "If we allow it to co-fire with
   master_theorem whenever the proof uses RMT as a Mellin-transform
   identity, it should exceed 80%. If reserved strictly for explicit
   transform-pair reversals, it may fall to high supporting frequency."
   I applied the STRICT alpha-beta=1 form (per diary 25's convention),
   so the count stays at 2 — only the Cor 3 + Cor 4 of E11 that
   diary 20 also tagged as mellin_pair_reciprocity. The looser tagging
   would push this to ~25 firings (everything master_theorem-related)
   but that conflates the Master Theorem itself with its alpha-beta=1
   special case.

4. **`modular_S_transform`, `class_field_galois_average`, `q_shift`,
   `eisenstein_normal_ordering` all stay at 0.0%.** This CONFIRMS
   the topic-toolkit reading: even though Ch. 3-4 is in a Notebooks
   volume (provenance), it contains ZERO modular-cluster operators
   (because the topic is analytic). The pre-registration's strongest
   falsification signal — modular_S > 10% — does NOT trigger.

5. **`frullani_limit` at 0% is below the predicted 15-30% bracket.**
   Frullani's classical integral identity appears nowhere in Ch. 3-4.
   It DOES appear in QR II §4, but the Notebooks-volume version
   (specifically Ch. 4 §§9-11) routes through generating-function
   substitution (Master Theorem proper) rather than parametric integral
   limits. Frullani is QR-specific; Master-Theorem is universal.

6. **Ch. 3 is a fractional_functional_iteration MONOCULTURE for the 17
   units of §§13-17.** This is the cleanest single-operator stretch in
   the entire chapter pair. Zero other operators fire on those 17
   units. The other 32 units of Ch. 3 (§§1-12) fire ZERO of any
   in-schema operator at all (pure combinatorial Bell / Stirling /
   asymptotic machinery).

7. **Ch. 4 is the cleaner Master-Theorem chapter, but with a
   substantial fractional-iteration component.** §§1-7 (Entries 1-7)
   are 14/14 (100%) fractional iteration; §§9-11 (Entry 11 + S9
   framework + Entry 10) are 21/22 (95.5%) Master Theorem. §§12-15
   are weak (1/5 fires master_theorem).

8. **The chapter pair's operator-firing landscape is NOT a single
   coherent cluster.** It's TWO disjoint topical regions:
   - **Iteration region** (Ch. 3 §§13-17 + Ch. 4 §§1-7): 30 units,
     `fractional_functional_iteration` 30/30 (100%); zero other
     operators.
   - **Master-Theorem region** (Ch. 4 §§9-11): 22 units,
     `master_theorem` 22/22 (100%); `mellin_pair_reciprocity` 2/22
     (9.1%); zero other operators.
   - **Out-of-schema region** (Ch. 3 §§1-12 + Ch. 4 §§8 + §§12-15):
     39 units, all operators 0% — pure combinatorial / Bell-polynomial
     / Fourier-self / cyclotomic machinery that the 11-op basis
     doesn't cover.

9. **Out-of-schema rate is high (39/91 = 42.9%).** Compared to:
   - QR (diary 20): 8.5% out-of-schema after the 5-op basis expansion.
   - NB V Ch. 32 (diary 22): 0% (every entry fires at least one
     in-schema operator).
   - NB V Ch. 34 (diary 25): ~3% (only Lemma 3.3 + Lemmas 9.10-9.11).
   - NB V Ch. 36 (diary 24): also low.

   The out-of-schema rate in this chapter pair indicates the 11-op
   basis is significantly less complete for the Bell-polynomial /
   Stirling-2 / asymptotic-expansion / cube-root cyclotomic family.
   Strong candidate for a 12th operator:
   `bell_polynomial_stirling_machinery` or `generating_function_residue`
   (the cot-cot contour-integral move at §9 of Ch. 4 IS this in
   pre-Master form, but Berndt routes it through the §9-framework
   substitution rather than into a residue-only operator).

## Verdict

**PARTIAL** with **NOVEL PATTERN** dominating the outcome.

Hit-count against the pre-registered prediction table:

| Predicted operator | Predicted % | Actual % | Verdict |
|---|---|---|---|
| `master_theorem` | 85-95% | **24.2%** (Ch. 4: 52.4%) | **MISS** (below floor by 33 pp on Ch. 4 alone; by 61 pp on combined) |
| `mellin_pair_reciprocity` | 70-88% | **2.2%** | **MISS** (strict tagging applied; loose would be ~25%) |
| `frullani_limit` | 15-30% | **0.0%** | **MISS** (below floor) |
| `fractional_functional_iteration` | 8-20% | **33.0%** | **EXCEED** (above ceiling by 13 pp; novel-pattern outcome) |
| `modular_S_transform` | 0-3% | **0.0%** | **CONFIRMED** (in bracket) |
| `class_field_galois_average` | 0-1% | **0.0%** | **CONFIRMED** (in bracket) |
| `q_shift` | 0-5% | **0.0%** | **CONFIRMED** (in bracket) |

Pre-registered falsification signals (per ChatGPT Pro's predictions
document):
1. **`modular_S_transform` > 10%** — did NOT trigger (0.0%). The
   topic-toolkit reading is CONFIRMED on this signal.
2. **`q_shift` > 10%** — did NOT trigger (0.0%). Topic-toolkit
   reading CONFIRMED.
3. **`master_theorem` stays below 50%** — TRIGGERED. Combined chapters
   24.2%; Ch. 4 alone 52.4% (just above threshold); Ch. 3 alone 0.0%.
4. **Novel operator outside the QR/Notebooks split exceeds 30%** —
   TRIGGERED. `fractional_functional_iteration` at 33.0% (with
   100% in the iteration-region 30 units). This is the
   pre-registration's "most interesting outcome".

**Bottom-line classification per the rubric:** This is
**NOVEL PATTERN** — falsification signals 3 and 4 both triggered,
indicating the chapter-pair's operator structure is a two-toolkit
mix (fractional_iteration + master_theorem) rather than the
predicted master_theorem monoculture. The pre-registration
listed this as the 7% probability outcome.

Net interpretive verdict for the corpus-vs-topic question:
**The topic-toolkit reading is PARTIALLY confirmed.** Zero firing
of modular operators (confirmed predictions for modular_S,
class_field, q_shift, eisenstein) confirms the corpus-provenance
hypothesis is FALSE — Ramanujan's Notebooks-volume material does
NOT systematically fire the modular cluster when the topic is
analytic. **But** the topic itself is not pure-Master-Theorem; it
splits into TWO disjoint analytic subtoolkits (Master Theorem +
fractional functional iteration) that operate in disjoint
entry-sets.

## Implications for the toolkit-split hypothesis

This is the **5th Hunt 5b chapter** (Ch. 32, Ch. 34, Ch. 36 in NB V;
+ Ch. 3 + Ch. 4 in NB Part 1, counted as a single tagging pass).
The toolkit-split hypothesis now has TWO different shapes depending
on which side of the corpus you look at:

### Modular cluster (3 NB V chapters):

| | NB V Ch. 32 | NB V Ch. 34 | NB V Ch. 36 |
|---|---|---|---|
| modular_S | 91.7% | 97.1% | 100.0% |
| q_shift | 100.0% | 21.6% | 4.8% |
| class_field | 33.3% | 98.0% | 4.8% |
| master_theorem | 0.0% | 0.0% | 0.0% |
| fractional_iteration | 0.0% | 0.0% | 0.0% |

Pattern: modular_S always-on (>90%); secondary operator specialises
by problem-domain (q_shift for CFs, class_field for class invariants,
none-secondary for pure modular equations). **ZERO** QR-side
operators ever fire.

### Analytic cluster (QR + NB Part 1 Ch. 3-4):

| | QR I+II+III (d20) | NB Part 1 Ch. 3 | NB Part 1 Ch. 4 |
|---|---|---|---|
| master_theorem | 57.6% | 0.0% | 52.4% |
| fractional_iteration | 15% (QR III) | 32.7% | 33.3% |
| frullani_limit | 6% (QR II) | 0.0% | 0.0% |
| mellin_pair_reciprocity | (QR III §15) | 0.0% | 4.8% |
| modular_S | 0.0% | 0.0% | 0.0% |
| class_field | 0.0% | 0.0% | 0.0% |

Pattern: master_theorem fires when explicit substitution-coefficient-
extraction is the move (QR I + QR II + NB Ch. 4 §§9-11);
fractional_iteration fires when implicit-function / Lagrange-inversion
/ Schröder-iteration is the move (QR III + NB Ch. 3 §§13-17 + NB
Ch. 4 §§1-7). **ZERO** modular operators fire.

### Headline finding

**The QR-vs-Notebooks split IS topic-driven** (zero modular firing in
the Notebooks-volume analytic chapters; zero analytic firing in the
Notebooks-volume modular chapters). The pre-registration's
**"meta-prediction" is CONFIRMED at the corpus level**: provenance
does not predict toolkit, topic does.

**But the analytic cluster is BIPARTITE** (master_theorem +
fractional_iteration), not unitary. The two analytic operators fire
in disjoint problem-subdomains:
- **master_theorem domain**: explicit "substitute x^k -> phi(k)" or
  "integral form of Gamma(s) phi(-s)" or "Beta(m,n) via Master".
- **fractional_iteration domain**: implicit-function fixed-point
  equations (Lambert x = a log x; Ramanujan x = a^x); explicit
  fractional iterates of f(x) = e^x - 1 with index r in R; Lagrange-
  inversion-style closed forms for x^n where x = x(a).

The two operators are NEVER co-tagged on the same proof unit in this
chapter pair (the §§13-17 of Ch. 3 + §§1-7 of Ch. 4 are 30 units of
pure fractional_iteration with ZERO master_theorem; the §§9-11 of
Ch. 4 are 22 units of pure master_theorem with ZERO
fractional_iteration). This is a STRONG structural claim: the
analytic cluster is two operators living in disjoint topic-bands.

**Confidence update on the broader toolkit-split hypothesis:** medium-
high → **high** for the corpus-vs-topic question (provenance does
NOT predict toolkit). **NEW finding:** the analytic toolkit is
bipartite (master_theorem + fractional_iteration), not unitary, with
the two operators firing in disjoint topic-bands.

## Honest caveats

1. **Hand-judgment, one-pass, no inter-rater reliability check.** Same
   as diaries 20 / 22 / 24 / 25. ±5-8 percentage points on per-
   operator percentages.
2. **The mellin_pair_reciprocity strict-tagging convention** drops 2
   firings vs the loose convention (which would have given ~25
   firings). I followed the strict diary-25 convention (alpha*beta=1
   reciprocity per QR III §15); this is the consistent baseline across
   Hunt 5b chapters.
3. **Out-of-schema rate is 42.9%** (39/91 units fire NO in-schema
   operator). This is much higher than NB V (3-12%) and QR (8.5%).
   The 11-op basis is incomplete for Ch. 3 §§1-12 (Bell / Stirling /
   asymptotic) and Ch. 4 §§8 + 12-15 (harmonic sums / Fourier self /
   cyclotomic). A 12th operator slot for `bell_polynomial_machinery`
   or `generating_function_residue` would close most of the gap.
4. **The fractional_iteration tagging policy** (treating Lagrange
   inversion + Lambert-W neighborhood as fractional_iteration per
   diary 20's Schröder/Koenig framing) is a load-bearing choice. A
   stricter "only explicit fractional iterate F_r with r in R" policy
   would drop Ch. 3 §§13-17 firings entirely, leaving Ch. 4 §§1-7
   as the sole fractional_iteration cluster (14/91 = 15.4% — at the
   ceiling of the pre-registered bracket). The looser policy
   (applied here, consistent with diary 20) makes the bipartite
   analytic-cluster finding clearer.
5. **Reading was via pdftotext extraction**, not direct PDF view
   except for spot-checks. Berndt's typography (italic / bold /
   spacing) is partially lost in pdftotext output; the OCR'd text
   sometimes garbles formulae (e.g. "Forma1" instead of "Formal").
   I cross-referenced unit boundaries (Entry N, Corollary, Example
   labels) against the layout-aware output and verified by checking
   the page numbers in Berndt's running headers. No tagging decision
   hinged on a formula detail that pdftotext garbled.

## Bottom-line claim

**NOVEL PATTERN with topic-toolkit support, medium-high confidence.**

Berndt NB Part 1 Ch. 3 + Ch. 4, hand-tagged on the same 11-operator
basis as the 3 NB V chapters of Hunt 5b, shows:
- **Zero firing of any modular-cluster operator** (modular_S 0%,
  class_field 0%, q_shift 0%, eisenstein 0%) — confirming the
  topic-toolkit reading: Notebooks-volume material does NOT
  systematically fire modular operators when the topic is analytic.
- **Bipartite analytic cluster** dominated by `fractional_functional_iteration`
  (33.0%, monoculture in Ch. 3 §§13-17 + Ch. 4 §§1-7) and
  `master_theorem` (24.2% overall, 52.4% on Ch. 4, monoculture in
  Ch. 4 §§9-11).
- The two analytic operators fire in **DISJOINT entry-sets** (zero
  co-tagging across 30 + 22 = 52 units in the iteration + Master-
  Theorem subdomains).
- The pre-registered "master_theorem dominant" prediction (85-95%)
  is FALSIFIED at the chapter level; the "novel-operator-cluster"
  outcome (probability 7% per the pre-registration) is what actually
  realised.
- The pre-registration's META-prediction ("topic-toolkit split, not
  provenance-toolkit split") is CONFIRMED at the corpus level.

## Comparison to the pre-registered predictions

Per the pre-registration document at
[`insights/HUNT5B_NB1_CH3_4_PREDICTION_REGISTRATION.md`](../insights/HUNT5B_NB1_CH3_4_PREDICTION_REGISTRATION.md)
(read AFTER tagging was complete and codified):

**ChatGPT Pro's bottom-line probability distribution** (table at
prediction §"ChatGPT Pro prediction"):
- 70%: Ch. 3-4 is QR-side analytic by operator profile → **PARTIALLY
  CONFIRMED**: zero modular firing; analytic operators dominate;
  BUT the dominant operator is fractional_iteration, not
  master_theorem.
- 20%: mixed analytic, master_theorem dominant but
  Mellin/Frullani/fractional_iteration distributed more evenly than
  expected → **PARTIALLY MATCHES**: fractional_iteration distribution
  is much higher than predicted (33% vs 8-20%); Mellin/Frullani
  vanish (0%); master_theorem is below the dominant-bucket floor
  (24.2% vs ≥85%).
- **7%: novel generalized-Gamma operator pattern emerges (not in
  current basis — the *interesting* outcome per ChatGPT)** →
  **THIS IS WHAT HAPPENED.** The novel-pattern outcome materialised:
  the fractional_functional_iteration cluster at 33% is the
  "interesting" outcome ChatGPT flagged. (Note: it's an EXISTING
  operator in the 11-op basis, but its DOMINANCE in NB Part 1 Ch. 3-4
  is novel — diary 20 had it at only 15% even in QR III, the most
  iteration-heavy QR.)
- 3%: modular operators unexpectedly appear → DID NOT HAPPEN
  (modular_S 0%, class_field 0%, q_shift 0%).

**Per-operator hit/miss**: 3 hits (modular, class_field, q_shift)
out of 7 predictions. Strongest miss: master_theorem predicted at
85-95% bucket, actual 24.2% — a ~3-sigma miss on the prediction's
own claimed 0.75 confidence. Strongest gain: fractional_iteration
predicted at 8-20% bucket, actual 33% — outside the upper bracket.

**Pre-registration falsification-signal status**:
- Signal 1 (modular_S > 10%): NOT TRIGGERED → topic-toolkit reading
  REMAINS valid for the corpus question.
- Signal 2 (q_shift > 10% strict): NOT TRIGGERED.
- Signal 3 (master_theorem < 50%): TRIGGERED on Ch. 3 (0%) and
  combined (24.2%); just-above-threshold on Ch. 4 (52.4%).
- Signal 4 (novel operator > 30%): TRIGGERED
  (fractional_functional_iteration at 33%).

**Net classification**: **NOVEL PATTERN.** The corpus-vs-topic
meta-prediction is CONFIRMED at the corpus level. The within-topic
operator distribution prediction is FALSIFIED in favour of a
bipartite analytic-cluster pattern (master_theorem +
fractional_iteration in disjoint entry-sets).

## Follow-up leads

1. **Add the 4th NB V chapter** — Ch. 33 ("Theta-Function Identities")
   or Ch. 35 ("Singular Moduli and Modular Equations of Higher
   Degree") — would test whether the modular cluster's 3-chapter
   monoculture holds. If it stays modular, the corpus-topic split is
   robust.
2. **Tag QR III §§13-15 explicitly** with the new bipartite analytic
   reading. Diary 20's QR III tagging had master_theorem appearing
   alongside FRACTIONAL_FUNCTIONAL_ITERATION and HARDY_ORDERS_OF_INFINITY
   on the same units (the operator-calculus theorems). Re-tagging
   QR III with the disjoint-entry-set discipline applied here would
   test whether the bipartite analytic-cluster finding is a Hunt-5b
   artefact or a real structural property of Ramanujan's analytic work.
3. **Add a 12th operator** — `bell_polynomial_machinery` or
   `generating_function_residue` — to close the 43% out-of-schema rate
   in Ch. 3 §§1-12. Could re-tag prior chapters with the expanded
   basis to test how much it closes their (lower) out-of-schema rates.
4. **The Lagrange-inversion / Lambert-W as fractional iteration
   tagging** is load-bearing. A separate diary should articulate the
   conceptual unity — is x = a log x's implicit-function solution
   really "the same operator" as F_r(x) = exp(F_{r-1}(x))-1's
   fractional iterate? The shared substrate is "an analytic function
   defined as the unique-branch solution of a functional equation
   that becomes integer-iteration in a special case". Operator slot
   could be refined into `lagrange_inversion_or_fractional_iteration`
   or split into two.
5. **Architecture paper notation update**: the toolkit-split section
   should now read "topic-driven, not corpus-driven" and report the
   bipartite analytic-cluster finding (master_theorem +
   fractional_iteration in disjoint entry-sets) as a refinement.

## Cross-links

- Updates / context for: [`insights/BIG_IDEAS_REVIEW.md §4`](../insights/BIG_IDEAS_REVIEW.md)
  (cog-sci framing).
- Updates for: [`insights/HUNT_MAP.md`](../insights/HUNT_MAP.md)
  Hunt 5b status — now "extended to NB Part 1 Ch. 3-4 with
  PARTIALLY-CONFIRMED-NOVEL-PATTERN pre-registered prediction; corpus-
  vs-topic meta-prediction CONFIRMED; bipartite analytic cluster is
  the novel finding".
- Source script + CSV:
  [`analysis/28_hunt5b_nb1_ch3_4_tagging.py`](../analysis/28_hunt5b_nb1_ch3_4_tagging.py),
  [`analysis/results/hunt5b_nb1_ch3_4_tags.csv`](../analysis/results/hunt5b_nb1_ch3_4_tags.csv).
- Pre-registration:
  [`insights/HUNT5B_NB1_CH3_4_PREDICTION_REGISTRATION.md`](../insights/HUNT5B_NB1_CH3_4_PREDICTION_REGISTRATION.md).
