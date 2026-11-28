#!/usr/bin/env python3
"""Draws the Diamond-Tipped Crushing Wheel's plate texture from scratch.

Create's wheel model (an OBJ we only reference, never copy: Create's art is All Rights Reserved) maps its
"plates" texture like this, in pixels of a 16x16 image:
  columns 0-6, rows 2-13   the outer crushing face of each plate
  columns 0-6, rows 0-1 and 14-15   the plate's top and bottom edges
  column 15                the plate's sides
Everything here is our own pixels: dark steel plates with three diamond tips on each face.

Run from anywhere: python3 tools/mod/gen_texture.py
"""
from pathlib import Path

from PIL import Image

OUT = Path(__file__).parent / 'src/main/resources/assets/campfiremons/textures/block/diamond_tipped_crushing_wheel_plates.png'

STEEL = [(0x6a, 0x6f, 0x77), (0x73, 0x78, 0x80), (0x7c, 0x81, 0x89)]
STEEL_DARK = (0x4b, 0x4f, 0x56)
STEEL_EDGE = (0x3c, 0x3f, 0x45)
SHINE = (0xe6, 0xff, 0xfb)
LIGHT = (0x9c, 0xf6, 0xe8)
MID = (0x4f, 0xd8, 0xc6)
DARK = (0x2b, 0x9e, 0x91)
SHADOW = (0x1c, 0x6b, 0x63)


def steel(x, y):
    # A fixed brushed-metal pattern (no randomness, so the file is reproducible).
    return STEEL[(x * 3 + y * 5 + (x * y) % 3) % 3]


def main():
    im = Image.new('RGBA', (16, 16))
    px = im.load()
    for y in range(16):
        for x in range(16):
            px[x, y] = steel(x, y) + (255,)
    # Plate border: darker right edge, and the plate sides in column 15.
    for y in range(16):
        px[7, y] = STEEL_EDGE + (255,)
        px[15, y] = STEEL_DARK + (255,)
        px[14, y] = STEEL_EDGE + (255,)
    # A thin diamond inlay along the plate's top and bottom edges.
    for x in range(7):
        px[x, 1] = (LIGHT if x % 2 else MID) + (255,)
        px[x, 14] = (MID if x % 2 else DARK) + (255,)
    # Three diamond tips on the crushing face, centred on column 3.
    for cy in (4, 8, 12):
        tip = {
            (2, cy - 1): LIGHT, (3, cy - 1): SHINE, (4, cy - 1): LIGHT,
            (1, cy): DARK, (2, cy): MID, (3, cy): LIGHT, (4, cy): MID, (5, cy): DARK,
            (2, cy + 1): SHADOW, (3, cy + 1): DARK, (4, cy + 1): SHADOW,
        }
        for (x, y), c in tip.items():
            px[x, y] = c + (255,)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT)
    print(OUT)


if __name__ == '__main__':
    main()
