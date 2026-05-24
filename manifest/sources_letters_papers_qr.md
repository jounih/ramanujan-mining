# Ramanujan Source Manifest — Letters, Collected Papers, Quarterly Reports, Journal Papers

Compiled 2026-05-24 for the Ramanujan manuscript research project.

Coverage: (A) Ramanujan's letters to Hardy and others, (B) the 1927 Collected Papers, (C) the 1913-14 Quarterly Reports to the Madras Board of Studies, and (D) Ramanujan's original published journal papers (1911-1919).

Notes:
- All `wget` recipes below use polite headers; substitute a User-Agent if rate-limited.
- License column: PD = U.S. public domain (pre-1929 imprint); CC = Creative Commons; CR = under copyright but freely viewable; CR-RES = restricted to logged-in/borrowable.
- WebFetch was blocked by 403 for several Trinity / IMSC / archive.org item pages during research; URLs were verified via WebSearch result snippets. Confirm file sizes with `curl -sI <url>` at download time.

---

## A. Ramanujan's Letters

### A.1 Trinity College Cambridge — Wren Digital Library (primary source)

The originals of most surviving Ramanujan letters and manuscripts are held at Trinity. Two finding-aid pages list the holdings; image viewers live on `mss-cat.trin.cam.ac.uk`.

| Item | URL | Notes |
|---|---|---|
| Finding aid: "Letters from Srinivasa Ramanujan to G. H. Hardy" | https://archives.trin.cam.ac.uk/index.php/letters-from-ramanujan-to-g-h-hardy | Catalogue entry listing each letter; click-through to digitised images |
| Finding aid: "Papers of Srinivasa Ramanujan" (Add.MS.a.94) | https://archives.trin.cam.ac.uk/index.php/papers-of-srinivasa-ramanujan | Top-level collection, ~17 sub-items |
| Inventory (one-page list) | https://archives.trin.cam.ac.uk/index.php/papers-of-srinivasa-ramanujan/informationobject/inventory | Useful for scripting |
| "So-called Lost Notebook" sub-page | https://archives.trin.cam.ac.uk/index.php/the-so-called-lost-notebook-2 | |
| Wren Digital Library landing | https://www.trin.cam.ac.uk/library/wren-digital-library/ | IIIF compliant |
| Wren manuscripts viewer pattern | https://mss-cat.trin.cam.ac.uk/manuscripts/uv/view.php?n=Add.Ms.a.94.<N> | N = 1..17+ for sub-items |

Examples of confirmed sub-item viewer URLs (found in search snippets):
- Add.Ms.a.94.5 → https://mss-cat.trin.cam.ac.uk/manuscripts/uv/view.php?n=Add.Ms.a.94.5
- Add.Ms.a.94.6 → https://mss-cat.trin.cam.ac.uk/manuscripts/uv/view.php?n=Add.Ms.a.94.6
- Add.Ms.a.94.9 → https://mss-cat.trin.cam.ac.uk/manuscripts/uv/view.php?n=Add.Ms.a.94.9
- Add.Ms.a.94.13 → https://mss-cat.trin.cam.ac.uk/manuscripts/uv/view.php?n=Add.Ms.a.94.13
- Add.Ms.a.94.16 → https://mss-cat.trin.cam.ac.uk/manuscripts/uv/view.php?n=Add.Ms.a.94.16

Notable known references (per Trinity catalog snippets):
- Add.MS.a.94/2 — "Letters from Srinivasa Ramanujan to G. H. Hardy" dated 26 June 1918
- Add.MS.a.94 also contains the **last letter to Hardy (12 Jan 1920)** with the mock theta functions, plus the "Lost Notebook" sheets rediscovered by G. E. Andrews in 1976.

License: Wren Digital Library images are released under **CC BY-NC 4.0** (announced on the Trinity College Library blog, 2015). Image downloads via IIIF.

wget recipe (IIIF, once you have the manifest URL from the viewer):
```
# 1) Inspect viewer page to find IIIF manifest:
curl -s "https://mss-cat.trin.cam.ac.uk/manuscripts/uv/view.php?n=Add.Ms.a.94.2" | grep -oE 'manifest[^"]+\.json'
# 2) Download every canvas via jq:
curl -s <manifest_url> | jq -r '.sequences[].canvases[].images[].resource."@id"' \
  | xargs -n1 -I{} wget --user-agent="research-script/1.0" "{}"
```

