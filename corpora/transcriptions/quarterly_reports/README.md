# `quarterly_reports/` — Hunt 5 transcription target

Pre-wired landing zone for the Berndt 1984 typeset edition of Ramanujan's
three **Quarterly Reports** to the University of Madras Board of Studies
(1913–1914). Per `insights/HUNT_MAP.md §5`, this is the **highest-leverage
single arriving source** of the run — it is the closest existing evidence
of *how* Ramanujan worked through a problem (intermediate steps, not just
final statements), and is the ground truth for the latent-vocabulary
conjecture.

Source (per `manifest/sources_letters_papers_qr.md §C`):

| Field | Value |
|---|---|
| Primary editor | Bruce C. Berndt |
| Citation | "Ramanujan's Quarterly Reports", Bull. London Math. Soc. **16** (1984), 449-489 |
| Open-access PDF | https://hal.science/hal-03912911/document |
| Originals (lost) | Three reports by Ramanujan, March 1913 – early 1914 |
| Surviving witness | 1925 handwritten copy by T. A. Satagopan (U. Madras / Madras Math. Library); **not digitised** |
| Berndt's expansion | Chapter in *Ramanujan's Notebooks, Part I* (Springer 1985) |

When the PDF arrives, drop it as `../scans/QR_berndt_1984_blms.pdf`
(>1MB, so gitignored locally).

## Expected file naming

Transcriptions go in this directory under the strict pattern:

```
qr<N>_section_<M>.tex
```

where `<N>` ∈ {1, 2, 3} is the Quarterly Report number and `<M>` is the
section as Berndt numbers it. Examples (Berndt 1984's section structure,
per the table of contents in HAL hal-03912911):

```
qr1_section_1.tex      # QR I, §1 — Master Theorem statement + integrals
qr1_section_2.tex      # QR I, §2 — Mellin-style examples
qr1_section_3.tex      # QR I, §3 — gamma/beta function derivations
qr1_section_4.tex      # QR I, §4 — applications to definite integrals
qr2_section_1.tex      # QR II, §1 — extensions of the Master Theorem
qr2_section_2.tex      # QR II, §2 — calculus of zeta values
qr2_section_3.tex      # QR II, §3 — definite-integral evaluations
qr2_section_4.tex      # QR II, §4 — connection with q-series
qr3_section_1.tex      # QR III, §1 — further integral evaluations
qr3_section_2.tex      # QR III, §2 — connection with theta / modular
qr3_section_3.tex      # QR III, §3 — concluding examples
```

If Berndt's actual section count differs, follow Berndt's numbering
literally; agents will discover it by `ls` rather than by hardcoded
expectation. Names match `^qr[123]_section_\d+\.tex$`.

Sub-divide a section into multiple files only if it exceeds ~10kB of
transcription. Suggested suffix: `_partA.tex`, `_partB.tex`.

## Required transcription headers

See `../README.md` for the format spec. Every QR transcription must carry
a `% Provenance` block whose `source_file` is
`../../scans/QR_berndt_1984_blms.pdf` (or the actual filename the user
chose), and whose `source_pages` field cites the BLMS page range.

## Expected per-section structure

Each section file should preserve, in order:

1. `\section*{Quarterly Report <N>, §<M> — <Berndt's title>}` heading.
2. Berndt's English commentary preamble (1-2 paragraphs), as LaTeX text.
3. The Ramanujan content — every theorem, equation, and worked example
   Berndt reproduces — verbatim. Each labelled formula must carry a
   `\label{qr<N>:sec<M>:eq<seq>}` so downstream scripts can cite it.
4. Berndt's per-result commentary inline as LaTeX `\textbf{Remark}`
   blocks or `% Berndt-comment:` lines.

A skeleton template lives in `../README.md`. Copy-paste, fill in.

## Operator-tagging workflow (Hunt 5 core deliverable)

Once a section file lands:

```
$ python3 -c "
from ramanujan.corpora.transcriptions.operator_tagging_schema import tag, flagged
text = open('ramanujan/corpora/transcriptions/quarterly_reports/qr1_section_1.tex').read()
print('confidences:', tag(text))
print('flagged operators:', flagged(text))
"
```

For each labelled identity block in the section, run the schema and
record:

- the LaTeX `\label{...}` key,
- the per-operator confidence vector (six floats ∈ [0,1]),
- the flagged operators (those above each operator's `flag_threshold`).

Aggregate over the whole corpus into a single CSV
(`analysis/results/qr_operator_tags.csv` — to be created when the
transcriptions arrive) and check the HUNT_MAP §5 prediction:

> "5-10 operators recur 80%+ of the time"

The prediction is **confirmed** if ≥80% of labelled identities are
flagged by at least one of the six operators in the schema. If the
prediction fails, the failure modes themselves are informative —
either (a) some labelled identities use no operator in our basis
(suggests the basis is incomplete; what's the missing 7th?), or (b)
several identities cross-flag many operators (suggests the operators
are not the right granularity).

Either outcome is publishable per the latent-space-speedrun hypothesis
in `insights/CANDIDATE_INSIGHTS.md §D`.

## What "verified against transcription" means

Each `Operator` in `../operator_tagging_schema.py` carries a flag
`verified_against_transcription`. They are all currently `False` because
the schema's example manipulations are training-memory recall of textbook
forms. **As soon as a Berndt section is transcribed and the operator's
example is matched against a real Ramanujan manipulation, update the
flag and add a `notes` line citing the specific
`qr<N>:sec<M>:eq<seq>` label.**

Do not silently change the example string itself — instead, add a new
`example_from_qr` field on the Operator if the verified version differs
materially. The original training-memory example stays as a reference
point so the regression history is preserved.
