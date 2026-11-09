# Ramanujan corpus mining, non-EBM pass 2

Run timestamp: 2026-05-24 11:42:59 UTC

## Brief intuition

The biggest-looking opportunity is **not** a single forgotten theorem. It is a way of treating Ramanujan’s formulas as a catalog of *compressed executable representations*: long sequences become hidden poles and weights; divisor sums become finite periodic bases; products become recurrences or continued fractions; coefficient problems become congruence checks or asymptotic reconstructions. The useful mining target is therefore a compiler/query planner: “given this computation, which Ramanujan-style representation is cheapest and safest?”

## What now feels big and exciting

### 1. Ramanujan-Prony latent decomposer

**Source motif.** moment/power-sum sequence -> rational generating function -> partial fractions


**Modern targets.** sparse FFT, recurrence discovery, sequence compression, system identification, model distillation


**Why exciting.** Turns long traces into a small set of hidden poles/weights; directly matches the user intuition of compressed latent representations.


**Novelty caveat.** Classical method exists; opportunity is a Ramanujan-style automated compressor that tries rational, q-rational, product, and continued-fraction latent forms across notebook formulas.


**Next experiment.** Run over formula-generated sequences and score by recovered poles, residual, and extrapolation; compare to Berlekamp-Massey, matrix pencil, sparse FFT, Padé.


### 2. Ramanujan-sum periodicity layer

**Source motif.** finite trigonometric/Ramanujan sums c_q(n) as divisor-aware basis


**Modern targets.** time-series periodicity, event streams, neural sequence features, anomaly detection, sparse periodic coding


**Why exciting.** A periodicity basis indexed by integer period/divisibility rather than only Fourier frequency; can reveal hidden cycles at low sample counts.


**Novelty caveat.** Signal-processing literature exists; ML/attention/kernel deployment looks underexplored.


**Next experiment.** Implement differentiable Ramanujan-filter bank and compare against Fourier features on integer-period synthetic and real event data.


### 3. q-series representation compiler

**Source motif.** switch among product, sum, recurrence, congruence, modular, and asymptotic coefficient views


**Modern targets.** formal power series, exact combinatorics, symbolic algebra, coefficient extraction, theorem proving benchmarks


**Why exciting.** The same object has many executable forms; a cost model can pick the cheapest representation for coefficient, residue, or asymptotic queries.


**Novelty caveat.** Strong special-case SOTA exists for partitions/modular forms; general compiler for arbitrary Ramanujan-style q-products is less mature.


**Next experiment.** DSL for q-Pochhammer/eta quotients; query planner chooses DP, recurrence, modular formula, or asymptotic; compare to Sage/FLINT/Mathematica where possible.


### 4. Continued-fraction executable approximants

**Source motif.** compact continued fractions and product quotients as small stable programs


**Modern targets.** special functions, constants, activation approximants, online filters, kernel compression


**Why exciting.** A continued fraction is often more stable and state-light than a polynomial/rational approximation.


**Novelty caveat.** Ramanujan Machine validates automated CF search; opportunity is function/kernel libraries rather than constants only.


**Next experiment.** Mine CF templates, fit to target functions, verify with intervals, compare to minimax/Chebyshev/Padé.


### 5. Divisor-rich hardware scheduler

**Source motif.** integers optimized by divisor lattice/factorization optionality


**Modern targets.** FFT/NTT lengths, GPU tiles, batch/sequence padding, distributed shard sizes


**Why exciting.** Low-hanging practical payoff: pick sizes that keep many algorithmic decompositions open, not merely powers of two.


**Novelty caveat.** Mixed-radix planning is known; explicit HCN-style optionality objective is the recombination.


**Next experiment.** Benchmark candidate lengths under FFT libraries and GPU kernels with padding costs.


### 6. Congruence checksums for exact/approximate computation

**Source motif.** cheap modular invariants and partition congruences


**Modern targets.** large DP, coefficient extraction, computer algebra, theorem prover sanity checks, approximate integer pipelines


**Why exciting.** Attaches very cheap truth constraints to expensive computations.


**Novelty caveat.** Known in computational number theory; useful as modern library engineering.


**Next experiment.** Wrap generating-function algorithms with residue sentinels; inject errors and measure detection/pruning.


### 7. Asymptotic + exact-correction kernels

