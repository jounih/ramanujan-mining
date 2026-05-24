# Ramanujan Mining Run — Handoff Brief

You are taking over an ongoing research run that has been running across
multiple Claude Code sessions (remote + now local). The run is mining
Ramanujan's mathematical work for novel insights in three areas:
**(1) computation acceleration**, **(2) energy-based modeling / Friston FEP**,
**(3) "latent-space speedrun" — what compressed representations Ramanujan
carried in his head**.

This file is your orientation. Read it once, then start from `todo.md`.

---

## First five files to read (in order)

1. `diary/00_charter.md` — mission, operating discipline, corpus inventory
2. `diary/INDEX.md` — every diary entry with topic + source pointer
3. `todo.md` — current state of every Pass A/B/C/D/E + cross-cutting deliverable
4. `insights/CANDIDATE_INSIGHTS.md` — every substantiated finding, with confidence + novelty tags
5. `insights/DID_NOT_PAN_OUT.md` — the equally-important refuted / corrected speculations

After those five files you'll know what's been done, what's pending, and what was tried and didn't work. Then read `insights/HUNT_MAP.md` for the prioritized targets that need primary-scan access.

---

## File layout

```
ramanujan/
├── CLAUDE.md                  ← you are here
├── todo.md                    ← live state of all passes
├── analysis/                  ← experiment scripts; numbered ##_*.py
│   ├── 02..21_*.py            ← experiments (some skipped — see todo)
│   └── results/               ← every script writes a *.csv here
├── diary/                     ← numbered ##_*.md entries
│   ├── 00_charter.md
│   ├── INDEX.md               ← keep updated when adding entries
│   └── 01..18_*.md            ← latest entry # is the head of the run
├── insights/                  ← synthesis documents
│   ├── CANDIDATE_INSIGHTS.md  ← positive findings, organized A/B/C/D/E
│   ├── DID_NOT_PAN_OUT.md     ← refuted / corrected / outstanding
│   └── HUNT_MAP.md            ← priority targets for primary-scan access
├── manifest/                  ← cataloging of primary sources (per Berndt-Andrews bibliography)
├── sota_comparisons/          ← what published work covers vs doesn't
├── corpora/                   ← primary sources
│   ├── scans/                 ← raw facsimile PDFs (gitignored above 1MB)
│   ├── transcriptions/        ← LaTeX/unicode transcriptions
│   │   ├── README.md          ← format spec
│   │   ├── operator_tagging_schema.py  ← 6-operator schema for Hunt 5
│   │   └── quarterly_reports/ ← naming spec: qr<N>_section_<M>.tex
│   ├── RamanujanMachine/      ← vendored 3rd-party (Trinity College Dublin project)
│   └── RamanujanMachine_v0/   ← older vendored fork
└── rkc/                       ← STANDALONE PACKAGE — kernel-fingerprint recognizer
    ├── __init__.py, recognizer.py, registry.py, routing.py, costs.py
    ├── completions.py         ← (if V1 has landed) wires MCR route to exp 17
    ├── README.md              ← 1-page worked example
    └── tests/                 ← pytest unit tests; MUST stay green
```

There's also `.venv/` at `ramanujan/.venv/` — activate before running scripts.

---

## Conventions (non-negotiable)

### Provenance flags
Every cited identity carries one of:
- **(scan)** — primary source, page-cited; transcription expected in `corpora/transcriptions/`
- **(transcription)** — Berndt/Andrews printed text or verified GitHub mirror, cited
- **(training-memory)** — recalled from training data; **must be numerically verified before use** (≥50 digits via mpmath/PSLQ)

If a citation lacks a provenance flag, treat it as suspect.

### Diary discipline
- Every experiment session writes a numbered, dated entry in `diary/`.
- Each entry: `# Diary <N> — <topic>` + Date + Source/Status + body.
- Body: setup, what you did, numbers, surprises, one-line bottom-line claim with confidence tag (high/medium/low/indicative).
- Update `diary/INDEX.md` when you add an entry.

