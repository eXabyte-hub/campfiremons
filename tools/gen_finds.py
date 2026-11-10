"""Generate the stage "finds" data (DESIGN.md §4.3): power items that start turning up in structure chests once a
player reaches the stage that unlocks them. Edit the config below, run, then `packwiz refresh`.

    python -I tools/gen_finds.py

Writes (all under kubejs/data/, overwriting previous output):
  campfiremons/advancement/stage/{root,1..9}.json   stage advancements: titles/hints, and the RCT gym win that grants each
  campfiremons/advancement/found/<id>.json          "found it" flags for find-once items (inventory_changed)
  campfiremons/loot_table/finds/<id>.json           one-item tables the loot modifiers roll
  campfiremons/loot_modifiers/finds/<id>.json       NeoForge add_table modifiers, gated per player
  neoforge/loot_modifiers/global_loot_modifiers.json
  campfiremons/loot_table/rewards/stage_N.json      direct stage rewards (gym badges, the Master Ball)

Per-player rolls rely on Lootr: each player's chest loot is generated with that player as the loot context.
"""
import json
import shutil
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "kubejs" / "data"

# Structure chests that can hold finds. Villages, the spawn bonus chest and block drops are left out on purpose.
VANILLA = [
    "simple_dungeon", "abandoned_mineshaft", "desert_pyramid", "jungle_temple", "igloo_chest", "pillager_outpost",
    "ruined_portal", "shipwreck_treasure", "shipwreck_supply", "buried_treasure", "underwater_ruin_big",
    "underwater_ruin_small", "stronghold_corridor", "stronghold_crossing", "stronghold_library", "woodland_mansion",
    "ancient_city", "nether_bridge", "bastion_treasure", "bastion_other", "bastion_bridge", "end_city_treasure",
    "trial_chambers/supply", "trial_chambers/corridor", "trial_chambers/intersection", "trial_chambers/entrance",
]
COBBLEMON_RUINS = [
    "base", "ruins", "alluringvoice", "burningjealousy", "chillingwater", "coaching", "corrosivegas", "dracometeor",
    "dragoncheer", "gimmialluringvoice", "grassyglide", "hardpress", "lashout", "meteorbeam", "mistyexplosion",
    "poltergeist", "pounce", "psychicnoise", "risingvoltage", "scaleshot", "scorchingsands", "skydrop", "steelbeam",
    "supercellslam", "telekinesis", "temperflare", "trailblaze", "tripleaxel", "upperhand",
]
CHESTS = (
    [f"minecraft:chests/{c}" for c in VANILLA]
    + [f"cobblemon:ruins/gilded_chests/{c}" for c in COBBLEMON_RUINS]
    + [f"cobblemon:shipwreck_coves/gilded_chests/{c}" for c in
       ("big_treasure_blastburn", "big_treasure_frenzyplant", "big_treasure_hydrocannon", "lesser_treasure")]
    + [f"cobblemon:shipwreck_coves/vanilla_chests/{c}" for c in ("cove1_barrel", "cove1_chest", "cove2_barrel")]
    + ["mega_showdown:archaeological_site/archaeological_site_chest", "mega_showdown:wishing_weald/wishing_weald_chest"]
    + [f"mega_showdown:chests/{c}" for c in
       ("observatory_barrel", "observatory_barrel_2", "observatory_barrel_3", "observatory_chest", "observatory_dome_chest")]
    # Legendary Monuments exploration chests (dojo vaults/spawners and NPC rewards left out)
    + [f"legendarymonuments:chests/{c}" for c in
       ("bell_tower_chest", "calyrex_chest", "dragoeleki_chest", "heatran_cave_chest", "kubfu_dark_chest",
        "kubfu_water_chest", "liberty_island_chest", "lugia_temple_chest", "regice_chest", "regigigas_chest",
        "regirock_chest", "registeel_chest", "swsh_temple_shield", "swsh_temple_sword", "thalic_chest",
        "turnback_cave_chest")]
    # Worldgen structures: YUNG's (Better Mineshafts reuses vanilla's table), When Dungeons Arise treasure chests,
    # Incendium treasure, Terralith's non-village structures
    + [f"betterdungeons:{c}" for c in
       ("skeleton_dungeon/chests/common", "skeleton_dungeon/chests/middle", "small_dungeon/chests/loot_piles",
        "small_nether_dungeon/chests/common", "spider_dungeon/chests/egg_room", "zombie_dungeon/chests/common",
        "zombie_dungeon/chests/special", "zombie_dungeon/chests/tombstone")]
    + [f"betterstrongholds:chests/{c}" for c in
       ("armoury", "common", "crypt", "grand_library", "library_md", "mess", "prison_lg", "trap", "treasure")]
    + [f"betterfortresses:chests/{c}" for c in
       ("beacon", "extra", "hall", "keep", "obsidian", "puzzle", "quarters", "storage", "worship")]
    + [f"dungeons_arise:chests/{c}" for c in
       ("aviary/aviary_treasure", "bandit_towers/bandit_towers_treasure", "ceryneian_hind/ceryneian_hind_treasure",
        "foundry/foundry_treasure", "heavenly_challenger/heavenly_challenger_treasure",
        "heavenly_conqueror/heavenly_conqueror_treasure", "heavenly_rider/heavenly_rider_treasure",
        "illager_corsair/illager_corsair_treasure", "illager_fort/illager_fort_treasure",
        "illager_galley/illager_galley_treasure", "illager_windmill/illager_windmill_treasure",
        "infested_temple/infested_temple_top_treasure", "infested_temple/infested_temple_vault_treasure",
        "jungle_tree_house/jungle_tree_house_treasure", "keep_kayra/keep_kayra_garden_treasure",
        "keep_kayra/keep_kayra_library_treasure", "keep_kayra/keep_kayra_treasure",
        "kisegi_sanctuary/kisegi_sanctuary_treasure", "kisegi_sanctuary/kisegi_sanctuary_vault_normal_treasure",
        "kisegi_sanctuary/kisegi_sanctuary_vault_ominous_treasure", "mechanical_nest/mechanical_nest_treasure",
        "mines_treasure_big", "mines_treasure_medium", "mines_treasure_small",
        "mining_complex/mining_complex_treasure", "mining_system/mining_system_treasure",
        "mushroom_house/mushroom_house_treasure", "mushroom_mines/mushroom_mines_treasure",
        "mushroom_village/mushroom_village_treasure", "plague_asylum/plague_asylum_treasure",
        "scorched_mines/scorched_mines_treasure", "shiraz_palace/shiraz_palace_treasure",
        "small_blimp/small_blimp_treasure", "thornborn_towers/thornborn_towers_top_treasure", "typhon/typhon_treasure",
        "undead_pirate_ship/undead_pirate_ship_treasure")]
    + [f"incendium:{c}" for c in
       ("castle/treasure/quartz", "lab/treasure", "pipeline/base/treasure", "pipeline/treasure",
        "quartz_flats/kitchen_treasure", "quartz_flats/kitchen_extra_treasure", "reactor/office_treasure",
        "reactor/treasure", "sanctum/common_loot", "sanctum/lower_loot")]
    + [f"terralith:{c}" for c in ("mage/treasure", "spire/treasure", "underground/chest")]
    + [f"cobblemonextrastructures:chests/{c}" for c in
       ("berry", "burned_tower", "fishing", "generic_dungeon", "great_dungeon", "pharmacy", "snowpoint_regice",
        "snowpoint_regirock", "snowpoint_registeel", "suerebe")]
    # Poké Labs (rare, 5 chests; the mod names its table in the minecraft namespace). Pokécenters and PokéStops are
    # rest stops, so their chests stay out
    + ["minecraft:chests/common_loot"]
    # Cobbleloots loot balls, opened per player (top-level tables only; their shared/* sub-tables would double-roll)
    + [f"cobbleloots:loot_ball/{c}" for c in
       ("azure", "citrine", "dive", "dusk", "great", "heal", "lure", "luxury", "master", "nest", "net", "poke",
        "premier", "pumpkin", "quick", "rainbow", "roseate", "safari", "slate", "timer", "ultra", "verdant")]
)
WHERE = "structure chests: dungeons, temples, shipwrecks, ruins, strongholds and more"

