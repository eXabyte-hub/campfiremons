#!/usr/bin/env python3
"""Adds "Stage 0: Boulder Badge" to the top of the Gym Challenge group, in place (rebuild.sh is off: it re-IDs quests).

Since v0.1.44 each stage chapter is named after the badge at its end (add_key_fight_chains.py), so the Boulder
Badge, earned in Getting Started's "Beat Brock", had no chapter of its own. This one shows the road to Brock like the
others: Getting Started's welcome quest and its Beat Brock quest as quest links (the same quests, so they complete in
both places and nobody's progress moves) with a "Road to Brock" quest between them (level cap, where Brock is), under
a Boulder Badge banner with Rock type icons.
Safe to re-run: it does nothing once the chapter exists.
    python3 tools/quest_book/add_boulder_chapter.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_book as bb  # noqa: E402
from snbt import Raw, dump, parse  # noqa: E402

Q = bb.Q
LANG = Q / 'lang' / 'en_us.snbt'
ART = Path(__file__).resolve().parents[2] / 'kubejs' / 'assets' / 'campfiremons' / 'textures' / 'quests'
FILE = 'boulder_badge'
GYM_GROUP = '33ACE78A3A205CA0'
WELCOME = '7BFE2B886541122D'  # Getting Started: Welcome to Campfiremons
BEAT_BROCK = '1D77FC3C44DE2076'  # Getting Started: Beat Brock
ROAD = ('The Road to Brock', 'Your first gym', [
    'Brock, the Pewter City gym leader, is your first badge. There are no key fights before him.',
    '',
    'Level cap until you win: &e15&r.',
    'He waits in the &ePewter Gym&r: type &a/gymmap&r for directions to the nearest one.',
    '',
    'Beating him earns the &eBoulder Badge&r and Stage 1, and opens &eStage 1: Cascade Badge&r.',
])


def snbt_string(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main():
    path = Q / 'chapters' / f'{FILE}.snbt'
    if path.exists():
        print('The Boulder Badge chapter is already in the book')
        return
    chapters = {f.stem: parse(f.read_text()) for f in sorted((Q / 'chapters').glob('*.snbt'))}
    for c in chapters.values():  # every ID in the book, so the new ones can't collide
        bb.USED.add(c['id'])
        for q in c['quests']:
            bb.USED.add(q['id'])
            for x in q.get('tasks', []) + q.get('rewards', []):
                bb.USED.add(x['id'])
        for x in c.get('images', []) + c.get('quest_links', []):
            bb.USED.add(x['id'])
    first = min(int(str(c['order_index'])) for c in chapters.values() if c.get('group') == GYM_GROUP)

    # Banner and Rock type icons, laid out like the stage chapters'
    import gen_quest_art
    from PIL import Image
    png = ART / f'{FILE}.png'
    if not png.exists():
        title, top, bottom = gen_quest_art.BANNERS[FILE]
        gen_quest_art.banner(title, top, bottom).save(png)
    w, h = Image.open(png).size
    width = round(1.6 * w / h, 2)
    tera = next(im['image'] for im in chapters['stage_1']['images'] if 'tera_types/' in im['image'])
    rock = re.sub(r'tera_types/[a-z]+\.png', 'tera_types/rock.png', tera)
    images = [bb.image(f'campfiremons:textures/quests/{FILE}.png', 4.0, -3.2, width, 1.6),
              bb.image(rock, 4.0 - round(width / 2 + 1.1, 3), -3.2, 1.5, 1.5),
              bb.image(rock, 4.0 + round(width / 2 + 1.1, 3), -3.2, 1.5, 1.5)]

    road = bb.new_id()
    quests = [{'dependencies': [WELCOME], 'icon': bb.poke_icon('onix'), 'id': road, 'rewards': [bb.r_xp(2)],
               'shape': 'hexagon', 'size': bb.d(1.1), 'tasks': [bb.t_check()], 'x': bb.d(4.0), 'y': bb.d(0)}]
    links = [{'id': bb.new_id(), 'linked_quest': WELCOME, 'shape': 'gear', 'size': bb.d(2.5), 'x': bb.d(0),
              'y': bb.d(0)},
             {'id': bb.new_id(), 'linked_quest': BEAT_BROCK, 'shape': 'hexagon', 'size': bb.d(2.0), 'x': bb.d(8.0),
              'y': bb.d(0)}]
    cid = bb.new_id()
    ch = {'default_hide_dependency_lines': Raw('false'), 'default_quest_shape': '', 'filename': FILE,
          'group': GYM_GROUP, 'icon': {'id': 'cobblemon:poke_ball'}, 'id': cid, 'images': images,
          'order_index': Raw(str(first - 1)), 'quest_links': links, 'quests': quests}
    path.write_text(dump(ch) + '\n')

    lines = LANG.read_text().splitlines()
    first_chapter = next(i for i, l in enumerate(lines) if l.startswith('\tchapter.'))
    lines.insert(first_chapter, f'\tchapter.{cid}.title: "Stage 0: Boulder Badge"')
    title, sub, desc = ROAD
    first_quest = next(i for i, l in enumerate(lines) if l.startswith('\tquest.'))
    lines[first_quest:first_quest] = ([f'\tquest.{road}.quest_desc: ['] + [f'\t\t{snbt_string(s)}' for s in desc] +
                                      ['\t]', f'\tquest.{road}.quest_subtitle: {snbt_string(sub)}',
                                       f'\tquest.{road}.title: {snbt_string(title)}'])
    LANG.write_text('\n'.join(lines) + '\n')
    print(f'Added "Stage 0: Boulder Badge" ({cid}), order {first - 1}')


if __name__ == '__main__':
    main()
