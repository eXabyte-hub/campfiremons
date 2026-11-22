"""Draw the quest book's art (DESIGN.md §3.1, quest book): chapter title banners and the Pokédex panel.

Writes PNGs to kubejs/assets/campfiremons/textures/quests/, which the chapters reference as chapter images
(campfiremons:textures/quests/<name>.png). All drawn here from a system font, nothing taken from other packs.
Re-run after changing a title or colour:
    python -I tools/gen_quest_art.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "kubejs" / "assets" / "campfiremons" / "textures" / "quests"
FONT = "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"

# file name: (title, fill top colour, fill bottom colour). A stage chapter's banner names the badge at its end
# (Stage 1 runs from Brock to Misty: Cascade Badge), since v0.1.44
BANNERS = {
    "getting_started": ("Getting Started", "#ff6b6b", "#c8102e"),
    "evolution": ("Evolution", "#6fa8ff", "#1d4fd8"),
    "gotta_find_em_all": ("Gotta Find 'Em All!", "#ff6b6b", "#c8102e"),
    "archaeology": ("Archaeology", "#ffc35c", "#c46a12"),
    "fishing": ("Fishing", "#7ff0ea", "#138a96"),
    "stage_1": ("Cascade Badge", "#7cc4ff", "#1f6fd1"),
    "stage_2": ("Thunder Badge", "#fff07a", "#d6a10f"),
    "stage_3": ("Rainbow Badge", "#9cf08a", "#2f9e3a"),
    "stage_4": ("Marsh Badge", "#ff9fd0", "#c4377e"),
    "stage_5": ("Soul Badge", "#d9a3ff", "#7a2fc4"),
    "stage_6": ("Volcano Badge", "#ffad5c", "#d1361f"),
    "stage_7": ("Rising Badge", "#a8a2ff", "#4b2fd1"),
    "stage_8": ("Champion", "#fff1a3", "#d6a10f"),
    "stage_9": ("Hall of Fame", "#fff1a3", "#d6a10f"),
    "poke_balls": ("Poké Balls", "#ff6b6b", "#c8102e"),
    "battle_gimmicks": ("Battle Gimmicks", "#a5d8ff", "#2f7fd6"),
    "mega_evolution": ("Mega Evolution", "#a5d8ff", "#2f7fd6"),
    "z_moves": ("Z-Moves", "#fff07a", "#d6a10f"),
    "terastallizing": ("Terastallizing", "#ffa3e0", "#c4379e"),
    "dynamaxing": ("Dynamaxing", "#ff9b7a", "#d1361f"),
    "ultra_beasts": ("Ultra Beasts", "#8ff6ff", "#14a3c4"),
    "paradox": ("Paradox", "#f3a3ff", "#a32fc4"),
    "past": ("Past", "#ff8a7a", "#c4281f"),
    "future": ("Future", "#8ff6ff", "#1f6fd1"),
    "legendary": ("Legendary", "#fff1a3", "#d69a0f"),
    "sub_legendary": ("Sub-Legendary", "#fff1a3", "#d69a0f"),
    "box_legends": ("Box Legends", "#fff1a3", "#d69a0f"),
    "mythical": ("Mythical", "#ffd0f0", "#d65a9a"),
    "artifacts": ("Artifacts", "#8fd8ff", "#1f5fd6"),
    "slot_head": ("Head", "#8fd8ff", "#1f5fd6"),
    "slot_necklace": ("Necklace", "#8fd8ff", "#1f5fd6"),
    "slot_hands": ("Hands", "#8fd8ff", "#1f5fd6"),
    "slot_belt": ("Belt", "#8fd8ff", "#1f5fd6"),
    "slot_feet": ("Feet", "#8fd8ff", "#1f5fd6"),
    "create": ('Create', "#f3c98a", "#8a5a2b"),
    "create_power": ('Rotational Power', "#f3c98a", "#8a5a2b"),
    "create_items": ('Item Logistics', "#f3c98a", "#8a5a2b"),
    "create_fluids": ('Fluid Logistics', "#f3c98a", "#8a5a2b"),
    "create_machines": ('Machines', "#f3c98a", "#8a5a2b"),
    "create_contraptions": ('Contraptions', "#f3c98a", "#8a5a2b"),
    "create_tools": ('Tools', "#f3c98a", "#8a5a2b"),
    "create_trains": ('Trains', "#f3c98a", "#8a5a2b"),
    "create_addons": ('Addons', "#f3c98a", "#8a5a2b"),
    "oritech": ('Oritech', "#eaff9c", "#7fa82a"),
    "oritech_machines": ('Machines', "#eaff9c", "#7fa82a"),
    "oritech_energy": ('Energy', "#c8f0a0", "#4f9a2f"),
    "oritech_logistics": ('Logistics', "#ff9fc8", "#c4285e"),
    "oritech_addons": ('Addons', "#eaff9c", "#7fa82a"),
    "oritech_gear": ('Equipment', "#eaff9c", "#7fa82a"),
    "oritech_reactor": ('Reactor', "#ffc27a", "#d1601f"),
    "storage": ('Storage', "#ffd27a", "#c4741f"),
    "storage_toms": ("Tom's Storage", "#ffd27a", "#c4741f"),
    "storage_rs": ('Refined Storage', "#ffd27a", "#c4741f"),
    "storage_soph": ('Sophisticated Storage', "#ffd27a", "#c4741f"),
    "storage_packs": ('Backpacks', "#ffd27a", "#c4741f"),
    "storage_upgrades": ('Upgrades', "#ffd27a", "#c4741f"),
    "relics": ('Relics', "#ffc98a", "#a0441f"),
    "relic_back": ('Back', "#ffc98a", "#a0441f"),
    "relic_belt": ('Belt', "#ffc98a", "#a0441f"),
    "relic_feet": ('Feet', "#ffc98a", "#a0441f"),
    "relic_head": ('Head', "#ffc98a", "#a0441f"),
    "relic_necklace": ('Necklace & Ring', "#ffc98a", "#a0441f"),
    "relic_other": ('In Hand', "#ffc98a", "#a0441f"),
    "tools_weapons": ('Tools & Weapons', "#eef3f8", "#5f7186"),
    "tier_wood": ('Wood & Gold', "#eef3f8", "#5f7186"),
    "tier_stone": ('Stone', "#eef3f8", "#5f7186"),
    "tier_iron": ('Iron', "#eef3f8", "#5f7186"),
    "tier_diamond": ('Diamond', "#eef3f8", "#5f7186"),
    "tier_netherite": ('Netherite', "#eef3f8", "#5f7186"),
    "pickaxes": ('Pickaxes', "#eef3f8", "#5f7186"),
    "swords": ('Swords', "#eef3f8", "#5f7186"),
    "pokemon_weapons": ('Pokémon Weapons', "#eef3f8", "#5f7186"),
    "armor": ('Armor', "#eef3f8", "#5f7186"),
    "pokemon_armor": ('Pokémon Armor', "#eef3f8", "#5f7186"),
    "shiny_armor": ('Shiny Sets', "#eef3f8", "#5f7186"),
    "trainer_hats": ('Trainer Hats', "#eef3f8", "#5f7186"),
    "mythic_armor": ('Mythic Upgrades', "#eef3f8", "#5f7186"),
    "raids": ('Raid Dens', "#e3a3ff", "#7a2fc4"),
    "training": ('Training', "#ffb3a3", "#d6403a"),
    "train_tms": ('TMs & TRs', "#ffb3a3", "#d6403a"),
    "train_caps": ('Bottle Caps', "#ffb3a3", "#d6403a"),
    "train_mints": ('Mints', "#ffb3a3", "#d6403a"),
    "train_vitamins": ('Vitamins', "#ffb3a3", "#d6403a"),
    "train_candy": ('Candy', "#ffb3a3", "#d6403a"),
    "train_power": ('Power Items', "#ffb3a3", "#d6403a"),
    "train_feathers": ('Feathers', "#ffb3a3", "#d6403a"),
    "building": ('Home & Building', "#c8f0a0", "#4f9a2f"),
    "build_chipped": ('Chipped', "#c8f0a0", "#4f9a2f"),
    "build_rechiseled": ('Rechiseled', "#c8f0a0", "#4f9a2f"),
    "build_handcrafted": ('Handcrafted', "#c8f0a0", "#4f9a2f"),
    "build_framed": ('FramedBlocks', "#c8f0a0", "#4f9a2f"),
    "build_furnies": ('CobbleFurnies', "#c8f0a0", "#4f9a2f"),
    "build_gadgets": ('Building Gadgets', "#c8f0a0", "#4f9a2f"),
    "build_travel": ('Waystones', "#c8f0a0", "#4f9a2f"),
    "dmg_4": ('4 Damage', "#eef3f8", "#5f7186"),
    "dmg_5": ('5 Damage', "#eef3f8", "#5f7186"),
    "dmg_6": ('6 Damage', "#eef3f8", "#5f7186"),
    "dmg_7": ('7 Damage', "#eef3f8", "#5f7186"),
    "dmg_8": ('8 Damage', "#eef3f8", "#5f7186"),
    "dmg_9": ('9 Damage', "#eef3f8", "#5f7186"),
    "armor_7": ('7 Armor', "#eef3f8", "#5f7186"),
    "armor_11": ('11 Armor', "#eef3f8", "#5f7186"),
    "armor_12": ('12 Armor', "#eef3f8", "#5f7186"),
    "armor_15": ('15 Armor', "#eef3f8", "#5f7186"),
    "armor_20": ('20 Armor', "#eef3f8", "#5f7186"),
    "pasture_jobs": ('Pasture Jobs', "#c8f0a0", "#4f9a2f"),
    "jobs_setup": ('Setup', "#c8f0a0", "#4f9a2f"),
    "jobs_farming": ('Farming', "#c8f0a0", "#4f9a2f"),
    "jobs_machines": ('Machines', "#c8f0a0", "#4f9a2f"),
    "jobs_treasure": ('Treasure & Mining', "#c8f0a0", "#4f9a2f"),
    "jobs_helpers": ('Helpers', "#c8f0a0", "#4f9a2f"),
}


def banner(title, top, bottom, size=112):
    font = ImageFont.truetype(FONT, size)
    pad = 28
    left, upper, right, lower = font.getbbox(title)
    w, h = right - left + pad * 2, lower - upper + pad * 2
    origin = (pad - left, pad - upper)

    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text(origin, title, font=font, fill=255)

    def grown(radius):
        return mask.filter(ImageFilter.MaxFilter(radius * 2 + 1))

    def solid(shape):
        """The shape with its enclosed holes (the inside of o, e, a...) filled, so the rims stay outside."""
        outside = Image.eval(shape, lambda v: 0 if v > 127 else 255)
        ImageDraw.floodfill(outside, (0, 0), 128)
        return Image.eval(outside, lambda v: 0 if v == 128 else 255)

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    img.paste((255, 255, 255, 255), (0, 0), solid(grown(11)))  # white outer rim
    img.paste((24, 24, 32, 255), (0, 0), solid(grown(7)))  # dark outline
    gradient = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(gradient)
    a, b = Image.new("RGB", (1, 1), top).getpixel((0, 0)), Image.new("RGB", (1, 1), bottom).getpixel((0, 0))
    for y in range(h):
        t = min(max((y - pad) / max(h - 2 * pad, 1), 0), 1)
        gd.line([(0, y), (w, y)], fill=tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,))
    img.paste(gradient, (0, 0), mask)
    shine = Image.new("L", (w, h), 0)  # a soft highlight across the upper half of the letters
    ImageDraw.Draw(shine).rectangle([0, 0, w, pad + (h - 2 * pad) * 0.42], fill=70)
    img.paste((255, 255, 255, 255), (0, 0), Image.composite(shine, Image.new("L", (w, h), 0), mask))
    return img


def pokedex_panel(w=900, h=760):
    """A Pokédex-style frame: red casing, dark bezel, striped teal screen split in two."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 36, fill="#b3122a", outline="#5c0613", width=8)
    d.rounded_rectangle([18, 18, w - 19, h - 19], 28, outline="#e8384f", width=4)
    d.rounded_rectangle([42, 52, w - 43, h - 43], 22, fill="#20262e")
    sx0, sy0, sx1, sy1 = 58, 70, w - 59, h - 59
    d.rounded_rectangle([sx0, sy0, sx1, sy1], 16, fill="#4fc6d6")
    for i, y in enumerate(range(sy0 + 24, sy1, 44)):
        d.rectangle([sx0 + 6, y, sx1 - 6, y + 18], fill="#62d3e0" if i % 2 else "#43b8c9")
    d.line([(w // 2, sy0 + 10), (w // 2, sy1 - 10)], fill="#2b8f9d", width=6)
    for i, colour in enumerate(("#3ba4ff", "#ffd23b", "#57e05a")):  # indicator lights
        d.ellipse([22, 120 + i * 34, 40, 138 + i * 34], fill=colour, outline="#5c0613", width=2)
    d.rounded_rectangle([w // 2 - 110, 26, w // 2 + 110, 40], 6, fill="#5c0613")
    return img


def wormhole(size=800, seed=7):
    """Ultra Space: a starfield with a spiral of white and violet sparks around a dark centre."""
    import math
    import random
    rnd = random.Random(seed)
    img = Image.new("RGBA", (size, size), (14, 10, 24, 255))
    d = ImageDraw.Draw(img)
    for _ in range(140):  # stars
        x, y, r = rnd.randrange(size), rnd.randrange(size), rnd.choice((1, 1, 2, 3))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, rnd.randrange(120, 255)))
    c = size / 2
    for arm in range(3):  # spiral arms
        for i in range(900):
            t = i / 900
            ang = arm * 2 * math.pi / 3 + t * 4.2 * math.pi
            rad = 70 + t * (size * 0.42) + rnd.uniform(-14, 14)
            x, y = c + math.cos(ang) * rad, c + math.sin(ang) * rad
            colour = (255, 255, 255, 230) if rnd.random() < 0.55 - t * 0.35 else (190, 60, 255, 210)
            r = rnd.choice((2, 3, 3, 4))
            d.ellipse([x - r, y - r, x + r, y + r], fill=colour)
    d.ellipse([c - 60, c - 60, c + 60, c + 60], fill=(8, 4, 16, 255), outline=(200, 160, 255, 255), width=4)
    return img.filter(ImageFilter.SMOOTH)


def crystal_tiles(cols, rows, palette, tile=96):
    """Faceted crystal tiles (the Paradox panels): each tile a diamond lit from the top left."""
    img = Image.new("RGBA", (cols * tile, rows * tile))
    d = ImageDraw.Draw(img)
    for r in range(rows):
        for c in range(cols):
            base = palette[(c + r) % len(palette)]
            rgb = Image.new("RGB", (1, 1), base).getpixel((0, 0))
            light = tuple(min(255, v + 60) for v in rgb)
            dark = tuple(max(0, v - 55) for v in rgb)
            x0, y0, m = c * tile, r * tile, tile // 2
            d.rectangle([x0, y0, x0 + tile - 1, y0 + tile - 1], fill=rgb)
            d.polygon([(x0, y0), (x0 + tile, y0), (x0 + m, y0 + m)], fill=light)
            d.polygon([(x0, y0 + tile), (x0 + tile, y0 + tile), (x0 + m, y0 + m)], fill=dark)
            d.polygon([(x0 + m, y0 + 14), (x0 + tile - 14, y0 + m), (x0 + m, y0 + tile - 14), (x0 + 14, y0 + m)],
                      outline=light, width=4)
            d.rectangle([x0, y0, x0 + tile - 1, y0 + tile - 1], outline=dark, width=2)
    return img


def gold_panel(w=700, h=560):
    """A glowing gold card for the Legendary sections."""
    pad = 30
    img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    glow = Image.new("L", img.size, 0)
    ImageDraw.Draw(glow).rounded_rectangle([pad - 6, pad - 6, w + pad + 6, h + pad + 6], 40, fill=150)
    img.paste((255, 226, 120, 255), (0, 0), glow.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([pad, pad, w + pad, h + pad], 30, fill="#f6e7a6", outline="#3a2c10", width=10)
    d.rounded_rectangle([pad + 16, pad + 16, w + pad - 16, h + pad - 16], 22, outline="#e0c460", width=4)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (title, top, bottom) in BANNERS.items():
        img = banner(title, top, bottom)
        img.save(OUT / f"{name}.png")
        print(f"  {name}.png {img.size[0]}x{img.size[1]}")
    pokedex_panel().save(OUT / "pokedex_panel.png")
    wormhole().save(OUT / "wormhole.png")
    crystal_tiles(5, 2, ["#d93a3a", "#e8508a", "#e8692a", "#c4562a", "#e0a020"]).save(OUT / "past_tiles.png")
    crystal_tiles(5, 2, ["#2f8fe8", "#6a4fe0", "#2fb8e8", "#3a5fd6", "#20c0c0"]).save(OUT / "future_tiles.png")
    gold_panel().save(OUT / "gold_panel.png")
    print("  pokedex_panel, wormhole, past_tiles, future_tiles, gold_panel")


if __name__ == "__main__":
    main()