# once=True: stops appearing for you after it's been in your inventory (match = what counts as "found")
FINDS = [
    dict(id="mega_bracelet", item="mega_showdown:mega_bracelet", match="#mega_showdown:mega_bracelet", name="Mega Bracelet", stage=2, chance=0.25, once=True),
    dict(id="z_ring", item="mega_showdown:z_ring", match="#mega_showdown:z_ring", name="Z-Ring", stage=3, chance=0.25, once=True),
    dict(id="tera_orb", item="mega_showdown:tera_orb", name="Tera Orb", stage=6, chance=0.25, once=True),
    dict(id="dynamax_band", item="mega_showdown:dynamax_band", name="Dynamax Band", stage=7, chance=0.25, once=True),
    dict(id="red_orb", item="mega_showdown:red_orb", name="Red Orb", stage=8, chance=0.25, once=True),
    dict(id="blue_orb", item="mega_showdown:blue_orb", name="Blue Orb", stage=8, chance=0.25, once=True),
    dict(id="rusted_sword", item="mega_showdown:rusted_sword", name="Rusted Sword", stage=8, chance=0.25, once=True),
    dict(id="rusted_shield", item="mega_showdown:rusted_shield", name="Rusted Shield", stage=8, chance=0.25, once=True),
    dict(id="ability_capsule", item="cobblemon:ability_capsule", name="Ability Capsule", stage=8, chance=0.08, once=False),
    dict(id="ability_patch", item="cobblemon:ability_patch", name="Ability Patch", stage=8, chance=0.05, once=False),
]

