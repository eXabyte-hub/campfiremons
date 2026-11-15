#!/usr/bin/env python3
"""Writes the mod list in README.md (between the modlist markers) from the pack's .pw.toml files.

Run it after adding, removing or renaming mods: `python3 tools/gen_modlist.py`. `--check` exits 1 if the README's list
is out of date (CI runs it).
"""
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
START, END = '<!-- modlist:start -->', '<!-- modlist:end -->'
SECTIONS = [('mods', 'Mods'), ('resourcepacks', 'Resource packs'), ('shaderpacks', 'Shaders'), ('datapacks', 'Data packs')]
SIDES = {'both': '', 'client': 'client only', 'server': 'server only'}


def entry(path):
    d = tomllib.loads(path.read_text())
    update = d.get('update', {})
    if 'modrinth' in update:
        url, source = f"https://modrinth.com/project/{update['modrinth']['mod-id']}", 'Modrinth'
    elif 'curseforge' in update:
        url, source = f"https://www.curseforge.com/projects/{update['curseforge']['project-id']}", 'CurseForge'
    else:
        url, source = d['download']['url'], 'direct'
    notes = [SIDES.get(d.get('side', 'both'), d.get('side', ''))]
    if d.get('option', {}).get('optional'):
        notes.append('optional')
    name = d['name'].replace('|', '\\|')
    return name.lower(), f"| [{name}]({url}) | {', '.join(n for n in notes if n)} | {source} |"


def render():
    parts, total = [], 0
    for folder, title in SECTIONS:
        rows = sorted(entry(p) for p in (ROOT / folder).glob('*.pw.toml'))
        if not rows:
            continue
        total += len(rows) if folder == 'mods' else 0
        parts.append(f'### {title} ({len(rows)})\n\n| Name | Notes | From |\n| --- | --- | --- |\n'
                     + '\n'.join(r for _, r in rows) + '\n')
    head = (f'<details>\n<summary>All {total} mods, plus resource packs and shaders (click to open)</summary>\n\n'
            'Generated from the pack files by `tools/gen_modlist.py`. "Client only" mods are only on players\' '
            'computers, "server only" ones only on the server.\n\n')
    return head + '\n'.join(parts) + '\n</details>'


def main():
    text = README.read_text()
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    new = f'{before}{START}\n{render()}\n{END}{after}'
    if '--check' in sys.argv:
        if new != text:
            print('README.md mod list is out of date: run python3 tools/gen_modlist.py')
            sys.exit(1)
        return
    README.write_text(new)


if __name__ == '__main__':
    main()
