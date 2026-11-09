# Claude handoff

Start with Hunt 5: `priority_sources/quarterly_reports/ramanujan_quarterly_reports_2022_HRJ_Berndt.txt` and `.operator_blocks.csv`. Convert QR manipulations into `formula_record_schema.json` records and tag each formula block with the operator taxonomy.

Next, split agents:

1. 1729/two-cubes/K3: inspect `priority_sources/lost_notebook_pages_341_343/` and compare with `priority_sources/open_access_context_pdfs/ono_trebat_leder_1729_k3_surface_arxiv_1510.00735.pdf`.
2. q-continued fractions: use `priority_sources/open_access_context_pdfs/bhatnagar_ramanujans_q_continued_fractions_arxiv_2208.12656.pdf` to seed registry entries; then map back to original notebook facsimile pages.
3. General operator mining: run OCR/tagging over `primary_originals/page_images/` and compare to `primary_originals/text/` and published-paper PDFs.
4. Trinity/Wren: on an internet-enabled machine, run `phase2_context/wren_ramanujan_downloader.py` with `phase2_context/ramanujan_wren_targets.csv`.

Do not claim novelty until each candidate is classified as classical-known, rediscovered, software-packaging novelty, failure-mode novelty, benchmark novelty, proof novelty, or speculative.