### A.2 Internet Archive — facsimile of the first letter (16 Jan 1913)

| Field | Value |
|---|---|
| URL | https://archive.org/details/ramanujans_letter |
| Coverage | The 16 January 1913 letter to Hardy (cover + ~11 pages of theorems, c. 120 results) |
| Item identifier | `ramanujans_letter` |
| Format | PDF, text, JP2, DjVu (auto-derived) |
| Direct PDF (text-derivative) | https://ia903209.us.archive.org/26/items/ramanujans_letter/ramanujans_letter_text.pdf |
| License | PD (pre-1929) |
| wget | `wget "https://archive.org/download/ramanujans_letter/ramanujans_letter_text.pdf"` (or use `ia download ramanujans_letter` after `pip install internetarchive`) |

### A.3 Internet Archive — Ramanujan: Letters and Commentary (Berndt & Rankin 1995)

Full-text reference volume that reproduces every letter to/from Ramanujan plus commentary. Companion volume "Ramanujan: Essays and Surveys" complements it.

| Field | Value |
|---|---|
| URL | https://archive.org/details/brucec.berndtandroberta.rankinramanujanzlib.org |
| Coverage | All known letters (Hardy, Hill, Hobson, Baker, Mahalanobis, Subramanian, Krishna Rao, Madras officials, etc.) with commentary |
| Format | PDF, EPUB, DjVu |
| License | CR (uploaded copy; verify access status) |
| wget | `wget "https://archive.org/download/brucec.berndtandroberta.rankinramanujanzlib.org/<file>.pdf"` — see item page for exact filename |

Companion: dokumen.pub mirror of "Ramanujan: Essays and Surveys": https://dokumen.pub/ramanujan-essays-and-surveys-1nbsped-9781470438906-9780821826249.html

### A.4 IMSC (Institute of Mathematical Sciences, Chennai) — K. Srinivasa Rao site

R. Balasubramanian / K. Srinivasa Rao has hosted a comprehensive page set with transcripts, photos, and PDFs.

| Item | URL | Notes |
|---|---|---|
| Site root | https://www.imsc.res.in/~rao/ramanujan/index.html | Hub |
| First-letter index (16 Jan 1913) | https://www.imsc.res.in/~rao/ramanujan/newnow/hardyletterindex.htm | Transcription + commentary, page-by-page |
| Last letter (12 Jan 1920, mock thetas) — **direct PDF** | https://www.imsc.res.in/~rao/ramanujan/newnow/lastletter.pdf | Confirmed facsimile/transcript |
| Letter to Krishna Rao (7 Aug 1914) | https://www.imsc.res.in/~rao/ramanujan/newnow/ramtokrisrao.htm | |
| Letters to Baker & Hobson context | https://www.imsc.res.in/~rao/ramanujan/newnow/bakerhobson.htm | |
| Neville → Dewsbury (re. first letter) | https://www.imsc.res.in/~rao/ramanujan/newnow/nevilletodews.htm | |
| Lost notebook background | https://www.imsc.res.in/~rao/ramanujan/newnow/lostNBfirstBG.htm | |
| Ramanujan's illness (D.A.B. Young) | https://www.imsc.res.in/~rao/ramanujan/newnow/illness.pdf | |
| K.S. Rao chapter 3 — Notebooks | https://www.imsc.res.in/~rao/ramanujan/images/KSRchap3.pdf | |
| Berndt interview transcript | https://www.imsc.res.in/~rao/ramanujan/interviews/transcripts/bruce.pdf | |

License: Personal academic site; clearly intended for research use. Treat as CR-RES; cite K. Srinivasa Rao when redistributing.

wget recipe (mirror the newnow/ tree):
```
wget -e robots=off -r -np -l2 -A "pdf,htm,html,jpg,png,gif" \
     -U "Mozilla/5.0 research-script" \
     https://www.imsc.res.in/~rao/ramanujan/newnow/
```

### A.5 Letters to Mahalanobis / Subramanian — print-only sources

