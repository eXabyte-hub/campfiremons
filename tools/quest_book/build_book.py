"""One-off rebuild of the Campfiremons quest book: hub layouts, banners, new chapters, text fixes.

Keeps every existing quest ID (progress on the live server carries over). Run with the repo as cwd's parent of
config/ftbquests; writes chapters, lang, chapter groups.
"""
import re
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from snbt import Raw, dump, parse  # noqa: E402

Q = Path(__file__).resolve().parents[2] / 'config' / 'ftbquests' / 'quests'
USED = set()


def d(v):
    return Raw(f"{float(v)}d")


def new_id():
    while True:
        i = '%016X' % secrets.randbits(63)  # FTB Quests replaces IDs >= 8000000000000000 with random ones on load
        if i not in USED and not i.startswith('0'):
            USED.add(i)
            return i


# ---------------------------------------------------------------- tasks and rewards
def t_check():
    return {'id': new_id(), 'type': 'checkmark'}


def t_item(item, count=1):
    t = {'id': new_id(), 'type': 'item', 'item': {'count': Raw('1'), 'id': item}}
    if count > 1:
        t['count'] = Raw(f"{count}L")
    return t


def t_cob(action, amount=1, **kw):
    t = {'abilities': '', 'action': action, 'amount': Raw(f"{amount}L"), 'aspects': '', 'biome': '',
         'dex_progress': 'seen', 'dimension': '', 'form': '', 'gender': '', 'held_items': '', 'id': new_id(),
         'max_level': Raw('0'), 'max_turns': Raw('0'), 'min_level': Raw('0'), 'moves': '', 'natures': '',
         'poke_ball_used': '', 'pokemon': '', 'pokemon_type': '', 'raid_tiers': '', 'region': '',
         'shiny': Raw('false'), 'targetPlayer': '', 'time_max': Raw('24000L'), 'time_min': Raw('0L'),
         'trainers': '', 'type': 'cobblemon_tasks:cobblemon_task'}
    t.update(kw)
    return t


def r_xp(n):
    return {'id': new_id(), 'type': 'xp_levels', 'xp_levels': Raw(str(n))}


def r_item(item, count=1):
    r = {'id': new_id(), 'type': 'item', 'item': {'count': Raw('1'), 'id': item}}
    if count > 1:
        r['count'] = Raw(str(count))
    return r


def image(path, x, y, w, h):
    return {'height': d(h), 'id': new_id(), 'image': path, 'rotation': d(0), 'width': d(w), 'x': d(x), 'y': d(y)}


BANNER_PX = {}  # banner name -> (w, h) in pixels, read from the PNGs


def banner(name, x, y, height=1.5):
    w, h = BANNER_PX[name]
    return image(f"campfiremons:textures/quests/{name}.png", x, y, round(height * w / h, 2), height)


TYPES = ['normal', 'fire', 'water', 'grass', 'electric', 'ice', 'fighting', 'poison', 'ground', 'flying',
         'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']


def type_icon(t, x, y, s=0.85):
    return image(f"mega_showdown:textures/gui/summary/tera_types/{t}.png", x, y, s, s)


def link(ch, qid, x, y, size=1.0, shape='circle'):
    ch['quest_links'].append({'id': new_id(), 'linked_quest': qid, 'shape': shape, 'size': d(size), 'x': d(x), 'y': d(y)})


def poke_icon(name):
    return {'id': 'cobblemon:pokemon_model', 'components': {'cobblemon:pokemon_item': {'species': f'cobblemon:{name}', 'aspects': []}}}


# ---------------------------------------------------------------- quests
class Book:
    def __init__(self):
        self.chapters = {}  # filename -> chapter dict
        self.lang = {}  # filename -> lang dict
        for f in sorted((Q / 'chapters').glob('*.snbt')):
            ch = parse(f.read_text())
            self.chapters[f.stem] = ch
            self.lang[f.stem] = parse((Q / 'lang/en_us/chapters' / f.name).read_text())
            USED.add(ch['id'])
            for q in ch['quests']:
                USED.add(q['id'])
                for x in q.get('tasks', []) + q.get('rewards', []):
                    USED.add(x['id'])
            for im in ch.get('images', []):
                USED.add(im['id'])

    def quest(self, chapter, qid):
        return next(q for q in self.chapters[chapter]['quests'] if q['id'] == qid)

    def place(self, chapter, qid, x, y, shape='circle', size=1.0, deps=None, hide_lines=None, optional=None):
        q = self.quest(chapter, qid)
        q['x'], q['y'], q['shape'], q['size'] = d(x), d(y), shape, d(size)
        if deps is not None:
            q['dependencies'] = list(deps)
        if hide_lines is not None:
            q['hide_dependency_lines'] = Raw('true' if hide_lines else 'false')
        if optional is not None:
            q['optional'] = Raw('true' if optional else 'false')
        return q

    def add(self, chapter, x, y, icon, tasks, rewards, title, subtitle, desc, shape='circle', size=1.0, deps=(),
            optional=False, qid=None):
        qid = qid or new_id()
        q = {'id': qid, 'icon': icon if isinstance(icon, dict) else {'id': icon}, 'shape': shape, 'size': d(size), 'x': d(x), 'y': d(y),
             'tasks': tasks, 'rewards': rewards}
        if deps:
            q['dependencies'] = list(deps)
        if optional:
            q['optional'] = Raw('true')
        self.chapters[chapter]['quests'].append(q)
        self.text(chapter, qid, title, subtitle, desc)
        return qid

    def text(self, chapter, qid, title=None, subtitle=None, desc=None):
        lang = self.lang[chapter]
        if title is not None:
            lang[f'quest.{qid}.title'] = title
        if subtitle is not None:
            lang[f'quest.{qid}.quest_subtitle'] = subtitle
        if desc is not None:
            lang[f'quest.{qid}.quest_desc'] = desc if isinstance(desc, list) else [desc]

    def move_text(self, chapter, old, new):
        lang = self.lang[chapter]
        for key in [k for k in lang if k.startswith(f'quest.{old}.')]:
            lang[key.replace(old, new)] = lang.pop(key)

    def new_chapter(self, filename, icon):
        cid = new_id()
        self.chapters[filename] = {'default_hide_dependency_lines': Raw('false'), 'default_quest_shape': '',
                                   'filename': filename, 'group': '', 'icon': {'id': icon}, 'id': cid,
                                   'images': [], 'order_index': Raw('0'), 'quest_links': [], 'quests': []}
        self.lang[filename] = {}
        return cid

    def write(self):
        for name, ch in self.chapters.items():
            ids = {q['id'] for q in ch['quests']}
            lang = {k: v for k, v in self.lang[name].items()
                    if not k.startswith('quest.') or k.split('.')[1] in ids}  # drop text of quests that are gone
            (Q / 'chapters' / f'{name}.snbt').write_text(dump(ch) + '\n')
            (Q / 'lang/en_us/chapters' / f'{name}.snbt').write_text(dump(lang) + '\n')


