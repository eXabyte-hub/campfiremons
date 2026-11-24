import sys, re, zipfile, glob, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from snbt import parse, mods_dir
from type_tooltips import link, tooltip
Q = Path(__file__).resolve().parents[2] / 'config' / 'ftbquests' / 'quests'
MODS = mods_dir()
items, textures = set(), set()
for jar in glob.glob(MODS + '/*.jar'):
    try: z = zipfile.ZipFile(jar)
    except Exception: continue
    for n in z.namelist():
        m = re.match(r'assets/([a-z0-9_]+)/models/item/([a-z0-9_/]+)\.json$', n)
        if m: items.add(f'{m.group(1)}:{m.group(2)}')
        m = re.match(r'assets/([a-z0-9_]+)/(textures/.+\.png)$', n)
        if m: textures.add(f'{m.group(1)}:{m.group(2)}')
for p in (Path(__file__).resolve().parents[2] / 'kubejs' / 'assets').rglob('*.png'):
    rel = p.relative_to(str(Path(__file__).resolve().parents[2] / 'kubejs' / 'assets')); textures.add(f'{rel.parts[0]}:{"/".join(rel.parts[1:])}')
LANG = parse((Q / 'lang' / 'en_us.snbt').read_text())
# FTB Quests reads &<code> as formatting; any other & ("Tools & Weapons") shows "Invalid formatting!" and must be \&
for k, v in LANG.items():
    for line in (v if isinstance(v, list) else [v]):
        if re.search(r'(?<!\\)&(?![0-9a-fk-orA-FK-OR])', line): problems_lang = globals().setdefault('problems_lang', []); problems_lang.append(f'{k}: bare & in "{line[:60]}" (write \\&)')
ids, quests, problems = collections.Counter(), {}, []
chapters = {}
for f in sorted((Q / 'chapters').glob('*.snbt')):
    ch = parse(f.read_text()); chapters[f.stem] = ch
    lang = LANG
    ids[ch['id']] += 1
    for q in ch['quests']:
        ids[q['id']] += 1; quests[q['id']] = f.stem
        for x in q.get('tasks', []) + q.get('rewards', []): ids[x['id']] += 1
        if f'quest.{q["id"]}.title' not in lang and not any((t.get('type') == 'cobblemon_tasks:cobblemon_task' and t.get('pokemon')) or t.get('type') == 'item' for t in q.get('tasks', [])):
            problems.append(f'{f.stem}: quest {q["id"]} has no title')
        icon = q.get('icon', {}).get('id')
        for it in [icon] + [t.get('item', {}).get('id') for t in q.get('tasks', []) + q.get('rewards', []) if t.get('type') == 'item']:
            if it and not it.startswith('minecraft:') and it not in items: problems.append(f'{f.stem}: unknown item {it}')
    for im in ch.get('images', []):
        ids[im['id']] += 1
        if im['image'] not in textures and not im['image'].startswith('minecraft:'): problems.append(f'{f.stem}: missing texture {im["image"]}')
    for l in ch.get('quest_links', []): ids[l['id']] += 1
for name, ch in chapters.items():
    for q in ch['quests']:
        for dep in q.get('dependencies', []):
            if dep not in quests: problems.append(f'{name}: {q["id"]} depends on missing {dep}')
    for l in ch.get('quest_links', []):
        if l['linked_quest'] not in quests: problems.append(f'{name}: link to missing {l["linked_quest"]}')
# Chapters are numbered as FTB Quests saves them, 0, 1, 2... within each group: any other numbers put a changed chapter in
# the wrong place on the server (see renumber_chapters.py; Stage 0 in v0.1.45, Stage 3 in v0.1.47)
order = collections.defaultdict(list)
for name, ch in chapters.items(): order[ch.get('group', '')].append((int(str(ch['order_index'])), name))
for g, rows in order.items():
    if [i for i, _ in sorted(rows)] != list(range(len(rows))): problems.append(f'chapter order in group {g} is not 0..{len(rows) - 1}: {sorted(rows)} (run renumber_chapters.py)')
# A type icon's tooltip and link must be its own type's (v0.1.44 changed the stage icons' pictures only)
for name, ch in chapters.items():
    for im in ch.get('images', []):
        m = re.search(r'tera_types/(\w+)\.png$', im['image'])
        if m and im.get('click_action') != link(m.group(1)): problems.append(f'{name}: {m.group(1)} icon links to {im.get("click_action")} (run type_tooltips.py)')
        if m and LANG.get(f'image.{im["id"]}.title') != '\\n'.join(tooltip(m.group(1))): problems.append(f'{name}: {m.group(1)} icon has another type\'s tooltip or none (run type_tooltips.py)')
dupes = [i for i, n in ids.items() if n > 1]
problems += globals().get('problems_lang', [])
# FTB Quests reads IDs as signed longs: one at or above 8000000000000000 gets a new random ID on every load, losing
# its text, links and progress (half the v0.1.10 book did)
problems += [f'id {i} is out of range (>= 8000000000000000)' for i in ids if int(i, 16) >= 1 << 63]
print(len(chapters), 'chapters,', len(quests), 'quests; duplicate ids:', dupes[:5])
print('\n'.join(problems[:30]) or 'no problems'); print(len(problems), 'problems')

# overlaps: quests too close to each other, and quests under a banner (images from campfiremons: named like banners)
over = []
for name, ch in chapters.items():
    pts = [(float(q['x'][:-1]), float(q['y'][:-1]), float(q.get('size', '1.0d')[:-1]), q['id']) for q in ch['quests']]
    pts += [(float(l['x'][:-1]), float(l['y'][:-1]), float(l.get('size', '1.0d')[:-1]), 'link') for l in ch.get('quest_links', [])]
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            a, b = pts[i], pts[j]
            if ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 < (a[2] + b[2]) / 2 * 0.92:
                over.append(f'{name}: quests overlap at ({a[0]},{a[1]}) and ({b[0]},{b[1]})')
    for im in ch.get('images', []):
        path = im['image']
        if not path.startswith('campfiremons:textures/quests/') or any(k in path for k in ('panel', 'wormhole', 'tiles')):
            continue
        x, y, w, h = (float(im[k][:-1]) for k in ('x', 'y', 'width', 'height'))
        for px, py, sz, _ in pts:
            if abs(px - x) < w / 2 + sz / 2 * 0.6 and abs(py - y) < h / 2 * 0.75 + sz / 2 * 0.6:
                over.append(f'{name}: quest at ({px},{py}) under banner {path.rsplit("/",1)[1]}')
for name, ch in chapters.items():
    bs = [im for im in ch.get('images', []) if im['image'].startswith('campfiremons:textures/quests/') and not any(k in im['image'] for k in ('panel', 'wormhole', 'tiles'))]
    for i in range(len(bs)):
        for j in range(i + 1, len(bs)):
            a, b = bs[i], bs[j]
            ax, ay, aw, ah = (float(a[k][:-1]) for k in ('x', 'y', 'width', 'height'))
            bx, by, bw, bh = (float(b[k][:-1]) for k in ('x', 'y', 'width', 'height'))
            if abs(ax - bx) < (aw + bw) / 2 * 0.95 and abs(ay - by) < (ah + bh) / 2 * 0.8:
                over.append(f"{name}: banners overlap {a['image'].rsplit('/',1)[1]} / {b['image'].rsplit('/',1)[1]}")
print(len(over), 'overlaps'); print('\n'.join(over[:40]))
