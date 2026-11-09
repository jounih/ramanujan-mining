# Ramanujan Phase 2 TODO: primary-source mining + operator-basis compiler

Created: 2026-05-24
Purpose: preserve the current strategy in a durable, handoff-ready artifact so the project does not depend on chat context.

## 0. North star

Treat Ramanujan's notebooks, manuscripts, letters, and papers as a corpus of **compressed executable representations** rather than only a corpus of formulas.

The working hypothesis is:

> Ramanujan's apparent speed came partly from a compact operator basis: a small set of transformations that map hard-looking sums, products, recurrences, continued fractions, coefficients, and congruences into easier forms. Phase 2 should test, refine, and operationalize that hypothesis.

This reframes the earlier “free-energy / EBM normalizer” lens into a broader research program:

> **Ramanujan as an operator-basis compression system:** a repertoire of transforms that maps hard representations into cheap, checkable, high-density forms.

The immediate product should be a reproducible corpus pipeline and a practical **recognizer + transform registry + degeneracy catalogue**, not a vague collection of interesting formulas.

## 1. Current status from previous passes

### Already created locally in this chat/session

- `ramanujan_autonomous_run_full.zip`: first-pass corpus, notes, manifests, experiments.
- `ramanujan_wren_bulk_download_pack.zip`: scripts to bulk download Trinity/Wren IIIF page images outside this sandbox.
- `ramanujan_non_ebm_pass2.zip`: non-EBM mining pass with candidate queue, dense-page triage, and experiments.
- Claude-side repo branch noted in the pasted report: `claude/ramanujan-original-works-4TwPG`, with 11 experiments, 7 diary entries, HUNT_MAP, CANDIDATE_INSIGHTS, and RKC v0/v0.5.

### Key judgment calls to preserve

1. Claude's report is useful as a **hypothesis map**, not final evidence.
2. Term-count speedups are useful demonstrations but must not be overclaimed as wall-clock or general-purpose speedups.
3. The strongest path is **Hunt 5 + recognizer registry + degeneracy catalogue**.
4. The central lens should no longer be “partition-function normalizers only”; that is one deployment surface of a broader operator-basis compression pattern.
5. Highly-composite / divisor-rich scheduling is low priority unless framed as an autotuning search prior with a very specific benchmark.
6. Mock-theta / free-energy / bias-diagnostic ideas are high-upside but fragile; keep as a moonshot, not the mainline.
7. A good phase 2 result can be software/corpus/architecture novelty even if many individual identities are classical.

## 2. Project operating principles

### Non-negotiables

- Preserve image provenance: every formula record must trace to page image, source collection, page index, and checksum.
- Separate transcription confidence from mathematical confidence.
- Never label a formula “new” until it has passed a modern-reference/SOTA audit.
- Treat OCR as hypothesis generation; formulas need verification by symbolic/numeric checks.
- Record both successes and failures. Failure modes are central, not incidental.
- Benchmark direct/naive vs transformed routes using wall-clock, precision, memory, term count, and robustness.
- Keep a disciplined diary with dated entries, source pages, claims, tests, and unresolved uncertainties.

### Claim labels

Use exactly these labels in notes and candidate records:

- `classical_known`: established identity/algorithm; useful only as part of architecture or teaching.
- `rediscovered`: not new, but independently found in the corpus/pipeline.
- `software_packaging_novelty`: known math, novel recognizer/registry/integration/tooling.
- `benchmark_novelty`: known transform, but new benchmark family or routing comparison.
- `corpus_novelty`: new structured index, operator-tag statistics, or provenance graph.
- `proof_novelty`: new proof, corrected proof, new bound, or new validity condition.
- `failure_mode_novelty`: newly characterized degeneracy/silent-failure regime.
- `speculative`: interesting but not yet grounded enough.

## 3. Master workstreams

## Workstream A — Corpus acquisition, checksums, OCR, and page database

### Goal

Finish the primary-source substrate so future mining can run from original images, not only printed/edited versions.

### Immediate tasks

- [ ] Run `ramanujan_wren_bulk_download_pack/scripts/wren_ramanujan_downloader.py` on a normal internet-enabled machine.
- [ ] Save all IIIF manifests, page images, download logs, and failures.
- [ ] Run `make_page_index.py` immediately after download.
- [ ] Store `page_image_manifest.csv` with SHA-256 checksums.
- [ ] Record rights/attribution metadata from each manifest.
- [ ] Run Chandra OCR on a stratified sample first before batch OCR.
- [ ] Compare Chandra OCR, GPT multimodal reads, and existing printed transcriptions on the same sample.
- [ ] Choose a formula-centric record format instead of page-level blob storage.

