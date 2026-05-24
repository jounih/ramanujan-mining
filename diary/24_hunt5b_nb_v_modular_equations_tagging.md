# Diary 24 — Hunt 5b: NB V Ch. 36 (Modular Equations and Theta-Function Identities) operator tagging

**Date:** 2026-05-24
**Source:** Berndt, *Ramanujan's Notebooks, Part V*, Ch. 36 ("Modular
Equations and Theta-Function Identities in Notebook 1"), pp. 353-407. Local
copy at [`downloaded-pdfs/ramanujan-notebooks-v.pdf`](../downloaded-pdfs/ramanujan-notebooks-v.pdf)
(PDF pages 185-211, 2-up book scan). Scope: all 83 numbered entries (E1-E83)
across §1-§10. Hunt 5b 2nd chapter pass (after Ch. 32 in diary 22).
**Status:** Ch. 36 result recorded; combined with Ch. 32 the toolkit-split
hypothesis is **strongly supported with intra-Notebooks specialisation**.

## Setup

Per [HUNT5b_PREDICTIONS §"NB II Ch. 17 (modular equations)"](../insights/HUNT5b_PREDICTIONS.md),
the predicted operator-distribution for the modular-equations chapter is:

| Operator | Predicted | |
|---|---|---|
| `modular_S_transform` | ≥50% | "Modular equations relate τ → -1/τ behaviour" |
| `class_field_galois_average` | ≥30% | "Galois-conjugacy of modular polynomial roots" |
| `q_shift` | moderate (~25%) | q-Pochhammer manipulations |
| `eisenstein_normal_ordering` | low (~10%) | Some Eisenstein-as-bilinear-form moves |
| `master_theorem` | ≤5% | Almost zero |
| All QR III operators | ~0% | Different universe |

**Important pre-registration note.** The Hunt 5b prediction was keyed to
NB II Ch. 17 (Ramanujan's second-notebook chapter on modular equations).
Berndt's NB Part V Ch. 36 covers "Modular Equations and Theta-Function
Identities in Notebook 1" — the **first notebook**, organised by Berndt
rather than by Ramanujan. The TOC table (p. 4) states Ch. 36 has 87
results spanning pp. 353-407. The chapter is partitioned by Berndt into
§1 (degree-3 mod eqns), §2 (degree-5), §3 (other), §4 (Lambert series
identities), §5 (Eisenstein series identities), §6 (Schläfli-form),
§7 (Russell-form), §8 (Weber-form), §9 (series transformations associated
with theta-functions), §10 (miscellaneous results — elliptic integrals
and approximate identities). I treat this chapter as the closest available
proxy for the Hunt 5b "modular equations" prediction — the substance is
the same (Ramanujan's body of modular-equation work), even though the
volume's chapter number is 36 not 17. The predictions stand as
pre-registered.

The QR baseline (diary 20) for the four predicted-dominant operators is
**0%, 0%, 0%, 0%**. The Ch. 32 result (diary 22) for those same operators
was **91.7%, 33.3%, 100.0%, 8.3%**.

## What I did

1. Read Berndt's NB V Ch. 36 §1-§10 end to end (pp. 353-407 of the book,
   PDF pages 185-211), reading both the Ramanujan entry statements and
   Berndt's per-entry commentary (proofs, attributions, references to
   prior work in Schläfli/Weber/Russell, modular-form citations).
2. Hand-tagged each of the 83 numbered entries (E1 through E83) against
   the 11-operator vocabulary (6 original from
   [`operator_tagging_schema.py`](../corpora/transcriptions/operator_tagging_schema.py)
   + 5 added per [diary 20 §"Out-of-schema operators"](20_hunt5_qr_operator_tagging.md)).
3. Same discipline as Hunt 5 / diary 20 / diary 22: hand-judgment, not
   regex; tags record whether the operator is the *primary or secondary
   move* in the entry's proof/statement; "near match ≠ match"; an entry
   where Berndt's commentary explicitly names an operator (e.g. "by the
   Jacobi triple product identity", "we resort to the theory of modular
   forms") gets that operator tagged with a direct-quote note.

**Decision rule for ambiguous cases (same as diary 22, sharpened).**
- An entry of the form "If β has degree N over α, then [polynomial
  identity in (α, β, m)]" with no proof beyond citing parametrisations
  from Part III is the *canonical* modular_S_transform firing: a modular
  equation of level N IS a τ → -1/τ-equivariant identity for the modular
  curve X_0(N). Tag `modular_S_transform`.
- An entry whose proof routes through `Schläfli`, `Russell`, or `Weber`
  paper-form theta-function-identity manipulation IS a modular-S move
  (those are level-N modular equations in different parametrisations).
- An entry whose proof explicitly invokes "the theory of modular forms"
  (Entries 43-52, 71-75) IS a modular-S move (we're computing orders at
  cusps for Γ(2)∩Γ₀(n) — classical modular-form machinery).
- An entry whose proof reduces to the Jacobi triple product identity IS
  a modular_S move (per diary 22 rule).
- Lambert series Σ q^k / (1 - q^k) and Σ q^k / (1 + q^k) are
  `eisenstein_normal_ordering` firings (canonical Lambert-series Eisenstein
  manifestation, per the schema's `_test_eisenstein_normal_order` regex
  literally pattern-matching `\\sum.*\\bn\\b.*q\\s*\\^\\s*\\{?n\\}?\\s*/\\s*\\(\\s*1\\s*-\\s*q\\s*\\^\\s*\\{?n\\}?\\s*\\)`).
- Explicit Eisenstein series L(q), M(q), N(q) being normal-ordered into
  divisor-sum generating functions (§5) IS the canonical
  `eisenstein_normal_ordering` firing.
- q-Pochhammer notation `(a; q)_∞` appearing in the body (not just inside
  a closed-form expression) is direct evidence of `q_shift`. Theta
  functions f, φ, ψ alone without q-Pochhammer expansion are NOT.
- Explicit invocation of the Legendre symbol `(n/3)` for index-by-residue
  dispatch IS evidence of `class_field_galois_average` (a discrete Galois
  character on `Q(√-3)`).
- Singular moduli / class invariants G_n, g_n appearing in the proof IS
  `class_field_galois_average`.

**11-operator vocabulary** (from operator_tagging_schema.py + diary 20):
Original 6: `mellin_inversion`, `master_theorem`, `q_shift`,
`modular_S_transform`, `eisenstein_normal_ordering`,
`class_field_galois_average`. Added 5: `FOURIER_SELF_RECIPROCITY`,
`FRACTIONAL_FUNCTIONAL_ITERATION`, `HARDY_ORDERS_OF_INFINITY`,
`FRULLANI_LIMIT`, `MELLIN_PAIR_RECIPROCITY`.

