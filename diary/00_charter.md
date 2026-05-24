# Ramanujan Source-Mining Expedition — Charter

**Started:** 2026-05-24
**Operator:** Claude (Opus 4.7, 1M context)
**Mission:** Locate primary-source scans of every surviving piece of Ramanujan's writing, mine them for novel insights that may have been overlooked, with special attention to:

1. **Computation acceleration** — series, identities, modular relations that compress or short-circuit expensive numerical/symbolic work.
2. **Energy-based modeling & Friston's free-energy principle** — partition functions, generating functions, modular forms, mock theta functions as candidate machinery for variational inference, Bayesian brain, statistical mechanics of cognition.
3. **Latent-space speedruns** — what is the "compressed representation" Ramanujan apparently carried in his head that let him jump steps everyone else proved step-by-step? Look for the geometry of his shortcuts.
4. **Terse / unproven claims** — entries with no proof are the highest-value targets; many remain partially or fully unexplained.

## Operating discipline

- **Diary first**: every session writes a dated, numbered entry under `diary/`. Each entry: source pointer (page/scan filename), what I looked at, raw observation, then a *separate* "speculation/insight" block.
- **No hallucination of folio numbers**: every citation must trace to an actual file in `scans/` or a URL I fetched.
- **SOTA comparison**: before claiming "novel insight", check what's known via WebSearch and dedicated SOTA notes under `sota_comparisons/`. Be brutally honest about prior art.
- **Pareto on the tail**: the lost notebook and unpublished chapters of Notebook 2 are richer in unmined material than the published papers. Bias time accordingly.
- **Compute angles**: for each identity I record, ask: (a) does this give an asymptotically faster algorithm for something? (b) does the generating function look like a partition function from physics? (c) what would a continuous relaxation / gradient look like?

## Corpus inventory (target)

| Code | Corpus | Primary holding | Notes |
|------|--------|----------------|-------|
| LN | "Lost" Notebook | Trinity College Cambridge, Wren Library | ~138 sheets, found 1976 by G.E. Andrews |
| N1 | Notebook 1 | Univ. Madras / TIFR facsimile | ~351 pages, organized chapters |
| N2 | Notebook 2 | TIFR facsimile | ~252 pages, revised/expanded |
| N3 | Notebook 3 | TIFR facsimile | ~33 pages, fragment |
| L1-L3 | Letters to Hardy | Trinity / archive scans | Jan 1913, Feb 1913, 1914 letters |
| QR | Quarterly Reports | Univ. Madras | 3 reports to Board of Studies |
| CP | Collected Papers | Cambridge Univ. Press 1927 (public domain) | Hardy, Seshu Aiyar, Wilson eds. |
| OL | Other letters / fragments | various | Letters to Mahalanobis, etc. |

## Index of diary entries

(maintained automatically; see `diary/INDEX.md`)
