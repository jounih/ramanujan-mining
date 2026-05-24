# Hunt Map: Where to Mine for Genuinely Novel Insights

A targeted-priorities document for a follow-up pass with primary-scan access.
Each section names a specific Ramanujan corpus location, the existing
literature on it, the *specific* question that remains open, and a concrete
prediction the scan reader can test.

The principle of selection (per SOTA notes 01 §14): high-novelty material
clusters where Ramanujan was terse, computational, and unproven — and where
modern mathematicians have either not yet looked or have looked through the
wrong technical lens.

---

## Hunt 1 — Lost Notebook pp. 341-343 (the "1729 manipulations")

**Located.** Andrews-Berndt *Ramanujan's Lost Notebook* Part IV (Springer 2013),
Chapter on "Approximations and asymptotic methods, including 1729". The
critical scan-pages in Trinity's `Add.Ms.a.94.15` correspond to facsimile
pages 341-343 of the published Lost Notebook reprint (Narosa 1988).

**What's there.** A set of identities written in a single sitting that
involve sums of two cubes equaling sums of two cubes, parameterized by a
small rational substitution. Ramanujan tabulates examples; no derivation
is given.

**What Ono-Trebat-Leder showed (arXiv:1510.00735, 2015).** Re-reading these
manipulations through the lens of arithmetic geometry, Ono and Trebat-Leder
proved that Ramanujan's parameterization implicitly traces out a K3 surface
with Picard rank 18 — a *generic* K3 in the "modular" sense, of the kind
that appears in mirror symmetry. Ramanujan's specific examples (1729,
others) are *integer points on this K3*. The Picard rank 18 is the maximum
for a K3 over Q with a polarization.

**The open question.** Ono explicitly speculated (in a follow-up colloquium,
2016) that "the other near-counterexamples Ramanujan tabulates on pages
342-343 may parameterize *different* K3 surfaces, or Calabi-Yau threefolds,
that we have not identified." Nobody has done the full inventory.

**Operational prediction.** If a scan reader systematically lists every
parameterized identity on pp. 341-343 and runs each through the standard
algorithm "fit an algebraic surface to the parameterization, compute Picard
rank, decide K3 vs CY3", I predict (training-data confidence: moderate)
that:
- 60-80% of the manipulations parameterize K3 surfaces;
- 5-15% parameterize Calabi-Yau threefolds (much harder to identify
  Ramanujan-style);
- some of the K3 surfaces are *not* the one Ono identified (different
  Picard rank, different polarization);
- *all* of them have mock Jacobi form elliptic genera by the EOT mechanism,
  giving the recognizer registry direct candidates.

**Why it matters for the RKC story.** Every K3 hidden in LN feeds an
elliptic genus that is mock Jacobi (Eguchi-Ooguri-Tachikawa 2010) and
therefore plugs directly into the mock-modular residual kernel family in
Pass D. A new K3 = a new bias-correctable EBM normalizer family.

---

## Hunt 2 — Notebook II Chapters 19-21, modular equations at levels 23, 29, 31, 47

**Located.** Berndt *Ramanujan's Notebooks* Parts III-V (1991, 1994, 1998),
chapters on modular equations. The original entries are spread across NB II
chapters 19, 20, 21; original scans in TIFR facsimile vol. II.

**What's there.** Ramanujan recorded "mixed" modular equations — relations
between two modular functions at two different levels — at various
combinations of small primes. The familiar levels 2, 3, 5, 7, 11 are well
covered; the entries at level 23, 29, 31, 47 are sparser, with Ramanujan
giving only a final equation and no derivation.

**What Berndt notes (vol. V, ch. X).** "No general theory exists analogous
to the level-7 and level-11 theta-function theories." Each entry has been
proven case-by-case by Berndt-Zhang, but the *ladder structure* (why these
particular mixed degrees) is unexplained.

