# `transcriptions/` — format spec for primary-source transcriptions

A transcription is a small, diffable LaTeX or unicode-text file that
faithfully reproduces a primary Ramanujan source for downstream
programmatic consumption (operator tagging, identity extraction, etc.).
Transcriptions are the durable representation; the raw PDFs under
`../scans/` are the provenance anchor.

## File format

- **Encoding:** UTF-8.
- **Extension:** `.tex` (preferred) or `.txt` (for pure-text manipulations
  where math markup is overkill).
- **Per-file content unit:** ONE coherent passage — a section, a folio
  page, or a single labelled identity. Not an entire chapter. The goal is
  small files so individual identities are easy to cite and diff.

## Required header

Every transcription begins with a `% Provenance` comment block of at
least the following form (LaTeX comment lines; plain `#` lines work for
`.txt`):

```latex
% Provenance:
%   source_file:   ../scans/QR_berndt_1984_blms.pdf
%   source_pages:  457-459
%   primary_ref:   Berndt 1984, BLMS 16:449-489, §3 ("Quarterly Report I")
%   transcriber:   <handle>          % who transcribed
%   transcribed:   YYYY-MM-DD
%   confidence:    high | medium | low   % subjective; "low" = check carefully
%   notes:         <free text; any ambiguities, illegible marks, etc.>
```

The `source_file` MUST resolve relative to the repo (so a downstream
script can chase the PDF). If the PDF is gitignored (>1MB), the path
still resolves locally for whoever has the file.

## Body conventions

- Verbatim where possible. If Ramanujan writes `(a; q)_\infty`, the
  transcription writes `(a; q)_\infty` — not the expanded product.
- Use LaTeX inline math (`$...$`) and display math (`\[...\]` or
  `equation` environments).
- Each labelled identity gets a LaTeX `\label{<key>}` so downstream
  scripts can refer to it. Suggested key shape:
  `<corpus>:<location>:<seq>` — e.g. `qr1:sec3:eq04`.
- Comments preserve Ramanujan's marginalia / hand-flags exactly.
- If an OCR pass produced the initial text, mark with a `% OCR-source`
  line and the model/tool used. Human cleanup MUST follow.

## Worked example (LaTeX skeleton)

```latex
% Provenance:
%   source_file:   ../scans/QR_berndt_1984_blms.pdf
%   source_pages:  457
%   primary_ref:   Berndt 1984, BLMS 16:449-489, §3 (Quarterly Report I, Theorem 1)
%   transcriber:   claude
%   transcribed:   2026-05-24
%   confidence:    high
%   notes:         Master Theorem statement as Berndt typesets it.
\documentclass[border=2pt]{standalone}
\usepackage{amsmath, amssymb}
\begin{document}

\textbf{Quarterly Report I, Theorem 1 (Master Theorem).}\label{qr1:sec1:thm1}
If $F(x) = \sum_{n \ge 0} \phi(n) (-x)^n / n!$ then
\[
  \int_0^\infty x^{s-1} F(x)\, dx \;=\; \Gamma(s)\, \phi(-s),
\]
provided the integral and the analytic continuation of $\phi$ make sense.

\textbf{Remark} (Ramanujan).  The proof rests on the formal interchange of
sum and integral; rigorous conditions were established later by Hardy.

\end{document}
```

## How transcriptions feed downstream tools

- The operator-tagging schema (`operator_tagging_schema.py`) accepts a
  LaTeX snippet (or any unicode string) and returns per-operator
  confidence ∈ [0,1] for each of the six abstract operators in
  HUNT_MAP §5. Run it over each `\label{...}` block to build the
  Hunt 5 evidence base.
- Other future tools (identity extractor, generating-function arithmetic
  detector) will consume the same `.tex` snippets. Keep the math
  semantic and the comments machine-readable.

## Sub-directories

- `quarterly_reports/` — the Hunt 5 target. Pre-wired file naming and
  section structure live in its own README.
- (future) `lost_notebook/`, `notebook_ii/`, etc. — add as new corpora
  arrive.

## Operator-tagging schema self-test

`operator_tagging_schema.py` is importable AND runs a built-in self-test
when executed as a script:

```
$ python3 ramanujan/corpora/transcriptions/operator_tagging_schema.py
```

The self-test exercises each operator on its embedded "example
manipulation" string and asserts that the operator's own `test()`
returns a confidence above the per-operator threshold for its own
example. This guards against silent regressions in the matcher
heuristics.
