# Diary 33 — Project C v0.9-hardy: hardy_orders_of_infinity ships as divergence diagnostic

**Date:** 2026-05-24
**Source:** Implementation of `_hardy_orders_apply` in
`rkc/search/basis.py` (previously a stub returning None since v0.3),
new `ConvergenceClass` enum + top-level `SearchState.convergence_class`
field in `rkc/search/core.py`, engine 2-tuple return convention
extension in `rkc/search/engine.py`, JsonlRegistry persistence in
`rkc/search/registries.py`. 5 new `test_v09a_*` tests.
**Status:** SHIPPED. 92/92 tests passing (87 v0.8b baseline +
5 new v0.9a). Resolves a STUB in the operator basis that's been there
since v0.3. ChatGPT-Pro's proposer-test motivating example
(`1/(1-exp(-βn))` literal divergence) now flagged before any
modular transform is attempted.

## Setup

ChatGPT-Pro's proposer-test answer (testing the v0.8a/b hypothesis)
identified that the `hardy_orders_of_infinity` operator in our 7-op
basis (Hunt 5 §5 revised basis, per diary 20) was a stub since v0.3
— `_hardy_orders_apply` returned None for every input. The intended
role: the engine's **divergence diagnostic**, applied first on each
new state to flag whether the literal summand-as-sum converges, and
tag the state with a `convergence_class`.

The motivating concrete example: the seed `1/(1 - exp(-β n))` summed
literally diverges (each term → 1 as n → ∞). The proposer needs to
know this before suggesting any modular transform — otherwise the
verifier wastes cycles trying to compare divergent sums. ChatGPT's
answer: "apply `hardy_orders_of_infinity` first" to diagnose. The
v0.8b `modular_transform_with_correction` operator already exists
and handles the convergent **log** form
`log(1 - exp(-β n))` cleanly (Dedekind-eta route, R17 closed in
diary 31), but nothing was flagging the divergent literal form
before the proposer tried it.

This diary entry covers the v0.9-hardy implementation. It is
parallel-developed with v0.8c (modular-transform Stieltjes/Lambert
extension by a sibling subagent) and v0.9b
(`InSessionClaudeProposer`, also by a sibling subagent). All three
land independently with no merge conflicts.

## What I did

### Step 1 — Decide where the convergence_class lives

The brief offered two architectural choices:

  (a) `SearchState.convergence_class` (top-level field on the state)
  (b) `OperatorApplication.metadata['convergence_class']` (per-application)

I went with **(a) plus mirror to `SearchState.metadata`**. Rationale:

  - convergence_class is a property of the EXPRESSION / state, not of
    the operator application that classified it. Two different
    operators inspecting the same payload would compute the same
    convergence class.
  - The top-level field gives direct attribute access
    (`state.convergence_class`) without dict-lookup overhead at every
    proposer call.
  - The metadata mirror means existing JsonlRegistry serialization
    (which dumps `metadata` via `_str_keys`) automatically picks it up
    — no schema break for downstream parsers.
  - Defense-in-depth: the audit-trail JSONL stores BOTH
    `state_after_convergence_class` (top-level, structured) AND
    `state_after_meta.convergence_class` (in the meta dict).

### Step 2 — Decide pre-pass vs regular operator

The brief offered two implementation choices:

  (a) Pre-pass: engine calls hardy_orders once per new state, separate
      from the proposer step.
  (b) Regular operator: the proposer can suggest hardy_orders like any
      other op; the engine applies it via the standard pipeline.

I went with **(b) regular operator**. Reasons documented inline in
`_hardy_orders_apply`'s docstring:

  1. **Zero engine surgery beyond the metadata-merge.** The 2-tuple
     return-convention extension is small, backward-compatible, and
     reuses the same dispatch path the v0.8b 3-tuple takes.
  2. **Composability.** Future operators (e.g. an Abel regularization
     operator that fires only when convergence_class is
     NEEDS_REGULARIZATION) can read the class off the state and decide
     whether to apply. A pre-pass would need its own hook system.
  3. **The proposer can BE the gating logic.** ClaudeProposer (v0.8a)
     and InSessionClaudeProposer (v0.9b) can read the state's
     convergence_class and decide whether to chain hardy_orders first.
     A future v0.9c will wire a system-prompt hint suggesting
     "if convergence_class is None on a novel state, fire hardy_orders
     first to diagnose." For now, RandomProposer fires hardy_orders
     ~1/8 of the time uniformly — fine for a cheap diagnostic.

