# Diary 28 — Chandra runner `--async` ships; expanded OCR audit on LN pp. 342-344 widens the error profile

**Date:** 2026-05-24 (evening)
**Source:** Datalab API outputs from
`corpora/transcriptions/hunt1_lost_notebook_p341_343/out/page-{341,342,343}.md`
(LN reprint pp. 342, 343, 344 per the off-by-one filename mapping from
diary 21); audited against the ground-truth content recorded in diary 21
(Hunt 1 closure inventory).
**Status:** Async runner SHIPS; expanded OCR audit promotes the error
profile from 4 classes (diary 27, n=1) to **6 classes (n=4)** including
two new failure modes that significantly downgrade Chandra 2's
reliability on Ramanujan's hand.

## What I shipped

Updated `corpora/scripts/chandra_api_runner.py` with:

- `--async` flag (uses `AsyncDatalabClient` + asyncio)
- `--concurrency N` flag (default 6; server cap 400)
- Bounded-semaphore concurrent processing via `asyncio.as_completed`,
  so results print/log as each page finishes (not in submission order)
- Same idempotency, dry-run, force, and logging contracts as the sync path

**Smoke-test measurement** (3 pages, concurrency=3):
- Sync (3 pages × ~9s each, prev measurement): would be ~27 s
- Async: **17.4 s wall** for all 3 (limited by the slowest single page)
- Speedup factor at concurrency=3: ~1.55×; expected to be ~5–8× at
  concurrency=10–20 for the full 1,149-page Notebook corpus

The async path is the right tool for the bulk OCR pass when we decide
to do it.

## Expanded OCR audit (n=4 pages now, vs n=1 in diary 27)

I OCR'd pp. 342, 343, 344 of the Lost Notebook (= the 3 follow-up
pages to the 1729 page) via the new async path and audited each
against diary 21's hand-transcribed content. The audit yields a
**significantly worse** Chandra 2 picture than the diary 27 single-page
test suggested:

### Page-by-page summary

| File (LN page) | Diary 21 says it is | Chandra 2 returned | Verdict |
|---|---|---|---|
| `page-340.md` (341) | Three rational functions over `1−82x−82x²+x³` + master `a³+b³=c³±1` + 6 examples | Three rational functions over `1−85x−85x²+x³` + master with garbled adornments + 6 examples with corrupted numerals | DRAFT-USABLE (structure OK; numerals wrong) |
| `page-341.md` (342) | Weber's Results table of `f₁(√−n)` for 15 discriminants | **Hallucinated German text** ("Morera-Beweis", "zu zeigen ist", "schauen wir mal"); invented `f(√(2−s²)) = F_n√s` style modular polynomials; the actual `f₁(√−n)` table content **was not produced at all** | **UNUSABLE — content is fabricated** |
| `page-342.md` (343) | `θ = ⁵√2` and `θ = ⁷√2` blocks with `O(…)` bounds | `θ = √5` (5th root of 2 read as square root of 5); fragmentary `g_min = 0` / Golden-ratio-shaped expressions; no recognizable bound structure | **UNUSABLE — topic mis-identified** |
| `page-343.md` (344) | Denesting identities `η⁵=2`/`η⁵=3` with explicit polynomial identities | Dense `s_n + r_n = ...` expressions; some `√(c+r)` denesting-shaped substructure visible but no specific identity matches diary 21's catalogue; `(87)` Trinity folio number at end correctly preserved | **PARTIAL — denesting-shape preserved but specific identities lost** |

### Expanded error classification (6 classes, n=4 pages)

Original 4 (from diary 27, page-340 audit):
- **A: Digit substitution** — cursive `2↔5`, `7↔1`, `8↔0` (`82 → 85`)
- **B: Exponent-as-subscript** — cube `³` collapses to `_3` systemically
- **C: Phantom adornments** — spurious `w` superscripts, `_2` subscripts
- **D: Letter/digit confusion** — `9 → d`, `i → l`, `8 → S`

New from the expanded audit:
- **E: Language hallucination** ⚠️ — German words ("Morera-Beweis",
  "zu zeigen ist", "schauen wir mal", "d.h.", "s entspricht") inserted
  on a page of Ramanujan's English/mathematical handwriting where no
  such words exist. This is a **content-generation** failure, not a
  recognition failure. Severity: CRITICAL — the output looks plausible
  but is wholly invented.
- **F: Structural hallucination** ⚠️ — a TABLE of Weber class
  invariants `f₁(√−20), f₁(√−27), ...` was read as a paragraph of
  *display equations* with completely different content. The actual
  table data does not appear anywhere in the OCR output. Severity:
  CRITICAL — when the page layout doesn't match Chandra's expected
  "math text" template, the model overconfidently fabricates.
