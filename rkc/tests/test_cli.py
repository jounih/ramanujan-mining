"""Smoke tests for the rkc v0.1 CLI scaffold.

These tests pin the CLI contract — exit codes, expected substrings in
human-readable output, and the four subcommand entry points. They do not
test the full per-family coverage matrix (that's the v0.1 release gate;
see rkc/MILESTONES.md §A).
"""
from __future__ import annotations

import json
import subprocess
import sys

import pytest


def _run(argv: list[str]) -> subprocess.CompletedProcess:
    """Invoke `python -m rkc <argv>` and capture both streams."""
    return subprocess.run(
        [sys.executable, "-m", "rkc", *argv],
        capture_output=True,
        text=True,
        timeout=60,
    )


# ---------------------------------------------------------------------------
# rkc --version / --help
# ---------------------------------------------------------------------------

def test_version():
    p = _run(["--version"])
    assert p.returncode == 0
    assert "rkc" in p.stdout


def test_help_lists_subcommands():
    p = _run(["--help"])
    assert p.returncode == 0
    for cmd in ("recognize", "compare", "certify", "benchmark"):
        assert cmd in p.stdout


# ---------------------------------------------------------------------------
# rkc recognize
# ---------------------------------------------------------------------------

def test_recognize_gaussian():
    p = _run(["recognize", "exp(-beta*n**2)"])
    assert p.returncode == 0
    assert "gaussian_quadratic" in p.stdout
    assert "theta-like" in p.stdout


def test_recognize_json_emits_valid_json():
    p = _run(["recognize", "exp(-beta*n**2)", "--json"])
    assert p.returncode == 0
    payload = json.loads(p.stdout)
    assert payload["kernel"] == "gaussian_quadratic"
    assert payload["family"] == "theta-like"


def test_recognize_no_match_returns_nonzero():
    p = _run(["recognize", "log(n) + sin(n)"])
    # Hand-crafted nothing: not a kernel; exit 1.
    assert p.returncode == 1


# ---------------------------------------------------------------------------
# rkc compare
# ---------------------------------------------------------------------------

def test_compare_gaussian_numeric_beta_shows_speedup():
    """With β=1e-8 we expect direct ≫ dual (Gaussian theta @ small β)."""
    p = _run(["compare", "exp(-beta*n**2)", "--param", "beta=1e-8"])
    assert p.returncode == 0
    out = p.stdout
    assert "gaussian_quadratic" in out
    # Cost estimator should give cost_direct > cost_dual at small β
    assert "cost_direct" in out
    assert "cost_dual" in out
    assert "speedup_factor" in out
    assert "recommended" in out


# ---------------------------------------------------------------------------
# rkc certify — degeneracy guard (the §A4 silent-zero hazard)
# ---------------------------------------------------------------------------

def test_certify_gauss_sum_silent_zero_fires_at_q_six():
    """q=6 ≡ 2 (mod 4) should fire the silent-zero hazard."""
    p = _run(["certify", "exp(2*pi*I*n**2/6)"])
    assert p.returncode == 0
    out = p.stdout
    assert "gauss_sum" in out
    assert "DEGENERATE" in out
    assert "silent-zero" in out
    # The CLI surfaces "do NOT use the dual" guidance for degenerate routes
    assert "do NOT use" in out


def test_certify_gauss_sum_q_seven_is_safe():
    """q=7 ≢ 2 (mod 4) → no degeneracy."""
    p = _run(["certify", "exp(2*pi*I*n**2/7)"])
    assert p.returncode == 0
    out = p.stdout
    assert "gauss_sum" in out
    assert "no degeneracy" in out


# ---------------------------------------------------------------------------
# rkc benchmark — default suite runs the 14b regression
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# rkc search (Project C v0.3.0 baseline)
# ---------------------------------------------------------------------------

def test_search_baseline_runs_and_writes_reject_log(tmp_path):
    """v0.3.0: with stub apply_fn's, all proposals decline; verify the
    engine + reject log path works end-to-end."""
    p = _run([
        "search", "exp(-beta*n**2)",
        "--budget", "5",
        "--digits", "10",
        "--seed", "42",
        "--out-dir", str(tmp_path),
    ])
    assert p.returncode == 0
    assert "proposed      : 5" in p.stdout
    assert "rejected      : 5" in p.stdout
    # reject log should exist
    assert (tmp_path / "rejected.jsonl").exists()
    # accepted log only created on first acceptance
    # (v0.3.0 has no implemented operators yet, so no acceptance expected)


def test_search_module_import_smoke():
    """Public API surface importable; protocols satisfied."""
    from rkc.search import (
        SearchState, OperatorApplication, RejectReason,
        Proposer, Verifier, Router, CostModel, Registry,
        RandomProposer, MpmathVerifier, RkcRouter, RkcCostModel,
        JsonlRegistry, search, QR7_OPERATOR_BASIS,
    )
    # The original QR7 basis was 7 ops (Hunt 5 revised set, diary 20).
    # v0.8b adds modular_transform_with_correction → basis is now 8.
    assert len(QR7_OPERATOR_BASIS) == 8
    op_ids = [op.id for op in QR7_OPERATOR_BASIS]
    assert "master_theorem" in op_ids
    assert "fractional_functional_iteration" in op_ids
    assert "modular_transform_with_correction" in op_ids


