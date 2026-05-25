# Level-pq Lambert annihilator expository note — LaTeX source

This directory contains the LaTeX source for a short expository note on
the unique (up to scale) linear relation among the four Lambert
"conjugate-pair blocks" $T_d(\alpha,\beta)$ indexed by $d \mid pq$, at
squarefree composite level $N = pq$. The main result is an explicit
closed-form coefficient vector $(-\delta, m, -m, \delta)$ in terms of
$g := \gcd(pq-1, q-p)$, $\delta := (q-p)/g$, $m := (pq-1)/g$, derived
from the 1916 Hardy-Ramanujan-Berndt identity plus five lines of
Gaussian elimination, and identified post-hoc with the classical
dimension formula $\dim E_2(\Gamma_0(pq)) = 3$.

The companion markdown draft is at
[`../2026-05_level_pq_lambert_annihilator_expository.md`](../2026-05_level_pq_lambert_annihilator_expository.md).
This LaTeX version is the submission-ready format with AMS class +
bibtex bibliography, targeting Math. Mag. style.

## Files

- `main.tex` — the paper source, ~2,200 words typeset, six sections
  plus abstract
- `refs.bib` — bibliography (11 entries: Hardy-Ramanujan 1916,
  Berndt NB Parts I & II, Andrews-Berndt Lost Notebook, Diamond-Shurman,
  Stein, LMFDB, Berndt-Yee, Berndt-Dixit, Project C repo, ChatGPT-Pro
  interface)

## Compile

If `pdflatex` + `bibtex` are installed:

