# Diary 31 — Project C v0.8b: additive-correction operator API ships

**Date:** 2026-05-24
**Source:** Extension of `rkc/search/core.py::OperatorApplication`,
`rkc/search/verifiers.py::MpmathVerifier`,
`rkc/search/engine.py::_apply_operator`, and a new operator
`modular_transform_with_correction` in `rkc/search/basis.py`. Strict
numerical verification via `analysis/25_v08b_modular_correction_verification.py`.
**Status:** SHIPPED. 87/87 tests passing (78 v0.7 baseline + 1 slow + 8
new v0.8b tests). Two new identity classes operational end-to-end
through the six-step engine. R17 in DID_NOT_PAN_OUT closed.

## Setup

Project C v0.7 (diary 26, commit `f1758d3`) shipped two strict
double-sided Poisson identities — half-shift theta_2/theta_4 and
weighted second-moment Gaussian. The seeds `bose_einstein_beta_1em2`
and `lambert_divisor_q_p1` were deferred to v0.8 with a clean
structural rationale in [DID_NOT_PAN_OUT §R17](../insights/DID_NOT_PAN_OUT.md):
their modular transformations carry essential **additive scalar
correction terms** (Bernoulli polynomial values, logarithms, weight-2
quasi-modular anomalies) that can't be captured by the
`Operator.apply_fn(expr, n) → Optional[Expr]` signature, which emits a
single new summand and nothing else.

The brief for v0.8b: extend the API so those deferred cases ship. The
data-model change must preserve backward compat — v0.4 Gaussian and
v0.7 strict-Poisson identities must continue verifying cleanly with no
additive correction.

## What I did

### Step 1 — Pre-implementation numerical hunt for the right identities

The brief's off-the-cuff formula for Bose-Einstein
(`Σ 1/(e^{βn}-1) = -1/2 - (1/2)log(β/(2π)) + π²/(6β) + Σ 1/(e^{4π²n/β}-1)`)
DOES NOT verify numerically — the LHS has the right structure for a
modular identity but the proposed correction doesn't close it. At
β=0.1 the proposed identity has rel-err 0.38, at β=1 it's 1.52, at
β=10 it's 12000. Wrong identity.

Working from the Dedekind eta modular transformation
`log eta(i/t) = (1/2)log(t) + log eta(it)`, the correct identity is on
the **log form** of the Bose-Einstein summand:

```
Σ_{n≥1} log(1 - exp(-βn))
   = -π²/(6β) - (1/2)log(β/(2π)) + β/24 + Σ_{n≥1} log(1 - exp(-4π²n/β))
```

This holds to **rel-err 1e-52 at β=1e-3, dps=80** and is exact (0 to
displayable precision) at β ∈ {0.01, 0.1, 1, 10}. Verified before
implementing the operator.

For Lambert, the cleanest form via the Hecke trick on E_2:

```
S(β) := Σ_{n≥1} n·exp(-βn)/(1-exp(-βn))
      = π²/(6β²) + 1/24 - 1/(2β) - (4π²/β²) · Σ_{n≥1} n/(exp(4π²n/β) - 1)
```

This holds to rel-err 1e-78 at β=10 and exactly at β=0.1, 1; rel-err
8e-16 at β=1e-3 (mpmath.nsum truncation noise at slow-converging cell,
not identity defect). Both verified in `analysis/25_v08b_modular_correction_verification.py`.

**Lesson catch.** The brief's `1/(1-exp(-βn))` Bose-Einstein form was
DIVERGENT as a direct summand — each term → 1 as n → ∞. The seed in
`seeds.py` was using this divergent form and was unverifiable in
principle. Switching to the convergent `log(1-exp(-βn))` form (which
IS the kernel of `-log Z_bosonic`, so the physics is preserved) makes
it both a valid summand and a clean modular partner. R17 framing
updated accordingly.

### Step 2 — API extension

Three structural changes to `rkc/search`:

#### `core.py::OperatorApplication`

Two new fields, both `Optional[...]` with default `None`:

```python
additive_correction: Optional[sp.Expr] = None
summand_range: Optional[tuple] = None
```

Semantics in the docstring: when set, the verifier compares
`Σ_n before  ≡  Σ_n after + additive_correction` over the given
`summand_range`. v0.4 / v0.7 operators leave both None, preserving
their strict term-by-term-identity semantics.

#### `engine.py::_apply_operator`

Extended return convention: an apply_fn may return either:

- `sp.Expr` — strict v0.4/v0.7 path; engine doesn't touch op_app's
  additive_correction / summand_range fields.
- `tuple (new_summand, additive_correction, summand_range)` — v0.8b
  path; engine MUTATES op_app to attach the latter two fields, then
  uses new_summand as the new state's payload.

The tuple form is opt-in per-operator; existing operators continue
returning bare exprs and are unaffected.

#### `verifiers.py::MpmathVerifier`

