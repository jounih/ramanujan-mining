# Ramanujan Mining Run — Live TODO

Maintained as the run progresses. Strikethrough or move to `done.md` when shipped.

## In-flight

- [x] Charter & directory scaffolding
- [x] Source-discovery sub-agents (lost notebook, notebooks 1-3, letters/papers/QRs)
- [x] SOTA: physics & computation
- [x] SOTA: open problems / under-mined corners
- [x] Theta-dual switching curve — Experiment 02
- [x] RKC v0 with rigorous erfc tail bounds — Experiment 03
- [x] Critique Gemini's commentary on ChatGPT-Pro report (diary 02)

## Next two passes

### Pass A — substantiate the central hypothesis on diverse kernels (experiments 04–08)

- [x] **04 Lambert ↔ Eisenstein switching.** Shipped as Experiment 12 (filename avoids collision with previously-done 04). Crossover β* = 2π; gain up to 1.21×10⁶× at extreme β. Diary 10. Two normalization gotchas caught by the cross-validation gate (sign factor, Bernoulli prefactor cancellation).
- [x] **05 HRR exact p(n) vs Euler-product recurrence.** Term-count crossover at small n (HRR wins on bits-per-term immediately); wall-clock crossover at n=100000 because per-HRR-term cost is enormous without binary-splitting + FLINT. Diary 07. Also caught a silent-zero-class failure mode (`round(float(mpf))` mangles p(1000)) — fixed with `int(mpmath.nint(...))`.
- [x] **06 Ramanujan 1/π vs AGM vs Chudnovsky vs Machin-like.** Shipped previously (commit e88f99d). Diary 06.
- [x] **07 Divisor sum σ_k(n) via Möbius vs direct vs Dirichlet-series q-expansion.** Batch crossover N* = 41 (much smaller than expected); at N=10⁵ method C uses 5.5% of method A's ops. Per-call B (Möbius/factor) wins everywhere. Diary 08.
- [x] **08 Class invariants G_n direct vs radical.** 8 invariants verified to ≥100 digits via PSLQ before use (5 excluded as un-verifiable in-env). Radical/direct cost ratio grows 1× → 369× as precision climbs from 30 to 1000 digits. Surprise: at d=30, direct beats radical at large n because the q = e^{-π√n} converges faster as n grows. Diary 09.

### Pass B — automated recognition layer (per Gemini's question)

- [x] **09 Kernel-fingerprint matcher v0.** Shipped previously (commit d0c7599). Diary 04.
- [x] **10 RKC routing benchmark.** Recognizer v1 with 11 kernels + per-kernel degeneracy detectors; routing benchmark 54/55 = 98.2%, macro precision 1.00 (zero false positives across families), silent-zero Gauss-sum hazard fires on every q ≡ 2 mod 4 case. One honest miss (`3·exp(-βn²)` — needs scalar-coefficient stripping wrapper). Diary 11.

### Pass C — under-mined corners from SOTA notes (BLOCKED: need primary-scan access; sourcing in progress)

- [ ] **11 Lost Notebook partial-theta corner (LN pp. 28-39).** Restate the Bringmann–Folsom–Rhoades identities computationally; check whether they admit a representation-switching gain for some sum.
- [ ] **12 NB II Chapter 32 Eisenstein-style continued fractions** (per Bhatnagar 2208.12656). Implement, benchmark.
- [ ] **13 LN pp. 341-343 / 1729-K3 manipulations** (per Ono-Trebat-Leder 1510.00735). Replicate the K3 family; look for any modular structure that could feed RKC.
- [ ] **14 Mixed modular equations at levels 23, 29, 31, 47.** Implement Ramanujan's modular equation polynomials; see whether they give cheaper isogeny / Schoof-style computations than Atkin's classical modular polynomials.

### Pass D — the FEP / mock-modular bridge (biggest white space per SOTA)

- [x] **15 Generative model whose evidence is a mock theta function.** Lattice gas with two bosonic species at chemical potential μ = π (i.e., fugacity z = -1); configuration (n, {a_k, b_k}_{k=1..n}); Hamiltonian E = n² + Σk·(a_k+b_k). Identically Z(q) = f(q) — verified to 25–50 digits across β ∈ [0.05, 10]. Natural piece: textbook (-1)^F bose-to-fermi duality at z=-1. Hand-tuned piece: the Durfee-square q^(n²) core sector and the n-mode constraint. Diary 13.
- [x] **16 "Shadow = mutual information?" probe.** Tested all four standard info-theoretic candidates (MI, KL, Surprise, Fisher) against g*(τ) across β ∈ [10⁻³, 10]. All FAIL the strict bar (≤1% rel. dev across ≥2 dex β). Structural reason: g* is BOUNDED at the cusp β→0 (limit ≈ 3.46) while KL/Surprise diverge and MI/Fisher vanish. Clean negative result with structural (not merely numerical) content. Diary 13.
- [x] **17 Mock-theta residual EBM v1 (was v0 in original plan; v0 also shipped earlier as exp 15).** v1 uses exact Hickerson-Mortenson shadow + Eichler integral via Watson's 1936 transformation; bias reduction ~258 bits at small β; modular cross-check passes at ≥30 digits. Found a real BUG in v0: it used the EVEN Kronecker character (12/·) when the shadow requires the ODD primitive character mod 12 (else the unary theta vanishes identically). v0's claimed "1/√β" asymptotic was also wrong (v1 saturates at the Watson-Hickerson radial limit 4/3). Diary 12.

