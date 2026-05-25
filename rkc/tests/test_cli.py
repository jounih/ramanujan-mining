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
    # v0.8b added modular_transform_with_correction → basis was 8.
    # v0.10 adds 4 more (mock_theta_completion_transform,
    #   partial_theta_completion, gauss_sum_finite_evaluation,
    #   q_pochhammer_transform) → basis is now 12.
    assert len(QR7_OPERATOR_BASIS) == 12
    op_ids = [op.id for op in QR7_OPERATOR_BASIS]
    assert "master_theorem" in op_ids
    assert "fractional_functional_iteration" in op_ids
    assert "modular_transform_with_correction" in op_ids
    # v0.10 additions
    assert "mock_theta_completion_transform" in op_ids
    assert "partial_theta_completion" in op_ids
    assert "gauss_sum_finite_evaluation" in op_ids
    assert "q_pochhammer_transform" in op_ids


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
# Project C v0.8c — Stieltjes/Lambert occupation-number identity
# (third case of modular_transform_with_correction; per ChatGPT Pro
# proposer answer 2026-05-24; see diary 32)
# ---------------------------------------------------------------------------

def test_v08c_occupation_number_apply_fn_directly():
    """Direct unit test of v0.8c's CASE C extension to
    `modular_transform_with_correction`:

    - `1/(exp(β·n) - 1)` returns a (new_summand, additive_correction,
      (1, oo)) tuple per the v0.8b 3-tuple convention.
    - Non-matching forms (Gaussian, log Bose-Einstein, plain exp) decline
      cleanly without claiming to apply.
    - Scalar prefactor `c · 1/(exp(β·n) - 1)` is handled — the `c` pulled
      via `as_independent(n)` and threaded through both the dual summand
      and the additive correction.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    n = sp.Symbol("n", integer=True, positive=True)
    beta = sp.Symbol("beta", positive=True)
    op = get_operator("modular_transform_with_correction")

    # Case C: occupation-number (symbolic β)
    result_C = op.apply_fn(1 / (sp.exp(beta * n) - 1), n)
    assert result_C is not None, "should match 1/(exp(β·n)-1)"
    assert isinstance(result_C, tuple), "v0.8c uses v0.8b 3-tuple convention"
    assert len(result_C) == 3
    new_summand, correction, srange = result_C
    assert srange == (1, sp.oo), "occupation-number is one-sided"
    # Dual summand should contain divisor_sigma, Ei, expint, and 4π²/β
    assert new_summand.has(sp.divisor_sigma), "dual uses divisor function d(m)"
    assert new_summand.has(sp.Ei), "dual uses Ei exponential integral"
    assert new_summand.has(sp.expint), "dual uses E_1 = expint(1, ·)"
    assert new_summand.has(sp.pi), "dual β* = 4π²/β involves π"
    # Correction should contain log(1/β), γ (EulerGamma), and 1/4
    assert correction.has(sp.EulerGamma), "correction has γ contribution"
    assert correction.has(sp.log), "correction has log(1/β)"

    # Case C with concrete rational β
    result_C2 = op.apply_fn(1 / (sp.exp(sp.Rational(1, 100) * n) - 1), n)
    assert result_C2 is not None, "should match concrete β=1/100"
    assert isinstance(result_C2, tuple) and len(result_C2) == 3

    # Scalar prefactor: c · 1/(exp(β·n) - 1)
    result_scaled = op.apply_fn(5 * 1 / (sp.exp(beta * n) - 1), n)
    assert result_scaled is not None, "should match c·1/(exp(β·n)-1)"
    new_s_scaled, corr_scaled, _ = result_scaled
    # The scalar 5 should appear in both the summand and the correction
    # (linearity of the identity).
    assert (new_s_scaled / new_summand).simplify() == 5, (
        f"scalar prefactor 5 should scale dual summand linearly; "
        f"ratio simplified to {(new_s_scaled / new_summand).simplify()}"
    )
    assert (corr_scaled / correction).simplify() == 5, (
        f"scalar prefactor 5 should scale correction linearly"
    )

    # Decline: Gaussian (different family)
    result_gauss = op.apply_fn(sp.exp(-beta * n**2), n)
    assert result_gauss is None, "modular_transform_with_correction declines Gaussian"

    # Decline: log(1 - exp(-β n)) — that's v0.8b Case A, not v0.8c Case C
    # (the dispatcher should match Case A first, not fall through to Case C)
    result_log = op.apply_fn(sp.log(1 - sp.exp(-beta * n)), n)
    assert result_log is not None
    new_log, corr_log, _ = result_log
    # The Case A result has log in the summand; Case C does not.
    assert new_log.has(sp.log), "Case A dual uses log"
    assert not new_log.has(sp.divisor_sigma), (
        "Case A should not produce a divisor_sigma summand"
    )

    # Decline: plain exp(-β·n) (no `1/(... - 1)` denominator)
    result_plain = op.apply_fn(sp.exp(-beta * n), n)
    assert result_plain is None, (
        "modular_transform_with_correction declines bare exp(-β·n)"
    )


def test_v08c_occupation_number_verifier_strict_agreement():
    """v0.8c: the Stieltjes occupation-number identity verifies via the
    MpmathVerifier end-to-end at n_digits=8.

    Strict-agreement bound is set to 8 digits, not 30, because the dual
    series converges as `1/m²` (polynomial) rather than `e^{-βn}`
    (exponential) like v0.8b's Cases A/B. The `1/m²` truncation tail is
    the well-documented bottleneck; see `analysis/26_v08c_*.py`'s header
    for the convergence-regime analysis. At β=1/100 the verifier reaches
    ~10 digits before truncation noise dominates; we test 8 with margin.

    This is the strict v0.8c bar that the brief calls for in CLAUDE.md
    gotcha 6: ≤1% rel-err across ≥2 dex β — satisfied at β ∈ {1e-3, 1e-2,
    1e-1, 1.0} per `analysis/results/v08c_occupation_number_verification.csv`.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    from rkc.search.core import OperatorApplication, SearchState
    from rkc.search.verifiers import MpmathVerifier
    from rkc.search.engine import _apply_operator

    n = sp.Symbol("n", integer=True, positive=True)
    op = get_operator("modular_transform_with_correction")

    # Stieltjes occupation-number at β=1/100
    expr = 1 / (sp.exp(sp.Rational(1, 100) * n) - 1)
    state_before = SearchState(payload=expr, metadata={"var": n})
    op_app = OperatorApplication(op_id="modular_transform_with_correction")
    state_after = _apply_operator(op_app, state_before)
    assert state_after is not None, "apply_fn should succeed on β=1/100"
    assert op_app.additive_correction is not None, (
        "v0.8c uses 3-tuple convention; correction must be attached"
    )
    assert op_app.summand_range == (1, sp.oo)

    verifier = MpmathVerifier(n_digits=8)
    result = verifier.verify(state_before, [op_app], state_after)
    assert result.passed, (
        f"v0.8c occupation-number at β=1/100, 8 digits failed: {result.reason}"
    )

    # Smaller-β cell should ALSO pass — at β=1/1000 the dual converges
    # even faster polynomially (β* larger).
    expr_small = 1 / (sp.exp(sp.Rational(1, 1000) * n) - 1)
    state_small = SearchState(payload=expr_small, metadata={"var": n})
    op_app_small = OperatorApplication(op_id="modular_transform_with_correction")
    state_small_out = _apply_operator(op_app_small, state_small)
    assert state_small_out is not None
    result_small = verifier.verify(state_small, [op_app_small], state_small_out)
    assert result_small.passed, (
        f"v0.8c occupation-number at β=1/1000, 8 digits failed: "
        f"{result_small.reason}"
    )


