# Claude Code continuation prompt

We are continuing the Ramanujan Phase 2 project. Start by reading `docs/RAMANUJAN_PHASE2_TODO.md`, then implement the durable scaffolding before doing new experiments.

Primary objective:
Build a primary-source formula database and degeneracy-aware operator registry for Ramanujan-style representation switching.

Do the following in order:

1. Commit the Phase 2 TODO pack into the repo.
2. Create or update:
   - `PROJECT_LEDGER.md`
   - `DECISIONS.md`
   - `CLAIMS.md`
   - `docs/DEGENERACY_CATALOGUE.md`
3. Add JSON schemas for formula records, operator tags, and registry entries.
4. Implement validators for formula records and registry entries.
5. Encode the 10 seed registry entries from `seed_registry/ramanujan_transform_registry_seed.yaml` into the repo registry format.
6. Create tests for each entry: positive, negative, and degenerate/unsafe cases.
7. Build a benchmark harness that records term count, wall-clock, precision, memory, setup cost, correctness certificate, and hardware/library metadata.
8. Prepare the Hunt 5 calibration workflow, but do not mass-OCR until the page-image manifest exists.

Key constraints:

- Do not claim novelty until SOTA audit is done.
- Do not report term-count speedups as general wall-clock speedups.
- Degeneracy modes and failure cases are required, not optional.
- Recognizer output must be one of `recognized`, `not_recognized`, or `unsafe`.
- The mainline is Hunt 5 + registry + degeneracy catalogue. Mock-theta/FEP and divisor scheduling are lower-priority lanes.

Deliverables for this coding pass:

- Passing schema validators.
- Seed registry entries loaded and validated.
- Test skeletons or tests for positive/negative/degenerate cases.
- Updated project ledger and claims log.
- A short report listing what is now executable and what remains blocked by external Wren download.