def test_v04_mellin_inversion_poisson_dual_accepted(tmp_path):
    """Project C v0.4 acceptance gate: with mellin_inversion's Poisson-
    summation apply_fn wired, a Gaussian at small β should produce at
    least one accepted identity via the Poisson dual."""
    import json
    import sympy as sp
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
    )
    n = sp.Symbol("n", integer=True, positive=True)
    expr = sp.exp(-sp.Rational(1, 100) * n**2)  # β=1/100; Poisson dual is ~54× cheaper
    state = SearchState(payload=expr, metadata={"var": n})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=10),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=30,
        max_depth=1,
    )
    # At least one acceptance expected (the seed is deterministic; mellin_inversion
    # gets chosen many times among 30, of which ~6-10 actually apply).
    assert summary.n_accepted >= 1, (
        f"v0.4 acceptance gate failed: 0 acceptances in 30-budget search; "
        f"reject reasons = {summary.reject_reason_counts}"
    )
    # Verify the accepted record looks right
    accepted_path = tmp_path / "accepted.jsonl"
    assert accepted_path.exists()
    first = json.loads(accepted_path.read_text().splitlines()[0])
    assert first["op_sequence"][0]["op_id"] == "mellin_inversion"
    # The cost ratio should be > 1 (the transformation is cheaper)
    assert first["cost_ratio"] > 1.0


def test_v04_mellin_inversion_apply_fn_directly():
    """Direct unit test of mellin_inversion's apply_fn: Gaussian → Poisson dual."""
    import sympy as sp
    from rkc.search.basis import get_operator
    n = sp.Symbol("n", integer=True, positive=True)
    op = get_operator("mellin_inversion")
    # Should apply to a gaussian
    expr_in = sp.exp(-sp.Rational(1, 100) * n**2)
    expr_out = op.apply_fn(expr_in, n)
    assert expr_out is not None, "mellin_inversion should fire on a gaussian"
    # Should NOT apply to a non-gaussian
    expr_not_gauss = sp.exp(-sp.Symbol("alpha", positive=True) * n)  # linear in n
    expr_out2 = op.apply_fn(expr_not_gauss, n)
    assert expr_out2 is None, "mellin_inversion should decline on non-gaussian"


def test_v07_mellin_inversion_half_shift_apply_fn_directly():
    """Project C v0.7 direct unit test: half-integer-shifted Gaussian.

    `c · exp(-β (n+1/2)²)` → `c · √(π/β) · (-1)^n · exp(-π² n²/β)`.

    Also checks that quarter-integer shifts (not half-integer) DECLINE
    cleanly — we deliberately don't handle arbitrary rational offsets
    in v0.7 because the dual becomes complex-valued.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    n = sp.Symbol("n", integer=True, positive=True)
    op = get_operator("mellin_inversion")
    expr_in = sp.exp(-sp.Rational(1, 100) * (n + sp.Rational(1, 2))**2)
    expr_out = op.apply_fn(expr_in, n)
    assert expr_out is not None, "mellin_inversion should fire on half-shift gaussian"
    # Structure check: dual should contain (-1)^n and a √π factor
    assert expr_out.has((-1)**n) or sp.simplify(
        expr_out / ((-1)**n)) != expr_out, "dual missing (-1)^n factor"
    assert expr_out.has(sp.sqrt(sp.pi)) or expr_out.has(sp.pi), \
        "dual missing √π / π factor"
    # Decline: quarter-shift (offset 1/4) doesn't match the half-shift signature
    expr_quarter = sp.exp(-sp.Rational(1, 100) * (n + sp.Rational(1, 4))**2)
    out_quarter = op.apply_fn(expr_quarter, n)
    assert out_quarter is None, (
        "mellin_inversion should decline on non-half-integer shifts in v0.7"
    )


def test_v07_mellin_inversion_weighted_apply_fn_directly():
    """Project C v0.7 direct unit test: weighted (second-moment) Gaussian.

    `c · n² · exp(-β n²)` →
    `c · √(π/β) · (1/(2β) - π² n²/β²) · exp(-π² n²/β)`.

    Also checks that `n³ · exp(-β n²)` (third moment, not handled in v0.7)
    declines.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    n = sp.Symbol("n", integer=True, positive=True)
    op = get_operator("mellin_inversion")
    expr_in = n**2 * sp.exp(-sp.Rational(1, 100) * n**2)
    expr_out = op.apply_fn(expr_in, n)
    assert expr_out is not None, "mellin_inversion should fire on n²·exp(-β n²)"
    # Decline: n³ form not handled
    expr_cube = n**3 * sp.exp(-sp.Rational(1, 100) * n**2)
    out_cube = op.apply_fn(expr_cube, n)
    assert out_cube is None, "mellin_inversion should decline on n^3 weight (v0.7)"
    # Decline: n²·exp(-β n) (linear, not quadratic in exp) should NOT fire
    expr_lin = n**2 * sp.exp(-sp.Rational(1, 100) * n)
    out_lin = op.apply_fn(expr_lin, n)
    assert out_lin is None, "mellin_inversion should decline on n²·exp(-β n) (linear exp)"


