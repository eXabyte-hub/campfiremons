"""Mod chapters for the quest book (imported by build_book.py)."""
import json
import math
from pathlib import Path

HERE = Path(__file__).parent
ALL_ITEMS = {k: set(v) for k, v in json.load(open(HERE / 'data' / 'all_items.json')).items()}
DUMP = [l.split(' ', 2) for l in open(HERE / 'data' / 'dump.txt').read().splitlines()]
MISSING = []


def have(ns, names):
    """Only the items that exist (vanilla is assumed); records the rest so we can see what got dropped."""
    out = []
    for n in names:
        if ns == 'minecraft' or n in ALL_ITEMS.get(ns, ()):
            out.append(f'{ns}:{n}')
        else:
            MISSING.append(f'{ns}:{n}')
    return out


def install(g):
    """Bring build_book's helpers into this module."""
    globals().update({k: g[k] for k in ('t_check', 't_item', 't_cob', 'r_xp', 'r_item', 'image', 'banner', 'link',
                                        'Raw', 'd', 'BANNER_PX', 'title_of')})


def item_quest(b, c, item, x, y, sub, shape='rsquare', size=0.75, xp=1, title=None):
    return b.add(c, round(x, 2), round(y, 2), item, [t_item(item)], [r_xp(xp)], title, None, None, shape, size,
                 deps=[sub] if sub else (), optional=True)


def grid(b, c, items, cx, cy, cols, sub, shape='rsquare', size=0.75, step=1.0):
    rows = math.ceil(len(items) / cols)
    for i, it in enumerate(items):
        r, col = divmod(i, cols)
        n = min(cols, len(items) - r * cols)
        item_quest(b, c, it, cx + (col - (n - 1) / 2) * step, cy + (r - (rows - 1) / 2) * step, sub, shape, size)
    return cols * step, rows * step


def branch_chapter(b, c, chapter_icon, banner_name, hub, branches, R=5.0):
    b.new_chapter(c, chapter_icon)
    ch = b.chapters[c]
    hub_id = b.add(c, 0, 0, hub['icon'], hub.get('tasks') or [t_check()], [r_xp(3)], hub['title'], hub.get('sub'),
                   hub['desc'], 'gear', 2.5)
    ch['images'] = []
    for br in branches:
        items = br['items']
        if not items:
            continue
        a = math.radians(br['angle'])
        dx, dy = math.cos(a), math.sin(a)
        sx, sy = dx * br.get('R', R), dy * br.get('R', R)
        first = items[0]
        sub = b.add(c, round(sx, 2), round(sy, 2), first, [t_item(first)], [r_xp(3)], br['title'], br.get('sub'),
                    br.get('desc'), 'gear', 1.6, deps=[hub_id])
        rest = items[1:]
        if not rest:
            continue
        n = len(rest)
        cols = br.get('cols') or max(1, min(n, math.ceil(math.sqrt(n * 1.8))))
        rows = math.ceil(n / cols)
        gw, gh = cols * 1.0, rows * 1.0
        dist = 1.5 + 0.5 * abs(dx) * gw + 0.5 * abs(dy) * gh
        gx, gy = sx + dx * dist, sy + dy * dist
        grid(b, c, rest, gx, gy, cols, sub, br.get('shape', 'rsquare'))
        ly = gy + gh / 2 + 0.75 if dy > 0.3 else gy - gh / 2 - 0.75
        ch['images'].append(banner(br['label'], round(gx, 2), round(ly, 2), 0.9))
    for q in ch['quests']:
        if q.get('optional') == 'true':
            q['hide_dependency_lines'] = Raw('true')
    top = min([float(q['y'][:-1]) - float(q['size'][:-1]) for q in ch['quests']] +
              [float(i['y'][:-1]) - float(i['height'][:-1]) / 2 for i in ch['images']])
    ch['images'].append(banner(banner_name, 0, round(top - 1.3, 2), 1.8))
    return hub_id


