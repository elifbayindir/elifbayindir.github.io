"""Shared helper: fetch TrueType versions of the site fonts for image generation.

Pillow and fontTools cannot read the site's woff2 files without brotli, so the
scripts download the matching Fontsource TTF files into tools/.cache/ (git-ignored).
"""

import urllib.request
from pathlib import Path

CACHE = Path(__file__).resolve().parent / ".cache"
SOURCE = "https://cdn.jsdelivr.net/fontsource/fonts/{family}@latest/latin-{style}.ttf"


def font_path(family: str, style: str) -> Path:
    """Return a local TTF path, e.g. font_path("source-serif-4", "500-normal")."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"{family}-latin-{style}.ttf"
    if not path.exists():
        urllib.request.urlretrieve(SOURCE.format(family=family, style=style), path)
    return path
