# corpora/oeis_mock_theta/ — Ramanujan mock theta function coefficients (OEIS)

**Source.** OEIS data repository (https://github.com/oeis/oeisdata),
CC BY-SA 4.0 license. Fetched 2026-05-24 via raw GitHub URLs
(`https://raw.githubusercontent.com/oeis/oeisdata/main/seq/A053/A053XXX.seq`).

**Why this is here.** The Wikipedia *Mock modular form* page + OEIS data
together provide the **complete computable spec** for Ramanujan's
mock theta functions — series definitions, working Mathematica code,
asymptotic formulas, and b-files with up to 10,000 coefficients each.
This removes the original Tier-1 "need Hickerson 1988 / Berndt-Chan 2007"
ask from `downloaded-pdfs/README.md`: we can build `rkc/completions.py`
f5/f7/f10 paths directly from this material + Zwegers' open-access PhD
thesis (arXiv:0807.4834) for the shadow / completion theory.

## Contents — 22 Ramanujan mock theta sequences

### Order 5 (12 functions; Hickerson 1988 *Inventiones Math.* 94)

| OEIS | Function | Series |
|---|---|---|
| A053256 | f_0(q) | one of the "first class" of 5th-order |
| A053257 | f_1(q) | |
| A053258 | phi_0(q) | |
| A053259 | phi_1(q) | |
| A053260 | psi_0(q) | |
| A053261 | psi_1(q) | |
| A053262 | chi_0(q) | one of the "second class" of 5th-order |
| A053263 | chi_1(q) | |
| A053264 | F_0(q) | |
| A053265 | F_1(q) | |
| A053266 | Phi(q) | |
| A053267 | Psi(q) | |

### Order 7 (6 functions)

| OEIS | Function | Notes |
|---|---|---|
| A053275 | F_0(q) | one of Ramanujan's 3 canonical 7th-order |
| A053276 | F_1(q) | |
| A053277 | F_2(q) | |
| A053278 | (unnamed 7th-order) | |
| A053279 | (unnamed 7th-order) | |
| A053280 | (unnamed 7th-order) | |

### Order 10 (4 functions; Choi 1999 *Inventiones Math.* 136)

| OEIS | Function | Series |
|---|---|---|
| A053281 | phi(q) | |
| A053282 | psi(q) | |
| A053283 | X(q) | |
| A053284 | chi(q) | `chi(q) = Σ_{n≥0} (−1)ⁿ q^(n+1)² / ((1+q)(1+q²)…(1+q^(2n+1)))` |

## Per-`.seq` file structure (OEIS internal format)

Each file is a small text file (~1-2 KB) with these fields:
- `%I` — sequence ID + revision history
- `%S`, `%T`, `%U` — the first 50-60 coefficients
- `%N` — natural-language description
- `%D` — reference book (often Ramanujan, *Lost Notebook*, p. X)
- `%H` — links to b-files (often 10,000+ coefficients) and papers
- `%F` — formulas (including the explicit q-series)
- `%t` — Mathematica code (port to mpmath trivially)
- `%Y` — cross-references to related sequences
- `%A` — author of the OEIS entry (Hickerson for these)

## Still to add to this directory (if/when needed)

- **Order 3** Ramanujan mock thetas — A000025-area, need to discover exact A-numbers
- **Order 6** mock thetas (Andrews-Hickerson 1991) — A-numbers TBD
- **Order 8** mock thetas (Gordon-McIntosh 1995) — A-numbers TBD

To grab a new sequence by A-number:
```bash
N=053284  # adjust
PREFIX=${N:0:3}
curl -sS -L "https://raw.githubusercontent.com/oeis/oeisdata/main/seq/A${PREFIX}/A${N}.seq" -o A${N}.seq
```

To grab the b-file (high-precision coefficients up to n=10,000):
```bash
# URL is referenced in the %H line of each .seq
curl -sS -L "https://oeis.org/A053284/b053284.txt" -o b053284.txt
# Or via GitHub if mirrored under files/
curl -sS -L "https://raw.githubusercontent.com/oeis/oeisdata/main/files/b053/b053284.txt" -o b053284.txt
```

## Project C / rkc usage

These coefficients are the natural **ground-truth oracle** for the v0.8b
mock-theta completion work (per task #45). Workflow:

1. Port the Mathematica `%t` formula to mpmath `nsum`/`nprod`
2. Verify against the inline `%S/%T/%U` coefficients (first 50)
3. Cross-validate against the b-file (10,000 coefficients) for q values
   near the cusp
4. Use the OEIS asymptotic formula (where given) to verify the
   Zwegers-style completion's leading behavior matches

Result: `rkc/completions.py` gains f5/f7/f10 routes that return numerical
values ≥30 digits with a `MockThetaCompletionCertificate` analogous to
the existing f3 path.
