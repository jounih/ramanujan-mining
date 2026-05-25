# AB Entry 4.2.3 corrigendum — LaTeX source

This directory contains the LaTeX source for a short corrigendum to
Andrews & Berndt's *Ramanujan's Lost Notebook, Part IV* (Springer 2013),
specifically section 4.4 (pp. 116-117) and the underlying argument in
Berndt 2004 (Proc. Amer. Math. Soc. 132:2983-2988).

The companion markdown draft is at
[`../2026-05_ab_entry_423_corrigendum.md`](../2026-05_ab_entry_423_corrigendum.md).
This LaTeX version is the submission-ready format with AMS class +
bibtex bibliography.

## Files

- `main.tex` — the paper source, ~2,400 words typeset
- `refs.bib` — bibliography (8 entries: AB 2013, Berndt 2004, Berndt
  NB Part I, Lost Notebook facsimile, Gorenflo-Kilbas-Mainardi-Rogosin,
  Gradshteyn-Ryzhik, Abramowitz-Stegun, Project C repo)

## Compile

If `pdflatex` + `bibtex` are installed:

```bash
cd papers/ab_entry_423_corrigendum
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

- [ ] Compile main.tex locally; verify all citations resolve
- [ ] Verify the table in §6 typesets correctly
- [ ] Verify the \cref / \crefrange references all work
- [ ] Bruce Berndt courtesy review (email with .pdf + cover note)
- [ ] Format conversion to Ramanujan Journal style if accepted as venue
  (Springer's `springer-svjour3` class — convert from amsart)
- [ ] Update commit hash in the Acknowledgments if any further changes
  are made before submission
- [ ] Final proof-read for word repetition (currently sectioning may
  cause "asymptotic" to appear too often near the §6 discussion)

## Target venue

Primary: **Ramanujan Journal** (Springer). Short-communication track.
Alternative: **Hardy-Ramanujan Journal** (open access, hrj.episciences.org).
Word count well under either journal's short-comm limit (~2,400 words
excluding refs vs typical ~5,000-word limit).

## Citation key map (for future cross-referencing)

- `AB2013` — Andrews & Berndt, *Lost Notebook Part IV* (2013)
- `Berndt2004` — Berndt, Proc. Amer. Math. Soc. 132 (2004) 2983-2988
  (where the original §4.4 argument first appeared)
- `BerndtNB1` — Berndt, *Ramanujan's Notebooks, Part I* (1985)
  (source of "Chapter 3 Entry 10" cited by AB)
- `LostNotebook` — original Narosa/Springer 1988 facsimile (p. 199)
- `GorenfloKilbasMainardiRogosin` — Mittag-Leffler reference for §5
- `GradshteynRyzhik` — formula 3.466.1 used in §4
- `AbramowitzStegun` — formula 6.147 = AB's (4.4.2)
- `ProjectC` — the GitHub repository where verification numbers live

## Provenance

This corrigendum's verification was carried out by an adversarial
verification subagent in May 2026. The subagent independently
implemented the identity, swept 223 parameter cells at mpmath dps=80,
verified the AB-test cell at dps=200 to 200+ digits, reconstructed
the Mittag-Leffler contour proof from scratch, and audited the
literature finding no published treatment of Entry 4.2.3 since the
2013 monograph.

The full audit trail:
- `/Users/jouni/Documents/ramanujan-mining/diary/57_ab_entry_423_adversarial_verification_results.md`
- `/Users/jouni/Documents/ramanujan-mining/analysis/31_ab_entry_423_adversarial_verification.py`
- `/Users/jouni/Documents/ramanujan-mining/analysis/results/31_ab_entry_423_verification.csv`
- commit `bd17551d975a777eb671530a7adbffbccb2a8e86` on `main` branch
