#!/usr/bin/env python
"""Render PDF page(s) to PNG so you can LOOK at tables, ticks, diagrams (text extraction loses columns).

    python _kb/tools/pdfpage.py midsem-solutions.pdf 3          # -> _kb/tmp/midsem-solutions_p3.png (and opens it)
    python _kb/tools/pdfpage.py slides.pdf 100 105 --zoom 1.4   # several pages
Page numbers are PDF page numbers (the ones search.py prints), 1-based.
"""
import argparse, os, sys
from pathlib import Path
import fitz

ap = argparse.ArgumentParser()
ap.add_argument("pdf"); ap.add_argument("pages", nargs="+", type=int)
ap.add_argument("--zoom", type=float, default=1.6); ap.add_argument("--no-open", action="store_true")
a = ap.parse_args()
out = Path(__file__).resolve().parent.parent / "tmp"; out.mkdir(exist_ok=True)
doc = fitz.open(a.pdf)
for n in a.pages:
    f = out / f"{Path(a.pdf).stem}_p{n}.png"
    doc[n - 1].get_pixmap(matrix=fitz.Matrix(a.zoom, a.zoom)).save(f)
    print(f)
    if not a.no_open and os.name == "nt":
        os.startfile(f)
