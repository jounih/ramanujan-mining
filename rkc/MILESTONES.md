# rkc roadmap — milestones

Status as of 2026-05-24: the package is currently a research-quality
recognizer + routing benchmark. It is not yet a tool other people can
pick up and use. The headline target — per parallel-Claude review and
[insights/BIG_IDEAS_REVIEW.md](../insights/BIG_IDEAS_REVIEW.md) — is to
ship **rkc v0.1** as a usable degeneracy-aware special-function routing
compiler with a CLI + stable Python API.

## v0 — research artefact (SHIPPED)

What exists today:
- 11 registered kernel families with per-kernel matchers + degeneracy detectors.
- 55/55 = 100% on the routing benchmark (macro precision 1.00).
- 50/50 unit tests passing.
- `MODULAR_COMPLETION_REQUIRED` route end-to-end on f3 mock theta (Watson-
  Hickerson Eichler integral; ≥30 digits with certificate).
- f5/f7 surface `CompletionNotImplemented` honestly.
- Cost estimator using per-term complexity, not bits-per-term.
- Silent-zero hazard guarded at Gauss sums q ≡ 2 mod 4.

Internal modules: `recognizer.py`, `registry.py`, `routing.py`, `costs.py`,
`completions.py`. Tests in `tests/`. README is a 1-page worked example.

## v0.1 — usable tool (TARGET)

The minimum useful version someone else could pick up. Three additions:

### A. CLI

A `rkc` command (entry point) wrapping the existing recognizer/router:

```
rkc recognize "exp(-beta*n**2)" --var n
    → recognized: gaussian_quadratic
    → kernel_id: theta_3
    → confidence: 1.00

rkc compare "Sum(exp(-beta*n**2), (n, -oo, oo))" --beta 1e-8 --digits 80
    → direct: 151745 terms estimated, n_terms_certified ~ 151745
    → dual:    3 terms estimated, n_terms_certified ~ 3
    → recommended_route: dual
    → estimated_speedup: 50_581x
    → certificate: erfc_tail; truncation_error_bound = 1.04e-81

rkc certify "Sum(KroneckerDelta(n % q, r) * exp(2*pi*I*n*x/q), (n, 0, q-1))" --q 6 --r 2
    → degeneracy_check: q ≡ 2 mod 4 with non-trivial r → SILENT_ZERO_HAZARD
    → recommended_route: FINITE_DIRECT (do not use dual)
    → certificate: degeneracy_detector fired

rkc benchmark examples/theta_gaussian.yaml
    → reads yaml of (expr, params) cells; prints a per-cell speedup table
```

### B. Python API

```python
from rkc import route, recognize, certify

# One-shot: identify + route + certify + numerical answer
result = route(
    "Sum(exp(-beta*n**2), (n, -oo, oo))",
    var="n",
    params={"beta": 1e-8},
    digits=80,
)
print(result.recognized)          # "gaussian_quadratic"
print(result.best_route)          # "dual"
print(result.estimated_speedup)   # 50_581.0
print(result.certificate)         # CertificateBundle(...)
print(result.value)               # mpf value to 80 digits
```

The internal `recognize()` and `certify()` functions are also exposed for
users who want to plug into their own evaluation loop.

### C. Coverage table

A tested, documented coverage matrix in the README:

| Family | Recognize | Routes | Certify | Degeneracy guard | Benchmark |
|---|---|---|---|---|---|
| Gaussian theta (Σ exp(−βn²)) | yes | direct / dual | yes | yes | yes |
| Bose-Einstein partition (Π (1−e^(−βn))⁻¹) | yes | direct / modular | partial | yes | yes |
| Lambert / Eisenstein | yes | direct / modular | partial | yes | yes |
| Gauss sum | yes | finite / direct | yes | yes (q≡2 mod 4) | yes |
| Mock theta f3 | yes | completion (Watson-Hickerson) | partial | yes (char parity) | yes |
| Mock theta f5, f7 | yes | completion (NotImplemented) | n/a | yes | n/a |
| q-Pochhammer (a;q)_∞ | yes | direct | partial | partial | yes |
| Partial theta | yes | direct | partial | partial | yes |
| Dirichlet L | yes | direct | partial | partial | yes |
| Divisor sum σ_k | yes | direct / Möbius / Lambert sieve | partial | partial | yes |

(All values "yes" today for the recognize column per the 55/55 benchmark;
the gaps to close for v0.1 are in the Certify / Benchmark columns.)

### Gates for v0.1 release

1. `rkc` CLI installed via `pip install -e .` runs the four commands above.
2. The Python API surface (`route`, `recognize`, `certify`) is stable and
   documented; `tests/test_api.py` covers the public contract.
3. README walks through a worked example for each kernel family.
4. `examples/` directory has one YAML per family + a CI-runnable
   `python -m rkc.bench` that produces the coverage table.
5. All 50/50 existing tests still green; CLI tests added.
6. CHANGELOG.md tracks the v0 → v0.1 delta.

## v0.2 — transform-family expansion (NEXT)

After v0.1 ships, expand the registry with families informed by the
unblocked Hunts:

- **Eisenstein continued fractions** (Hunt 3 / T2): clustered family from
  Berndt NB Part V Ch. 32 + Berndt-Yee 2002. Quasi-modular (weight-2
  anomaly) territory. Concrete output: `eisenstein_cf_family_N` registry
  entry, with the Hunt 3 clustering as the design rationale.
- **Mellin-pair αβ=1 reciprocity** (H10 / T4): from Berndt-Dixit 2009.
  Opens routable computations involving Γ'/Γ + Riemann Ξ; potentially
  relevant to anomalous-diffusion / fractional-operator / spectral-sum
  kernels.
- **Umbral operator primitives** (W6): from QR III §12. Shift E,
  difference Δ, Riemann-Liouville D^α as composable operators rather than
  individual kernels. Structurally the natural lens for the recognizer
  (operates on generating functions).
- **f5 / f7 Watson-Hickerson instrumentation** (H3): close out
  `CompletionNotImplemented` on the higher-order mock thetas using
  Hickerson 1988 / Berndt-Chan.

## v0.3 — Project C: RKC-guided symbolic search (W5 / T3 / X3) — SHIPPED (v0.3.0 → v0.7) ✓

Full design: [../insights/PROJECT_C_DESIGN.md](../insights/PROJECT_C_DESIGN.md).

**Project C** = the "practical Ramanujan latent speedrun" system. The
6-step loop: choose expression → proposer suggests operator sequence
→ rkc normalizes and routes → verifier tests to high precision → cost
model decides usefulness → store accepted identity or reject with reason.

### Shipped (incremental):

- **v0.3 scaffold (SHIPPED)** — core dataclasses + Protocols + RandomProposer,
  MpmathVerifier, RkcRouter, RkcCostModel, JsonlRegistry. `rkc search` CLI
  works end-to-end on the Hunt 5 7-operator basis (stubs except master_theorem
  and mellin_inversion, which v0.4-v0.7 fleshed out).
- **v0.4 (SHIPPED, diary 14b)** — first concrete operator transformation:
  `mellin_inversion` on pure Gaussian `exp(-βn²)` via Poisson summation
  (Σ_n exp(-βn²) ↔ √(π/β)·Σ_k exp(-π²k²/β)); ~54× cost-ratio at β=1/100.
- **v0.5 (SHIPPED, commit `3cbe013`)** — master_theorem on canonical
  Mellin-transform integrals: Beta function, Gamma function, π/sin(πs).
  sp.Integral handling in MpmathVerifier via mp.quad.
- **v0.6 (SHIPPED, commit `a47e71a`)** — multi-step composition (`max_depth>1`).
  Engine chains operator applications and verifies initial ↔ final state.
- **v0.6+ (SHIPPED, commit `a7d3bcc`)** — 15-seed library + parallel sweep
  harness via `multiprocessing.Pool('spawn')`. `rkc sweep --workers N`.
- **v0.7 (SHIPPED, diary 26, commit `f1758d3`)** — two additional strict
  Poisson identity classes within `mellin_inversion`: half-shifted Gaussian
  (theta₂/theta₄ partner) and weighted Gaussian (n²·exp(-βn²) second moment).
  Both verified to numerical zero across 6 orders of magnitude in β.
  Tests: 73/73 passing.

- **v0.8b SHIPPED (diary 31)** — `OperatorApplication` extended with
  `additive_correction` + `summand_range` fields (None-default for
  backward compat); `MpmathVerifier` folds the correction into the
  comparison; new `modular_transform_with_correction` operator handles
  log-Bose-Einstein (Dedekind eta-derived) and Lambert (E_2
  quasi-modular) one-sided summands. Both verified to rel-err ≤ 1e-30
  at dps=80 across 4 dex of β. Basis is now 8 ops. 87/87 tests passing.

### Next (queued):

- **v0.3.1 — NeuralProposer (T3)** — gated until basis grows past 10-20
  operators. Per PROJECT_C_DESIGN, nonlinear ICA / JEPA is the default
  architectural choice but the `Proposer` interface is modular.
- **v0.3.2 — Cross-repo extraction (X3)** — pull `Proposer / Verifier /
  Router / CostModel / Registry` interfaces into a shared
  `compositional_search` package so arc-agi-ebm-agent can plug in ARC's
  DSL as a second instance.

### Validation target (still pending):

≥80% of the 11 known kernel identities in the rkc registry recovered by
random composition within budget=1000 compositions of length ≤3. Current
state (v0.8b): the engine recovers Gaussian / half-shift / weighted-Gaussian
strict identities + Beta/Gamma/π-sin Mellin integrals + log-Bose-Einstein +
Lambert (8 of 11). Mock-theta f3 + partial theta + Gauss-sum + q-Pochhammer
remain gated on dedicated apply_fn implementations.

## Non-goals (for now)

- A full SymPy integration (use SymPy for AST parsing only; don't try to
  replace its evaluation logic).
- A general theorem-proving framework (use mpmath / PSLQ as the
  numerical-only verifier).
- Symbolic differentiation through routed evaluations (out of scope).
- Distributed evaluation (single-process is fine for v0.1-v0.3).