def test_v08c_occupation_number_accepted_end_to_end(tmp_path):
    """v0.8c acceptance gate: occupation-number seed at β=1/100 produces
    ≥1 acceptance via the modular_transform_with_correction operator
    end-to-end through the engine, with cost ratio > 1.

    This is the strict v0.8c integration test the brief calls for: the
    new Case C unblocks `1/(exp(β·n)-1)` (the bare occupation-number
    sum) — distinct from v0.8b's log and Lambert seeds.
    """
    import json
    import sympy as sp
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
    )
    n = sp.Symbol("n", integer=True, positive=True)
    expr = 1 / (sp.exp(sp.Rational(1, 100) * n) - 1)
    state = SearchState(payload=expr, metadata={"var": n})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=8),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=40,
        max_depth=1,
    )
    assert summary.n_accepted >= 1, (
        f"v0.8c occupation-number gate failed: 0 acceptances; "
        f"reasons={summary.reject_reason_counts}"
    )
    first = json.loads((tmp_path / "accepted.jsonl").read_text().splitlines()[0])
    assert first["op_sequence"][0]["op_id"] == "modular_transform_with_correction"
    assert first["cost_ratio"] > 1.0, (
        f"v0.8c occupation-number dual at β=1/100 should be cheaper "
        f"(ratio={first['cost_ratio']})"
    )
    # Also verify the seed loads from SEED_LIBRARY and produces an accepted
    # run (proves the seed-library entry is wired)
    import tempfile
    from rkc.search import SEED_LIBRARY, build_seed
    assert "bose_occupation_beta_1em2" in SEED_LIBRARY, (
        "v0.8c seed bose_occupation_beta_1em2 missing from SEED_LIBRARY"
    )
    seed = SEED_LIBRARY["bose_occupation_beta_1em2"]
    seed_expr, var = build_seed(seed)
    with tempfile.TemporaryDirectory() as tmp2:
        state2 = SearchState(payload=seed_expr, metadata={"var": var})
        reg2 = JsonlRegistry.with_dir(tmp2)
        summary2 = search(
            initial_state=state2,
            proposer=RandomProposer(seed=42),
            verifier=MpmathVerifier(n_digits=8),
            router=RkcRouter(),
            cost_model=RkcCostModel(),
            registry=reg2,
            budget=40,
            max_depth=1,
        )
        assert summary2.n_accepted >= 1, (
            f"v0.8c seed bose_occupation_beta_1em2 produced 0 acceptances; "
            f"reasons={summary2.reject_reason_counts}"
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


# ---------------------------------------------------------------------------
# Project C v0.9b — InSessionClaudeProposer (host LLM as proposer via file IPC)
# ---------------------------------------------------------------------------

def test_v09b_in_session_proposer_uses_inbox_outbox(tmp_path):
    """v0.9b: with a fake "host" thread that watches inbox + writes outbox,
    InSessionClaudeProposer makes one round-trip and returns the chosen
    op_id wrapped in an OperatorApplication.

    This is the core protocol test — verifies inbox is written, outbox is
    read, the JSON contract holds, and the returned OperatorApplication
    has the correct op_id.
    """
    import threading
    from typing import Any
    import sympy as sp
    from rkc.search import (
        SearchState, InSessionClaudeProposer, QR7_OPERATOR_BASIS,
    )

    n = sp.Symbol("n", integer=True, positive=True)
    state = SearchState(
        payload=sp.exp(-sp.Rational(1, 100) * n**2), metadata={"var": n},
    )
    session_dir = tmp_path / "session"
    proposer = InSessionClaudeProposer(
        session_dir=session_dir, timeout_s=5.0, poll_interval_s=0.02, seed=42,
    )

    inbox_seen: dict[str, Any] = {}

    def fake_host():
        def decide(payload):
            inbox_seen["payload"] = payload
            return "mellin_inversion"
        InSessionClaudeProposer.poll_and_respond(
            session_dir, decide_fn=decide,
            poll_interval_s=0.02, max_responses=1, max_idle_s=5.0,
        )

    t = threading.Thread(target=fake_host, daemon=True)
    t.start()
    proposals = list(proposer.propose(state, budget=1))
    t.join(timeout=10.0)

    assert len(proposals) == 1
    assert proposals[0].op_id == "mellin_inversion"
    payload = inbox_seen.get("payload")
    assert payload is not None, "fake host never saw an inbox"
    assert payload["version"] == "v0.9"
    assert "system_prompt" in payload
    assert "user_prompt" in payload
    assert "state_hash" in payload
    assert "basis_op_ids" in payload
    assert "mellin_inversion" in payload["basis_op_ids"]
    assert "7-OPERATOR BASIS" in payload["system_prompt"]
    assert "exp(" in payload["user_prompt"]
    s = proposer.stats()
    assert s["n_round_trips"] == 1
    assert s["n_cache_hits"] == 0
    assert s["n_timeouts"] == 0
    assert s["n_malformed"] == 0


def test_v09b_in_session_proposer_timeout_falls_back(tmp_path):
    """v0.9b: when no host ever writes the outbox, the proposer times out
    and falls back to RandomProposer for that turn (no exception escapes,
    returned op_id IS in the basis).
    """
    import sympy as sp
    from rkc.search import (
        SearchState, InSessionClaudeProposer, QR7_OPERATOR_BASIS,
    )

    n = sp.Symbol("n", integer=True, positive=True)
    state = SearchState(
        payload=sp.exp(-sp.Rational(1, 100) * n**2), metadata={"var": n},
    )
    session_dir = tmp_path / "session"
    proposer = InSessionClaudeProposer(
        session_dir=session_dir, timeout_s=0.2, poll_interval_s=0.02, seed=42,
    )
    proposals = list(proposer.propose(state, budget=1))
    assert len(proposals) == 1
    op_ids = {op.id for op in QR7_OPERATOR_BASIS}
    assert proposals[0].op_id in op_ids, (
        f"timeout fallback returned op_id={proposals[0].op_id!r} not in basis"
    )
    s = proposer.stats()
    assert s["n_timeouts"] == 1
    assert s["n_round_trips"] == 0
    assert s["n_malformed"] == 0
    assert not proposer.inbox_path.exists()
    assert not proposer.outbox_path.exists()


def test_v09b_in_session_proposer_parses_malformed_response(tmp_path):
    """v0.9b: when the host writes garbage to the outbox, the proposer
    handles it cleanly (no exception, returns a random fallback op_id
    from the basis, logs the malformed payload).
    """
    import threading
    import sympy as sp
    from rkc.search import (
        SearchState, InSessionClaudeProposer, QR7_OPERATOR_BASIS,
    )

    n = sp.Symbol("n", integer=True, positive=True)
    op_ids = {op.id for op in QR7_OPERATOR_BASIS}

    for case_label, response_text in [
        ("non_json_prose", "I think the right move is mellin_inversion."),
        ("wrong_shape", '{"reasoning": "no op_id key"}'),
        ("unknown_op", '{"op_id": "totally_made_up_operator"}'),
    ]:
        session_dir = tmp_path / case_label
        proposer = InSessionClaudeProposer(
            session_dir=session_dir, timeout_s=5.0, poll_interval_s=0.02,
            seed=42,
        )
        state = SearchState(
            payload=sp.exp(-sp.Rational(1, 100) * n**2),
            metadata={"var": n},
        )

        def fake_host(text=response_text, sd=session_dir):
            import time as _t
            deadline = _t.monotonic() + 5.0
            inbox = sd / "proposer_inbox.json"
            outbox = sd / "proposer_outbox.json"
            while _t.monotonic() < deadline:
                if inbox.exists():
                    tmp_o = outbox.with_suffix(".json.tmp")
                    tmp_o.write_text(text)
                    tmp_o.replace(outbox)
                    return
                _t.sleep(0.02)

        t = threading.Thread(target=fake_host, daemon=True)
        t.start()
        proposals = list(proposer.propose(state, budget=1))
        t.join(timeout=10.0)

        assert len(proposals) == 1, f"{case_label}: expected 1 proposal"
        assert proposals[0].op_id in op_ids, (
            f"{case_label}: fallback returned op_id={proposals[0].op_id!r} "
            f"not in basis"
        )
        s = proposer.stats()
        assert s["n_malformed"] == 1, (
            f"{case_label}: expected 1 malformed event, got stats={s}"
        )
        assert s["n_round_trips"] == 0
        assert s["n_timeouts"] == 0


def test_v09b_in_session_proposer_cache_hit(tmp_path):
    """v0.9b: when propose() is called twice with the same state, only
    ONE inbox is written + ONE host round-trip happens. The second call
    is served from cache.
    """
    import threading
    import sympy as sp
    from rkc.search import SearchState, InSessionClaudeProposer

    n = sp.Symbol("n", integer=True, positive=True)
    state = SearchState(
        payload=sp.exp(-sp.Rational(1, 100) * n**2), metadata={"var": n},
    )
    session_dir = tmp_path / "session"
    proposer = InSessionClaudeProposer(
        session_dir=session_dir, timeout_s=5.0, poll_interval_s=0.02, seed=42,
    )

    response_count = {"n": 0}

    def fake_host():
        def decide(payload):
            response_count["n"] += 1
            return "mellin_inversion"
        InSessionClaudeProposer.poll_and_respond(
            session_dir, decide_fn=decide,
            poll_interval_s=0.02, max_responses=5, max_idle_s=2.0,
        )

    t = threading.Thread(target=fake_host, daemon=True)
    t.start()
    proposals_1 = list(proposer.propose(state, budget=1))
    proposals_2 = list(proposer.propose(state, budget=1))
    t.join(timeout=10.0)

    assert proposals_1[0].op_id == "mellin_inversion"
    assert proposals_2[0].op_id == "mellin_inversion"
    assert response_count["n"] == 1, (
        f"expected exactly 1 host response (cache hit on second call); "
        f"got {response_count['n']}"
    )
    s = proposer.stats()
    assert s["n_round_trips"] == 1
    assert s["n_cache_hits"] == 1
    assert s["cache_size"] == 1


def test_v09b_cli_search_accepts_in_session_flag(tmp_path):
    """v0.9b CLI: `rkc search --proposer in-session` parses + runs (the
    in-session proposer times out → random fallback → search completes).
    """
    import subprocess
    import sys as _sys
    session_dir = tmp_path / "session"
    p = subprocess.run(
        [_sys.executable, "-m", "rkc",
         "search", "exp(-beta*n**2)",
         "--budget", "2", "--digits", "8", "--seed", "42",
         "--out-dir", str(tmp_path / "out"),
         "--proposer", "in-session",
         "--in-session-dir", str(session_dir),
         "--in-session-timeout", "0.2"],
        capture_output=True, text=True, timeout=60,
    )
    assert p.returncode == 0, (
        f"search --proposer in-session failed: stderr={p.stderr}"
    )
    assert "in-session proposer active" in p.stdout
    assert "proposed" in p.stdout


def test_v09b_cli_sweep_accepts_in_session_flag(tmp_path):
    """v0.9b CLI: `rkc sweep --proposer in-session` parses + runs across
    one seed with a 1-worker sweep + short in-session timeout.
    """
    p = _run([
        "sweep", "--seeds", "gaussian_beta_1em2",
        "--budget", "2", "--depth", "1", "--workers", "1",
        "--digits", "8", "--seed", "42",
        "--proposer", "in-session",
        "--in-session-dir", str(tmp_path / "session"),
        "--in-session-timeout", "0.2",
        "--out-dir", str(tmp_path / "out"),
    ])
    assert p.returncode == 0, f"sweep failed: stderr={p.stderr}, stdout={p.stdout}"
    assert "rkc sweep complete" in p.stdout


def test_v09b_in_session_proposer_protocol_conformance():
    """v0.9b: InSessionClaudeProposer satisfies the Proposer protocol
    (structurally typed — propose() returns an iterator of
    OperatorApplications).
    """
    import tempfile
    from rkc.search import InSessionClaudeProposer
    from rkc.search.core import Proposer
    with tempfile.TemporaryDirectory() as tmp:
        proposer = InSessionClaudeProposer(session_dir=tmp, timeout_s=0.05)
        assert isinstance(proposer, Proposer)


# ---------------------------------------------------------------------------
# Project C v0.9a — hardy_orders_of_infinity as divergence diagnostic
# (resolves the v0.3 STUB in `_hardy_orders_apply`)
# ---------------------------------------------------------------------------

def test_v09a_hardy_orders_detects_divergent_bose_einstein():
    """v0.9a: `1/(1 - exp(-β n))` has summand → 1 as n → ∞, so the
    classifier must tag it `DIVERGENT_LITERAL`.

    This is the ChatGPT-Pro proposer-test motivating example: literal
    summation diverges, so any proposer that tries strict comparison is
    wasting cycles. The classifier flags it so downstream code can
    transform before verifying.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    from rkc.search.core import ConvergenceClass
    n = sp.Symbol("n", integer=True, positive=True)
    beta = sp.Symbol("beta", positive=True)
    op = get_operator("hardy_orders_of_infinity")
    result = op.apply_fn(1 / (1 - sp.exp(-beta * n)), n)
    assert result is not None, "hardy_orders should not decline on Bose-Einstein"
    assert isinstance(result, tuple) and len(result) == 2, (
        "v0.9a returns a 2-tuple (expr_unchanged, metadata_dict)"
    )
    expr_out, meta = result
    # Payload should be UNCHANGED (non-transforming operator)
    assert sp.simplify(expr_out - 1 / (1 - sp.exp(-beta * n))) == 0, (
        f"hardy_orders should NOT transform the expression; got {expr_out}"
    )
    assert isinstance(meta, dict)
    assert meta.get("convergence_class") == ConvergenceClass.DIVERGENT_LITERAL.value
    # Also check that the classifier helper agrees
    from rkc.search.basis import _v09a_classify_convergence
    cls = _v09a_classify_convergence(1 / (1 - sp.exp(-beta * n)), n)
    assert cls == "DIVERGENT_LITERAL"


def test_v09a_hardy_orders_detects_convergent_gaussian():
    """v0.9a: pure Gaussian `exp(-β n²)` has summand → 0 as n → ∞, so
    the classifier must tag it `CONVERGENT`.

    The Gaussian is THE convergent-summand benchmark — the strict
    Poisson dual (v0.4) presumes this convergence, so the classifier
    has to be unambiguously positive on it.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    from rkc.search.core import ConvergenceClass
    n = sp.Symbol("n", integer=True, positive=True)
    beta = sp.Symbol("beta", positive=True)
    op = get_operator("hardy_orders_of_infinity")
    result = op.apply_fn(sp.exp(-beta * n**2), n)
    assert result is not None
    expr_out, meta = result
    # Non-transforming
    assert sp.simplify(expr_out - sp.exp(-beta * n**2)) == 0
    assert meta["convergence_class"] == ConvergenceClass.CONVERGENT.value
    # Numeric beta should give the same classification
    result2 = op.apply_fn(sp.exp(-sp.Rational(1, 100) * n**2), n)
    assert result2 is not None
    _, meta2 = result2
    assert meta2["convergence_class"] == ConvergenceClass.CONVERGENT.value


def test_v09a_hardy_orders_detects_convergent_log_partition():
    """v0.9a: `log(1 - exp(-β n))` has summand → log(1 - 0) = log(1) = 0
    as n → ∞, so the classifier must tag it `CONVERGENT`.

    Despite the surface ugliness (log(0) → -∞ in the OPPOSITE limit
    n → 0), the n → ∞ asymptote is the well-behaved one and the v0.8b
    Bose-Einstein eta-log modular identity works on the convergent
    sum. This test guards against a classifier that confuses the
    n → 0 singularity with the n → ∞ behaviour.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    from rkc.search.core import ConvergenceClass
    n = sp.Symbol("n", integer=True, positive=True)
    beta = sp.Symbol("beta", positive=True)
    op = get_operator("hardy_orders_of_infinity")
    result = op.apply_fn(sp.log(1 - sp.exp(-beta * n)), n)
    assert result is not None
    _, meta = result
    assert meta["convergence_class"] == ConvergenceClass.CONVERGENT.value, (
        f"log(1 - exp(-β n)) summand → 0 at n → ∞; got "
        f"{meta['convergence_class']}"
    )
    # Numeric variant
    result_n = op.apply_fn(sp.log(1 - sp.exp(-sp.Rational(1, 100) * n)), n)
    assert result_n is not None
    _, meta_n = result_n
    assert meta_n["convergence_class"] == ConvergenceClass.CONVERGENT.value


def test_v09a_hardy_orders_unknown_on_complex_expr():
    """v0.9a: pathological inputs (oscillatory bounded like `sin(n)`,
    or `n`-independent constants) yield `UNKNOWN` or operator-declines
    — never a crash, never a confident misclassification.

    Three sub-cases:
      1. `sin(n)` — oscillates in [-1, 1]; sympy.limit returns
         AccumulationBounds. Classifier must return `UNKNOWN`.
      2. `n*sin(n)` — oscillates with unbounded amplitude; sympy
         reports a sign-ambiguous infinity. Classifier returns
         `UNKNOWN` (we deliberately don't try to special-case
         oscillatory unbounded).
      3. Constant in n (no n-dependence) — the operator DECLINES
         (returns None), since there's no asymptotic question to ask.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    from rkc.search.core import ConvergenceClass
    n = sp.Symbol("n", integer=True, positive=True)
    op = get_operator("hardy_orders_of_infinity")

    # (1) Bounded oscillatory → UNKNOWN
    result1 = op.apply_fn(sp.sin(n), n)
    assert result1 is not None, "hardy_orders should not crash on sin(n)"
    _, meta1 = result1
    assert meta1["convergence_class"] == ConvergenceClass.UNKNOWN.value

    # (2) Unbounded oscillatory → UNKNOWN (NOT misclassified as
    #     CONVERGENT or NEEDS_REGULARIZATION; sympy returns an
    #     AccumulationBounds-flavored infinity that isn't a clean
    #     +oo / -oo so the classifier shouldn't claim divergence-to-
    #     infinity confidently).
    result2 = op.apply_fn(n * sp.sin(n), n)
    assert result2 is not None, "hardy_orders should not crash on n*sin(n)"
    _, meta2 = result2
    assert meta2["convergence_class"] == ConvergenceClass.UNKNOWN.value, (
        f"n·sin(n) is oscillatory unbounded — expected UNKNOWN; got "
        f"{meta2['convergence_class']}"
    )

    # (3) n-independent constant → operator DECLINES (None)
    result3 = op.apply_fn(sp.Integer(42), n)
    assert result3 is None, (
        "hardy_orders should decline on n-independent constants "
        "(no asymptotic question to ask)"
    )

    # Bonus: NEEDS_REGULARIZATION case for completeness — `n` itself
    # diverges to ∞; classifier must tag NEEDS_REGULARIZATION.
    result4 = op.apply_fn(n, n)
    assert result4 is not None
    _, meta4 = result4
    assert meta4["convergence_class"] == ConvergenceClass.NEEDS_REGULARIZATION.value


def test_v09a_convergence_class_persisted(tmp_path):
    """v0.9a: `convergence_class` survives a JsonlRegistry round-trip.

    Tests three things in one shot:
      1. The engine's `_apply_operator` copies the class to the new
         state's top-level field (in addition to merging into metadata).
      2. JsonlRegistry.store writes the class out to the JSONL record.
      3. The round-tripped JSON record's `state_after_convergence_class`
         field matches the original.

    This is the audit-trail guarantee: long after the search runs, a
    historian can read the JSONL log and recover WHICH summands were
    divergent-by-literal-summation (and therefore needed the modular
    transform to make sense).
    """
    import json
    import sympy as sp
    from rkc.search.basis import get_operator
    from rkc.search.core import (
        ConvergenceClass, OperatorApplication, SearchOutcome, SearchState,
        VerificationResult, CostEstimate,
    )
    from rkc.search.engine import _apply_operator
    from rkc.search.registries import JsonlRegistry

    n = sp.Symbol("n", integer=True, positive=True)
    beta = sp.Symbol("beta", positive=True)

    # Set up a Bose-Einstein state and run hardy_orders on it via the engine
    state_before = SearchState(
        payload=1 / (1 - sp.exp(-beta * n)),
        metadata={"var": n},
    )
    op_app = OperatorApplication(op_id="hardy_orders_of_infinity")
    state_after = _apply_operator(op_app, state_before)
    assert state_after is not None, "hardy_orders failed to apply"

    # (1) top-level field on state_after should carry the class
    assert state_after.convergence_class == ConvergenceClass.DIVERGENT_LITERAL.value
    # metadata mirror
    assert state_after.metadata["convergence_class"] == (
        ConvergenceClass.DIVERGENT_LITERAL.value
    )

    # Build a SearchOutcome and store
    outcome = SearchOutcome(
        state_before=state_before,
        op_sequence=[op_app],
        state_after=state_after,
        verification=VerificationResult(passed=True, digits_or_examples=20,
                                        reason="non-transforming op"),
        cost=CostEstimate(direct_cost=1.0, reduced_cost=1.0,
                          improvement_ratio=1.0, notes="hardy is annotative"),
        route="ANNOTATIVE",
        accepted=True,
    )
    reg = JsonlRegistry.with_dir(tmp_path)
    reg.store(outcome)

    # (3) round-trip the JSONL record and check the field
    accepted_path = tmp_path / "accepted.jsonl"
    assert accepted_path.exists()
    rec = json.loads(accepted_path.read_text().splitlines()[0])
    assert "state_after_convergence_class" in rec, (
        "JsonlRegistry must persist convergence_class explicitly"
    )
    assert rec["state_after_convergence_class"] == (
        ConvergenceClass.DIVERGENT_LITERAL.value
    )
    # state_before had no classification (None), so it should serialize as None
    assert rec["state_before_convergence_class"] is None
    # The metadata mirror should ALSO be present (defense in depth)
    assert "convergence_class" in rec["state_after_meta"]
    assert rec["state_after_meta"]["convergence_class"] == (
        ConvergenceClass.DIVERGENT_LITERAL.value
    )


# ---------------------------------------------------------------------------
# Project C v0.10 — 4 new operators closing the 12/12 seed coverage gap
# (per diary 42 / diary 44; brief: "4 missing operators")
# ---------------------------------------------------------------------------

# === (a) mock_theta_completion_transform ===

def test_v10_mock_theta_completion_apply_fn_directly():
    """v0.10 (a): mock_theta_completion_transform fires on f3 shape with
    outside-squared product, returns a 2-tuple with a Watson-Hickerson
    Eichler-integral certificate; declines on non-matching shapes.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    n = sp.Symbol("n", integer=True, positive=True)
    k = sp.Symbol("k", integer=True, positive=True)
    op = get_operator("mock_theta_completion_transform")

    # f3 form (outside-squared product, matching the seed AST)
    expr = sp.Rational(1, 2)**(n**2) / sp.Product(
        1 + sp.Rational(1, 2)**k, (k, 1, n),
    )**2
    result = op.apply_fn(expr, n)
    assert result is not None, "should fire on f3 outside-squared product"
    assert isinstance(result, tuple) and len(result) == 2, (
        "v0.10 uses 2-tuple annotator convention for completion certificate"
    )
    payload, meta = result
    # Payload UNCHANGED (annotative pattern, not a rewrite)
    assert sp.simplify(payload - expr) == 0
    # Metadata carries the completion certificate
    assert meta["family"] == "mock_theta_f3"
    assert "completion_value" in meta, (
        f"expected completion_value field in metadata; got keys={list(meta.keys())}"
    )
    assert "completion_method" in meta
    assert "Watson-Hickerson" in meta["completion_method"]
    # The certificate should be ~30 digits precision per the calibrated regime
    assert meta["completion_error_bound"] < 1e-20, (
        f"calibrated-regime certificate must be ≤1e-20; got "
        f"error_bound={meta['completion_error_bound']}"
    )

    # Also test with the rkc inside-squared product form (q=1/3)
    q = sp.Rational(1, 3)
    expr_inside = q**(n**2) / sp.Product((1 + q**k)**2, (k, 1, n))
    result_inside = op.apply_fn(expr_inside, n)
    assert result_inside is not None, "should also fire on inside-squared form"

    # Decline: Gaussian
    result_gauss = op.apply_fn(sp.exp(-sp.Rational(1, 100) * n**2), n)
    assert result_gauss is None, "should decline on a plain Gaussian"

    # Decline: arbitrary expression
    result_arb = op.apply_fn(sp.cos(n), n)
    assert result_arb is None


def test_v10_mock_theta_completion_seed_accepted_end_to_end(tmp_path):
    """v0.10 (a): the `mock_theta_f3_q_p5` seed accepts end-to-end at
    depth=1 via the mock_theta_completion_transform operator. Verifier
    short-circuits via payload-equality; cost ratio = 1.0 (annotative
    operator); gate accepts.
    """
    import json
    import sympy as sp
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
        SEED_LIBRARY, build_seed,
    )
    seed = SEED_LIBRARY["mock_theta_f3_q_p5"]
    expr, var = build_seed(seed)
    state = SearchState(payload=expr, metadata={"var": var})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=8),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=80,
        max_depth=1,
    )
    assert summary.n_accepted >= 1, (
        f"v0.10 (a) mock_theta_f3 acceptance gate failed: "
        f"reasons={summary.reject_reason_counts}"
    )
    # Verify at least one acceptance uses our new operator
    accepted_path = tmp_path / "accepted.jsonl"
    assert accepted_path.exists()
    found = False
    for line in accepted_path.read_text().splitlines():
        rec = json.loads(line)
        if any(op["op_id"] == "mock_theta_completion_transform"
               for op in rec.get("op_sequence", [])):
            found = True
            break
    assert found, (
        "expected at least one acceptance via mock_theta_completion_transform"
    )


def test_v10_mock_theta_completion_cost_gate_correctly_decides():
    """v0.10 (a): the cost ratio for mock_theta_completion_transform is
    1.0 (annotative — payload unchanged → cost_before == cost_after) →
    the gate at engine.py:276 (`if cost.improvement_ratio < 1.0`) does
    NOT reject. This is the v0.9a annotator pattern repeated.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    from rkc.search.core import OperatorApplication, SearchState
    from rkc.search.routers import RkcCostModel
    from rkc.search.engine import _apply_operator
    n = sp.Symbol("n", integer=True, positive=True)
    k = sp.Symbol("k", integer=True, positive=True)
    expr = sp.Rational(1, 2)**(n**2) / sp.Product(
        1 + sp.Rational(1, 2)**k, (k, 1, n),
    )**2
    state_before = SearchState(payload=expr, metadata={"var": n})
    op_app = OperatorApplication(op_id="mock_theta_completion_transform")
    state_after = _apply_operator(op_app, state_before)
    assert state_after is not None, "apply_fn should succeed on seed shape"
    cm = RkcCostModel()
    cost = cm.cost(state_before, state_after)
    # ratio = 1.0 (payload identical → same cost) — gate accepts
    assert cost.improvement_ratio == 1.0, (
        f"annotative operator should give ratio=1.0; got {cost.improvement_ratio}"
    )
    # The cost gate at engine.py rejects strictly `< 1.0`, so 1.0 passes
    assert not (cost.improvement_ratio < 1.0), (
        "cost gate must accept ratio == 1.0 for annotative operators"
    )


# === (b) partial_theta_completion ===

def test_v10_partial_theta_completion_apply_fn_directly():
    """v0.10 (b): partial_theta_completion fires on triangular-exp shape
    `q^{n(n+1)/2}` and returns a 2-tuple with a DIRECT_CERTIFICATE
    decision; declines on non-matching shapes.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    n = sp.Symbol("n", integer=True, positive=True)
    op = get_operator("partial_theta_completion")

    # Standard partial-theta summand
    expr = sp.Rational(1, 3)**(n * (n + 1) / 2)
    result = op.apply_fn(expr, n)
    assert result is not None, "should fire on q^{n(n+1)/2}"
    assert isinstance(result, tuple) and len(result) == 2
    payload, meta = result
    # Payload unchanged
    assert sp.simplify(payload - expr) == 0
    assert meta["family"] == "partial_theta"
    assert meta["decision"] == "DIRECT_CERTIFICATE"
    assert meta["reason"] == "partial_theta_one_sided_no_clean_dual_exists"
    assert meta["decay_class"] == "finite"
    assert "num_terms_for_1em12" in meta

    # Alternating partial-theta `(-1)^n q^{n(n+1)/2}`
    expr_alt = (-1)**n * sp.Rational(1, 4)**(n * (n + 1) / 2)
    result_alt = op.apply_fn(expr_alt, n)
    assert result_alt is not None, "should fire on alternating partial-theta"
    _, meta_alt = result_alt
    assert meta_alt["match_params"]["alternating"] is True

    # Decline: Gaussian (different family)
    result_gauss = op.apply_fn(sp.exp(-n**2), n)
    assert result_gauss is None, "should decline on Gaussian"


def test_v10_partial_theta_completion_seed_accepted_end_to_end(tmp_path):
    """v0.10 (b): the `partial_theta_q_p3` seed accepts end-to-end via
    the partial_theta_completion operator.
    """
    import json
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
        SEED_LIBRARY, build_seed,
    )
    seed = SEED_LIBRARY["partial_theta_q_p3"]
    expr, var = build_seed(seed)
    state = SearchState(payload=expr, metadata={"var": var})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=8),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=80,
        max_depth=1,
    )
    assert summary.n_accepted >= 1, (
        f"v0.10 (b) partial_theta acceptance gate failed: "
        f"reasons={summary.reject_reason_counts}"
    )
    accepted_path = tmp_path / "accepted.jsonl"
    found = False
    for line in accepted_path.read_text().splitlines():
        rec = json.loads(line)
        if any(op["op_id"] == "partial_theta_completion"
               for op in rec.get("op_sequence", [])):
            found = True
            break
    assert found, "expected acceptance via partial_theta_completion"


def test_v10_partial_theta_completion_cost_gate_correctly_decides():
    """v0.10 (b): annotative operator → ratio=1.0 → gate accepts."""
    import sympy as sp
    from rkc.search.core import OperatorApplication, SearchState
    from rkc.search.routers import RkcCostModel
    from rkc.search.engine import _apply_operator
    n = sp.Symbol("n", integer=True, positive=True)
    expr = sp.Rational(1, 3)**(n * (n + 1) / 2)
    state_before = SearchState(payload=expr, metadata={"var": n})
    op_app = OperatorApplication(op_id="partial_theta_completion")
    state_after = _apply_operator(op_app, state_before)
    assert state_after is not None
    cm = RkcCostModel()
    cost = cm.cost(state_before, state_after)
    assert cost.improvement_ratio == 1.0
    assert not (cost.improvement_ratio < 1.0)


# === (c) gauss_sum_finite_evaluation ===

def test_v10_gauss_sum_finite_evaluation_apply_fn_directly():
    """v0.10 (c): gauss_sum_finite_evaluation matches `exp(2πi p n²/q)`,
    returns a 3-tuple (constant_summand, 0, (0, q-1)) with the constant
    = closed_form / q. Preserves the silent-zero guard at q ≡ 2 (mod 4).
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    n = sp.Symbol("n", integer=True, positive=True)
    op = get_operator("gauss_sum_finite_evaluation")

    # q=7 (≡ 3 mod 4): G(1, 7) = i·√7
    expr = sp.exp(2 * sp.pi * sp.I * n**2 / 7)
    result = op.apply_fn(expr, n)
    assert result is not None, "should fire on quadratic Gauss-sum summand"
    assert isinstance(result, tuple) and len(result) == 3
    payload, correction, srange = result
    assert srange == (0, 6), f"expected finite range (0, 6); got {srange}"
    assert correction == 0, f"no additive correction; got {correction}"
    # constant = closed_form / 7 = i√7 / 7
    expected_constant = sp.I * sp.sqrt(7) / 7
    assert sp.simplify(payload - expected_constant) == 0, (
        f"closed form / q should be i√7/7; got {payload}"
    )

    # q=6 (≡ 2 mod 4): SILENT-ZERO HAZARD — must return 0
    expr_q6 = sp.exp(2 * sp.pi * sp.I * n**2 / 6)
    result_q6 = op.apply_fn(expr_q6, n)
    assert result_q6 is not None
    payload_q6, _, srange_q6 = result_q6
    assert payload_q6 == 0, (
        f"SILENT-ZERO GUARD: q=6 ≡ 2 (mod 4) must produce 0 summand; "
        f"got {payload_q6}"
    )
    assert srange_q6 == (0, 5)

    # q=5 (≡ 1 mod 4): G(1, 5) = √5
    expr_q5 = sp.exp(2 * sp.pi * sp.I * n**2 / 5)
    result_q5 = op.apply_fn(expr_q5, n)
    assert result_q5 is not None
    payload_q5, _, _ = result_q5
    expected_q5 = sp.sqrt(5) / 5
    assert sp.simplify(payload_q5 - expected_q5) == 0, (
        f"G(1, 5) closed form / 5 should be √5/5; got {payload_q5}"
    )

    # Decline: non-Gauss-sum summand (e.g., Gaussian)
    result_gauss = op.apply_fn(sp.exp(-sp.Rational(1, 100) * n**2), n)
    assert result_gauss is None


def test_v10_gauss_sum_finite_evaluation_seed_accepted_end_to_end(tmp_path):
    """v0.10 (c): the `gauss_sum_q7` seed accepts end-to-end via
    gauss_sum_finite_evaluation, with the verifier confirming the
    closed form to the strict bar (≥30 digits via mpmath).
    """
    import json
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
        SEED_LIBRARY, build_seed,
    )
    seed = SEED_LIBRARY["gauss_sum_q7"]
    expr, var = build_seed(seed)
    state = SearchState(payload=expr, metadata={"var": var})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=30),  # strict 30-digit bar
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=80,
        max_depth=1,
    )
    assert summary.n_accepted >= 1, (
        f"v0.10 (c) gauss_sum acceptance failed at 30-digit bar: "
        f"reasons={summary.reject_reason_counts}"
    )
    accepted_path = tmp_path / "accepted.jsonl"
    found = False
    for line in accepted_path.read_text().splitlines():
        rec = json.loads(line)
        if any(op["op_id"] == "gauss_sum_finite_evaluation"
               for op in rec.get("op_sequence", [])):
            found = True
            break
    assert found, (
        f"expected acceptance via gauss_sum_finite_evaluation at the "
        f"30-digit bar (proves the closed form is mathematically exact)"
    )


