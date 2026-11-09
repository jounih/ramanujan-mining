# OCR and operator-tagging agent prompt

You are helping build a primary-source formula database for Ramanujan Phase 2.

Input:
- Page image or page image path.
- Page metadata: source collection, page ID, image checksum, rights note if available.
- Optional OCR output from Chandra or another OCR tool.

Tasks:

1. Segment the page into formula blocks.
2. For each formula block, produce a cautious LaTeX transcription.
3. Mark uncertain characters explicitly with `\text{[?]}` or a note; do not silently guess.
4. Assign 1–3 operator tags from the seed taxonomy.
5. For each tag, explain why it applies in one sentence.
6. Identify the input representation and output representation.
7. State the computational gain hypothesis: what becomes cheaper, denser, more stable, or more checkable?
8. Mark verification status: `ocr_only`, `numeric_checked`, `symbolic_checked`, `proved`, `disproved`, or `ambiguous`.
9. Assign an evidence level 0–7.
10. Do not claim novelty. Use `speculative` unless a reference/status check has been performed.

Output format:
JSONL, one formula block per line, matching `schemas/formula_record_schema.json` as closely as possible.

Operator tags available:
- MODULAR_TRANSFORM
- POISSON_THETA_DUAL
- PRODUCT_TO_SERIES
- SERIES_TO_PRODUCT
- SERIES_TO_CONTINUED_FRACTION
- CONTINUED_FRACTION_TO_SERIES
- ASYMPTOTIC_EXTRACTION
- CONGRUENCE_SIEVE
- FINITE_GAUSS_COLLAPSE
- PARAMETER_SPECIALIZATION
- PARAMETER_LIFTING
- RECURRENCE_COMPILER
- PARTIAL_FRACTION_LATENTS
- RAMANUJAN_SUM_PERIODICITY
- ELLIPTIC_AGM_ACCELERATION
- MOCK_MODULAR_COMPLETION
- COMBINATORIAL_BIJECTION_OR_REINDEX
- NUMERICAL_VERIFIER
- UNKNOWN_OPERATOR
- NOT_A_TRANSFORM