**Source motif.** dominant asymptotic plus compact correction/error expression


**Modern targets.** special function evaluation, inverse estimates, big coefficient approximations, initialization for solvers


**Why exciting.** Fast approximate jump followed by a small certified correction; very Ramanujan-like in feel.


**Novelty caveat.** Core numerical-analysis pattern; opportunity is a curated Ramanujan-derived catalog with implementation tests.


**Next experiment.** Build formula cards with regimes, error terms, and code kernels.


## Local corpus ranking by computational motif

Top published-paper clusters from the keyword/motif pass:


|   id | title                                                                           |   total_mining_score | top_motifs                                                                                                       |
|-----:|:--------------------------------------------------------------------------------|---------------------:|:-----------------------------------------------------------------------------------------------------------------|
|   36 | Asymptotic formulae in combinatory analysis                                     |               36.608 | q_series_modular_product:6.399; partition_coefficient_extraction:5.419; asymptotic_reconstruction:5.317          |
|   18 | On certain arithmetical functions                                               |               28.946 | q_series_modular_product:7.271; divisor_factorization_scheduling:4.526; finite_fourier_gauss_transform:4.394     |
|   37 | On the coefficients in the expansions of certain modular functions              |               27.73  | q_series_modular_product:6.153; partition_coefficient_extraction:4.045; integral_kernel_transform:3.219          |
|   15 | Highly composite numbers                                                        |               26.66  | divisor_factorization_scheduling:6.934; asymptotic_reconstruction:4.394; q_series_modular_product:4.19           |
|   21 | On certain trigonometrical sums and their applications in the theory of numbers |               25.406 | finite_fourier_gauss_transform:7.754; q_series_modular_product:3.807; divisor_factorization_scheduling:3.135     |
|    1 | Some properties of Bernoulli’s numbers                                          |               23.943 | finite_fourier_gauss_transform:4.554; constant_special_function_evaluation:3.833; q_series_modular_product:2.996 |
|   34 | Asymptotic formulae for the distribution of integers of various types           |               23.294 | asymptotic_reconstruction:4.296; q_series_modular_product:4.248; integral_kernel_transform:2.833                 |
|    6 | Modular equations and approximations to π                                       |               22.864 | q_series_modular_product:7.425; asymptotic_reconstruction:4.714; integral_kernel_transform:4.332                 |
|   20 | On the expression of a number in the form ax²+by²+cz²+du²                       |               21.795 | quadratic_forms_lattice_theta:6.565; q_series_modular_product:4.773; asymptotic_reconstruction:2.303             |
|   35 | The normal number of prime factors of a number n                                |               19.094 | divisor_factorization_scheduling:4.332; q_series_modular_product:3.829; asymptotic_reconstruction:3.555          |
|   30 | Congruence properties of partitions                                             |               17.586 | q_series_modular_product:5.691; partition_coefficient_extraction:4.944; congruence_checksum_sieve:3.485          |
|   27 | A class of definite integrals                                                   |               15.229 | integral_kernel_transform:5.497; finite_fourier_gauss_transform:4.127; q_series_modular_product:3.526            |


Interpretation: the top cluster is not surprising—partition/modular/asymptotic papers dominate—but the important non-EBM outliers are Paper 3 (latent rational reconstruction), Paper 21 (Ramanujan sums as a signal basis), and Paper 15 (divisor-lattice scheduling).

## Experiment 1: Ramanujan-Prony latent decomposer

Paper 3 takes a sequence of moments `a_1, …, a_{2n}` and reconstructs unknown weights `x_i` and poles `y_i` using a rational generating function. This is essentially a sparse exponential / Prony / rational reconstruction pipeline. It matches the “latent-space speedrun” intuition extremely well: replace a long trace by a tiny set of latent atoms.


Recovered latent components from Ramanujan’s 5-component example:


|   component |   weight_x_real |   weight_x_imag |   pole_y_real |   pole_y_imag |   denominator_root_theta_real |   denominator_root_theta_imag |
|------------:|----------------:|----------------:|--------------:|--------------:|------------------------------:|------------------------------:|
|           1 |         1.28885 |               0 |     -1.61803  |             0 |                     -0.618034 |                             0 |
|           2 |        -0.6     |               0 |     -1        |             0 |                     -1        |                             0 |
|           3 |         1.57639 |               0 |      0.381966 |             0 |                      2.61803  |                             0 |
|           4 |        -2.28885 |               0 |      0.618034 |             0 |                      1.61803  |                             0 |
|           5 |         2.02361 |               0 |      2.61803  |             0 |                      0.381966 |                             0 |


