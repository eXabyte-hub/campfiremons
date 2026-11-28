#!/usr/bin/env python3
"""Draws the Jade Orb item texture (16x16, our own art): a jade sphere with a darker rim, a soft glow and a highlight.
Writes kubejs/assets/campfiremons/textures/item/jade_orb.png. Run from the repo root."""
import math
from PIL import Image

N = 16
img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
cx = cy = 7.5
R = 6.6
light = (-0.45, -0.55, 0.70)  # from the upper left, towards the viewer
for y in range(N):
    for x in range(N):
        dx, dy = (x - cx) / R, (y - cy) / R
        d2 = dx * dx + dy * dy
        if d2 > 1.0:
            continue
        dz = math.sqrt(1.0 - d2)
        shade = max(0.0, dx * light[0] + dy * light[1] + dz * light[2])
        t = 0.25 + 0.75 * shade
        # jade: deep green to pale mint
        r = int(20 + 120 * t ** 1.6)
        g = int(90 + 150 * t)
        b = int(60 + 110 * t ** 1.3)
        if d2 > 0.78:  # rim
            r, g, b = int(r * 0.55), int(g * 0.6), int(b * 0.55)
        img.putpixel((x, y), (min(r, 255), min(g, 255), min(b, 255), 255))
for x, y in ((5, 4), (6, 4), (5, 5)):  # highlight
    img.putpixel((x, y), (235, 255, 240, 255))
img.save("kubejs/assets/campfiremons/textures/item/jade_orb.png")
print("wrote kubejs/assets/campfiremons/textures/item/jade_orb.png")
