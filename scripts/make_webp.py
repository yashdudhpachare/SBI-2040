#!/usr/bin/env python3
"""Generate WebP chapter images from JPG sources."""
from pathlib import Path

from PIL import Image


def main() -> None:
    src_dir = Path("public/board")
    # full.jpg is a tall reference export that exceeds WebP's 16383px limit.
    jpgs = [p for p in sorted(src_dir.glob("*.jpg")) if p.name != "full.jpg"]
    for jpg in jpgs:
        webp = jpg.with_suffix(".webp")
        with Image.open(jpg) as im:
            im.save(webp, "WEBP", quality=82, method=6)
        print(f"{jpg.name} -> {webp.name}")


if __name__ == "__main__":
    main()