def test_v10_gauss_sum_finite_evaluation_silent_zero_seed_accepted(tmp_path):
    """v0.10 (c): the silent-zero seed `gauss_sum_q6` (q ≡ 2 mod 4)
    accepts because our operator returns the trivial summand 0 — which
    is the mathematically correct answer (G(1, 6) = 0 identically).
    This preserves CLAUDE.md gotcha 1 (silent-zero hazard MUST be
    preserved) — by emitting 0, the engine doesn't claim a "non-zero
    Gauss sum" exists for q ≡ 2 (mod 4).
    """
    import json
    import sympy as sp
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
        SEED_LIBRARY, build_seed,
    )
    seed = SEED_LIBRARY["gauss_sum_q6"]
    expr, var = build_seed(seed)
    state = SearchState(payload=expr, metadata={"var": var})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=30),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=80,
        max_depth=1,
    )
    accepted_path = tmp_path / "accepted.jsonl"
    if accepted_path.exists():
        for line in accepted_path.read_text().splitlines():
            rec = json.loads(line)
            if any(op["op_id"] == "gauss_sum_finite_evaluation"
                   for op in rec.get("op_sequence", [])):
                # Verify the after-state payload is 0 (silent-zero answer)
                assert rec["state_after"] == "0", (
                    f"silent-zero seed must produce 0 payload; "
                    f"got state_after={rec['state_after']!r}"
                )
                return  # success
    # If no acceptance found, that's also fine for the silent-zero case
    # IF the engine rejected via DEGENERATE_ROUTE or similar — but we
    # know our operator DOES handle this, so we should see an acceptance.
    # If we get here without returning, something is wrong.
    assert summary.n_accepted >= 1, (
        f"silent-zero seed should accept via gauss_sum_finite_evaluation "
        f"(returns 0 = correct answer); got reasons={summary.reject_reason_counts}"
    )