### Claim discipline (strict)
- Every numerical claim must be reproducible by running the script (no orphan numbers).
- Tag speculation explicitly. The boundary between observation and interpretation must be clear in every diary entry.
- **If a "near match" exists in an experiment, report it as a near-match with the specific deviation pattern — never as a match.** Noisy positives are the worst possible outcome.
- The strict bar for proportionality claims: ≤1% relative deviation across ≥2 orders of magnitude in the swept parameter.
- Honest "did not pan out" entries go in `insights/DID_NOT_PAN_OUT.md`. The credibility of the run depends on this file growing alongside `CANDIDATE_INSIGHTS.md`.

### Bug-find protocol (per T7's mock-theta v0 bug)
The strongest single methodological lesson from the run: **rerun prior work with explicit "verify rigorously" instructions every few experiments**. T7 caught a real character-parity bug in v0 of the mock-theta toy that the original session's introspection missed. If you find a similar bug while extending earlier work, retract the prior claim in `DID_NOT_PAN_OUT.md` and ship the fix — never paper over.

---

## Environment

### Local vs remote
- **This file was written from the REMOTE Claude-Code-on-the-web session.** The remote env has constraints the local env may not: no outbound HTTP except github/pypi/npm + WebSearch tool; no archive.org/Trinity/arXiv direct; no binary-PDF download; no PARI/GP (cypari2 fails to build); ephemeral container.
- **The local env almost certainly has more capabilities** — full network for arXiv/Wikipedia, ability to install PARI/GP, persistent filesystem for large PDFs, and (critically) direct access to wherever the user is storing primary-source scans.
- **If you need a PDF that the remote agent couldn't fetch, fetch it.** Just commit it under `corpora/scans/` with a SHA-256 manifest; the `.gitignore` excludes files >1MB so it stays out of history. Add a `corpora/scans/MANIFEST.tsv` if multiple PDFs land.

### Dependencies
```
python 3.11
sympy 1.14
mpmath 1.3
numpy
pytest (for rkc/tests)
```
All in `ramanujan/.venv/`. Activate: `source ramanujan/.venv/bin/activate`.
If you need PARI/GP (for class-number / modular-polynomial work), install it locally and document the dependency in any new script.

### Branch
- Working branch: `claude/ramanujan-original-works-4TwPG`
- Branch is merged to `Main` as of commit `599d5a5`. Re-merge after major work, or keep developing on the feature branch and merge in one go.
- **Default expectation**: commit & push to the feature branch frequently. The remote env has a stop-hook that complains about untracked files; the user's preference is "commit and push frequently."

---

## Git workflow

```bash
# Standard cycle when finishing an experiment:
git add ramanujan/analysis/NN_*.py ramanujan/analysis/results/NN_*.csv ramanujan/diary/NN_*.md
git commit -m "Exp NN: <one-line summary>"
git push origin claude/ramanujan-original-works-4TwPG

# Do NOT push to Main directly. Merge feature → Main with --no-ff after major checkpoints.
# Do NOT use --no-verify or --no-gpg-sign.
# Do NOT amend published commits.
```

If the user asks you to "merge to Main" again: use `--no-ff` so the merge commit is easy to identify when they split repos. The plan is to split `ramanujan/` into its own repository — see git-filter-repo notes below.

---

## Current state (as of handoff, branch HEAD at commit `f289a51` or later)

### Completed
- **Pass A (representation switching)**: 5 kernels substantiated (Gaussian theta, Bose-Einstein partition, Lambert-Eisenstein, π methods, divisor sum). Universal β\* = c·π crossover pattern (§A6); per-term-cost vs term-count framing (§A7).
- **Pass B (recognizer)**: shipped as standalone `rkc/` package. v2 hits **55/55 = 100%** on the routing benchmark with macro precision 1.00. **50 passing unit tests** (35 base + 15 completions). `MODULAR_COMPLETION_REQUIRED` route wired through to Watson-Hickerson Eichler integral — **f3 mock-theta inputs return numerical values to ≥30 digits with a certificate**; f5/f7 surface `CompletionNotImplemented` honestly.
- **Pass D (FEP × mock-modular bridge) — CLOSED for the candidate-family approach**: forward direction confirmed as an *identity* (lattice gas → f(q) to 25-50 digits); reverse direction *falsified for 20 candidates across 5 structurally-different families* (Exp 16: 4 marginal divergences, Exp 18: 8 bounded-at-cusp, Exp 20: 4 Wigner-negativity, Exp 21: 3 path-measure, Exp 22: transfer-matrix eigenstructure). Two decisive structural arguments anchor the closure (Exp 21 path-direction; Exp 22 (K+1)² dim mismatch + Watson-reduction). **The cohomological-irreducibility conjecture is essentially established at medium-high → high confidence**: g\* is irreducibly an Eichler cocycle in H¹(Γ, V_k).
- **Cross-cutting deliverables**: `insights/CANDIDATE_INSIGHTS.md` (positive findings), `insights/DID_NOT_PAN_OUT.md` (14 entries + 6 outstanding), `insights/HUNT_MAP.md` (scan-blocked targets), `corpora/transcriptions/operator_tagging_schema.py` (6-operator schema ready for Hunt 5).