```bash
cd papers/level_pq_lambert_annihilator_expository
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

- [ ] Compile `main.tex` locally; verify all citations resolve and the
  bibliography typesets cleanly under `amsplain`
- [ ] Verify the 16-row verification table in §4 typesets on a single
  page (uses `booktabs`); reduce `\tabcolsep` further or shrink to
  `\footnotesize` if it overflows
- [ ] Verify all `\cref` / `\eqref` references resolve (no `??` markers)
- [ ] Check word count against target venue's short-comm limit
  (Math. Mag. ~3,500 words; we are well under)
- [ ] Final proof-read for clarity of the §6 provenance language —
  this is the "honest novelty framing" section and is the political
  heart of the paper
- [ ] Update commit hash in `refs.bib` (`ProjectC` entry) if further
  changes are made to `analysis/30_*.py` or `analysis/32_*.py` after
  the current `bf5aacf` reference
- [ ] If targeting Math. Mag. specifically, double-check their
  current submission guidelines for any author-information macros
  (e.g., `\address`, `\email`) they prefer to suppress

## Target venue

Primary: **Mathematics Magazine** (Math. Mag.) — Mathematical
Association of America. Short-communication / expository note. Their
style guide explicitly favours `amsart` with `\bibliographystyle{amsplain}`
(full author names, not abbreviated initials), numbered sections, and
accessible prose with worked examples rather than dense theorem-proof
chains. This paper is built to that style.

Alternative venues if Math. Mag. declines or the topic feels too
modular-forms-heavy:

- **The American Mathematical Monthly** (Amer. Math. Monthly) — also
  MAA; broader audience; word limit ~5,000. Same `amsart` /
  `amsplain` style.
- **The College Mathematics Journal** (Coll. Math. J.) — MAA;
  undergraduate audience; would require softening §3 and §5.
- **Hardy-Ramanujan Journal** (open access, hrj.episciences.org) —
  niche-appropriate; would convert the §6 provenance angle into a
  longer methodological discussion.

Word count well under any of these limits (~2,200 words typeset,
~2,500 including refs).

## Citation key map (for future cross-referencing)

- `HardyRamanujan1916` — Hardy & Ramanujan, *Asymptotic formulae in
  combinatory analysis*, Proc. London Math. Soc. (2) **17** (1918)
  75-115 (submitted 1916). Source of the base Lambert/$E_2$ identity
  (1.55).
- `BerndtNB1` — Berndt, *Ramanujan's Notebooks, Part I* (1985).
  Cited for context.
- `BerndtNB2` — Berndt, *Ramanujan's Notebooks, Part II* (1989).
  Ch. 14, Entries 26-27 cover the H-R-B Lambert/$E_2$ identity.
- `AndrewsBerndt` — Andrews & Berndt, *Ramanujan's Lost Notebook,
  Parts I-IV* (2005-2013). Cited in the literature-diff list in §6.
- `DiamondShurman` — Diamond & Shurman, *A First Course in Modular
  Forms* (2005). §3.5, §3.9, §5.6 for the Eisenstein-subspace
  dimension formula and old-form construction.
- `Stein` — Stein, *Modular Forms, A Computational Approach* (2007).
  Ch. 5 for the Eisenstein subspace at squarefree level.
- `LMFDB` — L-functions and Modular Forms Database. Used to confirm
  $\dim E_2(\Gamma_0(33)) = 3$.
- `BerndtYee` — Berndt & Yee, *A page on Eisenstein series in
  Ramanujan's lost notebook*, RIMS Kokyuroku **1274** (2002).
  Cited in the literature-diff list.
- `BerndtDixit` — Berndt & Dixit, *A transformation formula...*
  (2010; arXiv:0904.1053). Cited in the literature-diff list.
- `ProjectC` — the GitHub repository where the engine code, diary,
  and verification scripts live. Currently points at commit
  `bf5aacf` (diary 58 + analysis/30 + analysis/32).
- `ChatGPTPro` — OpenAI's frontier-model interface, used May 2026
  as a sounding board during the run.

## Provenance

The formula in this note was produced by Project C, an LLM-driven
symbolic-search engine in the `ramanujan-mining` private repository,
in late May 2026. The engine surfaced the Level-$33$ instance from
the Hardy-Ramanujan-Berndt seed identity using only its base operator
basis (`mellin_inversion`, `master_theorem`,
`modular_transform_with_correction`, and others) plus an `mpmath`
cost model with a strict $\le 10^{-30}$ relative-error gate. A
follow-up prompted-exploration cycle enumerated the additional seven
instances $\{35, 51, 65, 77, 87, 95, 115\}$ and the closed-form
$\gcd(pq-1, q-p)$ pattern was hand-extracted from the resulting
coefficient table.

Adversarial verification was then performed:

- Independent reimplementation of the formula and the H-R-B identity.
- Sweep across 16 instances at `mpmath` working precision 200 digits,
  evaluating at five test cells on $\alpha\beta = \pi^2$ each.
- Structural-extension audit (3-prime, $p^2$, $p^2 q$) confirming
  uniqueness is special to $N = pq$.
- Literature diff across six volumes of Berndt's commentary plus
  LMFDB, OEIS, and ~12 arXiv / AMS targeted searches; the explicit
  $\gcd$ parameterization was not located in the surveyed sources.
- Identification of the post-hoc structural reason
  ($\dim E_2(\Gamma_0(pq)) = 3$) by the verification subagent.

The full audit trail:

- `/Users/jouni/Documents/ramanujan-mining/diary/55_infinite_family_e2_lambert_annihilators_squarefree_composite_levels.md`
  (original engine claim)
- `/Users/jouni/Documents/ramanujan-mining/diary/58_level_pq_family_adversarial_verification.md`
  (adversarial verification and literature audit)
- `/Users/jouni/Documents/ramanujan-mining/analysis/30_level33_lambert_e2_annihilator_verification.py`
  (Level-33 numerics)
- `/Users/jouni/Documents/ramanujan-mining/analysis/32_level_pq_family_adversarial_verification.py`
  (16-instance family verification)
- commit `bf5aacfd` or later on `main`

The §6 provenance section in the paper is intentionally honest about
the engine's role: the *structure* is classical, the *explicit
parameterization in `gcd(pq-1, q-p)` form* may be novel-as-form, and
the *autonomous-rediscovery angle* is what makes the note suitable
for an expository venue rather than a research one.
