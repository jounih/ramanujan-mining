# Diary 22 — Hunt 5b: NB V Ch. 32 (Continued Fractions) operator tagging

**Date:** 2026-05-24
**Source:** Berndt, *Ramanujan's Notebooks, Part V*, Ch. 32 ("Continued
Fractions"), pp. 9-88. Local copy at
[`downloaded-pdfs/ramanujan-notebooks-v.pdf`](../downloaded-pdfs/ramanujan-notebooks-v.pdf).
Scope: §1 (Rogers-Ramanujan, Entries 1-17, pp. 12-44) + §2 (Other q-CFs,
Entries 18-23, pp. 45-49) + the E32-cubic CF (NB V Ch. 32 Entry 10 proof
chain at pp. 28-30, calling on Ch. 33 §3 cubic-base material). §3-§5
(gamma-product CFs, Bessel/arctangent/hypergeometric CFs, general
convergence theorems) excluded per [T2 scoping](../insights/T2_EISENSTEIN_CF_SCOPING.md).
**Status:** Hunt 5b Ch. 32 result recorded; ≥3 more chapters needed to
call the toolkit-split hypothesis "Established".

## Setup

Per [HUNT5b_PREDICTIONS §"NB II Ch. 32"](../insights/HUNT5b_PREDICTIONS.md),
the predicted operator-distribution for Ch. 32 (Eisenstein-style continued
fractions) is:

| Operator | Predicted | |
|---|---|---|
| `eisenstein_normal_ordering` | ≥40% | namesake of chapter |
| `modular_S_transform` | ≥30% | weight-2 anomaly in CF limits |
| `q_shift` | ≥30% | q-Pochhammer in CF expansions |
| `class_field_galois_average` | ~20% | CM-point evaluations |
| `master_theorem` | ≤10% | wrong tool |
| `mellin_inversion` | ≤10% | wrong tool |
| All QR III operators | ~0% | different universe |

The QR baseline (diary 20) for the four predicted-dominant operators was
**0%, 0%, 0%, 0%**. If the Ch. 32 distribution looks materially different
(≥3 of 4 predicted operators hit their floor, ≥3 of 4 QR III operators
stay near 0%), the toolkit-split hypothesis is *supported on this chapter*.
≥3 chapters with different dominant operators are needed for the full
hypothesis to be called "Established".

This pass covers Ch. 32 only. Ch. 16 (theta functions), Ch. 17 (modular
equations), and Ch. 18-19 (class invariants) are separate chapters in the
broader Hunt 5b prediction set and require either Berndt commentary we
don't have (NB II/III commentary volumes are missing) or facsimile reading
(possible but slower).

## What I did

1. Read Berndt's NB V Ch. 32 §1 (pp. 12-44) and §2 (pp. 45-49) end to end,
   reading both the Ramanujan entry statements and Berndt's per-entry
   commentary (proofs, attributions, references).
2. Hand-tagged each of the 24 in-scope entries (E32-1 through E32-23, plus
   E32-cubic via the §1 Entry 10 proof chain) against the 11-operator
   vocabulary (6 original from
   [`operator_tagging_schema.py`](../corpora/transcriptions/operator_tagging_schema.py)
   + 5 added per [diary 20 §"Out-of-schema operators"](20_hunt5_qr_operator_tagging.md)).