# ---------------------------------------------------------------- Create
def create(b):
    C = lambda *n: have('create', n)
    branch_chapter(b, 'create', 'create:cogwheel', 'create', {
        'icon': 'create:cogwheel', 'title': 'Create', 'sub': 'Engineering with Pokémon in mind',
        'desc': ["Create is mechanical engineering: spin shafts with water wheels, windmills or engines, and",
                 "use that rotation to drive presses, mixers, belts and moving contraptions.",
                 "Start with &eandesite alloy&r. Hold &aW&r over any Create item to &ePonder&r it: an animated",
                 "guide shows exactly how it works. Cobblemon: Create Industries adds ball production lines."]}, [
        dict(label='create_power', angle=-45, title='Rotational Power', sub='Make things spin',
             items=C('water_wheel', 'shaft', 'cogwheel', 'large_cogwheel', 'gearbox', 'hand_crank', 'large_water_wheel',
                     'windmill_bearing', 'steam_engine', 'blaze_burner', 'encased_chain_drive', 'clutch', 'gearshift',
                     'rotation_speed_controller')),
        dict(label='create_machines', angle=0, title='Machines', sub='Process anything',
             items=C('mechanical_press', 'mechanical_mixer', 'basin', 'millstone', 'crushing_wheel', 'encased_fan',
                     'mechanical_saw', 'deployer', 'mechanical_crafter', 'mechanical_drill', 'mechanical_harvester',
                     'mechanical_plough')),
        dict(label='create_trains', angle=45, title='Trains', sub='Rail networks',
             items=C('track', 'track_station', 'track_signal', 'track_observer', 'controls', 'railway_casing')),
        dict(label='create_tools', angle=90, title='Tools', sub='The engineer’s kit',
             items=C('wrench', 'goggles', 'sand_paper', 'extendo_grip', 'potato_cannon', 'wand_of_symmetry',
                     'schematic_table', 'schematicannon', 'linked_controller')),
        dict(label='create_contraptions', angle=135, title='Contraptions', sub='Things that move',
             items=C('mechanical_bearing', 'mechanical_piston', 'sticky_mechanical_piston', 'gantry_carriage',
                     'rope_pulley', 'elevator_pulley', 'cart_assembler', 'linear_chassis', 'radial_chassis',
                     'super_glue', 'portable_storage_interface')),
        dict(label='create_fluids', angle=180, title='Fluid Logistics', sub='Pipes and tanks',
             items=C('fluid_pipe', 'mechanical_pump', 'fluid_tank', 'fluid_valve', 'spout', 'item_drain',
                     'hose_pulley')),
        dict(label='create_items', angle=-135, title='Item Logistics', sub='Belts, funnels and packages',
             items=C('belt_connector', 'andesite_funnel', 'brass_funnel', 'andesite_tunnel', 'brass_tunnel', 'chute',
                     'smart_chute', 'depot', 'weighted_ejector', 'mechanical_arm', 'item_vault', 'packager',
                     'stock_link', 'stock_ticker', 'package_frogport')),
        dict(label='create_addons', angle=-90, title='Addons', sub='Electricity, deco and copycats',
             items=have('createaddition', ['electric_motor', 'alternator', 'connector', 'large_connector',
                                           'rolling_mill', 'tesla_coil', 'portable_energy_interface',
                                           'modular_accumulator']) +
             have('createdeco', ['andesite_catwalk', 'andesite_hull', 'andesite_support', 'andesite_window']) +
             have('copycats', ['copycat_block', 'copycat_beam', 'copycat_board'])),
    ], R=5.2)