The reconstruction table exactly matches the given 10 terms to numerical precision and extrapolates additional terms. This is old mathematics, but the mining opportunity is to generalize it into a corpus-driven **latent sequence compressor** that tries rational, q-rational, product, and continued-fraction explanations.

## Experiment 2: Ramanujan sums as sparse periodicity atoms

Paper 21 defines finite trigonometric sums now called Ramanujan sums. I tested a synthetic signal made from hidden `c_q(n)` atoms. Orthogonal projection recovered the planted periods exactly in the clean case:


|   q |   estimated_coefficient |   true_coefficient |   abs_error |     basis_energy |
|----:|------------------------:|-------------------:|------------:|-----------------:|
|   6 |                    1.25 |               1.25 |           0 | 720720           |
|  10 |                   -0.75 |              -0.75 |           0 |      1.44144e+06 |
|  15 |                    0.5  |               0.5  |           0 |      2.88288e+06 |
|   3 |                    0    |               0    |           0 | 720720           |
|   4 |                    0    |               0    |           0 | 720720           |
|   2 |                    0    |               0    |           0 | 360360           |
|   1 |                    0    |               0    |           0 | 360360           |
|   7 |                    0    |               0    |           0 |      2.16216e+06 |
|   5 |                    0    |               0    |           0 |      1.44144e+06 |
|   9 |                    0    |               0    |           0 |      2.16216e+06 |


The practical target is a differentiable or streaming **Ramanujan-sum periodicity layer** for event data and integer-period signals. Unlike ordinary Fourier features, these atoms are indexed by arithmetic divisibility, so they may be more sample-efficient when the hidden structure is exact or near-exact integer periodicity.

## Experiment 3: partition recurrences and congruence checksums

I compared a generic coin-change DP for partition numbers with the pentagonal recurrence. The recurrence gives the same values with far fewer updates; this is a small example of a representation switch that should be repeated for every executable identity.


|    N |   pentagonal_seconds |   coin_dp_seconds |   speedup |   p_N_digits |
|-----:|---------------------:|------------------:|----------:|-------------:|
|  250 |          0.000394761 |        0.00148844 |   3.77049 |           15 |
|  500 |          0.00103033  |        0.00742069 |   7.20222 |           22 |
| 1000 |          0.00310451  |        0.0318228  |  10.2505  |           32 |
| 2000 |          0.00940354  |        0.352429   |  37.4783  |           46 |
| 3000 |          0.0170155   |        0.334603   |  19.6646  |           57 |


I also saved congruence checks and error-injection tests. The broader idea: compile Ramanujan-style congruences into cheap runtime invariants for large integer/combinatorial pipelines.

## Experiment 4: divisor-rich sizes as scheduling priors

I ran a small NumPy/pocketfft microbenchmark on selected transform lengths and annotated each length by factorization. This is not a rigorous systems benchmark. It does show the right conservative conclusion: factorization structure is a useful search prior, but actual runtime is library/hardware-specific.


|    n | factorization   |   divisor_count_tau |   largest_prime_factor |   median_seconds |   ns_per_nlog2n |
|-----:|:----------------|--------------------:|-----------------------:|-----------------:|----------------:|
| 4096 | 2^12            |                  13 |                      2 |      4.3317e-05  |        0.881287 |
| 5040 | 2^4 3^2 5 7     |                  60 |                      7 |      5.55295e-05 |        0.89581  |
| 2880 | 2^6 3^2 5       |                  42 |                      5 |      3.263e-05   |        0.985904 |
| 2048 | 2^11            |                  12 |                      2 |      2.2211e-05  |        0.985929 |
| 3072 | 2^10 3          |                  22 |                      3 |      3.54305e-05 |        0.995546 |
| 2400 | 2^5 3 5^2       |                  36 |                      5 |      2.75e-05    |        1.02044  |
| 2304 | 2^8 3^2         |                  27 |                      3 |      2.6543e-05  |        1.03138  |
| 2520 | 2^3 3^2 5 7     |                  48 |                      7 |      2.9577e-05  |        1.03874  |
| 2160 | 2^4 3^3 5       |                  40 |                      5 |      2.508e-05   |        1.04824  |
| 8192 | 2^13            |                  14 |                      2 |      0.000112045 |        1.05211  |
| 1920 | 2^7 3 5         |                  32 |                      5 |      2.2593e-05  |        1.07888  |
| 1800 | 2^3 3^2 5^2     |                  36 |                      5 |      2.1774e-05  |        1.11863  |


