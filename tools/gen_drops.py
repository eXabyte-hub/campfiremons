"""Generate Pokémon drop fixes (DESIGN.md §4.8) into kubejs/data/<ns>/species_additions/.

Cobblemon's species_additions *replace* a species' drop table (only forms/evolutions append). Cobblemon Armory,
Legendary Monuments and Mega Showdown ship additions that set drops, which wipes those species' normal drops
(feathers, porkchop, scutes …). With vanilla farm animals removed we need those drops, so for every such file we
write an override at the SAME id (KubeJS data loads after mods) whose drops = original Cobblemon drops + the mod's.
We also add eggs to a few common birds (only the Chansey and Exeggcute lines drop eggs otherwise).

    python -I tools/gen_drops.py [path/to/mods]
Re-run after updating Cobblemon or any mod that ships species_additions.
"""
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "kubejs" / "data"
DEFAULT_MODS = os.path.expanduser("~/.local/share/PrismLauncher/instances/Campfiremons Dev/minecraft/mods")
EGG = {"item": "minecraft:egg", "percentage": 35.0, "quantityRange": "1-2"}
EGG_LAYERS = ["pidgey", "pidgeotto", "pidgeot", "spearow", "fearow", "starly", "staravia", "staraptor", "fletchling"]


def amount(drops):
    a = drops.get("amount", 1)
    if isinstance(a, str) and "-" in a:
        return tuple(int(x) for x in a.split("-", 1))
    return (int(a), int(a))


def merged(original, extra):
    lo1, hi1 = amount(original)
    lo2, hi2 = amount(extra)
    out = {"entries": original.get("entries", []) + extra.get("entries", [])}
    out["amount"] = lo1 + lo2 if (lo1, hi1) == (hi1, hi1) and lo2 == hi2 else f"{lo1 + lo2}-{hi1 + hi2}"
    return out


def main():
    mods = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODS
    jars = sorted(f for f in os.listdir(mods) if f.endswith(".jar"))
    cobblemon = zipfile.ZipFile(os.path.join(mods, next(f for f in jars if f.startswith("Cobblemon-neoforge"))))
    original = {}
    for n in cobblemon.namelist():
        if n.startswith("data/cobblemon/species/") and n.endswith(".json"):
            original[n.rsplit("/", 1)[1][:-5]] = json.loads(cobblemon.read(n)).get("drops") or {"amount": 0, "entries": []}

    # Clear previous output (our egg files and every override we wrote last time)
    for ns_dir in DATA.iterdir():
        shutil.rmtree(ns_dir / "species_additions", ignore_errors=True)

    overridden = set()
    for f in jars:
        z = zipfile.ZipFile(os.path.join(mods, f))
        for n in z.namelist():
            if "/species_additions/" not in n or not n.endswith(".json") or not n.startswith("data/"):
                continue
            addition = json.loads(z.read(n))
            if "drops" not in addition:
                continue
            species = addition["target"].split(":", 1)[1]
            addition["drops"] = merged(original.get(species, {"amount": 0, "entries": []}), addition["drops"])
            if species in EGG_LAYERS:
                addition["drops"] = merged(addition["drops"], {"amount": 1, "entries": [EGG]})
            out = DATA / n[len("data/"):]
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(addition, indent=2) + "\n")
            overridden.add(species)

    for species in EGG_LAYERS:
        if species in overridden:
            continue
        out = DATA / "campfiremons" / "species_additions" / f"{species}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"target": f"cobblemon:{species}",
                                   "drops": merged(original[species], {"amount": 1, "entries": [EGG]})}, indent=2) + "\n")
    print(f"restored original drops on {len(overridden)} species overridden by mods; eggs added to {len(EGG_LAYERS)}")


if __name__ == "__main__":
    main()