# ---------------------------------------------------------------- Oritech
def oritech(b):
    O = lambda *n: have('oritech', n)
    branch_chapter(b, 'oritech', 'oritech:pulverizer_block', 'oritech', {
        'icon': 'oritech:pulverizer_block', 'title': 'Oritech', 'sub': 'Industrial machines',
        'desc': ["Oritech is big industry: generators make energy, pipes carry it, and machines turn ores and",
                 "crops into far more than a furnace ever could. Addons bolt onto machines to make them faster,",
                 "more efficient or able to do new jobs. Check each machine's recipe and uses in EMI."]}, [
        dict(label='oritech_machines', angle=0, title='Machines', sub='Processing',
             items=O('pulverizer_block', 'fragment_forge_block', 'assembler_block', 'foundry_block', 'cooler_block',
                     'centrifuge_block', 'atomic_forge_block', 'refinery_block', 'powered_furnace_block',
                     'laser_arm_block', 'deep_drill_block', 'drone_port_block', 'placer_block', 'destroyer_block',
                     'fertilizer_block', 'treefeller_block', 'enchanter_block', 'pump_block', 'charger_block')),
        dict(label='oritech_energy', angle=-60, title='Energy', sub='Power generation',
             items=O('basic_generator_block', 'bio_generator_block', 'lava_generator_block', 'fuel_generator_block',
                     'steam_engine_block', 'big_solar_panel_block', 'small_storage_block', 'large_storage_block',
                     'energy_pipe', 'superconductor', 'power_pole_block')),
        dict(label='oritech_logistics', angle=-120, title='Logistics', sub='Pipes and filters',
             items=O('item_pipe', 'transparent_item_pipe', 'item_filter_block', 'fluid_pipe', 'small_tank_block',
                     'pipe_booster_block')),
        dict(label='oritech_reactor', angle=180, title='Reactor', sub='Late game power',
             items=O('reactor_controller', 'reactor_wall', 'reactor_rod', 'reactor_vent', 'reactor_heat_pipe',
                     'reactor_fuel_port', 'reactor_energy_port')),
        dict(label='oritech_gear', angle=120, title='Equipment', sub='Exosuit and tools',
             items=O('wrench', 'target_designator', 'exo_helmet', 'exo_chestplate', 'exo_leggings', 'exo_boots',
                     'jetpack', 'portable_laser', 'electric_mace', 'chainsaw', 'hand_drill', 'promethium_pickaxe',
                     'promethium_axe')),
        dict(label='oritech_addons', angle=60, title='Addons', sub='Upgrade your machines',
             items=O('machine_speed_addon', 'machine_efficiency_addon', 'machine_ultimate_addon', 'quarry_addon',
                     'machine_processing_addon', 'machine_fluid_addon', 'machine_yield_addon', 'crop_filter_addon',
                     'machine_hunter_addon', 'machine_capacitor_addon', 'machine_acceptor_addon',
                     'machine_inventory_proxy_addon', 'machine_extender', 'steam_boiler_addon',
                     'machine_redstone_addon', 'machine_silk_touch_addon', 'machine_burst_addon')),
    ], R=5.4)


