#!/usr/bin/env bash
# Compile all 5 paper bundles in this directory.
# Usage: bash papers/compile_all.sh
#
# Requires: pdflatex + bibtex (or latexmk) on PATH. Install via:
#   brew install texlive             # formula, no sudo
#   brew install --cask basictex     # cask, needs sudo
#   brew install --cask mactex       # cask, full distribution, ~5GB

set -e
cd "$(dirname "$0")"

PAPERS=(
    "ab_entry_423_corrigendum"
    "computational_primitives_tool_paper"
    "level_pq_lambert_annihilator_expository"
    "methodology_workflow_paper"
    "project_c_first_results_short_note"
)

# Detect available compile driver
if command -v latexmk &> /dev/null; then
    COMPILER="latexmk"
    echo "[info] Using latexmk"
elif command -v pdflatex &> /dev/null && command -v bibtex &> /dev/null; then
    COMPILER="manual"
    echo "[info] Using manual pdflatex + bibtex passes"
else
    echo "[error] Neither latexmk nor pdflatex+bibtex found on PATH."
    echo "[error] Install via: brew install texlive"
    exit 2
fi

PASS=0
FAIL=0
RESULTS=()

for paper in "${PAPERS[@]}"; do
    echo ""
    echo "================================================================"
    echo "Compiling: $paper"
    echo "================================================================"

    if [ ! -d "$paper" ]; then
        echo "[skip] $paper directory not found"
        continue
    fi

    cd "$paper"

    if [ "$COMPILER" = "latexmk" ]; then
        if latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex > compile.log 2>&1; then
            PASS=$((PASS + 1))
            RESULTS+=("PASS: $paper -> main.pdf ($(du -h main.pdf 2>/dev/null | cut -f1))")
            echo "[ok] main.pdf generated"
        else
            FAIL=$((FAIL + 1))
            RESULTS+=("FAIL: $paper (see $paper/compile.log)")
            echo "[fail] see compile.log; tail:"
            tail -20 compile.log
        fi
    else
        # Manual: pdflatex, bibtex, pdflatex, pdflatex
        if pdflatex -interaction=nonstopmode -halt-on-error main.tex > pass1.log 2>&1 && \
           bibtex main > bib.log 2>&1 && \
           pdflatex -interaction=nonstopmode -halt-on-error main.tex > pass2.log 2>&1 && \
           pdflatex -interaction=nonstopmode -halt-on-error main.tex > pass3.log 2>&1; then
            PASS=$((PASS + 1))
            RESULTS+=("PASS: $paper -> main.pdf ($(du -h main.pdf 2>/dev/null | cut -f1))")
            echo "[ok] main.pdf generated"
        else
            FAIL=$((FAIL + 1))
            RESULTS+=("FAIL: $paper")
            echo "[fail] see pass*.log; tail of last pass:"
            tail -20 pass3.log 2>/dev/null || tail -20 pass2.log 2>/dev/null || tail -20 pass1.log
        fi
    fi

    cd ..
done

echo ""
echo "================================================================"
echo "SUMMARY: $PASS passed, $FAIL failed"
echo "================================================================"
for r in "${RESULTS[@]}"; do
    echo "  $r"
done

exit $FAIL
