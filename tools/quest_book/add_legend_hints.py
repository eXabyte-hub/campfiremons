#!/usr/bin/env python3
"""Where-to-find hints on the catch quests of the legendaries the pack itself gives a source (asked for on
2026-11-28): the wild spawns in tools/gen_legend_spawns.py, the Raid Dens bosses and the summon items. Writes a
quest_desc into config/ftbquests/quests/lang/en_us.snbt for every "Catchable from Stage N" quest with that title,
in place (quest IDs and progress are untouched). Re-running replaces the hints it wrote before.
Run from the repo root, then tools/quest_book/validate.py.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gen_legend_spawns import SPAWNS  # noqa: E402

LANG = Path("config/ftbquests/quests/lang/en_us.snbt")
NAMES = {"tapukoko": "Tapu Koko", "tapulele": "Tapu Lele", "tapubulu": "Tapu Bulu", "tapufini": "Tapu Fini",
         "typenull": "Type: Null"}
MARK = "&r&r"  # invisible in game; marks the hints this tool wrote, so re-runs replace them

HINTS = {NAMES.get(sp, sp.capitalize()): f"{MARK}Turns up wild, rarely: {why}." for sp, _l, _p, _c, _pct, why in SPAWNS}
HINTS.update({
    "Zygarde": f"{MARK}A ★6 Raid Den boss (Stage 7 dens).",
    "Terapagos": f"{MARK}A ★6 Raid Den boss (Stage 7 dens).",
    "Koraidon": f"{MARK}A ★6 Raid Den boss (Stage 7 dens).",
    "Miraidon": f"{MARK}A ★6 Raid Den boss (Stage 7 dens).",
    "Mewtwo": f"{MARK}A ★7 Raid Den boss (Stage 8 dens).",
    "Necrozma": f"{MARK}A ★7 Raid Den boss (Stage 8 dens).",
    "Magearna": f"{MARK}Build a &eSoul-Heart&r in a Create Mechanical Crafter and use it to summon Magearna.",
    "Genesect": f"{MARK}Build a &eGenesect Drive&r in a Create Mechanical Crafter and use it to summon Genesect.",
    "Pecharunt": f"{MARK}Mix a &ePoisoned Mochi&r (Potato Mochi, a Poisonous Potato and a Fermented Spider Eye, "
                 f"heated) and use it to summon Pecharunt.",
    "Type: Null": f"{MARK}Buy a &eBeast Memory&r in the Battle Tower's BP shop and use it to summon Type: Null.",
    "Silvally": f"{MARK}Evolve a Type: Null with high friendship.",
    "Rayquaza": f"{MARK}Catchable only after the Champion. Very rare: high in the outer End, on the roofs of End City towers. A &eJade Orb&r "
                f"(Dragon's Breath, a Dragon Head, a Nether Star, an Elytra and emerald blocks) used up there "
                f"calls it, but only 1 time in 4, and the orb is used up either way.",
})


def main():
    text = LANG.read_text(encoding="utf-8")
    titles = dict(re.findall(r'\tquest\.([0-9A-F]{16})\.title: "([^"]*)"', text))
    subs = dict(re.findall(r'\tquest\.([0-9A-F]{16})\.quest_subtitle: "([^"]*)"', text))
    done = 0
    for qid, title in titles.items():
        if title not in HINTS or not subs.get(qid, "").startswith("Catchable from Stage"):
            continue
        line = f'\tquest.{qid}.quest_desc: ["{HINTS[title]}"]\n'
        pat = re.compile(rf'\tquest\.{qid}\.quest_desc: \[.*?\]\n', re.S)
        if pat.search(text):
            if MARK not in pat.search(text).group(0):
                print(f"skipped {title} ({qid}): it already has its own description")
                continue
            text = pat.sub(line.replace('\\', '\\\\'), text, count=1)
        else:
            text = text.replace(f'\tquest.{qid}.quest_subtitle:', line + f'\tquest.{qid}.quest_subtitle:', 1)
        done += 1
    LANG.write_text(text, encoding="utf-8")
    missing = sorted(set(HINTS) - {titles[q] for q in titles if titles[q] in HINTS})
    print(f"{done} quest hints written" + (f"; no quest for {missing}" if missing else ""))


if __name__ == "__main__":
    main()