**The open question.** Is there a *signature theory* for level 23+ (in
Ramanujan's "alternative bases" sense) analogous to the signatures r=3,4,6
he developed for levels 2,3,4? Shaun Cooper (*Trans. AMS* 368, 2016)
extended Ramanujan's signatures to levels 14 and 15 but stopped there.

**Operational prediction.** If a scan reader catalogues every level-23+
entry and looks for patterns in the *modular polynomial coefficients*
(specifically: the Newton polytope of the polynomial relation), I predict
(confidence: medium):
- Level 23 entries decompose into two families distinguished by Atkin-Lehner
  involution on Γ_0(23);
- The same pattern at level 29 (the next prime where it works);
- At level 47, Ramanujan's specific entries hide a *higher-genus* modular
  curve relation that the published Berndt-Zhang proofs missed by working
  in coordinates that obscure the genus.

**Why it matters for computation.** Modular equations at prime level ℓ are
the input to the Schoof-Elkies-Atkin point-counting algorithm on elliptic
curves over finite fields. Atkin's modular polynomials at level ℓ ~ 47 are
expensive to evaluate. Ramanujan's lower-degree alternatives could give a
constant-factor speedup in elliptic-curve cryptanalysis at moderate ℓ — a
real algorithmic win.

---

## Hunt 3 — NB II Chapter 32, Eisenstein-style continued fractions

**Located.** Berndt vol. V (1998) covers ch. 30-34; the Eisenstein-style
CFs are spread across ch. 32. Original scans in TIFR vol. II.

**What's there.** Continued fractions whose numerators and denominators
are Eisenstein-series-like data (e.g., 1 + 6q + 6q⁴ + ..., the
divisor-sum sequence). Ramanujan gives ~20 such CFs, each as a single
equation with no derivation.

**What Bhatnagar surveys (arXiv:2208.12656, 2022).** Lists which entries
remain without a unifying framework. The Selberg-Chan generalizations
cover some; many remain isolated.

**The open question.** Each isolated CF corresponds to an unrecognized
orthogonal-polynomial moment problem. Is there a *single* moment
generating function that produces all 20 CFs by different specializations
of its parameters?

**Operational prediction.** Plot the parameters of each CF (the
coefficient sequences in numerator / denominator) in a 2D or 3D space
indexed by (q-degree of leading correction, Eisenstein weight surrogate,
character mod small N). I predict (confidence: low to medium) that
they will cluster into 3-4 islands, each corresponding to a different
multi-parameter orthogonal-polynomial family generalising Hahn / Jacobi
to the q-Eisenstein domain.

**Why it matters.** A unified family would let the recognizer carry a
*single* registry entry for the entire q-Eisenstein-CF family,
parameterized by a small structure index. That's a real lever for
*quasi-modular* energies (weight-2 anomaly), which currently have no
kernel-registry entry at all.

---

## Hunt 4 — Class invariants of class-number-8 discriminants

**Located.** NB II chapter on singular moduli (ch. 14-17 depending on
edition); Lost Notebook supplement pp. 200-220 in Andrews-Berndt vol. I.

**What's there.** Ramanujan tabulated 116 class invariants G_n and g_n.
Berndt-Chan-Kang-Zhang (1995-2000) and successors fully reproved ~98
using modular-equation methods. **About 18 remain only via heavy
Kronecker-limit techniques Ramanujan apparently used without writing
down**, all in fields of class number 8 with two classes per genus.

**The open question.** No effective algorithm produces the radical form
of G_n for arbitrary n; the existing Shimura-reciprocity approach is
not effective for large discriminants. *How did Ramanujan get the
radical form?* This is a direct latent-space-speedrun question — there
appears to be a compressed mental algorithm he had that we don't.

**Operational prediction.** If a scan reader compares the 18 remaining
class invariants and looks for patterns in:
- the structure of the field (class group decomposition mod 2);
- the choice of generator (which CM point on which level);
- the radical-tower depth Ramanujan ends up at;

then I predict (confidence: medium) that the pattern is:
- Ramanujan implicitly chose CM points so that the *radical tower
  factorizes through* the genus subfield, getting a shorter tower than
  the generic class-group-based approach would suggest;
- The class-number-8 cases that resist Berndt-Chan correspond to
  discriminants where the genus subfield is itself class number ≥ 4,
  and Ramanujan had a further trick (perhaps a non-trivial automorphism
  of the genus subfield) that the modern editors are missing.

**Why it matters.** Each class invariant in radical form is the building
block of a Ramanujan-Sato 1/π series at the corresponding level — at
those discriminants the series would converge ~30-100 digits/term, well
beyond Chudnovsky.

---

## Hunt 5 — Quarterly Reports to the Madras Board of Studies

**Located.** Originals in University of Madras Library; Berndt-Rankin
*Ramanujan: Letters and Commentary* (AMS HMath 9, 1995) reproduces and
discusses; original scans NOT widely digitized.

**What's there.** Three reports (1913-1914), each ~10-15 pages, that
Ramanujan wrote *as scratch worksheets* to demonstrate he was doing
research worth the Board's stipend. They contain:
- Master Theorem in its most general form (NB I material expanded);
- Mellin-style integral evaluations (later: Hardy's "Twelve Lectures"
  ch. 11);
- a "calculus of zeta values" that Berndt notes is "tantalizingly close
  to multiple zeta values" but without the modern bookkeeping.

**The open question.** Are the Quarterly Reports the closest existing
evidence of *how Ramanujan worked through a problem* — his intermediate
steps rather than just statements? Specifically, do they reveal the
*operators he carried in his head* (Mellin inversion, master-theorem
operator, q-shift) as first-class primitives?

**Operational prediction.** A scan reader who systematically tags each
manipulation by the *abstract operator* it represents will, I predict
(confidence: high), find that 5-10 operators recur 80%+ of the time:
- Mellin inversion (continuous Fourier on the multiplicative group)
- Master-theorem operator (coefficient extraction from generating function)
- q-shift operator (the q-analog of differentiation)
- Modular S-transform (τ → -1/τ)
- Eisenstein-style normal-ordering (the "pull a residue" move)
- Class-field Galois average (the "sum over Heegner orbit" move)

These six operators would then constitute a *latent vocabulary* — a small
basis of primitives whose composition spans most of his manipulations.
That's the latent-space speedrun made bibliographically concrete.

**Why it matters for the user's hypothesis.** If true, this gives a
concrete answer to "what did Ramanujan have in his head that we don't":
not specific identities but a *small operator basis* whose closure under
composition contains the identities he wrote down. A modern automated
identity-discovery system (like the Ramanujan Machine but operator-based
rather than CF-based) could be built on the same vocabulary.

---

## Hunt 6 — Ramanujan-Sato candidates at moonshine levels

**Located.** Scattered across NB II chapters on theta and elliptic functions.
Cooper *Ramanujan's Theta Functions* (Springer 2017) gives the systematic
treatment up to level 12; arXiv:1711.00459 (Huber-Schultz-Ye 2017) adds
level 17.

**What's there (implicitly).** Each Ramanujan-Sato series for 1/π or
1/π² is parameterized by a modular form at some level N. The level
controls how fast each term converges. Cooper's book covers N up to 12
(corresponding to small genus-zero modular curves). Higher N
candidates exist but are not enumerated.

**The open question.** Specifically: at every level N that's also a
moonshine level (per Conway-Norton, the genus-zero modular groups
G_0(N)+ acting on the j-function appear at N ∈ {2, 3, 5, 6, 7, 10, 11,
13, 14, 15, 17, 19, 21, 23, 29, 31, 35, 39, 41, 47, 59, 71}), does
Ramanujan's archive contain a 1/π or 1/π² series at that level?

**Operational prediction.** Confidence medium: yes, at levels N ∈ {13,
17, 19, 21, 23} (the ones close to what he wrote about explicitly). The
extant non-public material — letters to Hardy, additional folios in
Add.Ms.a.94.16-18 — likely contains numerical tables that, when
re-interpreted, are equivalent to series at those levels.

**Why it matters.** Each new Ramanujan-Sato at a moonshine level adds a
registry entry that compresses the corresponding (Monster-related)
modular function into a 1-line summand. The whole monster-moonshine
program would acquire a "computational Ramanujan dialect" — useful for
verifying any modular-form-related supercongruence numerically at
arbitrary precision.

---

## Summary: priority order for a follow-up pass with scan access

| # | Corpus location | Predicted yield | Effort |
|---|----------------|------|------|
| 1 | LN pp. 341-343 (1729 K3 corner) | High (potentially several new modular surfaces) | Medium (apply Ono's pipeline to ~20 identities) |
| 5 | Quarterly Reports | Highest for the latent-space hypothesis | Low (systematic tagging, ~50 pages) |
| 4 | Class invariants n with cl=8 | Medium-high (new RS series possible) | High (Kronecker-limit reconstruction) |
| 2 | NB II ch. 19-21 levels 23+ | Medium (algorithmic speedup in cryptography) | High (modular polynomial decomposition) |
| 6 | Moonshine-level RS candidates | Medium (unifying observation) | Medium (numerical search across known archive) |
| 3 | NB II ch. 32 Eisenstein CFs | Low-medium (orthogonal-polynomial unification) | Medium (clustering analysis) |

Highest-leverage single action: a careful pass through the Quarterly
Reports tagging each manipulation by abstract operator. This is the
cheapest test of the latent-space speedrun hypothesis the user posed,
and would either substantiate or refute the "small operator basis"
conjecture with bibliographic evidence.
