# Ramanujan "Lost Notebook" — Digital Source Manifest

Compiled 2026-05-24. All URLs verified via WebSearch; live HTTP probes from this
sandbox were blocked by an allowlist, so file sizes marked "approx." should be
confirmed by a one-off `curl -I` from an unrestricted host before bulk fetch.

The historical object is the bundle of ~138 loose sheets in Ramanujan's hand
(work from 1919–1920) discovered by George Andrews in 1976 in G. N. Watson's
papers at the Wren Library, Trinity College, Cambridge. The primary catalogue
reference is **Trinity College Add.MS.a.94/15** (the parent collection
Add.MS.a.94 also contains the Hardy–Ramanujan correspondence, scribal copies of
Notebook 2, and related Watson/Hardy material).

---

## 1. Trinity College Library, Cambridge — Wren Digital Library (primary)

### Landing pages

- Collection top: <https://archives.trin.cam.ac.uk/index.php/papers-of-srinivasa-ramanujan>
- Inventory list: <https://archives.trin.cam.ac.uk/index.php/papers-of-srinivasa-ramanujan/informationobject/inventory>
- Lost Notebook item record: <https://archives.trin.cam.ac.uk/index.php/the-so-called-lost-notebook-2>
- Library overview: <https://www.trin.cam.ac.uk/library/wren-digital-library/>

### Image-viewer URL pattern

Trinity exposes a Universal Viewer instance, with one URL per shelfmark:

```
https://mss-cat.trin.cam.ac.uk/manuscripts/uv/view.php?n=Add.Ms.a.94.<N>
```

The Lost Notebook proper is `Add.Ms.a.94.15`. Related items in the same series
(useful neighbours for the research project):

| Shelfmark         | Contents (per Trinity catalogue)                    |
|-------------------|-----------------------------------------------------|
| Add.Ms.a.94.1–14  | Hardy correspondence, scribal copies of Notebook 2, miscellanea |
| **Add.Ms.a.94.15**| **"So-called Lost Notebook" – 138 loose sheets**    |
| Add.Ms.a.94.16–18 | Further loose papers / Watson notes                 |

### IIIF manifest

The viewer is backed by IIIF Presentation manifests at:

```
https://mss-cat.trin.cam.ac.uk/Manuscript/<SHELFMARK>/manifest.json
```

Example confirmed live for a different MS: `…/Manuscript/O.3.58/manifest.json`.
For the Lost Notebook the manifest is therefore expected at:

```
https://mss-cat.trin.cam.ac.uk/Manuscript/Add.Ms.a.94.15/manifest.json
```

Each canvas in the manifest contains a IIIF Image API `service["@id"]`, from
which any page can be pulled at:

```
<service_id>/full/full/0/default.jpg     # full resolution master
<service_id>/full/2000,/0/default.jpg    # 2000-px wide derivative
```

### What is available

Full notebook, all sheets (recto + verso where applicable), high-resolution
colour. Trinity states "Ramanujan's papers have all been digitised" and access
to originals is now restricted for preservation.

### Format & size

- Per-image JPEG/JP2 via IIIF Image API (typical master ≈ 3–8 MB/page).
- No single bundled PDF is offered by Trinity. For ~250 sides at ~5 MB
  → expect roughly **1.0–1.5 GB** if you pull masters; ~150 MB at 2000-px.

### Licence / rights