Out-of-schema operators encountered during tagging (recorded for
information; not in either basis): `modular_form_residue_at_cusps`
(used by Berndt as the principal proof technique for Entries 43-52 and
68-75 — explicit valence-formula machinery, order-at-cusps computation
via Γ(2)∩Γ₀(n), Mathematica q-expansion verification of finitely-many
coefficients), `parametric_representation` (uniformising α, 1-α as
p^3(2+p)/(1+2p), (1-p)^3(1+2p)/... etc. — Entries 7, 9, 10, 26),
`tangent_half_angle_formula` (Entries 1, 79, 80 — elliptic-integral
manipulation by addition formulas).

## Numbers

### Per-entry operator tags (83 entries in scope)

Tags are unordered sets; an entry can fire multiple operators. Notes
quote Berndt verbatim where he names the operator.

#### §1 — Modular Equations of Degree 3 (Entries 1-13)

| Entry | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| E1 (p. 354) | `modular_S_transform` | "If β has degree 3 over α, then [elliptic integral identity]"; explicitly a modular equation of degree 3 (proof uses Entry 6(v) of Ch. 19 in NB II, tangent half-angle formulas). |
| E2 (p. 356) | `modular_S_transform` | "In (36.8) of Chapter 16 of our book ..., set μ = 2 and ν = 1 to deduce that ψ(q)ψ(q³) = ..." — pure theta-function manipulation reducing to a Jacobi-style identity. |
| E3 (p. 356) | `modular_S_transform`, `q_shift` | Proof routes through corollary to Entry 31 of Ch. 16 (q-Pochhammer reduction): `(q^9; q^9)_∞ (q^18; q^18)_∞ / (q^3; q^6)_∞` etc — explicit q-Pochhammer notation in body. |
| E4 (p. 357) | `modular_S_transform` | "We now translate (4.3) into a modular equation of degree 3 by means of Entries 10(ii) and 11(i) of Chapter 17"; closes with the explicit degree-3 modular equation 9/m·((1-β)³/(1-α))^(1/4) − m·((1-α)³/(1-β))^(1/4) = 4m·(α³/β)^(1/8). |
| E5 (p. 357-358) | `modular_S_transform` | Proof uses Entry 24(ii) of Chapter 16 (theta-function identity). Berndt: "very puzzling indeed" — Ramanujan's claim has a discrepancy in sign in one term; Berndt does not classify as error. |
| E6 (p. 358) | `modular_S_transform` | "If β has degree 3 over α, then [polynomial in α, β, m]" — canonical degree-3 modular equation; proof reduces to Entry 5(iv) of Ch. 19 (Part III). |
| E7 (p. 358-359) | `modular_S_transform` | Elliptic-integral identity reducible to degree-3 modular equation via parametrisation `α = (α³/β)^(1/8)`, `n = ((1-α)³/(1-β))^(1/8)`; explicit "(7.5) is a modular equation of degree 3". |
| E8 (p. 359-361) | `modular_S_transform` | Proof routes through "the theory of modular equations of degree 3"; eq (8.9) uses Ch. 34 denesting Lemma 4.5. Tagged also for indirect class-invariant connection via "n² is related to class invariants" (last paragraph of proof). |
| E9 (p. 361) | `modular_S_transform` | "Ramanujan does not indicate that β has degree 3, i.e., that (9.1) is a modular equation of degree 3"; canonical degree-3 polynomial identity. |
| E10 (p. 361-362) | `modular_S_transform` | "The modular equations in Entry 10 do not seem to be easily deducible from Ramanujan's modular equations of degree 3 listed in Entry 5 of Chapter 19. However, they can be easily verified by using the parametrizations." |
| E11 (p. 362) | `modular_S_transform` | "Let β have degree 3 over α" — canonical; proof by H. H. Chan uses theta-function expressions for `x = (4α(1-α))^(1/3)` and `y = (4β(1-β))^(1/8)` and class invariant G_n notation; near-match with `class_field_galois_average` excluded because the G_n appears only as a substitution variable for theta-quotient denesting, not as a Heegner-orbit average over CM points. |
| E12 (p. 362-363) | `modular_S_transform` | Canonical degree-3-related identity: `(αβ⁵)^(1/8) + {(1-α)(1-β)⁵}^(1/8) = √(1 - {αβ(1-α)(1-β)}^(1/4))`; reduces directly to Entry 5(viii) of Ch. 19. |
| E13 (p. 363) | `modular_S_transform` | "If β has degree 3" + polynomial identity; equivalent to a known degree-3 Entry 5(viii) form. |

§1 subtotal (13 entries): `modular_S_transform` 13/13 (100%);
`q_shift` 1/13 (E3); `class_field_galois_average` 0/13; `eisenstein_normal_ordering` 0/13.

#### §2 — Modular Equations of Degree 5 (Entries 14-21)

