#!/usr/bin/env python3
"""Draws the Diamond-Tipped Crushing Wheel's plate texture from scratch.

Create's wheel model (an OBJ we only reference, never copy: Create's art is All Rights Reserved) maps its
"plates" texture like this, in pixels of a 16x16 image:
  columns 0-6, rows 2-13   the outer crushing face of each plate
  columns 0-6, rows 0-1 and 14-15   the plate's top and bottom edges
  column 15                the plate's sides (its leading and trailing edges as the wheel turns)
Everything here is our own pixels, made to look like real diamond tooling: a dark steel plate with six 2x2 diamond
cutters set into the crushing face in staggered rows (like the cutters on a diamond drill bit; 2x2 so they still show
from a distance, where single-pixel specks blur away), and diamond inserts along the plate's sides.

Run from anywhere: python3 tools/mod/gen_texture.py
"""
from pathlib import Path

from PIL import Image

OUT = Path(__file__).parent / 'src/main/resources/assets/campfiremons/textures/block/diamond_tipped_crushing_wheel_plates.png'

STEEL = [(0x5f, 0x64, 0x6c), (0x68, 0x6d, 0x75), (0x71, 0x76, 0x7e)]
STEEL_DARK = (0x47, 0x4b, 0x52)
STEEL_EDGE = (0x38, 0x3b, 0x41)
SHINE = (0xf0, 0xff, 0xfc)
LIGHT = (0x9c, 0xf6, 0xe8)
MID = (0x4f, 0xd8, 0xc6)
DARK = (0x2b, 0x9e, 0x91)

# Top-left corners of the 2x2 diamond cutters on the crushing face: (column, row), in staggered rows.
CUTTERS = [(1, 3), (4, 3), (2, 7), (5, 7), (1, 11), (4, 11)]


def steel(x, y):
    # A fixed brushed-metal pattern (no randomness, so the file is reproducible).
    return STEEL[(x * 3 + y * 5 + (x * y) % 3) % 3]


def main():
    im = Image.new('RGBA', (16, 16))
    px = im.load()

    def put(x, y, c):
        px[x, y] = c + (255,)

    for y in range(16):
        for x in range(16):
            put(x, y, steel(x, y))
    # Plate border, and the plate sides in column 15.
    for y in range(16):
        put(7, y, STEEL_EDGE)
        put(14, y, STEEL_EDGE)
        put(15, y, STEEL_DARK)
    # Crushing face: each cutter is lit from the top left, so it reads as a raised facet set into the steel.
    for x, y in CUTTERS:
        put(x, y, SHINE)
        put(x + 1, y, LIGHT)
        put(x, y + 1, MID)
        put(x + 1, y + 1, DARK)
    # Sides (leading and trailing edges): a diamond insert every third row.
    for y in range(2, 14):
        put(15, y, MID if y % 3 == 0 else STEEL_DARK)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT)
    print(OUT)


if __name__ == '__main__':
    main()