### Pass E — "latent-space speedrun" hypothesis evidence

- [ ] **18 Notational compression survey.** Tally how often Ramanujan uses (a;q)_∞ vs spelled-out products in a given chapter; quantify "notation density per identity."
- [ ] **19 Parallel-derivation evidence.** Find pairs of consecutive entries in NB II that arrive at the same identity by genuinely different routes — direct evidence of his "multiple-paths-in-latent-space" working style.
- [ ] **20 Generating-function arithmetic as primitive.** Identify entries where the manipulation is purely at the GF level (multiplying/dividing/applying operators to entire infinite products as opaque objects) — argue this is structurally analogous to operating in a learned embedding space.

### Cross-cutting deliverables (at end)

- [x] Synthesis report: shipped as `insights/CANDIDATE_INSIGHTS.md`; revised after the parallel sweep with §A5 v0-bug retraction, new §A6 (universal β* = c·π pattern), new §A7 (FEP-bridge half-buildable).
- [x] Cumulative diary index: see `diary/INDEX.md` (entries 00–15).
- [x] A standalone `rkc/` package with the prototype recognizer + the canonical-kernel registry. Shipped at `ramanujan/rkc/` with v2 implementation (100% on the 55-case routing benchmark, macro precision 1.00), 35 passing unit tests, registry + costs + routing + degeneracy detectors as separate modules. README + 1-page example included.
- [x] Honest "did not pan out" log: shipped at `insights/DID_NOT_PAN_OUT.md` — 14 entries (5 REFUTED, 3 CORRECTED, 5 PARTIALLY REFUTED, 1 DOWNGRADED) + 6 OUTSTANDING. Every refuted/corrected entry cites a specific diary entry + experiment script.

### Follow-up pass (Recognizer v2, bounded-cusp shadow, scan scaffold)