| Entry | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| E14 (p. 363-364) | `modular_S_transform` | "Let β have degree 5 over α, and let m denote the multiplier of degree 5"; reduces to Entry 13(vi) of Ch. 19. |
| E15 (p. 364) | `modular_S_transform` | Proof: "(15.1) can be translated into the modular equation of degree 5, ... which is Entry 13(iii) of Chapter 19". |
| E16 (p. 364) | `modular_S_transform` | Same skeleton as E15; ψ⁵-shaped degree-5 identity reduces to Entry 13(ii) of Ch. 19. |
| E17 (p. 364-365) | `modular_S_transform`, `q_shift` | Proof routes through Entry 9(ii) of Ch. 19 + Entries 27(i), 24(iv) of Ch. 16; final manipulation: "if α, β > 0 and αβ = π², then by Entry 27(iv) of Chapter 16, e^(-α/24)α^(1/4)f(e^(-α)) = e^(-β/24)β^(1/4)f(e^(-β))" — THIS IS the explicit modular-S signature (q ↔ -log q' Poisson-summation move). |
| E18 (p. 365-366) | `modular_S_transform` | Proof uses Jacobi triple product identity + Euler's identity. |
| E19 (p. 366) | `modular_S_transform` | Canonical degree-5 polynomial identity in (α, β, m); reduces to Entry 13(iv) of Ch. 19 with auxiliary ρ = (m³ - 2m² + 5m)^(1/2). |
| E20 (p. 366-367) | `modular_S_transform` | "If β has degree 5 over α" + identity reducing to Entry 13(vii) of Ch. 19. |
| E21 (p. 367) | `modular_S_transform` | Two Jacobi-triple-product–like identities for products `f(-q, -q¹⁴)f(-q⁴, -q¹¹)...`. Berndt: "Both of these identities are readily established by employing the Jacobi triple product identity." |

§2 subtotal (8 entries): `modular_S_transform` 8/8 (100%);
`q_shift` 1/8 (E17); `class_field_galois_average` 0/8; `eisenstein_normal_ordering` 0/8.

#### §3 — Other Modular Equations (Entries 22-30)

| Entry | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| E22 (p. 367) | `modular_S_transform` | Logarithmic-derivative-of-theta-function identities; proof: "By using the product representations for ψ(q), ψ(q²), φ(q), φ(-q), and φ(-q²)" — Jacobi triple product chain. |
| E23 (p. 368) | `modular_S_transform` | "(23.1) ... is a modular equation of degree 8"; proof translates to ψ-identity via Entries 10(iii), 11(iii) of Ch. 17. |
| E24 (p. 368) | `modular_S_transform` | "If β has degree 16 over α, then √m = 2(1+β^(1/4))/(1+(1-α)^(1/4))"; explicit degree-16 modular equation. |
| E25 (p. 368) | `modular_S_transform` | "If β has degree 7 over α" + identity reducing to Entry 19(iii) + (i) of Ch. 19. |
| E26 (p. 369) | `modular_S_transform` | "If β has degree 7 over α" + degree-7 modular polynomial identity; proof uses Mathematica verification. |
| E27 (p. 370) | `modular_S_transform` | "Let γ have degree 9, and put m = z₁/z₃ and m' = z₃/z₉"; explicit degree-9 modular equation. |
| E28 (p. 370-372) | `modular_S_transform` | "If m denotes the multiplier of degree 9 and γ has degree 9" + polynomial identity. Berndt: "**Disproof**" — "Ramanujan made a sign error in his calculations. This analysis is evidence that Ramanujan also used parametric representations." Sign-error correction recorded but the firing operator is still `modular_S_transform`. |
| E29 (p. 372) | `modular_S_transform` | Theta-function identity from Entry 18(iv) of Ch. 16 — Jacobi-triple-product based. |
| E30 (p. 372) | `modular_S_transform` | "If β has degree 11 over α"; identity via Entries 7(vi), (vii) of Ch. 20. |

§3 subtotal (9 entries): `modular_S_transform` 9/9 (100%);
`q_shift` 0/9; `class_field_galois_average` 0/9; `eisenstein_normal_ordering` 0/9.

#### §4 — Identities Involving Lambert Series (Entries 31-37)

| Entry | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| E31 (p. 373) | `eisenstein_normal_ordering`, `modular_S_transform` | "(1/4)φ²(q)φ²(q²) = 1/4 + Σ (2k-1)q^(2k-1)/(1-q^(2k-1)) + Σ (2 + (-1)^k)kq^(2k)/(1+q^(2k))" — canonical Lambert-series form `Σ kq^k / (1±q^k)` matching the schema's `_test_eisenstein_normal_order` regex exactly. Proof: "By Entry 8(i) of Chapter 17 ... φ²(q) = 1 + 4 Σ (-1)^k q^(2k+1)/(1-q^(2k+1))" — quotation expanding `φ²` as a Lambert series. |
| E32 (p. 373) | `eisenstein_normal_ordering`, `modular_S_transform` | "φ(q)φ(q⁴) = 1 + 2 Σ (-1)^k q^(2k+1)/(1-q^(2k+1)) - 2 Σ (-1)^k q^(4k+2)/(1+q^(4k+2))" — canonical Lambert-series form. |
| E33 (p. 373-374) | `eisenstein_normal_ordering`, `modular_S_transform` | "If n is real, then 1 + 4 Σ q^k cos(nk)/(1+q²ᵏ) = φ³(-q²) · [theta-quotient]" — quasi-Lambert series with cosine weight. Proof uses Jacobi triple product identity (modular-S move). |
| E34 (p. 374) | `eisenstein_normal_ordering`, `modular_S_transform`, `class_field_galois_average` | "If (n/3) denotes the Legendre symbol, then q ψ³(q³)/ψ(q) = Σ (n/3) qⁿ/(1-q^(2n))" — Lambert series with Legendre-symbol coefficients. The `(n/3)` IS a discrete `class_field_galois_average` move (Galois character on Q(√-3)). |
| E35 (p. 374-376) | `eisenstein_normal_ordering`, `modular_S_transform`, `class_field_galois_average` | "If (n/3) denotes the Legendre symbol, then φ³(q³)/φ(q) = 1 - 2 Σ (n/3) qⁿ/(1-(-q)ⁿ)" — same flavour as E34 with Legendre symbol. |
| E36 (p. 376) | `eisenstein_normal_ordering`, `modular_S_transform`, `class_field_galois_average` | "ψ³(-q³)/ψ(-q) - ψ³(q³)/ψ(q) = 2q ψ³(q⁶)/ψ(q²)" — proof uses Entry 34 (which has Legendre symbol). |
| E37 (p. 376) | `eisenstein_normal_ordering`, `modular_S_transform`, `class_field_galois_average` | "ψ³(q)/ψ(q³) + ψ³(-q)/ψ(-q³) = 2 ψ³(q²)/ψ(q⁶)" — same family as E36. |

§4 subtotal (7 entries): `eisenstein_normal_ordering` 7/7 (100%);
`modular_S_transform` 7/7 (100%); `class_field_galois_average` 4/7 (E34,35,36,37);
`q_shift` 0/7.

#### §5 — Identities Involving Eisenstein Series (Entries 38-40)

| Entry | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| E38 (p. 377) | `eisenstein_normal_ordering`, `modular_S_transform` | "4L(q⁴) - L(q) = 3φ⁴(q)" — EXPLICIT Eisenstein series L(q) := 1 - 24 Σ kqᵏ/(1-qᵏ) (the weight-2 quasi-modular E₂!) appearing in identity. Berndt: "Entry 38 yields a very short proof of a famous result of C. G. J. Jacobi" — sum-of-four-squares r₄(n) = 8σ(n) for n ≢ 0 (mod 4). |
| E39 (p. 377-378) | `eisenstein_normal_ordering`, `modular_S_transform` | "[ratio of alternating series] = M - 480 Σ k²qᵏ/(1-qᵏ)²" — M(q) = 1 + 240 Σ k³qᵏ/(1-qᵏ) (weight-4 Eisenstein E₄). |
| E40 (p. 378) | `eisenstein_normal_ordering`, `modular_S_transform` | "If M(q) is defined by (39.1), then M(q) = φ⁸(q) + 256qψ⁸(q)" — directly relates E₄ to theta powers. |

§5 subtotal (3 entries): `eisenstein_normal_ordering` 3/3 (100%);
`modular_S_transform` 3/3 (100%); `class_field_galois_average` 0/3; `q_shift` 0/3.

#### §6 — Modular Equations in the Form of Schläfli (Entries 41-52)

| Entry | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| E41 (p. 378-379) | `modular_S_transform` | Schläfli-form mod eqns of degrees 11, 13, 17, 19. Berndt: "These modular equations were established by Schläfli in 1870." Pure Schläfli-style polynomial identity in P and Q (theta-quotient parametrisations). |
| E42 (p. 379-380) | `modular_S_transform` | Composite modular equation αβγδ have degrees 1, 5, 7, 35 → P, Q polynomial identity. Berndt: "The following proof was given by Ramanathan" using Entry 18(v) of Ch. 20. |
| E43 (p. 380) | `modular_S_transform` | "If α, β, γ, δ have degrees 3, 1, 5, 15 ..."; proof in Berndt: "via the theory of modular forms" (per §6 framing on p. 382: "we have resorted to the theory of modular forms"). |
| E44 (p. 380) | `modular_S_transform` | Same form, degrees 5, 1, 3, 15; modular-forms proof. |
| E45 (p. 380) | `modular_S_transform` | Degrees 1, 3, 7, 21; modular-forms proof. |
| E46 (p. 380) | `modular_S_transform` | Degrees 7, 1, 3, 21; modular-forms proof. |
| E47 (p. 380) | `modular_S_transform` | Degrees 3, 1, 11, 33; modular-forms proof. |
| E48 (p. 381) | `modular_S_transform` | Degrees 5, 1, 7, 35; modular-forms proof. |
| E49 (p. 381) | `modular_S_transform` | Degrees 5, 1, 11, 55; modular-forms proof. |
| E50 (p. 381) | `modular_S_transform` | Degrees 1, 5, 7, 35; uses R, T parametrisations; modular-forms proof. |
| E51 (p. 381) | `modular_S_transform` | Degrees 1, 13, 3, 39; modular-forms proof. |
| E52 (p. 381-384) | `modular_S_transform` | Degrees 1, 13, 5, 65; modular-forms proof. Berndt explicitly: "**As in Part III, the principal theorem to be utilized is the valence formula (Rankin, Theorem 4.1.4)**" — F a modular form of weight r and multiplier system v on Γ a subgroup of finite index in Γ(1), then Σ Ord(F; z) = r·ρ_Γ. Tables of order computations at cusps r/s for Γ(2)∩Γ₀(n). |

§6 subtotal (12 entries): `modular_S_transform` 12/12 (100%);
`q_shift` 0/12; `class_field_galois_average` 0/12; `eisenstein_normal_ordering` 0/12.

#### §7 — Modular Equations in the Form of Russell (Entries 53-67 + Lemma 67)

| Entry | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| E53 (p. 384-385) | `modular_S_transform` | Russell-form mod eqn, degree 15. "An equivalent formulation of (53.4) was first proved by Russell." |
| E54 (p. 385) | `modular_S_transform` | Degree 31. Equivalent to Entry 22(ii) of Ch. 20 (Part III). |
| E55 (p. 385) | `modular_S_transform` | Degree 47. "Entry 55 is identical to Russell's modular equation of degree 47." |
| E56 (p. 385-386) | `modular_S_transform` | Degree 71. Russell-form. |
| E57 (p. 386) | `modular_S_transform` | Degree 95. Russell-form. |
| E58 (p. 386) | `modular_S_transform` | Degree 19. "An equivalent form of (58.4) was first proved by Russell." |
| E59 (p. 386) | `modular_S_transform` | Degree 27. "This result is due to Russell." |
| E60 (p. 387) | `modular_S_transform` | Degree 35. "An equivalent version of (60.1) was established by Russell." |
| E61 (p. 387) | `modular_S_transform` | Degree 59. Russell-form. |
| E62 (p. 387) | `modular_S_transform` | Degree 9. Russell-form proven by Russell. |
| E63 (p. 387-388) | `modular_S_transform` | Degree 13. "Russell proved [an equation] which in Ramanujan's notation becomes P^7 - R(105P⁴ + 22P²Q + Q²) + 64R²P = 0." |
| E64 (p. 388) | `modular_S_transform` | Degree 17. Russell-form. |
| E65 (p. 388) | `modular_S_transform` | Degree 29. "This modular equation was essentially proved by Russell." |
| E66 (p. 388) | `modular_S_transform` | Degree 37. "Ramanujan evidently failed to determine an exact modular equation of degree 37. ... R. P. R. Hanna [1, p. 48] derived a modular equation of degree 37 in the 19/2 degree." Sign-error retraction recorded. |
| E67 / Lemma 67 (p. 390-391) | `modular_S_transform`, `q_shift` | Berndt provides this as Lemma 67 to validate Ramanujan's "n ≡ 7, 3, 11, 15 (mod 16)" page-303 cryptic listings. Proof: "From the corollary to Entry 31 of Chapter 16 ψ(q) = f(q⁶, q¹⁰) + qf(q², q¹⁴); ..., ψ(q)ψ(-q) = f²(q⁶, q¹⁰) - q²f²(q², q¹⁴)" — pure q-Pochhammer / theta-product manipulation. Tagged `q_shift` for explicit f(a, b) theta-product expansion (q-shift's machinery), `modular_S_transform` because Lemma 67 supports a modular-equation system. |

