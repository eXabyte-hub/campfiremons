#!/usr/bin/env python3
"""Numbers every chapter 0, 1, 2... within its group (order_index), keeping the current order: FTB Quests' own numbering.

FTB sorts each group's chapters by order_index and, on its first autosave after a start, rewrites every chapter file with
its position in the group (BaseQuestFile.writeChapterFiles). packwiz only replaces the files a release changes, so the
server holds a mix: its own numbers for untouched chapters, ours for changed ones. With any other numbering, a chapter we
change jumps: "Stage 0: Boulder Badge" came in as 9 among 0..8 (v0.1.45, below Stage 9), Stage 3 as 14 among 0..9
(v0.1.47, last). v0.1.46's "unique across the whole book" numbering was a wrong diagnosis; it only looked right because it
replaced every gym chapter at once. With FTB's numbering, ours and the server's always agree.
Only order_index lines change. Run it after adding, removing or moving a chapter; validate.py checks it.
    python3 tools/quest_book/renumber_chapters.py
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from snbt import parse  # noqa: E402

Q = Path(__file__).resolve().parents[2] / 'config' / 'ftbquests' / 'quests'


def main():
    groups = [g['id'] for g in parse((Q / 'chapter_groups.snbt').read_text())['chapter_groups']]
    by_group = defaultdict(list)
    for f in sorted((Q / 'chapters').glob('*.snbt')):
        ch = parse(f.read_text())
        g = ch.get('group', '')
        by_group[groups.index(g) if g in groups else len(groups)].append((int(str(ch['order_index'])), f.stem, f))
    changed = 0
    for g in sorted(by_group):
        for new, (old, name, f) in enumerate(sorted(by_group[g])):
            if old != new:
                text = f.read_text()
                text, n = re.subn(r'^\torder_index: \d+$', f'\torder_index: {new}', text, count=1, flags=re.M)
                assert n == 1, name
                f.write_text(text)
                changed += 1
            print(f'{g} {new:3} {name}' + (f'  (was {old})' if old != new else ''))
    print(f'{changed} chapters renumbered')


if __name__ == '__main__':
    main()
