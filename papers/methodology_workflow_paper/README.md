# Methodology workflow paper — LaTeX source

This directory contains the LaTeX source for a methodology paper
documenting the four-component workflow developed during a 30-cycle
private research run (Ramanujan-mining, May 2026) for filtering
LLM-proposed mathematical results: Erdős-style prompts, machinery
loading, adversarial verification subagents, and diary discipline.

The companion markdown draft is at
[`../2026-05_methodology_workflow_paper.md`](../2026-05_methodology_workflow_paper.md).
This LaTeX version is the submission-ready format with AMS class +
bibtex bibliography.

## Files

- `main.tex` — the paper source, ~3,000 words typeset (9 sections +
  acknowledgments)
- `refs.bib` — bibliography (5 entries: Project C repo, OpenAI Erdős
  demonstration, AB 2013, Berndt NB I-V, Caux-Konno-Sorrell-Weston 2012)

## Compile

If `pdflatex` + `bibtex` are installed:

```bash
cd papers/methodology_workflow_paper
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
- [ ] Verify both tables (§3 taxonomy, §4 honest cycles) typeset
  cleanly without overflow
- [ ] Verify the \cref / \crefrange references all work across all 9
  numbered sections
- [ ] Verify the verbatim code block in §2.1 (prompt template
  skeleton) renders without line-overflow
- [ ] Pick arxiv categories: primary `cs.AI` or `math.HO`, secondary
  `cs.LG` (see "Target venue" below)
- [ ] Confirm `https://github.com/jounih/ramanujan-mining` is public
  and contains the cited diary entries (55-60) before posting
- [ ] If submitting to a workshop venue, convert from `amsart` to the
  workshop style file (typically NeurIPS / ICML `.sty` package);
  conversion is largely mechanical because no theorem environments
  are actually used in the body
- [ ] Final proof-read for the candid §5 / §6 / §8 framing — the
  paper's primary contribution is the honest accounting of what
  LLMs do and do not contribute; do not soften on copy-edit

## Target venue

Primary: **arxiv preprint**.
- Primary category: `cs.AI` (LLM-assisted research methodology) or
  `math.HO` (history / overview of mathematics)
- Secondary: `cs.LG` (machine learning, since the verification gate
  is itself an LLM agent loop)

Alternative: **AI-for-mathematics workshop track** at a major ML
venue. Strong candidates:
- NeurIPS 2026 AI-for-Math workshop
- ICML 2026 AI-for-Science workshop
- ICLR 2027 AI-for-Mathematics workshop (if accepted)

The `amsart` class compiles cleanly to arxiv standards. Conversion to
NeurIPS `neurips_2026.sty` or ICML `icml2026.sty` is mechanical: drop
amsart preamble, swap `\title`/`\author`/`\maketitle` block, retain
bibtex. No theorem environments are actively used in this
methodology paper (they are pre-declared in main.tex for safety but
not invoked in the body), so workshop-style conversion is low-risk.

## Citation key map (for future cross-referencing)

- `ProjectC` — Helminen, *ramanujan-mining* GitHub repository (2026);
  the public artifact containing prompt templates, diary entries,
  per-cell CSVs, and the methodology source
- `OpenAIErdos2026` — OpenAI's `ChatGPT-o3` Erdős unit-distance
  combinatorics demonstration; the design inspiration for the
  open T/F prompt template (§2.1); local archival copy lives in
  the project repo at
  `downloaded-pdfs/openai_2026_unit_distance_erdos_remarks.pdf`
- `AB2013` — Andrews & Berndt, *Ramanujan's Lost Notebook, Part IV*
  (Springer 2013); the source corpus that yielded the Entry 4.2.3
  corrigendum case study referenced in §3
- `BerndtNB` — Berndt, *Ramanujan's Notebooks, Parts I-V* (Springer
  1985-2005); five-volume series; the broader source corpus
  underlying the toolkit-split / operator-basis machinery loading
  in §2.2
- `CauxKonnoSorrellWeston2012` — Caux-Konno-Sorrell-Weston,
  *J. Stat. Mech.* 2012 P01007; the structural-obstruction
  reference for the XXZ chain calibrated-honest cycle in §4

## Provenance

This methodology paper documents the workflow that produced the AB
4.2.3 corrigendum (separate paper at
`../ab_entry_423_corrigendum/main.tex`), the level-pq Lambert
annihilator expository note (separate draft at
`../2026-05_level_pq_lambert_annihilator_expository.md`), and the
computational primitives tool paper (separate directory at
`../computational_primitives_tool_paper/`).

The cycle counts and category breakdowns reported in §3 and §4 are
based on the diary entries 31-60 in the project repo. The 30-cycle
window is May 2026; the count of ~30 is approximate because some
diary entries record multi-prompt cycles and the boundaries between
"substantive cycle" and "minor follow-up" are judgment calls.

The 75% adversarial-subagent downgrade rate quoted in §6 (b) is
based on 3 downgrades out of 4 adversarial verification subagent
runs (diaries 57, 58, 59, 60). This is a small sample; we report it
honestly as a methodological observation rather than as a calibrated
statistical claim.

The "did not pan out" log referenced in §2.4 and §8 lives at
`insights/DID_NOT_PAN_OUT.md` in the project repo.

This paper does not introduce any new mathematical claims of its
own; it documents the workflow that produced separately-submitted
mathematical claims. Submission of this methodology paper is
independent of the submission status of the corrigendum or the tool
paper, but cross-references to those papers are expected to be
added once each lands at its venue.