def main():
    from PIL import Image
    art = Path(__file__).resolve().parents[2] / 'kubejs' / 'assets' / 'campfiremons' / 'textures' / 'quests'
    for p in art.glob('*.png'):
        BANNER_PX[p.stem] = Image.open(p).size
    b = Book()

    # ------------------------------------------------ text that lost its quest when quests were re-ID'd (800a3cb)
    for chapter, old, new in [
            ('stage_0', 'FE35AD43E70A72D1', '7BFE2B886541122D'), ('stage_0', 'C2B290715D042AD2', '0440240B5085D636'),
            ('stage_1', 'D5DC4192ED160AE8', '7F9958556C02DF15'), ('stage_1', '901636C69E2512B5', '5404ADE871497700'),
            ('stage_1', 'AD4E5491BD22A501', '3C85D0F002E65112'), ('stage_2', '8976FC1F2EBF20C9', '5ECA8FC5E895C86C'),
            ('stage_2', '8F9368E4F9FA5A82', '385B0BD23EB96AA2'), ('stage_2', 'F0C61560FD1C794A', '4FF0A1ECD784785A'),
            ('stage_2', 'D7CC07EDED5AEA39', '06CA7CC483D0C8F4'), ('stage_3', 'ABA5E1CF60E8731E', '7D617531A42E36ED'),
            ('stage_4', 'BD95E6EDDA9C33DE', '6B3BF4CF69AB6063'), ('stage_4', '81DBEC90E713DC66', '0003E6E0530C6E98'),
            ('stage_5', 'A4A1503F25CFE7CF', '34D7A6CED618B0DF'), ('stage_5', 'A71C0D5D1AD1966D', '026F1DF4C892C8EB'),
            ('stage_6', 'D3D6C99E71D40EC6', '134977A1494685F1'), ('stage_7', 'DA87870A2FE118B1', '21D425525C990B07'),
            ('stage_8', '8C44F8C3AB2C06FD', '4C029B208A6F165B'), ('stage_8', 'D607CA6A5633F780', '7F1D37F035F13725'),
            ('stage_8', 'A4B38243E9B5C746', '01F859EDB8C5D546'), ('stage_8', 'E7B766F9C6BA1490', '2821F035DFC0EBD5'),
            ('stage_9', 'B5701991E9C0EC9F', '534ACB982620E7AD')]:
        b.move_text(chapter, old, new)

    getting_started(b)
    stage_chapters(b)
    evolution(b)
    gotta_find(b)
    poke_balls(b)
    battle_gimmicks(b)
    legends(b)
    artifacts(b)
    import mods_chapters as M
    M.install(globals())
    for f in (M.create, M.oritech, M.storage, M.relics, M.training, M.building, M.tools_weapons, M.armor, M.raids):
        f(b)
    print('dropped items:', M.MISSING)
    groups_and_titles(b)
    b.write()
    merge_lang()
    total = sum(len(c['quests']) for c in b.chapters.values())
    print(f"{len(b.chapters)} chapters, {total} quests")