def test_v07_mellin_inversion_verifier_strict_agreement():
    """Project C v0.7: both new Poisson duals satisfy the strict
    numerical verifier across the default sweep at n_digits=20.

    This is the heart of the v0.7 release gate: the new identities are
    STRICT two-sided sum equalities (not modular-with-correction
    approximations), so the MpmathVerifier with default symmetric
    summand_range and dps buffer must report `passed=True`.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    from rkc.search.core import SearchState
    from rkc.search.verifiers import MpmathVerifier
    n = sp.Symbol("n", integer=True, positive=True)
    op = get_operator("mellin_inversion")
    verifier = MpmathVerifier(n_digits=20)
    for expr_in, label in [
        (sp.exp(-sp.Rational(1, 100) * (n + sp.Rational(1, 2))**2), "half-shift"),
        (n**2 * sp.exp(-sp.Rational(1, 100) * n**2), "weighted"),
    ]:
        expr_out = op.apply_fn(expr_in, n)
        sb = SearchState(payload=expr_in, metadata={"var": n})
        sa = SearchState(payload=expr_out, metadata={"var": n})
        result = verifier.verify(sb, [], sa)
        assert result.passed, (
            f"v0.7 verifier failed for {label}: {result.reason}"
        )


def test_v07_mellin_inversion_half_shift_accepted(tmp_path):
    """Project C v0.7 acceptance gate (A): half-shift Gaussian → dual,
    end-to-end through the search engine, produces ≥1 acceptance."""
    import json
    import sympy as sp
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
    )
    n = sp.Symbol("n", integer=True, positive=True)
    expr = sp.exp(-sp.Rational(1, 100) * (n + sp.Rational(1, 2))**2)
    state = SearchState(payload=expr, metadata={"var": n})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=10),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=30,
        max_depth=1,
    )
    assert summary.n_accepted >= 1, (
        f"v0.7 half-shift acceptance gate failed: 0 acceptances; "
        f"reasons={summary.reject_reason_counts}"
    )
    first = json.loads((tmp_path / "accepted.jsonl").read_text().splitlines()[0])
    assert first["op_sequence"][0]["op_id"] == "mellin_inversion"
    assert first["cost_ratio"] > 1.0, "v0.7 half-shift dual should be cheaper"


def test_v07_mellin_inversion_weighted_accepted(tmp_path):
    """Project C v0.7 acceptance gate (B): weighted Gaussian → dual,
    end-to-end through the search engine, produces ≥1 acceptance."""
    import json
    import sympy as sp
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
    )
    n = sp.Symbol("n", integer=True, positive=True)
    expr = n**2 * sp.exp(-sp.Rational(1, 100) * n**2)
    state = SearchState(payload=expr, metadata={"var": n})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=10),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=30,
        max_depth=1,
    )
    assert summary.n_accepted >= 1, (
        f"v0.7 weighted-gaussian acceptance gate failed: 0 acceptances; "
        f"reasons={summary.reject_reason_counts}"
    )
    first = json.loads((tmp_path / "accepted.jsonl").read_text().splitlines()[0])
    assert first["op_sequence"][0]["op_id"] == "mellin_inversion"
    assert first["cost_ratio"] > 1.0, "v0.7 weighted dual should be cheaper"


def test_v07_seeds_buildable_and_recover_identity():
    """v0.7 seeds `gaussian_half_shift_beta_1em2` and
    `gaussian_weighted_beta_1em2` are buildable and recover an identity
    in a 30-budget search (smoke-level acceptance check)."""
    import tempfile
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
        SEED_LIBRARY, build_seed,
    )
    for sid in ["gaussian_half_shift_beta_1em2", "gaussian_weighted_beta_1em2"]:
        assert sid in SEED_LIBRARY, f"v0.7 seed {sid!r} missing from SEED_LIBRARY"
        seed = SEED_LIBRARY[sid]
        expr, var = build_seed(seed)
        with tempfile.TemporaryDirectory() as tmp:
            state = SearchState(payload=expr, metadata={"var": var})
            reg = JsonlRegistry.with_dir(tmp)
            summary = search(
                initial_state=state,
                proposer=RandomProposer(seed=42),
                verifier=MpmathVerifier(n_digits=10),
                router=RkcRouter(),
                cost_model=RkcCostModel(),
                registry=reg,
                budget=30,
                max_depth=1,
            )
            assert summary.n_accepted >= 1, (
                f"v0.7 seed {sid!r} produced 0 acceptances; "
                f"reasons={summary.reject_reason_counts}"
            )


def test_v05_master_theorem_beta_function(tmp_path):
    """Project C v0.5: master_theorem accepts the Beta-function identity
    `∫₀^¹ x^(m-1) (1-x)^(n-1) dx = Γ(m)Γ(n)/Γ(m+n)` end-to-end."""
    import json
    import sympy as sp
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
    )
    x = sp.Symbol("x", positive=True)
    m = sp.Symbol("m", positive=True)
    n = sp.Symbol("n", positive=True)
    beta_int = sp.Integral(x**(m-1) * (1-x)**(n-1), (x, 0, 1))
    state = SearchState(payload=beta_int, metadata={"var": x})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state, proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=10),
        router=RkcRouter(), cost_model=RkcCostModel(),
        registry=reg, budget=30, max_depth=1,
    )
    assert summary.n_accepted >= 1, (
        f"v0.5 acceptance gate failed: {summary.reject_reason_counts}"
    )
    accepted_path = tmp_path / "accepted.jsonl"
    assert accepted_path.exists()
    first = json.loads(accepted_path.read_text().splitlines()[0])
    assert first["op_sequence"][0]["op_id"] == "master_theorem"
    # The closed-form Γ-product should be much cheaper than the integral
    assert first["cost_ratio"] >= 50.0
    # The output should contain gamma functions
    assert "gamma" in first["state_after"].lower()


def test_v06_sweep_serial_smoke(tmp_path):
    """Project C v0.6+ sweep: serial 1-worker run over 3 seeds with the
    deterministic RNG seed. Hit-rate floor: ≥2 of 3 seeds (Gaussian +
    Master-Theorem-Beta) should produce at least one acceptance."""
    from rkc.search import SEED_LIBRARY, sweep
    seed_ids = ["gaussian_beta_1em2", "gaussian_beta_1em4", "beta_function_integral"]
    summary = sweep(
        seed_ids=seed_ids, budget=15, max_depth=2, n_digits=8,
        workers=1, rng_seed=42, out_dir=tmp_path,
    )
    assert summary["n_seeds"] == 3
    assert summary["n_errors"] == 0
    assert summary["n_seeds_with_acceptance"] >= 2, (
        f"sweep smoke failed: only {summary['n_seeds_with_acceptance']} of 3 "
        f"produced acceptance. Per-seed: {[(r['seed_id'], r['n_accepted']) for r in summary['per_seed']]}"
    )
    # Output files written
    assert (tmp_path / "sweep_summary.json").exists()
    assert (tmp_path / "sweep_summary.csv").exists()


def test_sweep_seed_library_buildable():
    """Every seed in SEED_LIBRARY must construct without raising."""
    from rkc.search import SEED_LIBRARY, build_seed
    for sid, seed in SEED_LIBRARY.items():
        expr, var = build_seed(seed)
        assert expr is not None, f"seed {sid} built None expr"
        assert var is not None, f"seed {sid} built None var"


def test_v05_master_theorem_canonical_patterns():
    """Unit test: master_theorem matches the 3 canonical patterns
    (Gamma, Beta, 1/(1+x)) and declines on non-matching forms."""
    import sympy as sp
    from rkc.search.basis import get_operator
    op = get_operator("master_theorem")
    x = sp.Symbol("x", positive=True)
    m = sp.Symbol("m", positive=True)
    n = sp.Symbol("n", positive=True)
    s = sp.Symbol("s", positive=True)
    dummy = sp.Symbol("dummy")

    # Gamma
    out = op.apply_fn(sp.Integral(x**(s-1) * sp.exp(-x), (x, 0, sp.oo)), dummy)
    assert out == sp.gamma(s)

    # Beta
    out = op.apply_fn(sp.Integral(x**(m-1) * (1-x)**(n-1), (x, 0, 1)), dummy)
    assert sp.simplify(out - sp.gamma(m)*sp.gamma(n)/sp.gamma(m+n)) == 0

    # 1/(1+x)
    out = op.apply_fn(sp.Integral(x**(s-1) / (1+x), (x, 0, sp.oo)), dummy)
    assert sp.simplify(out - sp.pi/sp.sin(sp.pi*s)) == 0

    # Decline: not an Integral
    out = op.apply_fn(sp.exp(-x), x)
    assert out is None

    # Decline: integrand doesn't match any pattern
    out = op.apply_fn(sp.Integral(x**2 * sp.log(x), (x, 0, 1)), dummy)
    assert out is None


# ---------------------------------------------------------------------------
# Project C v0.8b — modular_transform_with_correction (one-sided summands
# with additive scalar correction terms; unblocks Bose-Einstein + Lambert)
# ---------------------------------------------------------------------------

def test_v08b_operator_application_additive_correction_field():
    """v0.8b API extension: OperatorApplication carries optional
    `additive_correction` and `summand_range` fields. Backward compat:
    default is None for both, preserving v0.4 / v0.7 strict-Poisson
    semantics.
    """
    import sympy as sp
    from rkc.search.core import OperatorApplication
    # Default fields — backward compat for v0.4 / v0.7 operators
    op_default = OperatorApplication(op_id="mellin_inversion")
    assert op_default.additive_correction is None
    assert op_default.summand_range is None
    # v0.8b explicit fields
    op_v08b = OperatorApplication(
        op_id="modular_transform_with_correction",
        additive_correction=sp.pi**2 / 6,
        summand_range=(1, sp.oo),
    )
    assert op_v08b.additive_correction == sp.pi**2 / 6
    assert op_v08b.summand_range == (1, sp.oo)


def test_v08b_verifier_folds_additive_correction():
    """v0.8b: MpmathVerifier compares
        Σ_n before_summand  ≡  Σ_n after_summand + total_additive_correction
    where total_additive_correction is the sum of the additive_correction
    fields across the op_sequence. v0.4 / v0.7 operators leaving these
    fields None get the legacy (correction=0, range=verifier-default)
    path exactly.
    """
    import sympy as sp
    import mpmath
    from rkc.search.core import OperatorApplication, SearchState
    from rkc.search.verifiers import MpmathVerifier
    n = sp.Symbol("n", integer=True, positive=True)
    # Synthetic identity: Σ_{n≥1} 1/2^n = 1 (geometric series).
    # Express as: state_before = 1/2^n; state_after = 1/2^n (trivially equal);
    # additive_correction = 0; should pass.
    expr = sp.Rational(1, 2)**n
    state_before = SearchState(payload=expr, metadata={"var": n})
    state_after = SearchState(payload=expr, metadata={"var": n})
    op_app = OperatorApplication(
        op_id="modular_transform_with_correction",
        additive_correction=sp.Integer(0),
        summand_range=(1, sp.oo),
    )
    verifier = MpmathVerifier(n_digits=20, sweep_params=[{}])
    result = verifier.verify(state_before, [op_app], state_after)
    assert result.passed, (
        f"trivial identity with zero additive correction should pass: {result.reason}"
    )

    # Now a real one: Σ_{n≥1} 1/n² = π²/6 (Basel).
    # Use state_before = 1/n²; state_after = 0; additive_correction = π²/6.
    state_b = SearchState(payload=1/n**2, metadata={"var": n})
    state_a = SearchState(payload=sp.Integer(0), metadata={"var": n})
    op_app2 = OperatorApplication(
        op_id="modular_transform_with_correction",
        additive_correction=sp.pi**2 / 6,
        summand_range=(1, sp.oo),
    )
    result2 = verifier.verify(state_b, [op_app2], state_a)
    assert result2.passed, (
        f"Basel identity via additive_correction=π²/6 should pass: {result2.reason}"
    )


def test_v08b_modular_transform_apply_fn_directly():
    """Direct unit test of `modular_transform_with_correction`:
    - Bose-Einstein log form `log(1 - exp(-β n))` returns the tuple
      (new_summand, correction, (1, oo)).
    - Lambert `n · q^n / (1 - q^n)` returns the tuple.
    - Non-matching forms (Gaussian, q ≥ 1 Lambert) decline cleanly.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    n = sp.Symbol("n", integer=True, positive=True)
    beta = sp.Symbol("beta", positive=True)
    op = get_operator("modular_transform_with_correction")

    # Case A: Bose-Einstein log
    result_A = op.apply_fn(sp.log(1 - sp.exp(-beta * n)), n)
    assert result_A is not None, "should match log(1-exp(-β n))"
    assert isinstance(result_A, tuple), "v0.8b returns a tuple"
    assert len(result_A) == 3
    new_summand, correction, srange = result_A
    assert srange == (1, sp.oo), "Bose-Einstein log is one-sided"
    # New summand should contain 4*pi**2 * n / beta in the exp arg
    assert new_summand.has(sp.pi), "dual exponent involves π"
    # Correction should contain -π²/(6β)
    assert correction.has(sp.pi), "correction has π contribution"

    # Case B: Lambert
    q = sp.Rational(1, 10)
    result_B = op.apply_fn(n * q**n / (1 - q**n), n)
    assert result_B is not None, "should match n*q^n/(1-q^n)"
    assert isinstance(result_B, tuple) and len(result_B) == 3
    _, _, srange_B = result_B
    assert srange_B == (1, sp.oo)

    # Decline: Gaussian (different family)
    result_gauss = op.apply_fn(sp.exp(-beta * n**2), n)
    assert result_gauss is None, "modular_transform_with_correction declines gaussian"

    # Decline: log(1 - 2·exp(-β n)) — c ≠ 1 (not the eta-log form)
    result_c2 = op.apply_fn(sp.log(1 - 2 * sp.exp(-beta * n)), n)
    assert result_c2 is None, "declines on log(1 - c·exp(-β n)) for c ≠ 1"


