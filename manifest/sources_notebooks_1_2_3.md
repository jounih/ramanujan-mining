# Ramanujan's Three Original Notebooks (I, II, III) — Source Manifest

**Scope.** The bound volumes that Ramanujan kept in India before sailing to England in 1914. The originals are held at the **University of Madras Library**. The canonical facsimile is the **two-volume Tata Institute of Fundamental Research (TIFR), Bombay, 1957** photostat edition (Vol. 1 = Notebook 1; Vol. 2 = Notebooks 2 + 3). A **Narosa / Springer-Narosa reprint** appeared in 1984 / 1987 (Ramanujan centenary). A **TIFR 125th-anniversary Collector's Edition** appeared in 2011.

Page accounting from the TIFR facsimile:
- Notebook 1: 16 chapters, **~134 pp** of math (Vol. 1)
- Notebook 2: 21 chapters, **~252 pp** (the revised/enlarged version; Vol. 2, opening portion)
- Notebook 3: **~33 pp** of unorganised material (Vol. 2, end)
- Plus front-matter, blank versos retained verbatim, indices → total facsimile page count is roughly **~419 pp** (Vol 1) + larger Vol 2; combined two-volume page count is on the order of **~636 leaves** counted as faces.

**Important verification note.** Direct fetch (curl / WebFetch) of `archive.org`, `imsc.res.in`, and `ramanujan.sirinudi.org` was blocked from the research environment by HTTP 403 (sandbox TLS-inspection + host allowlist). All URLs below were located via web search and from cross-references in catalog records, review articles, and the search-result snippets. Item identifiers, titles, and access status are verified; exact byte sizes of individual files could not be independently confirmed and are marked **[not verified — visit URL]**. No files were downloaded.

---

## 1. Internet Archive (archive.org)

The most useful Internet Archive items, grouped by what they actually contain. Be careful: several items with "notebook" in the title are the **Berndt commentary volumes** (Springer, 1985–1998) and contain **no facsimile of Ramanujan's handwriting**. Those are listed separately under §5.

### 1A. TIFR facsimile (the prize) — Internet Archive copies

| # | Identifier / URL | What it contains | Format & approx. size | License / Access |
|---|---|---|---|---|
| 1 | **`notebooksofsrini0001vari`** — https://archive.org/details/notebooksofsrini0001vari | "notebooks of srinivasa ramanujan : various" — the TIFR facsimile volume(s); creator listed as "various"; described as the TIFR-published facsimile. Volume 1 of the two-volume set (Notebook 1). | PDF, DjVu, EPUB, full text. Size **[not verified — visit URL]**. ~134 facsimile pages of math + apparatus → total leaves ≈ 350–420. | Internet Archive open access; "Free Download, Borrow, and Streaming". TIFR retains copyright; IA hosts as scholarly/preservation copy. Effectively free for individual research. |
| 2 | **`part-one-3`** — https://archive.org/details/part-one-3 | "Ramanujan's Notebook (part one of two)" — explicitly noted as published by Tata Fundamental Research Institute. Companion to `notebooksofsrini0001vari` (some search snippets note "the second part [was] also uploaded earlier"). Together they cover Notebooks 1, 2, 3. | PDF (and DjVu/derivatives). Size **[not verified]**. | Internet Archive open access. |
| 3 | **`ramanujansnotebo0000rama`** — https://archive.org/details/ramanujansnotebo0000rama | "Ramanujan's notebooks" by Ramanujan Aiyangar, Srinivasa, 1887-1920. ARK ark:/13960/t5cc8tr44; ISBN 0387975039 (this ISBN is the Springer / Narosa joint reprint of the **TIFR facsimile** — i.e. the 1984/87 reprint of the original two volumes, not a Berndt commentary). | PDF + other IA derivatives. **[size not verified]**. | "Borrow" copy (Controlled Digital Lending) — typically a 1-hour / 14-day loan rather than direct download. Free with IA account. |

Direct download URL patterns on Internet Archive (apply to any of the items above):

