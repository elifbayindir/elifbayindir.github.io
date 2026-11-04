#!/usr/bin/env python3
"""Prepare photos for the website.

For every image in SOURCE_DIR this script:
  - applies the camera orientation, then drops all metadata (EXIF, GPS, XMP, ICC),
  - writes a full-size copy (long edge 1600 px) to OUTPUT_DIR/<name>.jpg,
  - writes a thumbnail (long edge 800 px) to OUTPUT_DIR/thumbs/<name>.jpg,
  - saves both as progressive JPEG, quality ~80 (lower, down to 65, if a file
    stays over 400 KB full / 150 KB thumb), and prints their sizes.

Usage:
    python3 tools/optimise_images.py SOURCE_DIR [OUTPUT_DIR]

OUTPUT_DIR defaults to assets/img/gallery. Keep SOURCE_DIR out of git
(Website_Photos/ and tools/originals/ are already in .gitignore).
Requires Pillow: python3 -m pip install Pillow
"""

import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

FULL_EDGE = 1600
THUMB_EDGE = 800
QUALITY = 80
MIN_QUALITY = 65
FULL_TARGET_KB = 400
THUMB_TARGET_KB = 150
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff"}


def web_name(path: Path) -> str:
    """Lower-case file name with only letters, digits and hyphens."""
    stem = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
    return f"{stem}.jpg"


def save_resized(image: Image.Image, long_edge: int, target: Path, target_kb: int) -> int:
    copy = image.copy()
    copy.thumbnail((long_edge, long_edge), Image.LANCZOS)
    # A fresh image carries no metadata at all.
    clean = Image.new("RGB", copy.size)
    clean.paste(copy)
    # Lower the quality step by step for detailed photos that stay over target.
    for quality in range(QUALITY, MIN_QUALITY - 1, -5):
        clean.save(target, "JPEG", quality=quality, optimize=True, progressive=True)
        if target.stat().st_size // 1024 <= target_kb:
            break
    return target.stat().st_size // 1024


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    source = Path(sys.argv[1])
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("assets/img/gallery")
    thumbs = output / "thumbs"
    thumbs.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in source.iterdir() if p.suffix.lower() in EXTENSIONS)
    if not files:
        sys.exit(f"No images found in {source}")

    for path in files:
        with Image.open(path) as original:
            image = ImageOps.exif_transpose(original).convert("RGB")
        name = web_name(path)
        full_kb = save_resized(image, FULL_EDGE, output / name, FULL_TARGET_KB)
        thumb_kb = save_resized(image, THUMB_EDGE, thumbs / name, THUMB_TARGET_KB)
        warn = ""
        if full_kb > FULL_TARGET_KB or thumb_kb > THUMB_TARGET_KB:
            warn = "  (over target)"
        print(f"{name:40s} full {full_kb:4d} KB   thumb {thumb_kb:4d} KB{warn}")


if __name__ == "__main__":
    main()