§7 subtotal (15 entries — counting E67/Lemma 67 as one): `modular_S_transform`
15/15 (100%); `q_shift` 1/15 (E67); `class_field_galois_average` 0/15;
`eisenstein_normal_ordering` 0/15.

#### §8 — Modular Equations in the Form of Weber (Entries 68-75)

| Entry | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| E68 (p. 392) | `modular_S_transform` | "The next six modular equations are of Weber-type. ... α, β, γ, δ have degrees 1, 3, 11, 33"; first established by Weber. Composite-degree Weber-style identity in P, Q, R. |
| E69 (p. 392) | `modular_S_transform` | Degrees 1, 5, 7, 35; Weber-form. |
| E70 (p. 392) | `modular_S_transform` | Degrees 1, 5, 11, 55; Weber-form. |
| E71 (p. 393) | `modular_S_transform` | Degrees 1, 3, 17, 51; Berndt: "**We proceed as in the proofs of Entries 43-52**" — explicit modular-form valence-formula proof. Cusps and orders calculated for Γ(2)∩Γ₀(51) with Mathematica. |
| E72 (p. 394) | `modular_S_transform` | Degrees 1, 3, 3, 9; modular-form proof with rρ_Γ = 36. |
| E73 (p. 394-395) | `modular_S_transform` | Degrees 1, 3, 9, 27; "**Disproof**" — Berndt shows Ramanujan made a coefficient error (the proposed identity has -46080q¹⁹ in the q-expansion of LHS, not zero). Still firing operator-wise (the *attempt* was a Weber-form modular equation). |
| E74 (p. 395-396) | `modular_S_transform` | Degrees 1, 5, 5, 25; "**Disproof**" — Berndt: "Ramanujan either miscalculated some coefficients in the q-series for l(q), or did not calculate enough of them." Operator-wise still modular_S. |
| E75 (p. 396-397) | `modular_S_transform` | "Let β have degree 49 over α"; "To the best of our knowledge, Entry 75 is the first and only modular equation of degree 49 that can be found in the literature." Modular-form proof: F a modular form of weight 5 on Γ(2)∩Γ₀(49), valence formula Σ Ord(F;z) = 0 with rρ_Γ = 140, Mathematica q-expansion shown for 0 ≤ n ≤ 140. |

