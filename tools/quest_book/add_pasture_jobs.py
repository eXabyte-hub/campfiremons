#!/usr/bin/env python3
"""Adds the Pasture Jobs chapter (Cobbleworkers) to the live book, in place (rebuild.sh is off: it re-IDs quests).

Cobbleworkers gives pastured Pokémon jobs by type, ability, move or species, but nothing in game said which. This
writes chapters/pasture_jobs.snbt in the Guide group, right after Training (Raid Dens and Gotta Find 'Em All move
down one), with a hub (get a Pasture), three setup quests and one optional quest per kind of worker, each with a
Pokémon icon; the text goes into lang/en_us.snbt, and the Pasture quest in Getting Started points here. The jobs are
Cobbleworkers 2.0.7's (data/cobbleworkers/jobs in its jar) plus our Teleport job (DESIGN.md, Teleport job).
Safe to re-run: it does nothing once the chapter exists.
    python3 tools/quest_book/add_pasture_jobs.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_book as bb  # noqa: E402
from snbt import Raw, dump, parse  # noqa: E402

Q = bb.Q
LANG = Q / 'lang' / 'en_us.snbt'
FILE = 'pasture_jobs'
GUIDE = '502FAE08F3920C75'
AFTER = 'training'  # the new chapter takes the next order_index; later Guide chapters move down one
PASTURE_QUEST_TITLE = 'Pasture'

HUB = ('Pasture Jobs', 'Put your Pokémon to work', [
    'Pokémon in a &ePasture&r take on jobs that suit their type, ability or moves: farming, keeping furnaces '
    'burning, fishing, digging up treasure and more.',
    '',
    'They work the blocks within 8 blocks of the pasture (5 up or down) and bring what they make to a chest or '
    'barrel nearby. A Pokémon does any job it qualifies for, and each quest here is one kind of worker.',
])

SETUP = [  # (icon item, task item or None, title, subtitle, description)
    ('minecraft:chest', None, 'Drop-off', 'A chest by the pasture', [
        'Workers carry what they make to a container near the pasture: a chest, barrel or the like, within 8 '
        'blocks of it and 5 up or down. Keep some room in it.']),
    ('cobbleworkers:worker_inventory_selector', 'cobbleworkers:worker_inventory_selector',
     'Worker Inventory Selector', 'Choose the drop-off', [
         'Right-click a container with it to make it the drop-off for pastures in range; right-click again to undo. '
         'Pastures with no chosen container use any one nearby.',
         '',
         'Crafted from paper, a red apricorn and string.']),
    ('minecraft:red_bed', None, 'Day Off', 'Stop a worker', [
        'Open a pastured Pokémon\'s interaction wheel and choose &eRest&r to stop it working. Choose it again to '
        'send it back to work.']),
]

ROWS = [  # (banner, [(Pokémon icon, title, subtitle, description), ...])
    ('jobs_farming', [
        ('bulbasaur', 'Farmers', 'Grass types', [
            'Harvest fully grown crops (wheat, carrots, potatoes, beetroot, most modded crops, revival herbs, '
            'vivichokes, medicinal leeks), berries, sweet berry and galarica nut bushes, mistleaf and verdroot, '
            'and leave them planted to grow again.',
            '',
            'Hearty grains are picked whole, so replant those yourself.']),
        ('ledyba', 'Apricorn Pickers', 'Bug types', [
            'Pick ripe apricorns and leave the tree to grow more.']),
        ('clefairy', 'Mint Growers', 'Fairy types', [
            'Pick grown mints and leave them planted.']),
        ('gastly', 'Nether Wart Farmers', 'Ghost types', [
            'Harvest grown nether wart and leave it planted.']),
        ('pikachu', 'Voltaconia Pickers', 'Electric types', [
            'Pick voltaconia and replant its seed.']),
        ('ralts', 'Tidy Minds', 'Psychic types', [
            'Pick lucibell and replant its seed, and pick up items lying on the ground around the pasture.']),
    ]),
    ('jobs_machines', [
        ('charmander', 'Stokers', 'Fire types', [
            'Keep furnaces, smokers and blast furnaces burning while they have something to smelt, and fill empty '
            'cauldrons with lava.']),
        ('squirtle', 'Water Workers', 'Water types', [
            'Fill empty cauldrons with water, keep farmland wet and put out fires. Standing in water, they also '
            'fish: a catch every minute and a half.']),
        ('swinub', 'Snow Makers', 'Ice types', [
            'Fill empty cauldrons with powder snow.']),
        ('dratini', 'Brewing Helpers', 'Dragon types', [
            'Top up the fuel of brewing stands, so you need less blaze powder.']),
    ]),
    ('jobs_treasure', [
        ('meowth', 'Pickup', 'The Pickup ability', [
            'A Pokémon with Pickup finds something every three and a half minutes: held items, Poké Balls, '
            'evolution stones, EXP candy, healing items, type gems or apricorn seeds.']),
        ('diglett', 'Diggers', 'Ground types', [
            'Dig in dirt, gravel, mud, coarse dirt or rooted dirt with open air above it, turning up raw ores and '
            'other finds every four minutes.']),
        ('geodude', 'Amethyst Miners', 'Rock types', [
            'Break grown amethyst clusters. Budding amethyst grows new ones.']),
        ('magnemite', 'Tumblestone Miners', 'Steel types', [
            'Break grown tumblestone, black tumblestone and sky tumblestone clusters. They grow back from the budding '
            'block left behind.']),
        ('wailmer', 'Divers', 'Knows Dive', [
            'A Pokémon that knows Dive, standing in water, brings up treasure every three and a half minutes.']),
    ]),
    ('jobs_helpers', [
        ('ekans', 'Fletchers', 'Poison types', [
            'Pick up arrows lying around the pasture and turn them into Arrows of Poison.']),
        ('chansey', 'Healers', 'Knows a healing move', [
            'A Pokémon that knows Wish, Soft-Boiled, Moonlight, Recover, Roost, Heal Bell, Aromatherapy, Synthesis, '
            'Rest or Life Dew gives players near the pasture a short Regeneration boost.']),
        ('slowpoke', 'Rain Dancer', 'Slowpoke', [
            'A pastured Slowpoke calls rain at most every ten minutes. That is rain for the whole world, so check '
            'with your friends first.']),
        ('combee', 'Honey Makers', 'Combee and Vespiquen', [
            'Fill beehives with honey and collect honeycombs from full ones. Three honeycombs and a glass bottle make a '
            'honey bottle.']),
        ('abra', 'Ender Pearls', 'Knows Teleport', [
            'A Pokémon that knows Teleport fetches an &eEnder Pearl&r from an &eEnder Chest&r near the pasture every '
            'two or three minutes. Walkers like Natu and Ralts work more steadily than floaty Abra.']),
    ]),
]
ART = Path(__file__).resolve().parents[2] / 'kubejs' / 'assets' / 'campfiremons' / 'textures' / 'quests'
ROW_Y, ROW_X, STEP = 2.8, 4.0, 1.6  # rows 2.8 apart (a label above each), quests 1.6 apart from x = 4


def banner(name, x, y, height):
    """An image for one of gen_quest_art's banners, drawn into kubejs/assets first if it isn't there."""
    png = ART / f'{name}.png'
    if not png.exists():
        import gen_quest_art
        title, top, bottom = gen_quest_art.BANNERS[name]
        gen_quest_art.banner(title, top, bottom).save(png)
    from PIL import Image
    w, h = Image.open(png).size
    return bb.image(f'campfiremons:textures/quests/{name}.png', round(x, 2), round(y, 2), round(height * w / h, 2), height)


def snbt_string(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main():
    path = Q / 'chapters' / f'{FILE}.snbt'
    if path.exists():
        print('The Pasture Jobs chapter is already in the book')
        return
    chapters = {f.stem: (f, parse(f.read_text())) for f in sorted((Q / 'chapters').glob('*.snbt'))}
    for f, c in chapters.values():  # every ID in the book, so the new ones can't collide
        bb.USED.add(c['id'])
        for q in c['quests']:
            bb.USED.add(q['id'])
            for x in q.get('tasks', []) + q.get('rewards', []):
                bb.USED.add(x['id'])
        for x in c.get('images', []) + c.get('quest_links', []):
            bb.USED.add(x['id'])

    # Order: right after Training in the Guide group
    after = int(str(chapters[AFTER][1]['order_index']))
    for f, c in chapters.values():
        if c.get('group') == GUIDE and int(str(c['order_index'])) > after:
            text = f.read_text()
            old = f"\torder_index: {c['order_index']}\n"
            assert old in text, f.name
            f.write_text(text.replace(old, f"\torder_index: {int(str(c['order_index'])) + 1}\n", 1))

    lang = {}
    quests = []

    def quest(x, y, icon, tasks, xp, title, sub, desc, shape='circle', size=1.0, deps=(), optional=True):
        qid = bb.new_id()
        q = {'icon': icon if isinstance(icon, dict) else {'id': icon}, 'id': qid, 'rewards': [bb.r_xp(xp)],
             'shape': shape, 'size': bb.d(size), 'tasks': tasks, 'x': bb.d(x), 'y': bb.d(y)}
        if deps:
            q['dependencies'] = list(deps)
            q['hide_dependency_lines'] = Raw('true')
        if optional:
            q['optional'] = Raw('true')
        quests.append(q)
        lang[f'quest.{qid}.title'] = title
        lang[f'quest.{qid}.quest_subtitle'] = sub
        lang[f'quest.{qid}.quest_desc'] = desc
        return qid

    hub = quest(0, 0, 'cobblemon:pasture', [bb.t_item('cobblemon:pasture')], 3, *HUB, shape='gear', size=2.0,
                optional=False)
    images = []
    for i, (icon, task, title, sub, desc) in enumerate(SETUP):
        quest(-3.5, (i - 1) * 1.6, icon, [bb.t_item(task)] if task else [bb.t_check()], 2, title, sub, desc,
              shape='rsquare', deps=[hub])
    images.append(banner('jobs_setup', -3.5, -2.8, 0.7))
    for r, (label, row) in enumerate(ROWS):
        y = (r - (len(ROWS) - 1) / 2) * ROW_Y
        for c, (mon, title, sub, desc) in enumerate(row):
            quest(ROW_X + c * STEP, y, bb.poke_icon(mon), [bb.t_check()], 1, title, sub, desc, shape='hexagon',
                  deps=[hub])
        images.append(banner(label, ROW_X + (len(row) - 1) * STEP / 2, y - 1.15, 0.7))
    top = -((len(ROWS) - 1) / 2) * ROW_Y - 1.15
    images.append(banner('pasture_jobs', ROW_X / 2 + 1.5, top - 1.5, 1.5))

    cid = bb.new_id()
    ch = {'default_hide_dependency_lines': Raw('false'), 'default_quest_shape': '', 'filename': FILE,
          'group': GUIDE, 'icon': {'id': 'cobblemon:pasture'}, 'id': cid, 'images': images,
          'order_index': Raw(str(after + 1)), 'quest_links': [], 'quests': quests}
    path.write_text(dump(ch) + '\n')

    # Text: chapter title with the other chapter titles, quest keys with the other quest keys
    lines = LANG.read_text().splitlines()
    first_chapter = next(i for i, l in enumerate(lines) if l.startswith('\tchapter.'))
    lines.insert(first_chapter, f'\tchapter.{cid}.title: "Pasture Jobs"')
    new = []
    for k, v in lang.items():
        if isinstance(v, list):
            new.append(f'\t{k}: [')
            new += [f'\t\t{snbt_string(s)}' for s in v]
            new.append('\t]')
        else:
            new.append(f'\t{k}: {snbt_string(v)}')
    first_quest = next(i for i, l in enumerate(lines) if l.startswith('\tquest.'))
    lines[first_quest:first_quest] = new

    # The Getting Started pasture quest points here instead of explaining jobs itself
    book = parse('\n'.join(lines) + '\n')
    pasture = [k.split('.')[1] for k, v in book.items() if k.endswith('.title') and v == PASTURE_QUEST_TITLE
               and k.startswith('quest.')]
    if len(pasture) == 1:
        start = next(i for i, l in enumerate(lines) if l.startswith(f'\tquest.{pasture[0]}.quest_desc: ['))
        end = next(i for i in range(start, len(lines)) if lines[i].strip() == ']')
        keep = [l for l in lines[start + 1:end] if 'work the blocks' not in l and 'Teleport' not in l
                and 'Ender Chest' not in l and 'put what they make' not in l]
        while keep and keep[-1].strip() == '""':
            keep.pop()
        keep += ['\t\t""', '\t\t' + snbt_string('Pastured Pokémon also do jobs: see the &ePasture Jobs&r chapter.')]
        lines[start + 1:end] = keep
    else:
        print(f'note: found {len(pasture)} "{PASTURE_QUEST_TITLE}" quests, left their text alone')
    LANG.write_text('\n'.join(lines) + '\n')
    print(f'Added the Pasture Jobs chapter {cid}: {len(quests)} quests')


if __name__ == '__main__':
    main()
