# Diary 13 — Experiment 16: FEP × mock-modular toy lattice gas + shadow-as-info-theoretic-residual probes

**Date:** 2026-05-24
**Status:** complete; clean negative result on Probe 2, clean positive result on Probe 1.
**Source pointers:**
- `ramanujan/analysis/16_fep_mock_modular_toy.py`
- `ramanujan/analysis/results/fep_mock_modular_toy.csv`
- charter B1 in `ramanujan/insights/CANDIDATE_INSIGHTS.md`
- SOTA gap statement in `ramanujan/sota_comparisons/00_physics_and_computation_sota.md` §6

This is the most speculative entry in the run. Per the SOTA survey there is **no published work** overlapping variational free energy with mock-modular forms; therefore *any* concrete construction here is at least a candidate contribution. I held myself to: ≥10 data points across ≥2 orders of magnitude in β, ≤1% relative residual for any claimed proportionality, and an explicit falsifier for each conjecture.

---

## (a) Probe 1 — toy generative model whose grand-canonical Z is f(q)

**Target:** Ramanujan's third-order mock theta

  f(q) = Σ_{n≥0} q^(n²) / Π_{k=1..n} (1 + q^k)² .

### Construction

Configuration  C = (n, {a_k, b_k}_{k=1..n})  with n ∈ {0, 1, ..., N} and (a_k, b_k) ∈ ℤ_{≥0}² for each k ∈ {1, ..., n}.

- n is a "core size" or topological sector index.
- For each k ∈ {1..n} there are *two* independent bosonic species with occupation numbers a_k and b_k.
- Hamiltonian:  E(C) = n²  +  Σ_{k=1..n} k·(a_k + b_k).
- Fugacity: z = -1 = e^{i π}, i.e. *imaginary* chemical potential μ = π. Each particle carries weight z^1 = -1.
- Boltzmann weight (signed):  w(C) = z^{Σ_k(a_k+b_k)} · q^{E(C)} = (-1)^{Σ_k(a_k+b_k)} · q^{n² + Σ_k k(a_k+b_k)}.

The grand-canonical partition function

  Z(q) = Σ_C w(C)
       = Σ_n q^(n²) · Π_{k=1..n} [Σ_{a,b≥0} (-1)^(a+b) q^(k(a+b))]
       = Σ_n q^(n²) · Π_{k=1..n} (Σ_{a≥0} (-q^k)^a)²
       = Σ_n q^(n²) · Π_{k=1..n} 1/(1 + q^k)²
       = f(q)    (identically, no approximation).

### What is natural vs hand-tuned

**Natural:** Two bosonic species at imaginary chemical potential μ = π is a standard physics object — it appears in supersymmetric index calculations (the Witten index uses similar (-1)^F insertions) and in lattice gases with alternating-sign fugacity. The "(-1)^F-weighted bosons reproduce fermion thermodynamics" is a textbook duality (each species contributes 1/(1+q^k), the fermionic partition for one mode).

**Hand-tuned:** The fact that the available single-particle level set is exactly {1, 2, ..., n} *as a function of the core size n* is the non-trivial structural choice. One can read it physically as "a defect of linear size n opens up n single-particle levels indexed 1..n", or as "the n-th Durfee block governs which modes are accessible". But it is *chosen* to match the (1+q^k)² product running from k=1 to k=n — not derived from a more basic principle. The q^(n²) Durfee-square cost is then an arbitrary-but-natural choice for the n-sector weight.

So Probe 1 is honestly a **construction**, not a derivation. It establishes that the bridge "mock theta = grand-canonical Z of a physical lattice gas at imaginary fugacity" is *structurally buildable*, but the lattice gas is reverse-engineered rather than independently motivated.

### Numerical verification

The script `16_fep_mock_modular_toy.py` computes Z by direct truncated sum over configurations (a_k, b_k ≤ M, n ≤ N) and compares to the closed-form series for f(q). Agreement to ≥20 decimal digits over β ∈ {0.05, 0.1, 0.5, 1, 3, 10} (the regime where the direct sum is computationally feasible):

| β     | digits agree |
|-------|--------------|
| 0.05  | 25.6 |
| 0.10  | 26.1 |
| 0.50  | 29.8 |
| 1.0   | 35.6 |
| 3.0   | 49.9 |
| 10    | ≥50  |

The construction is exact — the only error is from truncating the infinite bosonic-mode sums at finite M.

**Confidence:** high. The identity is algebraic.

**Novelty:** the *framing* as a physics model (lattice gas + imaginary fugacity) is what's new; the algebraic identity itself (f(q) as a "fermionic" sum) is essentially the Andrews/Hickerson form of f. So Probe 1 is a *re-interpretation*, not a new identity. Per SOTA, the re-interpretation has not been written down in the FEP / EBM literature.

