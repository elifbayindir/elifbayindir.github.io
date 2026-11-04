#!/usr/bin/env python3
"""Generate the Open Graph image assets/img/og-image.png (1200×630).

White background, the name in Source Serif 4 500, a thin steel-blue rule and
"Research · Projects · Publications" in Inter, muted. No photo.

Usage (from the repo root):
    python3 tools/make_og_image.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from fonts import font_path

WIDTH, HEIGHT = 1200, 630
BACKGROUND = "#FFFFFF"
HEADING = "#1F1F1F"
MUTED = "#767676"
ACCENT = "#2C5E7C"
MARGIN = 96
OUTPUT = Path("assets/img/og-image.png")


def main() -> None:
    serif = ImageFont.truetype(str(font_path("source-serif-4", "500-normal")), 96)
    sans = ImageFont.truetype(str(font_path("inter", "400-normal")), 34)

    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    name_top = 214
    draw.text((MARGIN, name_top), "Elif Bayındır", font=serif, fill=HEADING)
    name_bottom = name_top + serif.getbbox("Elif Bayındır")[3]

    rule_y = name_bottom + 40
    draw.rectangle((MARGIN, rule_y, MARGIN + 120, rule_y + 2), fill=ACCENT)

    draw.text((MARGIN, rule_y + 38), "Research · Projects · Publications", font=sans, fill=MUTED)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, "PNG", optimize=True)
    print(f"{OUTPUT}  {OUTPUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