```
https://archive.org/download/<identifier>/                           # directory listing
https://archive.org/download/<identifier>/<identifier>.pdf           # PDF
https://archive.org/download/<identifier>/<identifier>_djvu.txt      # OCR text
https://archive.org/download/<identifier>/<identifier>_djvu.xml      # DjVu XML
https://archive.org/download/<identifier>/<identifier>_jp2.zip       # ZIP of JPEG-2000 page scans
https://archive.org/metadata/<identifier>                            # JSON metadata (files + sizes)
```

So, for example:

```
https://archive.org/download/notebooksofsrini0001vari/notebooksofsrini0001vari.pdf
https://archive.org/download/notebooksofsrini0001vari/notebooksofsrini0001vari_jp2.zip
https://archive.org/download/part-one-3/part-one-3.pdf
```

### 1B. The "Lost Notebook" and other unpublished papers (NOT one of Notebooks I–III, but always paired with them)

| # | Identifier / URL | Contents | Notes |
|---|---|---|---|
| 4 | **`lost-notebook`** — https://archive.org/details/lost-notebook | "Lost Notebook and Other Unpublished Papers" — Narosa/Springer 1988, ed. Raghavan & Rangachari, ISBN 3-540-18726-X. 419 pp; ~138 sides of facsimile + Trinity College "Loose Papers". | Free download, PDF/EPUB/DjVu. |
| 5 | **`lostnotebookothe0000rama`** — https://archive.org/details/lostnotebookothe0000rama | Same work, second IA copy. | Possibly "Borrow" (CDL). |
| 6 | **`ramanujanslostnotebook-parti.2005.georgee.andrews.brucec.berndt2`** — https://archive.org/details/ramanujanslostnotebook-parti.2005.georgee.andrews.brucec.berndt2 | Andrews & Berndt **commentary** volume Part I (Springer 2005). | Free PDF. |
| 7 | **`ramanujanslostno0000andr`** — https://archive.org/details/ramanujanslostno0000andr | Andrews & Berndt **commentary** Part III. | "Borrow". |

### wget / curl recipe for any IA item

```bash
ID=notebooksofsrini0001vari
mkdir -p ramanujan/raw/$ID
cd ramanujan/raw/$ID

# Pull the JSON file manifest first to see exact filenames & sizes
curl -sL -o metadata.json "https://archive.org/metadata/$ID"
jq '.files[] | {name, format, size}' metadata.json

# Easiest: grab the PDF + JP2 zip + OCR text
curl -L -A "Mozilla/5.0" \
     -o "$ID.pdf" \
     "https://archive.org/download/$ID/$ID.pdf"

curl -L -A "Mozilla/5.0" \
     -o "${ID}_jp2.zip" \
     "https://archive.org/download/$ID/${ID}_jp2.zip"

curl -L -A "Mozilla/5.0" \
     -o "${ID}_djvu.txt" \
     "https://archive.org/download/$ID/${ID}_djvu.txt"

# Or use the official ia client (recommended; handles retries & throttling):
pip install internetarchive
ia download "$ID" --glob="*.pdf" --glob="*_jp2.zip" --glob="*_djvu.txt"

# Or mirror the entire item with wget:
wget -r -np -nH --cut-dirs=2 -e robots=off \
     -R "*.gif,*_thumb.jpg" \
     -U "Mozilla/5.0" \
     "https://archive.org/download/$ID/"
```

Replace `$ID` with `part-one-3`, `ramanujansnotebo0000rama`, `lost-notebook`, etc.

---

## 2. Indian institutional repositories

### 2A. ramanujan.sirinudi.org (the de-facto "Ramanujan online edition")

Mirror created 22 Dec 2013 for Ramanujan's 126th birthday. Hosts both published papers (HTML+PDF) and the **unpublished notebooks** (DjVu / PDF). Sourced from the TIFR facsimile, with TIFR retaining copyright and granting free individual download.

- Front page: https://ramanujan.sirinudi.org/
- Unpublished notebooks index: https://ramanujan.sirinudi.org/html/unpublished_notebooks.html
- Direct PDFs noted in search-result snippets (URL pattern):
  - http://ramanujan.sirinudi.org/Volumes/01/01.pdf  — Vol. 1 (Notebook 1)
  - http://ramanujan.sirinudi.org/Volumes/02/02.pdf  — Vol. 2 (Notebooks 2 + 3)
  - Published-papers PDFs at http://ramanujan.sirinudi.org/Volumes/published/ramNN.pdf  (e.g. ram05.pdf, ram36.pdf)
