"""Generate structure spacing overrides into kubejs/data/<ns>/worldgen/structure_set/ (DESIGN.md §4.8).

A structure set places at most one of its structures per grid cell of `spacing` chunks (at least `separation` chunks
apart). For every set in a namespace listed in SPREAD, we write an override at the SAME id (KubeJS data loads after
mods) with both numbers multiplied. Spacing x2 leaves about a quarter as many structures, x1.25 about two-thirds.

    python -I tools/gen_structure_spacing.py [path/to/mods]
Re-run after updating a mod listed in SPREAD. Only affects chunks generated after the change.
"""
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "kubejs" / "data"
DEFAULT_MODS = os.path.expanduser("~/.local/share/PrismLauncher/instances/Campfiremons Dev/minecraft/mods")

# Structure set namespace -> spacing multiplier. Progression structures (Cobblemon ruins, Mega Showdown sites,
# Legendary Monuments, Radical Gyms) are deliberately left alone: they hold stage finds and gyms.
SPREAD = {
    "dungeons_arise": 2.0,  # huge dungeons that showed up everywhere
    "cobblemonextrastructures": 1.25,  # 18 small buildings, most every 30 chunks
}


def main():
    mods = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODS
    for ns in SPREAD:
        shutil.rmtree(DATA / ns / "worldgen" / "structure_set", ignore_errors=True)

    written = 0
    for f in sorted(f for f in os.listdir(mods) if f.endswith(".jar")):
        z = zipfile.ZipFile(os.path.join(mods, f))
        for n in z.namelist():
            parts = n.split("/")
            if len(parts) < 5 or parts[0] != "data" or parts[2:4] != ["worldgen", "structure_set"]:
                continue
            if parts[1] not in SPREAD or not n.endswith(".json"):
                continue
            structure_set = json.loads(z.read(n).decode("utf-8-sig"))
            placement = structure_set.get("placement", {})
            if "spacing" not in placement:
                continue
            factor = SPREAD[parts[1]]
            placement["spacing"] = round(placement["spacing"] * factor)
            placement["separation"] = min(round(placement.get("separation", 0) * factor), placement["spacing"] - 1)
            out = DATA / n[len("data/"):]
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(structure_set, indent=2) + "\n")
            written += 1
            print(f"  {parts[1]}:{'/'.join(parts[4:])[:-5]}  spacing {placement['spacing']}, separation {placement['separation']}")
    print(f"wrote {written} structure set overrides")


if __name__ == "__main__":
    main()