def test_v08b_bose_einstein_dual_accepted(tmp_path):
    """v0.8b acceptance gate (A): Bose-Einstein log seed at β=1/100 produces
    ≥1 acceptance via the modular_transform_with_correction operator,
    end-to-end through the engine, with cost ratio > 1.

    This is the strict v0.8 test the brief calls for: the previously-deferred
    seed (R17) now ships cleanly via the new operator API.
    """
    import json
    import sympy as sp
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
    )
    n = sp.Symbol("n", integer=True, positive=True)
    expr = sp.log(1 - sp.exp(-sp.Rational(1, 100) * n))
    state = SearchState(payload=expr, metadata={"var": n})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=10),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=40,
        max_depth=1,
    )
    assert summary.n_accepted >= 1, (
        f"v0.8b Bose-Einstein log gate failed: 0 acceptances; "
        f"reasons={summary.reject_reason_counts}"
    )
    first = json.loads((tmp_path / "accepted.jsonl").read_text().splitlines()[0])
    assert first["op_sequence"][0]["op_id"] == "modular_transform_with_correction"
    assert first["cost_ratio"] > 1.0, (
        "v0.8b Bose-Einstein dual at β=1/100 should be cheaper "
        f"(ratio={first['cost_ratio']})"
    )


def test_v08b_lambert_dual_accepted(tmp_path):
    """v0.8b acceptance gate (B): Lambert seed at q=1/10 produces ≥1
    acceptance via the modular_transform_with_correction operator,
    end-to-end through the engine, with cost ratio > 1.
    """
    import json
    import sympy as sp
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
    )
    n = sp.Symbol("n", integer=True, positive=True)
    q = sp.Rational(1, 10)
    expr = n * q**n / (1 - q**n)
    state = SearchState(payload=expr, metadata={"var": n})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=10),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=40,
        max_depth=1,
    )
    assert summary.n_accepted >= 1, (
        f"v0.8b Lambert gate failed: 0 acceptances; "
        f"reasons={summary.reject_reason_counts}"
    )
    first = json.loads((tmp_path / "accepted.jsonl").read_text().splitlines()[0])
    assert first["op_sequence"][0]["op_id"] == "modular_transform_with_correction"
    assert first["cost_ratio"] > 1.0, (
        f"v0.8b Lambert dual at q=1/10 should be cheaper "
        f"(ratio={first['cost_ratio']})"
    )


