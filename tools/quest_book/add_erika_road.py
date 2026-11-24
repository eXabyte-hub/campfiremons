#!/usr/bin/env python3
"""Stage 3 gets its prerequisites in the book like the other gyms (asked for on 2026-11-24), in place (rebuild.sh is off:
it re-IDs quests).

RCT's Radical Red series has key fights before every gym but Brock and Erika. Brock has "The Road to Brock"
(add_boulder_chapter.py), so Stage 3 gets "The Road to Erika" between the Thunder Badge and Beat Erika: no key fights,
the level cap, where to go. It also makes the Thunder Badge quest depend on Beat Lt. Surge: every other badge hub depends
on the gym before it, and this one lost its link in the 2026-11-10 layout change. Both quests complete on the same stage
advancement, so nobody's progress moves.
Safe to re-run: it does nothing once the road quest exists.
    python3 tools/quest_book/add_erika_road.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_book as bb  # noqa: E402
from snbt import dump, parse  # noqa: E402

Q = bb.Q
LANG = Q / 'lang' / 'en_us.snbt'
BEAT_SURGE = '06CA7CC483D0C8F4'
TITLE = 'The Road to Erika'
SUBTITLE = 'No key fights'
DESC = [
    'Erika, the Celadon City gym leader, is your next badge. There are no key fights before Erika: you can battle as soon '
    "as you've beaten Lt. Surge.",
    '',
    'Level cap until you win: &e44&r.',
    'Type &a/gymmap&r for directions to the nearest &eCeladon Gym&r.',
    '',
    'Winning earns the &eRainbow Badge&r and Stage 4, and opens &eStage 4: Marsh Badge&r.',
]


def snbt_string(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main():
    if TITLE in LANG.read_text():
        print('The Road to Erika is already in the book')
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
    assert any(q['id'] == BEAT_SURGE for q in chapters['stage_2']['quests'])
    ch = chapters['stage_3']
    hub = next(q for q in ch['quests'] if any(t.get('advancement') == 'campfiremons:stage/3' for t in q['tasks']))
    assert not hub.get('dependencies')
    hub['dependencies'] = [BEAT_SURGE]
    road = bb.new_id()
    ch['quests'].append({'dependencies': [hub['id']], 'icon': bb.poke_icon('venusaur'), 'id': road, 'rewards': [bb.r_xp(2)],
                         'shape': 'hexagon', 'size': bb.d(1.1), 'tasks': [bb.t_check()], 'x': bb.d(4.0), 'y': bb.d(0)})
    (Q / 'chapters' / 'stage_3.snbt').write_text(dump(ch) + '\n')

    lines = LANG.read_text().splitlines()
    first_quest = next(i for i, l in enumerate(lines) if l.startswith('\tquest.'))
    lines[first_quest:first_quest] = ([f'\tquest.{road}.quest_desc: ['] + [f'\t\t{snbt_string(s)}' for s in DESC] +
                                      ['\t]', f'\tquest.{road}.quest_subtitle: {snbt_string(SUBTITLE)}',
                                       f'\tquest.{road}.title: {snbt_string(TITLE)}'])
    LANG.write_text('\n'.join(lines) + '\n')
    print(f'Added "{TITLE}" ({road}); Thunder Badge now depends on Beat Lt. Surge')


if __name__ == '__main__':
    main()