### Acceptance criteria

- Every downloaded page has source URL, IIIF manifest URL, local path, SHA-256, dimensions, and rights note.
- OCR outputs are stored with tool version, parameters, confidence/uncertainty notes, and source image checksum.
- At least three OCR modes are compared on a calibration sample: Chandra, GPT/multimodal, and human/manual or edited transcription.
- No page enters the formula database without a stable page ID.

### Page ID format

Use:

```text
<collection>__<shelfmark_or_source>__p<zero_padded_page>
```

Examples:

```text
wren__Add.MS.a.94.15__p0007
notebook2__facsimile__p0054
lost_notebook__facsimile__p0008
```

## Workstream B — Hunt 5: operator-tagging the primary corpus

### Goal

Test the “latent-space speedrun” hypothesis directly: do Ramanujan's manipulations reduce to a small recurring set of operator primitives?

### Core question

For each formula/manipulation, ask:

> What transformation operator is being used to make the representation cheaper, denser, more checkable, or more general?

### Initial operator taxonomy

Use these tags first; refine only after tagging enough pages to see real ambiguity.

1. `MODULAR_TRANSFORM`: maps parameter to reciprocal/cusp/dual regime.
2. `POISSON_THETA_DUAL`: lattice/theta reciprocal summation.
3. `PRODUCT_TO_SERIES`: Euler/product/q-product to additive coefficient form.
4. `SERIES_TO_PRODUCT`: sum or recurrence to product/eta/q-product form.
5. `SERIES_TO_CONTINUED_FRACTION`: function/constant represented as CF.
6. `CONTINUED_FRACTION_TO_SERIES`: CF expanded to verify/generate terms.
7. `ASYMPTOTIC_EXTRACTION`: leading terms plus residual/tail structure.
8. `CONGRUENCE_SIEVE`: mod classes used as checksum, selection, or simplification.
9. `FINITE_GAUSS_COLLAPSE`: infinite/oscillatory object collapses under rational phase.
10. `PARAMETER_SPECIALIZATION`: hard identity becomes tractable at special values.
11. `PARAMETER_LIFTING`: special cases generalized via a parameter family.
12. `RECURRENCE_COMPILER`: coefficient family computed by recurrence rather than expansion.
13. `PARTIAL_FRACTION_LATENTS`: moments/traces decomposed into hidden poles/weights.
14. `RAMANUJAN_SUM_PERIODICITY`: arithmetic periodic basis / divisor-indexed trig sum.
15. `ELLIPTIC_AGM_ACCELERATION`: elliptic/modular/AGM route to faster convergence.
16. `MOCK_MODULAR_COMPLETION`: mock/false/partial theta object plus correction/shadow.
17. `COMBINATORIAL_BIJECTION_OR_REINDEX`: reindexing/repartitioning that reduces dimension.
18. `NUMERICAL_VERIFIER`: compact identity used as a check rather than primary computation.
19. `UNKNOWN_OPERATOR`: clear manipulation, operator not yet classified.
20. `NOT_A_TRANSFORM`: page contains definitions, prose, or formula with no visible operator.

### Tagging protocol

For each page:

1. Segment the page into formula blocks.
2. Transcribe formula block with uncertainty markers.
3. Assign 1–3 operator tags.
4. Record the apparent input representation and output representation.
5. Record what became cheaper: fewer terms, faster convergence, finite collapse, better conditioning, smaller proof, modular symmetry, easier verification, etc.
6. Link to known printed formula or modern theorem if available.
7. Create executable test where possible.
8. Mark proof/SOTA status.

### Sampling ladder

- [ ] Calibration batch: 25 pages across notebooks, lost notebook, letters, and published-paper facsimiles.
- [ ] Dense batch: top visually dense pages from the previous page-density triage.
- [ ] Thematic batch: continued fractions, q-series, congruences, asymptotics, modular equations.
- [ ] Exhaustive batch: all pages with mathematical content.

### Acceptance criteria

- At least 500 formula blocks tagged before drawing strong statistics.
- Inter-rater or agent-agreement check on at least 50 formula blocks.
- Confusion matrix for operator tags.
- Distribution of operator tags by source, date, topic, and page type.
- A ranked list of “unusual operator combinations” for deeper mathematical review.

