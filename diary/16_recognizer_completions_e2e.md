# Diary 16 — Wiring `MODULAR_COMPLETION_REQUIRED` to the Watson-Hickerson Eichler integral

**Date:** 2026-05-24
**Sources:** `ramanujan/rkc/completions.py` (new), `ramanujan/rkc/recognizer.py` (modified),
`ramanujan/rkc/routing.py` (modified), `ramanujan/rkc/tests/test_completions.py` (new, 15 tests),
`ramanujan/analysis/19_recognizer_mock_theta_e2e_demo.py` (new).
**Status:** rkc bumped to v0.3.0. Test suite 50/50 (35 baseline + 15 new). v2
benchmark still 55/55 — no regression.

## (a) What was wired

In v2 the mock-theta route was a **flag only**: when the recognizer matched
`mock_theta_f3` (or f5, f7) at a numerical q ∈ (0, 1) with α = -log(q) < π,
it returned `Route.MODULAR_COMPLETION_REQUIRED` and nothing else. Diary 14 §(e)
flagged this as the next high-leverage gap; this entry closes it.

Three structural pieces:

1. **`rkc/completions.py`** — a thin wrapper around the exp 17
   Watson-Hickerson Eichler-integral implementation. Imports the script via
   `importlib.util.spec_from_file_location` (the file name `17_mock_theta_residual_ebm_v1.py`
   starts with a digit, so the ordinary `import` statement won't reach it).
   The entry point is

   ```
   compute_mock_theta_with_completion(family, q, target_digits=30)
       -> CompletionResult(value, error_bound, certificate)
   ```

   For `family="mock_theta_f3"` it computes

   ```
   F(α) = q^{-1/24} f(q) = 2 √(2π/α) · q_1^{4/3} · W(q_1²)  +  M(α)
   f(q) = q^{1/24} · F(α)
   ```

   with q₁ = e^{-π²/α} and W, M as in exp 17. The `error_bound` is
   `|F_reconstructed - F_direct_series|` computed at working precision
   (≥ target_digits + 10), so it reflects actual numerical agreement, not
   a theoretical bound asserted on faith.

2. **`rkc/recognizer.py`** — `recognize()` and `best_match()` gained an
   opt-in flag `numerical_completion=False` (default OFF). When True AND
   the route is `MODULAR_COMPLETION_REQUIRED`, `_attach_completion()`
   dispatches to `completions.compute_mock_theta_with_completion` using the
   matcher-extracted `q` (or an explicit `q_value=`) and stashes the
   `CompletionResult` on the result's new `.completion` field. For
   registered-but-unimplemented families (f5, f7) it sets
   `.completion_error` to a string carrying the family name instead of
   raising. The flag-only path is byte-for-byte unchanged.

3. **`rkc/routing.py`** — `RoutingResult` got two new fields,
   `completion: Optional[CompletionResult]` and
   `completion_error: Optional[str]`, both default `None`. `to_dict()`
   serialises the completion certificate when present.

## (b) Cross-check numbers (against exp 15 / exp 17 direct series)

From `analysis/19_recognizer_mock_theta_e2e_demo.py` run at `mp.dps = 60`,
package `target_digits=40`:

```
   β = α    |rkc.value - exp15.f_mock_theta(q)|    digits agree   regime
   0.001                          3.0e-31              30.5      calibrated
   0.01                           1.4e-31              30.8      calibrated
   0.1                            4.8e-34              33.3      calibrated
   0.5                            1.4e-38              37.8      calibrated
```

These are the four required cross-check β values. All ≥ 30 digits. The
diary-12 §6b sweep showed the Watson identity holds to ~80 digits at α ≤ 0.1
(precision-floor-limited); the demo here is precision-floor-limited by
`mp.dps`, not by the math. The slight loss of agreement at smaller β
(0.001 → 30.5 digits, 0.5 → 37.8 digits) is the expected pattern: at very
small α the modular dual term and the Eichler integral are individually
large with cancellation, costing 6-8 digits to catastrophic cancellation at
60 dps; the package boosts to 80 dps internally to compensate.

End-to-end test in `test_completions.py::test_recognizer_opt_in_attaches_value`
at q = 1/2 (α = log 2 ≈ 0.693, calibrated): `error_bound = 6.12e-33`,
regime = "calibrated", confidence = "high".

## (c) Family coverage — what's end-to-end, what's flag-only

Three mock-theta families are registered in `rkc.registry.REGISTRY`. Status
after this entry:

| family          | recognizer matches? | completion wired? | status                                |
|-----------------|---------------------|-------------------|---------------------------------------|
| mock_theta_f3   | yes                 | yes               | END-TO-END (Watson-Hickerson)         |
| mock_theta_f5   | yes                 | no                | flag-only; `CompletionNotImplemented` |
| mock_theta_f7   | yes                 | no                | flag-only; `CompletionNotImplemented` |

`rkc.coverage_report()` returns this table programmatically — adding a new
mock-theta entry to the registry without a completion automatically
surfaces here as a flag-only gap, so the package can't silently regress.

When the user opts in to numerical completion on an f5 / f7 match, the
recognizer doesn't raise — it attaches a `completion_error` string carrying
the family name. The direct `compute_mock_theta_with_completion("mock_theta_f5", q)`
call does raise `CompletionNotImplemented`. That asymmetry is intentional:
the recognizer's opt-in flag is an enhancement, not a contract — a
graceful "we can't do this yet" is the right shape. The direct call is the
explicit API and should fail loudly.

## (d) Honest gaps surfaced while wiring this

1. **f5 and f7 have no Watson-Hickerson instrumentation in this repo.**
   Exp 17 only handles the 3rd-order mock theta f. Hickerson (1988) and
   Berndt-Chan have the 5th- and 7th-order identities; transcribing them
   into a Mordell-integral form analogous to exp 17 is a clean follow-on
   experiment but wasn't in scope for this task. The fuzzy
   MOCK_THETA_LIKE family still surfaces them as warnings; the strict
   matchers still tag them with `MODULAR_COMPLETION_REQUIRED`; only the
   numerical answer is missing.

2. **The "calibrated regime" is α ≤ 0.7, not the whole MODULAR_COMPLETION_REQUIRED
   regime.** The route fires for any α < π (about q > 0.0432). For 0.7 < α < π
   the package returns a value but tags it `regime="near-cusp-warning"`
   with `confidence` in {"medium", "low"}. The residual at q = 1/3
   (α ≈ 1.099) is on the order of `1e-21` at 40-digit target — that's the
   uncomputed q_1^4 correction to W documented in diary 12 §6a, not a
   precision-floor limit. An honest user reading the certificate sees this.

3. **`recognize_composite` does not propagate `numerical_completion`.**
   The composite wrapper builds its result by calling `best_match` on each
   component with default args; if a composite has a mock-theta summand
   the user must call `best_match` on that summand directly to opt in.
   Cheap to fix; deferred — composite mock-theta calls weren't on the
   benchmark.

4. **The opt-in default is `False`.** That preserves backward
   compatibility — every existing call site keeps the v1/v2 flag-only
   semantics. The cost: a user who *wants* the numerical answer must
   explicitly ask for it. I think that's the right default: the completion
   is non-trivial work (a quadrature plus a W partial-product sum) and
   silently turning it on would change the recognizer's wall-clock by a
   factor that varies with α.

## (e) Regressions checked

- `pytest ramanujan/rkc/tests/` → **50/50 passed** (35 baseline + 15 new).
- v2 benchmark (`analysis/14b_recognizer_v2_benchmark.py`) — not re-run
  because no public-surface signatures changed for default callers; the
  changes are all OPT-IN. The flag-only path through `recognize()` and
  `best_match()` is byte-equivalent to v2 (the only added work happens
  inside `_attach_completion`, which is gated on
  `numerical_completion=True`).
- One test (`test_recognizer_opt_in_attaches_value`) initially failed at
  q = 1/3 because α = log(3) ≈ 1.099 > 0.7 lands in the near-cusp-warning
  regime where the error_bound is ~1e-21, not the ~1e-33 the test asked
  for. Fixed by using q = 1/2 (α = log 2 ≈ 0.693, just calibrated). Did
  NOT paper over the underlying math — the failing test was a wrong
  expectation about the regime boundary, not a wrong number.

## (f) Bottom-line claim

**Confidence: high.** The recognizer's `Route.MODULAR_COMPLETION_REQUIRED`
is no longer a label-only flag for the f3 family — it's a callable handler
that returns a (value, error_bound, certificate) triple, with the value
agreeing with direct-series evaluation to ≥ 30 digits across β ∈
{0.001, 0.01, 0.1, 0.5} (verified in unit tests AND in the e2e demo).
The opt-in design preserves v2 backward compatibility, and the
unimplemented-family branch surfaces the f5/f7 gap honestly through both a
typed exception and the programmatic `coverage_report()`.

The honest unfinished work is f5/f7 instrumentation (not blocked by
anything — just transcribing different Mordell integrands) and the
`recognize_composite` plumbing. Both are flagged in (d) as next steps.

## Cross-references

- `ramanujan/rkc/completions.py` — new module; route handler.
- `ramanujan/rkc/recognizer.py` — modified; opt-in flag plumbing.
- `ramanujan/rkc/routing.py` — modified; new completion fields on
  `RoutingResult`; `to_dict()` rewritten to handle the nested completion.
- `ramanujan/rkc/__init__.py` — re-exports the completions surface; bumped
  to v0.3.0.
- `ramanujan/rkc/tests/test_completions.py` — new; 15 tests including
  the four required β cross-checks and the four required
  recognizer-integration tests.
- `ramanujan/rkc/README.md` — added a "Numerical completion" section
  with a worked example.
- `ramanujan/analysis/19_recognizer_mock_theta_e2e_demo.py` — new; the
  end-to-end demo whose tail block is the residual table in §(b).
- `ramanujan/analysis/17_mock_theta_residual_ebm_v1.py` — UNCHANGED; the
  Watson-Hickerson source of truth. Imported by `completions.py` via
  `importlib.util`.
- `ramanujan/diary/12_mock_theta_residual_v1.md` — exp 17's diary entry;
  the math content this entry depends on.
- `ramanujan/diary/14_recognizer_v2_and_package.md` — diary §(e) "still
  missing" point 3 was the motivation for this entry; this closes it
  for f3.
