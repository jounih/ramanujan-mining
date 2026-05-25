# Five verified computational primitives — LaTeX source

This directory contains the LaTeX source for a verified-implementation
tool paper presenting five computational primitives obtained by applying
a Ramanujan-style operator basis to problem classes outside its native
number-theoretic domain.

The companion markdown draft is at
[`../2026-05_computational_primitives_tool_paper.md`](../2026-05_computational_primitives_tool_paper.md).
This LaTeX version is the submission-ready format with AMS class +
bibtex bibliography.

## Files

- `main.tex` — the paper source, ~3,000 words typeset
- `refs.bib` — bibliography (11 entries: RetNet, Mamba SSD,
  Lightning Attention, Crowdy–Marshall, Schrödinger 1914, Trovato 2016,
  DLMF, Mera–Pedersen–Nikolić, Borwein–Borwein–Taylor, Crandall–Buhler,
  Project C repo)

## Compile

If `pdflatex` + `bibtex` are installed:

```bash
cd papers/computational_primitives_tool_paper
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

Or use latexmk:

```bash
latexmk -pdf main.tex
```

On macOS, `brew install --cask mactex-no-gui` installs TeX Live;
on Linux, `apt install texlive-full` or equivalent.

## Pre-submission checklist

- [ ] Compile `main.tex` locally; verify all 11 citations resolve
- [ ] Verify every benchmark / verification table typesets cleanly
      (booktabs `\toprule` / `\midrule` / `\bottomrule`)
- [ ] Verify the `\cref` references resolve (sections referenced from
      the abstract and §5.4)
- [ ] Verify equation labels in §6 (Airy Tricomi-U) typeset the special
      function arguments correctly (the `\pm 2 i \eta` cases)
- [ ] Verify the CsCl Madelung equation (5.3.2) typesets the
      $r_3^{\mathrm{odd}}$, $r_3$, $h(N)$ shell-weighting clearly
- [ ] Update DLMF release date in `refs.bib` to the actual release
      cited (currently a placeholder `2026-XX-XX`)
- [ ] Final proof-read for word repetition (likely concentrations:
      "speedup", "baseline", "asymptotic", "verified")
- [ ] Confirm subject classifications (currently 65D20, 65Y20 primary;
      33C10, 33E12, 68T07, 82B20 secondary) match target venue
- [ ] If arxiv: choose primary category (cs.DS or math.NA) +
      secondary (cs.LG)

## Target venue

**Primary: arXiv preprint.** Recommended categories:
- Primary: `cs.DS` (data structures and algorithms) or `math.NA`
  (numerical analysis) — choice depends on framing emphasis
- Secondary: `cs.LG` (machine learning) given primitive (a) overlaps
  the RetNet/Mamba-SSD lineage

**Alternative: SIAM Journal on Scientific Computing — Software section.**
This is the natural fit for a "verified implementation + benchmark +
prior art" tool paper of this style. The amsart class compiles cleanly;
final-format conversion to SIAM's `siamart220329` template would be
required for acceptance.

Word count well under either venue's typical limit (~3,000 words
excluding refs vs typical 5,000-10,000-word limit).

## Citation key map (for future cross-referencing)

| Bib key | Reference |
|---|---|
| `SunRetNet2023` | RetNet: Retentive Network for LLMs, arXiv:2307.08621 |
| `DaoGuSSD2024` | Mamba-2 / SSD, arXiv:2405.21060 |
| `QinLightningAttention2024` | Lightning Attention-2, arXiv:2401.04658 |
| `CrowdyMarshall2007` | Schottky–Klein prime function (Comput. Methods Funct. Theory 7) |
| `Schrodinger1914` | Original 1D harmonic-chain Bessel propagator (Ann. Phys. 349) |
| `Trovato2016` | Periodic harmonic-chain extension, arXiv:1608.00616 |
| `DLMF` | NIST Digital Library of Mathematical Functions, §9.6 |
| `MeraBoitoSumino2018` | Hypergeometric resummation, arXiv:1802.06034 |
| `BorweinBorweinTaylor1985` | Madelung convergence theory (J. Math. Phys. 26) |
| `CrandallBuhler1987` | Madelung Ewald expansions (J. Phys. A 20) |
| `ProjectC` | This repository (verification audits, source code, CSVs) |

## Provenance

This tool paper packages five computational primitives that were
implemented and verified during a private software-research project
(`ramanujan-mining` repository). Each primitive was independently
re-implemented and benchmarked by adversarial verification subagents
distinct from the proposing agent — a methodological safeguard against
silent-error propagation in the underlying claims.

The full audit trail:

- **Primitive (a) finite-pole attention** — verified in diary entry 59;
  source `rkc/attention/finite_pole.py`; tests
  `rkc/tests/test_accelerators.py`.
- **Primitive (b) annular Green function** — verified in diary entry 60;
  source `rkc/pde/annular_green.py`; tests in
  `rkc/tests/test_accelerators.py`.
- **Primitive (c) Bessel-image PH propagator** — verified in diary
  entry 53 (initial result) and re-audited in diary entry 63;
  source `rkc/ph/bessel_image_propagator.py`; tests in
  `rkc/tests/test_accelerators.py`.
- **Primitive (d) Airy Tricomi-U** — verified in diary entry 65;
  source `rkc/special/airy_resurgent.py`; tests in
  `rkc/tests/test_accelerators.py`.
- **Primitive (e) CsCl Madelung 42-shell** — verified in standalone
  script `analysis/37_cscl_madelung_42_shell_verification.py`;
  per-cell numerical output in `analysis/results/`.

All numerical work is reproducible from the public commit history.
The full per-primitive CSVs are under
`analysis/results/{37,...}_*.csv`, and all `rkc` accelerators ship
with the package documented in `rkc/README.md`.

### Honest framing

This is a **verified-implementation tool paper**, not a novel-math
paper:

- (a) is a multi-pole extension of RetNet/Mamba-SSD — explicit
  attribution to Sun et al. 2023 and Dao–Gu 2024.
- (b) is the thin-annulus packaging of Crowdy–Marshall θ-quotient
  Green functions — explicit attribution to Crowdy–Marshall 2007.
- (c) is Schrödinger's 1914 chain extended via standard image-method
  periodicity — explicit attribution to Schrödinger 1914 and
  Trovato 2016.
- (d) re-derives a DLMF-adjacent representation with specific
  (1/6, 1/3) parameters that appear less documented in canonical
  references — small packaging contribution possible.
- (e) re-packages classical Ewald/Poisson machinery (Borwein–Borwein–
  Taylor 1985; Crandall–Buhler 1987) with a specific three-shell
  weighting — packaging contribution.

The cross-domain pattern — applying a curated operator basis from one
domain to find fast representations in adjacent domains — is the
methodological contribution. The math is mostly classical or recently
published.