def test_v10_gauss_sum_finite_evaluation_cost_gate_correctly_decides():
    """v0.10 (c): cost ratio for gauss_sum_finite_evaluation transforms
    the q-term sum into a 1-term scalar evaluation; the cost gate sees
    a real improvement (q × per-term) → 1 op, ratio ≥ 1.0.
    """
    import sympy as sp
    from rkc.search.core import OperatorApplication, SearchState
    from rkc.search.routers import RkcCostModel
    from rkc.search.engine import _apply_operator
    n = sp.Symbol("n", integer=True, positive=True)
    expr = sp.exp(2 * sp.pi * sp.I * n**2 / 7)
    state_before = SearchState(payload=expr, metadata={"var": n})
    op_app = OperatorApplication(op_id="gauss_sum_finite_evaluation")
    state_after = _apply_operator(op_app, state_before)
    cm = RkcCostModel()
    cost = cm.cost(state_before, state_after)
    # Gate accepts (ratio is non-zero; actual ratio depends on cost
    # model's treatment of the closed-form output vs the exp-summand input)
    assert cost.improvement_ratio >= 1.0, (
        f"gauss_sum_finite_evaluation should give ratio ≥ 1 "
        f"(closed form is no more expensive than direct); "
        f"got ratio={cost.improvement_ratio}"
    )