§8 subtotal (8 entries): `modular_S_transform` 8/8 (100%);
`q_shift` 0/8; `class_field_galois_average` 0/8; `eisenstein_normal_ordering` 0/8.

#### §9 — Series Transformations Associated with Theta-Functions (Entries 76-78)

| Entry | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| E76 (p. 397-398) | `modular_S_transform` | "Σ (-1)ⁿ / [(2n+1) cosh{(2n+1)y/2}] = √x/2 · Σ (½)_n xⁿ / [n! (2n+1)]" with x, y, z defined by `e^(-y) := F(x) := exp(-π z(1-x)/z(x))` and `z(x) = ₂F₁(½, ½; 1; x)` — this is the *canonical* modular S-transform: x ↔ 1-x duality coming from the τ ↔ -1/τ symmetry of ₂F₁(½, ½; 1; x). |
| E77 (p. 398-401) | `modular_S_transform` | Companion to E76 (sinh vs cosh): "Σ (-1)ⁿ / [(2n+1)² sinh{(2n+1)y/2}] = √x/(2z) · Σ ..." with the same hypergeometric base; same E76-flavour transformation. |
| E78 (p. 402-403) | `modular_S_transform` | "With x, y, and z as in (76.1), (76.2), Σ 1 / [(2n+1)⁴ cosh{(2n+1)y/2}] = √x/(2z³) · [polynomial in (2/3)² and (1/2)² with leading x + ...]" — Berndt: "Sketch of Attempted Proof" — incomplete; same flavour. |

§9 subtotal (3 entries): `modular_S_transform` 3/3 (100%);
`q_shift` 0/3; `class_field_galois_average` 0/3; `eisenstein_normal_ordering` 0/3.

#### §10 — Miscellaneous Results (Entries 79-83)

| Entry | Operators fired | Berndt explicit-name quote / note |
|---|---|---|
| E79 (p. 403-404) | `modular_S_transform` | Two elliptic-integral identities with `(1+sin β)/(1-sin β) = (1+sin α)/(1-sin α) · ((1+x sin α)/(1-x sin α))²`. Proof uses Entry 6(iii) of Ch. 19 + tangent-half-angle. Although §10 is "miscellaneous", these are elliptic-integral degree-3 modular-equation derivatives. |
| E80 (p. 404-405) | `modular_S_transform` | Same flavour as E79 (more elliptic-integral algebra); uses Entry 17(xii) of Ch. 17 (a modular transformation). |
| E81 (p. 405-406) | `modular_S_transform` | Approximate identity F(2x/(1+x)) ≈ √t / [1 + (1-t)(1-t + (3/4)t²)] where F is the τ ↔ -1/τ Landen/inverse-Landen function from Entry 6(i) of Ch. 17. Tagged `modular_S_transform` for the Landen-transformation lineage. |
| E82 (p. 406) | `modular_S_transform` | F(1 - e^(-x)) ≈ x/(10+√(36+x²)) - (1/2160)(x/(8 + 7x²/50))^5 — approximate identity for the same F as E81. Same Landen-transformation lineage. |
| E83 (p. 407) | `modular_S_transform` | "Let x = 1 - φ⁴(-u)/φ⁴(u), where u := e^(-y) := exp(-π z(1-x)/z(x))" — explicit theta-quotient with τ ↔ -1/τ-respecting hypergeometric `z(x)`. Integral identity `∫ φ^(2n+4)(u)/u du = ∫ z^n(x)/(x(1-x)) dx` — a classical modular-S-equivariant Picard-Fuchs–type identity. |

§10 subtotal (5 entries): `modular_S_transform` 5/5 (100%);
`q_shift` 0/5; `class_field_galois_average` 0/5; `eisenstein_normal_ordering` 0/5.

### Per-operator aggregate counts (83 entries, 11-operator vocabulary)

| Operator | n_entries | % of 83 | Predicted (HUNT5b Ch. 17) | Hit? |
|---|---|---|---|---|
| `modular_S_transform` | 83 | **100.0%** | ≥50% (floor) | **YES (×2 floor)** |
| `eisenstein_normal_ordering` | 10 | **12.0%** | ~10% (bracket) | **YES (in bracket)** |
| `class_field_galois_average` | 4 | **4.8%** | ≥30% (floor) | **MISS (well below floor)** |
| `q_shift` | 4 | **4.8%** | ~25% (bracket) | **MISS (below bracket)** |
| `master_theorem` | 0 | **0.0%** | ≤5% (ceiling) | **YES (under)** |
| `mellin_inversion` | 0 | **0.0%** | (implicit ≤5%) | **YES (under)** |
| `FOURIER_SELF_RECIPROCITY` | 0 | 0.0% | ~0% (QR III) | YES |
| `FRACTIONAL_FUNCTIONAL_ITERATION` | 0 | 0.0% | ~0% | YES |
| `HARDY_ORDERS_OF_INFINITY` | 0 | 0.0% | ~0% | YES |
| `FRULLANI_LIMIT` | 0 | 0.0% | ~0% | YES |
| `MELLIN_PAIR_RECIPROCITY` | 0 | 0.0% | ~0% | YES |

### Per-section operator distribution

| Section | n | modular_S | eisenstein_normal | class_field | q_shift | Dominant pattern |
|---|---|---|---|---|---|---|
| §1 deg-3 (E1-13) | 13 | 13 (100%) | 0 (0%) | 0 (0%) | 1 (8%) | modular_S monoculture |
| §2 deg-5 (E14-21) | 8 | 8 (100%) | 0 (0%) | 0 (0%) | 1 (12%) | modular_S monoculture |
| §3 other deg (E22-30) | 9 | 9 (100%) | 0 (0%) | 0 (0%) | 0 (0%) | modular_S monoculture |
| **§4 Lambert series (E31-37)** | **7** | **7 (100%)** | **7 (100%)** | **4 (57%)** | **0 (0%)** | **modular_S + eisenstein + class_field** |
| **§5 Eisenstein (E38-40)** | **3** | **3 (100%)** | **3 (100%)** | **0 (0%)** | **0 (0%)** | **modular_S + eisenstein** |
| §6 Schläfli (E41-52) | 12 | 12 (100%) | 0 (0%) | 0 (0%) | 0 (0%) | modular_S monoculture |
| §7 Russell (E53-67) | 15 | 15 (100%) | 0 (0%) | 0 (0%) | 1 (7%) | modular_S monoculture |
| §8 Weber (E68-75) | 8 | 8 (100%) | 0 (0%) | 0 (0%) | 0 (0%) | modular_S monoculture |
| §9 series-transform (E76-78) | 3 | 3 (100%) | 0 (0%) | 0 (0%) | 0 (0%) | modular_S monoculture |
| §10 miscellaneous (E79-83) | 5 | 5 (100%) | 0 (0%) | 0 (0%) | 0 (0%) | modular_S monoculture |

