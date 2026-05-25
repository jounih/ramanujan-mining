#!/usr/bin/env python3
r"""
lit_search.py — lightweight literature search over the local pdftotext corpus.

Usage:
    python corpora/scripts/lit_search.py "level-pq lambert annihilator"
    python corpora/scripts/lit_search.py --regex "Entry\s*4\.2\.3"
    python corpora/scripts/lit_search.py --any "tricomi" "kummer" --context 2

Defaults:
    - Case-insensitive substring search
    - All terms must appear within the same file (use --any for OR)
    - Per-hit one-line context, with file + line number
    - Returns up to --max hits per file (default 5)

Purpose:
    Foundation for the future vector-DB literature-diff. This grep-style
    wrapper handles the keyword-based queries that don't need embeddings:
    identity nicknames, operator names, specific entry numbers, coefficient
    patterns. For semantic/structural search (e.g. "anything that looks like
    a 4-divisor Lambert annihilator"), we'd want embeddings.

Corpus expected at:
    corpora/text/*.txt
"""
import argparse
import re
import sys
from pathlib import Path


CORPUS = Path(__file__).resolve().parent.parent / "text"


def gather_files() -> list[Path]:
    if not CORPUS.exists():
        sys.stderr.write(
            f"error: {CORPUS} does not exist. "
            "Run pdftotext over downloaded-pdfs/ first.\n"
        )
        sys.exit(2)
    return sorted(CORPUS.glob("*.txt"))


def search_file(
    path: Path,
    patterns: list[re.Pattern],
    *,
    require_all: bool,
    max_hits: int,
    context_lines: int,
) -> list[tuple[int, str]]:
    """Return [(line_no, snippet), ...] for hits in this file."""
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception as exc:
        sys.stderr.write(f"warn: {path.name}: {exc}\n")
        return []

    # File-level filter: must contain ALL terms (or ANY)
    file_text = "\n".join(lines)
    matches_each = [bool(p.search(file_text)) for p in patterns]
    if require_all and not all(matches_each):
        return []
    if not require_all and not any(matches_each):
        return []

    hits: list[tuple[int, str]] = []
    seen: set[int] = set()
    for idx, line in enumerate(lines):
        if any(p.search(line) for p in patterns):
            if idx in seen:
                continue
            lo = max(0, idx - context_lines)
            hi = min(len(lines), idx + context_lines + 1)
            snippet = "\n".join(lines[lo:hi])
            hits.append((idx + 1, snippet))
            seen.add(idx)
            if len(hits) >= max_hits:
                break
    return hits


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("terms", nargs="+", help="Search terms (substring match)")
    p.add_argument(
        "--any",
        dest="require_any",
        action="store_true",
        help="Match files containing ANY term (default: ALL)",
    )
    p.add_argument(
        "--regex",
        action="store_true",
        help="Treat terms as regex patterns (default: literal substring, "
        "case-insensitive)",
    )
    p.add_argument(
        "--context",
        type=int,
        default=1,
        help="Lines of context around each hit (default: 1)",
    )
    p.add_argument(
        "--max",
        type=int,
        default=5,
        help="Max hits per file (default: 5)",
    )
    p.add_argument(
        "--files-only",
        action="store_true",
        help="Just list matching files (no snippets)",
    )
    args = p.parse_args()

    if args.regex:
        patterns = [re.compile(t, re.IGNORECASE) for t in args.terms]
    else:
        patterns = [
            re.compile(re.escape(t), re.IGNORECASE) for t in args.terms
        ]

    files = gather_files()
    if not files:
        sys.stderr.write("error: no .txt files in corpus.\n")
        return 2

    total_hits = 0
    matched_files = 0
    for path in files:
        hits = search_file(
            path,
            patterns,
            require_all=not args.require_any,
            max_hits=args.max,
            context_lines=args.context,
        )
        if not hits:
            continue
        matched_files += 1
        print(f"\n=== {path.name} ({len(hits)} hits, capped at --max) ===")
        if args.files_only:
            continue
        for line_no, snippet in hits:
            print(f"L{line_no}:")
            for s_line in snippet.splitlines():
                print(f"  {s_line}")
            total_hits += 1

    boolop = "any" if args.require_any else "all"
    print(
        f"\n[summary] {matched_files}/{len(files)} files matched "
        f"({total_hits} snippets shown); mode={boolop}, "
        f"terms={args.terms!r}",
        file=sys.stderr,
    )
    return 0 if matched_files else 1


if __name__ == "__main__":
    sys.exit(main())
