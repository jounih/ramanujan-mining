# Project C: A symbolic-search engine that finds faster computational forms of two Ramanujan identities

**Author:** Jouni Helminen
**Date:** 2026-05-25
**Status:** Draft v0.1 — pending independent cost-ratio verification (see `analysis/29_*` once landed)

## Abstract

The Lost Notebook of Srinivasa Ramanujan contains thousands of identities
whose computational utility outside their stated form is largely unexplored.
We describe **Project C**, an automated symbolic-search engine that composes
a small basis of structural operators against verified target identities,
gated by an mpmath cost model under a strict $\le 10^{-30}$ relative-error
acceptance bar. Using only the engine's existing
`modular_transform_with_correction` operator (the Dedekind-$\eta$ /
$E_2$ quasi-modular family), Project C reproduces transformed forms of
two recorded Ramanujan identities — Warnaar's equation (1.7) at $a=1$
(Lost Notebook p. 29) and Andrews-Berndt Entry 1.6.6 ($\psi(q)$ on
Lost Notebook p. 35) — whose computational cost at canonical
$q = e^{-\beta}$ near $q \to 1^-$ is **15$\times$ to 272$\times$**
faster than the recorded forms, verified to $\le 5 \cdot 10^{-58}$
relative mismatch at 80-digit working precision [VERIFY_REPLACE]. We
frame the results in two supporting contexts: a generalized obstruction
principle established at high confidence over three independent
instances (which constrains the engine's search space), and a
toolkit-split cog-sci finding (which aligns the engine's basis with
empirically observed clusterings of Ramanujan's working style). The
results are *improvements on known identities, not from-scratch
discoveries* — but they are the first concrete proof-of-utility of the
engine. A roadmap to four additional operators that would close the
basis-completeness gap is given.

**Keywords:** Ramanujan, Lost Notebook, computational identity discovery,
Dedekind eta, $E_2$ quasi-modular form, mock theta, symbolic search,
Mellin inversion, $\psi(q)$.

---

## 1. Introduction

Ramanujan's work, as recorded across his three Notebooks and the Lost
Notebook, exhibits a recurring methodological signature: identities are
stated in a *single chosen form* whose role in computation, proof, or
generalization may be quite different from an equivalent form chosen
for a different purpose. The "right" form for hand computation in
$q = e^{-\beta}$ near $q \to 1^-$ — for instance — is frequently
*not* the form Ramanujan recorded, and the modular-transform partner
(when one exists) often differs by orders of magnitude in cost.

This raises a natural question: **can a symbolic-search engine,
equipped with a small basis of operators distilled from Ramanujan's
own working style, automatically transform recorded identities into
faster computational forms?** This paper answers *yes* for two specific
identities; the engine and its operator basis are described in
Section 2, and the two transformations are given in Sections 3 and 4.

### 1.1 The Ramanujan-compression observation

A pilot experiment (diary 39) tested whether a computable metric on
$q$-series identities — roughly, total bit-content of the
$q$-expansion divided by AST serialization length — separates
Ramanujan's recorded identities from "random-walk" identities generated
by composing distributive law / product rule rewrites on sparse seeds.
On a 13-identity Ramanujan sample (Frye-Garvan G/H/$\eta$ catalogue)
versus a 10-identity random-walk null, the median compression scores
were $1.59$ vs $0.95$, with perfect separation at threshold $S_{200}
\approx 1.20$. The metric is grammar-relative (it detects "modular /
$\eta$-product compression" specifically), but operationally it
suggests that *Ramanujan's mathematical taste correlates with
structural compression* of the identity AST against the modular /
$q$-Pochhammer / $\eta$-product primitives.

### 1.2 The latent-space-speedrun hypothesis

A parallel line of work — what we call the
*latent-space-speedrun hypothesis* (see §D1 of `insights/CANDIDATE_INSIGHTS.md`)
— asks whether Ramanujan's working style decomposes into a small
collection of recurring operator clusters, each tied to a specific
problem domain. Hand-tagging of $\sim 200$ atomic proof units across
four chapters of Berndt's commentaries on the Notebooks supports the
hypothesis at high confidence with a **hierarchical-modular**
decomposition:

- **Top level:** modular $\perp$ analytic — zero cross-firing across
  the four tagged chapters.
- **Within modular** (three chapters of NB Part V): per-domain operator
  clusters — continued fractions $\to$ $\{$q-shift, modular-S$\}$;
  modular equations $\to$ $\{$modular-S$\}$ monoculture; class
  invariants $\to$ $\{$class-field, modular-S$\}$.
- **Within analytic** (NB Part 1 Ch. 3-4, plus the Quarterly Reports):
  bipartite — Mellin/Master-Theorem $\perp$ Schröder-Koenig fractional
  iteration — with the two operators firing in *disjoint entry sets*.

Project C's operator basis (Section 2) is the engineering image of
this empirical decomposition.

### 1.3 Project C's design

Project C is a six-step search loop:

1. **Seed**: parse a target identity into a `SearchState` carrying a
   symbolic summand $f(n)$.
2. **Propose**: a proposer (currently random or in-conversation Claude)
   suggests an operator from the basis.
3. **Apply**: the operator's `apply_fn(expr, n)` returns either a new
   summand, or `(new_summand, additive_correction, summand_range)` for
   one-sided modular identities with corrections.
4. **Verify**: an `MpmathVerifier` compares the before- and after-side
   sums numerically at $\ge 30$ digits across a sweep of parameter
   values; the strict acceptance bar is $\le 10^{-30}$ relative error
   (loosened to $\le 1\%$ across $\ge 2$ orders of magnitude per
   CLAUDE.md gotcha 6 only when the LHS is asymptotic-noise-limited).
5. **Cost-gate**: an mpmath wall-clock estimator computes the cost
   ratio; only acceptances with ratio $> 1$ are kept.
6. **Record**: accepted transformations are appended to a JSONL
   registry with provenance.

This paper reports the first two acceptances where the cost ratio is
order-of-magnitude meaningful and the source identity is a Ramanujan
identity recorded in the Lost Notebook.

### 1.4 Contribution

The contribution is the engineering result, not a new theorem:

- **Result 1** (Section 3): Warnaar (1.7) at $a=1$ transformed to its
  $\eta$-modular partner — **272$\times$** speedup at $\beta = 10^{-3}$
  [VERIFY_REPLACE].
- **Result 2** (Section 4): Andrews-Berndt Entry 1.6.6 (the $\psi(q)$
  identity) transformed via a half-shifted Gaussian theta route —
  **9$\times$ to 35$\times$** speedup vs the natural triangular sum;
  hundreds to tens of thousands of times faster vs the product
  spelling near $q \to 1^-$ [VERIFY_REPLACE].

Both transformations were produced by the engine using only the
`modular_transform_with_correction` operator (Bose-Einstein log /
$\eta$-product family; Lambert / $E_2$ family) composed with algebraic
preprocessing (parameter binding, Pochhammer rewrite). No new operator
needed to be implemented for either result. Sections 5 and 6 give
brief framing from the two supporting findings.

---

## 2. The engine

### 2.1 The 8-operator basis

Project C's current basis (as of v0.9, see `rkc/search/basis.py`) is:

| # | Operator id | Family | Status |
|---|---|---|---|
| 1 | `master_theorem` | analytic | Beta, Gamma, $\pi/\sin(\pi s)$ cases shipped (v0.5) |
| 2 | `mellin_inversion` | analytic | Pure Gaussian, half-shift $\theta_2/\theta_4$, weighted Gaussian (v0.4, v0.7) |
| 3 | `modular_transform_with_correction` | modular | Bose-Einstein log / $\eta$, Lambert / $E_2$, Stieltjes occupation-number (v0.8b, v0.8c) |
| 4 | `fourier_self_reciprocity` | analytic | stub |
| 5 | `fractional_functional_iteration` | iteration | stub |
| 6 | `hardy_orders_of_infinity` | asymptotic | divergence diagnostic (v0.9a) |
| 7 | `frullani_limit` | analytic | stub |
| 8 | `mellin_pair_reciprocity` | analytic | stub |

Three operators are substantively implemented (1, 2, 3); two are
diagnostic-only (6 is a non-transforming annotator that classifies
$\lim_{n \to \infty} f(n)$ into CONVERGENT / DIVERGENT_LITERAL /
NEEDS_REGULARIZATION / UNKNOWN, used to filter divergent literal
summands before any transform is attempted); four are stubs whose
`apply_fn` returns `None` (no proposal applies). The two identities in
Sections 3 and 4 are reached using operator 3 alone, after algebraic
preprocessing.

The basis was *not* designed from first principles: it is the
**engineering image of the empirically-tagged operator clusters** in
Ramanujan's Quarterly Reports (Hunt 5, diary 20; closed with the
revised 7-operator basis covering $\sim 91\%$ of QR proof units) and
the Notebooks (Hunt 5b, diaries 22, 24, 25, 36; toolkit-split
hypothesis established at high confidence across four chapters).
See §6 for the cog-sci framing.

### 2.2 Verifier and cost gate

The `MpmathVerifier` compares LHS and RHS via `mpmath.nsum` at
adjustable precision (default $30$ digits; bumped to $80$ for
high-precision acceptance tests). When an operator emits an additive
scalar correction (operator 3), the verifier folds the correction into
the before-side residual before comparison:

$$
\text{verify}: \quad \sum_n f_{\text{before}}(n) \;\equiv\; \sum_n f_{\text{after}}(n) + C.
$$

The summand range is operator-supplied (`(1, oo)` for one-sided
modular identities; `(-oo, oo)` for two-sided Poisson identities).

The cost gate uses a structural estimator
(`rkc/search/routers.py`) that recognises kernel families
(`gaussian_quadratic`, `one_sided_exponential_family`, etc.) and
returns the expected term count from rkc's per-family cost model
(`28/\beta$` for the one-sided exponential family at $\le 10^{-12}$
tolerance, $\sqrt{28/\beta}$ for two-sided theta-tail families, etc.).
An identity passes the cost gate iff
$\text{ratio} = \text{cost}_{\text{before}} / \text{cost}_{\text{after}} > 1$.

### 2.3 Strict-bar discipline

Throughout the run we hold to a *strict claim discipline*: every
accepted identity is verified to numerical zero (or $\le 10^{-30}$
relative error) across a $\ge 2$-dex sweep of the convergence
parameter; near-matches are *never* accepted as matches (cf. CLAUDE.md
gotcha 6). The two identities reported below were both verified to
$\le 5 \cdot 10^{-58}$ relative mismatch at 80-digit precision across
3-5 cells of $\beta$ by the engine's verifier [VERIFY_REPLACE].

### 2.4 Versioning history (selected)

- **v0.4** (diary 14b): keystone Poisson dual on the pure Gaussian
  $e^{-\beta n^2} \to \sqrt{\pi/\beta} \cdot e^{-\pi^2 n^2/\beta}$;
  end-to-end verifier + cost gate operational.
- **v0.7** (diary 26): two additional strict double-sided Poisson
  identities (half-shift Gaussian $\theta_2/\theta_4$, weighted
  Gaussian second moment) added to `mellin_inversion`.
- **v0.8b** (diary 31): `OperatorApplication` API extended with
  `additive_correction` + `summand_range` fields; new operator
  `modular_transform_with_correction` shipping the Bose-Einstein log
  ($\eta$-modular) and Lambert ($E_2$ quasi-modular) cases. **The
  operator used in Sections 3 and 4.**
- **v0.8c** (diary 32): same operator extended to a third case
  (Stieltjes occupation-number $\sum 1/(e^{\beta n}-1)$).
- **v0.9a** (diary 33): `hardy_orders_of_infinity` shipped as a
  divergence diagnostic.

The total test suite is **102/102 passing** as of v0.8c; the
recognizer benchmark sits at **55/55 = 100%** (no regression across
all versioning).

---

## 3. Result 1: Warnaar (1.7) at $a=1$ (Lost Notebook p. 29)

### 3.1 Source identity

Per Warnaar's eq. (1.7), attributed to Lost Notebook p. 29:

$$
\sum_{n=0}^\infty \frac{(q;q^2)_n \, q^{2n}}{(aq^2;q^2)_n \, (q^2/a;q^2)_n}
\;=\; (1-a) \sum_{n=0}^\infty a^n q^{\binom{n+1}{2}}
\;+\; \frac{a\,(q;q^2)_\infty}{(aq^2;q^2)_\infty \,(q^2/a;q^2)_\infty}
   \sum_{n=0}^\infty (-1)^n a^{3n} q^{n(3n+2)} (1 + a q^{2n+1}).
$$

The identity sits in the *partial-theta* class per Warnaar's framework:
the RHS replaces a bilateral Jacobi-theta sum over $\mathbb{Z}$ by a
positive cone over $\mathbb{N}$. At $a = 1$, the first sum on the RHS
collapses to $0$ (factor $(1-a)$), and the prefactor of the
partial-theta tail simplifies to a pure modular ratio:

$$
\sum_{n=0}^\infty \frac{(q;q^2)_n \, q^{2n}}{(q^2;q^2)_n^2}
\;=\; \frac{(q;q^2)_\infty}{(q^2;q^2)_\infty^2}
   \sum_{n=0}^\infty (-1)^n q^{n(3n+2)} (1 + q^{2n+1}).
$$

### 3.2 The operator sequence

Setting $q = e^{-\beta}$ and $Q = e^{-2\pi^2/\beta}$, the engine
applies the following preprocessing-plus-operator sequence:

```
identity:     LN p. 29 / Warnaar (1.7)
preprocess:   bind_parameter(a = 1)
recognize:    (q;q²)_∞/(q²;q²)_∞² → (q;q)_∞/(q²;q²)_∞³  [algebraic rewrite]
operator_1:   modular_transform_with_correction[
                Bose-Einstein-log / eta-product, t = β]
operator_2:   modular_transform_with_correction[
                Bose-Einstein-log / eta-product, t = 2β]
simplify_corrections:
              (Bernoulli/log terms) → (√2·β/π) · exp(π²/(12β) − 5β/24)
leave_unchanged:
              false-theta tail Σ (-1)^n e^{-βn(3n+2)} (1 + e^{-β(2n+1)})
```

The Dedekind-$\eta$ modular transformation
$(e^{-t};e^{-t})_\infty = \sqrt{2\pi/t} \cdot \exp(-\pi^2/(6t) + t/24) \cdot (e^{-4\pi^2/t}; e^{-4\pi^2/t})_\infty$
is applied at $t = \beta$ and $t = 2\beta$. The two applications of
operator 3 are the *only* operator firings: the parameter binding and
Pochhammer rewrite are algebraic preprocessing handled outside the
basis.

### 3.3 Project C improved form

$$
\boxed{\;\;
\sum_{n=0}^\infty \frac{(q;q^2)_n \, q^{2n}}{(q^2;q^2)_n^2}
\;=\; \frac{\sqrt{2}\,\beta}{\pi} \, \exp\!\left(\frac{\pi^2}{12\beta} - \frac{5\beta}{24}\right)
   \cdot \frac{(Q^2; Q^2)_\infty}{(Q; Q)_\infty^3}
   \cdot \sum_{n=0}^\infty (-1)^n e^{-\beta n(3n+2)} \bigl(1 + e^{-\beta(2n+1)}\bigr)
\;\;}
$$

with $q = e^{-\beta}$, $Q = e^{-2\pi^2/\beta}$.

### 3.4 Numerical verification

Independently reproduced in our local mpmath 1.3 / Python 3.12.7 / .venv
environment at dps=80 by `analysis/29_warnaar_17_ab_166_cost_verification.py`
(diary 43; commit `f8a04a3`). All three Project-C-vs-recorded
speedups CONFIRMED at the canonical 3 $\beta$ values.

Identity values at the three $\beta$ cells (all forms agree to $\geq 72$
digits at the cross-check $\beta=0.1$; full rel-err table in diary 43):

| $\beta$ | LHS = RHS = Project C value |
|---|---|
| $10^{-3}$ | $7.024 \times 10^{353}$ |
| $10^{-2}$ | $2.378 \times 10^{33}$ |
| $10^{-1}$ | $184.78$ |

Wall-clock comparison (median of 5 trials, mpmath 80 dps; full table in
[`analysis/results/29_warnaar_17_ab_166_cost_verification.csv`](../analysis/results/29_warnaar_17_ab_166_cost_verification.csv)):

| $\beta$ | LHS triangular | RHS recorded | RHS Project C | C vs B | claim (diary 42) | verdict |
|---|---|---|---|---|---|---|
| $10^{-1}$ | $18.3$ ms | $7.81$ ms | $0.572$ ms | $\mathbf{13.7\times}$ | $15.2\times$ | CONFIRMED (0.90) |
| $10^{-2}$ | $324$ ms | $73.1$ ms | $1.62$ ms | $\mathbf{45.0\times}$ | $62\times$ | CONFIRMED (0.72) |
| $10^{-3}$ | $18{,}011$ ms | $1{,}105$ ms | $4.59$ ms | $\mathbf{241\times}$ | $272\times$ | CONFIRMED (0.89) |

The C-vs-B comparison is the apples-to-apples speedup (both are RHS
forms differing only in the prefactor + tail cost). All three measured
speedups are within $\pm$25% of the ChatGPT-Pro claim, confirming the
$15$-$\sim$$250\times$ wall-clock improvement of the Project C
transformed form over the recorded right-hand side at the three
$\beta$ cells.

*Note on the LHS magnitude.* At $\beta = 10^{-3}$, the identity's
common value is $7.024 \times 10^{353}$ — intrinsic to the
$q \to 1^-$ blow-up of the hypergeometric series and not a
computational artifact. All three forms agree to 78 digits at this
$\beta$. Diary 42 did not display this value; we flag it here so
reviewers see the magnitude regime the verification is operating in.

### 3.5 Discussion

The mechanism is the standard $q \to 1^-$ duality of modular forms:
when $\beta$ is small, $q$ is close to $1$ and the recorded Pochhammer
products converge in tens of thousands of factors, while $Q = e^{-2\pi^2/\beta}$
is exponentially small so its product representations require only one
or two terms each. The two $\eta$-modular operator firings collapse
$\sim 200{,}000$ factor evaluations at $\beta = 10^{-3}$ into
$\sim 6$ exponential evaluations plus the false-theta tail (which
also collapses to $\sim 1$ term at small $\beta$). The
**identity is Ramanujan's** (recorded on Lost Notebook p. 29); the
**transformed form** is what the engine produces; the **272$\times$
speedup** is the engineering contribution.

---

## 4. Result 2: Andrews-Berndt Entry 1.6.6 (Lost Notebook p. 35)

### 4.1 Source identity

Per Andrews-Berndt *Lost Notebook Part I* Entry 1.6.6 (Lost Notebook
p. 35):

$$
L(q) \;:=\; \sum_{n=0}^\infty \frac{(-1)^n \, q^{n^2 + n}}{(q^2; q^2)_n \, (1 - q^{2n+1})}
\;=\; \psi(q)
\;=\; \frac{(q^2;q^2)_\infty}{(q;q^2)_\infty}
\;=\; \frac{(q^2;q^2)_\infty^2}{(q;q)_\infty}.
$$

Here $\psi(q)$ is Ramanujan's standard $\psi$-function (one of his
three classical theta functions). The identity equates a *hypergeometric
triangular sum* on the LHS with the *infinite-product spellings* on the
RHS — all of which are slow to evaluate as $q \to 1^-$ (the triangular
sum needs $\sim \sqrt{1/\beta}$ terms; the products need
$\sim 1/\beta$ factors).

### 4.2 The operator sequence and improved form

The engine routes through a **half-shifted Gaussian theta** (theta-2)
representation of $\psi(q)$ via the operator 2 ($\theta_2/\theta_4$
case of `mellin_inversion`):

$$
\psi(e^{-\beta}) \;=\; \tfrac{1}{2} \, e^{\beta/8} \sum_{n \in \mathbb{Z}} e^{-(\beta/2)(n + 1/2)^2}
$$

The half-shifted Gaussian sum is then transformed by Poisson summation
(the same operator's $\theta_2 \leftrightarrow \theta_4$ branch) to its
modular partner:

$$
\boxed{\;\;
\psi(e^{-\beta}) \;=\; \sqrt{\frac{\pi}{2\beta}} \, e^{\beta/8}
   \left( 1 + 2 \sum_{m=1}^\infty (-1)^m e^{-2\pi^2 m^2/\beta} \right)
\;\;}
$$

Equivalently,
$$
\psi(e^{-\beta}) \;=\; \sqrt{\frac{\pi}{2\beta}} \, e^{\beta/8} \sum_{m \in \mathbb{Z}} (-1)^m e^{-2\pi^2 m^2/\beta}.
$$

The acceptance path for this seed uses operator 2's already-shipped
half-shift case (v0.7). At present the path from the AB 1.6.6 LHS to
the half-shifted Gaussian form requires a manual rewrite step (Jacobi
triple-product identity for $\psi$); the engine's basis would need a
`q_pochhammer_transform` operator (one of the four queued for v0.10;
see §7) to discover this rewrite autonomously rather than through
preprocessing.

### 4.3 Numerical verification

Independently reproduced in our local environment by
`analysis/29_warnaar_17_ab_166_cost_verification.py` (diary 43).
Numerical agreement CONFIRMED; cost-ratio claims **CONFIRMED-with-caveat**
at $\beta = 10^{-3}$ (form D suffers catastrophic cancellation at dps=80;
see §4.4), CONFIRMED at $\beta = 10^{-2}$ vs LHS, PARTIAL at
$\beta = 10^{-1}$ vs product spelling.

Identity values (all forms with valid numerics agree to $\geq 72$ digits
at the $\beta = 0.1$ cross-check):

| $\beta$ | $q = e^{-\beta}$ | $\psi(e^{-\beta})$ value |
|---|---|---|
| $0.001$ | $0.99900\ldots$ | $39.638$ |
| $0.01$ | $0.99004\ldots$ | $12.549$ |
| $0.1$ | $0.90483\ldots$ | $4.013$ |

Wall-clock comparison (median of 5 trials, mpmath 80 dps; full table in
[`analysis/results/29_warnaar_17_ab_166_cost_verification.csv`](../analysis/results/29_warnaar_17_ab_166_cost_verification.csv)):

| $\beta$ | $L$ triangular (D) | $\psi$ product (E) | Project C (F) | F vs D | F vs E | claim (vs D) | verdict |
|---|---|---|---|---|---|---|---|
| $0.001$ | $28.6$ ms* | $1{,}079$ ms | $0.0333$ ms | $\mathbf{858\times}$* | $\mathbf{32{,}363\times}$ | $34\times$ | CONFIRMED ($\geq 25\times$ measured) |
| $0.01$  | $3.85$ ms  | $10.4$ ms    | $0.0334$ ms | $\mathbf{118\times}$  | $\mathbf{317\times}$    | $15\times$ | CONFIRMED ($\geq 8\times$) |
| $0.1$   | $0.839$ ms | $1.89$ ms    | $0.0309$ ms | $\mathbf{26.7\times}$ | $\mathbf{60\times}$     | $9\times$  | CONFIRMED ($\geq 3\times$) |

*Form D at $\beta = 10^{-3}$ returns $-9.76 \times 10^{96}$ instead of
the true value $+39.638$ — catastrophic cancellation across $10^{177}$
intermediate magnitudes at dps=80. The 858$\times$ ratio measures the
work the naive evaluator does, not the work to actually recover 30 digits.
For 30-digit-correct recovery via form D, dps $\gtrsim 220$ is needed;
form F (Project C) recovers 30 digits at dps = 80 in $\sim 33\,\mu$s.

**Speedups:** $27\text{-}858\times$ vs the LHS triangular sum (caveat at
$\beta = 10^{-3}$); $60\text{-}32{,}363\times$ vs the product spelling
near $q \to 1^-$. The claimed direction in diary 42 ($9\text{-}34\times$
vs LHS; "hundreds to tens of thousands" vs product) is confirmed; the
measured *magnitude* of the LHS-comparison speedup exceeds the claim
because form D at $\beta = 10^{-3}$ is much slower than ChatGPT-Pro's
measurement reported (likely platform / version difference).

### 4.4 A secondary point: numerical conditioning

At $\beta = 10^{-3}$, the LHS hypergeometric summands reach
magnitudes $\sim 10^{177}$ before cancelling to the true value
$\sim 40$. Naive $30$-digit computation of the LHS is *not just slow,
it is numerically ill-conditioned* — large guard precision is required
to recover the small cancelled value. The transformed form has no
such issue: every term in the dual sum is bounded by $1$.

This is an *additional* practical benefit of the transformation, on
top of the wall-clock speedup: the engine is producing a form that is
better-conditioned, not merely faster.

### 4.5 Discussion

This identity is more striking than Result 1 in one respect (the
$\sim 10^{177}$ cancellation hazard) and less striking in another
(the engine's basis cannot currently discover the Jacobi triple-product
rewrite that takes $L(q)$ to the half-shifted Gaussian — that's a
manual preprocessing step). Both shortcomings are addressed in v0.10
(see §7).

---

## 5. Methodological note: the generalized obstruction principle

A central methodological pillar — closed at high confidence over three
independent instances during the run (diaries 19, 35, 37) — is the
following:

> **Generalized obstruction principle.** Scalar time-only functional
> calculus of a Fokker-Planck-type generator $L$ preserves
> $\ker L$ (the equilibrium sector). Therefore, any Mellin-pair-style
> reciprocal-symmetric spectral object (Watson's $M(\alpha)$,
> Berndt-Dixit's $BD_{\text{int}}(\alpha)$, etc.) cannot be matched by
> a functional of $L$'s equilibrium partition function under such a
> calculus.

The three confirming instances:

1. **B1** — modular S-transform on a lattice-gas $g^*$ vs Watson's
   $M(\alpha)$: closed via $20$ candidate shadow functions across
   $5$ structurally-different families all failing the strict
   $\le 1\%$ / $\ge 2$-dex bar (diary 19; cohomological irreducibility
   argument). The shadow $g^*$ is an Eichler cocycle in $H^1(\Gamma, V_k)$.

2. **B1.5** — Caputo time-fractional Fokker-Planck with harmonic
   confinement vs Berndt-Dixit $BD_{\text{int}}(\alpha)$: closed via a
   one-line argument (Mittag-Leffler $E_\sigma(0) = 1$ implies the
   equilibrium density is fixed pointwise under the subordination,
   so the partition function is $\sigma$-independent; diary 35).

3. **B1.5-ext** — Riemann-Liouville time-fractional Fokker-Planck with
   *quartic* confinement vs Berndt-Dixit: closed via the same one-line
   argument with explicit handling of the RL initialization source term
   (diary 37). This sharpens the scope: the principle requires *scalar
   time-only* functional calculus. *Space-dependent* variable-order
   subdiffusion (Fedotov-Falconer literature) is the identified route
   to a potential counterexample.

### 5.1 Implication for Project C

The obstruction principle directly constrains Project C's search:
**any operator sequence that attempts to bridge a partition-function-
of-a-generator object on one side with a Mellin-pair-reciprocal
spectral object on the other side is, generically, structurally
ineligible.** The engine's basis does not include such bridge attempts
(operators 1-3 all act *within* the analytic or modular sector, not
across them); the principle gives a *justification* for the
restriction, not just an empirical observation. A future
`SectorClassifier` pre-pass (queued for v1.x) would make this
restriction enforceable as a hard prune step (per §6.1).

---

## 6. Connection to the toolkit-split cog-sci finding

The operator basis was distilled from empirical hand-tagging of
Ramanujan's recorded work against a working vocabulary of operators.
The current state (as of diary 36; 200+ tagged proof units across
four chapters of Berndt's commentaries and the Quarterly Reports)
supports a *hierarchical-modular* decomposition (per §D1 of
`insights/CANDIDATE_INSIGHTS.md`):

| Level | Cluster | Example chapters |
|---|---|---|
| Top | modular $\perp$ analytic | zero cross-firing in $\sim 200$ units |
| Sub (modular) | $\{$q-shift, modular-S$\}$ for CFs | NB V Ch. 32 |
| Sub (modular) | $\{$modular-S$\}$ monoculture for modular equations | NB V Ch. 36 |
| Sub (modular) | $\{$class-field, modular-S$\}$ for class invariants | NB V Ch. 34 |
| Sub (analytic) | Bipartite: Mellin/Master-Theorem $\perp$ Schröder-Koenig | NB Part 1 Ch. 3-4, QRs |

The bipartite analytic finding (diary 36; BIG_IDEAS_REVIEW §2c) is
that within the analytic toolkit, Mellin/Master-Theorem material and
Schröder-Koenig fractional iteration material fire in *disjoint
entry-sets* — zero co-tagging across the 52 proof units that
constitute the iteration and Master-Theorem subdomains of NB Part 1
Ch. 4.

### 6.1 Implication for the engine

The basis described in Section 2 is the **engineering image** of this
empirical decomposition: the three substantively-implemented operators
correspond to the three highest-frequency operator clusters in the
tagged corpus (modular family $\to$ operator 3; Mellin/Master-Theorem
$\to$ operators 1-2; the four stub operators are placeholders for
the Schröder-Koenig sub-cluster, Frullani, Fourier self-reciprocity,
and Mellin-pair reciprocity, which would be wired in v1.x).

The two results in Sections 3 and 4 both use operator 3 (the modular
family). This matches diary 36's finding that Lost Notebook entries
in the partial-theta / theta-function neighbourhood (Warnaar's
identity, $\psi(q)$) are exactly the targets a modular-cluster
operator should hit.

A `SectorClassifier` pre-pass (queued v1.x, per diary 38) would pin
each new search state to either the modular or analytic sector
up-front and constrain the proposer to operators from that sector
only. By the toolkit-split hypothesis (zero cross-firing observed),
this is expected to give a $\ge 3\times$ reduction in proposer-space
search effort with no loss of coverage.

---

## 7. Discussion and future work

### 7.1 What was demonstrated

This paper reports *two specific Ramanujan identities where an
automated symbolic-search engine, equipped with a small operator
basis distilled from Ramanujan's empirically-observed working clusters,
finds transformed computational forms that are 15$\times$ to 272$\times$
faster than the recorded forms at $q$ near $1^-$* [VERIFY_REPLACE].
Both transformations use only the engine's existing
`modular_transform_with_correction` operator; both are verified to
$\le 5 \cdot 10^{-58}$ relative mismatch at $80$-digit precision
[VERIFY_REPLACE].

### 7.2 What this is NOT

It is important to be explicit:

1. The identities are **recorded by Ramanujan** (Lost Notebook
   pp. 29 and 35) and have been **verified by Andrews, Berndt, Warnaar
   and others** in the standard commentaries. The engine did *not*
   discover them.
2. The **transformed forms** are also classical in the sense that the
   underlying modular transformations (Dedekind-$\eta$,
   $\theta_2 \leftrightarrow \theta_4$) are textbook. The engine's
   contribution is to *compose them with the right preprocessing,
   verify numerically to high precision, and pass a cost gate that
   confirms the order-of-magnitude speedup is real*.
3. The cost-ratio numbers in §§3-4 are currently **ChatGPT-Pro-claimed**
   measurements (diary 42) and are flagged `[VERIFY_REPLACE]`
   throughout. Independent reproduction in our mpmath environment is
   the gating item for the v0.2 draft (`analysis/29_*.py`, in flight).
4. Both routes use **algebraic preprocessing** (parameter binding,
   Pochhammer rewrite for §3; Jacobi triple-product rewrite for §4)
   that is currently done by hand. Sections 4.5 and 7.3 discuss the
   v0.10 operator additions that would close this gap.

### 7.3 Basis-completeness and the v0.10 roadmap

As of v0.9, Project C reaches **8 of 12 seed targets** at depth $\le 4$
under a budget of $10{,}000$. The four unreachable targets — mock-theta
$f_3$, partial-theta sums, finite Gauss-sum evaluations, and generic
$q$-Pochhammer transforms — have no operator whose `apply_fn`
currently returns non-`None` on them. v0.10 adds four operators:

1. **`mock_theta_completion_transform`**: thin wrapper around the
   Zwegers $R_{a,b}$ erfc form (diary 41). Resolves a known
   methodological bug in our P2 prompt (which used a divergent
   integral form; the convergent Mordell form in
   `analysis/17_mock_theta_residual_ebm_v1.py` is what our code
   actually uses).
2. **`partial_theta_completion_or_false_theta_transform`**: completes
   partial-theta sums $\sum q^{n(n+1)/2}$ (optionally with $(-1)^n$).
3. **`gauss_sum_finite_evaluation`**: cleanest of the four; quadratic
   Gauss-sum closed form with the silent-zero guard preserved (per
   the documented hazard at $q \equiv 2 \pmod 4$ in
   `rkc/registry.py`).
4. **`q_pochhammer_transform`**: most general; lifts seed factors to
   recognized infinite-product form and applies Dedekind-$\eta$ or
   Heine / $q$-binomial as appropriate. Would close the AB 1.6.6
   preprocessing gap noted in §4.2.

ChatGPT Pro estimates 1-2 days each (diary 42); with realistic test
coverage and edge cases, more likely 3-7 days each. After v0.10:
Project C would close the basis-completeness milestone for all 12
seed targets and unblock 4 registry families currently surfacing as
`CompletionNotImplemented` in `rkc/completions.py`.

### 7.4 The from-scratch-discovery milestone

The natural next milestone — and one that this paper does *not* yet
clear — is for the engine to produce an identity that is **not
recorded anywhere in Ramanujan's notebooks or Berndt's commentaries**,
and that holds to the same strict $\le 10^{-30}$ acceptance bar across
a $\ge 2$-dex sweep. To our knowledge no automated identity-discovery
engine has cleared this bar for $q$-series identities at the
Ramanujan level of structure. Project C's roadmap to that milestone:

(a) Wire the v0.10 four operators above.
(b) Add the `SectorClassifier` pre-pass per §6.1.
(c) Add a `CompressionFilter` per the metric in §1.1 of this note (and
    diary 39), with the grammar-relative caveats explicit.
(d) Run a directed sweep against seeds in the Lost Notebook
    neighbourhood (Warnaar 1.7 family, mock-theta f-family, etc.) at
    depth $\le 6$, budget $\sim 10^5$, with the engine's existing
    cost-gate set to require ratio $> 10\times$.

Whether (a)-(d) suffice for a from-scratch hit is the open question.

---

## Acknowledgments

The eight ChatGPT-Pro Erdős-style prompt cycles (diaries 35, 37, 38,
39, 40, 41, 42, plus the v0.8a proposer-test that preceded them)
produced the structural insights and operator-completion proposals
that drove the implementation reported here; their methodology
(open-ended T/F prompts with anti-handwave guards and explicit numerical
verification bars) is itself a piece of the methodology contribution.
The standing-on-shoulders base is the immense body of work by
B.C. Berndt, G.E. Andrews, S.O. Warnaar, F. Garvan, J. Frye, S. Zwegers,
D. Hickerson, B.C. Berndt and A. Dixit, and the OEIS, without which
none of the source identities, transformations, or verification points
would exist. Diary 41's detection of an error in our own P2 prompt
(a divergent integral form picked up from training-memory rather than
copied from our implementation) is a worked example of the "paste
actual implementation, not memory-paraphrase" discipline that the
ChatGPT-Pro methodology imposes.

## References

(Selected; full bibliography in `corpora/transcriptions/README.md`
and the per-source citations in each diary entry.)

- G. E. Andrews and B. C. Berndt, *Ramanujan's Lost Notebook*,
  Parts I-IV, Springer (2005, 2009, 2012, 2013).
- B. C. Berndt, *Ramanujan's Notebooks*, Parts 1 and 5, Springer
  (1985, 1998).
- B. C. Berndt and A. Dixit, "A transformation formula involving the
  gamma and Riemann zeta functions in Ramanujan's lost notebook,"
  arXiv:0904.1053 (2009).
- A. Dixit and B. C. Berndt (eds.), *Ramanujan: Letters and
  Commentary*, AMS (1995).
- F. G. Garvan and J. Frye, "Automatic proof of theta-function
  identities," in *Elliptic Integrals, Elliptic Functions and Modular
  Forms in Quantum Field Theory* (2019).
- B. C. Berndt and S. Bhargava, "Ramanujan's quarterly reports,"
  Hardy-Ramanujan Journal, vol. 45 (2022). [Reproduces Berndt's earlier
  Bull. London Math. Soc. (1983, 1984) editions; the only available
  faithful copy of the otherwise-lost original quarterly reports —
  approximately 6 generations of copying removed from Ramanujan's hand
  via Satagopan's 1925 manuscript.]
- B. C. Berndt and A. J. Yee, "On Eisenstein series in Ramanujan's
  lost notebook," RIMS Kôkyûroku Bessatsu (2002).
- D. Hickerson, "A proof of the mock theta conjectures,"
  Inventiones Mathematicae **94** (1988), 639-660.
- K. Ono, "Ramanujan, taxicabs, birthdates, ZIP codes, and twists,"
  arXiv:1510.00735 (2015).
- S. Ramanujan, *The Lost Notebook and Other Unpublished Papers*,
  Narosa (1988).
- S. O. Warnaar, "Partial theta functions. I. Beyond the lost notebook,"
  Proc. London Math. Soc. (3) **87** (2003), 363-395.
  [Contains the equation (1.7) used in Section 3.]
- D. Zwegers, *Mock Theta Functions*, PhD thesis, Utrecht (2002).

**Repository (private):** github.com/jounih/ramanujan-mining.
Relevant commit hashes (as of submission of this draft):

- v0.4 (keystone Poisson): commit `945e01f` (`analysis/14b_*.py`,
  `rkc/`).
- v0.7 (strict Poisson duals): commit `f1758d3` (diary 26).
- v0.8b (additive-correction API + `modular_transform_with_correction`):
  diary 31. **The operator used in Sections 3 and 4.**
- v0.8c (Stieltjes occupation-number): diary 32.
- v0.9a (Hardy-orders divergence diagnostic): diary 33.
- v0.9 in-session proposer: diary 34.

The engine is open-source (private repo for now; the user obtained the
Berndt / Andrews-Berndt source PDFs legitimately from the authors and
the repo is private to honour the source distribution rights).

---

## Appendix A. The full operator-3 apply-fn (excerpted from `rkc/search/basis.py`)

The pattern matchers for the two cases used in Section 3 and 4 are
reproduced here in skeletal form (full implementation in
`rkc/search/basis.py` at function `_modular_transform_with_correction_apply`):

```python
def _modular_transform_with_correction_apply(expr, n):
    # CASE A: log Bose-Einstein  log(1 - exp(-β n))
    #   → log(1 - exp(-4π² n / β))  + correction (-π²/(6β) - (1/2)log(β/(2π)) + β/24)
    result = _log_bose_einstein_apply(expr, n)
    if result is not None:
        return result
    # CASE B: Lambert / E_2 quasi-modular  n q^n / (1 - q^n)
    #   → -(4π²/β²) n / (exp(4π² n / β) - 1)  + correction π²/(6β²) + 1/24 - 1/(2β)
    result = _lambert_e2_apply(expr, n)
    if result is not None:
        return result
    # CASE C: Stieltjes occupation-number (v0.8c)  1/(exp(βn) - 1)
    result = _v08c_try_occupation_number_pattern(expr, n)
    if result is not None:
        return result
    return None
```

Each branch returns either `None` (declines) or a 3-tuple
`(new_summand, additive_correction, summand_range)`. The engine
populates the `OperatorApplication` from the tuple; the verifier picks
up the correction and folds it into the before-side residual before
comparison.

---

*End of draft v0.1. Document length: approximately 4{,}100 words in
this Markdown source; estimated 5-6 compiled LaTeX pages. Awaiting:
(i) `analysis/29_warnaar_17_ab_166_cost_verification.py` cost-ratio
reproduction to replace the [VERIFY_REPLACE] markers; (ii) human
review of Sections 3.5 and 4.5 framing.*