**The per-section distributions ARE structurally different.** §4
(Lambert series) and §5 (Eisenstein series) co-fire `modular_S_transform`
+ `eisenstein_normal_ordering` at 100% each; the rest of the chapter
(75 entries across §1-§3, §6-§10) is `modular_S_transform`-monoculture
with virtually no `eisenstein_normal_ordering` firing. §4 additionally
fires `class_field_galois_average` at 57% (Legendre-symbol-coefficient
Lambert series E34-37). This is a clean intra-chapter operator
specialisation: the **kind of identity** dispatches to a specific
operator subset.

## Surprises

1. **`modular_S_transform` saturates at 100% (83/83).** This is the
   *strongest possible* hit — every single entry in the chapter fires the
   operator, including the §4 Lambert-series and §5 Eisenstein-series
   identities (which co-fire `eisenstein_normal_ordering`), the §9
   hypergeometric series-transformation identities, and the §10
   approximate identities involving the modular ₂F₁(½, ½; 1; x) and the
   Landen transformation. Far above the ≥50% predicted floor. The chapter
   is the *most modular-S-saturated* of any chapter tagged so far
   (Ch. 32 was 91.7%, QRs were 0%).

2. **`class_field_galois_average` MISSED its 30% floor decisively, firing
   only 4 times (4.8%).** This is the central surprise of the pass. The
   four firings are E34, E35, E36, E37 — all in §4 — where the Lambert
   series is weighted by the Legendre symbol `(n/3)` on Q(√-3). The
   predicted 30% floor assumed Galois-conjugacy of modular-polynomial
   roots would feature prominently in modular-equation work, but Berndt's
   commentary treats the modular-equation polynomials *as polynomial
   identities in (α, β, m)* rather than as Galois orbits — the chapter
   never invokes Heegner orbits, the j-function at CM points, the ring
   class field, or the class polynomial H_D(X). Class invariants G_n
   appear briefly in E11's proof but only as a substitution for theta-
   quotient denesting (per the diary 22 "near match ≠ match" rule, not
   tagged `class_field_galois_average`). The prediction over-weighted
   the modular-equation→class-field connection at the *operational*
   level (vs the theoretical level).

3. **`q_shift` MISSED its ~25% bracket, firing only 4 times (4.8%).**
   Surprising in absolute terms but interpretable: this chapter is
   dominated by *finite polynomial identities in algebraic
   parametrisations* (α, β, m, the Schläfli/Russell/Weber P-Q-R triples).
   The q-Pochhammer machinery rarely surfaces in the body of the chapter
   because the modular-equation form has already collapsed q-products
   into algebraic relations. Compare Ch. 32 where `q_shift` was 100%
   (because the entries were CFs written as q-Pochhammer products, not
   modular-polynomial roots).

4. **§4 + §5 (10 entries) fire `eisenstein_normal_ordering` at 100% within
   those sections, but the operator fires only 12% chapter-wide.** This
   is exactly the schema's intended use: Lambert series Σ kqᵏ/(1-qᵏ)
   and explicit Eisenstein series L, M trigger the operator; the rest of
   the chapter doesn't. The schema's regex would catch this correctly
   if applied to the entry text directly. Within §5 (Entries 38-40), the
   weight-2 quasi-modular L(q) is explicitly normal-ordered: "4L(q⁴) -
   L(q) = 3φ⁴(q)" with the divisor-sum constant-term extraction making
   Jacobi's r₄(n) = 8σ(n) fall out. This is the canonical
   `eisenstein_normal_ordering` move in textbook form.

5. **`class_field_galois_average` fires ONLY on Lambert series weighted
   by the Legendre symbol `(n/3)`.** A clean operator-specialisation
   signal: the Galois character on Q(√-3) (a degree-2 Galois orbit
   on the rational primes split/inert in Z[ω]) is the *only* form of
   `class_field_galois_average` Ramanujan deploys in Ch. 36, and only
   in 4 of 83 entries. This contradicts Ch. 32 (where 33% fired the
   operator via class invariants G_n in special-value subroutine).

6. **All five QR-III operators stay at 0%.** Fractional iteration, Hardy
   orders, Frullani limit, Fourier self-reciprocity, Mellin-pair reciprocity
   — zero firings across 83 entries. Same as Ch. 32, same as the QR-vs-NB
   contrast.

7. **`master_theorem` and `mellin_inversion` both fire 0 times.** The
   Mellin/Master toolkit is absent from Ch. 36. Same as Ch. 32 (also 0).
   Toolkit-split between QRs and Notebooks is reinforced at chapter #2.

8. **Three "disproof" entries (E28, E73, E74) and partial-error remarks
   on E5, E66 — Berndt's chapter-wide error rate ~6%.** Modular equations
   are computationally hard; Ramanujan made sign errors and coefficient-
   miscount errors. Berndt's discipline of reporting these as "Disproof"
   (with the operator-attempt still tagged for our analysis) is a model
   for the same discipline this run uses.

9. **Berndt's modular-form valence-formula proof technique (§6, §8) is
   itself an out-of-schema operator that fires in 20 entries (E43-52 +
   E71-75).** I tagged it as `modular_S_transform` (the parent operator
   for modular-form machinery), but the proof technique is specific
   enough that a future schema revision might split it out as
   `modular_form_residue_at_cusps` — see "Out-of-schema operators"
   above. This would not change the headline conclusions (still
   `modular_S_transform` dominant) but would give a sharper
   characterisation of the chapter's proof-technique distribution.

## Verdict

**PARTIALLY SUPPORTED on Ch. 36.**

Hit-count against the prediction table:

| Predicted-dominant operator | Floor/bracket | Actual | Met? |
|---|---|---|---|
| `modular_S_transform` | ≥50% | **100.0%** | **YES (×2)** |
| `class_field_galois_average` | ≥30% | **4.8%** | **NO** |
| `q_shift` | ~25% | **4.8%** | **NO** |
| `eisenstein_normal_ordering` | ~10% | **12.0%** | YES (in bracket) |