- [x] **Exp 14b RKC routing benchmark v2.** Recognizer v2 hits **55/55 = 100%** (vs v1's 54/55). The one previously-failing case (`3·exp(-βn²)`) now matches via scalar-coefficient stripping wrapper. Macro precision 1.00, macro recall 0.95. No v1 regressions. Diary 14.
- [x] **Exp 18 bounded-at-cusp shadow probes.** Eight new candidates tested (Rényi-α for α∈{0.5, 1.5, 2, 5, ∞}, Bhattacharyya d_B, Hellinger², entropic uncertainty). Zero passes, zero near-passes. **Twelve candidates total** across Exp 16 + 18, all fail. Surprise: Rényi-α and Bhattacharyya *also* diverge at the cusp here because unsigned/signed bosonic mass migrates to disjoint supports as β → 0. Sharpened conjecture (per diary 15): g* is most plausibly an **Eichler cocycle in H¹(Γ, V_k)** — a cohomological object on the modular group, not a probabilistic functional of any natural marginal. Remaining viable directions: Wigner-negativity-aware divergences on the joint signed measure, or path-measure functionals.
- [x] **Scan-ingestion scaffold.** `corpora/scans/` and `corpora/transcriptions/` directories with format READMEs. 6-operator tagging schema (`operator_tagging_schema.py`) for Hunt 5 — self-test passes. `quarterly_reports/` dir ready with naming spec `qr<N>_section_<M>.tex`. `.gitignore` excludes binary facsimiles >1MB.

### Third follow-up pass — Recognizer ↔ Eichler, Wigner-negativity, Path-measure

- [x] **Exp 19 — Wire `MODULAR_COMPLETION_REQUIRED` to Watson-Hickerson.** `rkc/completions.py` shipped. Recognizer now returns a (value, error_bound, certificate) tuple for f3 mock-theta inputs, cross-checked at ≥30 digits across β ∈ {0.001, 0.01, 0.1, 0.5}. f5/f7 surface `CompletionNotImplemented` honestly. 50/50 unit tests, no v2 regression. Diary 16.
- [x] **Exp 20 — Wigner-negativity-aware divergences.** 4 candidates probed (negativity volume, mana, Rényi-α=0.5 on |W|, Rényi-α=2 on |W|). All fail the strict bar. One zero-parameter cusp-asymptote coincidence: log(2)/g\*(0) = 0.20025 matches empirical cusp-window ratio 0.20033 to 0.04%, but bulk shape fails by 100% — coincidence, not proportionality. Diary 17.
- [x] **Exp 21 — Path-measure functionals.** 3 candidates probed (path entropy production, path KL cumulative, Eichler-shaped path average). All fail. **Decisive structural finding (candidate 3, the structurally-most-likely-positive):** the cooling path traverses the imaginary-axis half-line in the *wrong direction* — the Watson-Hickerson Eichler integral runs interior → cusp at ∞, while the cooling path goes cusp at 0 → interior. Disjoint half-lines, opposite directions; rules out the partition-function-path-integral interpretation structurally. Diary 18.

**Cumulative B1 falsification count: 19 candidates across Exp 16, 18, 20, 21.** Sharpened conjecture (medium-high confidence): g\* is irreducibly cohomological — an Eichler cocycle in H¹(Γ, V_k) intrinsic to Γ acting on the upper half-plane, NOT derivable from any natural functional of the lattice gas.

### Fourth follow-up — closure on the FEP × mock-modular candidate-family approach

- [x] **Exp 22 — Direct Eichler-cocycle reconstruction from lattice-gas transfer matrix.** STRUCTURAL NEGATIVE with three independent reasons: (i) diagonal T_K(β) has trivial eigenstructure — Γ-equivariance lives in the trace, not in any spectral invariant; (ii) S-transform Ω_K ↔ Ω'_K has fundamental (K+1)² dimension mismatch at every finite K — no unitary intertwiner can exist; (iii) K → ∞ defect reduces analytically to Watson 1936's partner-function identity (tautological — Watson's 90-year-old identity restated in lattice-gas language, not new). Interior β ∈ [0.3, 3] ratio matches 1.0000000140 (7 decimals) but only over 1 dex AND the matching constant is Watson's identity — disciplined-rejected, not a positive. Diary 19.

**Cumulative B1 falsification: 20 candidates across 5 structurally-different families (Exp 16, 18, 20, 21, 22). No remaining structurally-different candidate family.** The cohomological-irreducibility conjecture is essentially established at medium-high → high confidence: g* is an intrinsic element of H¹(Γ, V_k), an Eichler cocycle for Γ acting on H, that does NOT reduce to any natural functional of the underlying lattice gas. **Investigation of the candidate-family approach is closed.**

### Next-pass leads (mostly blocked on scans)
- **f5/f7 Watson-Hickerson instrumentation** for `rkc/completions.py`. Requires transcribing Hickerson 1988 / Berndt-Chan identities (out of scope for the original remote env; natural local-env task).
- **`recognize_composite` `numerical_completion` propagation** — cheap fix flagged in diary 16; deferred.
- **Hunt 5 Quarterly-Reports operator tagging** — runs the moment Berndt-Rankin material arrives. Schema is ready at `corpora/transcriptions/operator_tagging_schema.py`.

## Sourcing pipeline (user is providing primary scans for Pass C / Pass E)

Priority order (per user offer + HUNT_MAP §):
1. Berndt & Rankin, *Ramanujan: Letters and Commentary* (AMS HMath 9, 1995) — **Quarterly Reports chapter** (~50 pages). Highest-leverage single source per HUNT_MAP §5.
2. Andrews & Berndt, *Ramanujan's Lost Notebook Part IV* (Springer 2013) — chapter on "Approximations and asymptotic methods, including 1729", LN pp. **341-343**. Unlocks Hunts 1 + Pass C-13.
3. Berndt, *Ramanujan's Notebooks Part V* (1998), **Chapter 32** Eisenstein-style continued fractions. Unlocks Hunt 3 + Pass C-12.
4. Berndt, *Ramanujan's Notebooks Parts III-V* — modular equations at levels **23, 29, 31, 47**. Unlocks Hunt 2 + Pass C-14.
5. Cooper, *Ramanujan's Theta Functions* (Springer 2017) — Ramanujan-Sato table by level. Unlocks Hunt 6.
6. Andrews-Berndt, *Lost Notebook Vol. I* supplement pp. 200-220 — the ~18 unproven class invariants Gₙ. Unlocks Hunt 4.

Drop materials under `ramanujan/corpora/scans/` or `ramanujan/corpora/transcriptions/`. Large PDFs should be .gitignored before commit.

## Provenance ledger

Three sources for any identity I cite:
- **(scan)** — Trinity shelfmark or archive.org identifier, NOT read in this env; awaiting ChatGPT-Pro corpus or future env.
- **(transcription)** — Berndt/Andrews printed text, Hardy *Collected Papers*, or verified GitHub mirror.
- **(training-memory)** — recalled from training data, MUST be numerically verified before use.

## Constraints in this environment

- Outbound HTTP is allow-listed to github/pypi/npm + WebSearch tool. No archive.org, Trinity, arXiv direct, no Wikipedia. Cannot save binary PDFs locally.
- Compute: Python 3.11, sympy 1.14, mpmath 1.3, numpy. No PARI/GP (cypari2 fails to build).
- Diary entries and experiments are the durable artifacts; everything pushed to branch `claude/ramanujan-original-works-4TwPG`.