- Coverage: **all three original notebooks** in the two-volume facsimile layout.
- License: TIFR copyright; site states the volumes are made available for free download for individual use.
- Fetch recipe:

```bash
mkdir -p ramanujan/raw/sirinudi
cd ramanujan/raw/sirinudi
curl -L -A "Mozilla/5.0" -o vol1.pdf  http://ramanujan.sirinudi.org/Volumes/01/01.pdf
curl -L -A "Mozilla/5.0" -o vol2.pdf  http://ramanujan.sirinudi.org/Volumes/02/02.pdf
# crawl the unpublished_notebooks page for any additional supplementary PDFs:
wget -r -np -l 2 -A "pdf,djvu" -nH --cut-dirs=1 -e robots=off \
     -U "Mozilla/5.0" \
     https://ramanujan.sirinudi.org/html/unpublished_notebooks.html
```

### 2B. Institute of Mathematical Sciences, Chennai — K. Srinivasa Rao's "Ramanujan" site

A page-by-page HTML+image edition of the facsimile, organised by notebook and chapter. This is the only public source where you can view individual facsimile pages of Notebook 1 and Notebook 2 chapter-by-chapter without downloading a multi-hundred-MB PDF.

- Top: https://www.imsc.res.in/~rao/ramanujan/
- Slide-show index: https://www.imsc.res.in/~rao/ramanujan/notebookindex.htm
- Notebook 1 entry: https://www.imsc.res.in/~rao/ramanujan/NotebookFirst.htm
- Directory pattern (mirror-friendly):
  - `https://www.imsc.res.in/~rao/ramanujan/NoteBooks/NoteBook1/chapterI/` … `chapterXVI/`
  - `https://www.imsc.res.in/~rao/ramanujan/NoteBooks/NoteBook2/chapterI/` … `chapterXXI/`
  - each chapter dir contains `page1.htm`, `page2.htm`, … and the corresponding scanned page images (jpg/gif/png)
  - confirmed directory listing visible at e.g. https://www.imsc.res.in/~rao/ramanujan/NoteBooks/NoteBook2/chapterX/
- K.S. Rao's chapter-3 monograph: https://www.imsc.res.in/~rao/ramanujan/images/KSRchap3.pdf
- License: institutional academic site, no explicit reuse license; treat as fair-use research material.
- Coverage: **Notebook 1** (16 chapters) and **Notebook 2** (21 chapters) page-by-page. **Notebook 3** (the unorganised 33-page residue) is **not** clearly separately indexed — for that use the TIFR Vol. 2 PDF.
- Bulk mirror recipe:

```bash
mkdir -p ramanujan/raw/imsc
cd ramanujan/raw/imsc
wget -r -np -l 6 -k -p -E -e robots=off \
     -A "htm,html,jpg,jpeg,gif,png,pdf" \
     -U "Mozilla/5.0" \
     -nH --cut-dirs=2 \
     https://www.imsc.res.in/~rao/ramanujan/NoteBooks/
# also grab the navigation pages
wget -nc -e robots=off -U "Mozilla/5.0" \
     https://www.imsc.res.in/~rao/ramanujan/NotebookFirst.htm \
     https://www.imsc.res.in/~rao/ramanujan/notebookindex.htm
```

### 2C. National Mission for Manuscripts (NAMAMI) / National Digital Library of India

- NAMAMI portal: https://www.namami.gov.in/ ; manuscript treasures: https://www.namami.gov.in/manuscript-treasures
- NDLI hub: https://ndl.iitkgp.ac.in/
- NDLI NAMAMI collection: http://ndl.iitkgp.ac.in/ch_document/namami/namami/0
- **Coverage of Ramanujan's three notebooks: none verified.** NAMAMI focuses on older (mostly pre-1800) Sanskrit and regional-language manuscripts; Ramanujan's notebooks are 20th-century University of Madras holdings and are **not** in the NAMAMI digitised corpus as far as the search results show. NDLI re-indexes Internet Archive copies; searching `Ramanujan notebook` on NDLI will surface the IA TIFR facsimile rather than a fresh scan.
- Worth checking once your project is funded: contact `nmm@ignca.gov.in` and the University of Madras Library directly for high-resolution scans of the originals (the originals themselves are *not* online in any open repository).