### Blocked on primary scans (priority order per user-confirmed sourcing pipeline)
1. **Berndt-Rankin Quarterly Reports** → unlocks Hunt 5 (operator-tagging test of latent-space-speedrun hypothesis). **Highest-leverage single source — this is the user's central question.** Schema is ready at `corpora/transcriptions/operator_tagging_schema.py`.
2. **Andrews-Berndt Lost Notebook Part IV pp. 341-343** → unlocks Hunt 1 (1729-K3 inventory).
3. **Berndt Notebooks Part V Ch. 32** → unlocks Hunt 3 (Eisenstein-style CFs) — would add the recognizer's missing quasi-modular (weight-2 anomaly) registry entry.
4. **Berndt Notebooks Parts III-V** modular equations at levels 23+ → unlocks Hunt 2.
5. **Cooper Theta Functions** → unlocks Hunt 6 (RS series at moonshine levels).
6. **Andrews-Berndt LN Vol I supplement pp. 200-220** → unlocks Hunt 4 (class invariants); partial work in Exp 08 verified 8 invariants via PSLQ.

When material arrives, drop under `corpora/scans/<source-tag>/` (or `corpora/transcriptions/<source-tag>/` if pre-OCR'd). The `.gitignore` excludes binary facsimiles >1MB.

### Next-pass leads (tractable WITHOUT scans, in order of value)

1. **f5/f7 Watson-Hickerson instrumentation for `rkc/completions.py`** — requires transcribing Hickerson 1988 / Berndt-Chan identities for the higher-order mock thetas; out of scope in the original remote env but natural with local network / PDF access. After this, the recognizer is end-to-end complete on all three registered mock-theta families.
2. **`recognize_composite` `numerical_completion` propagation** — cheap fix flagged in diary 16; deferred. Wire the opt-in flag through to per-component calls so composites return values not flags.
3. **Watson-identity calibration regime extension** — the W-partner formula in `analysis/17_*.py` is calibrated only for α ≤ 0.7; in (0.7, π) results are tagged `regime="near-cusp-warning"` with uncomputed q₁⁴ correction. Computing the next-order correction extends the calibrated regime.
4. **The cohomological generative model** — given the B1 closure, the question shifts from "find the shadow as a functional" to "build a generative model that has H¹(Γ, V_k) cocycle structure as a primitive." This is research-grade math, not a well-scoped experiment. See diary 19 §"what next" for entry points.

### Numbered experiment slots that are FREE
- **Experiments**: 23+ are clear. (00, 01 reserved historically; 02-22 used.)
- **Diary entries**: 20+ are clear.

---

## Known gotchas (these will bite you if you don't watch for them)

1. **Silent-zero hazard at Gauss sums q ≡ 2 mod 4** (§A4). Built into `rkc/registry.py` as a degeneracy detector. If you add a new Gauss-sum-related kernel, *test the degeneracy branch explicitly* — sympy auto-reduces `2n²/6 → n²/3` before the matcher sees it; use `recognize_with_raw_string` for AST-pre-reduction work.

2. **Character parity in mock-theta shadows** (T7's bug). The unary theta shadow of Ramanujan's f3 uses the **ODD primitive character mod 12**, not the even Kronecker character. Using the even one makes the weight-3/2 theta with `n` in front vanish identically. Documented in `diary/12_*.md` and `DID_NOT_PAN_OUT.md` R2.

3. **Mock-theta v0 asymptotic claim was wrong** (T7). The "1/√β" asymptotic for the bias is incorrect; the actual modular-only residual saturates at the Watson-Hickerson radial limit 4/3. See `DID_NOT_PAN_OUT.md` R1.

4. **Bits-per-term is a misleading routing metric** (§A7). The recognizer's cost estimator must use per-term complexity, not just term count. HRR uses 4× fewer terms than pentagonal recurrence at n=10⁵ but is comparable in wall-clock without binary-splitting + FLINT.

5. **Cross-validate before benchmarking** any new representation-switching pair. At least one (kernel, β) cell must match to ≥40 digits across both representations before you trust the comparison. See `analysis/12_*.py` for the template: it caught a sign-factor bug and a Bernoulli-prefactor cancellation that would have shipped silently otherwise.

6. **Strict claim discipline at candidate 3 of any "shadow probe"**. Any path-measure / Eichler-shaped candidate is the structurally-most-likely-to-match candidate in the FEP × mock-modular investigation. A noisy positive at one of those is the worst-possible outcome — hold the ≤1% / ≥2-dex bar ruthlessly. Falsify cleanly or confirm cleanly; nothing in between.

---

## Repo-split plan (when the user asks)

The `ramanujan/` directory was merged into `Main` alongside an unrelated `studio-gear-configurator` project as a temporary co-residence. The user plans to split. The clean extraction is:

```bash
# Clone a working copy, then:
git filter-repo --path ramanujan/ --path-rename ramanujan/:.

# This moves ramanujan/ contents to repo root and drops everything else.
# Run `git remote remove origin && git remote add origin <new-repo-url>`,
# then push to the new repo.
```

The vendored `RamanujanMachine/` and `RamanujanMachine_v0/` (~14K of ~17.7K lines on the merge) are 3rd-party code. Consider replacing with `git submodule` after the split — they're large and rarely modified.

---

## Bottom line

The intellectual win of this run is **the lens + the catalogue + a closed conjecture**, not new theorems:
- An operational kernel-fingerprint recognizer with documented failure modes, end-to-end on mock-theta f3;
- A universal β\* = c·π crossover pattern across five independent kernels;
- A **closed-verdict** FEP × mock-modular bridge story: forward direction = identity, reverse direction falsified for 20 independent candidates across 5 structurally-different families, sharpened cohomological conjecture established at medium-high → high confidence;
- The honest "did not pan out" log.

The deepest research question — *what compressed representations did Ramanujan carry in his head?* — is blocked on Hunt 5 (Quarterly Reports operator tagging). When those scans arrive, **that's the single highest-leverage experiment remaining in the entire run**. The 6-operator schema is ready and waiting.

Carry on with the same discipline. Commit & push frequently. Diary entries are the durable artifacts.

---

## Quick-start for a fresh Claude Code session

```bash
# 1. Get the latest branch
git fetch origin claude/ramanujan-original-works-4TwPG
git checkout claude/ramanujan-original-works-4TwPG
git pull --ff-only

# 2. Set up the venv (skipped from git history; ~30 seconds)
cd ramanujan
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Verify everything works
python -m pytest rkc/tests/        # expect 50/50 passing
python analysis/14b_recognizer_v2_benchmark.py  # expect 55/55 = 100%

# 4. Read CLAUDE.md (this file), then todo.md, then insights/CANDIDATE_INSIGHTS.md
# 5. Start work — incoming scans go under corpora/scans/<source-tag>/
```

If a primary-source scan arrives:
1. Drop the PDF under `corpora/scans/<source-tag>/`.
2. If you OCR or transcribe, put the text under `corpora/transcriptions/<source-tag>/`.
3. For Quarterly Reports specifically: use the schema at `corpora/transcriptions/operator_tagging_schema.py`, file under `corpora/transcriptions/quarterly_reports/qr<N>_section_<M>.tex`.
4. Then dispatch a Hunt-N agent (see `insights/HUNT_MAP.md` for the specific prediction each scan is meant to test).
