# Project C first-results short note — LaTeX source

This directory contains the LaTeX source for a short note describing
Project C, an automated symbolic-search engine, and its first two
acceptances on recorded Ramanujan identities (Warnaar 1.7 at a=1 on
Lost Notebook p. 29, and Andrews-Berndt Entry 1.6.6 on Lost Notebook
p. 35).

The companion markdown draft is at
[`../2026-05_project_c_first_results_short_note.md`](../2026-05_project_c_first_results_short_note.md).
This LaTeX version is the submission-ready format with AMS class +
bibtex bibliography. Numeric verification figures throughout the
LaTeX source are the **independently-reproduced** measurements from
diary 43 (commit `f8a04a3`), not the original ChatGPT-Pro claims
from diary 42. Where the original markdown still carried
`[VERIFY_REPLACE]` markers in the abstract, §1.4, §2.3, §7.1, and
§7.2, those have been replaced in the LaTeX with the diary-43
numbers (see Provenance section below). The §3.4 and §4.3 tables
were already updated in the markdown source.

## Files

- `main.tex` — the paper source, ~4,400 words typeset
- `refs.bib` — bibliography (18 entries: Project C repo + the standard
  Ramanujan / Berndt / Warnaar / Andrews-Berndt / Zwegers / Hickerson
  / Garvan-Frye / Berndt-Bhargava / Berndt-Yee / Berndt-Dixit / Ono
  literature)

## Compile

If `pdflatex` + `bibtex` are installed:

