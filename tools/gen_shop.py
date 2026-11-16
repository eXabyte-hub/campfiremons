"""Ship CobbleDollars' default shop config (DESIGN.md §4.5) without items that must only come from progression.

CobbleDollars reads its shop from config/cobbledollars/default_shop.json, writing its built-in defaults there on
first launch (the copy under data/ in its jar is only that template), so we ship the config file itself.

Everything else stays for sale: use-locks (config.js itemLocks) already stop players *using* a ball or cap above
their stage, the same as crafting. The Master Ball (and the Hisuian Origin Ball) is the exception: one per player, from the Champion.

We add a Seeds tab (EXTRA) with Farmer's Delight's four crops: its wild crops only generate in new chunks, and the
server's world around spawn was pregenerated before it was added, so without the shop they'd be chest loot only.

    python -I tools/gen_shop.py [path/to/mods]
Re-run after updating CobbleDollars.
"""
import glob
import json
import os
import sys
import zipfile
from pathlib import Path

SHOP = "data/cobbledollars/cobbledollars/shop/default.json"
OUT = Path(__file__).resolve().parent.parent / "config" / "cobbledollars" / "default_shop.json"
DEFAULT_MODS = os.path.expanduser("~/.local/share/PrismLauncher/instances/Campfiremons Dev/minecraft/mods")
NOT_FOR_SALE = {"cobblemon:master_ball", "cobblemon:ancient_origin_ball"}  # both guaranteed catches
EXTRA = [  # our own tabs, after CobbleDollars' (prices as strings, like its own)
    {"name": "Seeds", "offers": [{"item": f"farmersdelight:{i}", "price": "500"}
                                 for i in ("cabbage_seeds", "tomato_seeds", "onion", "rice")]},
]


def main():
    mods = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODS
    jar = sorted(glob.glob(os.path.join(mods, "CobbleDollars-*.jar")))[-1]
    shop = json.loads(zipfile.ZipFile(jar).read(SHOP))
    removed = 0
    for category in shop:
        before = len(category["offers"])
        category["offers"] = [o for o in category["offers"] if o["item"] not in NOT_FOR_SALE]
        removed += before - len(category["offers"])
    shop += EXTRA
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(shop, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(OUT.parents[2])}: {sum(len(c['offers']) for c in shop)} offers, {removed} removed")


if __name__ == "__main__":
    main()