# ---------------------------------------------------------------- Getting Started (stage_0)
def getting_started(b):
    c = 'stage_0'
    ch = b.chapters[c]
    hub = '7BFE2B886541122D'
    b.place(c, hub, 0, 0, 'gear', 3.0)
    b.text(c, hub, 'Welcome to Campfiremons', 'Read me first', [
        "Campfiremons is a gym run: beat a leader to reach the next &6stage&r, and each stage opens up more.",
        "",
        "The branches around this quest show you the basics: catching (left), looking after your team (right),",
        "growing your Pokémon (below), finding your way (lower right) and how the pack's stages work (upper left).",
        "",
        "When you're ready, &eBrock&r is waiting on the far right. Your &eTrainer Card&r shows your level cap and",
        "progress, and &aL&r opens the Campfiremons League tab."])

    # Catching (left)
    b.place(c, '07770E338AC86117', -3.25, -0.9, 'circle', 1.25, deps=[hub])
    b.place(c, '0440240B5085D636', -5.5, -0.9, 'circle', 1.0, deps=['07770E338AC86117'])
    apricorn = b.add(c, -3.25, 1.4, 'cobblemon:red_apricorn', [t_item('cobblemon:red_apricorn')],
                     [r_xp(2), r_item('cobblemon:poke_ball', 8)], 'Apricorn Picking', 'Pick a Red Apricorn',
                     ["Apricorn trees grow wild in most biomes; each colour of apricorn crafts different balls.",
                      "Red ones make Poké Balls. Plant the seeds to grow your own tree.",
                      "Better balls only work once you reach their stage."], 'rsquare', 1.0, deps=[hub])
    b.add(c, -5.5, 1.4, 'cobblemon:white_apricorn',
          [t_item(f'cobblemon:{col}_apricorn') for col in
           ('red', 'yellow', 'green', 'blue', 'pink', 'black', 'white')],
          [r_xp(3), r_item('cobblemon:poke_ball', 8)], 'Every Colour', 'Collect all seven apricorns',
          "Seven colours, seven trees. A full apricorn orchard keeps you in balls for the whole run.",
          'square', 0.85, deps=[apricorn], optional=True)
    raid = b.add(c, -7.6, -0.9, 'cobblemonraiddens:raid_pouch', [t_cob('win_raid')],
                 [r_xp(4), r_item('cobblemon:exp_candy_s', 3)], 'Raid Den', 'Win a raid',
                 ["Glowing crystals out in the world are &eRaid Dens&r. Beat the boss with friends (or alone) and",
                  "you get a chance to catch it.",
                  "&e★1&r dens are open now; each gym opens the next star tier."],
                 'circle', 1.0, deps=['0440240B5085D636'])

    # Looking after your team (right)
    heal = b.add(c, 3.25, -1.6, 'cobblemon:healing_machine', [t_item('cobblemon:healing_machine')],
                 [r_xp(2), r_item('cobblemon:potion', 4)], 'Healing Machine', 'Get a Healing Machine',
                 ["Put your party's balls in it to heal them. Pokécenters out in the world have one too,",
                  "and Sophisticated Backpacks can take a healing upgrade."], 'hexagon', 1.25, deps=[hub])
    pc = b.add(c, 5.5, -1.6, 'cobblemon:pc', [t_item('cobblemon:pc')],
               [r_xp(2), r_item('cobblemon:poke_ball', 8)], 'PC', 'Get a PC',
               "Your boxes, from any PC: 60 boxes per PC, plenty of room for a living Pokédex.",
               'hexagon', 1.25, deps=[heal])
    b.add(c, 7.6, -2.6, 'cobblemon:pasture', [t_item('cobblemon:pasture')],
          [r_xp(2), r_item('cobblemon:oran_berry', 6)], 'Pasture', 'Get a Pasture',
          ["Pokémon in a pasture wander nearby and produce items that suit them: wool, eggs, honey and more.",
           "With no farm animals in the pack, pastures are your farms."], 'hexagon', 1.0, deps=[pc])
    trainer = b.add(c, 3.25, 1.4, 'rctmod:trainer_card', [t_cob('defeat_trainer')],
                    [r_xp(3), r_item('cobblemon:potion', 4)], 'First Trainer Battle', 'Beat any trainer',
                    ["Trainers roam the world. Walk up and talk to them to battle.",
                     "Beating the &ekey trainers&r raises your level cap; your Trainer Card lists who's next."],
                    'circle', 1.25, deps=[hub])

    # Growing your Pokémon (below)
    b.place(c, '2CB794566D297784', 0, 3.4, 'circle', 1.25, deps=[hub])
    b.add(c, -2.4, 3.4, 'cobblemon:pokedex_red', [t_cob('scan')],
          [r_xp(2), r_item('cobblemon:exp_candy_xs', 4)], 'Pokédex', 'Scan a Pokémon',
          ["Craft a Pokédex and scan Pokémon to fill in their entries, even the ones you haven't caught yet."],
          'diamond', 1.25, deps=[hub])
    b.add(c, 2.4, 3.4, 'cobblemon:fire_stone', [t_check()], [r_xp(2)], 'More Evolution', 'See the Evolution chapter',
          "Stones, held items and trades: the &eEvolution&r chapter shows every way Pokémon evolve.",
          'diamond', 1.0, deps=['2CB794566D297784'])

    # Finding your way (lower right)
    b.place(c, '509520097CAAFD27', 5.5, 1.4, 'circle', 1.0, deps=[trainer])
    b.add(c, 5.5, 3.4, 'minecraft:filled_map', [t_check()], [r_xp(2), r_item('minecraft:compass')],
          'Finding Your Way', 'Gyms, towns and Pokécenters',
          ["Type &a/gymmap&r for a map to your next gym, with the distance and direction in chat.",
           "Pokémon towns and the Kanto cities have Pokécenters, shops and trainers; Pokécenters and",
           "PokéStops along the way heal your team. Waystones let you teleport between the ones you've found."],
          'diamond', 1.25, deps=['509520097CAAFD27'])

    # How Campfiremons works (upper left)
    stages = b.add(c, -2.6, -3.3, 'minecraft:campfire', [t_check()], [r_xp(2)], 'Stages and the Level Cap',
                   'How progress works',
                   ["Progress is measured in &6stages&r: beat a gym leader to reach the next one.",
                    "Your Pokémon can't gain EXP past your &elevel cap&r: the ace level of your next unbeaten key",
                    "trainer. Trainers won't battle you while a party Pokémon is over it. You can still catch",
                    "anything at any level; box the over-levelled ones before a trainer battle."],
                   'diamond', 1.25, deps=[hub])
    b.add(c, -4.8, -3.3, 'cobblemon:master_ball', [t_check()], [r_xp(2)], 'Legendaries by Stage',
          'When you can catch them',
          ["&eStage 5&r: sub-legendaries. &eStage 6&r: Ultra Beasts and Paradox Pokémon.",
           "&eStage 7&r: mythicals and box legends. Before that you can't battle or catch them."],
          'diamond', 1.0, deps=[stages])
    b.add(c, -0.4, -3.3, 'cobblemon:great_ball', [t_check()], [r_xp(2)], 'Gear by Stage', 'Locked items',
          ["Better balls, Bottle Caps, TMs and the PokéNav can be crafted any time but only used once you",
           "reach their stage. Mega Bracelets, Z-Rings and other power items turn up in structure chests after",
           "the gym that unlocks them, and every player gets their own copy of the loot."],
          'diamond', 1.0, deps=[stages])

    # Brock (far right)
    brock = b.place(c, '1D77FC3C44DE2076', 10.5, 0, 'hexagon', 2.0, deps=[hub], hide_lines=True)
    goal_text(b, c, brock['id'], 'Brock', 'Pewter Gym', 'Pewter', 1)

    ch['images'] = [banner('getting_started', 0, -6.6, 1.6)]
    for i, t in enumerate(TYPES):  # two rows of nine above the banner
        ch['images'].append(type_icon(t, -4.0 + (i % 9), -9.0 + (i // 9) * 1.0))


# ---------------------------------------------------------------- gyms
GYMS = {  # stage reached by beating the goal quest in stage_(n-1): leader, place, Kanto city, where
    1: ('Brock', 'Pewter Gym', 'Pewter', None), 2: ('Misty', 'Cerulean Gym', 'Cerulean', None),
    3: ('Lt. Surge', 'Vermilion Gym', 'Vermilion', None), 4: ('Erika', 'Celadon Gym', 'Celadon', None),
    5: ('Sabrina', 'Saffron Gym', 'Saffron', None), 6: ('Koga', 'Fuchsia Gym', 'Fuchsia', None),
    7: ('Blaine', 'Cinnabar Gym', 'Cinnabar', 'the Nether'), 8: ('Clair', 'Blackthorn Gym', 'Viridian', 'the End'),
}


def goal_text(b, chapter, qid, leader, place, city, stage, where=None):
    desc = [f"{leader} waits in the &e{place}&r" + (f" in {where}" if where else "") + ".",
            "Type &a/gymmap&r for directions to the nearest one" + ("" if where else ", with a map") + "."]
    if city:
        desc.append(f"You can also challenge {leader} in {city}'s gym in the Kanto cities: talk to them there.")
    desc += ["", "Your whole party must be at or under your level cap to battle."]
    b.text(chapter, qid, f"Beat {leader}", f"Reach Stage {stage}", desc)


STAGE_TYPE = {1: 'rock', 2: 'water', 3: 'electric', 4: 'grass', 5: 'psychic', 6: 'poison', 7: 'fire', 8: 'dragon',
              9: 'stellar'}
# Hub slots: U = up-left chain (power items), R = right-up, D = right-down, L = left, B = lower left
SLOT = {'U1': (-1.9, -3.3), 'U2': (-4.2, -3.3), 'R1': (3.0, -2.4), 'R2': (5.2, -2.4), 'D1': (3.0, 2.4),
        'D2': (5.2, 2.4), 'L1': (-3.4, 0), 'B1': (-1.9, 3.3), 'B2': (-4.2, 3.3), 'U3': (1.9, -3.9)}
LAYOUT = {  # stage: hub, goal, {slot: (qid, parent slot or 'hub')}
    1: ('7F9958556C02DF15', '6EFA1D7CDA08F0A4', {'R1': ('35D7D9A5A5A1AEBB', 'hub'), 'D1': ('5404ADE871497700', 'hub'),
                                                  'L1': ('3C85D0F002E65112', 'hub')}),
    2: ('374ED3817109D1AE', '06CA7CC483D0C8F4', {'U1': ('5ECA8FC5E895C86C', 'hub'), 'U2': ('16CFD93FC04F16F8', 'U1'),
                                                  'R1': ('5F400D25B5BCD4D9', 'hub'), 'D1': ('385B0BD23EB96AA2', 'hub'),
                                                  'L1': ('4FF0A1ECD784785A', 'hub'), 'B1': ('48A7DEDFD3D5011B', 'hub')}),
    3: ('1783D60CE9E9DB38', '267B4C856236D8EB', {'U1': ('10A6D6C341C9DE6F', 'hub'), 'U2': ('7D617531A42E36ED', 'U1'),
                                                  'R1': ('42EE0BCEB05AED22', 'hub'), 'D1': ('457B46D8E62CF8AA', 'hub')}),
    4: ('389BB3BBD7ABD021', '5AAE215A3FED46AB', {'R1': ('4A1909D2C33CD3FE', 'hub'), 'D1': ('6B3BF4CF69AB6063', 'hub'),
                                                  'L1': ('0003E6E0530C6E98', 'hub')}),
    5: ('3426FB3074FCED6C', '080EFFF2C23BE2C4', {'U1': ('219C6B0EF7C308FF', 'hub'), 'D1': ('3FF732B035717862', 'hub'),
                                                  'L1': ('34D7A6CED618B0DF', 'hub'), 'B1': ('026F1DF4C892C8EB', 'hub')}),
    6: ('21FDD3645BEC06AC', '242F5963CF4C6819', {'U1': ('77BDF8BC23C0AC35', 'hub'), 'U2': ('69AD611B45A6FE70', 'U1'),
                                                  'R1': ('134977A1494685F1', 'hub'), 'D1': ('6E41E96B40451144', 'hub'),
                                                  'L1': ('619EAA0CB27820B9', 'hub')}),
    7: ('69C0821EA21C4C93', '1F0B4EF36C9FB5B7', {'U1': ('6E95CF8E029955B9', 'hub'), 'U2': ('21D425525C990B07', 'U1'),
                                                  'R1': ('0612A68FC7008D19', 'hub'), 'D1': ('33BAAF0DAA8D5881', 'hub'),
                                                  'L1': ('14F86FB31E011ACE', 'hub')}),
    8: ('4C029B208A6F165B', '7EC34193D0BD8315', {'U1': ('5CF63FA2C8331298', 'hub'), 'U2': ('7F1D37F035F13725', 'U1'),
                                                  'R1': ('1F8AD986D9B689B8', 'hub'), 'R2': ('01F859EDB8C5D546', 'R1'),
                                                  'D1': ('30AE46A577517A11', 'hub'), 'D2': ('2821F035DFC0EBD5', 'D1'),
                                                  'L1': ('056CC15916CA9B0B', 'hub')}),
    9: ('534ACB982620E7AD', None, {'R1': ('7F9748B62E911B11', 'hub'), 'R2': ('7EFFCF53AB81B423', 'R1')}),
}
BANNER_TEXT_FIX = {}


def stage_chapters(b):
    for stage, (hub, goal, slots) in LAYOUT.items():
        c = f'stage_{stage}'
        ch = b.chapters[c]
        hq = b.place(c, hub, 0, 0, 'gear', 2.5)
        for slot, (qid, parent) in slots.items():
            x, y = SLOT[slot]
            pid = hub if parent == 'hub' else slots[parent][0]
            q = b.quest(c, qid)
            big = q.get('tasks', [{}])[0].get('type') == 'advancement'  # power-item finds stand out a little
            shape = {'L1': 'diamond', 'B1': 'diamond'}.get(slot, 'pentagon' if big else 'circle')
            b.place(c, qid, x, y, shape, 1.25 if slot.endswith('1') else 1.0, deps=[pid], hide_lines=False)
        if goal:
            b.place(c, goal, 8.0, 0, 'hexagon', 2.0, deps=[hub], hide_lines=True)
            leader, place, city, where = GYMS[stage + 1] if stage + 1 in GYMS else ('Champion Terry', None, None, None)
            if stage + 1 in GYMS:
                goal_text(b, c, goal, leader, place, city, stage + 1, where)
            else:
                b.text(c, goal, 'Become the Champion', 'Reach Stage 9', [
                    "Beat the Elite Four (Agatha, Bruno, Lance and Lorelei), then &eChampion Terry&r at the",
                    "&eKanto League&r in the End. Type &a/gymmap&r there for directions.",
                    "", "Your whole party must be at or under your level cap to battle."])
        extra(b, c, stage, hub)
        w, h = BANNER_PX[c]
        bw = round(1.6 * w / h, 2)
        ch['images'] = [banner(c, 0, -6.2, 1.6), type_icon(STAGE_TYPE[stage], -bw / 2 - 1.1, -6.2, 1.5),
                        type_icon(STAGE_TYPE[stage], bw / 2 + 1.1, -6.2, 1.5)]
        hq.pop('hide_dependency_lines', None)


def extra(b, c, stage, hub):
    """New quests for a stage's unlocks."""
    x, y = SLOT['B1']
    if stage == 4:
        b.add(c, x, y, 'minecraft:bell', [t_check()], [r_xp(3), r_item('cobblemon:exp_candy_m', 2)],
              'Battle Tower', 'Open from Stage 4',
              ["The &eBattle Tower&r takes challengers from now on: win streaks earn Battle Points to spend",
               "in its shop."], 'diamond', 1.25, deps=[hub])
    if stage == 6:
        b.add(c, x, y, 'cobblemon:beast_ball', [t_check()], [r_xp(3), r_item('cobblemon:exp_candy_l', 2)],
              'Ultra Space', 'Wormholes open from Stage 6',
              ["Rare wormholes lead to &eUltra Space&r, each home to one Ultra Beast. Before Stage 6 you're",
               "sent straight back home."], 'diamond', 1.25, deps=[hub])
    if stage == 9:
        b.add(c, SLOT['D1'][0], SLOT['D1'][1], 'cobblemon:pokedex_black', [t_cob('have_registered', 300)],
              [r_xp(10), r_item('cobblemon:rare_candy', 5)], 'Living Legend', 'Register 300 Pokémon',
              "A Champion's Pokédex. See &eGotta Find 'Em All!&r for the milestones on the way.",
              'circle', 1.25, deps=[hub])


# ---------------------------------------------------------------- Evolution
STONES = [  # stone, ore texture, where to look
    ('fire_stone', 'nether_fire_stone_ore', "Its ore turns up underground and in the Nether."),
    ('water_stone', 'water_stone_ore', "Its ore turns up underground, often near water."),
    ('thunder_stone', 'thunder_stone_ore', "Its ore turns up underground."),
    ('leaf_stone', 'leaf_stone_ore', "Its ore turns up underground."),
    ('moon_stone', 'dripstone_moon_stone_ore', "Its ore turns up underground and in dripstone caves."),
    ('sun_stone', 'terracotta_sun_stone_ore', "Its ore turns up underground and in badlands terracotta."),
    ('shiny_stone', 'shiny_stone_ore', "Its ore turns up underground."),
    ('dusk_stone', 'dusk_stone_ore', "Its ore turns up underground."),
    ('dawn_stone', 'dawn_stone_ore', "Its ore turns up underground."),
    ('ice_stone', 'ice_stone_ore', "Its ore turns up underground in cold places."),
]
HELD = ['kings_rock', 'metal_coat', 'dragon_scale', 'upgrade', 'protector', 'electirizer', 'magmarizer',
        'reaper_cloth']


def title_of(item):
    t = {'kings_rock': "King's Rock", 'upgrade': 'Up-Grade'}.get(item, item.replace('_', ' ').title())
    return t.replace('Poke ', 'Poké ').replace(' Z', '-Z').replace('Charizardite X', 'Charizardite X')


def evolution(b):
    c = 'evolution'
    b.new_chapter(c, 'cobblemon:fire_stone')
    ch = b.chapters[c]
    hub = b.add(c, 0, 0, 'cobblemon:shiny_stone', [t_check()], [r_xp(3), r_item('cobblemon:exp_candy_s', 4)],
                'How Pokémon Evolve', 'Read me', [
                    "Most Pokémon evolve by levelling up. Others need something more:",
                    "&e- Evolution stones&r (around this quest): use one on the Pokémon.",
                    "&e- Held items&r (below): give it the item, then level it up or trade it.",
                    "&e- Friendship, time of day or a trade&r: the Pokédex entry shows how.",
                    "Hold an &eEverstone&r to stop a Pokémon evolving."], 'gear', 2.5)
    e10 = b.add(c, 0, -3.0, 'cobblemon:exp_candy_m', [t_cob('evolve', 10)],
                [r_xp(4), r_item('cobblemon:exp_candy_m', 4)], 'Growth Spurt', 'Evolve 10 Pokémon', None,
                'circle', 1.25, deps=[hub])
    b.add(c, 0, -5.0, 'cobblemon:exp_candy_l', [t_cob('evolve', 25)],
          [r_xp(6), r_item('cobblemon:exp_candy_l', 4)], 'Evolution Expert', 'Evolve 25 Pokémon', None,
          'circle', 1.0, deps=[e10])
    # stones: five each side, with their ore beside them
    for i, (stone, ore, where) in enumerate(STONES):
        side = -1 if i < 5 else 1
        row = i % 5
        x, y = side * (3.4 + (0.6 if row in (1, 3) else 0)), -3.2 + row * 1.6
        b.add(c, x, y, f'cobblemon:{stone}', [t_item(f'cobblemon:{stone}')], [r_xp(2)],
              title_of(stone), 'Find one', [where, "Mining the ore drops the stone; they also turn up in chests."],
              'rsquare', 1.0, deps=[hub], optional=True)
        ch['images'].append(image(f'cobblemon:textures/block/evolution/{ore}.png', x + side * 1.3, y, 0.9, 0.9))
    held_hub = b.add(c, 0, 3.4, 'cobblemon:metal_coat', [t_check()], [r_xp(2)], 'Held-Item Evolutions',
                     'Give it, then level or trade',
                     ["Some Pokémon evolve while holding an item: Onix with a Metal Coat, Seadra with a Dragon",
                      "Scale, Porygon with an Up-Grade... Most of these happen when you &etrade&r the Pokémon",
                      "to a friend, so team up. The items turn up in structure chests and from some Pokémon."],
                     'diamond', 1.25, deps=[hub])
    for i, item in enumerate(HELD):
        x = -3.5 + i
        b.add(c, x, 5.4, f'cobblemon:{item}', [t_item(f'cobblemon:{item}')], [r_xp(1)], title_of(item), None,
              None, 'square', 0.8, deps=[held_hub], optional=True)
    b.add(c, 0, 7.0, 'cobblemon:exp_candy_m', [t_cob('trade_for')], [r_xp(3)], 'Trade Partners',
          'Trade a Pokémon with a friend', "Some evolutions only happen in a trade. Bring the item, then swap.",
          'circle', 1.0, deps=[held_hub])
    ch['images'] += [banner('evolution', 0, -7.4, 1.6)]


# ---------------------------------------------------------------- Gotta Find 'Em All
FOSSILS = ['helix_fossil', 'dome_fossil', 'old_amber_fossil', 'root_fossil', 'claw_fossil', 'skull_fossil',
           'armor_fossil', 'cover_fossil', 'plume_fossil', 'jaw_fossil', 'sail_fossil']


def gotta_find(b):
    c = 'gotta_find_em_all'
    b.new_chapter(c, 'cobblemon:pokedex_red')
    ch = b.chapters[c]
    ch['images'] = [image('campfiremons:textures/quests/pokedex_panel.png', 0, -1.1, 19.0, 12.8),
                    banner('gotta_find_em_all', 0, -10.6, 1.7),
                    banner('archaeology', -4.6, -5.6, 1.1), banner('fishing', 4.6, -5.6, 1.1)]
    # Pokédex milestones across the top of the screen
    prev = None
    for i, (n, title, reward) in enumerate([(50, 'Researcher', 'exp_candy_m'), (150, 'Collector', 'exp_candy_l'),
                                            (300, 'Living Pokédex', 'rare_candy')]):
        prev = b.add(c, -2.2 + i * 2.2, -8.7, 'cobblemon:pokedex_red', [t_cob('have_registered', n)],
                     [r_xp(4 + 3 * i), r_item(f'cobblemon:{reward}', 3)], title, f'Register {n} Pokémon',
                     "Every Pokémon you catch is registered in your Pokédex." if i == 0 else None,
                     'gear' if i == 2 else 'circle', 1.25 if i == 2 else 1.0, deps=[prev] if prev else ())
    # Archaeology (left screen)
    brush = b.add(c, -7.0, -3.6, 'minecraft:brush', [t_item('minecraft:brush')], [r_xp(1)], 'Brush', 'Craft a brush',
                  "Brush &esuspicious sand and gravel&r at ruins and dig sites to uncover fossils.",
                  'rsquare', 1.0)
    analyzer = b.add(c, -4.6, -3.6, 'cobblemon:fossil_analyzer', [t_item('cobblemon:fossil_analyzer')], [r_xp(2)],
                     'Fossil Analyzer', 'Craft one', None, 'hexagon', 1.0, deps=[brush])
    tank = b.add(c, -2.2, -3.6, 'cobblemon:restoration_tank', [t_item('cobblemon:restoration_tank')], [r_xp(2)],
                 'Restoration Tank', 'Craft one',
                 "Place it next to the Fossil Analyzer with a Monitor on top; the recipe viewer shows the parts.",
                 'hexagon', 1.0, deps=[analyzer])
    revive = b.add(c, -4.6, -1.4, 'cobblemon:helix_fossil', [t_cob('revive_fossil')],
                   [r_xp(5), r_item('cobblemon:exp_candy_m', 3)], 'Back to Life', 'Revive a fossil',
                   "Feed a fossil into the machine and wait: an ancient Pokémon wakes up.", 'heart', 1.75,
                   deps=[tank])
    for i, fossil in enumerate(FOSSILS):
        x, y = -7.3 + (i % 6) * 1.08, 1.2 + (i // 6) * 1.25
        b.add(c, x, y, f'cobblemon:{fossil}', [t_item(f'cobblemon:{fossil}')], [r_xp(1)], title_of(fossil), None,
              None, 'square', 0.8, deps=[revive], optional=True)
    # Fishing (right screen)
    rod = b.add(c, 4.6, -3.6, 'cobblemon:poke_rod', [t_item('cobblemon:poke_rod')], [r_xp(2)], 'Poké Rod',
                'Craft one', "A Poké Rod fishes up Pokémon instead of fish. Better balls make better rods.",
                'gear', 1.5)
    bait = b.add(c, 4.6, -1.6, 'cobblemon:poke_bait', [t_item('cobblemon:poke_bait')], [r_xp(1)], 'Poké Bait',
                 'Make some bait', "Bait on the rod changes what bites: try berries and other treats.",
                 'rsquare', 1.0, deps=[rod])
    first = b.add(c, 4.6, 0.4, 'cobblemon:poke_rod', [t_cob('fishing')], [r_xp(3), r_item('cobblemon:poke_ball', 8)],
                  'Something Bit!', 'Fish up a Pokémon', None, 'circle', 1.25, deps=[bait])
    b.add(c, 4.6, 2.6, 'cobblemon:dive_ball', [t_cob('fishing', 25)],
          [r_xp(6), r_item('cobblemon:exp_candy_m', 4)], 'Master Angler', 'Fish up 25 Pokémon', None,
          'heart', 1.75, deps=[first])


# ---------------------------------------------------------------- Poké Balls
BALL_RINGS = [  # centre ball, stage it's usable from, the other balls of that stage
    ('poke_ball', 0, ['premier_ball', 'heal_ball', 'safari_ball', 'citrine_ball', 'verdant_ball', 'azure_ball',
                      'roseate_ball', 'slate_ball', 'ancient_poke_ball', 'ancient_feather_ball', 'ancient_heavy_ball']),
    ('great_ball', 1, ['net_ball', 'dive_ball', 'nest_ball', 'level_ball', 'lure_ball', 'heavy_ball', 'moon_ball',
                       'friend_ball', 'fast_ball', 'sport_ball', 'park_ball', 'ancient_great_ball', 'ancient_wing_ball',
                       'ancient_leaden_ball']),
    ('ultra_ball', 3, ['quick_ball', 'dusk_ball', 'timer_ball', 'repeat_ball', 'luxury_ball', 'love_ball',
                       'ancient_ultra_ball', 'ancient_jet_ball', 'ancient_gigaton_ball']),
    ('beast_ball', 6, ['dream_ball']),
    ('master_ball', 9, ['ancient_origin_ball']),
]
BALL_TEXT = {
    0: ["Poké Balls and the apricorn balls work from the start. Craft them from apricorns: the recipe viewer",
        "shows every one."],
    1: ["Beating Brock unlocks &eGreat Balls&r and the specialty balls of the same tier: Net, Dive, Nest,",
        "Level, Lure and more. Each is better in its own situation."],
    3: ["Beating Lt. Surge unlocks &eUltra Balls&r with Quick, Dusk, Timer, Repeat, Luxury and Love Balls."],
    6: ["Beating Koga unlocks the &eBeast Ball&r (best on Ultra Beasts, poor on everything else) and the",
        "Dream Ball."],
    9: ["The &eMaster Ball&r never misses. You get one as the Champion; there's no recipe."],
}


def poke_balls(b):
    c = 'poke_balls'
    b.new_chapter(c, 'cobblemon:poke_ball')
    ch = b.chapters[c]
    ch['images'] = [banner('poke_balls', 0, -6.4, 1.6)]
    import math
    x = -15.5
    for centre, stage, others in BALL_RINGS:
        r = max(1.8, len(others) * 1.05 / (2 * math.pi)) if len(others) > 1 else 1.7
        x += r + 1.2
        size = 2 * r + 2.0
        ch['images'].append(image(f'cobblemon:textures/item/poke_balls/{centre}.png', x, 0, size, size))
        cid = b.add(c, x, 0, f'cobblemon:{centre}', [t_item(f'cobblemon:{centre}')],
                    [r_xp(3), r_item(f'cobblemon:{centre}', 4)], f"{title_of(centre)}s",
                    'Usable from the start' if stage == 0 else f'Usable from Stage {stage}', BALL_TEXT[stage],
                    'gear', 1.75)
        for i, ball in enumerate(others):
            ang = -math.pi / 2 + i * 2 * math.pi / len(others) if len(others) > 1 else math.pi / 2
            b.add(c, round(x + r * math.cos(ang), 2), round(r * math.sin(ang), 2), f'cobblemon:{ball}',
                  [t_item(f'cobblemon:{ball}')], [r_xp(1)], title_of(ball), None, None, 'circle', 0.75,
                  deps=[cid], optional=True)
        x += r + 1.2


# ---------------------------------------------------------------- Battle Gimmicks
GIMMICKS = [  # banner, stage, (find, use) quests in that stage chapter, items to collect, arm direction
    ('mega_evolution', 2, ('5ECA8FC5E895C86C', '16CFD93FC04F16F8'),
     ['venusaurite', 'charizardite_x', 'blastoisinite', 'gengarite', 'gyaradosite', 'lucarionite', 'garchompite',
      'mewtwonite_x'], (-1, -1)),
    ('z_moves', 3, ('10A6D6C341C9DE6F', '7D617531A42E36ED'),
     ['normalium_z', 'firium_z', 'waterium_z', 'grassium_z', 'electrium_z', 'psychium_z', 'dragonium_z',
      'darkinium_z', 'fairium_z'], (1, -1)),
    ('terastallizing', 6, ('77BDF8BC23C0AC35', '69AD611B45A6FE70'),
     [f'{t}_tera_shard' for t in ('normal', 'fire', 'water', 'grass', 'electric', 'psychic', 'dragon', 'dark',
                                   'stellar')], (-1, 1)),
    ('dynamaxing', 7, ('6E95CF8E029955B9', '21D425525C990B07'),
     ['dynamax_candy', 'max_mushroom', 'max_soup', 'max_honey'], (1, 1)),
]


def battle_gimmicks(b):
    c = 'battle_gimmicks'
    b.new_chapter(c, 'mega_showdown:omni_ring')
    ch = b.chapters[c]
    hub = b.add(c, 0, 0, 'mega_showdown:omni_ring', [t_check()], [r_xp(3)], 'Battle Gimmicks', 'Four ways to power up',
                ["&eMega Evolution&r opens at Stage 2, &eZ-Moves&r at 3, &eTerastallizing&r at 6 and &eDynamaxing&r at 7.",
                 "Each needs its key item (Mega Bracelet, Z-Ring, Tera Orb, Dynamax Band), which turns up in",
                 "structure chests once you reach that stage. Gym leaders from then on use the gimmick too."],
                'gear', 2.25)
    ch['images'] = [banner('battle_gimmicks', 0, -7.2, 1.6)]
    for name, stage, (find, use), items, (sx, sy) in GIMMICKS:
        link(ch, find, sx * 2.0, sy * 1.7, 1.25, 'pentagon')
        link(ch, use, sx * 3.7, sy * 2.9, 1.0)
        w, h = BANNER_PX[name]
        ch['images'].append(banner(name, sx * 4.4, sy * 4.4, 1.0))
        for i, item in enumerate(items):
            col, row = i % 4, i // 4
            b.add(c, round(sx * (5.6 + col * 1.0), 2), round(sy * (0.9 + row * 1.0), 2), f'mega_showdown:{item}',
                  [t_item(f'mega_showdown:{item}')], [r_xp(1)], title_of(item), f'Stage {stage}', None, 'square', 0.7,
                  deps=[hub], optional=True)
    for q in ch['quests']:
        if q['id'] != hub:
            q['hide_dependency_lines'] = Raw('true')


# ---------------------------------------------------------------- Legends: Legendary, Ultra Beasts, Paradox
import json as _json
SPECIES = _json.load(open(Path(__file__).parent / 'data' / 'species_labels.json'))
PAST = ['greattusk', 'screamtail', 'brutebonnet', 'fluttermane', 'slitherwing', 'sandyshocks', 'roaringmoon',
        'walkingwake', 'gougingfire', 'ragingbolt']
FUTURE = ['irontreads', 'ironbundle', 'ironhands', 'ironjugulis', 'ironmoth', 'ironthorns', 'ironvaliant',
          'ironleaves', 'ironboulder', 'ironcrown']


def tier(name):
    labels = set(SPECIES[name]['labels'])
    for label, t in (('restricted', 'box'), ('mythical', 'mythical'), ('ultra_beast', 'ub'), ('paradox', 'paradox'),
                     ('legendary', 'sub')):
        if label in labels:
            return t


def species_quest(b, c, name, x, y, stage, size=0.8, shape='rsquare', xp=3, deps=()):
    return b.add(c, x, y, poke_icon(name), [t_cob('catch', pokemon=f'cobblemon:{name}')], [r_xp(xp)],
                 SPECIES[name].get('display') or name.title(), f'Catchable from Stage {stage}', None, shape, size,
                 deps=deps, optional=True)


def legends(b):
    import math
    by_dex = sorted(SPECIES, key=lambda n: (SPECIES[n]['dex'], n))
    # Legendary
    c = 'legendary'
    b.new_chapter(c, 'cobblemon:master_ball')
    ch = b.chapters[c]
    ch['images'] = [banner('legendary', 0, -7.6, 1.8)]
    x0 = -14.0
    for t, label, stage, cols, link_to in [('sub', 'sub_legendary', 5, 8, '219C6B0EF7C308FF'),
                                            ('box', 'box_legends', 7, 6, '0612A68FC7008D19'),
                                            ('mythical', 'mythical', 7, 6, '0612A68FC7008D19')]:
        names = [n for n in by_dex if tier(n) == t]
        rows = math.ceil(len(names) / cols)
        w, h = cols * 1.05 + 1.4, rows * 1.05 + 1.6
        cx = x0 + w / 2
        ch['images'] += [image('campfiremons:textures/quests/gold_panel.png', cx, -4.6 + h / 2, w + 0.6, h + 0.6),
                         banner(label, cx, -5.6, 1.0)]
        link(ch, link_to, x0 + 0.9, -3.9, 1.0, 'gear')
        for i, n in enumerate(names):
            species_quest(b, c, n, round(x0 + 1.5 + (i % cols) * 1.05 - 0.5, 2), round(-2.7 + (i // cols) * 1.05, 2),
                          stage)
        x0 += w + 1.0
    # Ultra Beasts
    c = 'ultra_beasts'
    b.new_chapter(c, 'cobblemon:beast_ball')
    ch = b.chapters[c]
    ch['images'] = [image('campfiremons:textures/quests/wormhole.png', 0, 0, 13.0, 13.0),
                    banner('ultra_beasts', 0, -7.4, 1.6)]
    hub = b.add(c, 0, 0, 'cobblemon:beast_ball', [t_check()], [r_xp(3)], 'Ultra Beasts', 'Catchable from Stage 6',
                ["Ultra Beasts come from &eUltra Space&r: rare wormholes open in the world, each leading to one",
                 "beast's home. You can enter from Stage 6; before that you're sent straight back.",
                 "&eBeast Balls&r (Stage 6) catch them far more easily than any other ball."], 'gear', 2.25)
    link(ch, '134977A1494685F1', 0, -2.1, 1.0)
    ubs = [n for n in by_dex if tier(n) == 'ub']
    for i, n in enumerate(ubs):
        ang = -math.pi / 2 + i * 2 * math.pi / len(ubs)
        species_quest(b, c, n, round(4.6 * math.cos(ang), 2), round(4.6 * math.sin(ang), 2), 6, 1.1, 'rsquare', 4)
    # Paradox
    c = 'paradox'
    b.new_chapter(c, 'minecraft:clock')
    ch = b.chapters[c]
    ch['images'] = [banner('paradox', 0, -3.6, 1.6),
                    image('campfiremons:textures/quests/past_tiles.png', -7.4, 0, 6.5, 2.6),
                    image('campfiremons:textures/quests/future_tiles.png', 7.4, 0, 6.5, 2.6),
                    banner('past', -7.4, 2.3, 1.1), banner('future', 7.4, 2.3, 1.1)]
    hub = b.add(c, 0, 0, 'minecraft:clock', [t_check()], [r_xp(3)], 'Paradox Pokémon', 'Catchable from Stage 6',
                ["Ancient Pokémon from the &cpast&r and machines from the &bfuture&r. Both kinds can be caught",
                 "from Stage 6. &eKoraidon&r and &eMiraidon&r are box legends: those wait for Stage 7."], 'gear', 2.25)
    link(ch, '134977A1494685F1', 0, 2.1, 1.0)
    for side, names, legend in ((-1, PAST, 'koraidon'), (1, FUTURE, 'miraidon')):
        for i, n in enumerate(names):
            species_quest(b, c, n, round(side * 7.4 + (i % 5 - 2) * 1.3, 2), round((i // 5 - 0.5) * 1.3, 2), 6,
                          0.95, 'rsquare', 4)
        species_quest(b, c, legend, side * 3.1, 0, 7, 1.6, 'pentagon', 10, deps=[hub])

# ---------------------------------------------------------------- Artifacts
ART = {
    'head': ['plastic_drinking_hat', 'novelty_drinking_hat', 'villager_hat', 'superstitious_hat', 'cowboy_hat',
             'anglers_hat', 'snorkel', 'night_vision_goggles'],
    'necklace': ['lucky_scarf', 'scarf_of_invisibility', 'cross_necklace', 'panic_necklace', 'shock_pendant',
                 'flame_pendant', 'thorn_pendant', 'charm_of_sinking', 'charm_of_shrinking'],
    'hands': ['digging_claws', 'feral_claws', 'power_glove', 'fire_gauntlet', 'pocket_piston', 'vampiric_glove',
              'golden_hook', 'onion_ring', 'pickaxe_heater', 'withered_bracelet'],
    'belt': ['cloud_in_a_bottle', 'obsidian_skull', 'antidote_vessel', 'universal_attractor', 'crystal_heart',
             'helium_flamingo', 'chorus_totem', 'warp_drive'],
    'feet': ['aqua_dashers', 'bunny_hoppers', 'kitty_slippers', 'running_shoes', 'snowshoes', 'steadfast_spikes',
             'flippers', 'rooted_boots', 'strider_shoes'],
    'other': ['umbrella', 'whoopee_cushion', 'eternal_steak', 'everlasting_beef'],
}


def artifacts(b):
    import math
    c = 'artifacts'
    b.new_chapter(c, 'artifacts:crystal_heart')
    ch = b.chapters[c]
    hub = b.add(c, 0, 0, 'minecraft:chest', [t_check()], [r_xp(3)], 'Artifacts', 'Trinkets with a twist',
                ["Artifacts are magic trinkets: hats, necklaces, gloves, belts and shoes, each with its own power.",
                 "They turn up in structure chests, and some chests are &cMimics&r that bite back.",
                 "Wear them in the accessory slots in your inventory."], 'gear', 2.25)
    ch['images'] = [banner('artifacts', 11.0, -4.6, 1.8)]

    def one(item, x, y, shape='rsquare'):
        b.add(c, round(x, 2), round(y, 2), f'artifacts:{item}', [t_item(f'artifacts:{item}')], [r_xp(2)],
              title_of(item), None, None, shape, 0.85, deps=[hub], optional=True)

    def grid(items, cx, cy, cols, shape='rsquare'):
        rows = math.ceil(len(items) / cols)
        for i, item in enumerate(items):
            r, col = i // cols, i % cols
            n = min(cols, len(items) - r * cols)  # centre short rows
            one(item, cx + (col - (n - 1) / 2) * 1.05, cy + (r - (rows - 1) / 2) * 1.05, shape)

    grid(ART['head'], 0, -5.6, 4)
    ch['images'].append(banner('slot_head', 0, -3.9, 1.0))
    for i, item in enumerate(ART['necklace']):  # a ring under the hub, like a necklace
        ang = math.pi * (0.05 + 0.9 * i / (len(ART['necklace']) - 1))
        one(item, 2.6 * math.cos(ang) * -1, 1.0 + 2.2 * math.sin(ang), 'circle')
    ch['images'].append(banner('slot_necklace', 0, 4.0, 1.0))
    grid(ART['hands'][:5], -6.0, -0.4, 2, 'diamond')
    grid(ART['hands'][5:], 6.0, -0.4, 2, 'diamond')
    ch['images'] += [banner('slot_hands', -6.0, 1.9, 1.0), banner('slot_hands', 6.0, 1.9, 1.0)]
    grid(ART['belt'], 0, 5.8, 4)
    ch['images'].append(banner('slot_belt', 0, 7.6, 1.0))
    grid(ART['feet'][:5], -2.9, 9.3, 3, 'hexagon')
    grid(ART['feet'][5:], 2.9, 9.3, 2, 'hexagon')
    ch['images'] += [banner('slot_feet', -2.9, 11.0, 1.0), banner('slot_feet', 2.9, 11.0, 1.0)]
    grid(ART['other'], 11.0, -2.6, 4, 'circle')
    for q in ch['quests']:
        if q['id'] != hub:
            q['hide_dependency_lines'] = Raw('true')


# ---------------------------------------------------------------- groups, order, chapter titles
def groups_and_titles(b):
    guide, legend_group, gyms, mods_group = new_id(), new_id(), new_id(), new_id()
    (Q / 'chapter_groups.snbt').write_text(dump({'chapter_groups': [{'id': guide}, {'id': legend_group},
                                                                   {'id': gyms}, {'id': mods_group}]}) + '\n')
    (Q / 'lang/en_us/chapter_group.snbt').write_text(dump({f'chapter_group.{guide}.title': 'Guide',
                                                           f'chapter_group.{legend_group}.title': 'Legends',
                                                           f'chapter_group.{gyms}.title': 'Gym Challenge',
                                                           f'chapter_group.{mods_group}.title': 'Mods & Gear'}) + '\n')
    guide_chapters = ['stage_0', 'evolution', 'poke_balls', 'battle_gimmicks', 'training', 'raids',
                      'gotta_find_em_all']
    legend_chapters = ['legendary', 'ultra_beasts', 'paradox']
    mod_chapters = ['tools_weapons', 'armor', 'artifacts', 'relics', 'storage', 'building', 'create', 'oritech']
    order = guide_chapters + legend_chapters + [f'stage_{n}' for n in range(1, 10)] + mod_chapters
    titles = {'stage_0': 'Getting Started', 'evolution': 'Evolution', 'poke_balls': 'Poké Balls',
              'battle_gimmicks': 'Battle Gimmicks', 'gotta_find_em_all': "Gotta Find 'Em All!", 'artifacts': 'Artifacts',
              'training': 'Training', 'raids': 'Raid Dens', 'tools_weapons': 'Tools & Weapons', 'armor': 'Armor',
              'relics': 'Relics', 'storage': 'Storage', 'building': 'Home & Building', 'create': 'Create',
              'oritech': 'Oritech',
              'legendary': 'Legendary', 'ultra_beasts': 'Ultra Beasts', 'paradox': 'Paradox',
              'stage_1': 'Stage 1: Boulder Badge', 'stage_2': 'Stage 2: Cascade Badge',
              'stage_3': 'Stage 3: Thunder Badge', 'stage_4': 'Stage 4: Rainbow Badge',
              'stage_5': 'Stage 5: Marsh Badge', 'stage_6': 'Stage 6: Soul Badge', 'stage_7': 'Stage 7: Volcano Badge',
              'stage_8': 'Stage 8: Rising Badge', 'stage_9': 'Stage 9: Champion'}
    chapter_lang = {}
    for i, name in enumerate(order):
        ch = b.chapters[name]
        ch['order_index'] = Raw(str(i))
        ch['group'] = (guide if name in guide_chapters else legend_group if name in legend_chapters
                       else mods_group if name in mod_chapters else gyms)
        chapter_lang[f"chapter.{ch['id']}.title"] = titles[name]
    (Q / 'lang/en_us/chapter.snbt').write_text(dump(chapter_lang) + '\n')


def merge_lang():
    """FTB Quests 2101 reads one table per language, lang/<locale>.snbt; a lang/<locale>/ folder of split files loads
    as an empty table (players see untitled quests). Merge everything into lang/en_us.snbt and drop the folder."""
    import shutil
    folder = Q / 'lang' / 'en_us'
    table = {}
    for f in sorted(folder.rglob('*.snbt')):
        table.update(parse(f.read_text()))
    (Q / 'lang' / 'en_us.snbt').write_text(dump(table) + '\n')
    shutil.rmtree(folder)
    data = parse((Q / 'data.snbt').read_text())
    data['fallback_locale'] = 'en_us'  # players on another English (en_au, en_gb) still get the text
    (Q / 'data.snbt').write_text(dump(data) + '\n')
    print(f"lang/en_us.snbt: {len(table)} entries")


if __name__ == '__main__':
    main()
