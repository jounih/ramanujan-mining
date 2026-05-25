# corpora/text/ — pdftotext extracts of downloaded-pdfs/

**Generated:** 2026-05-25 via `pdftotext -layout` on every file in
`downloaded-pdfs/`. ~143k lines across 14 files.

## Purpose

Foundation for the **literature-diff** layer of the verification workflow.
When ChatGPT-Pro claims a result is novel, we grep this corpus first
(cheap, in-repo, ~2s per query) before relying on WebFetch.

## Search

```bash
# Files containing all terms (default = AND)
python corpora/scripts/lit_search.py "Lambert" "annihilator"

# Files containing any term (OR)
python corpora/scripts/lit_search.py --any "Tricomi" "Kummer"

# Regex (raw — use anchors freely)
python corpora/scripts/lit_search.py --regex 'Entry\s*4\.2\.\d'

# File-list-only (skip snippets)
python corpora/scripts/lit_search.py --files-only "Hickerson"
```

## Per-file inventory

| File (.txt) | Lines | Source | Coverage |
|---|---|---|---|
| `Ramanujan_39_s_Lost_Notebook_Part_I_2005.txt` | 25,057 | AB LN Part I (Springer 2005) | q-series + theta + class invariants |
| `Ramanujan_39_s_Lost_Notebook_Part_II_2008.txt` | 25,775 | AB LN Part II (Springer 2008) | mock theta + partitions |
| `Ramanujan_39_s_Lost_Notebook_Part_III_2012.txt` | 24,379 | AB LN Part III (Springer 2012) | Eisenstein + modular eqns |
| `Ramanujan_39_s_Lost_Notebook_Part_IV_2013.txt` | 24,941 | AB LN Part IV (Springer 2013) | gamma function + 1729 |
| `ramanujan-notebooks-v.txt` | **0** | Berndt NB Part V (scanned) | **EMPTY** — facsimile, needs OCR (Chandra/Mathpix) |
| `ramanujankitap1.txt` | 17,228 | Berndt NB Part I | base Notebooks chapters |
| `pli.kerala.rare.28155.txt` | 13,871 | Ramanujan: Letters and Commentary (1995) | letters to Hardy |
| `KSRchap3.txt` | 764 | KSR chap 3 (likely supplementary) | small |
| `berndt_chan_zhang_1997_class_invariants_kronecker_modular_eqns_TAMS_349.txt` | 3,390 | Berndt-Chan-Zhang TAMS 1997 | class invariants |
| `hal-03912911.txt` | 2,860 | HAL preprint (Berndt-Dixit αβ=1?) | Mellin pair |
| `0904.1053v2.txt` | 631 | arxiv 0904.1053 (Ono?) | K3 / 1729 |
| `00000382.txt` | 2,532 | unknown — historical paper | misc |
| `1274-16.txt` | 783 | unknown — likely article | misc |
| `openai_2026_unit_distance_erdos_remarks.txt` | 1,003 | OpenAI Erdős 2026 | the Erdős CoT we're modeling on |

## Gaps to be aware of

- **`ramanujan-notebooks-v.txt` is empty** because `pdftotext` can't extract
  text from scanned page images. To search Berndt NB V, use the page
  images at `chatgpt-pro-mining/.../primary_originals/page_images/` +
  Chandra OCR (`corpora/scripts/chandra_api_runner.py`).
- **No Cooper *Theta Functions*** (still owed).
- **No Berndt NB Parts II/III/IV** (only Part V scanned facsimile + Part I).
- **No copyrighted vol of Andrews-Berndt that hasn't shipped to us** (we
  have all 4 LN parts; AB *Continued Fractions* etc. not in pack).

## Updating

Re-run the extraction if PDFs change:

```bash
for f in downloaded-pdfs/*.pdf; do
  base=$(basename "$f" .pdf)
  out="corpora/text/${base}.txt"
  pdftotext -layout "$f" "$out"
done
```

The text extracts are committed (text only, total ~5 MB) so any future
session can grep them without re-extracting.