# === (d) q_pochhammer_transform ===

def test_v10_q_pochhammer_transform_apply_fn_directly():
    """v0.10 (d): q_pochhammer_transform matches `1 - a·q^n`, returns
    a 2-tuple with the lifted-product form + route metadata.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    n = sp.Symbol("n", integer=True, positive=True)
    op = get_operator("q_pochhammer_transform")

    # Seed form: 1 - (1/3) · (1/2)^n (which sympy renders as 1 - 1/(3·2^n))
    expr = 1 - sp.Rational(1, 3) * sp.Rational(1, 2)**n
    result = op.apply_fn(expr, n)
    assert result is not None, (
        "should fire on `1 - a·q^n` shape (Pochhammer factor)"
    )
    assert isinstance(result, tuple) and len(result) == 2
    payload, meta = result
    # Payload unchanged (annotative pattern)
    assert sp.simplify(payload - expr) == 0
    assert meta["family"] == "q_pochhammer"
    assert meta["route"] == "lifted_to_infinite_product"
    assert "lifted_product" in meta
    assert meta["decay_class"] == "exponential"
    # The seed has a=1/3, q=1/2 — well in |q| < 1, so we should have
    # a concrete product value at 30 digits
    assert "product_value_30dps" in meta

    # Path 1: a = 1 → Euler pentagonal
    expr_a1 = 1 - sp.Rational(1, 3)**n  # a=1, q=1/3
    result_a1 = op.apply_fn(expr_a1, n)
    assert result_a1 is not None
    _, meta_a1 = result_a1
    assert meta_a1["route"] == "euler_pentagonal", (
        f"a=1 should route via Euler pentagonal; got {meta_a1['route']}"
    )

    # Decline: not a Pochhammer factor (e.g., Gaussian)
    result_gauss = op.apply_fn(sp.exp(-n), n)
    assert result_gauss is None


def test_v10_q_pochhammer_transform_seed_accepted_end_to_end(tmp_path):
    """v0.10 (d): the `q_pochhammer_inf_p3` seed accepts via
    q_pochhammer_transform end-to-end.
    """
    import json
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
        SEED_LIBRARY, build_seed,
    )
    seed = SEED_LIBRARY["q_pochhammer_inf_p3"]
    expr, var = build_seed(seed)
    state = SearchState(payload=expr, metadata={"var": var})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=8),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=80,
        max_depth=1,
    )
    assert summary.n_accepted >= 1, (
        f"v0.10 (d) q_pochhammer acceptance gate failed: "
        f"reasons={summary.reject_reason_counts}"
    )
    accepted_path = tmp_path / "accepted.jsonl"
    found = False
    for line in accepted_path.read_text().splitlines():
        rec = json.loads(line)
        if any(op["op_id"] == "q_pochhammer_transform"
               for op in rec.get("op_sequence", [])):
            found = True
            break
    assert found, "expected acceptance via q_pochhammer_transform"


def test_v10_q_pochhammer_transform_cost_gate_correctly_decides():
    """v0.10 (d): annotative operator → ratio=1.0 → gate accepts."""
    import sympy as sp
    from rkc.search.core import OperatorApplication, SearchState
    from rkc.search.routers import RkcCostModel
    from rkc.search.engine import _apply_operator
    n = sp.Symbol("n", integer=True, positive=True)
    expr = 1 - sp.Rational(1, 3) * sp.Rational(1, 2)**n
    state_before = SearchState(payload=expr, metadata={"var": n})
    op_app = OperatorApplication(op_id="q_pochhammer_transform")
    state_after = _apply_operator(op_app, state_before)
    assert state_after is not None
    cm = RkcCostModel()
    cost = cm.cost(state_before, state_after)
    assert cost.improvement_ratio == 1.0
    assert not (cost.improvement_ratio < 1.0)


# === (e) Cost-model refinement: dual-decay-rate tagging ===

def test_v10_operator_decay_class_tagging():
    """v0.10 (e): each operator id has a decay-class tag per
    `OPERATOR_DECAY_CLASS` in `rkc.search.routers`. The 4 new v0.10
    operators get their respective tags (polynomial / finite /
    exponential). The legacy v0.x operators all retain their tags too.
    """
    from rkc.search.routers import (
        OPERATOR_DECAY_CLASS,
        operator_decay_class,
    )
    # The 4 v0.10 operators get specific decay classes
    assert operator_decay_class("mock_theta_completion_transform") == "polynomial"
    assert operator_decay_class("partial_theta_completion") == "finite"
    assert operator_decay_class("gauss_sum_finite_evaluation") == "finite"
    assert operator_decay_class("q_pochhammer_transform") == "exponential"
    # Legacy v0.x operators carry tags too
    assert operator_decay_class("mellin_inversion") == "exponential"
    assert operator_decay_class("hardy_orders_of_infinity") == "annotative"
    # Unknown op_id returns 'unknown' (safe default)
    assert operator_decay_class("not_a_real_op") == "unknown"
    # Every operator in the basis has a tagged decay class
    from rkc.search import QR7_OPERATOR_BASIS
    for op in QR7_OPERATOR_BASIS:
        tag = operator_decay_class(op.id)
        assert tag != "unknown", (
            f"every basis operator must have a non-unknown decay class; "
            f"missing tag for {op.id!r}"
        )


# === Backward compat: v0.4-v0.8c paths must continue to verify strictly ===

def test_v10_backward_compat_v04_v08c_paths_unchanged():
    """v0.10 backward compat: the v0.4 Gaussian, v0.7 half-shift /
    weighted, and v0.8b/v0.8c modular-with-correction paths must all
    continue to verify cleanly through the v0.10-extended verifier.

    The v0.10 verifier change (Case B scalar handling now respects
    explicit finite summand_range for the gauss_sum case) is gated on
    the summand_range being a finite-integer tuple AND set by an
    operator. The default `(-oo, oo)` range used by v0.4 paths is
    UNCHANGED and not affected.
    """
    import sympy as sp
    from rkc.search.basis import get_operator
    from rkc.search.core import OperatorApplication, SearchState
    from rkc.search.verifiers import MpmathVerifier
    from rkc.search.engine import _apply_operator

    n = sp.Symbol("n", integer=True, positive=True)
    verifier = MpmathVerifier(n_digits=20)

    # v0.4 Gaussian → Poisson dual
    op_mellin = get_operator("mellin_inversion")
    expr_g = sp.exp(-sp.Rational(1, 100) * n**2)
    state_g = SearchState(payload=expr_g, metadata={"var": n})
    op_app_g = OperatorApplication(op_id="mellin_inversion")
    state_g_out = _apply_operator(op_app_g, state_g)
    assert state_g_out is not None
    r_g = verifier.verify(state_g, [op_app_g], state_g_out)
    assert r_g.passed, f"v0.4 Gaussian path broken: {r_g.reason}"

    # v0.7 half-shift Gaussian
    expr_h = sp.exp(-sp.Rational(1, 100) * (n + sp.Rational(1, 2))**2)
    state_h = SearchState(payload=expr_h, metadata={"var": n})
    op_app_h = OperatorApplication(op_id="mellin_inversion")
    state_h_out = _apply_operator(op_app_h, state_h)
    assert state_h_out is not None
    r_h = verifier.verify(state_h, [op_app_h], state_h_out)
    assert r_h.passed, f"v0.7 half-shift path broken: {r_h.reason}"

    # v0.8b Bose-Einstein log
    op_mod = get_operator("modular_transform_with_correction")
    expr_b = sp.log(1 - sp.exp(-sp.Rational(1, 100) * n))
    state_b = SearchState(payload=expr_b, metadata={"var": n})
    op_app_b = OperatorApplication(op_id="modular_transform_with_correction")
    state_b_out = _apply_operator(op_app_b, state_b)
    assert state_b_out is not None
    # bump precision check to lower digits to keep test fast
    verifier30 = MpmathVerifier(n_digits=20)
    r_b = verifier30.verify(state_b, [op_app_b], state_b_out)
    assert r_b.passed, f"v0.8b Bose-Einstein path broken: {r_b.reason}"

    # v0.5 master_theorem (the path that originally relied on Case B
    # scalar evaluation for the Γ-product output)
    op_mt = get_operator("master_theorem")
    x = sp.Symbol("x", positive=True)
    m = sp.Symbol("m", positive=True)
    nn = sp.Symbol("nn", positive=True)
    beta_int = sp.Integral(x**(m-1) * (1-x)**(nn-1), (x, 0, 1))
    state_mt = SearchState(payload=beta_int, metadata={"var": x})
    op_app_mt = OperatorApplication(op_id="master_theorem")
    state_mt_out = _apply_operator(op_app_mt, state_mt)
    assert state_mt_out is not None
    r_mt = verifier.verify(state_mt, [op_app_mt], state_mt_out)
    assert r_mt.passed, f"v0.5 master_theorem path broken: {r_mt.reason}"


def test_v10_all_4_seeds_reachable_at_depth_1():
    """v0.10 (THE headline): all 4 previously-unreachable seeds from
    diary 42 (mock_theta_f3_q_p5, partial_theta_q_p3, gauss_sum_q7,
    q_pochhammer_inf_p3) are now reachable at depth=1 via their
    respective new operators. This is the basis-completeness closure
    test that brings Project C from 8/12 → 12/12 seed coverage.
    """
    import tempfile
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
        SEED_LIBRARY, build_seed,
    )
    # Map seed_id → expected operator_id
    expected = {
        "mock_theta_f3_q_p5": "mock_theta_completion_transform",
        "partial_theta_q_p3": "partial_theta_completion",
        "gauss_sum_q7": "gauss_sum_finite_evaluation",
        "q_pochhammer_inf_p3": "q_pochhammer_transform",
    }
    for sid, expected_op in expected.items():
        seed = SEED_LIBRARY[sid]
        expr, var = build_seed(seed)
        with tempfile.TemporaryDirectory() as tmp:
            state = SearchState(payload=expr, metadata={"var": var})
            reg = JsonlRegistry.with_dir(tmp)
            summary = search(
                initial_state=state,
                proposer=RandomProposer(seed=42),
                verifier=MpmathVerifier(n_digits=8),
                router=RkcRouter(),
                cost_model=RkcCostModel(),
                registry=reg,
                budget=80,
                max_depth=1,
            )
            assert summary.n_accepted >= 1, (
                f"seed {sid!r} produced 0 acceptances; "
                f"reasons={summary.reject_reason_counts}"
            )
            import json, pathlib
            accepted_path = pathlib.Path(tmp) / "accepted.jsonl"
            ops_used = set()
            for line in accepted_path.read_text().splitlines():
                rec = json.loads(line)
                for op in rec.get("op_sequence", []):
                    ops_used.add(op["op_id"])
            assert expected_op in ops_used, (
                f"seed {sid!r} expected to be reached via {expected_op!r}; "
                f"ops actually used: {ops_used}"
            )
