# Ramanujan mining diary — first autonomous pass

Run created: 2026-05-24T09:38:59.666936+00:00

## Mission

Locate publicly accessible scans or facsimiles of Ramanujan's original-source material, save a local working corpus, then begin mining for computation-relevant ideas, especially for energy-based models, variational/free-energy computation, symbolic acceleration, and low-energy numerical methods.

## 1. Corpus acquisition log

### 1.1 Online Ramanujan corpus

Saved the four notebook facsimile PDFs:

| item | PDF pages | extracted page images | local path |
|---|---:|---:|---|
| Notebook 1 | 380 | 380 | `pdfs/notebooks/notebook1.pdf` |
| Notebook 2 | 355 | 355 | `pdfs/notebooks/notebook2.pdf` |
| Notebook 3 | 35 | 35 | `pdfs/notebooks/notebook3.pdf` |
| Lost Notebook | 379 | 379 | `pdfs/notebooks/lost_notebook.pdf` |

Saved 37 published-paper PDFs as `pdfs/published/published_ram01.pdf` through `published_ram37.pdf`, and extracted their text to `text/`.

### 1.2 Trinity College manuscripts

Inventoried Trinity College archive links for `Add.MS.a.94.1` through `Add.MS.a.94.18` and `Add.MS.a.396`. The archive states that Ramanujan's papers have been digitised and provides digital viewer links. In this run, I saved only a reference image for Add.MS.a.396, not the full set of Wren/UV high-resolution page images.

## 2. Integrity and reproducibility

- `manifests/file_manifest.csv` contains SHA-256 checksums for all locally saved files.
- `manifests/published_papers_manifest.csv` maps the 37 papers to titles, source URLs, local files, page counts, byte sizes, and themes.
- `manifests/notebooks_manifest.csv` maps the four notebook PDFs to local paths and extracted image folders.
- `manifests/trinity_archival_manifest.csv` records the archival digital viewer URLs still needing full-page download.

## 3. Mining discipline used in this first pass

1. Separate source acquisition from interpretation.
2. Label every idea as one of: established, known modern SOTA, plausible recombination, or speculative conjecture.
3. Prefer computational tests over impressionistic admiration.
4. Treat Ramanujan's terse formula style as a compression signal: ask what representation makes a hard calculation short.
5. Compare to modern bottlenecks: partition functions, MCMC bias, variational free energy, modular/duality transforms, coefficient extraction, and hardware-aware scheduling.

## 4. Immediate source-level observations

### O1 — Ramanujan repeatedly reduces infinite or dense calculations to sparse residue classes.

Visible already in the first published paper on Bernoulli numbers: root-of-unity and trigonometric decompositions separate Bernoulli subsequences and reduce recurrence terms. This is a recurring compression pattern: choose a transform basis where only one congruence class or frequency band remains.

Computational translation: search for small finite symmetry groups acting on a target sum/partition function; average over the group to annihilate irrelevant modes before numerical summation.

### O2 — Several papers are directly about normalizers in disguise.

Partition functions in statistical mechanics and EBMs are normalizing constants. Ramanujan's partition work, theta/quadratic-form papers, infinite products, modular equations, and Hardy-Ramanujan asymptotics all revolve around efficient coefficient extraction or normalization of generating functions.

Computational translation: for models with lattice, quadratic, periodic, product, or q-series structure, symbolic duality should be tried before sampling.

### O3 — Highly composite numbers are a scheduling primitive, not just a number-theory curiosity.

A divisor-rich dimension admits many factorizations, which means more possible tilings, radix decompositions, and communication layouts. This run produced `experiments/divisor_rich_block_sizes.csv` as a first table of divisor-rich sizes up to 8192.

Computational translation: instead of choosing powers of two by habit, choose block sizes by a multi-objective score combining divisor count, cache fit, tensor-core alignment, and padding overhead.

### O4 — Mock theta functions point to boundary asymptotics.

The final-letter/lost-notebook material is valuable for regimes where ordinary modular approximations are nearly right but fail at roots of unity or other singular boundaries. That pattern resembles modern failures near phase transitions, complex phases, or sharp posterior boundaries.

Computational translation: add a “mock correction” term to dual/asymptotic approximations when the leading theta/modular component leaves structured residuals.

## 5. First computational experiment

`experiments/toy_theta_partition_acceleration.csv` tests the simplest energy-model normalizer

`Z(β) = Σ_{n∈Z} exp(-β n²)`.

A direct sum becomes expensive for small β. Jacobi reciprocity rewrites it as

`Z(β) = sqrt(π/β) Σ_{n∈Z} exp(-(π²/β)n²)`.

For β = 1e-6, the direct summation used 11,871 terms at the set tolerance, while the modular-dual expression used 1 term with floating-point agreement at display precision. This is not new mathematics; it is a sanity check for the broader “representation switch” theme.

## 6. Limitation log

- No reliable handwriting OCR was attempted for the notebook images.
- No claim is made that all private letters, marginal notes, school exercises, or every archival scan worldwide were captured.
- Full Trinity Wren/UV high-resolution page mirroring remains incomplete.
- The insights below are research hypotheses, not proofs.