### Step 3 — Extend the apply_fn return convention

The basis's apply_fn signature `(expr, n) → Optional[Expr]` already
has two return forms (post v0.8b):

  - `Expr` — strict-Poisson identity (v0.4 / v0.7)
  - 3-tuple `(new_summand, additive_correction, summand_range)` —
    modular-with-correction (v0.8b)

I added a third:

  - **2-tuple `(payload_unchanged, metadata_dict)`** — non-transforming
    annotator (v0.9a). The first element is the original payload
    returned unchanged; the second is a `dict[str, Any]` whose keys
    merge into the new state's metadata. If the dict carries a
    `convergence_class` key, the engine ALSO copies its value to the
    top-level `SearchState.convergence_class` field.

The engine dispatches on tuple length AND on the type of the second
element (Expr → 3-tuple v0.8b, dict → 2-tuple v0.9a) to avoid
ambiguity.

### Step 4 — Implement the classifier

`_v09a_classify_convergence(expr, n)` is the shared classifier helper
(module-level in `basis.py`). It runs `sp.limit(expr, n, sp.oo)` in
a broad try/except and dispatches on the returned object's sympy
flags:

  - `lim.is_zero is True`               → CONVERGENT
  - `lim is sp.oo` or `lim is -sp.oo`   → NEEDS_REGULARIZATION
  - `lim.is_finite is True` AND
    `lim.is_number is True` AND
    `lim != 0`                          → DIVERGENT_LITERAL
  - everything else (AccumulationBounds, zoo, nan, sympy raises)
                                        → UNKNOWN

The `is_number=True` guard is the key correctness gate: sympy's
`AccumulationBounds(-1, 1)` (returned by `sp.limit(sin(n), n, oo)`)
reports `is_finite=True` but is NOT a classifiable point value. We
correctly classify it as UNKNOWN rather than DIVERGENT_LITERAL.

### Step 5 — Numerical verification

Five inputs from the test suite:

| Input                       | Expected class       | Got                  |
|-----------------------------|----------------------|----------------------|
| `1/(1 - exp(-β n))`         | DIVERGENT_LITERAL    | DIVERGENT_LITERAL    |
| `exp(-β n²)`                | CONVERGENT           | CONVERGENT           |
| `log(1 - exp(-β n))`        | CONVERGENT           | CONVERGENT           |
| `n` (zeta-style divergent)  | NEEDS_REGULARIZATION | NEEDS_REGULARIZATION |
| `sin(n)` (oscillatory)      | UNKNOWN              | UNKNOWN              |
| `n · sin(n)`                | UNKNOWN              | UNKNOWN              |
| `42` (n-independent)        | (operator declines)  | None (decline)       |

All as expected. The `log(1 - exp(-β n))` case is particularly
important: it's the v0.8b Bose-Einstein input shape, and the n → 0
singularity (log(0) → -∞) could easily fool a naive classifier — but
we ask the n → ∞ question, where the summand → log(1-0) = 0.
Classifier correctly returns CONVERGENT.

### Step 6 — Tests

Five new `test_v09a_*` tests in `rkc/tests/test_cli.py`:

  1. `test_v09a_hardy_orders_detects_divergent_bose_einstein` — the
     ChatGPT-Pro motivating example; verifies the divergent flag fires.
  2. `test_v09a_hardy_orders_detects_convergent_gaussian` — pure
     Gaussian gets CONVERGENT; numeric-β variant also tested.
  3. `test_v09a_hardy_orders_detects_convergent_log_partition` — the
     v0.8b Bose-Einstein log form gets CONVERGENT (guards against
     n→0 vs n→∞ confusion).
  4. `test_v09a_hardy_orders_unknown_on_complex_expr` — pathological
     inputs (`sin(n)`, `n*sin(n)`, n-independent `42`) handled cleanly
     without crashes; plus a bonus NEEDS_REGULARIZATION check on `n`.
  5. `test_v09a_convergence_class_persisted` — JsonlRegistry round-
     trip preserves the tag (audit-trail guarantee).