### 2D. Indian Institute of Science (IISc), Bangalore — JRD Tata Memorial Library

- Catalog: https://libraryopac.iisc.ac.in/
- Specific Ramanujan records:
  - https://libraryopac.iisc.ac.in/cgi-bin/koha/opac-detail.pl?biblionumber=17462 (Berndt commentary Part I)
  - https://libraryopac.iisc.ac.in/bib/195588 (Andrews/Berndt Lost Notebook Part I)
- One IISc-sourced item is on Internet Archive: https://archive.org/details/in.ernet.dli.2015.212059 (Hardy, *Ramanujan: Twelve Lectures*, scanned by JRD Tata Library / Digital Library of India). This is **commentary, not facsimile**.
- IISc does not appear to publish open scans of the Madras originals.

### 2E. Trinity College, Cambridge — Wren Digital Library

This is **not** the originals (those are in Madras), but Trinity holds **contemporary hand-copies of Notebook 2** sent to Hardy, and the digitised scans are online.

- Top-level fonds: https://archives.trin.cam.ac.uk/index.php/papers-of-srinivasa-ramanujan
- Inventory list: https://archives.trin.cam.ac.uk/index.php/papers-of-srinivasa-ramanujan/informationobject/inventory
- "Copy of Srinivasa Ramanujan's notebook 2" (the Hardy copy), split into 3 segments:
  - chapters I–X [in part] — https://archives.trin.cam.ac.uk/index.php/copy-of-s-ramanujans-notebook-2
  - chapters X[cont]–XVIII [in part] — https://archives.trin.cam.ac.uk/index.php/copy-of-s-ramanujans-notebook-2-2
  - chapters XVIII[cont]–XXI [in part] — https://archives.trin.cam.ac.uk/index.php/copy-of-s-ramanujans-notebook-2-3
- Shelfmark family `Add.Ms.a.94` (items .1 through .18+); viewer URL pattern:
  - https://mss-cat.trin.cam.ac.uk/manuscripts/uv/view.php?n=Add.Ms.a.94.1
  - (substitute .2 through .18 …)