# Stage advancements. Short title (shown in the toast), description = who to beat + what it unlocks.
STAGES = {
    1: ("Stage 1", "Beat Brock."),
    2: ("Stage 2 · Mega Bracelet", f"Beat Misty. A Mega Bracelet now turns up in {WHERE}."),
    3: ("Stage 3 · Z-Ring", f"Beat Lt. Surge. A Z-Ring now turns up in {WHERE}."),
    4: ("Stage 4", "Beat Erika."),
    5: ("Stage 5 · Sub-legends", "Beat Sabrina. Sub-legendary Pokémon can now be caught."),
    6: ("Stage 6 · Tera Orb, Ultra Beasts", f"Beat Koga. Ultra Beasts and Paradox Pokémon can be caught, and a Tera Orb turns up in {WHERE}."),
    7: ("Stage 7 · Dynamax Band, all legends", f"Beat Blaine. Mythicals and box legends can be caught, and a Dynamax Band turns up in {WHERE}."),
    8: ("Stage 8 · Primal & Crowned", f"Beat Clair. Red and Blue Orbs, the Rusted Sword and Shield, and Ability Capsules and Patches turn up in {WHERE}."),
    9: ("Stage 9: Champion", "Beat the Elite Four and Champion Terry. Reward: a Master Ball."),
}
STAGE_ICONS = ["poke_ball", "great_ball", "ultra_ball", "quick_ball", "dusk_ball", "beast_ball", "luxury_ball", "cherish_ball", "master_ball"]
# Beating this RCT trainer (Radical Red series, IDs from rctmod's own defeat_leader_* advancements) completes the stage
STAGE_TRAINERS = {
    1: ["leader_brock_019e"], 2: ["leader_misty_019f"], 3: ["leader_lt_surge_01a0"], 4: ["leader_erika_01a1"],
    5: ["leader_sabrina_01a4"], 6: ["leader_koga_01a2"], 7: ["leader_blaine_01a3"], 8: ["leader_clair_004a"],
    9: ["champion_terry_01b8", "champion_terry_01b7", "champion_terry_01b6"],
}
# Handed out by the stage advancement itself: the gym's PokeBadges badge (cosmetic) and the Champion's Master Ball
DIRECT_REWARDS = {
    1: ["pokebadges:boulder_kanto_badge", "pokebadges:badge_box"], 2: ["pokebadges:cascade_kanto_badge"],
    3: ["pokebadges:thunder_kanto_badge"], 4: ["pokebadges:rainbow_kanto_badge"], 5: ["pokebadges:marsh_kanto_badge"],
    6: ["pokebadges:soul_kanto_badge"], 7: ["pokebadges:volcano_kanto_badge"], 8: ["pokebadges:rising_johto_badge"],
    9: ["cobblemon:master_ball"],
}


