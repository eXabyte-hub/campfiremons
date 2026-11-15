#!/usr/bin/env python3
"""Hover text for the type icons in the quest book (the tera_types images in Getting Started and the gym chapters).

FTB Quests 2101 shows an image's title as its tooltip, from `image.<id>.title` in lang/en_us.snbt. This writes one per
type icon from the type chart below (the main-series chart since Gen 6, which Cobblemon uses), so attacking and
defending matchups always agree. FTB only notices the mouse over an image that has a click action (unless you're
editing the book), so each icon also opens its Bulbapedia type page when clicked; without one the tooltips never
showed (v0.1.15). Re-run after adding type icons: `python3 tools/quest_book/type_tooltips.py`.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from snbt import parse, dump  # noqa: E402

Q = Path(__file__).resolve().parents[2] / 'config' / 'ftbquests' / 'quests'
LANG = Q / 'lang' / 'en_us.snbt'

TYPES = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic',
         'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
# attacking type -> (super effective on, not very effective on, no effect on)
CHART = {
    'normal': ([], ['rock', 'steel'], ['ghost']),
    'fire': (['grass', 'ice', 'bug', 'steel'], ['fire', 'water', 'rock', 'dragon'], []),
    'water': (['fire', 'ground', 'rock'], ['water', 'grass', 'dragon'], []),
    'electric': (['water', 'flying'], ['electric', 'grass', 'dragon'], ['ground']),
    'grass': (['water', 'ground', 'rock'], ['fire', 'grass', 'poison', 'flying', 'bug', 'dragon', 'steel'], []),
    'ice': (['grass', 'ground', 'flying', 'dragon'], ['fire', 'water', 'ice', 'steel'], []),
    'fighting': (['normal', 'ice', 'rock', 'dark', 'steel'], ['poison', 'flying', 'psychic', 'bug', 'fairy'], ['ghost']),
    'poison': (['grass', 'fairy'], ['poison', 'ground', 'rock', 'ghost'], ['steel']),
    'ground': (['fire', 'electric', 'poison', 'rock', 'steel'], ['grass', 'bug'], ['flying']),
    'flying': (['grass', 'fighting', 'bug'], ['electric', 'rock', 'steel'], []),
    'psychic': (['fighting', 'poison'], ['psychic', 'steel'], ['dark']),
    'bug': (['grass', 'psychic', 'dark'], ['fire', 'fighting', 'poison', 'flying', 'ghost', 'steel', 'fairy'], []),
    'rock': (['fire', 'ice', 'flying', 'bug'], ['fighting', 'ground', 'steel'], []),
    'ghost': (['psychic', 'ghost'], ['dark'], ['normal']),
    'dragon': (['dragon'], ['steel'], ['fairy']),
    'dark': (['psychic', 'ghost'], ['fighting', 'dark', 'fairy'], []),
    'steel': (['ice', 'rock', 'fairy'], ['fire', 'water', 'electric', 'steel'], []),
    'fairy': (['fighting', 'dragon', 'dark'], ['fire', 'poison', 'steel'], []),
}
COLOR = {'normal': 'f', 'fire': 'c', 'water': '9', 'electric': 'e', 'grass': 'a', 'ice': 'b', 'fighting': '4',
         'poison': '5', 'ground': '6', 'flying': 'b', 'psychic': 'd', 'bug': '2', 'rock': '6', 'ghost': '5',
         'dragon': '9', 'dark': '8', 'steel': '7', 'fairy': 'd'}
STELLAR = ['&d&lStellar&r &7(Terastal only)',
           'A Stellar Tera Pokémon keeps its own types when hit.',
           'The first move of each type it uses gets a one-time power boost.',
           'Its Tera Blast is super effective on Terastallized Pokémon.',
           '&8Click for its Bulbapedia page']


def names(types):
    return ', '.join(t.capitalize() for t in types)


def tooltip(t):
    if t == 'stellar':
        return STELLAR
    strong, weak, none = CHART[t]
    weak_to = [a for a in TYPES if t in CHART[a][0]]
    resists = [a for a in TYPES if t in CHART[a][1]]
    immune = [a for a in TYPES if t in CHART[a][2]]
    lines = [f'&{COLOR[t]}&l{t.capitalize()} type', '&7Attacking:']
    lines.append(f'&a  Strong against:&r {names(strong) or "nothing"}')
    lines.append(f'&c  Weak against:&r {names(weak)}' + (f' &8(no effect on {names(none)})&r' if none else ''))
    lines.append('&7Defending:')
    lines.append(f'&c  Weak to:&r {names(weak_to)}')
    lines.append(f'&a  Resists:&r {names(resists) or "nothing"}' + (f' &8(immune to {names(immune)})&r' if immune else ''))
    return lines + CLICK


CLICK = ['&8Click for its Bulbapedia page']


def link(t):
    return f'open_uri:https://bulbapedia.bulbagarden.net/wiki/{t.capitalize()}_(type)'


def snbt_string(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main():
    # sanity: every type in the chart, and the chart's known totals (Gen 6+: 51 super effective, 61 resisted, 8 immune)
    assert set(CHART) == set(TYPES)
    assert [sum(len(CHART[t][i]) for t in TYPES) for i in range(3)] == [51, 61, 8]
    titles = {}
    for f in sorted((Q / 'chapters').glob('*.snbt')):
        text = f.read_text()
        chapter = parse(text)
        for im in chapter.get('images', []):
            m = re.search(r'tera_types/(\w+)\.png$', im['image'])
            if m:
                titles[f'image.{im["id"]}.title'] = '\\n'.join(tooltip(m.group(1)))  # FTB splits titles on \n
                im['click_action'] = link(m.group(1))
        if dump(chapter) + '\n' != text:
            f.write_text(dump(chapter) + '\n')
    text = LANG.read_text()
    lines = [l for l in text.splitlines() if not re.match(r'\timage\.[0-9A-F]{16}\.title: ', l)]
    first_quest = next(i for i, l in enumerate(lines) if l.startswith('\tquest.'))
    block = [f'\t{k}: {snbt_string(v)}' for k, v in sorted(titles.items())]
    LANG.write_text('\n'.join(lines[:first_quest] + block + lines[first_quest:]) + '\n')
    print(f'{len(titles)} type icon tooltips')


if __name__ == '__main__':
    main()
