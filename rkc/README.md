# rkc — Ramanujan Kernel Compiler / Recognizer

A standalone package that takes a symbolic AST for a sum/product and
routes it to **direct evaluation** vs a **closed-form / dual
representation**, using a registry of canonical kernels (theta, mock
theta, Lambert, Eisenstein, partial theta, q-Pochhammer, Dirichlet L,
Gauss sum).

This is v2 of the recognizer. v1 lives at
`ramanujan/analysis/13_recognizer_v1.py` and is kept untouched as a
stable reference. v2 closes the five documented gaps from v1's diary
(scalar-coefficient stripping, fuzzy second-pass matcher,
per-component cost rollup for composites, per-term complexity tracking,
Gauss-sum gcd reachability).

## Example

```python
import sympy as sp
from rkc import best_match, recognize_composite, Route

n = sp.symbols("n", integer=True, nonnegative=True)

# Plain kernel — strict match.
bm = best_match(sp.exp(-sp.Rational(1, 10) * n ** 2), n)
print(bm.kernel, bm.route, bm.total_cost)
# -> gaussian_quadratic Route.DUAL <a float>

# Scalar coefficient is now peeled (v1 missed this).
bm = best_match(3 * sp.exp(-sp.Rational(1, 10) * n ** 2), n)
print(bm.kernel, bm.scalar_coefficient)
# -> gaussian_quadratic 3

# Shifted theta — strict match REJECTS, fuzzy second pass FIRES.
bm = best_match(sp.exp(-sp.Rational(1, 5) * n ** 2 - sp.Rational(1, 10) * n),
                n, accept_fuzzy=True)
print(bm.kernel, bm.route, bm.confidence)
# -> theta-like Route.FUZZY 0.6

# Composite — sum of two kernels, per-component cost rollup.
expr = sp.exp(-sp.Rational(1, 4) * n ** 2) + 1 / (1 - sp.exp(-sp.Rational(1, 4) * n))
cm = recognize_composite(expr, n)
print(cm.kernel, cm.total_cost, len(cm.components))
# -> composite[sum](gaussian_quadratic,bose_einstein_geometric) <sum> 2
```

## Kernel registry

