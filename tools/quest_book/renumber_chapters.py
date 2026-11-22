#!/usr/bin/env python3
"""Gives every chapter a unique order_index, group by group, keeping the current order.

FTB Quests keeps chapters in a map keyed by order_index across the whole book, so two chapters with the same number
(even in different groups) collide and one of them drops to the bottom of its group: "Stage 0: Boulder Badge" (9,
like Paradox) ended up below Stage 9, and Gotta Find 'Em All shared 7 with Legendary. This numbers the chapters 0..n
in group order (chapter_groups.snbt), then by their current order_index, then by file name. Only order_index lines
change. Run it after adding a chapter.
    python3 tools/quest_book/renumber_chapters.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from snbt import parse  # noqa: E402

Q = Path(__file__).resolve().parents[2] / 'config' / 'ftbquests' / 'quests'


def main():
    groups = [g['id'] for g in parse((Q / 'chapter_groups.snbt').read_text())['chapter_groups']]
    chapters = []
    for f in sorted((Q / 'chapters').glob('*.snbt')):
        ch = parse(f.read_text())
        g = ch.get('group', '')
        chapters.append((groups.index(g) if g in groups else len(groups), int(str(ch['order_index'])), f.stem, f))
    changed = 0
    for new, (_, old, name, f) in enumerate(sorted(chapters)):
        if old != new:
            text = f.read_text()
            text, n = re.subn(r'^\torder_index: \d+$', f'\torder_index: {new}', text, count=1, flags=re.M)
            assert n == 1, name
            f.write_text(text)
            changed += 1
        print(f'{new:3} {name}' + (f'  (was {old})' if old != new else ''))
    print(f'{changed} chapters renumbered')


if __name__ == '__main__':
    main()