# ---------------------------------------------------------------- Storage
def storage(b):
    tiers = ['', 'copper_', 'iron_', 'gold_', 'diamond_', 'netherite_']
    branch_chapter(b, 'storage', 'minecraft:chest', 'storage', {
        'icon': 'minecraft:chest', 'title': 'Storage', 'sub': 'Never run out of room',
        'desc': ["&eSophisticated Storage&r: chests and barrels you upgrade in place, with sorting and pickup",
                 "upgrades. &eBackpacks&r carry the same upgrades on your back.",
                 "&eTom's Simple Storage&r links your chests to one terminal; &eRefined Storage&r goes fully digital,",
                 "with disks and autocrafting."]}, [
        dict(label='storage_soph', angle=0, title='Sophisticated Storage', sub='Upgradeable chests and barrels',
             items=have('sophisticatedstorage', [f'{t}chest' for t in tiers] + [f'{t}barrel' for t in tiers[1:]] +
                        ['barrel', 'limited_barrel_1', 'limited_barrel_2', 'limited_barrel_3', 'limited_barrel_4',
                         'shulker_box', 'storage_controller', 'storage_link', 'tank', 'storage_tool']) +
             have('sophisticatedstorageinmotion', ['storage_minecart'])),
        dict(label='storage_packs', angle=60, title='Backpacks', sub='Storage on your back',
             items=have('sophisticatedbackpacks', [f'{t}backpack' for t in tiers])),
        dict(label='storage_upgrades', angle=120, title='Upgrades', sub='For chests and backpacks',
             items=have('sophisticatedbackpacks', ['upgrade_base', 'pickup_upgrade', 'filter_upgrade', 'magnet_upgrade',
                                                   'feeding_upgrade', 'compacting_upgrade', 'void_upgrade',
                                                   'restock_upgrade', 'deposit_upgrade', 'refill_upgrade',
                                                   'smelting_upgrade', 'crafting_upgrade', 'stonecutter_upgrade',
                                                   'stack_upgrade_tier_1', 'everlasting_upgrade', 'inception_upgrade',
                                                   'jukebox_upgrade', 'tank_upgrade', 'battery_upgrade'])),
        dict(label='storage_toms', angle=180, title="Tom's Storage", sub='One terminal, every chest',
             items=have('toms_storage', ['storage_terminal', 'inventory_connector', 'crafting_terminal',
                                         'inventory_cable', 'inventory_cable_connector', 'inventory_interface',
                                         'filing_cabinet', 'wireless_terminal', 'adv_wireless_terminal', 'item_filter',
                                         'level_emitter', 'inventory_proxy'])),
        dict(label='storage_rs', angle=-90, title='Refined Storage', sub='Digital storage',
             items=have('refinedstorage', ['controller', 'disk_drive', 'grid', 'crafting_grid', '1k_storage_disk',
                                           '4k_storage_disk', '16k_storage_disk', '64k_storage_disk', 'cable',
                                           'importer', 'exporter', 'wireless_grid', 'autocrafter', 'pattern',
                                           'machine_casing', 'quartz_enriched_iron'])),
    ], R=5.0)


# ---------------------------------------------------------------- Relics
def relics(b):
    R_ = lambda *n: have('relics', n)
    branch_chapter(b, 'relics', 'relics:ring_of_the_seven_deadly_sins', 'relics', {
        'icon': 'relics:ring_of_the_seven_deadly_sins', 'title': 'Relics', 'sub': 'Trinkets that level up',
        'desc': ["Relics are powerful trinkets with abilities that grow the more you use them.",
                 "They turn up in structure chests across the Overworld, the Nether and the End.",
                 "Reliquified Artifacts lets the Artifacts level up the same way."]}, [
        dict(label='relic_back', angle=-30, title='Back', sub='Mantles', items=R_('leafy_mantle', 'midnight_mantle',
                                                                                    'glitchy_mantle', 'ghostly_mantle')),
        dict(label='relic_head', angle=-90, title='Head', sub='Masks and hats', items=R_('piglin_mask', 'chef_hat')),
        dict(label='relic_necklace', angle=-150, title='Necklace & Ring', sub='Around your neck',
             items=R_('reflective_necklace', 'jellyfish_necklace', 'ring_of_the_seven_deadly_sins',
                      'experience_disperser')),
        dict(label='relic_belt', angle=150, title='Belt', sub='Belts', items=R_('kinetic_belt', 'hunting_belt')),
        dict(label='relic_feet', angle=90, title='Feet', sub='Boots and skates',
             items=R_('roller_skate', 'springy_boot', 'cut_glass_boot')),
        dict(label='relic_other', angle=30, title='In Hand', sub='Held relics',
             items=R_('chorus_staff', 'clot_of_time', 'rider_flute', 'sphere_of_self_sacrifice',
                      'shield_of_retaliation', 'golden_tooth', 'pet_bone')),
    ], R=4.2)
    ch = b.chapters['relics']
    ch['images'].insert(0, image('campfiremons:textures/quests/gold_panel.png', 0, 0, 3.4, 2.9))


