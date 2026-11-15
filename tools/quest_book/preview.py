import sys, re, zipfile, glob, io, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).parent))
from snbt import parse, mods_dir
Q = Path(__file__).resolve().parents[2] / 'config' / 'ftbquests' / 'quests'
MODS = mods_dir()
tex = {}
for jar in glob.glob(MODS + '/*.jar'):
    try: z = zipfile.ZipFile(jar)
    except Exception: continue
    for n in z.namelist():
        m = re.match(r'assets/([a-z0-9_]+)/(textures/.+\.png)$', n)
        if m: tex.setdefault(f'{m.group(1)}:{m.group(2)}', (z, n))
for p in (Path(__file__).resolve().parents[2] / 'kubejs' / 'assets').rglob('*.png'):
    rel = p.relative_to(str(Path(__file__).resolve().parents[2] / 'kubejs' / 'assets')); tex[f'{rel.parts[0]}:{"/".join(rel.parts[1:])}'] = p
by_name = {}
for k in tex:
    if '/item/' in k or '/block/' in k: by_name.setdefault(k.split(':')[0] + ':' + k.rsplit('/', 1)[1][:-4], k)
def load(key):
    v = tex.get(key)
    if v is None: return None
    img = Image.open(v) if isinstance(v, Path) else Image.open(io.BytesIO(v[0].read(v[1])))
    img = img.convert('RGBA')
    if img.size[1] > img.size[0]: img = img.crop((0, 0, img.size[0], img.size[0]))  # animated strips
    return img
font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans-Bold.ttf', 11)
S = 36
lang = {}
lang.update(parse((Q / 'lang' / 'en_us.snbt').read_text()))
names = sys.argv[1:] or [f.stem for f in sorted((Q / 'chapters').glob('*.snbt'))]
allq = {}
for f in (Q / 'chapters').glob('*.snbt'):
    for q in parse(f.read_text())['quests']: allq[q['id']] = q
for name in names:
    ch = parse((Q / 'chapters' / f'{name}.snbt').read_text())
    pts = [(float(q['x'][:-1]), float(q['y'][:-1]), float(q.get('size', '1.0d')[:-1])) for q in ch['quests']]
    pts += [(float(l['x'][:-1]), float(l['y'][:-1]), 1) for l in ch.get('quest_links', [])]
    for im in ch.get('images', []):
        x, y, w, h = (float(im[k][:-1]) for k in ('x', 'y', 'width', 'height'))
        pts += [(x - w / 2, y - h / 2, 0), (x + w / 2, y + h / 2, 0)]
    x0 = min(p[0] - p[2] for p in pts) - 1; y0 = min(p[1] - p[2] for p in pts) - 1
    x1 = max(p[0] + p[2] for p in pts) + 1; y1 = max(p[1] + p[2] for p in pts) + 1
    W, H = int((x1 - x0) * S), int((y1 - y0) * S)
    img = Image.new('RGBA', (W, H), (52, 58, 66, 255)); d = ImageDraw.Draw(img)
    P = lambda x, y: ((x - x0) * S, (y - y0) * S)
    for im in ch.get('images', []):
        x, y, w, h = (float(im[k][:-1]) for k in ('x', 'y', 'width', 'height'))
        t = load(im['image'])
        if t is None: continue
        t = t.resize((max(1, int(w * S)), max(1, int(h * S))), Image.NEAREST)
        px, py = P(x - w / 2, y - h / 2); img.paste(t, (int(px), int(py)), t)
    qs = {q['id']: q for q in ch['quests']}
    for q in ch['quests']:
        if q.get('hide_dependency_lines') == 'true': continue
        for dep in q.get('dependencies', []):
            if dep in qs:
                a, b = qs[dep], q
                d.line([P(float(a['x'][:-1]), float(a['y'][:-1])), P(float(b['x'][:-1]), float(b['y'][:-1]))], fill=(200, 160, 160, 255), width=2)
    def node(x, y, size, shape, icon, label, link=False):
        r = size * S / 2; cx, cy = P(x, y)
        box = [cx - r, cy - r, cx + r, cy + r]
        col = (90, 96, 104, 255); edge = (220, 220, 220, 255) if not link else (120, 200, 255, 255)
        if shape in ('square', 'rsquare'): d.rounded_rectangle(box, 4 if shape == 'rsquare' else 0, fill=col, outline=edge, width=2)
        elif shape in ('diamond',): d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=col, outline=edge)
        elif shape in ('hexagon', 'pentagon', 'gear', 'heart', 'octagon'):
            n = {'hexagon': 6, 'pentagon': 5, 'gear': 10, 'heart': 3, 'octagon': 8}[shape]
            d.polygon([(cx + r * math.cos(-math.pi / 2 + i * 2 * math.pi / n), cy + r * math.sin(-math.pi / 2 + i * 2 * math.pi / n)) for i in range(n)], fill=col, outline=edge)
        else: d.ellipse(box, fill=col, outline=edge, width=2)
        t = None
        if icon and icon.get('id') == 'cobblemon:pokemon_model':
            sp = icon['components']['cobblemon:pokemon_item']['species'].split(':')[1]
            d.text((cx, cy), sp[:5], font=font, fill=(255, 255, 160, 255), anchor='mm')
        elif icon:
            k = by_name.get(icon['id'])
            t = load(k) if k else None
        if t is not None:
            s = int(r * 1.3); t = t.resize((max(1, s), max(1, s)), Image.NEAREST); img.paste(t, (int(cx - s / 2), int(cy - s / 2)), t)
    for q in ch['quests']:
        node(float(q['x'][:-1]), float(q['y'][:-1]), float(q.get('size', '1.0d')[:-1]), q.get('shape', 'circle'), q.get('icon'), lang.get(f'quest.{q["id"]}.title'))
    for l in ch.get('quest_links', []):
        lq = allq.get(l['linked_quest'], {})
        node(float(l['x'][:-1]), float(l['y'][:-1]), float(l.get('size', '1.0d')[:-1]), l.get('shape', 'circle'), lq.get('icon'), None, True)
    img.save(str(Path(__file__).parent / 'previews' / f'{name}.png')); print(name, img.size)