Eleven entries in v2 (same set as v1; v2's gains are structural):

| name                       | family            | route on `q→1`               | degeneracy guard          |
|----------------------------|-------------------|------------------------------|---------------------------|
| `gaussian_quadratic`       | theta-like        | DUAL (theta-S)               | —                         |
| `bose_einstein_geometric`  | lambert-like      | DUAL (Dedekind-eta)          | —                         |
| `lambert_divisor`          | lambert-like      | DUAL (Eisenstein)            | `q ∈ (0,1)`               |
| `mock_theta_f3`            | mock-theta-like   | MODULAR_COMPLETION_REQUIRED  | `q ∈ (0,1)`               |
| `mock_theta_f5`            | mock-theta-like   | MODULAR_COMPLETION_REQUIRED  | `q ∈ (0,1)`               |
| `mock_theta_f7`            | mock-theta-like   | MODULAR_COMPLETION_REQUIRED  | `q ∈ (0,1)`               |
| `partial_theta`            | partial-theta-like| DIRECT                       | `q ∈ (0,1)`               |
| `q_pochhammer_infty`       | pochhammer-like   | DIRECT                       | `a≠1`, `q ∈ (0,1)`        |
| `eisenstein_E2k`           | eisenstein-like   | DUAL when `q→1`              | even weight, `q ∈ (0,1)`  |
| `dirichlet_L`              | (n/a)             | DUAL (functional eqn)        | —                         |
| `gauss_sum`                | gauss-sum-like    | DIRECT, O(q)                 | **`q ≡ 2 (mod 4)`**       |

Three fuzzy fallback families (returned with `route=Route.FUZZY` when no
strict matcher fires):

| family               | catches                                                   | confidence |
|----------------------|-----------------------------------------------------------|-----------:|
| `theta-like`         | `q^(n^2 + linear n + ...)` (shifted theta)                | 0.60       |
| `mock-theta-like`    | mock-theta core × extra factor (e.g. `f_3(q) * cos n`)    | 0.50       |
| `lambert-like`       | `q^(an) / (1 - q^(bn))` with `a ≠ 1` or `b ≠ 1`          | 0.55       |

## Silent-zero hazard (§A4)

Gauss sum `G(p, q) = Σ_{n=0..q-1} exp(2π i p n² / q)` evaluates to
**zero identically** when `q ≡ 2 (mod 4)`. A naive recognizer would
report a happy `DIRECT, cost=q`. The rkc registry has a per-kernel
`degeneracy_check` that fires BEFORE the cost predictor; for Gauss
sums it returns the route `DEGENERATE` with reason string referencing
§A4. The unit tests cover this for q ∈ {6, 10, 14}.

A subtler hazard: sympy auto-reduces `2*n²/6 → n²/3` before the matcher
sees it, hiding any gcd(p, q) > 1 degeneracy. v2's
`recognize_with_raw_string` takes the raw expression source as a string,
extracts (p_raw, q_raw) BEFORE sympify reduces them, and threads that
through to the Gauss-sum degeneracy check as `raw_pq`. This is what
makes the gcd branch actually reachable.

## Routing semantics

Five route states:

  - `DIRECT` — converges fast as written
  - `DUAL` — closed-form / modular dual exists and is cheaper
  - `MODULAR_COMPLETION_REQUIRED` — needs Zwegers / non-holomorphic Eichler
    completion (mock theta near the cusp)
  - `DEGENERATE` — the answer is a trivial value (zero, infinity); do NOT
    report a numerical recommendation
  - `FUZZY` — soft match, operator should inspect (v2-new)

## Per-term cost tracking (§A7)

`bits-per-term` lies about wall-clock when per-term cost varies wildly
(HRR Dedekind sums at dps=372 vs pentagonal big-int adds). Each
registry entry carries a `per_term_cost(params, target_precision)`
function returning approximate mpmath / big-int ops per term, and the
result reports `total_cost = num_terms * per_term_cost` so routing
decisions can be driven by actual estimated work.

## Numerical completion (`Route.MODULAR_COMPLETION_REQUIRED`)

In v2 the mock-theta route was a flag only. v0.3 wires it through to
the Watson-Hickerson Eichler-integral pipeline from
`ramanujan/analysis/17_mock_theta_residual_ebm_v1.py`, so when the user
opts in the recognizer returns a numerical value with a rigorous
bias-correction certificate. Default behavior (flag-only) is unchanged.

```python
import sympy as sp
from rkc import best_match
n, k = sp.symbols("n k", integer=True, nonnegative=True)
q = sp.Rational(1, 2)
f3 = q ** (n ** 2) / sp.Product((1 + q ** k) ** 2, (k, 1, n))
bm = best_match(f3, n, numerical_completion=True, target_digits=35)
value, error_bound, cert = bm.completion   # tuple-unpack the CompletionResult
print(bm.route, value, error_bound, cert.regime)
# -> Route.MODULAR_COMPLETION_REQUIRED <f(1/2) to 35 digits> 6e-33 calibrated
```

Coverage in this run: only `mock_theta_f3` is end-to-end (the Watson
identity is calibrated to ≥30 digits for α = -log(q) ≤ 0.7). The
registered `mock_theta_f5` and `mock_theta_f7` families remain flag-only;
calling the completion path on them raises (or attaches) a
`CompletionNotImplemented` with the family name. See `coverage_report()`.

## Tests

```
$ source ../.venv/bin/activate
$ python -m pytest ramanujan/rkc/tests/
```

Covers every kernel family plus every degeneracy branch, plus the
completion route handler (cross-check vs analysis/17 at four β values,
backward-compat flag-only behavior, unimplemented-family exception).
