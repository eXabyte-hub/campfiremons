#!/usr/bin/env python3
"""Rewards overhaul (asked for on 2026-11-20): every quest keeps its XP and gains items from its own mod, scaled to the
quest's size, plus CobbleDollars on the bigger ones. Edits the live book in place (rebuild.sh is off: it re-IDs quests).

Every reward gets a new ID, so FTB Quests treats all of them as unclaimed: players keep their quest progress (stored by
quest and task ID) and can claim the new rewards on quests they've already finished (claims are stored by reward ID).
Existing item rewards are kept with their counts doubled.

Size comes from the quest's current XP reward: 1 level is small, 2-3 medium, 4-6 large, 7+ a milestone (gym wins).
Legendary, Paradox and Ultra Beast catches count as large at least. The mod comes from the quest's item tasks, else the
chapter. Nothing here hands out progression-locked items (Master Ball, Ability Capsule, gimmick enablers).

Running it again would re-ID (and so re-open) every reward, so it refuses once the book has CobbleDollars rewards
unless you pass --again.
    python3 tools/quest_book/rewards.py [--again]
"""
import collections
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_book as bb  # noqa: E402
from snbt import Raw, dump, parse  # noqa: E402

Q = bb.Q
LANG = Q / 'lang' / 'en_us.snbt'
MONEY = {1: 0, 2: 500, 3: 2000, 4: 5000}  # CobbleDollars (a Poké Ball costs 2,000 in the shop)
PICKS = {1: 1, 2: 2, 3: 2, 4: 3}  # how many items from the pool
MIN_TIER = {'legendary': 3, 'paradox': 3, 'ultra_beasts': 3}
COIN = 'cobblemon:relic_coin'
KEEP_COUNT = {'cobblemon:master_ball', 'rctmod:trainer_card'}  # one-offs: one Master Ball per player, one trainer card

GEMS = ['mythicupgrades:ruby', 'mythicupgrades:sapphire', 'mythicupgrades:jade', 'mythicupgrades:topaz',
        'mythicupgrades:citrine', 'mythicupgrades:peridot', 'mythicupgrades:aquamarine', 'mythicupgrades:ametrine']
STONES = ['cobblemon:fire_stone', 'cobblemon:water_stone', 'cobblemon:thunder_stone', 'cobblemon:leaf_stone',
          'cobblemon:moon_stone', 'cobblemon:sun_stone', 'cobblemon:dawn_stone', 'cobblemon:dusk_stone',
          'cobblemon:shiny_stone', 'cobblemon:ice_stone']
VITAMINS = ['cobblemon:hp_up', 'cobblemon:protein', 'cobblemon:iron', 'cobblemon:calcium', 'cobblemon:zinc',
            'cobblemon:carbos']