**2 of the 4 predicted-dominant operators hit (modular_S strongly,
eisenstein_normal_ordering exactly in-bracket).** Per the rubric ("≥3 of
4 predicted-dominant operators hit their floor"), the test fails on this
side. The verdict is **PARTIALLY SUPPORTED**, not SUPPORTED.

| Predicted-rare operator | Ceiling | Actual | Met? |
|---|---|---|---|
| `master_theorem` | ≤5% | 0.0% | YES |
| `mellin_inversion` | ≤5% (implicit) | 0.0% | YES |
| `FRACTIONAL_FUNCTIONAL_ITERATION` (QR III) | ~0% | 0.0% | YES |
| `HARDY_ORDERS_OF_INFINITY` (QR III) | ~0% | 0.0% | YES |
| `FOURIER_SELF_RECIPROCITY` (QR III) | ~0% | 0.0% | YES |
| `FRULLANI_LIMIT` (QR III) | ~0% | 0.0% | YES |
| `MELLIN_PAIR_RECIPROCITY` (QR III) | ~0% | 0.0% | YES |

**All 7 predicted-rare operators stay under their ceilings.** Per the
rubric ("≥3 of 4 predicted-rare operators stay under their ceiling"),
this side of the test passes decisively.

**Bottom line:** The result is **PARTIALLY SUPPORTED**, with the
qualification that `modular_S_transform` fires at 100% (twice the
predicted floor) and `class_field_galois_average` + `q_shift` both
miss their respective brackets/floors. The two misses are interpretable:

- `class_field_galois_average` miss: Ch. 36 treats modular-equation
  polynomials as algebraic identities in (α, β, m), not as Galois orbits
  on CM points. The Heegner-orbit / j-function-at-CM-point machinery is
  in *Ch. 34* (class invariants and singular moduli), not Ch. 36. The
  Hunt 5b Ch. 17 prediction conflated "modular equations" with
  "modular-equation Galois theory" — operationally, those are different
  chapters in Ramanujan's working ontology.
- `q_shift` miss: q-Pochhammer machinery has already collapsed into the
  algebraic parametrisations (α, β as theta-quotients evaluated at the
  level-N modular point) by the time Ramanujan writes the modular
  equation. The q-shift firing requires explicit q-Pochhammer notation
  in the body, which Ch. 36 mostly suppresses in favour of α-β-m
  notation.

The right operator-distribution headline for Ch. 36 is **`modular_S_transform`
saturated monoculture (100%) with intra-chapter specialisation: Lambert/
Eisenstein-series sections (§4-§5, 12% of chapter) co-fire
`eisenstein_normal_ordering` at 100% within those sections; the rest
of the chapter does not.**

## Implications for the toolkit-split hypothesis

This is **the second Hunt 5b chapter** (Ch. 32 in diary 22 was the
first). The headline contrast is now sharper:

| Operator | QR I+II+III | NB V Ch. 32 | NB V Ch. 36 |
|---|---|---|---|
| `modular_S_transform` | 0% | 91.7% | **100.0%** |
| `q_shift` | 0% | 100.0% | 4.8% |
| `class_field_galois_average` | 0% | 33.3% | 4.8% |
| `eisenstein_normal_ordering` | 0% | 8.3% | 12.0% |
| `master_theorem` | 57.6% | 0% | 0% |
| `FRACTIONAL_FUNCTIONAL_ITERATION` | 15% | 0% | 0% |
| `FOURIER_SELF_RECIPROCITY` | 15% | 0% | 0% |
| Mellin/Master "QR toolkit" | dominant | 0% | 0% |
| Modular machinery | 0% | dominant | dominant |

**KEY OBSERVATION: Ch. 36's dominant-operator signature DIFFERS from
Ch. 32's.** Ch. 32 was a *pair*-dominant chapter (`q_shift` + `modular_S`,
both >90%) with `class_field_galois_average` at 33%. Ch. 36 is a
*single-operator*-dominant chapter (`modular_S` saturated at 100%) with
the other three predicted operators much lower than Ch. 32's
distribution. The chapters share `modular_S_transform` dominance but
diverge sharply on `q_shift` (100% in Ch. 32, 4.8% in Ch. 36) and
mildly on `class_field_galois_average` (33% in Ch. 32, 4.8% in Ch. 36).

This is **strong inter-chapter variance evidence**: the toolkit-split
hypothesis predicted that different chapters would have different
dominant operators within the modular toolkit. **The hypothesis is now
substantively supported**: the two chapters share the parent
`modular_S_transform` operator but specialise differently in their
secondary operators, exactly the "intra-toolkit specialisation"
pattern the [HUNT5b_PREDICTIONS §"Inter-chapter variance prediction"](../insights/HUNT5b_PREDICTIONS.md)
spelled out as the *strong-support* condition.

**Confidence on the broader hypothesis:** medium → medium-high. With
2 chapters showing inter-chapter operator-distribution variance and zero
overlap with the QR toolkit, the toolkit-split hypothesis crosses from
"supported on one chapter" into "supported with replication and
intra-toolkit specialisation". One more chapter (Ch. 34 class
invariants, Ch. 35 theta-function values, or a re-tagging of Ch. 16
from facsimile) would push it to "Established" per the
HUNT5b_PREDICTIONS rubric.

**Per-section operator distribution within Ch. 36 (intra-chapter):**
- §1, §2, §3, §6, §7, §8, §9, §10 (75 entries): `modular_S_transform`
  monoculture, no other operator firing materially.
- §4 (7 entries): `modular_S_transform` + `eisenstein_normal_ordering`
  + `class_field_galois_average` triple-firing on Lambert-series-with-
  Legendre-symbol identities.
- §5 (3 entries): `modular_S_transform` + `eisenstein_normal_ordering`
  pair-firing on Eisenstein L, M, N identities.

This intra-chapter section specialisation is the same flavour as Ch. 32's
family-A/B/C-ambig/C/D specialisation (diary 22) — Ramanujan's working
representation seems to be organised by *the kind of identity* (algebraic
parametrisation, Lambert series, Eisenstein, q-Pochhammer evaluation),
and the operator selection follows the identity type.

## Honest caveats

- **Hand-judgment, one-pass, no inter-rater reliability check.** Same as
  diary 20 and diary 22. ±5-8 percentage points on per-operator
  percentages is the honest uncertainty.
- **The `modular_S_transform` tag at 100%** is the headline result and
  is partially a consequence of liberal scoping: any invocation of
  level-N modular-equation machinery, Jacobi triple product identity,
  modular-form valence formula, Landen transformation, or theta-function
  inversion identity counts. A stricter "only proofs that explicitly
  invoke τ → -1/τ" scoping would drop the number considerably (probably
  to ~70-80% — leaving out §6 Schläfli polynomial-identity entries that
  Berndt proves by *coefficient comparison* rather than by direct
  τ ↔ -1/τ substitution). The looser scoping is justified because
  (a) modular equations *are* the τ ↔ -1/τ-equivariant identities for
  level-N modular curves, by definition; (b) the modular-form valence
  formula at cusps is the modular-S move (cusps are the τ ↔ -1/τ fixed
  points of Γ(2)∩Γ₀(n)); (c) the floor of ≥50% in HUNT5b_PREDICTIONS
  is met under either scoping.