## Workstream C — Recognizer registry + transform compiler

### Goal

Turn the corpus-mined operator basis into executable tooling.

### Recognizer registry concept

Each registry entry should answer:

- What input pattern is recognized?
- What transform is available?
- When is it valid?
- When does it fail or become worse?
- What certificate/error bound is attached?
- What exact/approximate libraries already implement it?
- What benchmarks prove it is useful?

### Seed registry entries

- [ ] Gaussian theta / Jacobi transform.
- [ ] Dedekind eta / q-product S-transform.
- [ ] Partition pentagonal recurrence.
- [ ] Hardy–Ramanujan–Rademacher coefficient reconstruction.
- [ ] Ramanujan sums as periodic basis atoms.
- [ ] Finite Gauss sums with rational phases.
- [ ] Rogers–Ramanujan continued fraction/product/series switches.
- [ ] General continued-fraction approximants for constants/functions.
- [ ] Moment/power-sum to rational generating function / Prony latent decomposition.
- [ ] Congruence checksums for partition-like sequences.
- [ ] Mock/false/partial theta with correction term and boundary-regime warning.

### Degeneracy catalogue

This is a first-class output, not an appendix. For every transform, record failure cases such as:

- Direct route faster for moderate/small parameters.
- Dual route causes precision loss.
- Rational snapping changes the problem rather than approximating it safely.
- Gauss sum vanishes or aliases under specific denominator classes.
- Recurrence becomes numerically unstable.
- Modular transform lands at a bad cusp or high-level cusp with expensive multipliers.
- Continued fraction converges slowly or has misleading early approximants.
- Tail bound too loose to be useful.

### Acceptance criteria

- Minimum viable registry: 10 entries, each with tests, validity conditions, degeneracy modes, and benchmark scripts.
- Recognizer routing must report `recognized`, `not_recognized`, or `unsafe`, never silently choose a transform.
- Every transform must include a direct baseline and at least one adversarial/failure-case test.
- Benchmarks must separate term count, wall-clock, precision, memory, and setup cost.

## Workstream D — Experiments and benchmarks

### Benchmark rules

- Always include direct baseline, transformed route, and a “transform not helpful” control.
- Always record parameter regime, precision target, hardware, Python/library versions, and wall-clock method.
- Use term count as a diagnostic, not the headline metric unless wall-clock is impossible.
- Include correctness certificates: interval bounds, residual checks, modular checksums, or independent implementation comparisons.

### Experiment backlog

#### D1. Ramanujan-Prony latent decomposer

- [ ] Implement sequence-to-rational-generating-function recovery.
- [ ] Compare against Berlekamp–Massey, Padé, matrix pencil, sparse FFT where applicable.
- [ ] Mine paper/notebook formulas that define sequences or moments.
- [ ] Score compression ratio, extrapolation accuracy, and symbolic interpretability.
- [ ] Look for cases where poles/weights reveal simple algebraic or modular structure.

#### D2. Ramanujan-sum periodicity layer

- [ ] Build clean NumPy implementation of Ramanujan-sum feature transform.
- [ ] Compare against Fourier features on integer-period synthetic data.
- [ ] Add noisy, missing-data, and mixed-period tests.
- [ ] Try simple differentiable layer in PyTorch/JAX if available.
- [ ] Record when Fourier wins, ties, or loses.

#### D3. q-series representation compiler

- [ ] Select 20 q-series identities from notebooks/lost notebook/papers.
- [ ] Encode product, sum, recurrence, continued fraction, modular, and asymptotic forms when available.
- [ ] Implement router choosing cheapest route for coefficient query, evaluation query, or proof/check query.
- [ ] Compare against direct expansion and existing CAS where possible.

#### D4. Congruence checksums

- [ ] Convert Ramanujan-style congruences into runtime validators.
- [ ] Inject random and structured errors into partition-like computations.
- [ ] Measure detection probability, false positives, and cost.
- [ ] Generalize beyond partition numbers: eta-products, divisor sums, modular coefficients.

#### D5. Continued-fraction executable approximants

- [ ] Start from known Ramanujan continued fractions.
- [ ] Build evaluator with convergence diagnostics and failure warnings.
- [ ] Search small CF families for constants/functions, using Ramanujan Machine as conceptual baseline.
- [ ] Compare against Padé/minimax/rational approximants.

