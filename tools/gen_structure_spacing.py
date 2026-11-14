"""Generate Campfiremons' structure placement into kubejs/data/ (DESIGN.md §4.8).

Minecraft places each structure set on its own grid, one structure per cell, and every mod brings its own sets. With
this many structure mods the grids overlap at random, so ruins, dungeons, Pokécenters and villages pile up next to each
other however far each set is spread out. Only one structure can generate per cell of a single set, so this tool puts
the common overworld surface structures into ONE set, `campfiremons:surface_structures` (the shared grid):

- Each structure's weight is its current frequency (the mod's spacing, times RARER) and its share of its old set in
  the biomes it can generate in, so the mix of what you find stays the same.
- A weighted `campfiremons:empty_cell` (a one-block structure that places nothing) keeps cells empty. Where few
  structures fit the biome it usually wins, so no biome gets more structures than before. Dense biomes such as
  desert and ocean are capped at one per cell.
- Cells are SPACING chunks wide, and two structures in neighbouring cells are always more than SEPARATION chunks apart.

Finding a structure on the shared grid (/locate, explorer maps) means generating every cell where it could be, and a
rare one only gets a few of those cells, so a search can stall the server. Structures that maps or mods look up stay
on grids of their own, kept CLEARANCE chunks away from the shared grid's cells (spacing reduced to make up for the
cells they lose): explorer-map destinations, Legendary Monuments (its tracker) and the gyms. Pokécenters, PokéStops
and Poké Labs share a small grid of their own, `campfiremons:services`, kept clear the same way.

The old sets are overridden at the same id (KubeJS data loads after mods). Underground structures and the other
dimensions keep their own sets, spread by RARER.

    python -I tools/gen_structure_spacing.py [path/to/mods]
Re-run after adding or updating a structure mod. Only affects chunks generated after the change.
"""
import json
import math
import shutil
import sys
import tomllib
import zipfile
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "kubejs" / "data"
PRISM = Path.home() / ".local/share/PrismLauncher"
DEFAULT_MODS = PRISM / "instances/Campfiremons Dev/minecraft/mods"

POOL = "campfiremons:surface_structures"
EMPTY = "campfiremons:empty_cell"
SPACING, SEPARATION, SALT = 20, 10, 1460392713  # 320-block cells; neighbours at least 176 blocks apart
SERVICES, SERVICES_SALT = "campfiremons:services", 1460392714
SERVICE_SETS = {"cobblemon_simple_center", "cobblemon_poke_stops", "cobblemon_poke_labs"}
CLEARANCE = 5  # chunks that structures on their own grid keep from every shared-grid cell position

# Spacing multiplier on the mod's own value (x2 = a quarter as often), for the shared-grid weights and the own grids.
# A full id beats its namespace.
RARER = {
    "dungeons_arise": 2.0,
    "cobblemonextrastructures": 2.0,
    "cobblemon": 2.0,
    "cobblemon:shipwreck_coves": 1.0,
    "cobblemon:ruins/avoid_trial_chambers": 1.0,  # cave ruins
    "terralith": 2.0,
    "terralith:rare_village": 1.0,
    "terralith:underground": 1.0,
    "terralith:underground_dungeon": 1.0,
    "mega_showdown": 2.0,
    "mega_showdown:mega_site": 1.0,  # underground
    "supplementaries": 2.0,  # galleons and road signs
    "rgs": 1.5,  # the 7 Kanto gyms, each every 32 chunks; gym buildings contain their leader
    "rgs:blackthorn_gym": 1.0,  # Clair (Stage 8) has to be found
    "rgs:kanto_league": 1.0,
    "legendarymonuments:distortion_portal": 2.0,
}

# Never on the shared grid and not kept clear of it: underground structures, and Supplementaries (its biomes are
# filled in at runtime). Structures that can generate outside the overworld are left out automatically.
NOT_POOLED = {
    "betterdungeons", "betterfortresses", "bettermineshafts", "betterstrongholds", "supplementaries",
    "minecraft:strongholds", "minecraft:mineshafts", "minecraft:buried_treasures", "minecraft:trial_chambers",
    "minecraft:ancient_cities", "cobblemon:ruins/avoid_trial_chambers", "mega_showdown:mega_site",
    "terralith:underground", "terralith:underground_dungeon",
}

