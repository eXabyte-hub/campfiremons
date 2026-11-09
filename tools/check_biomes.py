"""Report how well biomes from worldgen mods are covered by Cobblemon spawn tags and RCT trainer biome tags.

Cobblemon spawns by biome tags (#cobblemon:is_forest …); RCT places trainers by tag *paths* in any namespace
(is_cave matches c:is_cave, cobblemon:is_cave, …). A modded biome in no Cobblemon tag gets no Pokémon.

    python -I tools/check_biomes.py [namespace ...]     (default: terralith incendium nullscape)
"""
import glob
import json
import os
import re
import sys
import zipfile
from collections import defaultdict

PRISM = os.path.expanduser("~/.local/share/PrismLauncher")
MODS = f"{PRISM}/instances/Campfiremons Dev/minecraft/mods"
EXTRA_JARS = glob.glob(f"{PRISM}/libraries/net/minecraft/client/1.21.1-*/client-1.21.1-*-extra.jar") + \
    glob.glob(f"{PRISM}/libraries/net/neoforged/neoforge/21.1.*/neoforge-21.1.*-universal.jar")
TAG = re.compile(r"data/([^/]+)/tags/worldgen/biome/(.+)\.json$")
BIOME = re.compile(r"data/([^/]+)/worldgen/biome/(.+)\.json$")


def main():
    namespaces = sys.argv[1:] or ["terralith", "incendium", "nullscape"]
    tags, biomes = defaultdict(set), set()
    for jar in sorted(glob.glob(f"{MODS}/*.jar")) + EXTRA_JARS:
        z = zipfile.ZipFile(jar)
        for n in z.namelist():
            if m := TAG.match(n):
                try:
                    data = json.loads(z.read(n))
                except ValueError:
                    continue
                for v in data.get("values", []):
                    tags[f"{m.group(1)}:{m.group(2)}"].add(v["id"] if isinstance(v, dict) else v)
            elif m := BIOME.match(n):
                biomes.add(f"{m.group(1)}:{m.group(2)}")

    def members(tag, seen=()):
        out = set()
        for v in tags.get(tag, ()):
            if v.startswith("#"):
                if v[1:] not in seen:
                    out |= members(v[1:], seen + (tag,))
            else:
                out.add(v)
        return out

    resolved = {t: members(t) for t in tags}
    rct_paths = set()
    for jar in glob.glob(f"{MODS}/rctmod-*.jar"):
        z = zipfile.ZipFile(jar)
        for n in z.namelist():
            if n.startswith("data/rctmod/mobs/trainers/single/") and n.endswith(".json"):
                rct_paths |= set(json.loads(z.read(n)).get("biomeTagWhitelist", []))

    for ns in namespaces:
        mine = sorted(b for b in biomes if b.startswith(ns + ":"))
        if not mine:
            print(f"== {ns}: no biomes (terrain/structures only)")
            continue
        uncovered, thin = [], []
        rct_hits = defaultdict(int)
        for b in mine:
            cobble = sorted(t.split(":", 1)[1] for t, ms in resolved.items() if t.startswith("cobblemon:") and b in ms)
            if not cobble:
                uncovered.append(b)
            elif len(cobble) <= 2:
                thin.append(f"{b} {cobble}")
            paths = {t.split(":", 1)[1] for t, ms in resolved.items() if b in ms}
            for p in paths & rct_paths:
                rct_hits[p] += 1
        print(f"== {ns}: {len(mine)} biomes; {len(uncovered)} in NO cobblemon tag; {len(thin)} in only 1-2")
        for b in uncovered:
            print(f"   NO SPAWNS  {b}")
        for t in thin[:12]:
            print(f"   thin       {t}")
        print(f"   RCT trainer tags matched: {dict(sorted(rct_hits.items()))}")


if __name__ == "__main__":
    main()
