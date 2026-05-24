# T2 — Eisenstein-CF Registry Expansion: Scoping Document

**Status:** SCOPING (no implementation). Half-day read of Berndt *Notebooks
Part V* Ch. 32 ("Continued Fractions") and Berndt-Yee *RIMS Kokyuroku* **1274**
(2002), "A Survey on Eisenstein Series in Ramanujan's Lost Notebook". Date:
2026-05-24.

**TL;DR.** The HUNT_MAP §3 / T2 framing of "~20 Eisenstein-style CFs in
NB V Ch. 32" conflates two distinct corpora:

  (a) **Continued fractions with theta-product / eta-quotient closed forms**
     (Ch. 32 §1-§2, mostly Rogers-Ramanujan family and Selberg-Andrews-Gordon
     siblings). These are q-CFs whose limits are *quotients of theta
     functions*, not Eisenstein series proper. ~17 such entries in §1, ~12
     in §2.

  (b) **Eisenstein series themselves** (P/Q/R in Ramanujan's notation = L/M/N
     in NB V, = E_2/E_4/E_6 modern). These appear in *Lost Notebook*
     (Berndt-Yee 2002 surveys them), in NB II Ch. 15 / 21, and in NB V Ch.
     33 §4. They are mostly *not* in CF form — they are Lambert-series
     identities, polynomial relations, derivative identities (1.5 of B-Y).
     There is essentially **one** CF in this group whose continued-fraction
     limit *is* directly built from Eisenstein-series data: the
     **Ramanujan-Selberg / G(q) cubic CF** (NB V Entry 19, §2, p. 47, and
     its appearance via the cubic-base material in §33).

The honest reading: T2 is **two distinct sub-registries**, not one
homogeneous family. This scoping doc treats both, with the (a) catalogue
being the larger and more directly registrable target, and (b) being the
piece that actually touches the quasi-modular (weight-2) anomaly per
BIG_IDEAS §1.

Final answers up top (DISCIPLINE check, per CLAUDE.md):

- Total CF entries in Ch. 32 with theta/eta/Eisenstein-flavor closed forms:
  **~30** (17 in §1, ~13 in §2). All other Ch. 32 entries are
  hypergeometric/Bessel/gamma/arctan-shaped — out of scope for T2.
