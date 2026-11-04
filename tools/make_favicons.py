#!/usr/bin/env python3
"""Generate the "EB" monogram favicons in steel blue on white.

Writes:
  favicon.svg            vector monogram (letter outlines, no font needed)
  favicon-32.png         32×32 fallback
  apple-touch-icon.png   180×180

Usage (from the repo root):
    python3 tools/make_favicons.py
"""

from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

from fonts import font_path

TEXT = "EB"
ACCENT = "#2C5E7C"
BACKGROUND = "#FFFFFF"
VIEWBOX = 64
TEXT_WIDTH = 46  # monogram width inside the 64-unit square


def svg_monogram(ttf: Path) -> str:
    font = TTFont(ttf)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    names = [cmap[ord(ch)] for ch in TEXT]

    # Measure the combined outline at font units.
    bounds = BoundsPen(glyphs)
    x = 0
    for name in names:
        glyphs[name].draw(TransformPen(bounds, (1, 0, 0, 1, x, 0)))
        x += glyphs[name].width
    xmin, ymin, xmax, ymax = bounds.bounds

    scale = TEXT_WIDTH / (xmax - xmin)
    offset_x = (VIEWBOX - TEXT_WIDTH) / 2 - xmin * scale
    offset_y = (VIEWBOX + (ymax - ymin) * scale) / 2 + ymin * scale

    path = SVGPathPen(glyphs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    x = 0
    for name in names:
        # Flip the y axis (fonts point up, SVG points down).
        transform = (scale, 0, 0, -scale, offset_x + x * scale, offset_y)
        glyphs[name].draw(TransformPen(path, transform))
        x += glyphs[name].width

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEWBOX} {VIEWBOX}">'
        f'<rect width="{VIEWBOX}" height="{VIEWBOX}" rx="10" fill="{BACKGROUND}"/>'
        f'<path fill="{ACCENT}" d="{path.getCommands()}"/></svg>\n'
    )


def png_monogram(ttf: Path, size: int, target: Path) -> None:
    scale = 4  # draw large, then downsample for smooth edges
    canvas = size * scale
    image = Image.new("RGB", (canvas, canvas), BACKGROUND)
    draw = ImageDraw.Draw(image)
    font_size = canvas
    font = ImageFont.truetype(str(ttf), font_size)
    # Shrink the font until the monogram is TEXT_WIDTH/VIEWBOX of the square.
    while font.getbbox(TEXT)[2] - font.getbbox(TEXT)[0] > canvas * TEXT_WIDTH / VIEWBOX:
        font_size -= 2
        font = ImageFont.truetype(str(ttf), font_size)
    left, top, right, bottom = font.getbbox(TEXT)
    position = ((canvas - (right - left)) / 2 - left, (canvas - (bottom - top)) / 2 - top)
    draw.text(position, TEXT, font=font, fill=ACCENT)
    image.resize((size, size), Image.LANCZOS).save(target, "PNG", optimize=True)


def main() -> None:
    ttf = font_path("source-serif-4", "500-normal")
    Path("favicon.svg").write_text(svg_monogram(ttf))
    png_monogram(ttf, 32, Path("favicon-32.png"))
    png_monogram(ttf, 180, Path("apple-touch-icon.png"))
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png"):
        print(f"{name:22s} {Path(name).stat().st_size} bytes")


if __name__ == "__main__":
    main()