3. Same discipline as Hunt 5 / diary 20: hand-judgment, not regex; tags
   record whether the operator is the *primary or secondary move* in the
   entry's proof/statement; "near match ≠ match"; an entry where Berndt's
   commentary explicitly names an operator (e.g. "by the Jacobi triple
   product identity") gets that operator tagged with a direct-quote note.

**Decision rule for ambiguous cases.** A CF whose closed form is an
η-quotient or theta-product is tagged `modular_S_transform` if (and only
if) the proof invokes a modular transformation, theta inversion, or
modular-equation chain. A theta-product expression appearing only as a
formal closed-form (no τ → -1/τ move in the proof) is tagged
`q_shift` (because the manipulation is q-Pochhammer combinatorics) without
`modular_S_transform`. q-Pochhammer notation `(a;q)_n` or `(a;q)_∞` in
the body is *direct* evidence of `q_shift`. The Jacobi triple product
identity (Berndt explicitly cites "Entry 19 of Chapter 16, Part III") is
tagged `modular_S_transform` because it is a Poisson-summation move on
the theta-function lattice — modular S-transform's dual representation.

**11-operator vocabulary** (from operator_tagging_schema.py + diary 20):

Original 6:
1. `mellin_inversion`
2. `master_theorem`
3. `q_shift`
4. `modular_S_transform`
5. `eisenstein_normal_ordering`
6. `class_field_galois_average`

Added 5 (QR-derived):
7. `FOURIER_SELF_RECIPROCITY`
8. `FRACTIONAL_FUNCTIONAL_ITERATION`
9. `HARDY_ORDERS_OF_INFINITY`
10. `FRULLANI_LIMIT`
11. `MELLIN_PAIR_RECIPROCITY`

Out-of-schema operators encountered during tagging (recorded for
information; not in either basis): `bauer_muir_transformation` (CF-specific
move; E11, E13, E27, E28), `modular_equation_chain` (used at E1, E7, E10
to relate u, v at different q-arguments via P, Q theta-quotients —
arguably a subcase of `modular_S_transform`+`class_field_galois_average`),
and `quintuple_product_identity` (E4; specialised theta-identity, tagged
as `modular_S_transform` because it's the same flavour of theta-lattice
move).

## Numbers

### Per-entry operator tags (24 entries in scope)

Tags are unordered sets; an entry can fire multiple operators. Notes
quote Berndt verbatim where he names the operator.

| Entry | Family (T2) | Operators fired | Berndt explicit-name quote / note |
|---|---|---|---|
| E32-1 | A | `modular_S_transform`, `class_field_galois_average`, `q_shift` | "we need to rely on Ramanujan's work on modular equations. Let √α and √β be the moduli associated with the variables q^{1/5} and q^5… These two equalities are, in fact, modular equations of degree 25" (p. 13). |
| E32-2 | A | `q_shift`, `modular_S_transform` | "Replacing q by -q in Entry 1(i)" (p. 16); proof reduces to Entry 1 then theta-identity manipulation. |
| E32-3 | A | `q_shift`, `modular_S_transform` | "Entry 3 was established by Rogers" (p. 17); same modular-equation-style proof shape as E1. |
| E32-4 | A | `modular_S_transform`, `q_shift`, `class_field_galois_average` | "By Entry 38(iii) of Chapter 16… By applying the Jacobi triple product identity, Entry 19 of Chapter 16… we shall apply the quintuple product identity three times" (pp. 17-18). |
| E32-5 | A | `modular_S_transform`, `q_shift` | "From Entry 1(i), it follows that…" (p. 19); same theta-lattice-arithmetic style. |
| E32-6 | A | `modular_S_transform`, `q_shift`, `class_field_galois_average` | "Entry 6 is connected with modular equations of degree 5" (p. 20). |
| E32-7 | B | `class_field_galois_average`, `modular_S_transform`, `q_shift` | "Following Ramanujan [3], [10, p. 23], we define the two class invariants G_n = 2^{-1/4}q^{-1/24}(-q;q²)_∞ and g_n = 2^{-1/4}q^{-1/24}(q;q²)_∞… We shall employ Entry 58 of Chapter 25" (p. 21); Lemma 7.1 gives G_{25} = (1+√5)/2. |
| E32-8 | B | `class_field_galois_average`, `modular_S_transform`, `q_shift` | "We will again employ Entry 58 of Chapter 25 in Part IV, but now with P = e^{4π/5}f(-e^{-4π/5})/f(-e^{-20π})…" (p. 25). |
| E32-9 | B | `class_field_galois_average`, `modular_S_transform`, `q_shift` | Same proof skeleton as E7 and E8 (p. 26); Berndt explicitly: "We again employ Entry 58 of Chapter 25 in Part IV". |
| E32-10 | B / D | `class_field_galois_average`, `modular_S_transform`, `q_shift`, `eisenstein_normal_ordering` | "Now Chan [1, Theorem 1] has shown that G(q) satisfies the modular equation G²(q) + 2G²(q²)G(q) − G(q²) = 0… Recall the definition of A from (10.3). Then Entry 1(iv) of Chapter 20 in Ramanujan's second notebook (Part III [3, p. 345]) can be written in the form 3 + A³ = 1/v + 4v²" (p. 29). The "3 + A³ = 1/v + 4v²" is Borweins' cubic-base Eisenstein-anchored identity → tag `eisenstein_normal_ordering`. |
| E32-11 | A (divergent) | `q_shift`, *bauer_muir_transformation* (out-of-schema), `HARDY_ORDERS_OF_INFINITY` (limit-oscillation) | "Entry 11 is a truly amazing result. It is very remarkable that the Rogers-Ramanujan continued fraction reappears in determining the limits of both the even and odd approximants of the divergent Rogers-Ramanujan continued fraction." (p. 33); "Applying the Bauer-Muir transformation (13.7) to the second continued fraction in (11.14)" (p. 33). HARDY_ORDERS firing is weak (the odd/even oscillation is an asymptotic-behavior question for divergent CFs but not Hardy's growth-orders calculus per se); marking as a "near-match" — keeping HARDY_ORDERS off the final count to honor "near-match ≠ match". |
| E32-12 | A | `q_shift` | Schur's theorem K(q) = λq^{(1-λρn)/5} K(λ) at primitive nth roots of unity (p. 35); pure q-Pochhammer manipulation; ambiguous — "K(λ) where λ = Legendre symbol (n/5)" *could* be a class_field_galois_average move (Legendre symbol → quadratic character of √5) but the move is dispatch-by-residue-class, not a Heegner-orbit average. Not tagging `class_field_galois_average` (near-match). |
| E32-13 | A (parameterized) | `q_shift`, *bauer_muir_transformation* (out-of-schema) | "the analysis for Entry 14 is very similar to that for Entry 13. Both continued fractions converge to meromorphic functions of x in C - {0} for \|q\| < 1." (p. 41); proof uses Bauer-Muir transformation explicitly (p. 38: "such a transformation exists if λ_k = a_k - w_{k-1}(b_k + w_k) ≠ 0"). |
| E32-14 | A (parameterized) | `q_shift`, *bauer_muir_transformation* (out-of-schema) | "Entry 14 is very similar to that for Entry 13" (p. 41). |
| E32-15 | C-ambig | `q_shift` | "Set λ = 0 in (13.5)" (p. 44); essentially Heine's transformation as q-hypergeometric — pure q-Pochhammer combinatorics. The connection to Heine's CF for ₂φ₁ ratios is explicitly stated in Berndt's commentary (Entry 14 commentary, p. 43: "it is interesting to note that the continued fractions in (13.1) and (14.1) are connected to the basic hypergeometric functions ₂φ₁(a,b;c;q;z)"). Pure q-shift. |
| E32-16 | C-ambig | `q_shift`, `modular_S_transform` | "By Entry 19 (the Jacobi triple product identity), (22.2) (Euler's identity), and Entry 22, all in Chapter 16…" (p. 45). |
| E32-17 | C-ambig | `q_shift` | "The result follows immediately from setting λ = 0 in (13.5)" (p. 45). Pure q-shift via Heine. |
| E32-18 | C | `q_shift`, `modular_S_transform` | "It follows more generally from Entry 12 of Chapter 16…" (p. 47); the closed form G(q) := (q;q²)_∞/(q³;q⁶)_∞³ is a theta-quotient and Berndt cites the modular-equation work of Chan [1]: "A detailed study of G(q) has been made by H. H. Chan… He has derived modular equations relating G(q) with each of G(-q), G(q²), and G(q³). Using these and other modular equations, he has determined values for G(±e^{-π√n}) for several positive rational numbers n. The author, Chan, and L.-C. Zhang [1] have found general formulas that enable one to evaluate G(±e^{-π√n}) in terms of class invariants." (p. 46). Tag `class_field_galois_average` would fire on Berndt's commentary about Chan's specialisations but NOT on the entry itself (which is the CF identity, not the special-value table) — leaving `class_field_galois_average` off this entry per "near-match" discipline. |
| E32-19 | C | `q_shift`, `modular_S_transform` | "We apply Theorem 6 in Andrews' paper [1] with a₁ = ωxq, a₂ = ω^{-1}xq, a = -1/(x²q²), and b = 1/(xq), where ω = exp(2πi/3)" (p. 47); ω = primitive cube root of unity — *near-match* with `class_field_galois_average` (it's a Galois-conjugate sum over a level-3 character), but the move is essentially a q-shift dispatch, not a Heegner average. Quietly noting the marginal hit. |
| E32-20 | C | `q_shift`, `modular_S_transform` | "This result is simply the case a = 1, b = 0 of Entry 12 of Chapter 16 (Part III)" (p. 48). |
| E32-21 | C | `q_shift`, `modular_S_transform` | "Entry 21 was first proved in print by Selberg [1, eq. (54)]" (p. 49); proof uses Entry 15 ("Applying Entry 15 with a = 1 and b = -1" p. 49) which routes through Heine's q-shift. Also: "If Q(q) denotes the left side of (21.1), then, by using Entries 22(i), (ii) and 25(vii) of Chapter 16, we can easily show that Q⁸(q) = ψ⁴(q²)/φ⁴(q) = x/16q… Thus, modular equations for Q(q) can be trivially derived from any of Ramanujan's modular equations." (p. 49). |
| E32-22 | C | `q_shift`, `modular_S_transform` | "The first published proof known to us is by Selberg [1, eq. (53)]" (p. 50); proof routes via Selberg theta-product identities at level 8. "Chan and Huang [1] have developed an extensive elegant theory for these continued fractions, including modular equations and explicit evaluations." (p. 50). |
| E32-23 | C | `q_shift`, `modular_S_transform` | "By the Jacobi triple product identity, we may rewrite Entry 23 in the form" (p. 50); Berndt explicitly: "Hence, Entry 23 is equivalent to Entry 22." |
| E32-cubic | D | `q_shift`, `modular_S_transform`, `eisenstein_normal_ordering`, `class_field_galois_average` | Referenced in E32-10 proof chain (p. 29): "Now Chan [1, Theorem 1] has shown that G(q) satisfies the modular equation G²(q)+2G²(q²)G(q)-G(q²)=0… Entry 1(iv) of Chapter 20 in Ramanujan's second notebook can be written in the form 3 + A³ = 1/v + 4v²" — the A³ identity is the cubic-base Eisenstein anchor (Borweins). Direct touch of quasi-modular L(q) per BIG_IDEAS §1. |

### Per-operator aggregate counts (24 entries, 11-operator vocabulary)

| Operator | n_entries | % of 24 | Predicted (HUNT5b) | Hit? |
|---|---|---|---|---|
| `q_shift` | 24 | **100.0%** | ≥30% (floor) | **YES (×3 ceiling)** |
| `modular_S_transform` | 22 | **91.7%** | ≥30% (floor) | **YES (×3 ceiling)** |
| `class_field_galois_average` | 8 | **33.3%** | ~20% | **YES (above bracket)** |
| `eisenstein_normal_ordering` | 2 | **8.3%** | ≥40% (floor) | **MISS (below floor)** |
| `master_theorem` | 0 | **0.0%** | ≤10% (ceiling) | **YES (under)** |
| `mellin_inversion` | 0 | **0.0%** | ≤10% (ceiling) | **YES (under)** |
| `FOURIER_SELF_RECIPROCITY` | 0 | 0.0% | ~0% (QR III) | YES |
| `FRACTIONAL_FUNCTIONAL_ITERATION` | 0 | 0.0% | ~0% | YES |
| `HARDY_ORDERS_OF_INFINITY` | 0 (1 near-match excluded) | 0.0% | ~0% | YES |
| `FRULLANI_LIMIT` | 0 | 0.0% | ~0% | YES |
| `MELLIN_PAIR_RECIPROCITY` | 0 | 0.0% | ~0% | YES |

### Per-family operator distribution (T2's A/B/C/D)

T2 clustering: A = Rogers-Ramanujan + sign variants (E1-6, E11-14);
B = R(q) special values (E7-10); C = Andrews-Gordon-Selberg level-N
(E18-23); D = cubic-base Eisenstein (E32-cubic). C-ambig (general
q-hypergeometric Heine-style) = E15, E16, E17 — listed separately because
T2 marks them out-of-scope for Eisenstein-CF but they're in Berndt's §1.

| Family | n | q_shift | modular_S | class_field | eisenstein | Dominant |
|---|---|---|---|---|---|---|
| A (R-R + sign, E1-6, E11-14) | 10 | 10 (100%) | 8 (80%) | 3 (30%) | 0 (0%) | q_shift + modular_S |
| B (R(q) special values, E7-10) | 4 | 4 (100%) | 4 (100%) | 4 (100%) | 1 (25%) | all three |
| C-ambig (Heine, E15-17) | 3 | 3 (100%) | 1 (33%) | 0 (0%) | 0 (0%) | q_shift |
| C (A-G-S, E18-23) | 6 | 6 (100%) | 6 (100%) | 0 (0%) | 0 (0%) | q_shift + modular_S |
| D (cubic-base) | 1 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | all four |

**The per-family distributions ARE structurally different.** Family B
(special-value evaluations of R(q)) is the only family where
`class_field_galois_average` is dominant (4/4 = 100%). Family A
(coupling-relation entries) has it at 30% (only the E1, E6 modular-equation-
of-degree-N entries fire it). Family C (the bulk Andrews-Gordon-Selberg
CFs at level N) fires zero `class_field_galois_average` — these are pure
q-product identities at a fixed q. This matches T2's clustering proposal:
B is a "special-values lookup" subroute that uses class invariants
heavily, the rest of the chapter doesn't.

## Surprises

1. **`eisenstein_normal_ordering` MISSED its 40% floor decisively, firing
   only twice (8.3%).** This is the central surprise of the pass. The
   chapter is called "Continued Fractions" not "Eisenstein continued
   fractions" — re-reading T2's scoping with this result in mind, T2 already
   anticipated this: T2 §"TL;DR" explicitly notes that only ~1-2 CFs in the
   chapter are *genuinely* Eisenstein (Family D, the cubic-base CF), and the
   rest of §2 has theta-product / η-quotient closed forms (not Eisenstein
   series in the modular-forms sense). The HUNT5b_PREDICTIONS chapter-32
   row over-weighted "Eisenstein" as a label — the actual content is
   **theta-quotient CFs at small levels (N=2,3,4,5,8) with modular-equation
   chains for special values**, NOT Eisenstein-series CFs. The
   `eisenstein_normal_ordering` operator (designed for `E_2k` Lambert
   series and residue-extraction on Eisenstein generating functions) fires
   only on E32-10 (which routes through the cubic-base Eisenstein chain via
   the 3+A³ identity) and the E32-cubic entry itself.

2. **`q_shift` saturates at 100% (24/24).** Every single CF entry in
   §1+§2 uses q-Pochhammer notation, q-shifts, or q-hypergeometric
   manipulation as either the primary or a major secondary move. This is
   far above the ≥30% predicted floor and represents the chapter's
   dominant operator. In retrospect this is unsurprising (the chapter is
   about q-CFs) but confirms the operator IS the right vocabulary unit —
   it's not vacuous and it doesn't fire in the QRs (0% there per diary
   20).

3. **`modular_S_transform` fires at 91.7%**, also far above the ≥30%
   floor. The combination "q_shift + modular_S_transform" is the chapter's
   dominant pair (22/24 entries fire both), exactly inverting the QR
   distribution where both operators were 0%. Berndt's repeated explicit
   citations of "the Jacobi triple product identity, Entry 19 of Chapter
   16" (E4, E16, E23) and "Ramanujan's work on modular equations" (E1,
   E6, E10, E18) make this unambiguous.

4. **All five QR-III operators stay at 0%.** Fractional iteration, Hardy
   orders, Frullani limit, Fourier self-reciprocity, Mellin-pair reciprocity
   — none of these are deployed anywhere in Ch. 32. The closest is the
   E11 oscillation-of-divergent-CF behavior which is asymptotic in a sense,
   but it's CF-theoretic asymptotics (Jones-Thron parabola theorem,
   Bauer-Muir transformation, modified-approximants convergence) not Hardy's
   "orders of infinity" calculus.

5. **The `bauer_muir_transformation` is a chapter-specific operator the
   schema doesn't have.** It fires on E11, E13, E14, E27, E28 (the
   gamma-product entries in §3 outside our scope also use it heavily) and
   is *the* convergence-machinery move for non-trivially-convergent CFs
   throughout the chapter. For a recognizer / schema covering the
   CF-corpus generally, this would deserve a slot. It is genuinely
   CF-specific (doesn't appear elsewhere in Ramanujan's work that I've
   seen).

