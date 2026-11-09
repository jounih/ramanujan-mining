# Ramanujan Claude Source Pack v2

Created/updated: 2026-05-24T12:43:06.419758+00:00

This pack is intended to unblock offline/cloud agents that cannot access the open internet. It bundles the locally available Ramanujan primary-source PDFs/page images, the high-leverage Quarterly Reports reproduction/transcription, and extra open-access context PDFs saved as-is.

## What is included

1. `priority_sources/quarterly_reports/`
   - `ramanujan_quarterly_reports_2022_HRJ_Berndt.pdf`: Hardy-Ramanujan Journal PDF of Bruce C. Berndt's faithful reproduction of Ramanujan's Quarterly Reports.
   - `ramanujan_quarterly_reports_2022_HRJ_Berndt.txt`: `pdftotext` extraction for programmatic Hunt 5 tagging.
   - `ramanujan_quarterly_reports_2022_HRJ_Berndt.operator_blocks.csv`: rough auto-triage rows for abstract-operator tagging.

2. `primary_originals/pdfs/notebooks/`
   - Notebook 1, Notebook 2, Notebook 3, and Lost Notebook facsimile PDFs.

3. `primary_originals/page_images/`
   - 1,149 extracted page images from the four notebook/lost-notebook PDFs.

4. `primary_originals/pdfs/published/`
   - 37 published-paper PDFs.

5. `primary_originals/text/`
   - Text extracted from the published-paper PDFs plus notebook text stubs.

6. `priority_sources/lost_notebook_pages_341_343/`
   - Convenience copies of Lost Notebook page images 341, 342, and 343 for the 1729/two-cubes/K3 target.

7. `priority_sources/open_access_context_pdfs/`
   - OA/context PDFs saved as-is, including Ono--Trebat-Leder on the 1729 K3 surface, Bhatnagar on Ramanujan q-continued fractions, Berndt--Li--Zaharescu's final-problem identity, historical/contextual lost-notebook papers, and a 1927 collected-papers scan. See `priority_sources/open_access_context_manifest.csv`.

8. `phase2_context/`
   - TODOs, schemas, registry seeds, Wren downloader targets, OCR wrappers, non-EBM mining context, and the pasted Claude report as `claude_report_user_paste.md`.

9. `source_status/`
   - Inclusion/exclusion status for the sourcing wishlist. Copyrighted AMS/Springer book chapters are logged but not redistributed.

## What is not included

- Full copyrighted AMS/Springer book scans such as *Ramanujan: Letters and Commentary*, Andrews--Berndt *Lost Notebook Part IV*, Berndt *Notebooks Part V*, and Cooper's *Ramanujan's Theta Functions*. See `source_status/RIGHTS_AND_NOT_INCLUDED.md`.
- Trinity/Wren high-resolution IIIF page images. The earlier container could not bulk-crawl those IIIF manifests/images. The downloader and Wren target CSV are included in `phase2_context/`.

## Recommended first agent commands

```bash
python scripts/extract_quarterly_report_text_blocks.py
```

Then review `priority_sources/quarterly_reports/*.operator_blocks.csv` and convert promising rows into the formula-record schema in `phase2_context/formula_record_schema.json`.

For the 1729 target, begin with:

```text
priority_sources/lost_notebook_pages_341_343/
priority_sources/open_access_context_pdfs/ono_trebat_leder_1729_k3_surface_arxiv_1510.00735.pdf
```

For q-continued-fraction registry expansion, begin with:

```text
priority_sources/open_access_context_pdfs/bhatnagar_ramanujans_q_continued_fractions_arxiv_2208.12656.pdf
primary_originals/pdfs/notebooks/notebook*.pdf
```

## Integrity

- `PACK_MANIFEST.csv` has SHA-256 hashes for every file.
- `PDF_MANIFEST.csv` has PDF page counts where `pdfinfo` could read them.
- PDFs are saved as-is; derived `.txt`, `.csv`, and page-image folders are added alongside them.
