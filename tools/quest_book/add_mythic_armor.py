#!/usr/bin/env python3
"""Adds the Mythic Upgrades armour sets to the live Armor chapter, in place (rebuild.sh is off: it re-IDs quests).

The builder skipped them: the KubeJS dump gives their material as "?" and armor() keeps only sets with a known
material (their tools did make it into Tools & Weapons). This puts a "Mythic Upgrades" banner under the trainer hats
and one quest per full set below it, in the style of the vanilla sets: all four pieces, 3 levels, optional, sorted by
armour. Safe to re-run: it does nothing once the chapter has Mythic Upgrades quests.
    python3 tools/quest_book/add_mythic_armor.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_book as bb  # noqa: E402
from snbt import Raw, dump, parse  # noqa: E402

Q = bb.Q
REPO = Path(__file__).resolve().parents[2]
ART = REPO / 'kubejs' / 'assets' / 'campfiremons' / 'textures' / 'quests'
LANG = Q / 'lang' / 'en_us.snbt'
ORDER = ('helmet', 'chestplate', 'leggings', 'boots')
BANNER = 'mythic_armor'


def snbt_string(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main():
    path = Q / 'chapters' / 'armor.snbt'
    text = path.read_text()
    ch = parse(text)
    assert dump(ch) + '\n' == text, 'armor.snbt would be reformatted; stopping'
    if any(str((t.get('item') or {}).get('id', '')).startswith('mythicupgrades:')
           for q in ch['quests'] for t in q.get('tasks', [])):
        print('The Armor chapter already has the Mythic Upgrades sets')
        return

    for f in (Q / 'chapters').glob('*.snbt'):  # every ID in the book, so the new ones can't collide
        c = parse(f.read_text())
        bb.USED.add(c['id'])
        for q in c['quests']:
            bb.USED.add(q['id'])
            for x in q.get('tasks', []) + q.get('rewards', []):
                bb.USED.add(x['id'])
        for x in c.get('images', []) + c.get('quest_links', []):
            bb.USED.add(x['id'])

    sets = {}
    for line in open(Path(__file__).parent / 'data' / 'dump.txt'):
        if 'mythicupgrades:' in line and '] armor ' in line:
            a = json.loads(line.split('] armor ', 1)[1])
            if a['type'] in ORDER:
                sets.setdefault(a['id'].split(':')[1].rsplit('_', 1)[0], {})[a['type']] = (a['id'], a['def'])
    sets = {m: v for m, v in sets.items() if len(v) == 4}  # full four-piece sets only
    names = sorted(sets, key=lambda m: (sum(p[1] for p in sets[m].values()), m))
    if not names:
        sys.exit('no Mythic Upgrades armour sets in data/dump.txt')

    lang_text = LANG.read_text()
    lang = parse(lang_text)
    hub = next(q['id'] for q in ch['quests'] if lang.get(f"quest.{q['id']}.title") == 'Armor')

    png = ART / f'{BANNER}.png'
    if not png.exists():
        import gen_quest_art
        title, top, bottom = gen_quest_art.BANNERS[BANNER]
        gen_quest_art.banner(title, top, bottom).save(png)
    from PIL import Image
    w, h = Image.open(png).size
    bottom_edge = max(float(q['y'][:-1]) + float(q.get('size', '1.0d')[:-1]) / 2 for q in ch['quests'])
    by = round(bottom_edge + 1.3, 2)
    ch['images'].append(bb.image(f'campfiremons:textures/quests/{BANNER}.png', 0, by, round(w / h, 2), 1.0))

    per_row, new_lang = 8, {}
    for i, m in enumerate(names):
        row, col = divmod(i, per_row)
        in_row = min(per_row, len(names) - row * per_row)
        x, y = round((col - (in_row - 1) / 2) * 1.3, 2), round(by + 1.4 + row * 1.3, 2)
        pieces = {t: sets[m][t][0] for t in ORDER}
        qid = bb.new_id()
        ch['quests'].append({'dependencies': [hub], 'hide_dependency_lines': Raw('true'),
                             'icon': {'id': pieces['chestplate']}, 'id': qid, 'optional': Raw('true'),
                             'rewards': [bb.r_xp(3)], 'shape': 'hexagon', 'size': bb.d(1.0),
                             'tasks': [bb.t_item(pieces[t]) for t in ORDER], 'x': bb.d(x), 'y': bb.d(y)})
        armour = sum(p[1] for p in sets[m].values())
        new_lang[f'quest.{qid}.title'] = f"{m.replace('_', ' ').title()} Armor"
        new_lang[f'quest.{qid}.quest_subtitle'] = f'All four pieces, {armour} armor'
    path.write_text(dump(ch) + '\n')

    # Text: the new quests' keys go in with the other quest keys, and the hub mentions Mythic Upgrades
    lines = lang_text.splitlines()
    first_quest = next(i for i, l in enumerate(lines) if l.startswith('\tquest.'))
    lines[first_quest:first_quest] = [f'\t{k}: {snbt_string(v)}' for k, v in new_lang.items()]
    start = next(i for i, l in enumerate(lines) if l.startswith(f'\tquest.{hub}.quest_desc: ['))
    end = next(i for i in range(start, len(lines)) if lines[i].strip() == ']')
    lines.insert(end, '\t\t' + snbt_string('&eMythic Upgrades&r gems make sets past netherite, at the bottom.'))
    LANG.write_text('\n'.join(lines) + '\n')
    print(f"Added {len(names)} Mythic Upgrades sets: " + ', '.join(f"{m} ({sum(p[1] for p in sets[m].values())})" for m in names))


if __name__ == '__main__':
    main()