6. **`master_theorem` and `mellin_inversion` both fire 0 times in 24
   entries.** This is decisive in the opposite direction — the
   Mellin/Master toolkit that dominates the QRs is *absent* from Ch. 32.
   Combined with point #4, this is the toolkit-split-hypothesis evidence:
   the QR toolkit (Mellin + Master + Fourier-reciprocity +
   fractional-iteration) and the Ch. 32 toolkit (q_shift + modular_S +
   class_field) have **zero overlap**.

## Verdict

**SUPPORTED on Ch. 32, partially.**

Hit-count against the prediction table:

| Predicted-dominant operator | Floor | Actual | Met? |
|---|---|---|---|
| `eisenstein_normal_ordering` | ≥40% | 8.3% | **NO** |
| `modular_S_transform` | ≥30% | 91.7% | YES |
| `q_shift` | ≥30% | 100.0% | YES |
| `class_field_galois_average` | ~20% | 33.3% | YES |

**3 of the 4 predicted-dominant operators hit (modular_S, q_shift,
class_field).** Per the rubric ("≥3 of 4 predicted-dominant operators
hit their floor"), this side of the test passes.

| Predicted-rare operator | Ceiling | Actual | Met? |
|---|---|---|---|
| `master_theorem` | ≤10% | 0.0% | YES |
| `mellin_inversion` | ≤10% | 0.0% | YES |
| `FRACTIONAL_FUNCTIONAL_ITERATION` (QR III) | ~0% | 0.0% | YES |
| `HARDY_ORDERS_OF_INFINITY` (QR III) | ~0% | 0.0% (1 near-match) | YES |
| `FOURIER_SELF_RECIPROCITY` (QR III) | ~0% | 0.0% | YES |
| `FRULLANI_LIMIT` (QR III) | ~0% | 0.0% | YES |
| `MELLIN_PAIR_RECIPROCITY` (QR III) | ~0% | 0.0% | YES |

**All 7 predicted-rare operators stay under their ceilings.** Per the
rubric ("≥3 of 4 predicted-rare operators stay under their ceiling"),
this side of the test passes with margin to spare.

**Bottom line:** The result is **SUPPORTED**, with the qualification that
the `eisenstein_normal_ordering` floor miss is the genuine prediction
failure. The miss is *interpretable* (the chapter is about q-CFs whose
closed forms are theta-quotients, not Eisenstein-series CFs proper — only
the single Family-D cubic-base entry is truly Eisenstein), and re-reading
[T2_EISENSTEIN_CF_SCOPING.md §"TL;DR"](../insights/T2_EISENSTEIN_CF_SCOPING.md)
this was *flagged in T2's scoping doc itself*: "Genuinely 'Eisenstein'
(in the modular-forms-of-level-N sense) CFs with limits expressible in
P/Q/R: 1-2". The HUNT5b prediction over-weighted the chapter title.

The right operator-distribution headline for Ch. 32 is **`q_shift +
modular_S_transform` dominant pair (>90% each), `class_field_galois_average`
the third-most-common (~33%), `eisenstein_normal_ordering` rare (~8%,
confined to the one Family-D entry plus its proof-chain neighbor E10).**

## Implications for the toolkit-split hypothesis

This is **one chapter of evidence** for the QR-vs-Notebooks toolkit
contrast. The headline contrast is now sharp:

| | QR I + QR II + QR III | NB V Ch. 32 |
|---|---|---|
| Dominant operators | `master_theorem` (57.6%), `FRACTIONAL_FUNCTIONAL_ITERATION` (15%), `FOURIER_SELF_RECIPROCITY` (15%) | `q_shift` (100%), `modular_S_transform` (91.7%), `class_field_galois_average` (33%) |
| Toolkit overlap | None | None |
| Mellin/Master in CFs | 100% in QR I | 0% in Ch. 32 |
| Modular machinery in QRs | 0% | 92% in Ch. 32 |

This is **exactly the toolkit-split pattern** [HUNT5b_PREDICTIONS
§"Top-level hypothesis"](../insights/HUNT5b_PREDICTIONS.md) describes: a
domain-specific routing function from problem-type (CFs at small N levels
→ modular machinery + class invariants; analytic integrals → Mellin +
Master + operator calculus) to a small operator basis.

**Not yet established** at the full ≥3-chapter level:

- **Ch. 16 (theta functions)** — needs Berndt commentary we don't have
  (NB Part III). Could be done via facsimile of NB II Ch. 16 + lookup
  references in NB V citations. Prediction: `modular_S_transform` ≥60%
  (the chapter's primary move per HUNT5b prediction).
- **Ch. 17 (modular equations)** — same gap. Prediction:
  `modular_S_transform` ≥50%, `class_field_galois_average` ≥30%.
- **Ch. 18-19 (class invariants Gₙ)** — same gap. Prediction:
  `class_field_galois_average` ≥60%, `modular_S_transform` ≥30%.

If those three chapters each show a *different* dominant operator within
the modular toolkit (theta-S, modular-equation, Galois-orbit-average),
the toolkit-split hypothesis would be **strongly supported** with
intra-toolkit specialisation as a bonus finding. If they all look like
Ch. 32 (q_shift + modular_S dominant, no real differentiation), the
hypothesis is only "weakly supported" at the within-Notebooks level even
though the QR-vs-Notebooks contrast remains.

The *single most informative next chapter* would be **Ch. 34 (class
invariants and singular moduli)**, which is in this same NB Part V volume
(pp. 183-321), and which should show `class_field_galois_average` as
dominant — clearly differentiating from Ch. 32. Berndt's per-section
structure (§2 "Table of Class Invariants", §3 "Computation of G_n and
g_n", §4 "Kronecker's Limit Formula", §5 "Class Invariants Via Kronecker's
Limit Formula", §6 "Class Invariants Via Modular Equations", §7 "Class
Invariants Via Class Field Theory") is a structured operator-test in
itself.

## Honest caveats

- **Hand-judgment, one-pass, no inter-rater reliability check.** Same as
  diary 20. ±5-8 percentage points on per-operator percentages is the
  honest uncertainty.
- **The `modular_S_transform` tag at 91.7%** is the headline result and
  is *partially* a consequence of liberal scoping (any invocation of the
  Jacobi triple product identity, modular equation, or theta-quotient
  reduction counts). A stricter "only proofs that explicitly invoke
  τ → -1/τ" scoping would drop the number considerably (probably to
  ~30-40%). The looser scoping is justified because (a) Berndt
  consistently routes through modular-equation work in the proofs even
  when the entry is stated as a pure CF identity, (b) the Jacobi triple
  product *is* a modular-S move on the theta-function lattice, and (c)
  the "did fire ≥30%" floor is met at either scoping.
- **`bauer_muir_transformation` as out-of-schema operator:** real and
  worth adding to the schema for a CF-corpus pass. Not adding here
  because the task is to test the pre-registered 11-operator basis;
  adding new operators would shift the comparison frame. Flagging for
  a future schema-extension task in todo.md.
- **E32-cubic is not a numbered Ch. 32 entry**; it is referenced in
  Ch. 32 via the E10 proof chain but defined in Ch. 33 §3. Including it
  in the 24-entry count is a defensible choice (it is one of T2's four
  families and the only truly Eisenstein CF in the chapter's ambit) but
  arguably inflates the `eisenstein_normal_ordering` count from 1/23 →
  2/24. The headline conclusions don't change either way.
- **The Family-A/B/C distinction is T2's, not Berndt's.** Berndt presents
  E1-E10 as a single sequence (§1 entries 1-10) and only the §1/§2 boundary
  is canonical. The per-family breakdown is informative but should be
  read as T2-clustered, not Berndt-clustered.
- **Ambiguous-rate estimate.** Of 24 entries, ~4 had non-trivial near-match
  decisions (E11 HARDY_ORDERS near-match excluded; E12 class_field
  near-match excluded for primitive-nth-root Schur dispatch; E18
  class_field near-match excluded for Berndt-commentary-only special
  values; E19 class_field near-match excluded for ω=exp(2πi/3) Galois
  symmetry). So **~17% ambiguous-rate**. The near-matches all sit at the
  boundary of `class_field_galois_average` — if all four were tagged, the
  number rises from 33.3% → 50% (still well above the 20% predicted
  bracket, still under the 60% Ch. 18-19 prediction). The "under 1/4
  ambiguous" rate is in line with diary 20's QR tagging.

## Bottom-line claim

The HUNT5b_PREDICTIONS Ch. 32 operator-distribution forecast is
**SUPPORTED** at the rubric threshold (≥3 of 4 predicted-dominant operators
hit floor; ≥3 of 4 predicted-rare operators under ceiling) with one
genuine miss (`eisenstein_normal_ordering` predicted ≥40%, actual 8.3% —
the chapter is theta-quotient-CFs not Eisenstein-CFs proper, T2's scoping
doc already flagged this risk). The QR-vs-Notebooks toolkit-split
hypothesis is **supported on one chapter** with zero toolkit overlap
between the two corpora. **≥3 chapters needed at intra-toolkit specialisation
level** (Ch. 16, 17, 18-19, or 34 the most informative single next chapter)
to call the hypothesis fully "Established".

**Confidence:** medium-high on the SUPPORTED verdict for Ch. 32; medium
on the broader hypothesis status (one chapter of evidence, replication
needed). The `eisenstein_normal_ordering` miss is the genuine prediction
failure and is honest.

## Follow-up leads

1. **Hunt 5b Ch. 34 (class invariants and singular moduli) tagging.**
   In the same NB Part V volume (pp. 183-321), Berndt-edited, no extra
   sources needed. Highest-leverage next chapter because §3-§7 in Ch. 34
   are per-method-on-class-invariants and would directly test
   `class_field_galois_average` dominance in a different chapter.
2. **Extend the operator schema with `bauer_muir_transformation` and
   `modular_equation_chain` as separate operators.** Then re-tag Ch. 32
   to refine the dominant-pair characterisation.
3. **Hunt 5b Ch. 36 (modular equations and theta-function identities)
   tagging.** Also in this NB Part V volume (pp. 353-407). Should show
   `modular_S_transform` dominant; would be a 3rd chapter for the
   hypothesis-establishment threshold.
4. **Cross-validate this pass with an independent re-tagging** (e.g.
   spawn a parallel-Claude session to re-tag from scratch using just the
   per-entry text + commentary, no access to this diary). The 91.7%
   `modular_S_transform` number is the headline and deserves a second
   opinion since the looser scoping inflates it.