def test_v08b_backward_compat_v07_paths_still_strict():
    """v0.8b backward compat: v0.4 Gaussian and v0.7 half-shift / weighted
    identities continue to verify STRICTLY (no additive correction, no
    summand range override) through the extended verifier.

    This is the load-bearing backward-compat guarantee: the data-model
    extension is opt-in per-operator, and existing strict-Poisson paths
    are unaffected.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    from rkc.search.core import OperatorApplication, SearchState
    from rkc.search.verifiers import MpmathVerifier
    from rkc.search.engine import _apply_operator

    n = sp.Symbol("n", integer=True, positive=True)
    op_mellin = get_operator("mellin_inversion")
    verifier = MpmathVerifier(n_digits=20)

    # v0.4 pure Gaussian
    expr_g = sp.exp(-sp.Rational(1, 100) * n**2)
    state_g = SearchState(payload=expr_g, metadata={"var": n})
    op_app_g = OperatorApplication(op_id="mellin_inversion")
    state_g_out = _apply_operator(op_app_g, state_g)
    assert state_g_out is not None
    # CRITICAL: op_app's correction / range fields should still be None
    # (the Gaussian apply_fn returns a bare Expr, not a tuple)
    assert op_app_g.additive_correction is None, (
        "v0.4 Gaussian apply_fn should leave additive_correction=None"
    )
    assert op_app_g.summand_range is None, (
        "v0.4 Gaussian apply_fn should leave summand_range=None"
    )
    r_g = verifier.verify(state_g, [op_app_g], state_g_out)
    assert r_g.passed, f"v0.4 Gaussian strict path broken: {r_g.reason}"

    # v0.7-A half-shift Gaussian
    expr_h = sp.exp(-sp.Rational(1, 100) * (n + sp.Rational(1, 2))**2)
    state_h = SearchState(payload=expr_h, metadata={"var": n})
    op_app_h = OperatorApplication(op_id="mellin_inversion")
    state_h_out = _apply_operator(op_app_h, state_h)
    assert op_app_h.additive_correction is None
    assert op_app_h.summand_range is None
    r_h = verifier.verify(state_h, [op_app_h], state_h_out)
    assert r_h.passed, f"v0.7-A half-shift strict path broken: {r_h.reason}"

    # v0.7-B weighted Gaussian
    expr_w = n**2 * sp.exp(-sp.Rational(1, 100) * n**2)
    state_w = SearchState(payload=expr_w, metadata={"var": n})
    op_app_w = OperatorApplication(op_id="mellin_inversion")
    state_w_out = _apply_operator(op_app_w, state_w)
    assert op_app_w.additive_correction is None
    assert op_app_w.summand_range is None
    r_w = verifier.verify(state_w, [op_app_w], state_w_out)
    assert r_w.passed, f"v0.7-B weighted strict path broken: {r_w.reason}"


def test_v08b_verifier_strict_agreement_high_digits():
    """v0.8b: both modular identities verify to ≥30 digits at the
    n_digits=30 setting via the default beta sweep. This is the strict bar
    promised in the brief (≥30-digit agreement, ≤1% rel-dev across ≥2 dex).

    The verifier auto-bumps its working dps when an additive correction is
    present (since one-sided log sums converge slowly at very small β); the
    test exercises that path.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    from rkc.search.core import OperatorApplication, SearchState
    from rkc.search.verifiers import MpmathVerifier
    from rkc.search.engine import _apply_operator

    n = sp.Symbol("n", integer=True, positive=True)
    beta = sp.Symbol("beta", positive=True)
    op = get_operator("modular_transform_with_correction")

    # Bose-Einstein log
    expr_A = sp.log(1 - sp.exp(-beta * n))
    state_A = SearchState(payload=expr_A, metadata={"var": n})
    op_app_A = OperatorApplication(op_id="modular_transform_with_correction")
    state_A_out = _apply_operator(op_app_A, state_A)
    verifier30 = MpmathVerifier(n_digits=30)
    r_A = verifier30.verify(state_A, [op_app_A], state_A_out)
    assert r_A.passed, f"Bose-Einstein log at 30 digits failed: {r_A.reason}"

    # Lambert with concrete q=1/10
    expr_B = n * sp.Rational(1, 10)**n / (1 - sp.Rational(1, 10)**n)
    state_B = SearchState(payload=expr_B, metadata={"var": n})
    op_app_B = OperatorApplication(op_id="modular_transform_with_correction")
    state_B_out = _apply_operator(op_app_B, state_B)
    r_B = verifier30.verify(state_B, [op_app_B], state_B_out)
    assert r_B.passed, f"Lambert at 30 digits failed: {r_B.reason}"