Wren Digital Library images are © Master & Fellows of Trinity College,
Cambridge, released under **Creative Commons BY-NC**
(see <https://trinitycollegelibrarycambridge.wordpress.com/2015/05/18/wdl-and-creative-commons/>).
Personal-study downloads are permitted from the viewer; publication requires
written permission from the Library.

### Download recipe (IIIF)

```bash
MAN=https://mss-cat.trin.cam.ac.uk/Manuscript/Add.Ms.a.94.15/manifest.json
curl -s "$MAN" -o lost_notebook_manifest.json
# Extract every image service @id and pull the full master:
jq -r '.sequences[0].canvases[].images[0].resource.service["@id"]' \
   lost_notebook_manifest.json \
 | awk '{ printf "%s/full/full/0/default.jpg\n", $0 }' \
 | wget -i - -P pages/ --content-disposition \
        --user-agent="research-bot (mailto:jouni@helminen.co)"
```

(Add `--wait=2 --random-wait` to be polite; Trinity has no public rate limit
documented but the server is small.)

---

## 2. Internet Archive

Three independent uploads of the **Narosa 1988 facsimile** ("The Lost
Notebook and Other Unpublished Papers", ed. G. E. Andrews et al., Narosa,
New Delhi, with TIFR/Springer co-imprint) cover the same content with
different scan quality.

### 2a. `lostnotebookothe0000rama` (best metadata)

- Details: <https://archive.org/details/lostnotebookothe0000rama>
- Download dir: <https://archive.org/download/lostnotebookothe0000rama>
- xxv + 419 pp., 32 cm. Includes the 90-leaf facsimile section plus 180 pp.
  of related unpublished MSS (28 pp. from the Trinity "Loose Papers").
- Formats: PDF, EPUB, full text, single-page-processed JP2 ZIP, DjVu.
- Approx. sizes: PDF ≈ 35–60 MB; JP2 ZIP ≈ 350–500 MB.
- Status: **Borrow-only (controlled digital lending, 1-hour / 14-day loans)**
  – item is in-copyright (Narosa/Springer 1988).

### 2b. `lost-notebook` (alternate upload)

- Details: <https://archive.org/details/lost-notebook>
- Download dir: <https://archive.org/download/lost-notebook>
- Same Narosa facsimile; marked openly downloadable on IA at time of writing
  (status can change — check the "DOWNLOAD OPTIONS" panel before scripting).
- Formats: PDF, JP2 ZIP, text.

### 2c. `xdpb_srinivasa-ramanujan-the-lost-note-book-and-other-unpublished-papers-1988-new-del`

- Details: <https://archive.org/details/xdpb_srinivasa-ramanujan-the-lost-note-book-and-other-unpublished-papers-1988-new-del>
- 1988 Narosa edition, community upload, openly downloadable. Lower OCR quality.

### 2d. Related notebooks (TIFR 1957 facsimile of Notebooks 1–3)

- <https://archive.org/details/notebooksofsrini0001vari>
- <https://archive.org/details/ramanujansnotebo0000rama>
- These are NOT the Lost Notebook but are the standard reference companions.

### IA download recipe

```bash
# Get the file inventory for any item:
curl -s "https://archive.org/metadata/lost-notebook" | jq '.files[].name'

# Pull just the PDF:
wget "https://archive.org/download/lost-notebook/lost-notebook.pdf"

# Pull the page-image JP2 ZIP (gives you per-page rasters):
wget "https://archive.org/download/lost-notebook/lost-notebook_jp2.zip"

# Bulk by identifier list (Internet Archive's official pattern):
echo -e "lost-notebook\nlostnotebookothe0000rama\nxdpb_srinivasa-ramanujan-the-lost-note-book-and-other-unpublished-papers-1988-new-del" > items.txt
wget -r -H -nc -np -nH --cut-dirs=1 -A .pdf,.zip -e robots=off -l1 \
     -i items.txt -B 'https://archive.org/download/'
```

Licence on IA: items show "in copyright" — uploads 2b/2c are tolerated but not
formally licensed for redistribution. Treat as research-fair-use copies.

---

## 3. Other repositories

### 3a. ramanujan.sirinudi.org (community mirror)

- <https://ramanujan.sirinudi.org/html/unpublished_notebooks.html>
- Curated index page maintained by Indian Ramanujan enthusiasts; links to the
  same Narosa facsimile PDF plus per-chapter splits and transcription PDFs.
  No new scans, but useful as a deep-linked index.

### 3b. HathiTrust

- A search of HathiTrust (catalog.hathitrust.org) for "Ramanujan lost notebook"
  returns the Narosa 1988 edition in **Search-Only / no-full-view** status
  (in-copyright, US). Not useful for bulk image retrieval.

### 3c. Google Books

- "The Lost Notebook and Other Unpublished Papers" (Narosa/Springer 1988,
  ISBN 0-387-18726-X / 978-0-387-18726-6) is on Google Books in
  **snippet-view only**.

### 3d. National Digital Library of India (NDLI) / Indian Digital Heritage

- NDLI (<https://ndl.iitkgp.ac.in>) indexes the Andrews-Berndt commentary
  volumes but not raw facsimile pages. No primary scans found beyond what is
  already on Internet Archive.

### 3e. Project Euclid / AMS

- Review (Askey 1988) of the Narosa edition, open access:
  <https://projecteuclid.org/journals/bulletin-of-the-american-mathematical-society-new-series/volume-19/issue-2/Review--Srinivasa-Ramanujan-The-lost-notebook-and-other-unpublished/bams/1183554749.full>
- Andrews & Schneider, "Uncovering Ramanujan's 'Lost' Notebook: An Oral
  History" (open access): <https://arxiv.org/abs/1208.2694>

---

## 4. Berndt & Andrews — Springer commentary series ("Ramanujan's Lost Notebook")

These are commentary/proof volumes, **not** facsimile editions, but each
chapter reproduces the relevant manuscript page-number citations from the Lost
Notebook (no full facsimile images; some volumes include 1–2 sample plates).
All paywalled on Springer Link; freely available on Internet Archive in
borrow-only form.

| Vol | Year | DOI / Springer URL | ISBN-13 | IA mirror |
|-----|------|--------------------|---------|-----------|
| I   | 2005 | <https://link.springer.com/book/10.1007/0-387-28124-X>          | 978-0-387-25529-3 | <https://archive.org/details/ramanujanslostnotebook-parti.2005.georgee.andrews.brucec.berndt2> |
| II  | 2009 | <https://link.springer.com/book/10.1007/b13290>                 | 978-0-387-77765-8 | (search IA: "ramanujan lost notebook part ii") |
| III | 2012 | <https://link.springer.com/book/10.1007/978-1-4614-3810-6>      | 978-1-4614-3809-0 | <https://archive.org/details/ramanujanslostno0000andr> |
| IV  | 2013 | <https://link.springer.com/book/10.1007/978-1-4614-4081-9>      | 978-1-4614-4080-2 | <https://archive.org/details/78bb-2c-662df-08bdfffff-8024fffffff-1> |
| V   | 2018 | <https://link.springer.com/book/10.1007/978-3-319-77834-1>      | 978-3-319-77832-7 | (search IA) |

Springer has not opened any of these volumes; no chapters carry free
supplementary facsimile bundles. Vol. I front-matter PDF preview is
freely fetchable:
`https://link.springer.com/content/pdf/10.1007/0-387-28124-X.pdf` (front
matter only without institutional access).

Part I IA download recipe (community upload, openly downloadable at present):

```bash
wget "https://archive.org/download/ramanujanslostnotebook-parti.2005.georgee.andrews.brucec.berndt2/Ramanujan%27s%20Lost%20Notebook%20%E2%80%93%20Part%20I%20.%202005%20.%20George%20E.%20Andrews%20.%20Bruce%20C.%20Berndt%20%282%29.pdf"
```

---

## Recommendation for the research project

For working with the **actual manuscript imagery**, pull from Trinity
(authoritative, high-res, CC-BY-NC) using the IIIF recipe in §1. Use the
IA Narosa facsimile (§2b) as a fallback / for items where the Trinity scan
is incomplete, and to cross-reference Andrews' published "sheet numbers"
(the Narosa edition's sheet numbering is the de facto citation standard used
by every paper in the field, and is the one Berndt & Andrews follow in the
Springer commentary volumes).

Always send a descriptive User-Agent string and a contact email; both
Trinity's `mss-cat` server and IA appreciate this for research crawls.