# pool -> tier -> [(item or list to pick one from, count)]
POOLS = {
    'create': {
        1: [('create:andesite_alloy', 16), ('create:shaft', 16), ('create:cogwheel', 8), ('create:zinc_ingot', 8),
            ('create:copper_sheet', 8), ('create:iron_sheet', 8)],
        2: [('create:brass_ingot', 8), ('create:large_cogwheel', 8), ('create:belt_connector', 8),
            ('create:electron_tube', 4), ('create:andesite_casing', 16), ('create:polished_rose_quartz', 4)],
        3: [('create:precision_mechanism', 2), ('create:brass_casing', 16), ('create:sturdy_sheet', 4),
            ('create:electron_tube', 8), ('create:brass_ingot', 16)],
        4: [('create:precision_mechanism', 4), ('create:blaze_cake', 4), ('create:sturdy_sheet', 8),
            ('create:brass_casing', 32)],
    },
    'createaddition': {
        1: [('createaddition:copper_wire', 16), ('createaddition:copper_spool', 4)],
        2: [('createaddition:capacitor', 4), ('oritech:electrum_ingot', 4), ('createaddition:copper_spool', 8)],
        3: [('createaddition:capacitor', 8), ('oritech:electrum_ingot', 8)],
        4: [('createaddition:capacitor', 16), ('oritech:electrum_ingot', 16)],
    },
    'oritech': {
        1: [('oritech:nickel_ingot', 8), ('oritech:raw_nickel', 8), ('oritech:raw_platinum', 4), ('oritech:silicon', 8)],
        2: [('oritech:steel_ingot', 8), ('oritech:magnetic_coil', 4), ('oritech:plastic_sheet', 8),
            ('oritech:electrum_ingot', 8)],
        3: [('oritech:motor', 4), ('oritech:processing_unit', 2), ('oritech:platinum_ingot', 8),
            ('oritech:carbon_fibre_strands', 8), ('oritech:basic_battery', 2)],
        4: [('oritech:advanced_computing_engine', 2), ('oritech:enderic_compound', 8), ('oritech:fluxite', 8),
            ('oritech:adamant_ingot', 4), ('oritech:duratium_ingot', 4)],
    },
    'sophisticatedbackpacks': {
        1: [('sophisticatedbackpacks:upgrade_base', 2)],
        2: [('sophisticatedbackpacks:upgrade_base', 4), ('sophisticatedbackpacks:pickup_upgrade', 1)],
        3: [('sophisticatedbackpacks:stack_upgrade_tier_1', 1), ('sophisticatedbackpacks:upgrade_base', 8)],
        4: [('sophisticatedbackpacks:stack_upgrade_tier_1', 2), ('sophisticatedbackpacks:upgrade_base', 16)],
    },
    'sophisticatedstorage': {
        1: [('sophisticatedstorage:upgrade_base', 2)],
        2: [('sophisticatedstorage:upgrade_base', 4), ('sophisticatedstorage:basic_to_iron_tier_upgrade', 1)],
        3: [('sophisticatedstorage:stack_upgrade_tier_1', 2), ('sophisticatedstorage:upgrade_base', 8)],
        4: [('sophisticatedstorage:stack_upgrade_tier_1', 4), ('sophisticatedstorage:upgrade_base', 16)],
    },
    'refinedstorage': {
        1: [('refinedstorage:quartz_enriched_iron', 8), ('refinedstorage:silicon', 4)],
        2: [('refinedstorage:basic_processor', 4), ('refinedstorage:quartz_enriched_copper', 8)],
        3: [('refinedstorage:improved_processor', 4), ('refinedstorage:1k_storage_part', 2)],
        4: [('refinedstorage:advanced_processor', 4), ('refinedstorage:4k_storage_part', 2)],
    },
    'toms_storage': {
        1: [('toms_storage:inventory_cable', 16)],
        2: [('toms_storage:inventory_cable_connector', 4), ('toms_storage:item_filter', 2)],
        3: [('toms_storage:storage_terminal', 1), ('toms_storage:inventory_cable', 32)],
        4: [('toms_storage:crafting_terminal', 1), ('toms_storage:wireless_terminal', 1)],
    },
    'building': {
        1: [('minecraft:glass', 32), ('minecraft:bricks', 32), ('framedblocks:framed_cube', 16), ('minecraft:lantern', 8)],
        2: [('minecraft:glass', 64), ('waystones:warp_dust', 8), ('framedblocks:framed_cube', 32),
            ('minecraft:quartz_block', 16)],
        3: [('waystones:warp_dust', 16), ('minecraft:quartz_block', 32), ('framedblocks:framed_cube', 64)],
        4: [('waystones:warp_stone', 1), ('minecraft:quartz_block', 64)],
    },
    'gear': {
        1: [('minecraft:iron_ingot', 8), ('minecraft:gold_ingot', 4), ('minecraft:copper_ingot', 16)],
        2: [('minecraft:iron_ingot', 16), ('minecraft:diamond', 2), ('minecraft:lapis_lazuli', 16)],
        3: [('minecraft:diamond', 4), (GEMS, 4), ('minecraft:experience_bottle', 16)],
        4: [('minecraft:netherite_scrap', 2), ('minecraft:netherite_upgrade_smithing_template', 1),
            ('mythicupgrades:necoium_ingot', 2)],
    },
    'artifacts': {
        1: [('minecraft:experience_bottle', 8), ('minecraft:lapis_lazuli', 8)],
        2: [('minecraft:experience_bottle', 16), ('minecraft:gold_ingot', 8)],
        3: [('minecraft:diamond', 2), ('minecraft:experience_bottle', 24)],
        4: [('minecraft:diamond', 4), ('minecraft:emerald', 8)],
    },
    'relics': {
        1: [('relics:relic_experience_bottle', 2)],
        2: [('relics:relic_experience_bottle', 4), ('minecraft:experience_bottle', 8)],
        3: [('relics:relic_experience_bottle', 8), ('minecraft:experience_bottle', 16)],
        4: [('relics:relic_experience_bottle', 16), ('minecraft:diamond', 2)],
    },
    'cobblemon': {
        1: [('cobblemon:poke_ball', 5), ('cobblemon:potion', 3), ('cobblemon:exp_candy_xs', 3)],
        2: [('cobblemon:great_ball', 5), ('cobblemon:super_potion', 3), ('cobblemon:exp_candy_s', 3),
            ('cobblemon:revive', 1)],
        3: [('cobblemon:ultra_ball', 5), ('cobblemon:hyper_potion', 3), ('cobblemon:exp_candy_m', 3),
            ('cobblemon:max_revive', 1)],
        4: [('cobblemon:ultra_ball', 10), ('cobblemon:full_restore', 3), ('cobblemon:exp_candy_l', 3),
            ('cobblemon:rare_candy', 2)],
    },
    'evolution': {
        1: [(STONES, 1), ('cobblemon:exp_candy_xs', 3)],
        2: [(STONES, 2), ('cobblemon:exp_candy_s', 3)],
        3: [(STONES, 2), ('cobblemon:link_cable', 1), ('cobblemon:exp_candy_m', 3)],
        4: [(STONES, 3), ('cobblemon:link_cable', 2), ('cobblemon:exp_candy_l', 3)],
    },
    'ultra_beasts': {
        1: [('cobblemon:beast_ball', 2)],
        2: [('cobblemon:beast_ball', 3), ('cobblemon:hyper_potion', 3)],
        3: [('cobblemon:beast_ball', 5), ('cobblemon:max_revive', 1), ('cobblemon:exp_candy_m', 3)],
        4: [('cobblemon:beast_ball', 10), ('cobblemon:full_restore', 3)],
    },
    'raids': {
        1: [('cobblemonraiddens:raid_shard', 4), ('cobblemonraiddens:cheer_attack', 1)],
        2: [('cobblemonraiddens:raid_shard', 8), ('cobblemonraiddens:cheer_heal', 1),
            ('cobblemonraiddens:cheer_defense', 1)],
        3: [('cobblemonraiddens:raid_shard', 16), ('cobblemonraiddens:raid_pouch', 1)],
        4: [('cobblemonraiddens:raid_shard', 32), ('cobblemonraiddens:raid_pouch', 2)],
    },
    'training': {
        1: [('cobblemon:exp_candy_xs', 3), ('simpletms:tm_blank', 1)],
        2: [(VITAMINS, 2), ('cobblemon:pp_up', 1), ('simpletms:tm_blank', 2)],
        3: [(VITAMINS, 3), ('obc:bottle_cap', 1), ('simpletms:tm_blank', 3)],
        4: [(VITAMINS, 4), ('obc:bottle_cap_gold', 1)],
    },
}
# item namespace -> pool, for quests whose tasks name items
NAMESPACE_POOL = {
    'create': 'create', 'createdeco': 'create', 'copycats': 'create', 'createaddition': 'createaddition',
    'oritech': 'oritech',
    'sophisticatedbackpacks': 'sophisticatedbackpacks', 'sophisticatedstorage': 'sophisticatedstorage',
    'sophisticatedstorageinmotion': 'sophisticatedstorage', 'refinedstorage': 'refinedstorage',
    'toms_storage': 'toms_storage',
    'handcrafted': 'building', 'cobblefurnies': 'building', 'framedblocks': 'building', 'waystones': 'building',
    'chipped': 'building', 'buildinggadgets2': 'building',
    'cobblemonarmory': 'gear', 'mythicupgrades': 'gear',
    'artifacts': 'artifacts', 'relics': 'relics', 'cobblemonraiddens': 'raids',
    'simpletms': 'training', 'obc': 'training',
}
# chapter -> pool, for quests without item tasks (or whose items don't name a pool)
CHAPTER_POOL = {
    'armor': 'gear', 'tools_weapons': 'gear', 'artifacts': 'artifacts', 'relics': 'relics', 'building': 'building',
    'create': 'create', 'oritech': 'oritech', 'storage': 'sophisticatedstorage', 'training': 'training',
    'evolution': 'evolution', 'ultra_beasts': 'ultra_beasts', 'raids': 'raids',
}


