#!/usr/bin/env python3
"""Wild spawns for the legendaries nothing else in the pack spawns (asked for on 2026-11-28).

Legendary Monuments summons most legendaries; 34 had no source at all (its own quest list marks them unfinished, and
no other mod spawns them). 23 of them get a rare wild spawn here, each tied to its lore: weather, time, moon, place.
The rest: Raid Dens ★6/★7 bosses (kubejs/data/campfiremons/raid/boss/), summon items (legendary_summons.js), and
Silvally by evolving Type: Null.

Every spawn is in the ultra-rare bucket with a fixed `percentage` of that bucket's picks, so a legendary stays rare
even where it's the only ultra-rare that fits (Cobblemon's FlatSelector picks percentage spawns first, then the rest
by weight). They spawn as ordinary wild Pokémon, so the tier locks still apply: throwing a ball at one, or starting
a battle with it, before your stage unlocks its tier is refused (tier_locks.js).

Writes kubejs/data/campfiremons/spawn_pool_world/legendaries.json. Run from the repo root.
"""
import json
from pathlib import Path

OUT = Path("kubejs/data/campfiremons/spawn_pool_world/legendaries.json")

SUB = "55-62"      # Stage 5 sub-legends; the level cap at Stage 5 is 63 to 68
TOP = "68-75"      # Stage 7 mythicals and box legends; the cap at Stage 7 is 79 to 81

# species, level, position, condition, percentage of ultra-rare picks, why
SPAWNS = [
    # Forces of Nature: the weather
    ("tornadus", SUB, "grounded", {"biomes": ["#cobblemon:is_mountain", "#cobblemon:is_hills", "#cobblemon:is_highlands"],
                                   "isRaining": True, "canSeeSky": True}, 12, "rides in on the rain over hills and mountains"),
    ("thundurus", SUB, "grounded", {"biomes": ["#cobblemon:is_mountain", "#cobblemon:is_hills", "#cobblemon:is_plains"],
                                    "isThundering": True, "canSeeSky": True}, 15, "thunderstorms"),
    ("landorus", SUB, "grounded", {"biomes": ["#cobblemon:is_plains", "#cobblemon:is_savanna", "#cobblemon:is_grassland"],
                                   "timeRange": "day", "isRaining": False, "canSeeSky": True}, 6, "clear days on open land"),
    # Tapus: island guardians
    ("tapukoko", SUB, "grounded", {"biomes": ["#cobblemon:is_jungle", "#cobblemon:is_tropical_island"],
                                   "isThundering": True}, 15, "jungle thunderstorms"),
    ("tapulele", SUB, "grounded", {"biomes": ["#cobblemon:is_beach", "#cobblemon:is_tropical_island"],
                                   "timeRange": "dawn"}, 12, "beaches at dawn"),
    ("tapubulu", SUB, "grounded", {"biomes": ["#cobblemon:is_jungle"], "timeRange": "day", "isRaining": False}, 6,
     "jungle by day"),
    ("tapufini", SUB, "surface", {"biomes": ["#cobblemon:is_warm_ocean", "#cobblemon:is_lukewarm_ocean"],
                                  "timeRange": "night"}, 10, "warm seas at night"),
    # Loyal Three and Ogerpon (Kitakami)
    ("okidogi", SUB, "grounded", {"biomes": ["#cobblemon:is_forest", "#cobblemon:is_hills"], "timeRange": "dusk"}, 12,
     "forests and hills at dusk"),
    ("munkidori", SUB, "grounded", {"biomes": ["#cobblemon:is_jungle", "#cobblemon:is_forest"], "timeRange": "night"}, 8,
     "forests at night"),
    ("fezandipiti", SUB, "grounded", {"biomes": ["#cobblemon:is_floral", "#cobblemon:is_grassland"],
                                      "timeRange": "twilight"}, 10, "flower fields at dawn and dusk"),
    ("ogerpon", SUB, "grounded", {"biomes": ["#cobblemon:is_forest"], "timeRange": "night", "isRaining": True}, 15,
     "forests on rainy nights"),
    # Mythicals
    ("jirachi", TOP, "grounded", {"biomes": ["#cobblemon:is_mountain", "#cobblemon:is_hills", "#cobblemon:is_plains"],
                                  "timeRange": "night", "moonPhase": "0", "isRaining": False, "canSeeSky": True}, 8,
     "clear full-moon nights"),
    ("deoxys", TOP, "grounded", {"biomes": ["#cobblemon:is_end"]}, 4, "the End: it fell from space"),
    ("manaphy", TOP, "submerged", {"biomes": ["#cobblemon:is_warm_ocean"]}, 6, "deep in warm seas"),
    ("phione", TOP, "surface", {"biomes": ["#cobblemon:is_warm_ocean", "#cobblemon:is_lukewarm_ocean"]}, 10,
     "drifting on warm seas"),
    ("shaymin", TOP, "grounded", {"biomes": ["#cobblemon:is_floral"], "timeRange": "day", "isRaining": False,
                                  "canSeeSky": True}, 8, "flower fields on clear days"),
    ("diancie", TOP, "grounded", {"biomes": ["#cobblemon:is_overworld"], "canSeeSky": False, "maxY": 32,
                                  "neededNearbyBlocks": ["minecraft:budding_amethyst", "minecraft:amethyst_cluster"]}, 15,
     "deep underground by amethyst geodes"),
    ("volcanion", TOP, "grounded", {"biomes": ["#minecraft:is_nether"]}, 4, "the Nether"),
    ("zeraora", TOP, "grounded", {"biomes": ["#cobblemon:is_plains", "#cobblemon:is_savanna"], "timeRange": "night",
                                  "isThundering": True}, 15, "thunderstorms on the plains at night"),
    ("zarude", TOP, "grounded", {"biomes": ["#cobblemon:is_jungle"]}, 5, "deep jungle"),
    # Weather trio
    ("kyogre", TOP, "surface", {"biomes": ["#cobblemon:is_deep_ocean"], "isThundering": True}, 15,
     "deep ocean in thunderstorms"),
    ("groudon", TOP, "grounded", {"biomes": ["#cobblemon:is_badlands", "#cobblemon:is_volcanic", "#cobblemon:is_desert"],
                                  "timeRange": "day", "isRaining": False, "canSeeSky": True}, 6,
     "badlands, deserts and volcanoes in the midday sun"),
    ("rayquaza", TOP, "grounded", {"biomes": ["#cobblemon:is_peak"], "minY": 160, "canSeeSky": True}, 10,
     "the highest mountain peaks"),
]


def main():
    spawns = []
    for species, level, position, condition, pct, _why in SPAWNS:
        spawns.append({
            "id": f"campfiremons-{species}",
            "pokemon": species,
            "presets": ["water"] if position in ("surface", "submerged") else ["natural"],
            "type": "pokemon",
            "spawnablePositionType": position,
            "bucket": "ultra-rare",
            "level": level,
            "weight": 1.0,
            "percentage": float(pct),
            "condition": condition,
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [],
                               "spawns": spawns}, indent=2) + "\n")
    print(f"{len(spawns)} legendary spawns -> {OUT}")


if __name__ == "__main__":
    main()
