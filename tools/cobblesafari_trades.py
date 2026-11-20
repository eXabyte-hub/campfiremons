#!/usr/bin/env python3
"""Keeps CobbleSafari's trades inside our tier locks (DESIGN.md, CobbleSafari row).

Wonder Trade and the GTS's NPC offers hand their Pokemon straight to the party, so they would skip our tier locks,
which act on the ball hit. This writes overrides into kubejs/data/cobblesafari/:
- Wonder Trade pools (`wonder_trade/pokemon_groups/`): the rare pools (legendaries, mythical, paradox, ultrabeast
  and their _vanilla twins) get our own lists of rare non-legendaries, so the events built on them still run;
  every other pool is copied without the tier-locked species.
- GTS NPC offers (`gts/unique_offers/`): an offer that gives a tier-locked Pokemon for one of a lower tier asks for
  the same species instead, like most of its legendary offers already do.
Files that need no change are skipped. Tiers follow config.js (`tiers`, `labelRules`, `overrides`).

Run it again after updating CobbleSafari or Cobblemon:
  python3 -I tools/cobblesafari_trades.py <cobblesafari jar> <Cobblemon jar>
"""
import json
import os
import sys
import zipfile

# config.js labelRules (first match wins) with each tier's unlock stage, and its per-species overrides
LABEL_STAGES = [('restricted', 7), ('mythical', 7), ('ultra_beast', 6), ('paradox', 6), ('legendary', 5)]
SPECIES_STAGES = {'arceus': 7}
PSEUDO = ['dratini', 'larvitar', 'bagon', 'beldum', 'gible', 'deino', 'goomy', 'jangmoo', 'dreepy']
FAVOURITES = ['eevee', 'riolu', 'larvesta', 'zorua', 'axew', 'togepi', 'munchlax', 'happiny', 'mimikyu', 'rotom']
FOSSILS = ['omanyte', 'kabuto', 'aerodactyl', 'lileep', 'anorith', 'cranidos', 'shieldon', 'tirtouga', 'archen',
           'tyrunt', 'amaura']
ALOLA = ['rockruff', 'wimpod', 'dhelmise', 'minior', 'komala', 'bruxish', 'drampa', 'turtonator', 'togedemaru',
         'salandit']
REPLACE = {
    'legendaries': PSEUDO, 'legendaries_vanilla': PSEUDO,
    'mythical': FAVOURITES, 'mythical_vanilla': FAVOURITES,
    'paradox': FOSSILS,
    'ultrabeast': ALOLA, 'ultrabeast_vanilla': ALOLA,
}
DATA = 'data/cobblesafari/'
GROUPS = DATA + 'wonder_trade/pokemon_groups/'
OFFERS = DATA + 'gts/unique_offers/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kubejs')


def load_species(cobblemon_jar):
    labels, implemented = {}, set()
    with zipfile.ZipFile(cobblemon_jar) as z:
        for name in z.namelist():
            if name.startswith('data/cobblemon/species/') and name.endswith('.json'):
                j = json.loads(z.read(name))
                sid = os.path.basename(name)[:-5]
                labels[sid] = set(j.get('labels', []))
                if j.get('implemented'):
                    implemented.add(sid)
    return labels, implemented


def main(safari_jar, cobblemon_jar):
    labels, implemented = load_species(cobblemon_jar)

    def stage(spec):  # 'moltres galarian' or 'hooh level=1 ...' -> unlock stage, 0 if never locked
        sid = spec.split()[0]
        if sid in SPECIES_STAGES:
            return SPECIES_STAGES[sid]
        return next((st for label, st in LABEL_STAGES if label in labels.get(sid, set())), 0)

    def write(name, j):
        path = os.path.join(OUT, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(json.dumps(j, indent=2) + '\n')

    for group, pop in REPLACE.items():
        for s in pop:
            assert s in implemented and not stage(s), f'{group}: {s} is locked or not implemented'
    with zipfile.ZipFile(safari_jar) as z:
        for name in sorted(z.namelist()):
            if not name.endswith('.json'):
                continue
            base = os.path.basename(name)[:-5]
            if name.startswith(GROUPS):
                j = json.loads(z.read(name))
                pop = j['population']
                new = REPLACE.get(base) or [p for p in pop if not stage(p)]
                if new != pop:
                    j['population'] = new
                    write(name, j)
                    print(f'wonder trade {base}: {len(pop)} -> {len(new)}')
            elif name.startswith(OFFERS):
                j = json.loads(z.read(name))
                given, wish = j['given'].split()[0], j['wish']
                if stage(given) > stage(wish['species']):
                    print(f'gts {base}: {given} for {wish["species"]} -> for {given}')
                    wish['species'] = given
                    write(name, j)


if __name__ == '__main__':
    main(*sys.argv[1:3])