#### D6. Rational snapping + Gauss-sum degeneracy note

- [ ] Formalize the “silent zero” / denominator-class failure mode.
- [ ] Generate reproducible examples and counterexamples.
- [ ] Search literature before calling it novel.
- [ ] If still promising, write as a short technical note with narrow claims.

#### D7. Mock-theta / bias diagnostic moonshot

- [ ] Do not lead with this.
- [ ] Find a non-contrived model whose partition-like object is genuinely mock/false/partial theta.
- [ ] Show a fitted approximation where missing the correction/shadow causes measurable bias.
- [ ] Only then connect to free-energy/FEP/EBM language.

#### D8. Divisor-lattice scheduling prior

- [ ] Keep low priority.
- [ ] Reframe as reducing autotuning search, not beating FFTW/cuFFT/MKL generally.
- [ ] Require a specific workload where divisor-rich candidate generation beats random/grid search under equal tuning budget.

## Workstream E — SOTA audit and novelty discipline

### Goal

Prevent self-deception. Every candidate must be sorted into known math, known software, new integration, new benchmark, new failure mode, or genuinely new mathematical content.

### Audit workflow

For each candidate:

1. Write the exact claim in one sentence.
2. Write the weakest version of the claim that is still useful.
3. Search modern references, library docs, and known implementations.
4. Record prior art and closest known results.
5. Classify novelty using the claim labels above.
6. Update candidate priority based on audit outcome.

### Evidence ladder

- Level 0: intuition only.
- Level 1: page/source located.
- Level 2: transcription checked.
- Level 3: numerical verification on examples.
- Level 4: symbolic/proof sketch or independent reference.
- Level 5: benchmark with baselines.
- Level 6: SOTA audit complete.
- Level 7: reproducible artifact or paper draft.

## Workstream F — Publication / deliverable paths

### F1. Architecture/software paper

Working title:

> A degeneracy-aware operator registry for Ramanujan-style representation switching

Core contribution:

- Kernel/formula recognizers.
- Transform registry.
- Validity and degeneracy conditions.
- Tail/error certificates.
- Composite routing.
- Benchmarks across theta, q-products, partitions, continued fractions, Ramanujan sums, and recurrence discovery.

Minimum result needed:

- 10 registry entries.
- 5 benchmark families.
- Failure-mode catalogue.
- Corpus-derived operator taxonomy.

### F2. Corpus/operator-basis paper

Working title:

> Ramanujan's operator basis: a primary-source taxonomy of compressed mathematical representations

Core contribution:

- Page-level and formula-level provenance.
- Operator-tag database.
- Statistics showing whether a small operator basis explains many manipulations.
- Examples linking original pages to modern executable forms.

Minimum result needed:

- 500+ formula blocks tagged.
- Cross-checking between two taggers/agents.
- Clear uncertainty policy.
- SOTA/proof-status links for top examples.

### F3. Short technical note

Working title:

> A silent failure mode in rational-phase Gauss-sum acceleration

Core contribution:

- Narrow theorem/example/counterexample.
- Reproducible numerical demonstration.
- Literature audit.

Minimum result needed:

- Formal statement.
- Proof or complete derivation.
- Evidence that the framing/failure mode is not already standard in the target literature.

### F4. Software package / benchmark suite

Working title:

> rkc: Ramanujan kernel compiler

Core contribution:

- Recognizers.
- Safe routing.
- Tail certificates.
- Failure warnings.
- Benchmark harness.
- Corpus-derived examples.

Minimum result needed:

- Clean install.
- CLI and Python API.
- Registry schema.
- Tests.
- Reproducible notebooks/scripts.

## 4. Prioritized backlog

### P0: keep project state durable

- [ ] Commit this TODO into the repo.
- [ ] Add links to all artifacts from ChatGPT and Claude.
- [ ] Create `PROJECT_LEDGER.md` listing source files, scripts, manifests, and decisions.
- [ ] Create `DECISIONS.md` with date-stamped strategic decisions.
- [ ] Create `CLAIMS.md` with all claims and evidence levels.

### P1: unblock primary scans

- [ ] Run Wren downloader externally.
- [ ] Fix any manifest parsing failures.
- [ ] Produce page manifest and checksums.
- [ ] Bring page manifest back into the analysis repo.

### P1: define data schemas before mass OCR