These letters are primarily reproduced in:
- **P. K. Srinivasan (ed.), "Ramanujan: Letters and Reminiscences"** (Memorial Number 1, Muthialpet High School, Madras, 1968). NLA cat: https://catalogue.nla.gov.au/Record/2590366 ; WorldCat: https://search.worldcat.org/title/ramanujan-letters-and-reminiscences/oclc/32971828
  - Contains: Mahalanobis "My friendship with Ramanujan in England"; letters to S.M. Subramanian (pp. 20-27); etc.
  - No archive.org copy located as of 2026-05-24. Held by NLA and several university libraries.
- **Berndt & Rankin, "Ramanujan: Letters and Commentary"** (1995) — see A.3, has full transcripts.

### A.6 Hardy's own Ramanujan correspondence — Trinity Wren

Hardy's papers (separate from Add.MS.a.94) include incoming letters and drafts of Hardy's outgoing letters. Search the Trinity ArchivesSpace: https://archives.trin.cam.ac.uk/ for "Hardy" + "Ramanujan". Hardy's 8 Feb 1913 reply is famously reproduced in Hardy's "Ramanujan: Twelve Lectures" (1940; see Collected Papers and the Wikisource entries below).

### A.7 Secondary scans / blog reproductions (use as cross-reference, not primary)

- Cantor's Paradise essay on the first letter: https://www.cantorsparadise.org/ramanujans-first-letter-to-g-h-hardy-1913-33244f545e80/
- Privatdozent (Veisdal): https://www.privatdozent.co/p/ramanujans-first-letter-to-gh-hardy-1d9
- Scribd upload of first letter: https://www.scribd.com/document/759781327/Ramanujan-s-first-letter
- Wolfram blog (Wolfram, 2016) with photos & letters: https://writings.stephenwolfram.com/2016/04/who-was-ramanujan/
- "Letter that changed Ramanujan's life" (Medium): https://siddharthlabh.medium.com/the-letter-that-changed-ramanujans-life-e0cdf9f97f48
- Twitter/X facsimile thread (Srinivas R.): https://threadreaderapp.com/thread/1255366474467770369.html
- ISI lecture notes (Abhishek): https://www.isical.ac.in/~abhishek/ramanujan.pdf
- Arizona talk (Cais) with first-letter excerpts: https://math.arizona.edu/~cais/Papers/Talks/rama_talk.pdf

---

## B. Collected Papers of Srinivasa Ramanujan (Hardy, Seshu Aiyar, Wilson, eds., Cambridge UP, 1927)

The 1927 first edition is **U.S. public domain**.

### B.1 Internet Archive — primary public-domain scan (Kerala Public Library copy)

| Field | Value |
|---|---|
| Detail URL | https://archive.org/details/pli.kerala.rare.28155 |
| Identifier | `pli.kerala.rare.28155` |
| Edition | 1927, Cambridge University Press; xxxvi + 355 pp. (~393 incl. front matter) |
| Coverage | All 37 published papers + notes + extracts from Ramanujan's letters to Hardy |
| Formats | PDF, EPUB, DjVu, full text (OCR), JP2 zip |
| License | PD |
| Direct PDF | https://archive.org/download/pli.kerala.rare.28155/pli.kerala.rare.28155.pdf |
| Direct DjVu txt | https://archive.org/stream/pli.kerala.rare.28155/pli.kerala.rare.28155_djvu.txt |
| wget | `wget "https://archive.org/download/pli.kerala.rare.28155/pli.kerala.rare.28155.pdf"` |
| Bulk dl | `ia download pli.kerala.rare.28155` (after `pip install internetarchive`) |

### B.2 HathiTrust — full view (Michigan copy)

| Field | Value |
|---|---|
| Catalog | https://catalog.hathitrust.org/Record/000125086 |
| Full view | https://babel.hathitrust.org/cgi/pt?id=mdp.39015037936096 |
| HathiTrust ID | `mdp.39015037936096` |
| Edition | 1927 first edition |
| Format | Per-page PDF / JPG; whole-volume PDF requires HT login (Partner institution) |
| License | PD |
| wget single page | HathiTrust does not allow anonymous full-PDF download. Page images: `https://babel.hathitrust.org/cgi/imgsrv/image?id=mdp.39015037936096;seq=<N>;size=full;rotation=0` |