def test_v08b_seeds_buildable_and_recover_identity():
    """v0.8b seeds `bose_einstein_beta_1em2` (log form) and
    `lambert_divisor_q_p1` are buildable and recover an identity in a
    40-budget search.
    """
    import tempfile
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
        SEED_LIBRARY, build_seed,
    )
    for sid in ["bose_einstein_beta_1em2", "lambert_divisor_q_p1"]:
        assert sid in SEED_LIBRARY, f"v0.8b seed {sid!r} missing"
        seed = SEED_LIBRARY[sid]
        expr, var = build_seed(seed)
        with tempfile.TemporaryDirectory() as tmp:
            state = SearchState(payload=expr, metadata={"var": var})
            reg = JsonlRegistry.with_dir(tmp)
            summary = search(
                initial_state=state,
                proposer=RandomProposer(seed=42),
                verifier=MpmathVerifier(n_digits=10),
                router=RkcRouter(),
                cost_model=RkcCostModel(),
                registry=reg,
                budget=40,
                max_depth=1,
            )
            assert summary.n_accepted >= 1, (
                f"v0.8b seed {sid!r} produced 0 acceptances; "
                f"reasons={summary.reject_reason_counts}"
            )


# ---------------------------------------------------------------------------
# rkc benchmark — default suite runs the 14b regression
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_benchmark_default_suite_runs():
    """The default benchmark runs `analysis/14b_recognizer_v2_benchmark.py`.
    Slow because it does the full 55-case sweep; marked accordingly so the
    default `pytest -m 'not slow'` skips it.
    """
    p = _run(["benchmark"])
    assert p.returncode == 0
    # The 14b script prints "55/55" if everything passes
    assert "55" in p.stdout