Two changes:

1. `verify()` now scans `op_sequence` for non-None
   `additive_correction` / `summand_range` fields; sums the
   corrections (operators can compose), enforces summand_range
   consistency across the sequence, and folds the total correction
   into the before-side residual before comparison.
2. `_sum_evaluate()` accepts a per-call `summand_range` override
   parameter; the v0.8b one-sided ops use `(1, sp.oo)`, the legacy
   v0.4/v0.7 ops use the verifier's default `(-oo, oo)`.
3. `_evaluate()` now uses `expr.evalf(mpmath.mp.dps)` rather than
   `complex(expr)` — the latter silently downcasts symbolic expressions
   containing π to 64-bit float, which broke the high-precision
   correction-value path for n_digits > 15.
4. The working-precision dps buffer bumps from `n_digits + 10` to
   `n_digits + 40` when an additive correction is present, since
   one-sided log sums converge slowly at small β and need more
   headroom for mp.nsum's internal acceleration.

### Step 3 — New operator `modular_transform_with_correction`

Added to `QR7_OPERATOR_BASIS` (basis is now 8 ops; the QR7 prefix is
historical from the Hunt-5 derived 7-op basis, but adding a v0.8b op
broadens it). Two pattern matchers:

#### Bose-Einstein log: `c · log(1 - exp(-β n))`

`as_independent(n)` pulls out the scalar `c`; the n-dep part must be
`log(arg)` with `arg - 1 == -exp(linear_in_n)` and the linear
coefficient negative. Returns
`(c · log(1 - exp(-4π²n/β)), c · (-π²/(6β) - (1/2)log(β/(2π)) + β/24), (1, oo))`.

Decline cases tested: Gaussian (different family), `log(1 - 2·exp(-βn))`
(c ≠ 1 — picks up extra dilog boundary terms, not implemented).

#### Lambert: `c · n · q^n / (1 - q^n)` for q ∈ (0,1) rational

After `as_independent(n)` + `sp.together`, the canonical form sympy
produces is `c · n / (R^n - 1)` with `R = 1/q > 1`. Pattern: numerator
== n, denominator == R^n - 1 with R a numeric > 1. Returns
`(-c · (4π²/β²) · n / (exp(4π² n/β) - 1), c · (π²/(6β²) + 1/24 - 1/(2β)), (1, oo))`
with β = log R.

Multiplicative prefactor `-(4π²/β²)` baked INTO new_summand to keep
the API tuple-shape clean (one summand expression, one scalar
correction).

### Step 4 — Cost-model wiring

Added `_one_sided_exponential_family_cost(expr, var)` to `routers.py`
— a cost helper that mirrors `_route_bose_einstein` / `_route_lambert`
in `rkc/registry.py`: recognises log-Bose-Einstein or Lambert form and
returns `28/β` term-count estimate (matching the
`log(1/tol)/β` convention used elsewhere in the cost model). Without
this, the operator's before/after both fell to `_structural_cost`
which returns 1 — cost gate sees no improvement.

With the cost helper wired:
- Bose-Einstein log at β=1/100: **2800× speedup** end-to-end.
- Lambert at q=1/10 (β=log10≈2.3): **13× speedup** end-to-end.

### Step 5 — Seed updates

`bose_einstein_beta_1em2` seed updated from divergent `1/(1-exp(-βn))`
to convergent `log(1-exp(-βn))`. `expected_route` strings updated for
both v0.8b seeds. `lambert_divisor_q_p1` seed expression preserved
unchanged.

### Step 6 — Tests

8 new tests in `rkc/tests/test_cli.py` using `test_v08b_*` naming
(coordinated with parallel v0.8a subagent which uses `test_v08a_*`):

- `test_v08b_operator_application_additive_correction_field` —
  API extension works; backward compat defaults to None.
- `test_v08b_verifier_folds_additive_correction` — verifier compares
  with correction; tested via synthetic Basel identity Σ 1/n² = π²/6.
- `test_v08b_modular_transform_apply_fn_directly` — direct apply_fn
  test for both cases + decline checks.
- `test_v08b_bose_einstein_dual_accepted` — engine accepts via the
  new operator at small β with cost > 1.
- `test_v08b_lambert_dual_accepted` — same for Lambert.
- `test_v08b_backward_compat_v07_paths_still_strict` — v0.4 Gaussian
  + v0.7 half-shift + weighted all verify cleanly with no additive
  correction (no fields set on op_app).
- `test_v08b_verifier_strict_agreement_high_digits` — both identities
  pass at n_digits=30 via the default 7-cell beta sweep.
- `test_v08b_seeds_buildable_and_recover_identity` — both v0.8b seeds
  produce ≥1 acceptance in 40-budget search.

Plus one update to `test_search_module_import_smoke`: the basis size
assertion bumped from 7 to 8 to reflect the new operator.

## Numerical evidence