This weakens the naive “highly composite always fastest” hypothesis and strengthens a better one: **use highly-composite/divisor-rich integers to reduce autotuning search**, then let FFTW/cuFFT/NTT planners decide locally.

## Experiment 5: non-OCR page triage for notebook mining

Scored 1149 local facsimile page images by ink density, spatial entropy, and bounding-box spread. This is not OCR; it is a cheap way to decide which pages should go first through Chandra/GPT/manual transcription. Highest-scoring pages:


| notebook      |   page |   ink_density |   row_entropy |   col_entropy |   formula_density_score | local_path                                                                       |
|:--------------|-------:|--------------:|--------------:|--------------:|------------------------:|:---------------------------------------------------------------------------------|
| notebook2     |     54 |      0.163113 |      0.974271 |      0.964562 |                0.238683 | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/notebook2/page-054.jpg     |
| lost_notebook |      8 |      0.144209 |      0.981692 |      0.958738 |                0.196649 | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/lost_notebook/page-008.jpg |
| notebook2     |    315 |      0.142538 |      0.957486 |      0.981482 |                0.196011 | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/notebook2/page-315.jpg     |
| lost_notebook |     87 |      0.140864 |      0.978585 |      0.951423 |                0.180675 | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/lost_notebook/page-087.jpg |
| lost_notebook |      9 |      0.129009 |      0.98124  |      0.960946 |                0.172517 | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/lost_notebook/page-009.jpg |
| lost_notebook |     27 |      0.13267  |      0.966111 |      0.960106 |                0.172295 | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/lost_notebook/page-027.jpg |
| notebook2     |    246 |      0.122092 |      0.936265 |      0.982578 |                0.170039 | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/notebook2/page-246.jpg     |
| notebook2     |    250 |      0.11938  |      0.95324  |      0.984467 |                0.169398 | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/notebook2/page-250.jpg     |
| notebook2     |    249 |      0.121422 |      0.95319  |      0.97542  |                0.16634  | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/notebook2/page-249.jpg     |
| notebook1     |     80 |      0.12824  |      0.948149 |      0.975033 |                0.161032 | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/notebook1/page-080.jpg     |
| notebook2     |     11 |      0.121304 |      0.951441 |      0.960669 |                0.156511 | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/notebook2/page-011.jpg     |
| notebook1     |     16 |      0.11944  |      0.947188 |      0.985493 |                0.156167 | /mnt/data/ramanujan_prev/ramanujan_mining/scans_pages/notebook1/page-016.jpg     |


Contact sheets were created in `figures/top_formula_density_pages_fast.jpg`, `figures/top_formula_density_by_notebook_fast.jpg`, and `figures/sparse_nonblank_pages_fast.jpg`.

## SOTA / “do not overclaim” notes

- Partition computation itself is mature: Hardy-Ramanujan-Rademacher implementations with rigorous enclosures already exist. The opportunity is exporting that style to other coefficient families, not beating partition specialists immediately.

- Continued-fraction identity discovery already has a modern example in the Ramanujan Machine. The open opportunity here is function/kernel libraries and q-series representation search, not just constants.

- FFTW-style planners already adapt transforms to hardware. Divisor-lattice scheduling should be framed as a search-space prior for planners/autotuners.

- The lost notebook has been extensively edited and many entries have proofs. The underexploited axis is computational packaging: executable forms, benchmarks, regimes, error bounds, and proof-status links.

## Concrete next build

Create an **Executable Ramanujan Identity Schema** with fields: source page/paper, normalized expression graph, assumptions, equivalent representations, numeric verifier, term-budget model, asymptotic/congruence metadata, proof-status pointer, and benchmark results. Populate the first batch from: Paper 3, Paper 21, Papers 25/28/30/36/37, and the highest-density notebook pages.