## Results

```
$ python -m pytest rkc/tests/ -q
............................................................................. [ 84%]
....................                                                            [100%]
92 passed in 38.32s
```

Test count: **87 → 92 (+5)**. Recognizer v2 benchmark still 55/55 =
100%. Hunt 5 QR tagging still 57.6%. No regressions.

The basis now has:

  - 6 operators with real apply_fn implementations
    (master_theorem, mellin_inversion,
     modular_transform_with_correction, hardy_orders_of_infinity, ...)
  - 4 still-stub operators (fourier_self_reciprocity,
    fractional_functional_iteration, frullani_limit,
    mellin_pair_reciprocity)

`hardy_orders_of_infinity` is the first operator in the basis that's
**non-transforming** — it annotates rather than rewrites. The 2-tuple
return convention generalises naturally to future annotators (e.g.
a "this kernel is theta-like" tagger, a "this expression has a
non-trivial automorphism" tagger).

## Implications

### For the proposer side (Hunt 5b toolkit-split, diary 25)

Hunt 5b found that the Notebooks use a different small toolkit per
chapter (modular_S monoculture in Ch. 36, class_field + modular_S
combo in Ch. 34). The convergence_class diagnostic adds a structural
gating signal: a proposer can read `state.convergence_class` and
narrow its candidate set. Concrete bias rules (to wire into
ClaudeProposer's system prompt in v0.9c):

  - convergence_class = DIVERGENT_LITERAL
    → prefer `modular_transform_with_correction` (v0.8b) — its log /
      Lambert handlers map divergent literal forms to convergent dual
      summands.
  - convergence_class = NEEDS_REGULARIZATION
    → prefer `frullani_limit` or `mellin_pair_reciprocity` (the QR
      operators that handle regularised divergent integrals); also
      `master_theorem` if the input is an Integral.
  - convergence_class = CONVERGENT
    → all transform operators are in play; pick based on shape
      (Gaussian → mellin_inversion, etc.).
  - convergence_class = UNKNOWN
    → defer judgement; the diagnostic isn't load-bearing for this
      state.

### For the cohomological-irreducibility closure (Pass D, BIG_IDEAS)

The convergence_class diagnostic is a small but structurally important
step toward "the engine can MECHANIZE the falsification protocol that
gave us the irreducibility conjecture's 20-candidate failure run."
Adding this layer means: when a future Pass-D-style shadow probe
input is given to the engine, the engine can flag "this probe's
naive sum diverges — you need to regularise before comparison,"
catching at the proposer level what the experimenter used to catch
manually in DID_NOT_PAN_OUT entries R5-R10.

## Confidence

**High** on the implementation correctness (5/5 unit tests pass,
classifier behavior matches expectations on all 7 probe inputs).
**Medium-high** on the architectural choice (regular operator with
2-tuple return convention vs pre-pass) — the 2-tuple convention is
clean and composable, but a pre-pass might be more defensive for a
truly novel proposer that forgets to suggest hardy_orders first.
v0.9c will measure the right answer empirically once
InSessionClaudeProposer (v0.9b) lands and we can compare
"convergence_class-aware proposer" vs "convergence_class-blind
proposer" on the seed library.

**Indicative** on the long-term value: the convergence_class diagnostic
is the first of what will probably be a 3-5 entry library of
"asymptotic profile" annotators (next likely candidates:
"is_modular_form_candidate", "has_periodic_singularity_pattern"). The
v0.9a 2-tuple convention is the load-bearing decision that makes the
rest of those cheap to add.

## Bottom line

Hardy_orders_of_infinity is no longer a stub — it ships as the
engine's divergence diagnostic. ChatGPT-Pro's proposer-test motivating
example (`1/(1-exp(-βn))`) now correctly flagged before the proposer
tries to verify a divergent sum. The implementation took the
regular-operator path (not pre-pass) with a new 2-tuple return
convention for non-transforming annotators, opening the door to a
small library of asymptotic-profile annotators in the v0.10+ roadmap.
92/92 tests green; no backward-compat breakage.