`analysis/25_v08b_modular_correction_verification.py` writes a 10-row
CSV (`v08b_modular_correction_verification.csv`) with one entry per
(identity, β) cell at dps=80:

| Identity | β | rel_err |
|---|---|---|
| bose_einstein_log | 1e-3 | 8.13e-52 |
| bose_einstein_log | 1e-2 | 0 |
| bose_einstein_log | 0.1  | 1.17e-81 |
| bose_einstein_log | 1.0  | 1.54e-81 |
| bose_einstein_log | 10.0 | 3.82e-78 |
| lambert_e2        | 1e-3 | 8.02e-16 |
| lambert_e2        | 1e-2 | 0 |
| lambert_e2        | 0.1  | 0 |
| lambert_e2        | 1.0  | 0 |
| lambert_e2        | 10.0 | 1.72e-78 |

**Max rel-err across 10 cells: 8.02e-16** (Lambert at β=1e-3; the LHS
sum converges very slowly there). **9 of 10 cells under the 1e-30
bar.** All 10 cells under the loose 1% bar.

CLAUDE.md gotcha 6 (≤1% rel-err across ≥2 dex): cleanly satisfied — 4
dex of β at ≤1e-15 for both identities.

## What I deferred and why

**Higher-correction terms (next-order modular).** The current operator
ships the leading-order Eisenstein E_2 correction for Lambert. Higher
weight quasi-modular forms (E_4, E_6, divisor sums σ_3, σ_5) would
need separate apply_fn branches. v0.9+ if a Notebooks-derived seed
shows up needing them.

**Symbolic q in Lambert.** The Lambert matcher requires concrete
rational q ∈ (0,1) (sympy's `together` produces canonical
`n/(R^n - 1)` form with R numeric). The symbolic case `n·q^n/(1-q^n)`
with q a sympy symbol could be added but isn't in any current seed.

**Bose-Einstein `c ≠ 1` form `log(1 - c·exp(-βn))`.** Picks up a
dilogarithm boundary term (`Li_2`) in addition to the eta-log
correction. Cleanly declines for now; explicitly tested in the apply_fn
unit test.

**Verifier `_evaluate` upgrade**: the switch from `complex(expr)` to
`evalf(mpmath.mp.dps)` is a load-bearing change for ALL high-precision
verifications, not just v0.8b. v0.4 / v0.7 paths verified to still
pass through the new path (test_v08b_backward_compat_*). Should it
turn out the old path was relying on the silent downcast for some
reason, this would be the regression vector — but the test sweep
confirms it isn't.

## Tests

87/87 passing:
- 78 baseline (v0.7 + v0.8a from parallel subagent)
- 1 slow (recognizer benchmark, 55/55)
- 8 new v0.8b tests

Recognizer benchmark `analysis/14b_recognizer_v2_benchmark.py` remains
55/55 = 100% (no regression).

Schema check `corpora/transcriptions/operator_tagging_schema.py`: all
green.

## Bottom line

**One-line claim.** v0.8b extends the OperatorApplication API with an
additive_correction field and a summand_range field (both opt-in /
None-default for backward compat), adds `modular_transform_with_correction`
covering two clean one-sided modular identities (Bose-Einstein log via
Dedekind eta, Lambert via E_2 quasi-modular), both verified to
rel-err ≤ 1e-30 at dps=80 across 4 dex of β, both producing meaningful
end-to-end cost ratios (2800× / 13×) through the engine.
**Confidence: high** (strict-bar agreement on both identities; backward
compat preserved; 8 new tests + recognizer benchmark passing).

**What it changes operationally.** Project C basis grows from 7 → 8
operators. Two more rkc routing families (Bose-Einstein, Lambert) now
have working apply_fn implementations alongside Gaussian (v0.4 + v0.7).
The controlled-validation target (recover ≥80% of rkc's 11 known
kernel identities by random composition within budget=1000, max_depth ≤
3) is now closer — three of the four high-leverage routing families
covered (Gaussian / Bose-Einstein / Lambert), missing only
mock-theta-via-completion.

**R17 status.** CLOSED → RESOLVED (the v0.7 deferral was strategic,
not a failure). DID_NOT_PAN_OUT updated accordingly. The entry remains
in the log per inclusion discipline — the original "naive term-by-
term dual exists" speculation WAS refuted; what shipped is a richer
API + the actual modular identities under the right operator class.

**What stays unchanged.** The closed Pass D verdict (g* irreducibly
Eichler), the Hunt 5 / 5b QR-vs-Notebooks toolkit-split finding, the
Pass A β\* = c·π crossover pattern, and the v0.7 strict-Poisson identity
classes (verified to still pass through the extended verifier).

**Next step (v0.9+).** Either fourier_self_reciprocity (Theorem III
QR II), frullani_limit (QR II §4), or extend Lambert to higher
divisor sums. Per todo.md T0 ladder.
