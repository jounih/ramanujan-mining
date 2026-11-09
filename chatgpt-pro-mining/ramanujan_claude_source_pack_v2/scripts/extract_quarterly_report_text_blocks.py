#!/usr/bin/env python3
"""Create a rough operator-tagging worklist from the Berndt/HRJ Quarterly Reports text.

This is intentionally conservative: it does not claim OCR/LaTeX correctness. It simply
splits the text into paragraph-ish blocks and flags blocks with math/operator cues so
Claude/agents can start Hunt 5 immediately.
"""
from __future__ import annotations
import csv, re, sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / "priority_sources/quarterly_reports/ramanujan_quarterly_reports_2022_HRJ_Berndt.txt"

CUES = {
    "mellin_ramanujan_master_theorem": [r"Γ\(n\)", r"phi\(-n\)", r"coefficient", r"integral", r"x\s*n−1|x\s*n-1"],
    "definite_integral_evaluation": [r"∫|Z ∞|integral", r"cos|sin|Bessel|Gamma|Γ"],
    "series_expansion": [r"expansion", r"powers of x", r"coefficient", r"series"],
    "asymptotic_or_approximation": [r"asymptotic|approximately|approximation|error"],
    "recurrence_or_sequence": [r"u[nₙ]?|u_n|sequence|recurrence|values of n"],
    "continued_fraction": [r"continued fraction|fraction"],
}

def split_blocks(text: str):
    # Preserve report boundaries when visible.
    text = text.replace("\r\n", "\n")
    raw = re.split(r"\n\s*\n+", text)
    for i,b in enumerate(raw):
        b = re.sub(r"[ \t]+", " ", b.strip())
        if len(b) >= 50:
            yield i,b

def tags_for(block: str):
    tags=[]
    for tag, pats in CUES.items():
        hits = sum(1 for p in pats if re.search(p, block, flags=re.I))
        if hits >= 2 or (tag == "continued_fraction" and hits >= 1):
            tags.append(tag)
    return tags

def report_id(block: str, idx: int):
    low=block.lower()
    if "third quarterly" in low or "march" in low:
        return "QR3?"
    if "second quarterly" in low or "7th november" in low:
        return "QR2?"
    if "5th aug" in low or idx < 120:
        return "QR1?"
    return "unknown"

def main(path: Path = DEFAULT, out_csv: Path | None = None):
    text = path.read_text(errors="replace")
    rows=[]
    for idx, block in split_blocks(text):
        tags=tags_for(block)
        if tags:
            rows.append({
                "block_id": f"qr_block_{idx:04d}",
                "rough_report": report_id(block, idx),
                "suggested_operator_tags": ";".join(tags),
                "char_len": len(block),
                "needs_human_check": "yes",
                "snippet": block[:500].replace("\n"," "),
            })
    if out_csv is None:
        out_csv = path.with_suffix(".operator_blocks.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["block_id","rough_report","suggested_operator_tags","char_len","needs_human_check","snippet"])
        w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} rows to {out_csv}")

if __name__ == "__main__":
    p = Path(sys.argv[1]) if len(sys.argv)>1 else DEFAULT
    o = Path(sys.argv[2]) if len(sys.argv)>2 else None
    main(p,o)