# On a grid of their own, kept clear of the shared one: the gyms, Legendary Monuments (its tracker finds them), and
# (found automatically) every set holding a destination of an explorer map from loot or from these vanilla trades.
OWN_GRID = {"rgs", "legendarymonuments"}
MAP_TAGS = ["minecraft:on_woodland_explorer_maps", "minecraft:on_ocean_explorer_maps",
            "minecraft:on_trial_chambers_maps", "minecraft:on_treasure_maps"]


def lookup(table, set_id, default=None):
    if set_id in table:
        return table[set_id]
    return table.get(set_id.split(":", 1)[0], default)


def listed(names, set_id):
    return set_id in names or set_id.split(":", 1)[0] in names


def jars(mods):
    pack = tomllib.loads((REPO / "pack.toml").read_text())["versions"]
    yield PRISM / f"libraries/com/mojang/minecraft/{pack['minecraft']}/minecraft-{pack['minecraft']}-client.jar"
    yield PRISM / f"libraries/net/neoforged/neoforge/{pack['neoforge']}/neoforge-{pack['neoforge']}-universal.jar"
    for meta in sorted((REPO / "mods").glob("*.pw.toml")):  # only the jars the pack ships
        jar = Path(mods) / tomllib.loads(meta.read_text())["filename"]
        if jar.suffix == ".jar":
            if not jar.exists():
                sys.exit(f"{jar} is missing: sync the dev instance first")
            yield jar


def read_data(mods):
    """Tags, biomes, structures, structure sets and map destinations from vanilla, NeoForge, the mods, kubejs/data."""
    tags = {"biome": defaultdict(list), "structure": defaultdict(list)}
    biomes, structures, sets, map_targets = set(), {}, {}, set(MAP_TAGS)

    def find_maps(node):
        if isinstance(node, dict):
            if str(node.get("function", "")).endswith("exploration_map") and "destination" in node:
                map_targets.add(node["destination"].lstrip("#"))
            for v in node.values():
                find_maps(v)
        elif isinstance(node, list):
            for v in node:
                find_maps(v)

    def take(rel, read, from_jar):
        parts = rel.split("/")
        if len(parts) < 3 or not rel.endswith(".json"):
            return
        ns, name = parts[0], lambda skip: f"{parts[0]}:{'/'.join(parts[skip:])[:-5]}"
        if parts[1:3] == ["tags", "worldgen"] and len(parts) > 4 and parts[3] in tags:
            data = json.loads(read())
            key = name(4)
            if data.get("replace"):
                tags[parts[3]][key] = []
            tags[parts[3]][key] += data.get("values", [])
        elif parts[1:3] == ["worldgen", "biome"]:
            biomes.add(name(3))
        elif parts[1:3] == ["worldgen", "structure"]:
            structures[name(3)] = json.loads(read())
        elif parts[1:3] == ["worldgen", "structure_set"] and from_jar:
            sets[name(3)] = json.loads(read())
        elif parts[1] == "loot_table":
            try:
                find_maps(json.loads(read()))
            except ValueError:
                pass

    for jar in jars(mods):
        with zipfile.ZipFile(jar) as z:
            for n in z.namelist():
                if n.startswith("data/"):
                    take(n[5:], lambda n=n: z.read(n).decode("utf-8-sig"), True)
    for path in sorted(DATA.rglob("*.json")):
        take(path.relative_to(DATA).as_posix(), lambda p=path: p.read_text("utf-8-sig"), False)
    return tags, biomes, structures, sets, map_targets


def tag_resolver(tags):
    cache = {}

    def resolve(ref, stack=()):
        if isinstance(ref, dict):  # optional tag entry, or a NeoForge holder set
            kind = ref.get("type", "")
            if kind == "neoforge:and":
                parts = [resolve(v, stack) for v in ref["values"]]
                return set.intersection(*parts) if parts else set()
            if kind == "neoforge:or":
                return resolve(ref["values"], stack)
            if "id" in ref:
                return resolve(ref["id"], stack)
            raise ValueError(f"unhandled holder set {ref}")
        if isinstance(ref, list):
            return set().union(*(resolve(v, stack) for v in ref)) if ref else set()
        if not ref.startswith("#"):
            return {ref}
        tag = ref[1:]
        if tag not in cache:
            cache[tag] = set() if tag in stack else resolve(tags.get(tag, []), stack + (tag,))
        return cache[tag]

    return resolve