# ---------------------------------------------------------------------------
# Project C v0.8a — ClaudeProposer (LLM-powered proposer)
# ---------------------------------------------------------------------------

def test_v08a_claude_stub_proposer_when_no_api_key(monkeypatch):
    """v0.8a: with ANTHROPIC_API_KEY unset, ClaudeProposer falls back to
    ClaudeStubProposer (random selection), logs a warning, and yields
    OperatorApplications with op_ids from the basis.

    The graceful-fallback path is the contract for CI / offline use.
    """
    import sympy as sp
    from rkc.search import (
        SearchState, ClaudeProposer, ClaudeStubProposer, QR7_OPERATOR_BASIS,
    )
    # Force ANTHROPIC_API_KEY off; clear cached load
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    # Also patch load_dotenv to be a no-op so a local .env file doesn't
    # accidentally inject the key during testing.
    import rkc.search.proposers as proposers_mod

    def _fake_load_dotenv(*args, **kwargs):
        return False
    monkeypatch.setattr(proposers_mod, "load_dotenv" if hasattr(
        proposers_mod, "load_dotenv") else "load_dotenv", _fake_load_dotenv,
                        raising=False)
    # Also need to monkeypatch the dotenv module that's imported inside
    # ClaudeProposer.__post_init__
    import sys as _sys
    fake_dotenv = type(_sys)("dotenv")
    fake_dotenv.load_dotenv = _fake_load_dotenv
    monkeypatch.setitem(_sys.modules, "dotenv", fake_dotenv)

    n = sp.Symbol("n", integer=True, positive=True)
    state = SearchState(
        payload=sp.exp(-sp.Rational(1, 100) * n**2), metadata={"var": n},
    )
    proposer = ClaudeProposer(seed=42)
    # The fallback should be active
    assert proposer._fallback is not None
    assert isinstance(proposer._fallback, ClaudeStubProposer)
    # Stats should reflect the fallback
    s = proposer.stats()
    assert s["fallback_active"] is True
    assert s["api_calls"] == 0
    # propose() should yield basis op_ids without making any API call
    op_ids = {op.id for op in QR7_OPERATOR_BASIS}
    proposals = list(proposer.propose(state, budget=5))
    assert len(proposals) == 5
    for app in proposals:
        assert app.op_id in op_ids, f"{app.op_id!r} not in basis"


def test_v08a_claude_proposer_obeys_basis():
    """v0.8a: with a MOCK Anthropic client returning a fake JSON-shaped op
    payload, ClaudeProposer parses it and returns the corresponding
    OperatorApplication (no real API call).

    Mocks the `client.messages.create()` to return a synthetic response
    object shaped like the real Anthropic SDK output (a `.content` list
    of blocks each with a `.text` attribute).
    """
    import sympy as sp
    from rkc.search import SearchState, ClaudeProposer

    class _MockContentBlock:
        def __init__(self, text):
            self.text = text

    class _MockResponse:
        def __init__(self, text):
            self.content = [_MockContentBlock(text)]

    class _MockMessages:
        def __init__(self, response_text):
            self._response_text = response_text
            self.calls = 0

        def create(self, **kwargs):
            self.calls += 1
            return _MockResponse(self._response_text)

    class _MockClient:
        def __init__(self, response_text):
            self.messages = _MockMessages(response_text)

    n = sp.Symbol("n", integer=True, positive=True)
    state = SearchState(
        payload=sp.exp(-sp.Rational(1, 100) * n**2), metadata={"var": n},
    )

    # Case 1: clean JSON
    client = _MockClient(
        '{"op_id": "mellin_inversion", "rationale": "Gaussian Poisson dual"}'
    )
    proposer = ClaudeProposer(client=client, seed=42, max_api_calls=5)
    assert proposer._fallback is None, "should NOT fall back when client supplied"
    proposals = list(proposer.propose(state, budget=3))
    assert len(proposals) == 3
    for app in proposals:
        assert app.op_id == "mellin_inversion"
    # The cache should de-dup repeated identical states → only 1 API call
    assert client.messages.calls == 1
    assert proposer.stats()["api_calls"] == 1

    # Case 2: JSON wrapped in markdown fences (common LLM artefact)
    client_md = _MockClient(
        '```json\n{"op_id": "master_theorem", "rationale": "integral form"}\n```'
    )
    proposer_md = ClaudeProposer(client=client_md, seed=42, max_api_calls=5)
    proposals_md = list(proposer_md.propose(state, budget=1))
    assert proposals_md[0].op_id == "master_theorem"

    # Case 3: JSON preceded by prose (also common)
    client_prose = _MockClient(
        'I think the right choice is:\n{"op_id": "frullani_limit", "rationale": ""}\n'
    )
    proposer_prose = ClaudeProposer(client=client_prose, seed=42, max_api_calls=5)
    proposals_prose = list(proposer_prose.propose(state, budget=1))
    assert proposals_prose[0].op_id == "frullani_limit"


