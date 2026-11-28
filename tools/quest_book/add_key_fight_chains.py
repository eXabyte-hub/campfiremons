#!/usr/bin/env python3
"""Stage chapters end with the badge they're named after, the key fights stand in line before the gym, and the
level cap is spelled out (asked for on 2026-11-22). In place: rebuild.sh is off (it re-IDs quests).

Each stage chapter runs from one badge to the next (Stage 1: from Brock to Misty). Its title used to name the badge
you already had; now it names the one at the end ("Stage 1: Cascade Badge"), with that gym's banner colours and type
icons, and Stage 9, after the Champion, becomes "Hall of Fame". No quest changes chapter, so nobody's progress moves.
Between the badge hub and the gym quest, on the same line, one quest per key fight (RCT's Radical Red series, in
order; rival variants are one quest, the Elite Four one quest with four parts), each completed by RCT's own "defeat"
advancement, so fights already won tick off by themselves. The gym quest keeps its dependency on the hub, so nothing
new can block a gym. The hub, each fight and each gym quest say the level cap (RCT's: the strongest Pokémon of the
next key trainer you haven't beaten; 15 before Brock).
Safe to re-run: it does nothing once the fight quests exist.
    python3 tools/quest_book/add_key_fight_chains.py [path/to/rctmod.jar]
"""
import glob
import json
import os
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_book as bb  # noqa: E402
import gen_finds  # noqa: E402
import gen_key_trainers  # noqa: E402  BIOMES, readable()
from snbt import Raw, dump, mods_dir, parse  # noqa: E402

Q = bb.Q
LANG = Q / 'lang' / 'en_us.snbt'
ART = Path(__file__).resolve().parents[2] / 'kubejs' / 'assets' / 'campfiremons' / 'textures' / 'quests'
SERIES = 'radicalred'
INITIAL_CAP = 15  # defaultconfigs/rctmod-server.toml initialLevelCap
# Stage n's chapter ends with: (title badge, gym leader's name, gym type icon)
GOALS = {1: ('Cascade Badge', 'Misty', 'water'), 2: ('Thunder Badge', 'Lt. Surge', 'electric'),
         3: ('Rainbow Badge', 'Erika', 'grass'), 4: ('Marsh Badge', 'Sabrina', 'psychic'),
         5: ('Soul Badge', 'Koga', 'poison'), 6: ('Volcano Badge', 'Blaine', 'fire'),
         7: ('Earth Badge', 'Clair', 'dragon'), 8: ('Champion', 'Champion Terry', 'stellar'),
         9: ('Hall of Fame', None, 'stellar')}
E4_ORDER = ('lorelei', 'bruno', 'agatha', 'lance')
CHAIN_X, CHAIN_STEP, GYM_GAP = 2.6, 1.6, 2.2


