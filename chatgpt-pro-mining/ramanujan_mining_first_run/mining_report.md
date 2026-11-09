# First mining report: Ramanujan source patterns for computational acceleration

## Scope of this report

This is a first-pass research map built from the saved corpus and a source/theme pass over Ramanujan's published papers and notebook facsimiles. It is deliberately conservative: I separate established mathematics from new engineering hypotheses.

## A. What appears most relevant to modern computation

### 1. Reciprocal-kernel compiler for energy normalizers

**Source pattern.** Ramanujan's work repeatedly exploits reciprocal transformations: modular equations, theta-like transformations, Riemann ξ/Ξ integral forms, quadratic forms, and partition asymptotics. The computational signature is a switch between two regimes where one side is dense and the other is sparse.

**Modern bottleneck.** Energy-based models need partition functions or log-partition estimates. Current learning often treats exact partition computation as intractable and uses MCMC, contrastive divergence, score matching, learned log-partition surrogates, or variational objectives.

**Hypothesis.** Build a compiler that detects whether a discrete/continuous energy decomposes into sums of kernels with known reciprocal transforms. For each temperature β and tolerance ε, it selects the representation with the smallest certified term budget.

**Toy result saved.** For `Z(β)=Σ exp(-βn²)`, the saved theta experiment shows the term count collapse at small β. At β=1e-6, direct summation needs thousands of terms, while the reciprocal form needs only the n=0 term to the chosen tolerance.

**Status.** Established for theta/Gaussian kernels; plausible extension as a compiler for structured EBMs, lattice models, Fourier-feature energies, and variational free-energy components.

### 2. Rational-temperature snapping via Gauss sums

**Source pattern.** Ramanujan's definite integrals connected with Gauss sums and trigonometrical sums suggest aggressive use of rational phases and finite sums. Many infinite-looking expressions become finite or nearly finite at rational points or roots of unity.

**Hypothesis.** When evaluating a free energy or log-normalizer over a continuum of β, approximate β or phase parameters by rationals p/q when error bounds are favorable. Then replace expensive infinite/Fourier sums by finite Gauss-sum evaluations plus a controlled residual.

**Where to test first.** Periodic EBMs, lattice Gaussian models, Fourier energy models, quantum-inspired phase sums, and any model whose partition function is a theta/q-series with roots-of-unity behaviour.

**Status.** Known in analytic number theory; potentially underused as an adaptive approximation primitive in ML normalizer estimation.

### 3. Divisor-rich / highly-composite compute schedules

**Source pattern.** The highly composite numbers paper is an optimization theory of integers with many divisors. Divisor-rich sizes have many decompositions.

**Hypothesis.** Treat batch sizes, sequence lengths, FFT/NTT lengths, block sizes, and sharding dimensions as highly-composite optimization targets rather than arbitrary powers of two. Objective:

`score(n)=benefit(divisor lattice, radix options, tensor-core alignment) − cost(padding, memory pressure, communication)`.

**Saved artifact.** `experiments/divisor_rich_block_sizes.csv` lists record-setting and top divisor-rich candidates up to 8192.

**Status.** The general idea of mixed-radix scheduling is well known; the Ramanujan-inspired angle is to search over the divisor lattice itself and carry an explicit “factorization optionality” score.

### 4. Modular checksums and congruence sieves for dynamic programs

**Source pattern.** Ramanujan's partition congruences and related modular identities provide cheap arithmetical invariants of huge coefficient sequences.

**Hypothesis.** In combinatorial dynamic programs, compute low-cost congruence invariants in parallel with the main recurrence. Use them as checksums, pruning signals, or error detectors for approximate coefficient extraction.

**Example target.** Partition-like DP, inside-outside algorithms with generating functions, symbolic sequence search, and integer-valued probabilistic programs.

**Status.** Congruence checks are established in computational number theory; use as runtime verification for approximate DP is a plausible engineering recombination.

### 5. Continued-fraction variational ansätze