# ---------------------------------------------------------------- Training
def training(b):
    Cb = lambda *n: have('cobblemon', n)
    mints = ['adamant', 'jolly', 'timid', 'modest', 'bold', 'calm', 'careful', 'impish', 'brave', 'quiet', 'relaxed',
             'sassy', 'lonely', 'naughty', 'hasty', 'naive', 'mild', 'rash', 'gentle', 'lax', 'serious']
    tms = [n for n in sorted(ALL_ITEMS.get('simpletms', ())) if n.startswith('tm_')]
    picks = [f'tm_{m}' for m in ('thunderbolt', 'flamethrower', 'icebeam', 'earthquake', 'psychic', 'shadowball',
                                 'dragonpulse', 'surf', 'swordsdance', 'calmmind')]
    branch_chapter(b, 'training', 'cobblemon:exp_candy_l', 'training', {
        'icon': 'cobblemon:exp_candy_l', 'title': 'Training', 'sub': 'Build a winning team',
        'desc': ["&eEXP Candy&r levels Pokémon up to your cap. &eVitamins&r and &efeathers&r raise EVs, &emints&r",
                 "change which stat a nature boosts, and &ePower items&r focus EV gains in battle.",
                 "&eBottle Caps&r max out IVs from Stage 2. TRs (one use) work from Stage 1 and TMs (reusable)",
                 "from Stage 5. Ability Capsules and Patches are Stage 8 finds."]}, [
        dict(label='train_candy', angle=0, title='Candy', sub='Levels on demand',
             items=Cb('exp_candy_xs', 'exp_candy_s', 'exp_candy_m', 'exp_candy_l', 'exp_candy_xl', 'rare_candy',
                      'ability_capsule', 'ability_patch')),
        dict(label='train_vitamins', angle=-60, title='Vitamins', sub='Raise EVs',
             items=Cb('hp_up', 'protein', 'iron', 'calcium', 'zinc', 'carbos', 'pp_up', 'pp_max')),
        dict(label='train_feathers', angle=-120, title='Feathers', sub='Fine-tune EVs',
             items=Cb('health_feather', 'muscle_feather', 'resist_feather', 'genius_feather', 'clever_feather',
                      'swift_feather')),
        dict(label='train_mints', angle=180, title='Mints', sub='Change the nature’s stat', cols=7,
             items=have('cobblemon', [f'{m}_mint' for m in mints])),
        dict(label='train_power', angle=120, title='Power Items', sub='Focus EV gains',
             items=Cb('power_weight', 'power_bracer', 'power_belt', 'power_lens', 'power_band', 'power_anklet')),
        dict(label='train_caps', angle=60, title='Bottle Caps', sub='Perfect IVs (Stage 2)',
             items=have('obc', ['bottle_cap', 'bottle_cap_hp', 'bottle_cap_attack', 'bottle_cap_defence',
                               'bottle_cap_special_attack', 'bottle_cap_special_defence', 'bottle_cap_speed',
                               'bottle_cap_gold'])),
        dict(label='train_tms', angle=-90, title='TMs & TRs', sub='Teach moves', R=7.6,
             items=have('simpletms', ['machine_tm', 'case_tm', 'case_tr'] + [p for p in picks if p[3:] in
                                                                              {t[3:] for t in tms}])),
    ], R=5.0)