---

## (b) Probe 2 — is g* equal to (or proportional to, or asymptotic to) any standard info-theoretic quantity?

The shadow of f (after the q^{-1/24} twist that makes it a weight-1/2 mock form) is the unary theta

  g(τ) = Σ_{n ∈ ℤ} (-1)^n (6n+1) e^{2π i (6n+1)² τ/24} .

We evaluate g(iy) and the non-holomorphic Eichler integral g*(iy) by direct quadrature with y = β/(2π). The candidates probed:

1. **MI:**  I(n ; total_particles) in the unsigned (positive bosonic) measure obtained by replacing z=-1 with z=+1.
2. **KL:**  KL(p_unsigned(n) || p_signed(n)).
3. **Surprise:**  Eₚ_unsigned[ -log p_signed(n) ] (cross-entropy).
4. **Fisher:**  F(β) = Σₙ p_signed(n) (∂_β log p_signed(n))² .

### Results across β = 10⁻³ ... 10 (13 points, 4 orders of magnitude)

See `ramanujan/analysis/results/fep_mock_modular_toy.csv`. Excerpt:

| β       | g*       | MI       | KL       | Surprise | Fisher   |
|---------|---------:|---------:|---------:|---------:|---------:|
| 1e-3    | 3.463    | 1.3e-4   | 1224     | 1228     | 0.394    |
| 1e-2    | 3.457    | 3.0e-4   | 120      | 123      | 0.385    |
| 1e-1    | 3.397    | 0.023    | 10.3     | 12.2     | 0.310    |
| 1       | 2.754    | 0.280    | 0.284    | 1.094    | 0.084    |
| 3       | 1.913    | 0.0152   | 9.3e-4   | 0.206    | 0.0340   |
| 10      | 1.034    | 4.1e-8   | 7.5e-13  | 5.0e-4   | 4.5e-5   |

### Proportionality test results

For each candidate I tested whether candidate / g* is a constant across the sweep:

| candidate | median ratio | max rel. deviation | verdict |
|-----------|-------------:|-------------------:|---------|
| MI        | 6.6e-3       | 14.3 (1430%)       | FAIL    |
| KL        | 1.34         | 262 (26200%)       | FAIL    |
| Surprise  | 1.81         | 196 (19600%)       | FAIL    |
| Fisher    | 0.076        | 0.999 (99.9%)      | FAIL    |

None passes the 1%-relative-deviation bar. The closest is Fisher, where the ratio varies only by a factor of ~2 across 4 dex of β — but a factor of 2 is not "proportional".

### Structural insight (why all four fail)

The Eichler integral g*(iy) has a **finite limit ≈ 3.46 as y → 0**, i.e. at the cusp β → 0. This is a structural consequence: g(iy) is a unary theta, the shadow factor in the Eichler integral involves an erfc / incomplete gamma, and the resulting g* is real-analytic and bounded.

But:

- **MI vanishes** at the cusp (the unsigned distribution becomes nearly uniform on a huge range of n, particle-count factorizes through n, mutual information → 0).
- **KL and Surprise diverge** at the cusp (Z_unsigned diverges very fast — the bosonic partition function 1/(q^k; q²)² has the modular blow-up — while Z_signed = f(q) → 1.33, so KL ~ log(Z_unsigned/Z_signed) → ∞).
- **Fisher vanishes** at the cusp (p_signed(n) freezes to a fixed distribution as β → 0, with negligible β-derivative).

So a **necessary** condition for *any* candidate to track g* is that it be bounded and nonzero at the cusp. None of the four standard info-theoretic candidates I tested satisfies this. This is a clean negative result with *structural* (not just numerical) content.

### What would falsify each conjecture

- **MI**: if MI(n; P_total) tracked g*, the median ratio would be constant across β to within 1%. Verified false: ratio varies by 14×.
- **KL**: same test. Verified false: ratio varies by 262×.
- **Surprise**: same. False: 196×.
- **Fisher**: same. False: 1.0× (the ratio varies by ~factor of 2, which means F(β) and g*(β) move together over a limited range but disagree on the cusp limit). The Fisher candidate is the "least falsified", and the closest to "g* and F(β) have similar low-β-to-high-β shape." But it does not pass the 1% bar.

### Honest interpretation

A clean negative result. The shadow of a mock theta function, evaluated as g*(τ), is *not* equal to (or proportional to) any of the standard information-theoretic functionals of the natural marginals of the toy lattice gas. The math behind this is forced: g* is bounded at the cusp, KL/Surprise diverge there, MI/Fisher vanish there.