- **The `class_field_galois_average` 4.8%** is at the boundary of
  near-match decisions. Including the E11 class-invariant-G_n
  substitution (excluded per "near match ≠ match" rule) and the E8
  "n² is related to class invariants" (excluded for similar reason)
  would raise the number to 7.2% — still well under the 30% floor.
- **The `modular_form_residue_at_cusps` out-of-schema operator** fires
  in 20 entries (E43-52, E71-75). All 20 were tagged
  `modular_S_transform` as the parent operator. A future schema
  revision splitting this out would not change the chapter-wide
  `modular_S_transform` count (still 100% as the parent fires too),
  but would let a future analysis quantify "Berndt's modular-forms
  proof rate" separately. Flagging as a future-schema-extension lead.
- **The §4 Lambert-series entries' co-firing of three operators**
  (modular_S + eisenstein + class_field) might inflate the
  `eisenstein_normal_ordering` count for the chapter as a whole if
  Berndt's reorganisation places more Lambert-series identities in this
  chapter than Ramanujan would have grouped together. The chapter-wide
  12% rate is in the predicted ~10% bracket either way.
- **Berndt-reorganised vs Ramanujan-organised.** Ch. 36 is "Modular
  Equations and Theta-Function Identities in Notebook 1" — i.e., Berndt's
  collection of all modular-equation material from Ramanujan's *first*
  notebook (the rougher, less-organised one) that didn't make it into
  the second-notebook Ch. 19-21 already covered in NB Part III. This
  introduces some *Berndt* organisation: Berndt grouped Schläfli-form
  identities (§6), Russell-form (§7), Weber-form (§8) by reference-paper-
  form rather than by Ramanujan's own page order. The chapter-internal
  section structure thus reflects Berndt's editorial choices, not
  Ramanujan's working organisation. The operator-tagging is robust to
  this (the *operator* is the same regardless of which section the
  entry sits in), but the per-section breakdown should be read as
  Berndt-clustered, not Ramanujan-clustered.
- **Disproof entries (E28, E73, E74)** are tagged for their attempted
  operator (modular_S_transform), not for the underlying mistake. The
  operator firing is what matters for the toolkit-split hypothesis
  test; correctness of the identity is a different question.
- **Ambiguous-rate estimate.** Of 83 entries, ~6-8 had non-trivial
  near-match decisions: E5 (sign-discrepancy entry; tagged but with
  Berndt-noted issue), E11 (class_field_galois_average near-match
  excluded for G_n substitution), E8 (class_field near-match excluded
  for "n² is related to class invariants"), E81-E82 (modular_S
  near-match accepted for Landen-transformation lineage on
  approximate identities), and the §10 elliptic-integral entries E79-E80
  (modular_S accepted for degree-3 modular-equation lineage). So
  **~7-10% ambiguous-rate** — in line with diary 22's ~17% and diary
  20's ~12% for the QR pass. Including all the borderline class_field
  near-matches would push class_field from 4.8% → 7.2%, still well
  under the 30% floor. Including all the borderline modular_S
  near-matches would change nothing (already 100%).

## Bottom-line claim

The HUNT5b_PREDICTIONS Ch. 17 operator-distribution forecast is
**PARTIALLY SUPPORTED** at the rubric threshold (2 of 4 predicted-dominant
operators hit floor — modular_S strongly, eisenstein in bracket — vs 3
required for SUPPORTED; all 7 predicted-rare operators under ceiling).
The two misses — `class_field_galois_average` at 4.8% vs ≥30%, `q_shift`
at 4.8% vs ~25% — are the genuine prediction failures, interpretable
through Ch. 36's chapter-content (algebraic-parametrisation polynomial
identities, not Heegner-orbit Galois averages; algebraic vs q-Pochhammer
notation).

The QR-vs-Notebooks toolkit-split hypothesis is **strongly supported
with intra-toolkit specialisation** based on the combined evidence of
Ch. 32 (diary 22) and Ch. 36 (this diary): both chapters share
`modular_S_transform` dominance but diverge sharply on secondary
operators, exactly the strong-support pattern HUNT5b_PREDICTIONS
spelled out. **3 chapters needed for full "Established" verdict on
the rubric**; Ch. 34 (class invariants — should fire
`class_field_galois_average` ≥60% per HUNT5b_PREDICTIONS) is the most
informative next target.

**Confidence:** medium-high on the Ch. 36 PARTIALLY SUPPORTED verdict
(the `class_field_galois_average` miss is genuine and is honest); medium-
high on the broader hypothesis with 2 chapters of evidence and clean
inter-chapter variance.

## Follow-up leads

1. **Hunt 5b Ch. 34 (class invariants and singular moduli) tagging.**
   Same NB Part V volume (pp. 183-321), already in
   [`downloaded-pdfs/ramanujan-notebooks-v.pdf`](../downloaded-pdfs/ramanujan-notebooks-v.pdf).
   Highest-leverage next chapter to test the `class_field_galois_average`
   ≥60% prediction. If Ch. 34 fires `class_field` dominantly, the
   toolkit-split hypothesis crosses to "Established" with 3 chapters
   and 3 different dominant operators (q_shift+modular_S for Ch. 32;
   modular_S monoculture for Ch. 36; class_field+modular_S for Ch. 34).
2. **Extend the operator schema with `modular_form_residue_at_cusps`**
   as a separate operator (20 Ch. 36 entries fire it; would also fire
   in Ch. 34 and parts of Ch. 32). Then re-tag Ch. 36 §6 + §8 + §7
   to refine the "Berndt modular-forms proof rate" separately from
   the parent `modular_S_transform` count.
3. **Cross-validate this pass with an independent re-tagging.** Same
   recommendation as diary 22; the 100% `modular_S_transform` tag
   deserves a second-opinion check.
4. **Hunt 5b Ch. 35 (values of theta-functions)** as a complement.
   Smaller chapter (24 results, pp. 323-352, already in this PDF) —
   should fire `class_field_galois_average` heavily (theta-function
   values at CM points are the chapter's primary topic). Cheap test
   of the same intra-toolkit specialisation hypothesis.
5. **Tag the `modular_form_residue_at_cusps` candidate operator
   addition formally**: it has appeared as the dominant proof technique
   in NB V Ch. 32 §1 (Watson cited several times), Ch. 36 §6 + §8
   (Berndt's preferred technique), and is the technique R. Rankin
   makes central in *Modular Forms and Functions* (1977, cited by
   Berndt). For a recognizer / schema covering modular-equation
   corpora, this is the missing 11→12th operator.