# ---------------------------------------------------------------- Home & Building
def building(b):
    furn = sorted(ALL_ITEMS.get('cobblefurnies', ()))
    poke_furn = [f for f in furn if any(k in f for k in ('poke', 'apricorn', 'pc', 'healing'))][:10]
    branch_chapter(b, 'building', 'handcrafted:oak_chair', 'building', {
        'icon': 'handcrafted:oak_chair', 'title': 'Home & Building', 'sub': 'Make your base yours',
        'desc': ["Decorate with thousands of block variants and furniture.",
                 "&eChipped&r workbenches and the &eRechiseled&r chisel turn blocks into new styles;",
                 "&eHandcrafted&r and &eCobbleFurnies&r add furniture; &eFramedBlocks&r copy any texture onto any",
                 "shape; &eBuilding Gadgets&r place hundreds of blocks at once. &eWaystones&r link your bases."]}, [
        dict(label='build_chipped', angle=0, title='Chipped', sub='Workbenches',
             items=have('chipped', ['botanist_workbench', 'carpenters_table', 'glassblower', 'loom_table',
                                    'mason_table', 'alchemy_bench', 'tinkering_table'])),
        dict(label='build_rechiseled', angle=-90, title='Rechiseled', sub='The chisel',
             items=have('rechiseled', ['chisel'])),
        dict(label='build_handcrafted', angle=-120, title='Handcrafted', sub='Furniture',
             items=have('handcrafted', ['hammer', 'oak_chair', 'oak_table', 'oak_couch', 'oak_fancy_bed', 'oak_desk',
                                        'oak_shelf', 'oak_cupboard', 'oak_drawer', 'oak_nightstand', 'oak_bench',
                                        'oak_side_table'])),
        dict(label='build_furnies', angle=180, title='CobbleFurnies', sub='Pokémon furniture',
             items=have('cobblefurnies', poke_furn or furn[:10])),
        dict(label='build_framed', angle=120, title='FramedBlocks', sub='Any texture, any shape',
             items=have('framedblocks', ['framed_hammer', 'framed_cube', 'framed_slope', 'framed_slab',
                                         'framed_stairs', 'framed_door', 'framed_chest', 'framed_wrench',
                                         'framed_blueprint'])),
        dict(label='build_gadgets', angle=60, title='Building Gadgets', sub='Build faster',
             items=have('buildinggadgets2', ['gadget_building', 'gadget_exchanging', 'gadget_copy_paste',
                                             'gadget_destruction', 'template_manager'])),
        dict(label='build_travel', angle=-60, title='Waystones', sub='Fast travel',
             items=have('waystones', ['waystone', 'sharestone', 'warp_stone', 'warp_scroll', 'return_scroll',
                                      'bound_scroll', 'portstone', 'warp_plate'])),
    ], R=4.6)


# ---------------------------------------------------------------- Tools & Weapons, Armor
def dumped(kind):
    return [json.loads(v) for _, k, v in DUMP if k == kind]


