"""Generate structure spacing overrides into kubejs/data/<ns>/worldgen/structure_set/ (DESIGN.md §4.8).

A structure set places at most one of its structures per grid cell of `spacing` chunks (at least `separation` chunks
apart). Every mod's sets are placed independently, so with this many structure mods they pile up next to each other.
For every set matched in SPREAD we write an override at the SAME id (KubeJS data loads after mods) with both numbers
multiplied. Spacing x2 leaves about a quarter as many structures, x1.5 about 44%.

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

# Structure set id or whole namespace -> spacing multiplier; a full id beats its namespace, and None keeps a set as is.
# Surface structures get x2, gyms x1.5 (they hold the leaders until the hub is built). Left alone: underground sets (no surface clutter), sets that are already rare, the
# gyms players must find (Blackthorn, Kanto League), Terralith's fortified villages, and everything not listed
# (vanilla, strongholds, YUNG's, Pokécenters/PokéStops/Labs).
SPREAD = {
    "dungeons_arise": 2.0,  # huge dungeons that showed up everywhere
    "cobblemonextrastructures": 2.0,
    "cobblemon": 2.0,
    "cobblemon:ruins/avoid_trial_chambers": None,  # cave ruins
    "cobblemon:shipwreck_coves": None,  # every 100 chunks already
    "terralith": 2.0,
    "terralith:underground": None,
    "terralith:underground_dungeon": None,
    "terralith:rare_village": None,
    "rgs": 1.5,  # the 7 Kanto gyms, each every 32 chunks; gym buildings contain their leader
    "rgs:blackthorn_gym": None,  # Clair (Stage 8) has to be found
    "rgs:kanto_league": None,
    "legendarymonuments:distortion_portal": 2.0,  # the rest are rare already
    "mega_showdown": 2.0,
    "mega_showdown:mega_site": None,  # underground
    "supplementaries": 2.0,  # galleons and road signs
}


def factor_for(set_id):
    if set_id in SPREAD:
        return SPREAD[set_id]
    return SPREAD.get(set_id.split(":", 1)[0])


def main():
    mods = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODS
    for ns in {key.split(":", 1)[0] for key in SPREAD}:
        shutil.rmtree(DATA / ns / "worldgen" / "structure_set", ignore_errors=True)

    written = 0
    for f in sorted(f for f in os.listdir(mods) if f.endswith(".jar")):
        z = zipfile.ZipFile(os.path.join(mods, f))
        for n in z.namelist():
            parts = n.split("/")
            if len(parts) < 5 or parts[0] != "data" or parts[2:4] != ["worldgen", "structure_set"]:
                continue
            set_id = f"{parts[1]}:{'/'.join(parts[4:])[:-5]}"
            factor = factor_for(set_id)
            if factor is None or not n.endswith(".json"):
                continue
            structure_set = json.loads(z.read(n).decode("utf-8-sig"))
            placement = structure_set.get("placement", {})
            if "spacing" not in placement:
                continue
            placement["spacing"] = round(placement["spacing"] * factor)
            placement["separation"] = min(round(placement.get("separation", 0) * factor), placement["spacing"] - 1)
            out = DATA / n[len("data/"):]
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(structure_set, indent=2) + "\n")
            written += 1
            print(f"  {set_id}  spacing {placement['spacing']}, separation {placement['separation']}")
    print(f"wrote {written} structure set overrides")


if __name__ == "__main__":
    main()