def write(rel, data):
    out = DATA / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2) + "\n")


def set_path(set_id):
    ns, name = set_id.split(":", 1)
    return f"{ns}/worldgen/structure_set/{name}.json"


def weigh(entries_by_set, sets, fits):
    """Weight per structure: its set's density x its share of the set, averaged over the biomes it fits."""
    weights, density_now = {}, defaultdict(float)
    for set_id, entries in entries_by_set.items():
        placement = sets[set_id]["placement"]
        density = placement.get("frequency", 1.0) / (placement["spacing"] * lookup(RARER, set_id, 1.0)) ** 2
        for e in entries:
            shares = [e.get("weight", 1) / sum(o.get("weight", 1) for o in entries if b in fits[o["structure"]])
                      for b in fits[e["structure"]]]
            weights[e["structure"]] = weights.get(e["structure"], 0) + density * sum(shares) / len(shares)
        for b in set().union(*(fits[e["structure"]] for e in entries)):
            density_now[b] += density
    return weights, density_now


def main():
    mods = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODS
    tags, present, structures, sets, map_tags = read_data(mods)
    biome_tag, structure_tag = tag_resolver(tags["biome"]), tag_resolver(tags["structure"])

    elsewhere = biome_tag("#minecraft:is_nether") | biome_tag("#minecraft:is_end")
    for b in present:  # biomes of mod dimensions (Ultra Space, raid dens); Legendary Monuments' are in shared tags
        if b.split(":")[0] not in ("minecraft", "terralith", "mythicupgrades", "legendarymonuments"):
            elsewhere.add(b)
    overworld = present - elsewhere - {b for b in present if b.startswith("legendarymonuments:")}
    biomes = {s: biome_tag(st.get("biomes", [])) & present for s, st in structures.items()}
    looked_up = set()
    for t in map_tags:
        looked_up |= structure_tag("#" + t) if t in tags["structure"] else {t}

    # Sort every set: shared grid, services grid, own grid kept clear of the shared one, or left on its own grid.
    pooled, services, leftover, clear_of_pool = {}, {}, {}, set()
    for set_id, structure_set in sorted(sets.items()):
        if structure_set.get("placement", {}).get("type") != "minecraft:random_spread" or listed(NOT_POOLED, set_id):
            continue
        entries = structure_set["structures"]
        joins = [e for e in entries if biomes.get(e["structure"], set()) & overworld
                 and not biomes.get(e["structure"], set()) & elsewhere]
        if not joins:
            continue
        if listed(OWN_GRID, set_id) or any(e["structure"] in looked_up for e in entries):
            clear_of_pool.add(set_id)
        else:
            (services if listed(SERVICE_SETS, set_id) else pooled)[set_id] = joins
            leftover[set_id] = [e for e in entries if e not in joins]

    fits = {s: biomes.get(s, set()) & overworld for s in structures}
    weights, density_now = weigh(pooled, sets, fits)
    empty = 1 / SPACING**2  # as heavy as one full cell: a biome never gets more than it has now
    scale = 20 / min(min(weights.values()), empty)  # smallest weight 20, so rounding stays within 2.5%
    pool_entries = [{"structure": s, "weight": max(1, round(w * scale))} for s, w in sorted(weights.items())]
    pool_entries.append({"structure": EMPTY, "weight": round(empty * scale)})

    keep = math.sqrt(1 - (2 * CLEARANCE + 1) ** 2 / SPACING**2)  # spacing factor that makes up for the lost cells
    service_weights, _ = weigh(services, sets, fits)
    service_spacing = round(keep / math.sqrt(sum(service_weights.values())))
    service_scale = 100 / min(service_weights.values())

    for ns in {s.split(":")[0] for s in sets if s in pooled or s in services or s in clear_of_pool or
               lookup(RARER, s, 1.0) != 1.0}:
        shutil.rmtree(DATA / ns / "worldgen" / "structure_set", ignore_errors=True)
    shutil.rmtree(DATA / "campfiremons" / "worldgen", ignore_errors=True)

    write(set_path(POOL), {"structures": pool_entries, "placement": {
        "type": "minecraft:random_spread", "spacing": SPACING, "separation": SEPARATION, "salt": SALT,
        "spread_type": "triangular"}})
    write(set_path(SERVICES), {
        "structures": [{"structure": s, "weight": round(w * service_scale)} for s, w in sorted(service_weights.items())],
        "placement": {"type": "minecraft:random_spread", "spacing": service_spacing,
                      "separation": service_spacing // 2, "salt": SERVICES_SALT, "spread_type": "triangular",
                      "exclusion_zone": {"other_set": POOL, "chunk_count": CLEARANCE}}})
    every_pooled_biome = set().union(*(biomes[e["structure"]] for e in pool_entries[:-1]))
    write("campfiremons/worldgen/structure/empty_cell.json", {
        "type": "minecraft:jigsaw", "biomes": sorted(every_pooled_biome), "step": "surface_structures",
        "spawn_overrides": {}, "terrain_adaptation": "none", "start_pool": EMPTY, "size": 1,
        "start_height": {"absolute": 0}, "project_start_to_heightmap": "WORLD_SURFACE_WG",
        "max_distance_from_center": 16, "use_expansion_hack": False})
    write("campfiremons/worldgen/template_pool/empty_cell.json", {"fallback": "minecraft:empty", "elements": [
        {"weight": 1, "element": {"element_type": "minecraft:feature_pool_element", "feature": EMPTY,
                                  "projection": "rigid"}}]})
    write("campfiremons/worldgen/placed_feature/empty_cell.json", {"feature": EMPTY, "placement": []})
    write("campfiremons/worldgen/configured_feature/empty_cell.json", {"type": "minecraft:no_op", "config": {}})

    # The old sets: emptied (or left with what can't join), kept clear of the shared grid, or spread by RARER.
    overrides = 0
    for set_id, original in sorted(sets.items()):
        structure_set = json.loads(json.dumps(original))
        placement = structure_set.get("placement", {})
        if "spacing" not in placement:
            continue
        factor = lookup(RARER, set_id, 1.0)
        if set_id in pooled or set_id in services:
            structure_set["structures"] = leftover[set_id]
        if set_id in clear_of_pool:
            factor *= keep
            placement["exclusion_zone"] = {"other_set": POOL, "chunk_count": CLEARANCE}
        if structure_set["structures"] and factor != 1.0:
            placement["spacing"] = round(placement["spacing"] * factor)
            placement["separation"] = min(round(placement.get("separation", 0) * factor), placement["spacing"] - 1)
        if structure_set != original:
            write(set_path(set_id), structure_set)
            overrides += 1

    per_km2 = 1e6 / 256
    def after(b):
        fit = sum(w for s, w in weights.items() if b in fits[s])
        return per_km2 * fit / (fit + empty) / SPACING**2
    print(f"{POOL}: {len(pool_entries) - 1} structures from {len(pooled)} sets, one per {SPACING}x{SPACING} chunks")
    print(f"{SERVICES}: {', '.join(sorted(service_weights))}, one per {service_spacing}x{service_spacing} chunks")
    print(f"own grids kept clear of the shared one: {', '.join(sorted(clear_of_pool))}")
    print(f"{overrides} structure set overrides")
    print("shared-grid structures per km² by biome (now -> after):")
    rows = sorted(overworld, key=lambda b: -density_now[b])
    for b in rows[:4] + [r for r in ("minecraft:desert", "minecraft:plains", "minecraft:forest", "minecraft:taiga",
                                       "minecraft:river") if r in rows[4:]]:
        print(f"  {b:32} {density_now[b] * per_km2:5.1f} -> {after(b):4.1f}")
    nows = sorted(density_now[b] * per_km2 for b in overworld if density_now[b])
    afters = sorted(after(b) for b in overworld if density_now[b])
    print(f"  median biome                     {nows[len(nows) // 2]:5.1f} -> {afters[len(afters) // 2]:4.1f}")


if __name__ == "__main__":
    main()
