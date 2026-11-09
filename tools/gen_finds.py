"""Generate the stage "finds" data (DESIGN.md §4.3): power items that start turning up in structure chests once a
player reaches the stage that unlocks them. Edit the config below, run, then `packwiz refresh`.

    python -I tools/gen_finds.py

Writes (all under kubejs/data/, overwriting previous output):
  campfiremons/advancement/stage/{root,1..9}.json   stage advancements: titles/hints, and the RCT gym win that grants each
  campfiremons/advancement/found/<id>.json          "found it" flags for find-once items (inventory_changed)
  campfiremons/loot_table/finds/<id>.json           one-item tables the loot modifiers roll
  campfiremons/loot_modifiers/finds/<id>.json       NeoForge add_table modifiers, gated per player
  neoforge/loot_modifiers/global_loot_modifiers.json
  campfiremons/loot_table/rewards/stage_9.json      the one direct reward left (Master Ball)

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
DIRECT_REWARDS = {9: ["cobblemon:master_ball"]}


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