- [ ] Adopt `formula_record_schema.json`.
- [ ] Adopt `operator_tag_taxonomy.json`.
- [ ] Adopt `transform_registry_entry_schema.json`.
- [ ] Add validation scripts.

### P1: start Hunt 5 sample

- [ ] Select 25 calibration pages.
- [ ] OCR/transcribe formula blocks.
- [ ] Tag operators.
- [ ] Review disagreements.
- [ ] Update taxonomy only if needed.

### P1: recognizer registry MVP

- [ ] Implement registry loader.
- [ ] Encode 10 seed entries.
- [ ] Add tests and degenerate cases.
- [ ] Add benchmark harness.

### P2: candidate experiments

- [ ] Ramanujan-Prony latent decomposer.
- [ ] Ramanujan-sum periodicity layer.
- [ ] q-series representation compiler.
- [ ] Congruence checksum validator.
- [ ] Continued-fraction approximant explorer.
- [ ] Rational snapping / Gauss-sum failure note.

### P3: lower-priority speculative lanes

- [ ] Mock-theta bias diagnostic.
- [ ] Divisor-lattice scheduling prior.
- [ ] Cryptanalysis/SEA modular equation acceleration.

## 5. Division of labour across agents/tools

### Claude Code should do

- Repo organization and commits.
- Testable Python package structure.
- Benchmark harnesses.
- CI-style tests.
- Running experiments repeatedly.
- Git branch hygiene and issue tracking.

### ChatGPT/GPT should do

- OCR sanity checks on difficult formula images.
- Synthesis and candidate prioritization.
- SOTA/literature audits with citations.
- Writing paper outlines and claim-discipline memos.
- Creating schemas, prompts, and review rubrics.

### Chandra should do

- Bulk OCR over page images.
- Layout-aware HTML/Markdown/JSON extraction.
- Initial math/handwriting hypothesis generation.

### Human/math reviewer should do

- Verify high-value transcriptions.
- Judge whether operator tags reflect actual mathematical intent.
- Check proof sketches.
- Decide publishability after SOTA audit.

## 6. Recommended repository layout

```text
ramanujan-operator-basis/
  README.md
  PROJECT_LEDGER.md
  DECISIONS.md
  CLAIMS.md
  data/
    raw_manifests/
    raw_page_images/            # gitignored or pointer-managed
    page_image_manifest.csv
    formula_records.jsonl
    operator_tags.jsonl
    transform_registry.yaml
  docs/
    RAMANUJAN_PHASE2_TODO.md
    corpus_methodology.md
    operator_taxonomy.md
    degeneracy_catalogue.md
    publication_plans.md
  scripts/
    download_wren.py
    make_page_index.py
    run_chandra_ocr.py
    extract_formula_blocks.py
    validate_formula_records.py
    validate_registry.py
  rkc/
    __init__.py
    recognizers/
    transforms/
    certificates/
    registry.py
    routing.py
  experiments/
    prony_latents/
    ramanujan_sums/
    q_series_compiler/
    congruence_checksums/
    continued_fractions/
    gauss_snapping/
    mock_theta_moonshot/
  notebooks/
  reports/
  tests/
```

## 7. Formula record schema summary

Each formula block should eventually have:

- `formula_id`
- `page_id`
- `source_collection`
- `image_path`
- `image_sha256`
- `crop_box`
- `transcription_latex`
- `transcription_confidence`
- `uncertainty_notes`
- `operator_tags`
- `input_representation`
- `output_representation`
- `computational_gain_hypothesis`
- `verification_status`
- `known_reference_status`
- `modern_references`
- `executable_test_path`
- `claim_label`
- `evidence_level`
- `review_notes`

## 8. Transform registry schema summary

Each transform entry should have:

- `transform_id`
- `name`
- `operator_tags`
- `input_fingerprint`
- `output_representation`
- `validity_conditions`
- `degeneracy_modes`
- `certificate_type`
- `error_bound`
- `direct_baseline`
- `benchmark_cases`
- `known_implementations`
- `sota_notes`
- `source_examples`
- `tests`
- `status`

## 9. Immediate next operations

Do these in order:

1. Put this TODO into Claude's repo.
2. Run the Wren downloader externally and produce the full page manifest.
3. Select 25 calibration pages for Hunt 5.
4. Run Chandra on those pages; keep raw OCR output.
5. Manually/GPT-check formula blocks on the same 25 pages.
6. Tag operators using the seed taxonomy.
7. Create the first `formula_records.jsonl` and `operator_tags.jsonl`.
8. Encode 10 seed transform-registry entries.
9. Run at least one benchmark and one adversarial/failure-case benchmark per entry.
10. Write `DEGENERACY_CATALOGUE.md` before writing any optimistic paper abstract.

## 10. First 10 GitHub issues to open

1. **Set up Phase 2 ledger and schemas**
   - Add project ledger, decisions log, claims log, formula schema, operator taxonomy, registry schema.

2. **Run Trinity/Wren bulk downloader and freeze checksums**
   - Produce page manifest, image checksums, rights notes, and failure log.

3. **Build 25-page Hunt 5 calibration sample**
   - Select diverse pages; record page IDs and rationale.

4. **Run Chandra OCR on calibration sample**
   - Save JSON/HTML/Markdown outputs and tool parameters.

5. **Create formula-block extraction workflow**
   - Crop or segment formula blocks; assign stable formula IDs.

6. **Tag calibration sample by operator taxonomy**
   - Produce operator_tags.jsonl and disagreement notes.

7. **Implement recognizer registry loader and validator**
   - Load YAML/JSON entries; validate schema; fail loudly on missing degeneracy/certificate fields.

8. **Seed 10 recognizer entries with tests**
   - Include positive, negative, and degenerate cases.

9. **Create benchmark harness**
   - Standard metrics: term count, wall-clock, precision, memory, setup cost, correctness certificate.

10. **Write degeneracy catalogue v0**
    - For every seed entry: when not to use it, how it fails, and how router should report unsafe.

## 11. Candidate priority table

| Candidate | Priority | Why | Next concrete action | Kill criterion |
|---|---:|---|---|---|
| Hunt 5 operator tagging | P1 | Tests core speedrun/operator-basis hypothesis directly | Tag 25 calibration pages | Tags remain incoherent after calibration |
| Recognizer registry + degeneracy catalogue | P1 | Most practical software architecture | Implement 10 seed entries | Existing libraries already expose same safe routing cleanly |
| Ramanujan-Prony latent decomposer | P1 | Closest to latent-compression intuition | Compare with Padé/Berlekamp–Massey | No advantage over existing methods on corpus-derived examples |
| Ramanujan-sum periodicity layer | P2 | Practical signal/time-series angle | Noisy/missing data benchmark vs Fourier | Fourier dominates on all realistic regimes |
| q-series representation compiler | P2 | Directly corpus-aligned | 20 identities, route by query type | Existing CAS already routes equivalently with certificates |
| Congruence checksums | P2 | Cheap runtime validation | Error-injection experiments | Too many false negatives or too narrow |
| Continued-fraction approximants | P2 | Ramanujan Machine-adjacent | Function/kernel targets beyond constants | Search duplicates known methods only |
| Gauss-sum rational snapping note | P2 | Narrow, publishable if novel | Formalize failure mode | Literature shows exact same note already standard |
| Mock-theta bias diagnostic | P3 | High-upside but fragile | Find non-contrived model | Only metaphorical connection emerges |
| Divisor-lattice scheduler | P3 | Weak unless tightly scoped | Equal-budget autotuning test | No workload where it improves search |

## 12. Research diary template

Use the template in `templates/research_diary_entry.md`. Every entry should answer:

- What source pages/formulas were inspected?
- What operator tags were assigned?
- What computational hypothesis was generated?
- What verification was attempted?
- What failed?
- What changed in the TODO/backlog?
- What claim labels/evidence levels changed?

## 13. Stop conditions / red flags

Pause and re-evaluate if any of the following happen:

- The pipeline is generating formula records without stable page/image provenance.
- “Novel” claims are appearing before SOTA audit.
- Benchmarks are only reporting term counts and not wall-clock/certificates.
- Degeneracy cases are postponed.
- OCR errors are being treated as mathematical content.
- The project drifts back into broad free-energy metaphor without concrete transforms.
- Operator tags are too vague to be executable.

## 14. One-sentence handoff prompt

> Continue Ramanujan Phase 2 by building a primary-source formula database and degeneracy-aware operator registry: first run the Wren downloader, freeze page checksums, tag a 25-page Hunt 5 calibration sample by operator primitives, seed 10 safe recognizer entries with failure modes and benchmarks, and classify every candidate claim by evidence level before making novelty claims.