```bash
cd papers/project_c_first_results_short_note
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

- [ ] Compile main.tex locally; verify all citations resolve and the
  bibliography prints (`amsalpha` style; expect a few dozen-mark
  entries since most cited diaries are repo-internal under @misc)
- [ ] Verify the four numerical-results tables (§3.4 and §4.3, two
  each) typeset correctly in the page width — booktabs + array
  packages are loaded; long rows may need landscape if a journal
  template enforces narrower text width
- [ ] Verify all `\cref` / `\Cref` references resolve (need two
  `pdflatex` passes after bibtex)
- [ ] Sanity-check the §3.2 and §A operator-trace verbatim blocks for
  font / wrapping (UTF-8 mathematical symbols were transliterated to
  ASCII for verbatim safety — e.g. `pi^2` not `π²`)
- [ ] Independent commit-hash insertion in the Acknowledgments if any
  further changes are made before submission (current refs.bib cites
  diary 43 / commit `f8a04a3`)
- [ ] Run a spelling-pass; the LaTeX inherits the markdown's prose
  style which has not been copy-edited beyond first-draft level
- [ ] Decide whether to split into (a) a Project-C / `rkc` software
  tool paper (cs.SC venue) and (b) a Ramanujan-identity-acceleration
  paper (math.NT / Ramanujan Journal venue), or submit as a single
  comprehensive arXiv note (see Target venue below)
- [ ] Validate the appendix code excerpt against the actual
  `rkc/search/basis.py` to make sure the function name and structure
  still match at the moment of submission

## Target venue

**Primary: arXiv preprint** — `math.NT` primary, `cs.SC` secondary
(see arXiv subject taxonomy). A single comprehensive note for the
first preprint is the recommended path; the v0.10 milestone (per §7.3)
could subsequently support either a longer companion paper to the
AB 4.2.3 corrigendum in the Ramanujan Journal, or a software paper for
e.g. SoftwareX, the Journal of Symbolic Computation, or JOSS.

**Alternative:** **Ramanujan Journal** (Springer) as a longer
companion to the AB 4.2.3 corrigendum. Springer's `springer-svjour3`
class is the required template if accepted. Both the corrigendum and
this short note touch the same `analysis/` infrastructure and could
form a thematic pair.

Length: ~4,400 words typeset. Comfortably within arXiv's no-limit
context; on the long side of Ramanujan Journal short-comm but still
within a regular-article limit (typical limit 8,000-10,000 words).

## Citation key map

| BibTeX key | What it cites |
|---|---|
| `ProjectC` | This run's GitHub repository + diary entries (covers all internal `diary/NN_*.md` references) |
| `AB2005` | Andrews-Berndt, *Lost Notebook Part I* (where AB Entry 1.6.6 lives — primary citation for §4) |
| `AB2009` | Andrews-Berndt, *Lost Notebook Part II* (reference completeness) |
| `AB2012` | Andrews-Berndt, *Lost Notebook Part III* (reference completeness) |
| `AB2013` | Andrews-Berndt, *Lost Notebook Part IV* (where AB Entry 4.2.3 lives; sibling corrigendum) |
| `BerndtNB1` | Berndt, *Ramanujan's Notebooks Part I* (NB Part 1 Ch. 3-4 cited in §6) |
| `BerndtNB5` | Berndt, *Ramanujan's Notebooks Part V* (NB V Ch. 32, 34, 36 cited in §6) |
| `BerndtDixit2009` | Berndt-Dixit arXiv 2009 (Mellin-pair transformation; cited in §5 obstruction principle) |
| `DixitBerndt1995` | Dixit-Berndt eds., *Ramanujan: Letters and Commentary* |
| `GarvanFrye` | Garvan-Frye theta-function-identities paper (the 13-identity Ramanujan sample in §1.1) |
| `BerndtBhargava2022` | Berndt-Bhargava 2022 HRJ (the Quarterly Reports reproduction; cited in §2.1) |
| `BerndtYee2002` | Berndt-Yee RIMS 2002 (Eisenstein series in LN; reference completeness) |
| `Hickerson1988` | Hickerson 1988 Inventiones (mock-theta conjectures; cited for completeness re: §7.3 op 1) |
| `Ono2015` | Ono arXiv 2015 (taxicabs/K3; reference completeness) |
| `LostNotebook` | The 1988 Narosa/Springer facsimile (LN pp. 29, 35 are the primary cites) |
| `Warnaar2003` | Warnaar's 2003 PLMS paper (the equation (1.7) of §3) |
| `Zwegers2002` | Zwegers PhD thesis (the $R_{a,b}$ erfc form cited in §7.3 op 1) |

## Provenance

This short note's verification was carried out across two phases.

**Phase A (diary 42, ChatGPT-Pro 7-8th Erdős cycle):** The two source
identities were assembled by ChatGPT-Pro from its knowledge of the
Ramanujan / Berndt commentary literature, and the claimed cost-ratio
numbers (272× / 62× / 15× for Warnaar; 9-34× / hundreds-to-thousands×
for AB 1.6.6) were measured in ChatGPT-Pro's environment.

**Phase B (diary 43, our local environment):** The script
`analysis/29_warnaar_17_ab_166_cost_verification.py` independently
re-implemented all 6 forms (3 Warnaar + 3 AB 1.6.6) at `mp.dps = 80`
in our Python 3.12.7 / mpmath 1.3 / .venv environment, ran 5-trial
medians, and cross-checked at $\beta = 0.1$ to relative error
$\le 6 \times 10^{-72}$ (i.e. 72 digits of agreement) before
benchmarking. All Phase-A claims were confirmed within a factor of
2× at every $\beta$ cell; one new finding was added (the
catastrophic-cancellation observation for AB 1.6.6 form D at
$\beta = 10^{-3}$, where the naive evaluator returns
$-9.76 \times 10^{96}$ for a true value of $+39.638$).

The full audit trail:
- `/Users/jouni/Documents/ramanujan-mining/diary/42_project_c_improves_ramanujan_warnaar_17_and_ab_166.md`
- `/Users/jouni/Documents/ramanujan-mining/diary/43_warnaar_17_ab_166_cost_verification.md`
- `/Users/jouni/Documents/ramanujan-mining/analysis/29_warnaar_17_ab_166_cost_verification.py`
- `/Users/jouni/Documents/ramanujan-mining/analysis/results/29_warnaar_17_ab_166_cost_verification.csv`
- relevant commits: `f8a04a3` (analysis/29 + diary 43); `1a413d4`
  (markdown §3.4 / §4.3 table updates with the diary-43 numbers)

The other diary entries cited from `ProjectC` cover, in order of
first appearance in the paper:

- diary 14b: v0.4 keystone Poisson (§2.4)
- diary 19, 35, 37: the three obstruction-principle instances (§5)
- diary 20: Hunt 5 QR-tagging closure (§2.1)
- diary 22, 24, 25, 36: Hunt 5b Notebook-tagging (§2.1)
- diary 26: v0.7 strict Poisson duals (§2.4)
- diary 31: v0.8b additive-correction API (§2.4)
- diary 32: v0.8c Stieltjes occupation-number (§2.4)
- diary 33: v0.9a Hardy-orders diagnostic (§2.4)
- diary 34: v0.9 in-session proposer
- diary 36: bipartite analytic finding (§6)
- diary 38: SectorClassifier proposal (§5.1, §6.1)
- diary 39: compression-metric pilot (§1.1, §7.4)
- diary 40-42: ChatGPT-Pro Erdős cycles (Acknowledgments)
- diary 41: P2 prompt bug detection (Acknowledgments)
- diary 42: original cost-claim source (§3.4, §4.3)
- diary 43: this paper's verification reproduction (§3.4, §4.3)

`CLAUDE.md gotcha 6` and `insights/CANDIDATE_INSIGHTS.md §D1` /
`insights/BIG_IDEAS_REVIEW.md §2c` are also cited under the unified
`ProjectC` key (see the bibliography note).