def write(rel, obj):
    p = DATA / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def one_item_table(item):
    return {"type": "minecraft:chest", "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": item}]}]}


def main():
    for d in ("campfiremons/advancement/found", "campfiremons/loot_table/finds", "campfiremons/loot_modifiers",
              "campfiremons/loot_table/rewards"):
        shutil.rmtree(DATA / d, ignore_errors=True)

    write("campfiremons/advancement/stage/root.json", {
        "display": {
            "icon": {"id": "minecraft:campfire"},
            "title": {"text": "Campfiremons League"},
            "description": {"text": "Beat gyms to raise your stage. Each stage unlocks Pokémon to catch and items to find."},
            "background": "minecraft:textures/block/spruce_planks.png",
            "frame": "task", "show_toast": False, "announce_to_chat": False,
        },
        "criteria": {"joined": {"trigger": "minecraft:tick"}},
    })
    for n, (title, desc) in STAGES.items():
        adv = {
            "parent": "campfiremons:stage/root" if n == 1 else f"campfiremons:stage/{n - 1}",
            "display": {
                "icon": {"id": f"cobblemon:{STAGE_ICONS[n - 1]}"},
                "title": {"text": title}, "description": {"text": desc},
                "frame": "challenge" if n == 9 else "goal", "show_toast": True, "announce_to_chat": True,
            },
            # Same condition shape as rctmod's own advancements; /advancement grant still works for testing
            "criteria": {"beat_trainer": {"trigger": "rctmod:defeat_count", "conditions": {
                "count": 1, "entity": {"type": None}, "trainer_ids": STAGE_TRAINERS[n], "trainer_type": None}}},
        }
        if n in DIRECT_REWARDS:
            adv["rewards"] = {"loot": [f"campfiremons:rewards/stage_{n}"]}
            write(f"campfiremons/loot_table/rewards/stage_{n}.json", {
                "type": "minecraft:advancement_reward",
                "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": i}]} for i in DIRECT_REWARDS[n]],
            })
        write(f"campfiremons/advancement/stage/{n}.json", adv)

    chest_condition = {"condition": "minecraft:any_of",
                       "terms": [{"condition": "neoforge:loot_table_id", "loot_table_id": t} for t in CHESTS]}
    modifiers = []
    for f in FINDS:
        required = {f"campfiremons:stage/{f['stage']}": True}
        if f["once"]:
            required[f"campfiremons:found/{f['id']}"] = False
            write(f"campfiremons/advancement/found/{f['id']}.json", {
                "parent": f"campfiremons:stage/{f['stage']}",
                "display": {
                    "icon": {"id": f["item"]},
                    "title": {"text": f["name"]},
                    "description": {"text": f"Find it in {WHERE}."},
                    "frame": "task", "show_toast": True, "announce_to_chat": True,
                },
                "criteria": {"found": {"trigger": "minecraft:inventory_changed",
                                       "conditions": {"items": [{"items": f.get("match", f["item"])}]}}},
            })
        write(f"campfiremons/loot_table/finds/{f['id']}.json", one_item_table(f["item"]))
        write(f"campfiremons/loot_modifiers/finds/{f['id']}.json", {
            "type": "neoforge:add_table",
            "conditions": [
                chest_condition,
                {"condition": "minecraft:entity_properties", "entity": "this",
                 "predicate": {"type_specific": {"type": "minecraft:player", "advancements": required}}},
                {"condition": "minecraft:random_chance", "chance": f["chance"]},
            ],
            "table": f"campfiremons:finds/{f['id']}",
        })
        modifiers.append(f"campfiremons:finds/{f['id']}")

    write("neoforge/loot_modifiers/global_loot_modifiers.json", {"replace": False, "entries": modifiers})
    print(f"{len(FINDS)} finds across {len(CHESTS)} chest tables; {sum(f['once'] for f in FINDS)} find-once items")


if __name__ == "__main__":
    main()