def tier(chapter, quest):
    xp = max([int(str(r.get('xp_levels', 0)).rstrip('L')) for r in quest.get('rewards', [])
              if r.get('type') == 'xp_levels'] or [1])
    t = 1 if xp <= 1 else 2 if xp <= 3 else 3 if xp <= 6 else 4
    return max(t, MIN_TIER.get(chapter, 1))


def pool_for(chapter, quest):
    spaces = collections.Counter(str(t['item']['id']).split(':')[0] for t in quest.get('tasks', [])
                                 if t.get('type') == 'item' and isinstance(t.get('item'), dict))
    for ns, _ in spaces.most_common():
        if ns in NAMESPACE_POOL and not (chapter == 'training' and ns == 'cobblemon'):
            return NAMESPACE_POOL[ns]
    return CHAPTER_POOL.get(chapter, 'cobblemon')


def count_of(r):
    return int(str(r.get('count', '1')).rstrip('L'))


def snbt_string(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main():
    chapters = {f: parse(f.read_text()) for f in sorted((Q / 'chapters').glob('*.snbt'))}
    if '--again' not in sys.argv and any(r.get('type') == 'command' and 'cobbledollars' in str(r.get('command', ''))
                                         for ch in chapters.values() for q in ch['quests'] for r in q.get('rewards', [])):
        sys.exit('The book already has the new rewards; --again would re-open every reward for every player')
    for ch in chapters.values():  # every ID in the book, so the new ones can't collide
        bb.USED.add(ch['id'])
        for q in ch['quests']:
            bb.USED.add(q['id'])
            for x in q.get('tasks', []) + q.get('rewards', []):
                bb.USED.add(x['id'])
        for x in ch.get('images', []) + ch.get('quest_links', []):
            bb.USED.add(x['id'])

    titles, stats = {}, collections.Counter()
    for f, ch in chapters.items():
        for q in ch['quests']:
            t, pool = tier(f.stem, q), pool_for(f.stem, q)
            rng = random.Random(int(q['id'], 16))
            new, items = [], collections.OrderedDict()
            for r in q.get('rewards', []):
                if r.get('type') == 'item':
                    item = str(r['item']['id'])
                    # existing item rewards, doubled (except the one-offs)
                    items[item] = items.get(item, 0) + count_of(r) * (1 if item in KEEP_COUNT else 2)
                else:
                    r = dict(r, id=bb.new_id())  # XP and anything else, kept under a new ID
                    new.append(r)
            options = list(POOLS[pool][t])
            rng.shuffle(options)
            for item, n in options[:PICKS[t]]:
                if isinstance(item, list):
                    item = rng.choice(item)
                items[item] = items.get(item, 0) + n
            for item, n in items.items():
                new.append(bb.r_item(item, n))
                stats['items'] += 1
            if MONEY[t]:
                rid = bb.new_id()
                new.append({'command': f'/cobbledollars give @s {MONEY[t]}', 'feedback_message': '',
                            'icon': {'id': COIN}, 'id': rid, 'permission_level': Raw('2'), 'silent': Raw('true'),
                            'type': 'command'})
                titles[f'reward.{rid}.title'] = f'{MONEY[t]:,} CobbleDollars'
                stats['money'] += MONEY[t]
            q['rewards'] = new
            stats[f'tier{t}'] += 1
            stats[f'pool:{pool}'] += 1
        f.write_text(dump(ch) + '\n')

    lines = LANG.read_text().splitlines()
    first_quest = next(i for i, l in enumerate(lines) if l.startswith('\tquest.'))
    lines[first_quest:first_quest] = [f'\t{k}: {snbt_string(v)}' for k, v in titles.items()]
    LANG.write_text('\n'.join(lines) + '\n')
    print(dict(sorted(stats.items())))


if __name__ == '__main__':
    main()