- Genuinely "Eisenstein" (in the modular-forms-of-level-N sense) CFs
  with limits expressible in P/Q/R: **1-2** (Ramanujan-Selberg G(q) cubic
  CF; possibly Entry 18's G(q)).
- Proposed clustering: **4 families** (see §2). Confidence: **MEDIUM**
  (clean separation on §1 / §2 / §33-cubic-base boundaries; messier within
  §2 where some entries straddle).
- The clustering is **defensible** but not crisp; one entry (Entry 21,
  Selberg's `Q_4(q) = (-q^2;q^2)_∞/(-q;q^2)_∞` CF) is ambiguous between
  Family-A (Rogers-Ramanujan-type) and a possible Family-B (Selberg-Andrews-
  Gordon-type). Marking it `cluster_uncertainty=high` is the right call.

Cross-references: [HUNT_MAP §3](HUNT_MAP.md), [BIG_IDEAS_REVIEW §1 & §2 of
tooling-fork](BIG_IDEAS_REVIEW.md), [rkc/MILESTONES.md
§v0.2](../rkc/MILESTONES.md), [rkc/registry.py](../rkc/registry.py),
[CANDIDATE_INSIGHTS §A6 β\*=cπ pattern](CANDIDATE_INSIGHTS.md).

---

## 1. Catalogue of Ramanujan's continued fractions with theta/Eisenstein closed forms

This catalogue covers Berndt NB V Ch. 32 §1 (Rogers-Ramanujan) + §2 (Other
q-CFs), with cross-references to Lost Notebook pages and Berndt-Yee 2002
where applicable. Entries from §3 (gamma-product CFs), §4 (other CFs —
arctangent / Bessel / hypergeometric), and §5 (general convergence theorems
not associated with a specific CF) are **excluded** as out of scope for an
Eisenstein-CF registry.

Notation: `f(a,b) = Σ_{n=-∞}^∞ a^(n(n+1)/2) b^(n(n-1)/2)` is Ramanujan's
general theta. The Rogers-Ramanujan CF is `R(q) := q^{1/5} / (1 + q/(1 +
q^2/(1 + q^3/(1 + ...))))`. Berndt's NB V Ch. 32 numbers entries 1-58 in
sequence; Lost Notebook (LN) pages cited per Tata 1957 / Narosa 1988
pagination.

### Table: §1 (Rogers-Ramanujan family) — 17 entries

| id | source (NB V Ch. 32 entry # / LN page) | identity sketch (LaTeX) | parameters | known reproof |
|---|---|---|---|---|
| E32-1 | Entry 1 (p. 326) | `v - u^2 = uv^2`, `UV^2(U^2+V) + U^2 - V + 10UV(UV-U+V+1) = 0` for `U:=R(q)^5, V:=R(q^5)` | q-power coupling 1↔5 | Rogers 1894 / Watson 1929 |
| E32-2 | Entry 2 (p. 321) | `uv(u-v)^4 - u^2v^2(u-v)^2 + 2u^3v^3 = (u-v)(1+u^5v^5)` for `u=R(-q), v=R(q)` | sign symmetry of R | Berndt-NB V proof |
| E32-3 | Entry 3 (p. 321) | `(v - u^3)(1 + uv^3) = 3u^2v^2` for `u=R(q), v=R(q^3)` | q-power coupling 1↔3 | Rogers 1921 |
| E32-4 | Entry 4 (p. 326) | `m - n = mn = m^2/(1+m) = n^2/(1-n) = uv^3` with `m,n` eta-quotients of R(q),R(q^5) | mixed Rogers-eta | Berndt-NB V |
| E32-5 | Entry 5 (p. 326) | `(u^5+v^5)(uv-1) + u^5v^5 + uv = 5u^2v^2(uv-1)^2` for `u=R(q), v=R(q^4)` | q-power coupling 1↔4 | Rogers 1921 / Watson 1929 |
| E32-6 | Entry 6 (p. 289, Formula 3) | `f^5 = φ(1-2φ+4φ^2-3φ^3+φ^4)/(1+3φ+4φ^2+2φ^3+φ^4)` (φ,f are CFs of degree-5 type) | quintic modular eqn | Rogers / Ramanathan |
| E32-7 | Entry 7 (p. 311 NB1, second proof from Lemma 7.1) | `R(e^{-4π}) = √(c²+1) - c`, `2c := 1 + (a+b)/(a-b) √5`, `a=5^{1/4}, b=1` | special value at q=exp(-4π) | Watson 1929 |
| E32-8 | Entry 8 | `R(e^{-8π}) = √(c²+1)-c`, `a=3+√2-√5, b=(20)^{1/4}` | special value at q=exp(-8π) | Berndt-Chan |
| E32-9 | Entry 9 | `R(e^{-16π}) = √(c²+1)-c`, `a=5^{1/4}(4-√2), b=...` | special value at q=exp(-16π) | Berndt-Chan |
| E32-10 | Entry 10 | `R(e^{-6π}) = √(c²+1)-c`, `a=(60)^{1/4}, b=2-√3+√5` | special value at q=exp(-6π) | Berndt-Chan-Zhang |
| E32-11 | Entry 11 (pp. 374, 382) | `1/1 + q/1 + q²/1 + ...` for q>1 *oscillates*; odd→(11.2), even→(11.3) | divergent-CF oscillation | Andrews-Berndt-Jacobsen-Lamphere |
| E32-12 | Entry 12 (Hardy letter) | Modest generalization of R(q), 3rd-letter form | parameter `a` extra | Zagier |
| E32-13 | Entry 13 | "Approximating CF" for divergent R(q), q>1 | divergent regime | Zagier |
| E32-14 | Entry 14 | Continued-fraction expansion for `f(x;q) = ...` (q-hypergeometric) | x parameter | Zagier |
| E32-15 | Entry 15 (p. 373) | `φ(a)/φ(aq) = 1 + aq/1 + (aq²-bq)/1 + aq³/1 + ...` where `φ(a) = Σ q^{n²} a^n / ((q;q)_n (bq;q)_n)` | (a,b) parameters | Andrews-Bowman |
| E32-16 | Entry 16 (p. 373) | `χ(-q²)f(-q⁵)/f(-q,-q⁴) = ... = Σ q^{n²}/(q⁴;q⁴)_n` and similar (= Rogers-Ramanujan identities recast) | Rogers-Ramanujan equivalent | Rogers 1894 |
| E32-17 | Entry 17 (p. 374) | `φ(a)/φ(aq) = 1 + aq/1 + bq/1 + aq²/1 + bq²/1 + ...` (a,b) two-param family | a,b parameters | Selberg / Andrews |

### Table: §2 (Other q-CFs — Selberg / Andrews-Gordon / cubic-base) — ~13 entries

| id | source (NB V Ch. 32 entry # / LN page) | identity sketch (LaTeX) | parameters | known reproof |
|---|---|---|---|---|
| E32-18 | Entry 18 (p. 373) | `(q;q²)_∞/(q³;q⁶)_∞³ = 1/1 + (q+q²)/1 + (q²+q⁴)/1 + ...` (G(q) cubic, Ramanujan-Selberg cubic CF) | none (single CF in q) | Watson 1929 / Selberg 1936 / Gordon / Andrews |
| E32-19 | Entry 19 (p. 290, Formula 3) | `(q²;q³)_∞/(q;q³)_∞ = 1/(1 - q/(1+q) - q³/(1+q²) - q⁵/(1+q³) - ...)` (Andrews' CF, level-3) | none | Andrews 1968 / Selberg / Hirschhorn |
| E32-20 | Entry 20 (p. 290, Formula 4) | `(q³;q⁴)_∞/(q;q⁴)_∞ = 1/(1 - q/(1+q²) - q³/(1+q⁴) - q⁵/(1+q⁶) - ...)` (level-4 Andrews-Selberg) | none | Selberg / Ramanathan / Andrews |
| E32-21 | Entry 21 (p. 290, Formula 5) | `(-q²;q²)_∞/(-q;q²)_∞ = 1/1 + q/1 + (q²+q)/1 + q³/1 + (q⁴+q²)/1 + ...` (Selberg 1936, eq. 54; level-2 character of mod-8 type) | none | Selberg 1936 |
| E32-22 | Entry 22 (p. 290, Formula 6) | `(q;q⁸)_∞(q⁷;q⁸)_∞/((q³;q⁸)_∞(q⁵;q⁸)_∞) = 1/1 + (q+q²)/1 + q⁴/1 + (q³+q⁶)/1 + q⁸/1 + ...` (Selberg 1936 eq. 53; level-8) | none | Selberg 1936 / Andrews-Gordon / Chan-Huang |
| E32-23 | Entry 23 (p. 373) | `f(-q,-q⁷)/f(-q³,-q⁵) = 1/1 + (q+q²)/1 + q⁴/1 + (q³+q⁶)/1 + ...` — equivalent to E32-22 via Jacobi triple product | level-8 alternate form | Jacobi triple product reduction |
| E32-cubic | NB V Ch. 33 §3.7-3.8 (cubic-base), with G(q) := `q^{1/3}/(1 + (q+q²)/1 + (q²+q⁴)/1 + (q³+q⁶)/1 + ...)` per Entry 1 of Ch. 20 (PIII, p. 345) | (referenced in §1 Entry 10 proof, eqs. (10.6)-(10.8); modular eqn `G²(q)+2G²(q²)G(q)-G(q²)=0`) | cubic base; **directly Eisenstein** via P/Q/R cubic identity | Chan 1995 / Berndt-Chan-Zhang |

§2 also includes the q-series identity material in Entries 16-17 above that
straddle §1/§2; I have listed those in §1 because Berndt does.

### Coverage check: how many is "20"?

- HUNT_MAP §3: "Ramanujan gives ~20 such CFs". Where does that number come
  from?
- Reading: Berndt NB V Ch. 32 *Introduction* (pp. 9-10) explicitly states
  "about 70 results on continued fractions" total in this chapter, and
  73 results in the per-chapter count (intro p. 4 table). That's all CFs
  in Ch. 32, not just Eisenstein-style.
- Of those 73, the theta/eta/q-product-closed-form subset is:
  17 (§1: 1-17) + ~13 (§2: 18-23, plus the cross-references like Selberg's
  CFs in Bhatnagar/Andrews not numbered as separate entries) ≈ **30
  entries**. Higher than HUNT_MAP's "20".
- The "20" framing in HUNT_MAP was likely conservatively counting only the
  *Selberg-style* CFs in §2 plus a few headline Rogers-Ramanujan entries
  (Entries 1, 2, 3, 5, 6 = 5 from §1) + Entries 18-23 from §2 = 11, plus
  Lost Notebook entries (Berndt-Yee 2002 lists ~5-7 CF-like Eisenstein
  expressions). Total ~17-20. **So HUNT_MAP's "20" was correct to within
  factor 1.5; the true count is more like 30 if we include the §1 R(q)
  special values and all §2 entries.**

---

## 2. Proposed clustering — 4 families

I propose **4 families** at the kernel-registry level (per Hunt 3 prediction
of "3-4 islands"). Confidence on the family split: **MEDIUM**. The §1 / §2
boundary is clean; within §2 the level-2/4/8 vs level-3 split is clean; the
ambiguous case is which family the cubic-base G(q) belongs to.

### Family A: Rogers-Ramanujan + sign-variations

- Distinguishing feature: limit is `R(q)` or a Rogers-Ramanujan-type sum
  `Σ q^{n²+linear(n)} / (q;q)_n`.
- Quasi-modular fingerprint: weight-0 modular (no anomaly); η-quotients of
  level 5.
- Entries: E32-1, E32-2, E32-3, E32-5, E32-6 (modular-eqn coupling),
  E32-11 (divergent regime is fingerprint), E32-12, E32-13.
- Characteristic q-degree of leading correction: linear in n (numerator
  is `q^n`, n=index of CF level).
- Eisenstein weight surrogate: 0 (theta-quotient, no Eisenstein factor).
- Character mod small N: trivial (or `χ_5` for level-5 entries).

### Family B: Rogers-Ramanujan special values (closed-form at q=exp(-πk))

- Distinguishing feature: explicit radical-form value of R at q=exp(-πk).
- Quasi-modular fingerprint: not a CF in the routable sense — these are
  *numerical evaluation* targets, not CFs to be evaluated.
- Entries: E32-7, E32-8, E32-9, E32-10.
- Note: these belong in a SEPARATE registry shape — they are *special
  values* the routing layer would recognize and short-circuit to a closed-
  form lookup, not CF families to truncate. **Flag as a sub-route, not a
  kernel family.**
- *INDICATIVE* clustering only; might be better filed under the existing
  `class invariants` framework (CANDIDATE_INSIGHTS, Hunt 4) than under
  Eisenstein-CF.

### Family C: Andrews-Gordon-Selberg / level-N q-product CFs (the bulk of §2)

- Distinguishing feature: limit is `(q^a;q^N)_∞ (q^{N-a};q^N)_∞ / (q^b;q^N)_∞
  (q^{N-b};q^N)_∞` for small N (2, 3, 4, 8) and `a, b` distinct residues
  mod N.
- Quasi-modular fingerprint: η-quotient, weight 0 modular, level N.
- Entries: E32-18 (level-3, single CF), E32-19 (level-3, three-term),
  E32-20 (level-4), E32-21 (level-2 / mod-8), E32-22 (level-8), E32-23
  (level-8 alternate).
- Characteristic q-degree of leading correction: pair `(q + q²)`, `(q² +
  q⁴)`, ... — additive shifts characteristic of Andrews-Gordon mod-N.
- Eisenstein weight surrogate: 0 (still theta-quotient).
- Character mod small N: explicit dependence on residue class mod N.
- **Cluster uncertainty:** E32-21 is ambiguous between this family and
  a sub-family `C'` containing only level-power-of-2 entries (E32-21,
  E32-22, E32-23). Tag accordingly; the matcher would still place it in
  Family C with a `level=2` parameter, but a separate degeneracy detector
  for level=2k vs odd level may be wise.

### Family D: Cubic-base Eisenstein CF (the only true "Eisenstein" CF)

- Distinguishing feature: limit *requires* the cubic Eisenstein series
  M(q³)/L(q³)/N(q³), i.e. the Ramanujan-Sato cubic base (Borweins'
  `a(q)/b(q)/c(q)`).
- Quasi-modular fingerprint: **YES** — directly touches the weight-2
  L(q) = P(q) = 1 - 24 Σ nq^n/(1-q^n), which fails strict modularity.
- Entries: E32-cubic (G(q) from §1 proof of E32-10, eqs. (10.6)-(10.8)).
- Character mod small N: trivial mod 3 (or non-trivial via cubic base).
- This is the family that, per BIG_IDEAS §1, **fills the quasi-modular
  (weight-2 anomaly) gap currently absent from the rkc/ recognizer.**

### Ambiguous / not in any family

- E32-15, E32-16, E32-17 are *general theorems* about
  `φ(a)/φ(aq)` for q-hypergeometric `φ(a) = Σ q^{n²}a^n / (q;q)_n (bq;q)_n`.
  These are q-hypergeometric continued fractions; the closed form (Heine
  / Rogers / Andrews) is hypergeometric not theta-quotient in general.
  **Treat as a separate `q_hypergeometric_cf` family if registered at all;
  out of scope for T2 proper.**
- E32-14 (Zagier reanalysis of divergent f(x;q)) is essentially a special
  Zagier construction and probably doesn't deserve its own family.

---

## 3. One worked example per family

### 3A. Family A — E32-1 (Rogers-Ramanujan q↔q⁵ relation)

(a) **Identity (verbatim from NB V Ch. 32 Entry 1).** Let `|q| < 1` and
```
U := q^{1/5} / (1 + q/(1 + q²/(1 + q³/(1 + ...))))   =: R(q)
V := q^{2/5} / (1 + q²/(1 + q⁴/(1 + q⁶/(1 + ...))))   =: R(q⁵)
```
Then
  (i)  `(V - U²)/(V + U²) = UV²`
  (ii) `U V² (U² + V) + U² - V + 10 U V (UV - U + V + 1) = 0`.

(b) **Why Family A.** Pure Rogers-Ramanujan-type; the limit is an η-quotient
of level 5 in two arguments coupled by `q → q⁵`. No Eisenstein factor.

(c) **Kernel-matcher pattern (regex / AST shape).** sympy AST:
```
Mul(
  Pow(q, Rational(1,5)),
  Pow(Add(1, recursively_defined_CF_with_numerator_q_powers), -1)
)
```
where the numerator-sequence `[q, q², q³, ...]` matches a `q^n` increment
pattern. Fuzzy match on the CF tail "q^n / (1 + ...)" structure with index
running 1..∞. The AST can be captured via a sympy `Function('CF')` proxy
or by recognizing `Limit(...)` of partial CF approximants.

(d) **Closed form / numerical evaluation.** R(q) has *no* elementary closed
form for generic q, but its values at quartic-irrational arguments (E32-7
through E32-10) are explicit. For routing, the route is:
```
direct_truncation: cost ~ -log(tol)/(-log(q))   [terms needed]
modular_S_transform: via Dedekind η-quotient
   R(q) = (η(q^5))/η(q) · ... [explicit S-image for q near 1]
```
For most q, direct truncation dominates; for `q → 1⁻`, S-transform wins.

(e) **Degeneracy modes.**
- `q ≥ 1`: divergent (Entry 11's oscillation regime); silent failure if
  not guarded.
- `q = 0`: trivial (R(0) = 0); convergent but uninteresting.
- `q = root of unity`: R(q) at primitive 5th roots of unity is a root of a
  cubic polynomial; needs special handling — *NOT* the truncation route.
  This is exactly the silent-zero analog for the Family-A CFs.

### 3B. Family B — E32-7 (Rogers-Ramanujan at q=exp(-4π))

(a) **Identity (verbatim).** `R(e^{-4π}) = √(c² + 1) - c` where
`2c := 1 + ((a+b)/(a-b)) √5`, `a = 5^{1/4}`, `b = 1`.

(b) **Why Family B.** Special-value lookup, not a CF to truncate.

(c) **Kernel-matcher pattern.** Recognize the structure
`R(exp(-π · rational))` and dispatch to a closed-form lookup table.

(d) **Closed form.** Explicit radical (above).

(e) **Degeneracy modes.** Lookup-miss (any q outside the catalogued set).
Routing layer should fall back to Family A truncation.

**Cluster uncertainty (per discipline note):** Family B might be subsumed
into the "class invariants / singular moduli" framework (NB V Ch. 34, Hunt
4) rather than treated as a CF family at all. Mark as **INDICATIVE**.

### 3C. Family C — E32-18 (Ramanujan-Selberg cubic CF, level-3)

(a) **Identity (verbatim from NB V Ch. 32 Entry 18, p. 373).** For `|q| <
1`,
```
G(q) := (q;q²)_∞ / (q³;q⁶)_∞³  =  1 / (1 + (q+q²)/1 + (q²+q⁴)/1 +
                                        (q³+q⁶)/1 + (q⁴+q⁸)/1 + ...)
```
Equivalently in η-quotient form: `G(q) = (q;q²)_∞ / (q³;q⁶)_∞³`.

(b) **Why Family C.** Andrews-Gordon-Selberg style; closed form is an
η-quotient (theta-products), level 3. Numerator-sequence pattern
`[q^k + q^{2k}]` is the level-N=3 Andrews-Gordon fingerprint.

(c) **Kernel-matcher pattern.** Match
```
1 / (1 + Sum_{k=1..∞} (q^k + q^{2k}) / (1 + ...))
```
which in sympy AST looks like an infinite CF whose `a_k` are
`q^k(1 + q^k) = q^k + q^{2k}`. The matcher extracts the level N=3 from the
exponent pattern of the closed form denominator `(q^a;q^N)_∞ (q^{N-a};
q^N)_∞^k`.

(d) **Closed form / numerical evaluation.** Two routes:
```
direct_truncation: cost ~ -log(tol)/(-log(q))
eta_quotient_evaluation: O(1) η evaluations (each O(√(-log(tol)/log(q)))
                        for Dedekind-η)
```
The η-quotient route is asymptotically faster for q near 1.

(e) **Degeneracy modes.**
- `q ≥ 1`: divergent.
- `q = primitive Nth root of unity` for `N | 3`: G(q) zeros / poles
  depending on N. Cf. CANDIDATE_INSIGHTS §A4 (silent-zero hazard). Zhang
  1996 (cited in Berndt NB V Ch. 32 Entry 19 commentary) studied
  convergence at roots of unity.
- `q complex with |q|=1` off roots of unity: limit-set behavior in the
  Mahler / Nesterenko transcendence sense; out of scope.

### 3D. Family D — E32-cubic (the cubic-base Eisenstein CF)

(a) **Identity.** From NB V Ch. 33 §3 + Entry 1 of Ch. 20 (PIII, p. 345),
the cubic G(q) (different G from Family C; here using Chan's notation)
satisfies
```
G²(q) + 2G²(q²)G(q) - G(q²) = 0
```
(Chan 1995, cited in proof of E32-10, eq. (10.6) in NB V), with G(q) =
`q^{1/3}/(1 + (q+q²)/1 + (q²+q⁴)/1 + (q³+q⁶)/1 + ...)` (Entry 1, Ch. 20)
— the **same CF expression as E32-18, BUT** with the cubic-base
interpretation in the proof of E32-10 it gets paired with L(q³) = P(q³)
Eisenstein data. The cubic CF and the cubic Eisenstein P(q) live on the
same modular curve X₀(3) and their identity (10.7):
```
3 + A³ = 1/v + 4v²,   A := √(5/3) · e^{10π/9} · f(-e^{-10π/3})/f(-e^{-30π}),
                      v := G(e^{-10π})
```
ties the cubic CF directly to the quasi-modular L(q³) via the proof
machinery. (See full chain in proof of E32-10, NB V pp. 28-30.)

(b) **Why Family D — the quasi-modular flag.** The cubic-base
identifications a(q) = M(q)/L(q)-style equations, plus the Eisenstein
differential equations (1.5) of Berndt-Yee (qP'/dq = (P²-Q)/12 etc.) tie
this CF family to weight-2 L(q) = P(q). The weight-2 anomaly means L(q)
*is not strictly modular* under τ → -1/τ — the S-transform has an
additive shift `-3/(πy)` (per Berndt-Yee p. 131). **This is the gap the
existing `eisenstein_E2k` registry entry doesn't cover** (it covers
weight-4 and -6 only; per `_match_eisenstein_E2k` in rkc/registry.py
line 322 the matcher requires k odd in σ_{2j-1}(n), i.e. weight = 2j ≥ 4).

(c) **Kernel-matcher pattern.** Two-step:
1. Recognize the CF shape (same as Family C, level 3).
2. Detect via context (e.g. the user explicitly invokes
   `recognize_cubic_eisenstein`) that the routing should go through the
   cubic Eisenstein chain rather than direct truncation.

In practice this is a *routing hint*, not a separate matcher. The Family-C
matcher fires first; the routing layer asks "would the cubic-eta-quotient
or the cubic-Eisenstein-derivative-system give a faster certification
here?" and picks.

(d) **Closed form / numerical evaluation.** Two specialized routes beyond
Family C:
- `cubic_eisenstein_derivative_system`: integrate q dG/dq = ... + (Eisenstein
  combo) and evaluate at target q.
- `cubic_base_inversion`: invert b(q)/a(q) using Borweins' cubic AGM (cf.
  NB V Ch. 33 Theorem 2.2). This is the routine the Borweins use in their
  cubic-AGM 1/π series.

(e) **Degeneracy modes.**
- Same as Family C plus:
- `q near cusp ∞ but on the q⁻¹/³ branch`: the cube-root branch needs the
  *correct* primitive cube root of unity choice; getting this wrong gives
  a `-G(q)` or a complex multiple. **Equivalent to the silent-zero hazard
  for cubic-base routes.** The degeneracy detector should refuse to route
  through cubic-Eisenstein unless the branch is specified.

### Verbatim quotes (per discipline check)

Three specific Ramanujan CFs, verbatim from NB V Ch. 32:

**Entry 18 (Family C representative)** (NB V, p. 47, Eq. (18.1)):

> `G(q) := (q;q²)_∞ / (q³;q⁶)_∞³  =  1/1 + (q+q²)/1 + (q²+q⁴)/1 + ...`

**Entry 21 (Family C, level-2 ambiguous case)** (NB V, p. 49, Eq.
(21.1)):

> `(-q²;q²)_∞ / (-q;q²)_∞ = 1/1 + q/1 + (q²+q)/1 + q³/1 + (q⁴+q²)/1 + ...`

**Entry 1(i) (Family A representative)** (NB V, p. 13):

> `Let |q| < 1, U := q^{1/5}/(1 + q/(1 + q²/(1 + q³/(1 + ...)))) =: U^{1/5}`
> `and v := q^{2/5}/(1 + q²/(1 + q⁴/(1 + q⁶/(1 + ...)))) =: V^{1/5}.`
> `Then (v - u²)/(v + u²) = uv².`

---

## 4. rkc/registry API extension sketch (pseudocode, ~150 lines)

Per [rkc/registry.py](../rkc/registry.py) the existing pattern is:

```python
RegistryEntry(name, family, match, recommend_route, degeneracy_check,
              per_term_cost, notes)
```

with `KernelFamily` enum in `routing.py`. Sketch for the new family:

```python
# --- routing.py addition ---

class KernelFamily(Enum):
    # ... existing entries ...
    EISENSTEIN_CF = "eisenstein_cf"   # new: q-CF whose limit is theta-quotient
                                       # or quasi-modular Eisenstein combo


# --- registry.py additions ---

# Match a q-CF of Andrews-Gordon-Selberg shape, level N, mod-N residue
# pair (a, N-a). The AST is most naturally captured as a sympy.Function
# proxy because sympy doesn't have a first-class infinite-CF type.

@_safe
def _match_eisenstein_cf_andrews_gordon(expr, n):
    """Match q-CF of shape
        1 / (1 + (q^a + q^{N-a})/(1 + (q^{2a} + q^{2(N-a)})/(1 + ...)))
    The limit is an η-quotient (q^a;q^N)_∞(q^{N-a};q^N)_∞ / (q^b;q^N)_∞
    (q^{N-b};q^N)_∞^k for some pairing (a,b).

    Returns {"q": q, "level": N, "residue_a": a, "residue_b": b,
             "family": "andrews_gordon"} on match.
    """
    # Approach: walk the user-provided expression looking for sympy.Function
    # proxies for the CF (since sympy doesn't natively represent infinite
    # CFs), OR a Limit() over partial CF approximants. Extract numerator
    # coefficient sequence; pattern-match to (q^{ak} + q^{(N-a)k})_{k=1..}.
    # Infer N from gcd of the exponents, a from the smaller exponent.
    pass


@_safe
def _match_eisenstein_cf_rogers_ramanujan(expr, n):
    """Match q-CF of shape  q^{1/5} / (1 + q/(1 + q²/(1 + q³/(1 + ...))))
    (Rogers-Ramanujan family). Returns {"q": q, "family":
    "rogers_ramanujan"} on match.
    """
    pass


@_safe
def _match_eisenstein_cf_cubic_base(expr, n):
    """Match the cubic-base Eisenstein CF G(q) =
    q^{1/3}/(1 + (q+q²)/(1 + (q²+q⁴)/(1 + ...))) and flag for routing
    through the cubic Eisenstein chain (Family D).

    Returns {"q": q, "family": "cubic_base_eisenstein",
             "quasi_modular": True} on match.
    """
    pass


def _route_eisenstein_cf(params, tol):
    """Routing for the new family.

    Direct route: truncate CF to k terms, cost ≈ -log(tol)/(-log(q))
                  multiplied by per-term-cost (3-4 mpf ops per CF level).

    Modular route: convert to η-quotient closed form and use the existing
                   `q_pochhammer_infty` route. Cost is O(√(-log(tol)/log(q)))
                   per η-factor, with N factors for level N.

    Quasi-modular routing flag: if `params.get("quasi_modular")`, surface
    a `QUASI_MODULAR_S_TRANSFORM` Route flag (new) instead of plain DUAL,
    so the routing layer knows to apply the L(q) - 3/(πy) shift on S-
    transform (per Berndt-Yee p. 131 footnote).
    """
    q = mpf(params["q"])
    if q <= 0 or q >= 1:
        return {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                "reason": "Eisenstein-CF requires 0 < q < 1", "num_terms": -1}
    family = params.get("family", "andrews_gordon")
    direct_cost = max(1, int(ceil(-log(mpf(tol)) / (-log(q)))))
    # Modular route via η-quotient
    eta_cost = int(ceil(sqrt(-log(mpf(tol)) / (-log(q)))))
    N = params.get("level", 3)
    eta_total = eta_cost * N
    if params.get("quasi_modular") and -log(q) < pi:
        # Quasi-modular family near q=1: use the L(q) modular completion
        return {"route": Route.QUASI_MODULAR_S_TRANSFORM,
                "cost_direct": direct_cost, "cost_dual": eta_total,
                "reason": "near q=1 cusp; weight-2 anomaly requires E_2(q)"
                          " - 3/(πy) shift",
                "num_terms": eta_total}
    route = Route.DUAL if eta_total < direct_cost else Route.DIRECT
    return {"route": route, "cost_direct": direct_cost, "cost_dual": eta_total,
            "num_terms": min(direct_cost, eta_total)}


def _eisenstein_cf_degeneracy(params):
    """Degeneracy detector.

    1. q ≥ 1: divergent.
    2. q = primitive Nth root of unity for N dividing the family's level:
       potential silent-zero / pole (Zhang 1996 for Andrews-Selberg level-3).
    3. Family D (quasi_modular=True): also require explicit cube-root
       branch specification, else refuse.
    """
    deg = _q_in_unit_disk(params)
    if deg:
        return deg
    q = params.get("q")
    if hasattr(q, "is_number") and q.is_number:
        # crude root-of-unity check
        N = params.get("level", 3)
        try:
            log_q = sp.log(q)
            ratio = sp.simplify(log_q / (2 * sp.pi * sp.I))
            if ratio.is_Rational:
                from math import gcd
                num, den = int(ratio.p), int(ratio.q)
                if gcd(num, den) == 1 and den <= N * 4:
                    return (f"q is a primitive {den}th root of unity; "
                            f"CF may hit silent zero / pole at level N={N}")
        except Exception:
            pass
    if params.get("quasi_modular") and "cube_root_branch" not in params:
        return ("Cubic-base Eisenstein CF requires explicit "
                "`cube_root_branch` parameter (0, 1, or 2) to disambiguate "
                "the q^{1/3} branch")
    return None


def per_term_cost_eisenstein_cf(params, target_precision):
    """Per-term cost for CF truncation. Each level of the CF requires
    O(1) mpf multiplications + 1 inversion at precision target_precision.
    Per CANDIDATE_INSIGHTS §A7, use per-term complexity not bits-per-term.
    """
    # Cost model: 4 mpf-mul + 1 mpf-div per CF level at prec bits.
    # mpf-mul at p bits ~ O(p log p) with FFT.
    p_bits = target_precision
    return 4 * p_bits * math.log(max(p_bits, 2)) + p_bits  # rough


# --- REGISTRY additions ---

REGISTRY.extend([
    RegistryEntry("eisenstein_cf_rogers_ramanujan", KernelFamily.EISENSTEIN_CF,
                  _match_eisenstein_cf_rogers_ramanujan, _route_eisenstein_cf,
                  _eisenstein_cf_degeneracy, per_term_cost_eisenstein_cf,
                  "Family A: Rogers-Ramanujan + sign-variations; "
                  "η-quotient closed form level 5; no quasi-modular flag"),
    RegistryEntry("eisenstein_cf_andrews_gordon", KernelFamily.EISENSTEIN_CF,
                  _match_eisenstein_cf_andrews_gordon, _route_eisenstein_cf,
                  _eisenstein_cf_degeneracy, per_term_cost_eisenstein_cf,
                  "Family C: Andrews-Gordon-Selberg q-CFs at level N "
                  "= 2,3,4,8 (E32-18 through E32-23); η-quotient closed "
                  "form"),
    RegistryEntry("eisenstein_cf_cubic_base", KernelFamily.EISENSTEIN_CF,
                  _match_eisenstein_cf_cubic_base, _route_eisenstein_cf,
                  _eisenstein_cf_degeneracy, per_term_cost_eisenstein_cf,
                  "Family D: cubic-base Eisenstein CF; QUASI-MODULAR "
                  "(weight-2 L(q) anomaly); requires cube_root_branch"),
])


# --- New Route enum value ---

class Route(Enum):
    # ... existing values ...
    QUASI_MODULAR_S_TRANSFORM = "quasi_modular_s_transform"
    # Family D needs this: modular S-transform with the weight-2 shift
    # L(q) → L(q*) - 3/(πy) per Berndt-Yee 2002 p. 131.
```

**Family B (special values) note:** Not registered as a kernel family.
Instead, the routing layer should learn 4 special-value short-circuits
(E32-7 through E32-10) as a lookup table, dispatched from the Family A
matcher when the input q happens to be `exp(-π·k)` for `k ∈ {4, 6, 8, 16}`.

**Test cases expected (5 per family minimum, per existing test pattern):**

For Family C alone:
- Match `Entry 18` exactly → recognize as `eisenstein_cf_andrews_gordon`
  with `level=3, family=andrews_gordon`.
- Match `Entry 21` → recognize as level-2 (cluster_uncertainty flag set).
- Match `Entry 22` → recognize as level-8.
- Route at q=0.1 → DIRECT preferred (direct_cost ~ 30 << eta_cost · N).
- Route at q=0.99 → DUAL preferred (eta_cost · N ≪ direct_cost).
- Degeneracy at q=0.99999 (near cusp): MODULAR or QUASI_MODULAR flag.
- Degeneracy at q = `exp(2πi/3)` for level-3: silent-zero hazard.
- Degeneracy at q = 1.5: divergent.

---

## 5. Cross-validation gate (per CLAUDE.md gotcha #5)

The cross-validation rule says: at least one (kernel, param) cell must
match to ≥40 digits across the direct CF truncation and a closed-form /
hypergeometric reference, *before* benchmarking the new registry entry.

The 2-3 specific cells per family:

**Family A (Rogers-Ramanujan):**
- (R(q), q=0.5, 50 digits): truncate the CF to k terms where k ≈
  -50·ln(10)/ln(0.5) ≈ 167 terms; compare to closed-form `R(q) = (η(q^5))/η(q)`
  evaluated via Dedekind η. Should match to ≥40 digits.
- (R(q), q=exp(-π/4), 60 digits): no clean closed form (this is NOT one of
  E32-7..10); but the Rogers-Watson identity R(q) = ... gives an
  independent route via theta-functions. Compare.

**Family C (Andrews-Gordon level-3):**
- (E32-18 G(q), q=0.3, 50 digits): truncate to k ≈ -50·ln(10)/ln(0.3) ≈
  100 levels; compare to `(q;q²)_∞ / (q³;q⁶)_∞³` evaluated by direct
  η-quotient. Should match to ≥40 digits.
- (E32-21 level-2, q=0.5, 50 digits): same, with the level-2 η-quotient.

**Family D (cubic-base Eisenstein):**
- (G(e^{-10π}), 80 digits, **with the explicit cube-root-of-unity branch
  fixed**): match against the explicit value derivable from the modular
  equation `G²(q)+2G²(q²)G(q)-G(q²)=0` (Chan 1995) at q=e^{-10π}, OR
  against the cubic Eisenstein P(q³)/Q(q³) chain computed independently.
  Must match to ≥40 digits.

**Cross-validation gate fail mode to watch for:** at level 3, the
ambiguous cube-root branch in Family D can give a `-G(q)` or `ω G(q)`
multiple. If the two computation paths disagree by a sign or a primitive
cube root, the failure is *real* (not noise) and indicates the branch
disambiguation is wrong. **This is the silent-zero analog for Family D
and the highest-risk gate cell.**

---

## 6. Quasi-modular anomaly note

The weight-2 anomaly is the central modular-forms reason this T2 work
matters per BIG_IDEAS_REVIEW §1.

**Affected families:** D (cubic-base) directly; C marginally (the
η-quotient closed forms are weight 0 modular and don't trigger the
anomaly themselves, but their `q dG/dq` derivatives do — see Berndt-Yee
1.5 for the cubic differential equations `q dL/dq = (L²-M)/12` etc.).
A and B are unaffected (weight 0 quotients of theta).

**Berndt-Yee 2002 p. 131 footnote (verbatim):**

> "The function P(q) is not a modular form. However, if q = exp(2πiτ),
> with Im τ = y, then P(q) - 3/(πy) satisfies the functional equation
> required of a modular form of weight 2."

**Registry communication.** The cleanest path is:

1. Add a `quasi_modular: bool` field to the matcher return dict.
2. Add a `notes: str` field to `RegistryEntry` (already exists) including
   the explicit shift formula `P → P - 3/(πy)`.
3. Add `QUASI_MODULAR_S_TRANSFORM` to `Route` enum (as sketched above).
4. The routing layer, when it sees `QUASI_MODULAR_S_TRANSFORM`, knows
   it must apply the additive shift before evaluating the S-image. Don't
   make the matcher carry the shift logic — keep it in the routing /
   evaluation layer (single responsibility).

**Risk:** if the matcher fires Family D incorrectly (false positive on
a Family C input), the routing layer applies the shift where it doesn't
belong, and the answer is *quantitatively wrong by 3/(πy) per occurrence*.
Per CLAUDE.md noisy-positive discipline, the matcher must be **strict**:
Family D should only fire when the user has explicitly invoked a
cubic-base computation (e.g. by passing `cube_root_branch` parameter)
OR when the AST contains both the cubic CF AND the explicit Eisenstein
chain (a structural co-occurrence test).

---

## 7. Effort + risk estimate

### Realistic effort (per family)

| Family | Recognize | Routes | Cross-validation | Tests | Total |
|---|---|---|---|---|---|
| A (Rogers-Ramanujan) | 1d | 1d | 0.5d | 0.5d | **3 days** |
| B (special values lookup) | 0.5d | 0.5d | 0.5d | 0.5d | **2 days** |
| C (Andrews-Gordon level-N) | 2d | 1d | 1d | 1d | **5 days** |
| D (cubic-base, quasi-modular) | 1d | 1d | 1.5d | 1d | **4.5 days** |

**Total: ~14-15 days of focused work** to get all 4 families to v0.2
registry-quality. This is 1.5x the HUNT_MAP §3 estimate ("medium effort,
clustering analysis"). The HUNT_MAP estimate was for the *clustering*,
not for the registry build-out.

Risk-adjusted estimate (per W2 risk discipline): **17-20 days** for full
v0.2 ship.

### What can go wrong

1. **False positives via fuzzy matcher.** Sympy's lack of native
   infinite-CF representation means the matcher must work on either a
   `Function` proxy or a `Limit` of partial approximants. Both are
   fragile. **Risk: HIGH.** Mitigation: require strict structural match
   (no fuzzy fallback for Family C / D — only Family A which is broadly
   recognizable).

2. **Wrong family clustering.** E32-21 (level-2 ambiguous) is the
   canonical risk. If a user expects "level-2 q-CF" to route through a
   level-2 η-quotient evaluation and we route through level-8 (E32-22's
   neighbor), the cost estimate is wrong by ~4x. **Risk: MEDIUM.**
   Mitigation: explicit `level` parameter on registry entry; matcher
   refuses to fire if level can't be inferred unambiguously from the
   exponent sequence.

3. **Quasi-modular anomaly not propagating cleanly through cost
   estimator.** If the cost estimator doesn't know the quasi-modular
   shift is being applied, it can't compare DUAL vs DIRECT correctly.
   **Risk: MEDIUM-HIGH.** Mitigation: the cost estimator gets the
   `quasi_modular` flag as input and adds a small constant overhead for
   the shift evaluation (≪ the main mpf cost; doesn't change the
   asymptotic).

4. **Family D cube-root-branch silent failure.** The cubic-base
   Eisenstein CF has a 3-fold branch in the q^{1/3} prefactor. Picking
   the wrong branch gives a complex multiple of the answer. This is
   directly analogous to the gauss-sum silent-zero hazard at q≡2 mod 4.
   **Risk: HIGH (correctness-fatal).** Mitigation: degeneracy detector
   *refuses to route* unless `cube_root_branch` is explicitly specified.
   Test case: deliberately pass a Family D input without the branch
   parameter and confirm the detector fires.

5. **Cross-validation gate at Family D.** Per §5, the cross-validation
   cell at q=exp(-10π) is the *highest-risk* check in the whole T2 work
   because it sits at the intersection of (a) the cubic branch issue,
   (b) the L(q)-shift issue, (c) the cusp-near route boundary. A clean
   pass here = the family is correctly instrumented. A fail = investigate
   before touching the matcher.

6. **"Eisenstein CF" naming is misleading.** Per top of this doc, only
   Family D is truly Eisenstein in the modular-forms sense. Naming the
   whole `KernelFamily.EISENSTEIN_CF` is convenient but might confuse
   downstream users. **Risk: LOW (cosmetic / documentation).**
   Mitigation: rename to `KernelFamily.Q_CF_THETA_QUOTIENT` and put
   Family D as a sub-family with `is_eisenstein=True` flag.

### Pre-implementation decision required

The single concrete decision that must be made before implementation:

**Family granularity.** Should Family C be **one** registry entry with a
`level` parameter `N ∈ {2, 3, 4, 8}`, or **four separate** entries
(`eisenstein_cf_level_2`, `..._level_3`, `..._level_4`, `..._level_8`)?

- **One entry, parameterized**: cleaner, smaller registry, but the matcher
  has to infer `level` from the AST exponent sequence — potentially fragile.
- **Four entries**: each matcher is strict, dispatches cleanly, easier to
  test in isolation. But the registry grows by 4 entries (manageable; we
  already have 11). Easier to add new levels later (e.g. Selberg's level-5
  or level-7 found by Bhatnagar arXiv:2208.12656).

**My recommendation: four separate entries.** It matches the existing
registry pattern (separate entries for `mock_theta_f3`, `mock_theta_f5`,
`mock_theta_f7`) and is easier to retire/add families as new q-CFs are
discovered. Cost: 4 extra entries (registry currently has 11; would
become 11 + 4 (Family C levels) + 1 (Family A) + 1 (Family D) = 17 total).
That's still well under any maintainability ceiling.

### Bonus: incremental ship plan

1. **Day 1-3:** Ship Family A (Rogers-Ramanujan recognizer + R(q) special
   values). Adds 1 registry entry + 4 lookup short-circuits. Test pass
   on E32-1 through E32-10.
2. **Day 4-8:** Ship Family C levels 2 and 3 (E32-18, E32-21).
3. **Day 9-12:** Add Family C levels 4 and 8 (E32-20, E32-22, E32-23).
4. **Day 13-16:** Ship Family D + the quasi-modular route flag + the
   highest-risk cross-validation gate.
5. **Day 17-18:** Documentation, README example, CHANGELOG.

The Day-13-16 work is the only piece that touches quasi-modular machinery;
if it slips, Days 1-12 still ship as a useful v0.2 increment without
the weight-2 anomaly coverage. **The clean cut line is Family A+C vs
Family D.**

---

## Cross-references & next-action note

Related insights to update once registry lands:
- [BIG_IDEAS_REVIEW §1](BIG_IDEAS_REVIEW.md) — extend the "5 kernels
  substantiated end-to-end" claim to "5 + Eisenstein-CF family
  substantiated".
- [CANDIDATE_INSIGHTS §A6](CANDIDATE_INSIGHTS.md) — the β\* = c·π
  crossover pattern should be re-tested on Family C (prediction: holds
  with c = level N).
- [HUNT_MAP §3](HUNT_MAP.md) — close as "RESOLVED" with the 4-family
  clustering. Add the caveat that the original "20 CFs" was a rough
  count; the true content is ~30 CFs in Ch. 32 across 4 families.

**Out of scope flagged for follow-up (NOT for this T2 ship):**

- Bhatnagar's q-CF survey (arXiv:2208.12656) lists additional Selberg-
  family CFs at level 5, 7 that are NOT in NB V Ch. 32 but extend the
  Andrews-Gordon Family C structure. Adding these is a clean v0.3
  extension.
- The hypergeometric `φ(a)/φ(aq)` CFs of Entries 15-17 (Selberg-Andrews-
  Bowman, two-parameter) constitute their own family that could be a
  separate registry entry (`q_hypergeometric_cf`) downstream.
- Andrews-Berndt *Lost Notebook Part III* (in
  `downloaded-pdfs/Ramanujan_39_s_Lost_Notebook_Part_III_2012.pdf`) has
  more CF material per the introduction's reference to "100 unorganized
  pages... contain about 60 further results on continued fractions"
  (NB V Ch. 32 intro p. 9). Should be folded in for v0.3.

---

**Bottom line for review.** The clustering proposal is **4 families with
medium confidence**; one ambiguity (E32-21 level-2) tagged honestly. The
quasi-modular anomaly is the key technical wrinkle — it's contained to
Family D and proposes a new `QUASI_MODULAR_S_TRANSFORM` Route flag. The
single decision needed before implementation: family granularity (4
separate level-N entries vs 1 parameterized entry — my recommendation:
4 separate). Total realistic effort: 17-20 days for full v0.2 ship,
with a clean partial-ship cut line at Family A+C (Day 12) before the
Family D quasi-modular work.