**Source pattern.** Ramanujan and related Rogers-Ramanujan material show compact continued fractions and q-products that encode difficult constants or generating functions.

**Modern comparison.** The Ramanujan Machine demonstrates that meet-in-the-middle and gradient-descent searches over continued-fraction structures can generate nontrivial conjectural formulas for constants.

**Hypothesis.** Replace generic neural log-partition surrogates with constrained continued-fraction or J-fraction/S-fraction surrogates when the target log-normalizer has Stieltjes, moment, q-series, or recurrence structure. Enforce positivity/monotonicity via the recurrence coefficients.

**Status.** Known for moment problems and Padé/J-fraction approximation; new target is structured free-energy/EBM log-normalizer approximation with Ramanujan-Machine-style symbolic search.

### 6. Sparse polar reconstruction for coefficient families

**Source pattern.** Hardy-Ramanujan/Rademacher-style formulae reconstruct huge partition coefficients from modular/cuspidal data and Kloosterman-like finite sums.

**Hypothesis.** For generative models or physical systems with modular/duality symmetry, learn or infer only “polar”/boundary data and reconstruct large coefficient families through exact transform formulas instead of enumerating states.

**Status.** Established in modular forms; speculative but potentially powerful wherever a model has exact or approximate modular symmetry.

### 7. Mock-theta residual modelling near boundaries

**Source pattern.** Mock theta functions arise where ordinary theta/modular behavior is close but incomplete; modern theory completes them using non-holomorphic corrections / harmonic-Maass-form structure.

**Hypothesis.** In energy/free-energy settings with phase transitions, complex weights, or root-of-unity limits, fit a two-part approximation: modular/theta leading term plus mock-like boundary correction. This may outperform black-box residual networks by baking in asymptotic boundary structure.

**Status.** Speculative for ML; mathematically motivated by the post-Zwegers understanding of mock theta functions.

## B. Ranked next experiments

1. **Structured EBM normalizer compiler.** Start with diagonal/lattice Gaussian, Potts-on-cycle, Fourier-feature binary models. Compare direct enumeration, AIS/MCMC, variational τ-network, and reciprocal-transform compiler.
2. **HCN schedule benchmark.** Benchmark FFT/NTT/matmul/tensor contractions at same logical workload but with power-of-two versus divisor-rich padded sizes.
3. **Continued-fraction logZ surrogate.** Train J-fraction coefficients for toy Ising/RBM logZ curves; compare to MLP τ surrogates for extrapolation and monotonicity.
4. **Gauss-sum rational snapping.** For periodic energies, approximate β/phase by p/q, evaluate finite transform, and bound residual; compare to sampling.
5. **Mock residual test.** Fit theta + mock-like residual terms near a known critical/root-of-unity regime and compare to generic residual approximators.

## C. “Novel insight” candidates to protect from overclaiming

These are the ideas I would carry forward as potentially novel engineering contributions, not mathematical theorems:

1. A free-energy/EBM **reciprocal-kernel compiler** that automatically switches among direct, modular, Poisson, Gauss-sum, and asymptotic representations by certified term budget.
2. A **divisor-lattice compute scheduler** inspired by highly composite numbers, optimized for padding-plus-factorization optionality rather than powers-of-two alone.
3. **Rational-temperature snapping** for structured normalizers: deliberately approximate parameters by rationals to unlock finite Gauss-sum evaluation with error control.
4. **Mock-theta residual modelling** for boundary/phase-transition regimes where pure theta/modular approximations have structured residuals.
5. **Continued-fraction log-partition ansätze** searched by Ramanujan-Machine-style MITM/GD, constrained by positivity and monotonicity.

## D. Files produced by this pass

- `README.md`
- `diary.md`
- `manifests/run_summary.json`
- `manifests/published_papers_manifest.csv`
- `manifests/notebooks_manifest.csv`
- `manifests/trinity_archival_manifest.csv`
- `manifests/file_manifest.csv`
- `experiments/toy_theta_partition_acceleration.csv`
- `experiments/divisor_rich_block_sizes.csv`
