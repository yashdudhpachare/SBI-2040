#!/usr/bin/env python3
"""
Render the SBI Branch Modernization case-study board (a single tall PDF page)
into clean per-chapter section slices for the case-study site.

The source PDF (`Wipro Design Task SBI Bank.pdf`) is one page 1920 x 22102 pt.
Section boundaries are expressed in board y-units (pt) and scaled to the
rendered raster. Cut lines sit in the light gaps between sections.

Output: public/board/NN-slug.jpg + manifest.json (+ full.jpg)

Usage:
    python3 scripts/render_board.py [--width 2000] [--jpg-quality 86]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

# (start_y, end_y, slug, label) -- board y-coordinates (pt).
# Boundaries are chosen to fall in the pale gaps between sections so no
# heading or card is clipped.
BANDS = [
    (0,      2150,  "01-overview",   "Overview"),
    (2150,   3180,  "02-research",   "Research"),
    (3180,   5360,  "03-insights",   "Insights"),
    (5360,   7340,  "04-prioritize", "Prioritize"),
    (7340,   8860,  "05-field",      "Field Study"),
    (8860,   11000, "06-interviews", "Interviews"),
    (11000,  13635, "07-personas",   "Personas"),
    (13635,  16950, "08-solutions",  "Solutions"),
    (16950,  19030, "09-experience", "Experience"),
    (19030,  20350, "10-after",      "After"),
    (20350,  22102, "11-roadmap",    "Roadmap"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default="Wipro Design Task SBI Bank.pdf")
    ap.add_argument("--out", default="public/board")
    ap.add_argument("--width", type=int, default=2000, help="rendered raster width in px")
    ap.add_argument("--jpg-quality", type=int, default=86)
    args = ap.parse_args()

    pdf = Path(args.pdf).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf)
    page = doc.load_page(0)
    pw, ph = page.rect.width, page.rect.height
    zoom = args.width / pw
    print(f"-> board {pw:.0f}x{ph:.0f}pt  zoom {zoom:.3f}  raster {args.width}x{round(ph*zoom)}")

    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    full = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    doc.close()

    full_path = out / "full.jpg"
    full.save(full_path, "JPEG", quality=80, optimize=True, progressive=True)
    print(f"   full -> {full_path.name}  ({full_path.stat().st_size//1024} KB)")

    manifest = []
    for sy, ey, slug, label in BANDS:
        top = max(0, round(sy * zoom))
        bot = min(full.height, round(ey * zoom))
        crop = full.crop((0, top, full.width, bot))
        p = out / f"{slug}.jpg"
        crop.save(p, "JPEG", quality=args.jpg_quality, optimize=True, progressive=True)
        manifest.append({"slug": slug, "label": label, "w": crop.width, "h": crop.height})
        print(f"   {slug:14s} {crop.width}x{crop.height}  ({p.stat().st_size//1024} KB)")

    (out / "manifest.json").write_text(json.dumps({"chapters": manifest}, indent=2) + "\n")
    print("done.")


if __name__ == "__main__":
    main()