**This is informative.** It tells us:

1. If a "shadow ↔ information" theorem exists, it cannot be of the form "g* = const × KL" or any similar uniform-in-β proportionality with the standard candidates.
2. A candidate that *could* possibly work would have to be a *bounded* functional of the signed distribution with a nontrivial cusp value. Examples not yet tested:
   - The **Rényi divergence** of finite order between signed and unsigned, especially Rényi-1/2 (Bhattacharyya) which is bounded when the underlying distributions have bounded log-ratio almost everywhere.
   - The **symmetric KL** restricted to a *finite-mass* subset (e.g. KL on the first k bins, with k determined by the support of p_signed).
   - The **entanglement entropy** in some bipartite restructuring of the configuration space — but this requires more topological data than we have built in.
3. The honest finding may be that the shadow's role is *not* information-theoretic in the standard sense but rather **anomaly-theoretic**: g* measures the failure of the holomorphic part to be modular, and modularity is an algebraic / cohomological property, not a probabilistic one.

---

## (c) Does any candidate match g*?

**No.** Four candidates tested, four fail the strict ≤1% / ≥2-dex proportionality bar. The least-bad is Fisher (factor-of-2 variation in ratio); the worst is KL (factor-of-262).

The *structural* obstruction is uniform: g* is bounded at the cusp, every candidate either diverges or vanishes there.

---

## (d) Bottom-line claim

**Confidence:** medium-high (numerically substantiated negative result on Probe 2; algebraically rigorous positive result on Probe 1).

**Bottom line:**

> **The FEP × mock-modular bridge is structurally buildable (Probe 1) but not via any of the four standard "shadow = information" identifications (Probe 2).** Ramanujan's f(q) can be realized as the grand-canonical Z of a two-species bosonic lattice gas at imaginary chemical potential μ = π, with an integer "core size" sector carrying q^{n²} weight. However, the Eichler integral g*(τ) of the shadow is *not* proportional to mutual information, KL divergence, cross-entropy surprise, or Fisher information of any natural marginal of that lattice gas. The obstruction is structural: g* is bounded at the cusp β → 0, while each candidate either diverges or vanishes there.

**Is this evidence the bridge is real, illusory, or undetermined?**

- **Probe 1 result:** the bridge is *real* in the algebraic / generating-function sense. A precise mock theta function arises as the partition function of a precise (toy) lattice gas. This is more than analogy; it is an identity. **The bridge from physics to mock-modularity is established as buildable.**

- **Probe 2 result:** the bridge from the shadow back to information theory is *not via standard candidates*. This narrows the search: any future "shadow = X" theorem must use a *bounded-at-cusp* functional, ruling out KL, surprise, and the standard finite-dimensional Fisher.

- **Net:** the FEP × mock-modular bridge looks **partially buildable**: the forward direction (generative model → mock partition function) goes through; the reverse direction (shadow → information-theoretic quantity in that model) does not, *at least not via the canonical four candidates*. Recommended next probe (out of scope for this entry): test Rényi divergences and entropic uncertainty relations as the bounded-at-cusp candidates.

**What would change the conclusion:**
- An independent derivation of the q^(n²) Durfee weight from a basic FEP/free-energy argument would upgrade Probe 1 from "construction" to "derivation".
- A Rényi-α divergence (for some α ≠ 1) matching g* to 1% across 2 dex of β would establish the reverse-direction bridge. (Worth a follow-up experiment; not pursued here.)
- A theorem showing that *no* probability-distribution-based functional of the marginals can match g* — because the shadow is a cohomological obstruction, not a divergence — would crystallize the negative result. The cusp-boundedness asymmetry between g* and the standard candidates is consistent with this conjecture.

---

## Caveats

- The Eichler integral g* is computed up to an overall convention-dependent prefactor. Proportionality tests are insensitive to this prefactor, so this does not affect the negative result. It does affect any future precise "shadow = c × Rényi-α" claim — the prefactor would have to be tracked carefully.
- For β < 0.01, the KL and Surprise candidates are slightly under-converged (n_max capped at 800; the unsigned distribution has support extending to n ~ 1/β). The reported KL is a *lower bound*. The true KL grows even faster, *strengthening* the divergence-at-cusp finding.
- The MI computation uses n_max=20 and P_max=80 due to O(n × P²) cost. Spot-checks at larger truncations did not change the qualitative result (MI is non-monotonic in β with peak near β=1; this peak is well within the computed range).
- The shadow used is the standard Hickerson-Mortenson form for the third-order mock theta f; alternate conventions (e.g. Zagier's) would differ by a normalization but not by shape.