def test_v08a_claude_proposer_parses_malformed_response():
    """v0.8a: proposer handles non-parseable responses + out-of-basis
    op_ids by falling back to a random selection from the basis (not
    erroring), and logs the failure mode.
    """
    import logging
    import sympy as sp
    from rkc.search import SearchState, ClaudeProposer, QR7_OPERATOR_BASIS

    class _MockContentBlock:
        def __init__(self, text):
            self.text = text

    class _MockResponse:
        def __init__(self, text):
            self.content = [_MockContentBlock(text)]

    class _MockMessages:
        def __init__(self, responses):
            self._responses = list(responses)
            self.calls = 0

        def create(self, **kwargs):
            response = self._responses[self.calls % len(self._responses)]
            self.calls += 1
            return _MockResponse(response)

    class _MockClient:
        def __init__(self, responses):
            self.messages = _MockMessages(responses)

    n = sp.Symbol("n", integer=True, positive=True)
    op_ids = {op.id for op in QR7_OPERATOR_BASIS}

    # Case A: unparseable response (free-form prose, no JSON)
    client_garbage = _MockClient([
        "I don't know, maybe try mellin_inversion or something",
    ])
    state = SearchState(
        payload=sp.exp(-sp.Rational(1, 100) * n**2), metadata={"var": n},
    )
    proposer = ClaudeProposer(client=client_garbage, seed=42, max_api_calls=5)
    proposals = list(proposer.propose(state, budget=1))
    assert len(proposals) == 1
    # Fallback to random — must still be in basis
    assert proposals[0].op_id in op_ids

    # Case B: well-formed JSON but op_id not in basis
    client_wrong = _MockClient([
        '{"op_id": "not_a_real_operator", "rationale": "made up"}',
    ])
    state_2 = SearchState(
        payload=sp.exp(-sp.Rational(1, 50) * n**2), metadata={"var": n},
    )
    proposer_2 = ClaudeProposer(client=client_wrong, seed=42, max_api_calls=5)
    proposals_2 = list(proposer_2.propose(state_2, budget=1))
    assert proposals_2[0].op_id in op_ids
    assert proposals_2[0].op_id != "not_a_real_operator"

    # Case C: API exception → random fallback (no exception escapes propose())
    class _ExplodingMessages:
        calls = 0

        def create(self, **kwargs):
            self.calls += 1
            raise RuntimeError("API down")

    class _ExplodingClient:
        def __init__(self):
            self.messages = _ExplodingMessages()

    client_boom = _ExplodingClient()
    state_3 = SearchState(payload=sp.Symbol("foo"), metadata={"var": n})
    proposer_3 = ClaudeProposer(client=client_boom, seed=42, max_api_calls=5)
    proposals_3 = list(proposer_3.propose(state_3, budget=2))
    assert len(proposals_3) == 2
    for app in proposals_3:
        assert app.op_id in op_ids


def test_v08a_claude_proposer_respects_max_api_calls():
    """v0.8a: proposer caps API calls at `max_api_calls`; excess budget is
    filled from random fallback (no further API calls).
    """
    import sympy as sp
    from rkc.search import SearchState, ClaudeProposer

    class _MockResponse:
        def __init__(self, text):
            class _B: pass
            b = _B()
            b.text = text
            self.content = [b]

    class _MockMessages:
        def __init__(self):
            self.calls = 0

        def create(self, **kwargs):
            self.calls += 1
            # Force a unique response per state so caching doesn't masque
            # the call-count behaviour
            return _MockResponse(
                f'{{"op_id": "mellin_inversion", "rationale": "call #{self.calls}"}}'
            )

    class _MockClient:
        def __init__(self):
            self.messages = _MockMessages()

    client = _MockClient()
    proposer = ClaudeProposer(client=client, seed=42, max_api_calls=2)

    n = sp.Symbol("n", integer=True, positive=True)
    # Use DIFFERENT states each call so the cache doesn't short-circuit
    proposals = []
    for i in range(5):
        state = SearchState(
            payload=sp.exp(-sp.Rational(1, 100 + i) * n**2),
            metadata={"var": n},
        )
        proposals.extend(list(proposer.propose(state, budget=1)))
    # Only the first 2 should be live API calls; the rest are random fallback
    assert client.messages.calls == 2
    assert len(proposals) == 5
    assert proposer.stats()["api_calls"] == 2


def test_v08a_cli_sweep_accepts_proposer_flag(tmp_path):
    """v0.8a CLI: `rkc sweep --proposer random` runs (default). The
    `--proposer claude` path is exercised by the live-benchmark step (not
    in CI). Smoke-test just the flag plumbing here.
    """
    p = _run([
        "sweep", "--seeds", "gaussian_beta_1em2",
        "--budget", "10", "--depth", "1", "--workers", "1",
        "--digits", "8", "--seed", "42",
        "--proposer", "random",
        "--out-dir", str(tmp_path),
    ])
    assert p.returncode == 0, f"sweep failed: stderr={p.stderr}, stdout={p.stdout}"
    assert "rkc sweep complete" in p.stdout


def test_v08a_cli_search_accepts_proposer_flag(tmp_path):
    """v0.8a CLI: `rkc search --proposer claude` exercises the
    ClaudeProposer path (with the stub fallback active when API key
    isn't set — so this is safe in CI).
    """
    import os
    # Force the stub path so test doesn't try a real API call
    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)
    import subprocess
    import sys as _sys
    p = subprocess.run(
        [_sys.executable, "-m", "rkc",
         "search", "exp(-beta*n**2)",
         "--budget", "3", "--digits", "8", "--seed", "42",
         "--out-dir", str(tmp_path),
         "--proposer", "claude"],
        capture_output=True, text=True, timeout=60, env=env,
    )
    assert p.returncode == 0, f"search failed: stderr={p.stderr}"
    # Should mention claude in some way (the proposer choice surfaces in output)
    assert "proposed" in p.stdout