def tools_weapons(b):
    c = 'tools_weapons'
    b.new_chapter(c, 'minecraft:diamond_pickaxe')
    ch = b.chapters[c]
    hub = b.add(c, 0, 0, 'minecraft:stick', [t_check()], [r_xp(2)], 'Tools and Weapons', 'Gear up',
                ["Pickaxes are sorted by what they can mine, swords by their damage. &eMythic Upgrades&r gems",
                 "make tools past netherite; &eCobblemon: Armory&r adds weapons styled on Pokémon."], 'gear', 2.25)
    ch['images'] = [image('minecraft:textures/item/diamond_sword.png', -3.3, 0, 2.4, 2.4),
                    image('minecraft:textures/item/diamond_pickaxe.png', 3.3, 0, 2.4, 2.4),
                    banner('tools_weapons', 0, -10.4, 1.8), banner('pickaxes', 0, -8.6, 1.1),
                    banner('swords', 0, 2.3, 1.1)]
    picks = {p['id']: p['tier'] for p in dumped('pick')}
    tiers = [('tier_wood', ['minecraft:wooden_pickaxe', 'minecraft:golden_pickaxe']),
             ('tier_stone', ['minecraft:stone_pickaxe']), ('tier_iron', ['minecraft:iron_pickaxe']),
             ('tier_diamond', ['minecraft:diamond_pickaxe']),
             ('tier_netherite', ['minecraft:netherite_pickaxe'] + sorted(i for i, t in picks.items()
                                                                        if i.startswith('mythicupgrades:')))]
    for i, (label, items) in enumerate(tiers):
        x = -8.4 + i * 4.2
        ch['images'].append(banner(label, x, -7.3, 0.62))
        grid(b, c, items, x, -5.6 + (0.5 if len(items) > 3 else 0), 3, hub, 'circle', 0.8)
    swords = sorted(dumped('sword'), key=lambda s: (s['dmg'], s['id']))
    rows = {}
    for s in swords:
        if s['id'].startswith('cobblemonarmory:'):
            continue
        rows.setdefault(int(s['dmg']), []).append(s['id'])
    y = 3.7
    for dmg in sorted(rows):
        ch['images'].append(banner(f'dmg_{dmg}', -4.6, y, 0.75))
        for j, it in enumerate(rows[dmg]):
            item_quest(b, c, it, -2.3 + j * 1.0, y, hub, 'diamond', 0.8)
        y += 1.1
    armory = [s['id'] for s in swords if s['id'].startswith('cobblemonarmory:')]
    ch['images'].append(banner('pokemon_weapons', -4.6, y + 0.4, 0.75))
    for j, it in enumerate(armory):
        item_quest(b, c, it, -1.4 + j * 1.0, y + 0.4, hub, 'pentagon', 0.85)
    for q in ch['quests']:
        if q['id'] != hub:
            q['hide_dependency_lines'] = Raw('true')