def snbt_string(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def esc(s):
    return s.replace('&', '\\&')  # FTB reads & as formatting


def load_series(jar):
    """[(stage, [fight, ...], gym ace)] with fight = dict(name, ace, ids, advancements, biomes, icon, e4)."""
    z = zipfile.ZipFile(jar)
    names = set(z.namelist())
    mobs = {n.rsplit('/', 1)[1][:-5]: json.loads(z.read(n)) for n in names
            if n.startswith('data/rctmod/mobs/trainers/single/') and n.endswith('.json')}
    keys = {t: m for t, m in mobs.items() if SERIES in m.get('series', []) and not m.get('optional', False)}

    def reqs(m):
        r = m.get('requiredDefeats', [])
        r = r.get(SERIES, []) if isinstance(r, dict) else r
        return {x for g in r for x in (g if isinstance(g, list) else [g])}
    depth = {}

    def d(t):
        if t not in depth:
            depth[t] = 0
            depth[t] = 1 + max((d(x) for x in reqs(keys[t]) if x in keys), default=0)
        return depth[t]
    team = {t: json.loads(z.read(f'data/rctmod/trainers/{t}.json')) for t in keys}
    ace = {t: max(p['level'] for p in team[t]['team']) for t in keys}
    adv = {}
    for n in names:
        if n.startswith('data/rctmod/advancement/trainers/defeat_') and n.endswith('.json'):
            crit = json.loads(z.read(n))['criteria']
            if len(crit) != 1:
                continue  # "defeat all of the Elite Four": one criterion per member; we want each one's own
            for i in next(iter(crit.values())).get('conditions', {}).get('trainer_ids') or []:
                if i in keys:
                    adv.setdefault(i, 'rctmod:trainers/' + n.rsplit('/', 1)[1][:-5])
    gym_depth = {n: d(ids[0]) for n, ids in gen_finds.STAGE_TRAINERS.items()}
    gym_depth[0] = 0
    out = []
    for n in range(9):
        lo, hi = gym_depth[n], gym_depth[n + 1]
        groups = {}
        for t in sorted((t for t in keys if lo < d(t) < hi), key=lambda t: (d(t), t)):
            e4 = keys[t].get('type') == 'e4'
            key = ('e4', d(t)) if e4 else (team[t]['name'], d(t))
            g = groups.setdefault(key, {'name': 'The Elite Four' if e4 else team[t]['name'], 'ace': ace[t],
                                        'ids': [], 'adv': [], 'biomes': [], 'members': {}, 'e4': e4})
            g['ids'].append(t)
            if adv.get(t) and adv[t] not in g['adv']:
                g['adv'].append(adv[t])
            for b in keys[t].get('biomeTagWhitelist', []):
                if b not in g['biomes']:
                    g['biomes'].append(b)
            if e4:
                g['members'][team[t]['name'].split()[-1]] = keys[t].get('biomeTagWhitelist', [])
        fights = list(groups.values())
        for g in fights:
            best = [p for p in team[g['ids'][0]]['team'] if p['level'] == g['ace']]
            g['icon'] = (bb.poke_icon(best[-1]['species'].split()[0]) if len(g['ids']) == 1 and best
                         else {'id': 'rctmod:trainer_card'})
            if g['e4']:
                g['adv'].sort(key=lambda a: next((i for i, m in enumerate(E4_ORDER) if m in a), 9))
        leader = gen_finds.STAGE_TRAINERS[n + 1][0]
        out.append((n, fights, ace[leader]))
    return out


def main(jar):
    chapters = {f.stem: (f, parse(f.read_text())) for f in sorted((Q / 'chapters').glob('*.snbt'))}
    for f, c in chapters.values():
        if any(str(t.get('advancement', '')).startswith('rctmod:') for q in c['quests'] for t in q.get('tasks', [])):
            print('The key-fight quests are already in the book')
            return
        bb.USED.add(c['id'])
        for q in c['quests']:
            bb.USED.add(q['id'])
            for x in q.get('tasks', []) + q.get('rewards', []):
                bb.USED.add(x['id'])
        for x in c.get('images', []) + c.get('quest_links', []):
            bb.USED.add(x['id'])
    series = load_series(jar)
    lang = parse(LANG.read_text())
    lines = LANG.read_text().splitlines()

    def set_line(key, value):
        i = next(i for i, l in enumerate(lines) if l.startswith(f'\t{key}: '))
        lines[i] = f'\t{key}: {snbt_string(value)}'

    def set_desc(qid, desc):
        start = next(i for i, l in enumerate(lines) if l.startswith(f'\tquest.{qid}.quest_desc: ['))
        end = next(i for i in range(start, len(lines)) if lines[i].strip() == ']')
        lines[start + 1:end] = ['\t\t' + snbt_string(s) for s in desc]

    def stage_quest(ch, adv):
        return next(q for q in ch['quests'] if any(t.get('advancement') == adv for t in q.get('tasks', [])))

    new_lang = {}
    import gen_quest_art
    from PIL import Image
    for n, fights, gym_ace in series:
        f, ch = chapters[f'stage_{n}']
        gym = stage_quest(ch, f'campfiremons:stage/{n + 1}')
        caps = [g['ace'] for g in fights] + [gym_ace]
        if n == 0:
            caps = [max(INITIAL_CAP, c) for c in caps]
        cap_range = f'{caps[0]} → {caps[-1]}' if caps[0] != caps[-1] else str(caps[0])
        leader = GOALS[n][1] if n else 'Brock'
        # The gym quest: the cap until you win
        gdesc = lang[f"quest.{gym['id']}.quest_desc"]
        gdesc = [l for l in gdesc if not l.startswith('Level cap until you win')]
        gdesc[-1:] = [gdesc[-1], f'Level cap until you win: &e{gym_ace if n else caps[-1]}&r'
                      + (f" ({leader}'s strongest Pokémon)." if n else '.')]
        set_desc(gym['id'], gdesc)
        if n == 0:
            continue  # Getting Started keeps its title and has no key fights
        hub = stage_quest(ch, f'campfiremons:stage/{n}')
        hdesc = [l for l in lang[f"quest.{hub['id']}.quest_desc"] if not l.startswith('Level cap')]
        hdesc += ['', f'Level cap on the road to {leader}: &e{cap_range}&r' +
                  (', rising with each key fight in the line to the right.' if fights else '.')]
        set_desc(hub['id'], hdesc)
        # Chain: hub -> fights -> (in line with) the gym
        prev, x = hub['id'], CHAIN_X
        for g in fights:
            qid = bb.new_id()
            tasks = [{'advancement': a, 'criterion': '', 'id': bb.new_id(), 'type': 'advancement'} for a in g['adv']]
            ch['quests'].append({'dependencies': [prev], 'icon': g['icon'], 'id': qid, 'rewards': [bb.r_xp(3)],
                                 'shape': 'hexagon', 'size': bb.d(1.1), 'tasks': tasks, 'x': bb.d(x),
                                 'y': bb.d(0)})
            new_lang[f'quest.{qid}.title'] = esc(g['name'])
            new_lang[f'quest.{qid}.quest_subtitle'] = f"Key fight, Lv{g['ace']}"
            if g['e4']:
                where = [f"&e{m}&r: {gen_key_trainers.readable(g['members'][m])}"
                         for m in (k.capitalize() for k in E4_ORDER) if m in g['members']]
                desc = ['Beat all four, in any order. Each one has a Lv85 team, so your level cap stays at '
                        f"&e{g['ace']}&r until the Champion.", '', 'Where they spawn, 25 to 70 blocks from you:'] + \
                       ['- ' + w for w in where]
            else:
                desc = [f"Until you beat them, your level cap stays at &e{g['ace']}&r (their strongest Pokémon).",
                        '',
                        f"They spawn 25 to 70 blocks from you while you're in or near: "
                        f"{gen_key_trainers.readable(g['biomes'])}.",
                        'You get a chat message when they turn up.']
            new_lang[f'quest.{qid}.quest_desc'] = desc
            prev, x = qid, round(x + CHAIN_STEP, 2)
        if fights:
            gx = float(str(gym['x'])[:-1])
            if gx < x - CHAIN_STEP + GYM_GAP:
                gym['x'] = bb.d(round(x - CHAIN_STEP + GYM_GAP, 2))
            before = next((q for q in ch['quests'] if lang.get(f"quest.{q['id']}.title", '').startswith('Before ')),
                          None)
            if before:
                bdesc = lang[f"quest.{before['id']}.quest_desc"]
                bdesc[0] = f'These key trainers stand between you and {leader}, in this order (the quests in line to the right):'
                set_desc(before['id'], bdesc)
        f.write_text(dump(ch) + '\n')

    # Titles, banners and type icons: each stage chapter is named after the badge at its end
    for n in range(1, 10):
        f, ch = chapters[f'stage_{n}']
        goal, _, typ = GOALS[n]
        set_line(f"chapter.{ch['id']}.title", f'Stage {n}: {goal}')
        title, top, bottom = gen_quest_art.BANNERS[f'stage_{n}']
        png = ART / f'stage_{n}.png'
        gen_quest_art.banner(title, top, bottom).save(png)
        w, h = Image.open(png).size
        f2, ch = chapters[f'stage_{n}'][0], parse(chapters[f'stage_{n}'][0].read_text())
        ban = next(im for im in ch['images'] if im['image'].endswith(f'/stage_{n}.png'))
        height = float(str(ban['height'])[:-1])
        width = round(height * w / h, 2)
        ban['width'] = bb.d(width)
        for im in ch['images']:
            if 'tera_types/' in im['image'] and float(str(im['y'])[:-1]) == float(str(ban['y'])[:-1]):
                im['image'] = re.sub(r'tera_types/[a-z]+\.png', f'tera_types/{typ}.png', im['image'])
                side = 1 if float(str(im['x'])[:-1]) > 0 else -1
                im['x'] = bb.d(round(side * (width / 2 + 1.1), 3))
        f2.write_text(dump(ch) + '\n')

    first_quest = next(i for i, l in enumerate(lines) if l.startswith('\tquest.'))
    block = []
    for k, v in new_lang.items():
        if isinstance(v, list):
            block += [f'\t{k}: ['] + [f'\t\t{snbt_string(s)}' for s in v] + ['\t]']
        else:
            block.append(f'\t{k}: {snbt_string(v)}')
    lines[first_quest:first_quest] = block
    LANG.write_text('\n'.join(lines) + '\n')
    print(f"Added {sum(len(f) for _, f, _ in series)} key-fight quests; retitled Stages 1-9")


if __name__ == '__main__':
    jar = sys.argv[1] if len(sys.argv) > 1 else next(iter(sorted(glob.glob(os.path.join(mods_dir(), 'rctmod-*.jar')))), None)
    if not jar:
        sys.exit('no rctmod jar: pass its path')
    main(jar)