- **G: Radical-degree confusion** — `ⁿ√k` (nth root of k) read as
  `√n` (square root of n, k forgotten). On page-342, `⁵√2` and `⁷√2`
  both came back as `√5` and the 7-degree disappeared. Severity:
  HIGH — silently changes the mathematical content.

## What this changes about the OCR plan

Diary 27 concluded that Chandra 2 was "DRAFT-quality pre-pass" usable
for structural transcription. **That conclusion now needs qualification:**

| Page-type characterisation | Chandra 2 verdict |
|---|---|
| Dense display-math with familiar structure (numbered identities, rational functions, `a³+b³=c³` style) — page-340 was this | DRAFT-USABLE (numerals require review; structure OK) |
| Table of discrete entries with sparse text (Weber class-invariant table, square-root table, modular-polynomial table) — page-341 / page-342 are this | **UNUSABLE — fabricated content** (use Claude-vision-direct or hand transcription instead) |
| Densely nested radicals with multiple symbols — page-343 | PARTIAL — structural shape preserved, specific identities lost |

**Headline operational implication.** Before running the full 1,149-page
Notebook corpus through Chandra, we need a **layout-classifier pre-pass**
that flags table-shaped pages (where Chandra hallucinates) for a
different handler (vision-direct via Claude, hand transcription, or a
table-aware OCR). The current cost model "use Chandra for everything"
is wrong — it will produce convincing-looking garbage on table pages.

## Caveats

- **n=4 is still small.** The 6-class taxonomy is suggestive but not
  definitive. Need ~10-20 more spot-checks across page types to firm up.
- **The hallucinated German is reproducible.** I re-ran page-341 to
  rule out non-determinism; the German text appeared again (same
  "Morera-Beweis" header). Whatever pattern of marks on the page
  triggers this, it's stable.
- **Datalab's `mode="accurate"`** is the highest-accuracy tier
  documented. There is no higher setting to escalate to within the
  public SDK. Further accuracy would require either: (a) a different
  OCR provider for table pages, or (b) feeding Chandra cropped tighter
  bounding boxes of just the equation regions.
- **A bug?** It's possible Chandra 2 was trained with substantial German
  mathematical text in its corpus (the "Morera-Beweis" phrasing is
  classical German complex-analysis textbook style) and over-fits to
  that prior when faced with unfamiliar handwriting. Worth flagging
  upstream if we file a Datalab support ticket.

## Confidence

**High** on the operational pipeline (async path works as advertised).
**Medium-high** on the expanded 6-class error taxonomy (n=4 across
contrasting page-types; one of each major Lost Notebook layout class).
**Very high** on the headline downgrade: Chandra 2 **fabricates** when
shown table pages with Ramanujan's hand; this is a content-safety
issue, not a precision issue.

## Follow-up leads (in priority order)

1. **Write a layout-classifier pre-pass.** Before sending any page to
   Chandra, classify as `dense_display_math` vs `table` vs `mixed`. Only
   the first category gets Chandra; the others get vision-direct or
   hand transcription.
2. **Spot-check ~10 more Notebook pages** across layout types to firm
   up class-E + class-F frequencies. The current `chatgpt-pro-mining/
   .../primary_originals/page_images/lost_notebook/` directory has 379
   facsimile pages; a stratified sample of ~10 would suffice.
3. **File a Datalab support note** about class-E (language
   hallucination) — they may want to know that their model invents
   German on Ramanujan's English/math pages.
4. **For Hunt 4 (class invariants)**: the Weber `f₁(√−n)` table on
   p. 342 is a key Hunt 4 deliverable per diary 21 §"Hidden Hunt 4 /
   Hunt 1 overlap". Since Chandra returned nothing usable, this page
   needs hand transcription or vision-direct read for Hunt 4 to
   progress.
5. **Update H4 on todo.md and CLAUDE.md** to reflect the qualified
   verdict.

## Bottom line

The **`--async` runner ships** and works (3 pages in 17.4 s wall vs
~27 s sequential). The **expanded OCR audit** (n=4 pages, including
3 Hunt 1 / Hunt 4 priority pages) **promotes the error taxonomy from
4 to 6 classes** and adds two critical-severity failure modes:
**language hallucination** (German text on an English/math page) and
**structural hallucination** (tables read as display-math paragraphs
with fabricated content). Chandra 2 is **DRAFT-usable on dense
display-math pages** (page-340-style), but **UNUSABLE without a
layout-aware pre-pass** on table-shaped pages (page-341, page-342
style). The earlier "ready to scale to 1,149 pages" verdict from
diary 27 is **downgraded** to "ready to scale with a layout-classifier
gate". Confidence: high on the operational story, high on the
downgrade.
