#!/usr/bin/env python3
"""
Analyze the rendered SBI board to find clean horizontal cut points.

The SBI board is one tall page on a LIGHT background (white / pale-blue), with
the dark navy cover at the very top. "Ink" here means a pixel that is clearly
darker than the light background OR strongly coloured (cards, headers, images).
Gaps are near-empty light bands between sections -> candidate cut lines.

Prints, in BOARD y-units (pt):
  - "gaps"   : near-empty light bands between content (cut candidates)
  - "blocks" : runs of content

Usage:
    python3 scripts/analyze_bands.py [--width 2000] [--min-gap 24]
"""
from __future__ import annotations
import argparse
from pathlib import Path
import fitz
from PIL import Image
import numpy as np

PDF = Path("Wipro Design Task SBI Bank.pdf").resolve()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=2000)
    ap.add_argument("--min-gap", type=float, default=24)
    args = ap.parse_args()

    doc = fitz.open(PDF)
    page = doc.load_page(0)
    pw = page.rect.width
    zoom = args.width / pw
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    doc.close()

    a = np.asarray(img).astype(np.int16)
    brightness = a.max(axis=2)                 # 0..255
    chroma = a.max(axis=2) - a.min(axis=2)     # colourfulness
    # ink = darker-than-light-bg OR clearly coloured
    ink = (brightness < 210) | (chroma > 38)
    ink_row = ink.mean(axis=1)                 # fraction of inky pixels per row
    EMPTY = 0.012

    empty = ink_row < EMPTY
    h = len(empty)

    def runs(mask):
        out, i = [], 0
        while i < h:
            if mask[i]:
                j = i
                while j < h and mask[j]:
                    j += 1
                out.append((i, j))
                i = j
            else:
                i += 1
        return out

    inv = lambda y: y / zoom

    print(f"-> board {pw:.0f}x{page_h(zoom, h):.0f}pt  zoom {zoom:.3f}  raster {args.width}x{h}")
    print(f"\n== GAPS (empty light bands >= {args.min_gap:.0f}px) ==  (board y)")
    for s, e in runs(empty):
        if e - s >= args.min_gap:
            mid = (s + e) / 2
            print(f"  gap  {inv(s):8.1f} -> {inv(e):8.1f}   mid {inv(mid):8.1f}   (len {inv(e-s):6.1f})")

    print("\n== BLOCKS (content runs >= 120px) ==  (board y)")
    for s, e in runs(~empty):
        if e - s >= 120:
            print(f"  block {inv(s):8.1f} -> {inv(e):8.1f}   (h {inv(e-s):7.1f})")


def page_h(zoom, raster_h):
    return raster_h / zoom


if __name__ == "__main__":
    main()
