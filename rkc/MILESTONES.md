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

## v0.3 — Project C: RKC-guided symbolic search (W5 / T3 / X3)

Full design: [../insights/PROJECT_C_DESIGN.md](../insights/PROJECT_C_DESIGN.md).

**Project C** = the "practical Ramanujan latent speedrun" system. The
6-step loop: choose expression → neural model proposes operator sequence
→ rkc normalizes and routes → verifier tests to high precision → cost
model decides usefulness → store accepted identity or reject with reason.

Three sub-milestones:

- **v0.3.0 — Project C v0 (W5)**: pure-symbolic baseline (`RandomProposer`).
  Validates steps 3+4+5+6 end-to-end on the Hunt 5 7-operator basis.
  Output: `rkc/search/` module + CLI `rkc search`. ~1-2 weeks.
- **v0.3.1 — Project C v1 (T3)**: adds `NeuralProposer`. Nonlinear ICA /
  JEPA per Hyvärinen et al. arXiv 2303.16535 is the default architectural
  choice but the `Proposer` interface is modular.
- **v0.3.2 — Project C v2 (X3)**: extract `rkc.search` interface as a
  shared package so arc-agi-ebm-agent's program-induction loop can plug
  in ARC's DSL as a second instance.

Validation case for v0.3.0: random composition recovering ≥80% of the
11 known kernel identities in the rkc registry within budget=1000
compositions of length ≤3.

## Non-goals (for now)

- A full SymPy integration (use SymPy for AST parsing only; don't try to
  replace its evaluation logic).
- A general theorem-proving framework (use mpmath / PSLQ as the
  numerical-only verifier).
- Symbolic differentiation through routed evaluations (out of scope).
- Distributed evaluation (single-process is fine for v0.1-v0.3).