def armor(b):
    c = 'armor'
    b.new_chapter(c, 'minecraft:iron_chestplate')
    ch = b.chapters[c]
    hub = b.add(c, 0, 0, 'minecraft:iron_chestplate', [t_check()], [r_xp(2)], 'Armor', 'Suit up',
                ["Vanilla sets are sorted by armor points. &eCobblemon: Armory&r makes full sets styled on",
                 "Pokémon, each with a shiny version, plus the hats of the games' heroes."], 'gear', 2.25)
    ch['images'] = [banner('armor', 0, -6.6, 1.8)]
    sets = {}
    for a in dumped('armor'):
        if a['type'] in ('helmet', 'chestplate', 'leggings', 'boots') and a['mat'] != '?':
            sets.setdefault(a['mat'], {})[a['type']] = a['id']
    order = ('helmet', 'chestplate', 'leggings', 'boots')
    sets = {m: v for m, v in sets.items() if len(v) == 4}  # full four-piece sets only

    def set_quest(mat, x, y, size=1.0, shape='hexagon'):
        pieces = sets[mat]
        name = mat.split(':')[1].replace('shiny_', 'Shiny ').replace('_', ' ').title()
        b.add(c, round(x, 2), round(y, 2), pieces['chestplate'], [t_item(pieces[t]) for t in order], [r_xp(3)],
              f'{name} Armor', 'All four pieces', None, shape, size, deps=[hub], optional=True)

    vanilla = [('armor_7', ['minecraft:leather']), ('armor_11', ['minecraft:gold']),
               ('armor_12', ['minecraft:chainmail']), ('armor_15', ['minecraft:iron']),
               ('armor_20', ['minecraft:diamond', 'minecraft:netherite'])]
    for i, (label, mats) in enumerate(vanilla):
        x = -8.4 + i * 4.2
        ch['images'].append(banner(label, x, -4.6, 0.62))
        for j, m in enumerate(mats):
            set_quest(m, x + (j - (len(mats) - 1) / 2) * 1.3, -3.3)
    base = sorted(m for m in sets if m.startswith('cobblemonarmory:') and 'shiny_' not in m)
    shiny = sorted(m for m in sets if m.startswith('cobblemonarmory:shiny_'))
    for label, mats, x0 in (('pokemon_armor', base, -5.2), ('shiny_armor', shiny, 5.2)):
        ch['images'].append(banner(label, x0, 2.0, 1.0))
        for i, m in enumerate(mats):
            set_quest(m, x0 + (i % 6 - 2.5) * 1.15, 3.4 + (i // 6) * 1.15, 0.9, 'rsquare')
    hats = sorted(a['id'] for a in dumped('armor') if a['mat'].endswith('_hat'))
    rows = math.ceil(len(hats) / 9)
    ch['images'].append(banner('trainer_hats', 0, 7.2, 1.0))
    grid(b, c, hats, 0, 8.4 + (rows - 1) / 2, 9, hub, 'circle', 0.8)
    for q in ch['quests']:
        if q['id'] != hub:
            q['hide_dependency_lines'] = Raw('true')


# ---------------------------------------------------------------- Raids
RAID_TIERS = [(1, 0), (2, 1), (3, 3), (4, 4), (5, 6)]


def raids(b):
    c = 'raids'
    b.new_chapter(c, 'cobblemonraiddens:raid_crystal_block')
    ch = b.chapters[c]
    hub = b.add(c, 0, 0, 'cobblemonraiddens:raid_crystal_block', [t_check()], [r_xp(3)], 'Raid Dens',
                'Team up against bosses',
                ["Raid crystals glow across the world. Start a raid to fight a powerful boss with up to three",
                 "friends; beat it and you get a chance to catch it, plus rewards in a Raid Pouch.",
                 "Higher star tiers open as you progress: " + ", ".join(
                     f"★{s} {'from the start' if st == 0 else f'at Stage {st}'}" for s, st in RAID_TIERS) + "."],
                'gear', 2.5)
    ch['images'] = [banner('raids', 0, -5.0, 1.8), image('campfiremons:textures/quests/wormhole.png', 0, 0, 3.6, 3.6)]
    ch['images'].insert(0, ch['images'].pop())
    prev = hub
    for i, n in enumerate((1, 5, 10, 25, 50)):
        prev = b.add(c, 3.2 + i * 1.9, -1.0, 'cobblemonraiddens:raid_shard', [t_cob('win_raid', n)],
                     [r_xp(3 + 2 * i), r_item('cobblemon:exp_candy_m' if i < 3 else 'cobblemon:exp_candy_l', 2 + i)],
                     f"Raid {['Rookie', 'Regular', 'Veteran', 'Expert', 'Legend'][i]}",
                     f"Win {n} raid{'s' if n > 1 else ''}", None, 'gear' if i == 4 else 'circle',
                     1.4 if i == 4 else 1.0, deps=[prev])
    b.add(c, -3.2, -1.0, 'cobblemonraiddens:raid_pouch', [t_cob('open_raid_pouch')], [r_xp(2)], 'Spoils',
          'Open a Raid Pouch', None, 'rsquare', 1.0, deps=[hub])
    b.add(c, -5.1, -1.0, 'cobblemonraiddens:catching_charm', [t_item('cobblemonraiddens:catching_charm')], [r_xp(2)],
          None, None, "Raises your chance to catch the boss after a win.", 'rsquare', 0.85, deps=[hub], optional=True)
    for j, cheer in enumerate(('cheer_attack', 'cheer_defense', 'cheer_heal')):
        item_quest(b, c, f'cobblemonraiddens:{cheer}', -3.2 - j * 1.0, 1.2, hub, 'circle', 0.8)
    for i, (stars, stage) in enumerate(RAID_TIERS):
        b.add(c, -4.0 + i * 2.0, 3.6, 'cobblemonraiddens:raid_crystal_block', [t_check()], [r_xp(1)],
              f"{'★' * stars} Raids", 'Open from the start' if stage == 0 else f'Open from Stage {stage}',
              f"★{stars} dens need you to be at Stage {stage} or later to host or join." if stage else
              "★1 dens are open to everyone.", 'diamond', 1.0 + 0.1 * i, deps=[hub])