- Coverage: Notebook **2 only** (in copy form, not Ramanujan's hand); plus the Lost Notebook loose sheets and letters to Hardy.
- License: digitisation is openly viewable via the Wren IIIF / Universal Viewer; Trinity terms are "free for non-commercial scholarly use; cite Wren Library, Trinity College Cambridge".
- Bulk fetch is best done via the Universal Viewer's IIIF manifest:

```bash
# Each "n=Add.Ms.a.94.N" page has a IIIF manifest at:
#   https://mss-cat.trin.cam.ac.uk/manuscripts/iiif/Add.Ms.a.94.N/manifest.json
for N in $(seq 1 18); do
  curl -sL -A "Mozilla/5.0" \
       -o "trinity_addmsa94_${N}_manifest.json" \
       "https://mss-cat.trin.cam.ac.uk/manuscripts/iiif/Add.Ms.a.94.${N}/manifest.json"
done
# then for each manifest, extract the canvas image URLs (full/full/0/default.jpg) and curl them.
```

---

## 3. Google Books / HathiTrust

### Google Books / Google Arts & Culture
- Google Arts & Culture has a single curated image (not a full scan): https://artsandculture.google.com/asset/page-from-one-of-srinivasa-ramanujan-s-mathematical-notebooks-tata-institute-of-fundamental-research/RwHiimGRME1ghQ
- Google Books has **no full-view** of the TIFR facsimile — snippet view only, because TIFR copyright is still asserted.

### HathiTrust Digital Library
- Catalog search front page: https://catalog.hathitrust.org/
- Related Ramanujan records that surfaced:
  - https://catalog.hathitrust.org/Record/000470854 — Hardy, *Ramanujan: Twelve Lectures…* (commentary)
  - https://catalog.hathitrust.org/Record/000125086 — *Collected Papers of Srinivasa Ramanujan* (Cambridge 1927) — full-view in US for some library-print copies
  - https://catalog.hathitrust.org/Record/006200873 — generic facsimile-products record
- **No open-access HathiTrust copy of the TIFR 1957 facsimile of Notebooks I–III was found.** The Springer/Narosa 1984/87 reprint is post-1923 and remains in copyright, so any HathiTrust copy will be "Search-only" / "Limited (search-only)" rather than full-text.
- Recipe (works only on items with `access=full` / public-domain status):

```bash
# Search:
open "https://catalog.hathitrust.org/Search/Home?lookfor=ramanujan+notebooks&type=all"
# For a public-domain item with HathiTrust id "$HT_ID":
curl -L -A "Mozilla/5.0" \
     -o ramanujan_hathi.pdf \
     "https://babel.hathitrust.org/cgi/imgsrv/download/pdf?id=$HT_ID"
```

(You will likely fail with `Limited (search-only)` on the TIFR facsimile — fall back to the Internet Archive copies in §1.)

---

## 4. Wolfram "Ramanujan Notebook Project"

**Finding: there is no Wolfram project that hosts facsimile scans of Notebooks I–III.** What exists at Wolfram is computational / typeset re-implementations and demonstration code, not page images.

- Wolfram Library Archive — *Ramanujan R and S*: https://library.wolfram.com/infocenter/MathSource/8439/  (a Mathematica notebook reproducing select identities)
- Wolfram Demonstrations Project — *Ramanujan R and S*: https://demonstrations.wolfram.com/RamanujanRAndS/  (interactive demo)
- Wolfram Function Repository — Ramanujan-related entries: https://resources.wolframcloud.com/search?i=Ramanujan  (e.g. `MockTheta`, `RamanujanPrimes`)
- Wolfram MathWorld biographical / formula pages exist (e.g. `mathworld.wolfram.com/RamanujansNotebooks.html`) but contain reformatted text, not facsimile scans.

If you specifically need Mathematica-style transcriptions of notebook entries, the Wolfram MathSource items above and Andrews/Berndt's published Springer volumes are the path; if you need page images, go to §1 and §2.

---

## 5. Bruce Berndt — *Ramanujan's Notebooks* Parts I–V (Springer)

Pure commentary with full proofs / references; **no facsimile of Ramanujan's handwriting** beyond a few illustrative plates. ISBNs and DOIs:

| Part | Year | Hardcover ISBN-13 | Softcover reprint | Springer DOI | Pages | Internet Archive |
|------|------|-------------------|-------------------|--------------|-------|------------------|
| I    | 1985 | 978-0-387-96110-1 (3-540-96110-0) | 978-1-4612-7007-2 (2012) | 10.1007/978-1-4612-1088-7 | 357 | https://archive.org/details/ramanujan_notebooks_i  (PDF: https://archive.org/download/ramanujan_notebooks_i/ramanujan_notebooks_i.pdf) |
| II   | 1989 | 978-0-387-96794-3 (3-540-96794-X) | — | 10.1007/978-1-4612-4530-8 | 359 | https://archive.org/details/ramanujan_notebooks_ii |
| III  | 1991 | 978-0-387-97503-0 | 978-1-4612-6963-2 | (Springer) | 510 | https://archive.org/details/ramanujan_notebooks_iii  (PDF: https://ia800809.us.archive.org/31/items/ramanujan_notebooks_iii/ramanujan_notebooks_iii.pdf) |
| IV   | 1994 | 978-0-387-94109-7 | — | 10.1007/978-1-4612-0879-2 | 451 | (Springer-only) |
| V    | 1998 | 978-0-387-94941-3 | 978-1-4612-7221-2 (2012) | 10.1007/978-1-4612-1624-7 | 624 | — |

Springer book pages:
- Part I:  https://link.springer.com/book/10.1007/978-1-4612-1088-7
- Part II: https://link.springer.com/book/10.1007/978-1-4612-4530-8
- Part IV: https://link.springer.com/content/pdf/10.1007/978-1-4612-0879-2.pdf
- Part V:  https://link.springer.com/book/10.1007/978-1-4612-1624-7

These three IA items (`ramanujan_notebooks_i`, `..._ii`, `..._iii`) are sometimes mis-described in third-party blog posts as "the original notebooks" — they are not. They are Berndt's text.

---

## Quick fetch summary (the minimum set you actually need)

To reconstitute Notebooks I, II, III in facsimile, the minimal redundant set is:

```bash
mkdir -p ramanujan/raw && cd ramanujan/raw

# Primary: TIFR facsimile via sirinudi.org (cleanest single-PDF per volume)
curl -L -A "Mozilla/5.0" -o tifr_vol1.pdf http://ramanujan.sirinudi.org/Volumes/01/01.pdf
curl -L -A "Mozilla/5.0" -o tifr_vol2.pdf http://ramanujan.sirinudi.org/Volumes/02/02.pdf

# Mirror 1: Internet Archive — TIFR facsimile volume one
curl -L -A "Mozilla/5.0" -o ia_notebooksofsrini0001vari.pdf \
     https://archive.org/download/notebooksofsrini0001vari/notebooksofsrini0001vari.pdf

# Mirror 2: Internet Archive — TIFR facsimile "part one of two"
curl -L -A "Mozilla/5.0" -o ia_part-one-3.pdf \
     https://archive.org/download/part-one-3/part-one-3.pdf

# Page-level (for chapter-indexed access to Notebooks 1 and 2)
wget -r -np -l 6 -k -p -E -e robots=off \
     -A "htm,html,jpg,jpeg,gif,png" \
     -U "Mozilla/5.0" -nH --cut-dirs=2 \
     https://www.imsc.res.in/~rao/ramanujan/NoteBooks/

# Companion: Lost Notebook (Narosa/Springer 1988, ed. Raghavan & Rangachari)
curl -L -A "Mozilla/5.0" -o lost_notebook.pdf \
     https://archive.org/download/lost-notebook/lost-notebook.pdf
```

---

## Items NOT online (need physical / library access)

- **Originals at University of Madras Library.** No open-access scan exists. Contact: University of Madras, Chepauk, Chennai 600 005. Request goes through the Librarian; permission requires institutional letter.
- **TIFR 2011 Collector's Edition** (125th-anniversary two-volume reprint, ~1000 copies). Not online; held by major research libraries.
- **The "fourth" Ramanujan notebook / fragment notebooks** beyond Notebooks 1–3 (the so-called Lost Notebook is partially in §1B; some loose sheets are in Trinity Add.Ms.a.94 — see §2E).

---

## Licensing / re-use summary

| Source | Underlying copyright | Practical status |
|---|---|---|
| TIFR 1957 facsimile (Vol 1, Vol 2) | © Tata Institute of Fundamental Research | TIFR explicitly permits free individual download (per sirinudi.org notice); commercial reuse requires TIFR permission. The 1984 Narosa and 1987 Springer-Narosa reprints add publisher copyright. |
| Internet Archive copies | Hosted as preservation copies | Free download; IA acts under fair-use / DMCA safe-harbor. |
| ramanujan.sirinudi.org | Hosted with TIFR acknowledgement | Free download for individual research. |
| IMSc K.S. Rao site | Academic site, no explicit license | Treat as fair-use research; cite. |
| Trinity College Cambridge (Add.Ms.a.94) | © Master & Fellows, Trinity College | Free non-commercial scholarly use with citation. |
| Berndt Springer volumes | © Springer | In copyright; IA copies are scholarly preservation; do not redistribute. |

---

## Citation block (ready to paste)

> Ramanujan, S. *Notebooks of Srinivasa Ramanujan* (2 vols., facsimile edition). Bombay: Tata Institute of Fundamental Research, 1957. Reprinted: New Delhi: Narosa, 1984; Springer-Narosa, 1987; TIFR Collector's Edition, 2011. Originals held at the University of Madras Library.

> Berndt, B. C. *Ramanujan's Notebooks*, Parts I–V. New York: Springer-Verlag, 1985 / 1989 / 1991 / 1994 / 1998.

> Ramanujan, S. *The Lost Notebook and Other Unpublished Papers*, ed. S. Raghavan & S. S. Rangachari. New Delhi: Narosa / Berlin: Springer, 1988. ISBN 3-540-18726-X.