### B.3 Additional Internet Archive copies

- 1962 Chelsea reprint (Hardy/Aiyar/Wilson + Berndt/Rankin commentary): https://archive.org/details/srinivasaramanuj0000unse (CR-RES, borrowable)
- Another 1962 Chelsea copy: https://archive.org/details/collectedpapers0000srin (CR-RES)
- BWB scan (year not confirmed): https://archive.org/details/bwb_Y0-AAH-988
- Plain text/mirror PDF (Peach F. hosting): https://peachf.org/images/SouthAsia/IndiaMathPapersRamanujan.pdf
- Google Books (snippet/full view varies by region): https://books.google.com/books/about/Collected_Papers_of_Srinivasa_Ramanujan.html?id=oSioAM4wORMC
- 2015 Cambridge reissue (paid, modern ISBN): https://www.cambridge.org/9781107536517

### B.4 Project Gutenberg / Wikisource

No complete transcription was located on Project Gutenberg or English Wikisource as of 2026-05-24. The OCR text on archive.org (item `pli.kerala.rare.28155`, DjVu text derivative) is the closest machine-readable corpus.

---

## C. Ramanujan's Quarterly Reports to the Board of Studies, University of Madras (1913-1914)

The three quarterly reports were produced during Ramanujan's University of Madras research scholarship (75 rupees/month, granted March 1913). The originals are **lost**; the surviving textual witness is a 1925 handwritten copy made by T. A. Satagopan, now studied by Berndt.

### C.1 Berndt's edition / analyses

- **Bruce C. Berndt, "Ramanujan's Quarterly Reports"** — Bulletin of the London Mathematical Society 16 (1984), 449-489. This is the principal scholarly edition (faithful reproduction + commentary). Available behind LMS/Wiley paywall; PDF freely available via HAL: **https://hal.science/hal-03912911/document**
- **Bruce C. Berndt, "The quarterly reports of S. Ramanujan"** — American Mathematical Monthly 90 (1983), 505-516. JSTOR (paywalled) / MAA archive.
- Berndt's full-length treatment of the reports' contents appears as a chapter in **"Ramanujan's Notebooks, Part I"** (Springer, 1985). Archive.org search: https://archive.org/search?query=ramanujan+notebooks+berndt — Parts II, III, IV, V are all on archive.org:
  - Part II: https://archive.org/details/ramanujan_notebooks_ii
  - Part III: https://archive.org/details/ramanujan_notebooks_iii (direct PDF: https://ia800809.us.archive.org/31/items/ramanujan_notebooks_iii/ramanujan_notebooks_iii.pdf)
  - Part I copy: search archive.org under `ramanujan_notebooks_i` / `Ramanujan_notebooks_I` (multiple uploads exist, status varies).

### C.2 Original Satagopan handwritten copy

Held at the University of Madras / Madras Mathematical Library. **No public digitization** has been located as of 2026-05-24. Berndt's 1984 BLMS paper reproduces the mathematical content in typeset form.

### C.3 wget recipe for the Berndt 1984 HAL PDF

```
wget -U "Mozilla/5.0 research" \
     -O berndt_1984_quarterly_reports.pdf \
     https://hal.science/hal-03912911/document
```
License of HAL deposit: Author manuscript; treat as CR with personal-research-use OK.

---

## D. Original Published Journal Papers (1911-1919)

### D.1 ramanujan.sirinudi.org — most complete free PDF mirror

Master index pages:
- HTML index of all 37 papers: http://ramanujan.sirinudi.org/html/published_papers.html
- Directory listing of PDFs: http://ramanujan.sirinudi.org/Volumes/published/
- Unpublished notebooks index: https://ramanujan.sirinudi.org/html/unpublished_notebooks.html

Naming pattern: `ram01.pdf` … `ram37.pdf` for the 37 published papers, with matching `ramNN.html` description pages. Confirmed direct PDF URLs surfaced in search:

| # | Paper | Journal, year | sirinudi PDF |
|---|---|---|---|
| 06 | Modular equations and approximations to π | Quart. J. Pure Appl. Math. 45 (1914), 350-372 | https://ramanujan.sirinudi.org/Volumes/published/ram06.pdf |
| 10 | (q-series / hypergeometric paper) | — | http://ramanujan.sirinudi.org/Volumes/published/ram10.pdf |
| 13 | (paper #13) | — | http://ramanujan.sirinudi.org/Volumes/published/ram13.pdf |
| 15 | Highly composite numbers | Proc. London Math. Soc. (2) 14 (1915), 347-409 | https://ramanujan.sirinudi.org/Volumes/published/ram15.pdf |
| 18 | On certain arithmetical functions (introduces τ(n)) | Trans. Camb. Phil. Soc. 22, no. 9 (1916), 159-184 | https://ramanujan.sirinudi.org/Volumes/published/ram18.pdf |
| 36 | Asymptotic formulae in combinatory analysis (with Hardy) | Proc. London Math. Soc. (2) 17 (1918), 75-115 | https://ramanujan.sirinudi.org/Volumes/published/ram36.pdf |

Bulk mirror recipe:
```
mkdir -p ramanujan_sirinudi && cd ramanujan_sirinudi
for i in $(seq -w 1 37); do
  wget --continue "http://ramanujan.sirinudi.org/Volumes/published/ram${i}.pdf"
done
# Also grab the description HTML:
for i in $(seq -w 1 37); do
  wget --continue "http://ramanujan.sirinudi.org/Volumes/published/ram${i}.html"
done
```
License: posted by an academic mirror; the underlying papers are PD. Cite originals.

### D.2 Wiley Online Library — original PLMS scans

The London Mathematical Society's pre-1923 PLMS issues are **open access** (PD content; LMS sometimes also marks them OA). Direct DOIs for the key Ramanujan/Hardy papers:

| Paper | Year | DOI / URL |
|---|---|---|
| Highly Composite Numbers (Ramanujan) | 1915 | https://doi.org/10.1112/plms/s2_14.1.347 — PDF: https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/plms/s2_14.1.347 |
| Asymptotic Formulaæ in Combinatory Analysis (Hardy & Ramanujan) | 1918 | https://doi.org/10.1112/plms/s2-17.1.75 — abstract: https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/plms/s2-17.1.75 |
| One Class of Definite Integrals (multiple PLMS papers) | 1915-1918 | Browse PLMS s2-13…s2-17 issues via https://londmathsoc.onlinelibrary.wiley.com/journal/1460244x |

wget (PLMS PDFs are accessible without subscription for PD content; may need a UA):
```
wget -U "Mozilla/5.0" -O hcn_1915.pdf \
  "https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/plms/s2_14.1.347"
```

### D.3 Cambridge Core — Trans. & Proc. Cambridge Philosophical Society

Several Ramanujan papers appeared in CPS journals (e.g., "On certain arithmetical functions", 1916). Modern Cambridge Core listings (some are OA for pre-1923 content):
- "A look back at Ramanujan's Notebooks" (Hardy-Ramanujan): https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/look-back-at-ramanujans-notebooks/DFB7B37DD67D0DF771457DD0CD5EBE81
- Mordell, "Note on Ramanujan's arithmetical function τ(n)" (1917): https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/note-on-ramanujans-arithmetical-function-n/8F23A3DE950CF9AF3DDFC3ED2A4989D5
- Sophiararebooks listing of the 1916 offprint (for provenance): https://www.sophiararebooks.com/pages/books/6358/srinivasa-ramanujan/on-certain-arithmetical-functions-offprint-from-transactions-of-the-cambridge-philosophical

### D.4 Hardy-Ramanujan Journal (modern open-access journal, NOT originals)

`hrj.episciences.org` is Diamond OA (CC-BY 4.0) but publishes contemporary number-theory research — useful for commentary, not original Ramanujan papers. Volumes 43-44 are commemorative.

### D.5 Other Internet Archive items relevant to journal papers

- "The lost notebook and other unpublished papers" (Narosa 1988, facsimile): https://archive.org/details/lostnotebookothe0000rama and https://archive.org/details/xdpb_srinivasa-ramanujan-the-lost-note-book-and-other-unpublished-papers-1988-new-del and https://archive.org/details/lost-notebook
- Tata Institute "Notebooks of Srinivasa Ramanujan" (1957 facsimile, two volumes): https://archive.org/details/notebooksofsrini0001vari (also: https://archive.org/details/ramanujansnotebo0000rama and https://archive.org/details/part-one-3). Tata holds copyright; downloads permitted for individual use.
- Andrews/Berndt "Ramanujan's Lost Notebook Part I" (Springer, 2005): https://archive.org/details/ramanujanslostnotebook-parti.2005.georgee.andrews.brucec.berndt2
- "Ramanujan's lost notebook. Part III" (Andrews): https://archive.org/details/ramanujanslostno0000andr
- "Ramanujan's lost notebook part 4" upload: https://archive.org/details/78bb-2c-662df-08bdfffff-8024fffffff-1
- "Ramanujan's Notebooks Part II" (Berndt): https://archive.org/details/ramanujan_notebooks_ii
- "Ramanujan's Notebooks Part III" (Berndt): https://archive.org/details/ramanujan_notebooks_iii (PDF: https://ia800809.us.archive.org/31/items/ramanujan_notebooks_iii/ramanujan_notebooks_iii.pdf)

---

## E. Companion references (biography / context)

- Wikipedia: https://en.wikipedia.org/wiki/Srinivasa_Ramanujan and https://en.wikipedia.org/wiki/Ramanujan's_lost_notebook
- MacTutor (St Andrews): https://mathshistory.st-andrews.ac.uk/Biographies/Ramanujan/
- Short-life essay: https://mathshistory.st-andrews.ac.uk/SH/ramanujan_sh.pdf
- Wolfram, "Who Was Ramanujan?" (2016): https://writings.stephenwolfram.com/2016/04/who-was-ramanujan/
- Trinity College Library blog tag "Ramanujan": https://trinitycollegelibrarycambridge.wordpress.com/tag/ramanujan/
- Trinity Library "Remembering Ramanujan" (2020): https://trinitycollegelibrarycambridge.wordpress.com/2020/04/24/remembering-ramanujan/
- "The Man Who Knew Infinity" (Trinity blog, 2016): https://trinitycollegelibrarycambridge.wordpress.com/2016/04/08/the-man-who-knew-infinity/
- "Unpublished Manuscripts of Ramanujan" (Resonance 2010): https://www.ias.ac.in/public/Volumes/reso/015/02/0187-0197.pdf
- Andrews & Berndt, "Uncovering Ramanujan's Lost Notebook: An Oral History" (arXiv): https://arxiv.org/pdf/1208.2694
- Rankin review (IMSC mirror): https://www.imsc.res.in/~rao/ramanujan/books/rankin.html
- "Ramanujan's Deathbed Letter" (Rolen, Vanderbilt): https://math.vanderbilt.edu/rolenl/RamaDefn.pdf
- "Ramanujan's Last Letter to Hardy" (Andrews & Berndt, Springer chapter): https://link.springer.com/chapter/10.1007/978-3-319-77834-1_14

---

## F. Outstanding gaps / things still to chase

1. **Trinity per-letter direct image URLs** — the IIIF manifests resolve when you open each `Add.Ms.a.94.N` viewer; a one-shot crawl of `mss-cat.trin.cam.ac.uk/manuscripts/uv/view.php?n=Add.Ms.a.94.<1..30>` will surface every sub-item. Several archives.trin.cam.ac.uk and IMSC pages returned HTTP 403 to the WebFetch agent in this session — re-run from an unrestricted network to confirm direct image URLs.
2. **Letters to Mahalanobis / Subramanian** — no public scans located; only the print P.K. Srinivasan volume (1968) and the Berndt-Rankin transcription (1995).
3. **The three Quarterly Reports** — only Berndt's typeset version (BLMS 1984, HAL OA) is public. The Satagopan handwritten copy at U. Madras does not appear digitized.
4. **A clean PD scan of the 2nd letter (27 Feb 1913)** — present as transcription in the Collected Papers (`pli.kerala.rare.28155`) and Berndt-Rankin, but a standalone facsimile equivalent to the 16 Jan 1913 archive.org item was not located.
5. **HathiTrust full-PDF download** of `mdp.39015037936096` — needs an HT partner login; bypass by using the archive.org PD copy instead.

